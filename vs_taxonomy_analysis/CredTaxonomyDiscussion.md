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
