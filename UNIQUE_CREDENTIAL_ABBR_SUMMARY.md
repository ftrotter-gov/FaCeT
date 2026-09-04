# Unique Credential Abbreviation Implementation Summary

## Overview
Successfully added `unique_credential_abbr` column to the FaCeT credential database to handle duplicate abbreviations.

## Changes Made

### 1. Database Schema Update
- **File Modified**: `sql/create_credential.sql`
- **Change**: Added `unique_credential_abbr TEXT NOT NULL` column after `credential_abbr`
- This column stores a unique version of the abbreviation with suffixes (_1, _2, etc.) for duplicates

### 2. SQL Insert Statements Updated
All 10 credential insert files were updated to include the new column:
- `insert_credential_physicians.sql`
- `insert_credential_doctor_not_physician.sql`
- `insert_credential_nurses_batch1.sql`
- `insert_credential_nurses_batch2.sql`
- `insert_credential_midlevels.sql`
- `insert_credential_physical_therapists.sql`
- `insert_credential_psychosocial_therapists.sql`
- `insert_credential_other.sql`
- `insert_credential_animal_clinicians.sql`
- `insert_credential_not_clinicians.sql`

### 3. Duplicate Abbreviations Resolved

#### AP (Acupuncture Physician vs Advanced Practitioner)
- ID 20042: `AP` → `AP_1` (Acupuncture Physician)
- ID 50035: `AP` → `AP_2` (Advanced Practitioner)

#### BT (Behavior Technician vs Bachelor of Theology)
- ID 60033: `BT` → `BT_1` (Behavior Technician)
- ID 50067: `BT` → `BT_2` (Bachelor of Theology)

#### CNN (Certified Corrections Nurse vs Certified Nephrology Nurse)
- ID 1174: `CNN` → `CNN_1` (Certified Corrections Nurse)
- ID 1177: `CNN` → `CNN_2` (Certified Nephrology Nurse)

#### CRN (Certified Radiologic Nurse vs Certified Registered Nurse)
- ID 1145: `CRN` → `CRN_1` (Certified Radiologic Nurse)
- ID 1214: `CRN` → `CRN_2` (Certified Registered Nurse)

#### MT (Music Therapist vs Medical Technician)
- ID 60029: `MT` → `MT_1` (Music Therapist)
- ID 50087: `MT` → `MT_2` (Medical Technician)

#### RN-BC (12 different Board Certified Registered Nurse specialties)
- ID 1042: `RN-BC` → `RN-BC_1` (Certified Vascular Nurse)
- ID 1043: `RN-BC` → `RN-BC_2` (College Health Nursing)
- ID 1044: `RN-BC` → `RN-BC_3` (Community Health Nursing)
- ID 1045: `RN-BC` → `RN-BC_4` (Faith Community Nursing)
- ID 1047: `RN-BC` → `RN-BC_5` (General Nursing Practice)
- ID 1049: `RN-BC` → `RN-BC_6` (Hemostasis Nursing)
- ID 1050: `RN-BC` → `RN-BC_7` (High-Risk Perinatal Nursing)
- ID 1051: `RN-BC` → `RN-BC_8` (Home Health Nursing)
- ID 1052: `RN-BC` → `RN-BC_9` (Perinatal Nursing)
- ID 1054: `RN-BC` → `RN-BC_10` (Rheumatology Nursing)
- ID 1055: `RN-BC` → `RN-BC_11` (School Nursing)
- ID 1217: `RN-BC` → `RN-BC_12` (General Nursing Practice Certification)

#### Clinical-Adjacent (Non-Clinical) Collisions

The clinical-adjacent credential set (`insert_credentials_clinical_adjacent.sql` /
`json/insert_credentials_clinical_adjacent.json`, IDs in the 70000 range) introduced
several abbreviations that collide with credentials that already existed in the
codeset. These were briefly given a `" (nc)"` postfix; that pattern has been retired
in favor of the original `_1` / `_2` numeric suffix convention.

- ID 70013: `CPC` → `CPC_1` (Certified Professional Coder, AAPC) — collides with ID 50051 `CPC` (Certified Professional Coder)
- ID 70015: `CIC` → `CIC_1` (Certified Inpatient Coder, AAPC) — collides with ID 1142 `CIC` (Certified in Infection Control, clinical)
- ID 70052: `CPHRM` → `CPHRM_1` (Certified Professional in Health Care Risk Management, AHA) — collides with ID 1196 `CPHRM` (clinical nursing)
- ID 70083: `CPHQ` → `CPHQ_1` (Certified Professional in Healthcare Quality, NAHQ) — collides with ID 1195 `CPHQ` (clinical nursing)
- ID 70102: `CER` → `CER_1` (Certified Endoscope Reprocessor, HSPA) — collides with ID 50068 `CER` (Certificate, FHIR)
- ID 70106: `CMC` → `CMC_1` (Certified Medical Coder, PMI) — collides with ID 1072 `CMC` (Cardiac Medicine (Adult), clinical)

Collisions entirely inside the clinical-adjacent set are numbered in the same way:

- ID 70044: `CHC` → `CHC_1` (Certified in Healthcare Compliance, HCCA)
- ID 70048: `CHC` → `CHC_2` (Certified Health Care Constructor, AHA)

### 5. Suffix Convention and Clinical Precedence Rule

- Unique abbreviations are formed by appending `_1`, `_2`, `_3`, … to the base
  `credential_abbr`. Do **not** use parenthetical postfixes such as `" (nc)"`.
- **Clinical wins.** When a non-clinical (or clinical-adjacent) credential collides
  with a clinical credential, the clinical credential keeps the plain, unmodified
  abbreviation as its `unique_credential_abbr` (e.g. `CIC`), and the non-clinical
  credential receives the numeric suffix (`CIC_1`, `CIC_2`, and so on).
- When a collision is between two credentials of the same kind (both clinical, or
  both non-clinical), the incumbent/pre-existing row keeps the plain abbreviation
  where one already had it; otherwise all colliding rows are numbered `_1`, `_2`, …
- `credential_abbr` is always left unchanged — only `unique_credential_abbr` carries
  the suffix.
- Which row "wins" for auto-mapping purposes is tracked separately in
  `duplicate_abbreviation_code` (see `AI_Instructions/Duplicates.md`).

### 6. Merged SQL File Generated
- **File Created**: `merged_sql/merged.sql`
- Contains all CREATE and INSERT statements with the new `unique_credential_abbr` column
- Ready for database import

## Implementation Script
Created `update_credential_abbr.py` to automate the process:
- Systematically updates all INSERT statements
- Assigns unique suffixes based on credential ID
- Maintains original `credential_abbr` for backward compatibility

## Summary
- ✓ 1 CREATE TABLE statement updated
- ✓ 10 INSERT files updated
- ✓ 24 total duplicate credentials resolved in the original pass (6 abbreviations with 2-12 variants each)
- ✓ 8 additional clinical-adjacent collisions resolved with `_1` / `_2` suffixes (the retired `" (nc)"` postfix is no longer used anywhere)
- ✓ Merged SQL file generated successfully
- ✓ All credentials now have unique identifiers via `unique_credential_abbr`

## Next Steps
The database is now ready to use `unique_credential_abbr` as a unique key for credential lookups and mapping operations.
