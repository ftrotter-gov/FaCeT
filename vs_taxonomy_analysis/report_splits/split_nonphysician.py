#!/usr/bin/env python3
"""
split_nonphysician.py
---------------------
Reads NonPhysicianUsingPhysicianTaxonomy.csv and splits rows into five files
based on the facetCredentialName column, using regex matching.

Output files (written to the same directory as this script):
  LegitimatePairs.csv      – credential/taxonomy pairings that are CORRECT despite the
                             taxonomy code sitting in the physician grouping (e.g. a
                             DDS/DMD using 204E00000X Oral & Maxillofacial Surgery).
                             Removed from the mismatch report entirely.
  MisdecodedCredentials.csv – rows where FaCeT expanded the credential ABBREVIATION to
                             the wrong profession (e.g. "AA" → "Associate of Arts" when
                             these are Anesthesiologist Assistants). The provider's
                             taxonomy choice is fine; the credential dictionary is wrong.
                             Requires an upstream fix, not a taxonomy remap.
  NursePractitioners.csv   – credential name contains BOTH "nurse" AND "practi(c)tioner"
  PhysicianAssistants.csv  – credential name contains "physician assistant"
                             (NP rule wins if both match; also catches
                              "Master of Physician Assistant Studies")
  OtherNurses.csv          – credential name contains "nurs" (but not already NP)
  MasterOf.csv             – credential name starts with "master" (but not already
                             caught by NP, PA, or OtherNurse)
  AllOthers.csv            – everything that doesn't match any rule above

Priority (applied in order, first match wins):
  0.  LegitimatePairs       ← checked FIRST so valid pairings never reach the report
  0.5 MisdecodedCredentials ← credential-dictionary defects, not taxonomy defects
  1. NursePractitioners
  2. PhysicianAssistants
  3. OtherNurses
  4. MasterOf
  5. AllOthers

Annotation preservation
-----------------------
Three of the output files carry hand-authored analysis columns (should_use_tax,
should_use_tax_description, match_strength) that are NOT derivable from the source.
Re-running this script previously destroyed that work. It now reads any existing
output files first, keys the annotations by (facetCredentialCode, chosenTaxonomyCode),
and writes them back out. That key is unique across all 4,459 source rows.

Source columns:
  0  facetCredentialCode
  1  facetCredentialName   ← matching key
  2  chosenTaxonomyCode
  3  chosenTaxonomyDescription
  4  providerCount
"""

import csv
import pathlib
import re

from legitimate_pairs import is_legitimate_pair
from misdecoded_credentials import is_confirmed_misdecode, lookup as lookup_misdecode

# ── Paths ───────────────────────────────────────────────────────────────────
HERE   = pathlib.Path(__file__).parent
SOURCE = HERE / "NonPhysicianUsingPhysicianTaxonomy.csv"

OUT_LEGIT  = HERE / "LegitimatePairs.csv"
OUT_MISDEC = HERE / "MisdecodedCredentials.csv"
OUT_NP     = HERE / "NursePractitioners.csv"
OUT_PA     = HERE / "PhysicianAssistants.csv"
OUT_NURSE  = HERE / "OtherNurses.csv"
OUT_MASTER = HERE / "MasterOf.csv"
OUT_OTHER  = HERE / "AllOthers.csv"

# Hand-authored columns that must survive regeneration.
ANNOTATION_COLUMNS = [
    "should_use_tax",
    "should_use_tax_description",
    "match_strength",
]

# Extra diagnostic columns, written only to MisdecodedCredentials.csv.
MISDECODE_COLUMNS = [
    "current_credential_name",
    "corrected_credential_name",
]

# ── Compiled patterns ────────────────────────────────────────────────────────
# NP: name must contain BOTH "nurse" and "practi(c)tioner" (handles typos/variants)
RE_NURSE      = re.compile(r'nurs',             re.IGNORECASE)
RE_PRACTIONER = re.compile(r'practi[ct]ioner',  re.IGNORECASE)
RE_PA         = re.compile(r'physician\s+assistant', re.IGNORECASE)
RE_MASTER     = re.compile(r'^masters?\b',       re.IGNORECASE)


def classify(name: str, code: str = "", taxonomy_code: str = "",
             taxonomy_description: str = "") -> str:
    """
    Return the bucket name for a given credential row.

    Args:
        name:                 facetCredentialName (primary matching key).
        code:                 facetCredentialCode, used for the pair/misdecode checks.
        taxonomy_code:        chosenTaxonomyCode, used for the legitimate-pair check.
        taxonomy_description: chosenTaxonomyDescription, corroborates a misdecode.
    """
    # Rule 0 – Correct pairings are pulled out BEFORE any mismatch bucketing, so a
    # DDS/DMD legitimately using Oral & Maxillofacial Surgery is never reported as
    # an error. See legitimate_pairs.py.
    if is_legitimate_pair(code, name, taxonomy_code):
        return "legit"

    # Rule 0.5 – The credential itself is decoded wrong (e.g. "AA" expanded to
    # "Associate of Arts" when these providers are Anesthesiologist Assistants).
    # The provider's taxonomy choice is fine; FaCeT's credential dictionary is not.
    # Routing these separately keeps a *credential* defect out of a *taxonomy* report.
    # Only corroborated rows divert -- see misdecoded_credentials.py.
    if is_confirmed_misdecode(code, taxonomy_description):
        return "misdec"

    # Rule 1 – Nurse Practitioner (both words must appear anywhere in the name)
    if RE_NURSE.search(name) and RE_PRACTIONER.search(name):
        return "np"

    # Rule 2 – Physician Assistant
    if RE_PA.search(name):
        return "pa"

    # Rule 3 – Any other nurse / nursing credential
    if RE_NURSE.search(name):
        return "nurse"

    # Rule 4 – Master-of / Masters degree credentials
    if RE_MASTER.search(name):
        return "master"

    # Rule 5 – Everything else
    return "other"


OUTPUTS = {
    "legit":  OUT_LEGIT,
    "misdec": OUT_MISDEC,
    "np":     OUT_NP,
    "pa":     OUT_PA,
    "nurse":  OUT_NURSE,
    "master": OUT_MASTER,
    "other":  OUT_OTHER,
}

# Canonical source columns (the source file's own header quoting is inconsistent,
# so we normalise it here rather than propagating it into every output file).
BASE_HEADER = [
    "facetCredentialCode",
    "facetCredentialName",
    "chosenTaxonomyCode",
    "chosenTaxonomyDescription",
    "providerCount",
]


def load_existing_annotations() -> dict[tuple[str, str], list[str]]:
    """
    Read any existing output files and return previously-authored annotations keyed by
    (facetCredentialCode, chosenTaxonomyCode).

    These columns are hand-authored analysis that cannot be regenerated from the source
    data, so they must survive a re-run. The key is unique across all source rows.
    """
    saved: dict[tuple[str, str], list[str]] = {}

    for path in OUTPUTS.values():
        if not path.exists():
            continue
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            if not reader.fieldnames:
                continue
            if not any(col in reader.fieldnames for col in ANNOTATION_COLUMNS):
                continue  # file has no annotations to preserve

            for row in reader:
                values = [(row.get(col) or "").strip() for col in ANNOTATION_COLUMNS]
                if not any(values):
                    continue  # nothing worth keeping
                key = (
                    (row.get("facetCredentialCode") or "").strip(),
                    (row.get("chosenTaxonomyCode") or "").strip(),
                )
                saved[key] = values

    return saved


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    # Capture prior analysis BEFORE truncating any output file.
    saved = load_existing_annotations()
    header = BASE_HEADER + ANNOTATION_COLUMNS

    handles = {
        key: open(path, "w", newline="", encoding="utf-8")
        for key, path in OUTPUTS.items()
    }
    try:
        writers = {key: csv.writer(fh) for key, fh in handles.items()}
        for key, w in writers.items():
            # The misdecode file carries two extra diagnostic columns recording what
            # the credential is currently called vs. what it actually means, so the
            # upstream dictionary fix is actionable straight from the file.
            w.writerow(header + MISDECODE_COLUMNS if key == "misdec" else header)

        counts = {key: 0 for key in writers}
        providers = {key: 0 for key in writers}
        restored = 0

        with open(SOURCE, newline="", encoding="utf-8-sig") as src:
            reader = csv.reader(src)
            next(reader)  # discard source header; we emit a normalised one

            for row in reader:
                if len(row) < 5:
                    continue

                code, name, tax_code = row[0].strip(), row[1].strip(), row[2].strip()
                tax_desc = row[3].strip()
                bucket = classify(name, code, tax_code, tax_desc)

                annotations = saved.get((code, tax_code))
                if annotations:
                    restored += 1
                else:
                    annotations = [""] * len(ANNOTATION_COLUMNS)

                if bucket == "misdec":
                    # The correction is known and evidence-backed, so populate the ETL
                    # target directly rather than leaving it for manual annotation.
                    entry = lookup_misdecode(code)
                    writers[bucket].writerow(
                        row[:5]
                        + [entry.correct_taxonomy, entry.correct_taxonomy_name, "3"]
                        + [entry.wrong_name, entry.correct_name]
                    )
                else:
                    writers[bucket].writerow(row[:5] + annotations)
                counts[bucket] += 1
                try:
                    providers[bucket] += int(row[4])
                except ValueError:
                    pass
    finally:
        for fh in handles.values():
            fh.close()

    # ── Summary ──────────────────────────────────────────────────────────────
    notes = {
        "legit":  "  (correct pairings, excluded from mismatch report)",
        "misdec": "  (credential decoded wrong — fix upstream, not a taxonomy error)",
    }
    print("Split complete:")
    for key, path in OUTPUTS.items():
        print(f"  {counts[key]:>5} rows / {providers[key]:>6} providers → "
              f"{path.name}{notes.get(key, '')}")
    print(f"  {sum(counts.values()):>5} rows / {sum(providers.values()):>6} providers total")
    print(f"  {restored} row(s) had prior annotations restored")

    excluded = {"legit", "misdec"}
    mismatch_rows = sum(c for k, c in counts.items() if k not in excluded)
    mismatch_prov = sum(p for k, p in providers.items() if k not in excluded)
    print(f"\nActual taxonomy mismatches to remediate: "
          f"{mismatch_rows} rows / {mismatch_prov} providers")


if __name__ == "__main__":
    main()
