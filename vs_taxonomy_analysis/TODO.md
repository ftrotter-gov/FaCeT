# TODO — vs_taxonomy_analysis

Open items identified from reviewing the current state of the analysis.

## 1. Finish the two unanalyzed buckets (21,810 providers, ~31% of the data)

`split_nonphysician.py` produces five files, but only three have been annotated with
`should_use_tax` / `should_use_tax_description` / `match_strength`.

- [ ] **`OtherNurses.csv`** — 793 rows / 8,020 providers, no annotation columns at all.
- [ ] **`AllOthers.csv`** — 1,324 rows / 13,790 providers, no annotation columns at all.
- [ ] Update the "47,504 provider records reviewed" figure in `CredTaxonomyDiscussion.md`
      once these are done (true total is 69,314).

## 2. Easy ETL wins sitting in those unanalyzed files

These have exact, unambiguous NUCC codes that already exist — arguably cleaner
remaps than some rows already annotated:

- [ ] Physical Therapist family → `225100000X` (PT) / `225200000X` (PT Assistant) — **5,967 providers**
      currently pointing at `208100000X PHYSICAL MEDICINE & REHABILITATION PHYSICIAN`.
- [ ] `CRNA` Certified Registered Nurse Anesthetist → `367500000X` — **2,307 providers**
      currently pointing at `207L00000X ANESTHESIOLOGY PHYSICIAN`.
- [ ] `CNM` Certified Nurse Midwife → `367A00000X` (Advanced Practice Midwife) — **473 providers**
      currently pointing at `207V00000X OBSTETRICS & GYNECOLOGY PHYSICIAN`.
- [ ] Occupational Therapist family → `225X00000X` / `224Z00000X` — **663 providers**.
- [ ] Athletic Trainer → `2255A2300X` — **1,101 providers**.

## 3. Correct an error in `CredTaxonomyDiscussion.md`

- [ ] The doc lists **Athletic Trainer** as a "true NUCC gap" with no taxonomy home.
      This is wrong — `2255A2300X` (Specialist/Technologist, Athletic Trainer) exists.
      Re-verify the other two claimed gaps (Health Educator, Clinical Exercise Physiologist)
      against `nucc_taxonomy_recent.csv` the same way.

## 4. False positives: `204E00000X` Oral & Maxillofacial Surgery is not a mis-assignment

The whole report assumes "non-physician credential + code in the Allopathic & Osteopathic
Physicians grouping = error." That assumption breaks for OMFS. Oral & maxillofacial surgeons
routinely hold **both** dental and medical degrees (DMD/MD, DDS/MD), and NUCC itself files
`204E00000X` under the physician grouping while naming it **"Oral & Maxillofacial Surgery (D.M.D.)"** —
the dental degree is in the code's own display name. A `DDS` or `DMD` choosing this code is
**correct**, not a mismatch.

- [ ] Exclude `204E00000X` from the mismatch report for dental credentials —
      **1,072 providers** are currently miscounted as errors
      (`DDS` 641, `DMD` 419, `BDS` 10, `OMFS` 2, all in `AllOthers.csv`).
      Corrected `AllOthers.csv` denominator: 12,718 rather than 13,790.
- [ ] Keep the genuinely odd `204E00000X` rows for review: `PHD` (13), `OMS`
      (Ostomy Management Specialist — 1), `PC` (Pharmacist Clinician — 1),
      plus `MSD`/`MS`/`MPH`/`MBA` (66 in `MasterOf.csv`) and `NP`/`PA` (9).
      The `PA` rows were annotated strength-2 → `363AS0400X` Surgical PA, which is plausible
      and can stay; the rest are unexplained.
- [ ] **Generalize the fix.** OMFS is the clearest case but the same logic applies to any
      dual-degree or non-MD-degree path. Audit the other physician-grouping codes whose display
      name encodes a specific degree — `209800000X` Legal Medicine (M.D./D.O.) and
      `207SG0201X` Clinical Genetics (M.D.) — and more importantly define an explicit
      allow-list of legitimate credential × physician-taxonomy pairs so the report stops
      treating "physician grouping" as a synonym for "wrong."
- [ ] Add this caveat to `CredTaxonomyDiscussion.md`. Its headline framing that every
      non-physician-on-physician-code pairing is a data-quality defect is overstated.

## 5. Make the annotation step reproducible

- [ ] The committed scripts only **split** files; nothing in the repo generates
      `should_use_tax` or `match_strength`. That mapping appears to have been done by hand
      and cannot be re-run when NUCC publishes an update.
      Commit it as either a script or a checked-in credential→taxonomy lookup table.

## 6. Data-quality issues that are not taxonomy problems

- [ ] `CNA` (Certified Nursing Assistant, 697 providers) maps to `ANESTHESIOLOGY PHYSICIAN` —
      almost certainly `CNA` being confused with `CRNA` upstream. Flag as a source data bug.
- [ ] Separate the likely data-entry errors (e.g. `MS` choosing `CARDIOVASCULAR DISEASE PHYSICIAN`)
      from genuine scope-of-practice gaps before petitioning NUCC for anything.

## 7. Housekeeping

- [ ] `report_splits/NP_Summary.md` is a one-paragraph orphan whose content is already covered
      in `CredTaxonomyDiscussion.md` §Bucket 2. Fold it in or delete it.
- [ ] Normalize CSV quoting — the unannotated files keep the source's partial quoting
      (`"facetCredentialCode"` quoted, rest bare); the annotated ones were rewritten clean.
- [ ] Wire the results into the main FaCeT pipeline. Nothing outside this directory currently
      references `vs_taxonomy_analysis` or the `facetCredentialCode`/`chosenTaxonomy` columns.

