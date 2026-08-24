#!/usr/bin/env python3
"""
split_nonphysician.py
---------------------
Reads NonPhysicianUsingPhysicianTaxonomy.csv and splits rows into five files
based on the facetCredentialName column, using regex matching.

Output files (written to the same directory as this script):
  NursePractitioners.csv   – credential name contains BOTH "nurse" AND "practi(c)tioner"
  PhysicianAssistants.csv  – credential name contains "physician assistant"
                             (NP rule wins if both match; also catches
                              "Master of Physician Assistant Studies")
  OtherNurses.csv          – credential name contains "nurs" (but not already NP)
  MasterOf.csv             – credential name starts with "master" (but not already
                             caught by NP, PA, or OtherNurse)
  AllOthers.csv            – everything that doesn't match any rule above

Priority (applied in order, first match wins):
  1. NursePractitioners
  2. PhysicianAssistants
  3. OtherNurses
  4. MasterOf
  5. AllOthers

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

# ── Paths ───────────────────────────────────────────────────────────────────
HERE   = pathlib.Path(__file__).parent
SOURCE = HERE / "NonPhysicianUsingPhysicianTaxonomy.csv"

OUT_NP     = HERE / "NursePractitioners.csv"
OUT_PA     = HERE / "PhysicianAssistants.csv"
OUT_NURSE  = HERE / "OtherNurses.csv"
OUT_MASTER = HERE / "MasterOf.csv"
OUT_OTHER  = HERE / "AllOthers.csv"

# ── Compiled patterns ────────────────────────────────────────────────────────
# NP: name must contain BOTH "nurse" and "practi(c)tioner" (handles typos/variants)
RE_NURSE      = re.compile(r'nurs',             re.IGNORECASE)
RE_PRACTIONER = re.compile(r'practi[ct]ioner',  re.IGNORECASE)
RE_PA         = re.compile(r'physician\s+assistant', re.IGNORECASE)
RE_MASTER     = re.compile(r'^masters?\b',       re.IGNORECASE)


def classify(name: str) -> str:
    """Return the bucket name for a given facetCredentialName."""
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


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    with (
        open(SOURCE,     newline="", encoding="utf-8-sig") as src,
        open(OUT_NP,     "w", newline="", encoding="utf-8") as f_np,
        open(OUT_PA,     "w", newline="", encoding="utf-8") as f_pa,
        open(OUT_NURSE,  "w", newline="", encoding="utf-8") as f_nurse,
        open(OUT_MASTER, "w", newline="", encoding="utf-8") as f_master,
        open(OUT_OTHER,  "w", newline="", encoding="utf-8") as f_other,
    ):
        reader = csv.reader(src)
        header = next(reader)

        writers = {
            "np":     csv.writer(f_np),
            "pa":     csv.writer(f_pa),
            "nurse":  csv.writer(f_nurse),
            "master": csv.writer(f_master),
            "other":  csv.writer(f_other),
        }
        for w in writers.values():
            w.writerow(header)

        counts = {k: 0 for k in writers}

        for row in reader:
            if len(row) < 2:
                continue

            name   = row[1].strip()
            bucket = classify(name)
            writers[bucket].writerow(row)
            counts[bucket] += 1

    # ── Summary ──────────────────────────────────────────────────────────────
    labels = {
        "np":     OUT_NP.name,
        "pa":     OUT_PA.name,
        "nurse":  OUT_NURSE.name,
        "master": OUT_MASTER.name,
        "other":  OUT_OTHER.name,
    }
    print("Split complete:")
    for key, fname in labels.items():
        print(f"  {counts[key]:>5} rows → {fname}")
    print(f"  {sum(counts.values()):>5} total rows written")


if __name__ == "__main__":
    main()
