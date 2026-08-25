# Credential-to-Taxonomy Mismatch Analysis
## FaCeT Non-Physician Provider Review

---

## Overview

This document summarizes findings from a cross-file analysis of three non-physician provider groups in the FaCeT system: **Nurse Practitioners**, **Physician Assistants**, and **Masters-Degree Providers**. In each case, FaCeT credential codes were compared against the NUCC Health Care Provider Taxonomy to identify mismatches where providers have been classified using physician taxonomy codes rather than the correct non-physician taxonomy codes that exist for their credential type.

The analysis produced three output columns appended to each report file:

| Column | Meaning |
|---|---|
| `should_use_tax` | The NUCC taxonomy code the provider should have been assigned |
| `should_use_tax_description` | Human-readable label for that code |
| `match_strength` | Confidence: `3` = direct credential-name match, `2` = strong specialty-driven match, `1` = indirect/reasonable match, blank = no appropriate non-physician taxonomy exists |

Across all three files, **47,504 provider records** were reviewed.

---

## File-by-File Summary

### Nurse Practitioners

- **1,520 credential-specialty combination rows** representing **29,803 provider records**
- Source taxonomy reference: `nucc_splits/nurse_practitioners.csv` (18 NP-specific NUCC codes)

| Match Strength | Rows | Providers |
|---|---|---|
| 3 — Credential name directly matches NP taxonomy | 785 (51.6%) | 10,389 (34.9%) |
| 2 — Generic credential, specialty clearly maps to NP taxonomy | 354 (23.3%) | 13,247 (44.4%) |
| 1 — Indirect setting-based match | 12 (0.8%) | 584 (2.0%) |
| Blank — No appropriate NP taxonomy exists | 369 (24.3%) | 5,583 (18.7%) |

**Strength-3 credentials** (credential name encodes the specialty directly, no ambiguity): ACNP, ACNP-BC, ACNPC, ACNPC-AG, AG-ACNP, AGACNP-BC, ANP, ANP-BC, ANP-C, CANP, CFNP, CPNP, CPNP-PC, FNP, FNP-BC, FNP-C, FPNP, GNP, GNP-BC, NNP, NNP-BC, PMHNP, PMHNP-BC, PMHNP-C, PNP, PPCNP-BC, SNP-BC, WHNP, WHNP-BC

**Key insight:** Generic credentials (`NP`, `CNP`, `CRNP`, `ARNP`, etc.) were mapped using the chosen physician taxonomy as the signal for clinical intent. An `NP` who chose `PEDIATRICS PHYSICIAN` belongs under `363LP0200X` (Pediatric Nurse Practitioner), not a physician code.

Largest NP ETL targets by provider count:

| Target NP Taxonomy | Providers |
|---|---|
| Family Nurse Practitioner (363LF0000X) | 14,960 |
| Pediatric Nurse Practitioner (363LP0200X) | 2,477 |
| Psychiatric/Mental Health Nurse Practitioner (363LP0808X) | 1,975 |
| Adult Health Nurse Practitioner (363LA2200X) | 1,741 |
| Acute Care Nurse Practitioner (363LA2100X) | 981 |
| Obstetrics & Gynecology Nurse Practitioner (363LX0001X) | 693 |
| Neonatal Nurse Practitioner (363LN0000X) | 342 |
| Gerontology Nurse Practitioner (363LG0600X) | 315 |

---

### Physician Assistants

- **509 credential-specialty combination rows** representing **17,423 provider records**
- Source taxonomy reference: `nucc_splits/physician_assistants.csv` (3 PA-specific NUCC codes)

| Match Strength | Rows | Providers |
|---|---|---|
| 3 — Direct credential match | 0 (0%) | 0 (0%) |
| 2 — Chosen specialty clearly maps to Medical or Surgical PA | 389 (76.4%) | 14,394 (82.6%) |
| 1 — Indirect/procedurally mixed specialty | 77 (15.1%) | 2,652 (15.2%) |
| Blank — No appropriate PA taxonomy (imaging, pathology, anesthesia) | 43 (8.4%) | 377 (2.2%) |

**Key insight:** All PA credentials (PA, PA-C, PAC, RPA, RPA-C, MPAS, PA-S) are generic — none encode a specialty, so there are no strength-3 entries. The chosen physician taxonomy cleanly divides most cases into surgical vs. medical PA practice. Blank cases (Radiology 230 providers, Anesthesiology 61, Pathology 27) are correctly left unmapped — PAs work in those settings but neither Medical PA nor Surgical PA is a meaningful classification for them.

---

### Masters-Degree Providers

- **313 credential-specialty combination rows** representing **1,278 provider records**
- Source taxonomy reference: `nucc_splits/masters_degree_providers.csv` (7 NUCC codes: Behavior Analyst, Counselor, Marriage & Family Therapist, Genetic Counselor M.S., Dance Therapist, Rehabilitation Counselor, Audiologist)

| Match Strength | Rows | Providers |
|---|---|---|
| 3 — Credential name directly names the profession | 2 (0.6%) | 2 (0.2%) |
| 2 — Strong specialty/credential-driven match | 22 (7.0%) | 182 (14.2%) |
| 1 — Indirect match | 26 (8.3%) | 46 (3.6%) |
| Blank — No appropriate masters taxonomy | 263 (84.0%) | 1,048 (82.0%) |

**Key insight:** The 84% blank rate reflects a fundamental structural mismatch: the NUCC masters taxonomy covers only seven behavioral/rehabilitation professions and was not designed to cover the full scope of clinical practice that masters-prepared professionals now occupy. Credentials like MPT, MSPT, MS, MA, MPH, MED, MOT are generic academic degrees pointed at clinical roles with no masters-level non-physician NUCC home. Physical Therapists and Occupational Therapists do have NUCC codes — but under a separate grouping, not in this masters file.

Clean matches that do exist: `MCD` → Audiologist (strength 3); `MSW`/`MSSW` → Counselor (strength 2 for mental/behavioral health context, strength 1 otherwise); any credential + genetics specialty → Genetic Counselor M.S. (strength 2); any credential + core psychiatry → Counselor (strength 2).

---

## Three Buckets for Remediation

---

### 🟢 Bucket 1: SOLVE WITH ETL

> **A correct non-physician NUCC taxonomy code already exists. The provider record should simply be remapped.**
> No policy decision required — this is a pure data quality fix. The mapping is unambiguous and the
> target values are already populated in `should_use_tax` and `should_use_tax_description` in each output file.

**Nurse Practitioners:** All rows with `match_strength` of `2` or `3` are ETL candidates — **24,220 provider records** (81.3% of all NP providers in this file) who are currently carrying physician taxonomy codes when a specific NP code is correct and available.

**Physician Assistants:** Rows with `match_strength = 2` represent **14,394 provider records** (82.6%) that can be cleanly converted to either Medical PA (`363AM0700X`) or Surgical PA (`363AS0400X`). Strength-1 rows (2,652 providers) are reasonable conversions as well but warrant human review given specialty ambiguity.

**Masters-Degree:** Only 184 providers (14.4%) have clean ETL targets, reflecting the limited NUCC coverage in this grouping.

| Group | ETL-Ready Providers (strength 2+3) | % of Group |
|---|---|---|
| Nurse Practitioners | 23,636 | 79.3% |
| Physician Assistants | 14,394 | 82.6% |
| Masters Degree | 184 | 14.4% |
| **Total** | **38,214** | **80.4%** |

---

### 🟡 Bucket 2: CONSIDER PROPOSING A NEW NUCC CODE

> **A real, established clinical specialty exists. Providers are clearly practicing in it and attempting to
> self-identify through taxonomy selection — but no NUCC code exists to receive them.**
> These providers are forced into physician codes by the absence of an appropriate alternative.
> Each case here represents a candidate for a formal NUCC taxonomy petition.

#### NP Specialties with No Current NUCC Code

The following practice domains have meaningful NP provider populations, established professional credentialing bodies, and specialty-specific NP credentials — but no NUCC taxonomy code. These are the strongest candidates for new code petitions to NUCC:

| Specialty / Clinical Domain | NP Providers Affected | Notable Specialty Credentials |
|---|---|---|
| Emergency Medicine NP | 543 | ENP-C |
| Cardiovascular Disease NP | 374 | — |
| Dermatology NP | 317 | DCNP |
| Hematology & Oncology NP | 269 | AOCNP |
| Neurology NP | 231 | — |
| Nephrology NP | 186 | — |
| Pain Medicine NP | 177 | — |
| Gastroenterology NP | 175 | — |
| Endocrinology NP | 167 | — |
| Pulmonary Disease NP | 164 | — |
| Surgery NP | 157 | — |
| Urology NP | 156 | — |
| Orthopaedic Surgery NP | 143 | — |
| Hospice & Palliative Medicine NP | 235 (combined) | — |
| Infectious Disease NP | 119 | — |
| Allergy & Immunology NP | 73 (combined) | — |
| Rheumatology NP | 56 | — |

The credential specificity is itself an argument: `DCNP`, `AOCNP`, and `ENP-C` are real board certifications issued by credentialing bodies that have already formally recognized these specialties as distinct enough to certify. The fact that the certifying organizations have acted but NUCC has not is a meaningful signal that new codes are overdue.

#### PA Specialties with No Current NUCC Code

The PA taxonomy gap is structural: only three codes exist (generic, medical, surgical). The binary medical/surgical split is insufficient for modern PA practice. PAs practicing in Radiology (230 providers in this file), Anesthesiology (61), and Pathology (27+) have no code at all. Beyond those, the following domains have established PA board certifications but no corresponding NUCC code:

- Emergency Medicine PA
- Cardiovascular/Cardiothoracic Surgery PA
- Dermatology PA
- Orthopaedic Surgery PA
- Neurosurgery PA

#### Masters-Degree Providers

The masters file points to a gap for professions whose NUCC codes are present elsewhere in the taxonomy but not in the behavioral/rehabilitation masters grouping: Physical Therapists (MPT, MSPT — 168+ providers choosing PM&R physician codes) and Occupational Therapists (MOT, MOTR/L). The remediation here is partly a FaCeT classification fix (routing those credentials to the correct NUCC grouping) rather than a net-new code petition.

True NUCC gaps in the masters space include: **Athletic Trainer (MS/ATC)**, **Health Educator (MPH/CHES)**, and **Clinical Exercise Physiologist (MS)** — clinical roles increasingly integrated into care teams with no non-physician taxonomy home.

---

### 🔴 Bucket 3: NOT SURE HOW TO SOLVE

> **Neither an ETL remap nor a new NUCC code petition fully resolves these cases.**
> These records remain blank and should be flagged for manual review or held pending
> broader clinical policy decisions. The root cause varies — some are structural NUCC gaps,
> some are likely upstream data entry problems, and some are genuine scope-of-practice questions
> with no clean taxonomy answer.

- **NP + surgical specialty:** An `NP` or `CRNP` choosing `NEUROLOGICAL SURGERY` or `THORACIC SURGERY` is practicing in a surgical support role. There is no surgical NP taxonomy in NUCC. Whether this warrants a new code or is better captured by documenting the supporting care role is a clinical policy question.
- **PA + Radiology/Pathology/Anesthesia:** PAs work in these settings but neither Medical PA nor Surgical PA accurately describes them. A more granular PA taxonomy would resolve this, but is a NUCC petition issue.
- **Masters providers in clinical medicine:** An `MS` choosing `ENDOCRINOLOGY PHYSICIAN` or `CARDIOVASCULAR DISEASE PHYSICIAN` most likely reflects a clinical research coordinator, lab professional, or similar role — not independent masters-level clinical practice. These may represent upstream data entry problems rather than taxonomy gaps.
- **Generic credentials with no specialty signal:** A small number of rows carry generic credentials paired with administrative or unusual physician codes (`INDEPENDENT MEDICAL EXAMINER`, `LEGAL MEDICINE`, `CLINICAL INFORMATICS`) where neither a taxonomy match nor a new code is appropriate. These are best reviewed individually.

---

## Recommended Next Steps

1. 🟢 **SOLVE WITH ETL** — Run immediate ETL conversion for all `match_strength = 3` and `match_strength = 2` rows across the NP and PA files — approximately **38,000 provider records**. Target values are already populated in `should_use_tax` and `should_use_tax_description`. No manual review needed.

2. 🟢 **SOLVE WITH ETL (with review)** — Human review of `match_strength = 1` rows (~3,200 providers across NP and PA files) before conversion. These are reasonable but indirect matches where clinical context should confirm the mapping before the ETL runs.

3. 🟡 **CONSIDER NEW NUCC CODE** — Draft a NUCC taxonomy petition for the highest-volume NP specialty gaps: Emergency Medicine NP (543 providers), Cardiovascular NP (374), Dermatology NP (317), Hematology/Oncology NP (269), and Neurology NP (231) — all have established credentialing bodies already issuing specialty certificates, making the case for NUCC recognition strong.

4. 🟡 **CONSIDER NEW NUCC CODE** — Petition for specialty-specific PA codes beyond the current medical/surgical binary: Emergency Medicine PA, Cardiovascular/Cardiothoracic Surgery PA, Dermatology PA, Orthopaedic Surgery PA, and Neurosurgery PA all have established board certifications with no NUCC home.

5. 🟡 **CONSIDER NEW NUCC CODE (or reclassify)** — Reclassify MPT/MSPT/MOT records into the correct NUCC Physical Therapist or Occupational Therapist taxonomy groupings, which already have appropriate codes under their own NUCC section. This is a FaCeT classification fix more than a NUCC petition.

6. 🔴 **NOT SURE HOW TO SOLVE** — Flag and audit the remaining blank records. Separate the likely upstream data entry errors (MS choosing Cardiovascular Disease Physician) from the genuine scope-of-practice ambiguities (NP in Neurological Surgery, PA in Radiology) and handle each class differently based on clinical policy guidance.
