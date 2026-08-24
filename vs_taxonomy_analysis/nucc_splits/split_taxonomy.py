#!/usr/bin/env python3
"""
split_taxonomy.py
-----------------
Reads nucc_taxonomy_recent.csv and splits individual-provider rows into
four focused CSV files:

  physicians_osteopathic_allopathic.csv  – Allopathic & Osteopathic Physicians
  physician_assistants.csv               – Physician Assistants (PA grouping)
  nurse_practitioners.csv                – Nurse Practitioners (PA grouping)
  other_individual.csv                   – All other Individual-section rows

Rows where Section == "Non-Individual" are skipped entirely.

Column layout of the source file (0-indexed):
  0  Code
  1  Grouping          ← primary split key
  2  Classification    ← secondary split key (PA vs NP)
  3  Specialization
  4  Definition
  5  Notes
  6  Display Name
  7  Section           ← "Individual" vs "Non-Individual"
"""

import csv
import pathlib

# ── Paths ──────────────────────────────────────────────────────────────────────
HERE = pathlib.Path(__file__).parent
SOURCE = HERE / "nucc_taxonomy_recent.csv"

OUT_PHYSICIANS   = HERE / "physicians_osteopathic_allopathic.csv"
OUT_PA           = HERE / "physician_assistants.csv"
OUT_NP           = HERE / "nurse_practitioners.csv"
OUT_OTHER        = HERE / "other_individual.csv"

# ── Grouping / Classification constants ───────────────────────────────────────
GROUPING_PHYSICIANS = "Allopathic & Osteopathic Physicians"
GROUPING_PA_NP      = "Physician Assistants & Advanced Practice Nursing Providers"
CLASS_PA            = "Physician Assistant"
CLASS_NP            = "Nurse Practitioner"
SECTION_INDIVIDUAL  = "Individual"

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    with (
        open(SOURCE,        newline="", encoding="utf-8-sig") as src,
        open(OUT_PHYSICIANS, "w", newline="", encoding="utf-8") as f_phys,
        open(OUT_PA,         "w", newline="", encoding="utf-8") as f_pa,
        open(OUT_NP,         "w", newline="", encoding="utf-8") as f_np,
        open(OUT_OTHER,      "w", newline="", encoding="utf-8") as f_other,
    ):
        reader = csv.reader(src)
        header = next(reader)          # preserve header row in every output file

        writers = {
            "physicians": csv.writer(f_phys),
            "pa":         csv.writer(f_pa),
            "np":         csv.writer(f_np),
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

            # Route to the appropriate output file
            if grouping == GROUPING_PHYSICIANS:
                writers["physicians"].writerow(row)
                counts["physicians"] += 1

            elif grouping == GROUPING_PA_NP and classification == CLASS_PA:
                writers["pa"].writerow(row)
                counts["pa"] += 1

            elif grouping == GROUPING_PA_NP and classification == CLASS_NP:
                writers["np"].writerow(row)
                counts["np"] += 1

            else:
                writers["other"].writerow(row)
                counts["other"] += 1

    # ── Summary ────────────────────────────────────────────────────────────────
    print("Split complete:")
    print(f"  {counts['physicians']:>4} rows → {OUT_PHYSICIANS.name}")
    print(f"  {counts['pa']:>4} rows → {OUT_PA.name}")
    print(f"  {counts['np']:>4} rows → {OUT_NP.name}")
    print(f"  {counts['other']:>4} rows → {OUT_OTHER.name}")
    total = sum(counts.values())
    print(f"  {total:>4} individual rows written in total")


if __name__ == "__main__":
    main()
