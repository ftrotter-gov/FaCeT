#!/usr/bin/env python3
"""
split_taxonomy.py
-----------------
Reads nucc_taxonomy_recent.csv and splits individual-provider rows into
five focused CSV files:

  physicians_osteopathic_allopathic.csv  – Allopathic & Osteopathic Physicians
  physician_assistants.csv               – Physician Assistants (PA grouping)
  nurse_practitioners.csv                – Nurse Practitioners (NP grouping)
  masters_degree_providers.csv           – Roles that explicitly require a
                                           master's degree (cross-cutting across
                                           groupings; detected from definition
                                           text and classification name)
  other_individual.csv                   – All remaining Individual-section rows

Rows where Section == "Non-Individual" are skipped entirely.

Master's-degree detection rules (applied only after physicians/PA/NP routing):
  1. The Definition or Notes column contains the phrase "master's degree"
     (case-insensitive).  This is intentionally specific to avoid false
     positives such as "master's level performers" (athletes).
  2. The Classification column contains ", MS" or ", M.S." — the NUCC's own
     convention for signalling a master's-level classification (e.g.
     "Genetic Counselor, MS").

Column layout of the source file (0-indexed):
  0  Code
  1  Grouping          ← primary split key
  2  Classification    ← secondary split key (PA vs NP); also checked for ", MS"
  3  Specialization
  4  Definition        ← scanned for master's-degree language
  5  Notes             ← scanned for master's-degree language
  6  Display Name
  7  Section           ← "Individual" vs "Non-Individual"
"""

import csv
import pathlib
import re

# ── Paths ──────────────────────────────────────────────────────────────────────
HERE = pathlib.Path(__file__).parent
SOURCE = HERE / "nucc_taxonomy_recent.csv"

OUT_PHYSICIANS = HERE / "physicians_osteopathic_allopathic.csv"
OUT_PA         = HERE / "physician_assistants.csv"
OUT_NP         = HERE / "nurse_practitioners.csv"
OUT_MASTERS    = HERE / "masters_degree_providers.csv"
OUT_OTHER      = HERE / "other_individual.csv"

# ── Grouping / Classification constants ───────────────────────────────────────
GROUPING_PHYSICIANS = "Allopathic & Osteopathic Physicians"
GROUPING_PA_NP      = "Physician Assistants & Advanced Practice Nursing Providers"
CLASS_PA            = "Physician Assistant"
CLASS_NP            = "Nurse Practitioner"
SECTION_INDIVIDUAL  = "Individual"

# ── Master's-degree detection patterns ────────────────────────────────────────
# Rule 1: definition/notes text explicitly states a master's degree requirement.
# Using the two-word phrase "master's degree" keeps this precise and avoids
# false positives (e.g. "master's level performers" in sports-medicine text).
RE_MASTERS_DEGREE = re.compile(r"master'?s\s+degree", re.IGNORECASE)

# Rule 2: NUCC classification-column convention for master's-level roles
# (e.g. "Genetic Counselor, MS" or "Genetic Counselor, M.S.").
RE_MASTERS_CLASS = re.compile(r",\s*M\.?S\.?$", re.IGNORECASE)


def _is_masters_level(row: list[str]) -> bool:
    """
    Return True when a taxonomy row represents a role that explicitly requires
    a master's degree, based on its definition/notes text or classification name.

    Args:
        row: A single CSV row from nucc_taxonomy_recent.csv (at least 6 columns).

    Returns:
        True if the row matches either master's-degree detection rule.
    """
    classification = row[2] if len(row) > 2 else ""
    definition     = row[4] if len(row) > 4 else ""
    notes          = row[5] if len(row) > 5 else ""

    # Rule 1 – explicit "master's degree" phrase in the free-text fields
    if RE_MASTERS_DEGREE.search(definition) or RE_MASTERS_DEGREE.search(notes):
        return True

    # Rule 2 – NUCC classification name ends with ", MS" / ", M.S."
    if RE_MASTERS_CLASS.search(classification):
        return True

    return False

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    with (
        open(SOURCE,         newline="", encoding="utf-8-sig") as src,
        open(OUT_PHYSICIANS, "w", newline="", encoding="utf-8") as f_phys,
        open(OUT_PA,         "w", newline="", encoding="utf-8") as f_pa,
        open(OUT_NP,         "w", newline="", encoding="utf-8") as f_np,
        open(OUT_MASTERS,    "w", newline="", encoding="utf-8") as f_masters,
        open(OUT_OTHER,      "w", newline="", encoding="utf-8") as f_other,
    ):
        reader = csv.reader(src)
        header = next(reader)          # preserve header row in every output file

        writers = {
            "physicians": csv.writer(f_phys),
            "pa":         csv.writer(f_pa),
            "np":         csv.writer(f_np),
            "masters":    csv.writer(f_masters),
            "other":      csv.writer(f_other),
        }
        for w in writers.values():
            w.writerow(header)

        counts = {k: 0 for k in writers}

        for row in reader:
            # Guard against short / blank rows
            if len(row) < 8:
                continue

            grouping       = row[1].strip()
            classification = row[2].strip()
            section        = row[7].strip()

            # Skip Non-Individual entirely
            if section != SECTION_INDIVIDUAL:
                continue

            # ── Route to the appropriate output file ──────────────────────────
            # Physicians take priority first, then PA/NP sub-groupings.
            # Master's-degree detection is applied to everything that falls
            # outside those three buckets, so that physicians / PAs / NPs with
            # incidental master's-level language are not misrouted.
            if grouping == GROUPING_PHYSICIANS:
                writers["physicians"].writerow(row)
                counts["physicians"] += 1

            elif grouping == GROUPING_PA_NP and classification == CLASS_PA:
                writers["pa"].writerow(row)
                counts["pa"] += 1

            elif grouping == GROUPING_PA_NP and classification == CLASS_NP:
                writers["np"].writerow(row)
                counts["np"] += 1

            elif _is_masters_level(row):
                writers["masters"].writerow(row)
                counts["masters"] += 1

            else:
                writers["other"].writerow(row)
                counts["other"] += 1

    # ── Summary ────────────────────────────────────────────────────────────────
    print("Split complete:")
    print(f"  {counts['physicians']:>4} rows → {OUT_PHYSICIANS.name}")
    print(f"  {counts['pa']:>4} rows → {OUT_PA.name}")
    print(f"  {counts['np']:>4} rows → {OUT_NP.name}")
    print(f"  {counts['masters']:>4} rows → {OUT_MASTERS.name}")
    print(f"  {counts['other']:>4} rows → {OUT_OTHER.name}")
    total = sum(counts.values())
    print(f"  {total:>4} individual rows written in total")


if __name__ == "__main__":
    main()
