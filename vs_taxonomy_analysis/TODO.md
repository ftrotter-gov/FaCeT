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

- [x] **FIXED.** Excluded `204E00000X` from the mismatch report for dental credentials —
      **1,072 providers** were miscounted as errors
      (`DDS` 641, `DMD` 419, `BDS` 10, `OMFS` 2). They now route to `LegitimatePairs.csv`.
      `AllOthers.csv` corrected: 13,790 → **12,718 providers** (1,324 → 1,320 rows).
- [x] **FIXED.** Genuinely odd `204E00000X` rows still surface for review: `PHD` (13),
      `OMS` Ostomy Management Specialist (1), `PC` (1), `MSD`/`MS`/`MPH`/`MBA`/`MSED` (66),
      and `NP`/`PA` (9). Note `OMS` is overloaded — it means both "Oral & Maxillofacial
      Surgery" and "Ostomy Management Specialist", so the allow-list disambiguates on the
      credential *name*, not just the code.
- [x] **FIXED (mechanism).** Added `legitimate_pairs.py` — an explicit allow-list of valid
      credential × physician-taxonomy pairs, checked as rule 0 in `split_nonphysician.py`
      before any mismatch bucketing. The report no longer treats "physician grouping" as a
      synonym for "wrong." Locked by `test_split_nonphysician.py` (14 tests).
- [x] **FIXED.** Caveat added to `CredTaxonomyDiscussion.md`.
- [ ] **Still open:** audit the other degree-encoding physician codes the same way —
      `209800000X` Legal Medicine (M.D./D.O.) and `207SG0201X` Clinical Genetics (M.D.).
      Add any valid pairings to `LEGITIMATE_PAIRS`.

## 5. Misdecoded credential abbreviations (a *third* defect class)

Distinct from both the OMFS false positive and a genuine taxonomy mismatch: here the
provider chose a sensible code and **FaCeT expanded their credential abbreviation to the
wrong profession**. The fix is upstream, in the credential dictionary.

- [x] **FIXED (mechanism).** Added `misdecoded_credentials.py` + `MisdecodedCredentials.csv`.
      Routed as rule 0.5 in `split_nonphysician.py`, with correction targets pre-populated.
- [x] `AA` — FaCeT says *Associate of Arts*, actually **Anesthesiologist Assistant**.
      183 providers, 97.8% on anesthesiology codes → `367H00000X`.
- [x] `CAA` — FaCeT says *Certified Audiologist Assistant*, actually **Certified
      Anesthesiologist Assistant**. 94 providers, 100% on anesthesiology → `367H00000X`.
- [x] `CSFA` — FaCeT says *Certified School Food Administrator*, actually **Certified
      Surgical First Assistant**. 95 providers, 97.9% on surgical codes → `246ZC0007X`.
- [x] **Safety guard.** Corrections only apply when the provider's own taxonomy choice
      corroborates them. 366 of the 372 rows diverted; the 6 uncorroborated singletons
      (`AA` on Family Medicine / Emergency Medicine / PM&R / Surgery, `CSFA` on Family
      Medicine / Orthopaedic Trauma) stay in the mismatch report — an `AA` on a Family
      Medicine code may genuinely be an Associate of Arts.
- [ ] **ACTION REQUIRED — upstream. Root cause located in `json/`.** These are not just
      wrong labels; two of the three are filed as **non-clinical**, so they are being
      excluded from clinician-facing value sets entirely:

      | Abbrev | File | Line | `is_clinical` |
      |---|---|---|---|
      | `AA`   | `json/insert_credential_not_clinicians.json` | 292 | `false` |
      | `CSFA` | `json/insert_credential_not_clinicians.json` | 333 | `false` |
      | `CAA`  | `json/insert_credential_other.json`          | 274 | — |

      `CSFA` is additionally attributed to the *School Nutrition Association* with a
      "school food service management" description. All three need their name,
      description, credentialing organization, and `is_clinical` flag corrected, and
      `AA`/`CSFA` most likely need to move out of `insert_credential_not_clinicians.json`
      altogether. **Left unedited deliberately** — `json/` is the project's source of
      truth and feeds FSH generation, so this warrants a maintainer decision rather than
      an automated patch. Note `AA`/`CAA` share a NUCC code but are distinct certifications.
- [ ] **Audit the rest of the credential dictionary the same way.** Three misdecodes were
      found by inspecting one report; a systematic sweep for abbreviations whose provider
      population clusters on an unrelated specialty will likely find more. High-value
      heuristic: any credential where >90% of providers sit in one clinical domain that
      has nothing to do with the credential's stated meaning.

## 6. Make the annotation step reproducible

- [x] **PARTLY FIXED — data loss risk removed.** Re-running `split_nonphysician.py` used to
      silently destroy all hand-authored annotations (this was verified: a test run wiped the
      `PhysicianAssistants.csv` and `MasterOf.csv` analysis columns, recovered from git).
      The script now reads existing outputs first and re-attaches annotations keyed by
      `(facetCredentialCode, chosenTaxonomyCode)` — unique across all 4,459 source rows.
      Verified: 1,667 annotations restored, 0 lost, byte-identical across repeated runs.
- [ ] **Still open:** the annotation *logic* remains unreproducible — the values are preserved
      but nothing in the repo can regenerate them from scratch. If the source data gains new
      credential/taxonomy combinations, those rows come out blank and need manual authoring.
      Commit the mapping rules as a script or lookup table.

## 7. Data-quality issues that are not taxonomy problems

- [ ] `CNA` (Certified Nursing Assistant, 697 providers) maps to `ANESTHESIOLOGY PHYSICIAN` —
      almost certainly `CNA` being confused with `CRNA` upstream. Flag as a source data bug.
- [ ] Separate the likely data-entry errors (e.g. `MS` choosing `CARDIOVASCULAR DISEASE PHYSICIAN`)
      from genuine scope-of-practice gaps before petitioning NUCC for anything.

## 8. Housekeeping

- [ ] `report_splits/NP_Summary.md` is a one-paragraph orphan whose content is already covered
      in `CredTaxonomyDiscussion.md` §Bucket 2. Fold it in or delete it.
- [x] **FIXED.** CSV quoting normalized — the splitter now emits a canonical header
      (`BASE_HEADER`) to every output file instead of propagating the source's inconsistent
      quoting and BOM. All six files now share identical column headers.
- [ ] Wire the results into the main FaCeT pipeline. Nothing outside this directory currently
      references `vs_taxonomy_analysis` or the `facetCredentialCode`/`chosenTaxonomy` columns.

