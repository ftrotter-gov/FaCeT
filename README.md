# FACET - Framework for Accreditation & Credential Enumeration Taxonomy 

[![BETA](https://img.shields.io/badge/-BETA-red?style=for-the-badge&labelColor=red)](#)

FACET is a taxonomy of clinical credentials derived from the real-world [NPPES data](https://download.cms.gov/nppes/NPI_Files.html), the information that clinicians have actually typed themselves over the course of the almost 20 years that NPPES has been in existence. The data set is designed specifically to account for clinical credentials that appear repeatedly in the wild. Its purpose is to ensure that every clinician that has a legitimate clinical credential can represent their legitimate credential in the various provider directories that they will participate in. 

## FACET Features

* FACET is comprehensive. It has over 500 credentials, built from what actual clinicians have typed into NPPES over the last 20 years or so, this is representative of what actual in the wild credentials look like.
* It is properly segmented into different classes of credentials (Non-Physician, Non-Doctor Prescribing Providers (NPNDPP) vs physicians). It does through simple segmentation of ids (physicians are 1-1000, Nurses are 1001-10000 etc) 
* It has international credentials for physicians (i.e. MBChB, YI-XUE-SHI, etc). 
* FACET supports unicode representations of the same. (醫學士).
* It differentiates physician-only credentials (ABFP).
* It includes animal doctors as a distinct category.
* It includes a useful map, of how to convert random self-entered credential strings into the canonical representations. 
* It is capable of ensuring that credential text can be used to support data parsimony efforts, for instance ensuring that individuals who choose to represent themselves as Medical Doctors using 'MD' are also listed as some kind of Physician using [NUCC taxonomy codes](https://taxonomy.nucc.org/) and vice versa. 
* It provides hyperlinks to the organizations that maintain a specific credential when that is available. 
* It is available under an Open License and can be used commercially as needed.
* It details whether a credential is a board certificatin.
* whether a credential is retired.
* whether a credential is a current FHIR credential (which will go away if and when FACET itself becomes a FHIR codeset). 
* It details whether there are two clinical credentials with the same abbreviation.
* It is designed to be friendly to auto-select widgets in HTML5 and other standard interfaces

## Getting the Data

* Look in [csv/](./csv) for the CSV version of FACET and the map from raw strings
* Please look in [sql/](./sql) for the PostGreSQL codesets. 
* Please look in [json/](./json) for the JSON version of the codesets.

## FHIR Shorthand (FSH) Output

FACET is published inside FHIR Implementation Guides as
[FHIR Shorthand](https://hl7.org/fhir/uv/shorthand/), the plain-text language
used to author FHIR IGs. `facet_to_fsh.py` compiles the data in [json/](./json)
into the two `.fsh` files that the [US NDH IG](https://github.com/HL7/fhir-us-ndh)
expects in its `input/fsh/` directory:

| File | Contents |
|---|---|
| `facet_credentials.fsh` | `FaCeTcredentialVS` value set plus the `FaCeT-credentialCS` code system of individual clinician credentials |
| `facet_org_credential.fsh` | `FaCeTorganizationCredentialVS` value set plus the `FaCeT-org-credentialCS` code system of organizational credentials |

Write the FSH into a checkout of the IG with `--out-dir`:

```bash
# Compile both files into the IG's input/fsh directory
python facet_to_fsh.py --out-dir ../fhir-us-ndh/input/fsh

# Build only one of the two files
python facet_to_fsh.py --out-dir /tmp/fsh --only credentials
python facet_to_fsh.py --out-dir /tmp/fsh --only org

# Verify the generated files are up to date without writing (exits non-zero if stale)
python facet_to_fsh.py --out-dir ../fhir-us-ndh/input/fsh --check
```

Concepts are emitted in `id` order, so related credentials stay grouped
(physicians 1–1000, nurses 1001–10000, and so on). The hand-authored preamble of
each file — the value set, the property code system, and the code system
metadata — is reproduced verbatim; only the concept block is generated.

### Verifying the FSH

There are two layers of tests. The first checks the generated text and needs
nothing beyond Python:

```bash
python -m unittest test_facet_to_fsh -v
```

The second compiles the generated files with
[SUSHI](https://fshschool.org/docs/sushi/), the reference FSH compiler, and
asserts that it reports no errors and that the resulting FHIR CodeSystems and
ValueSets contain every credential:

```bash
python -m unittest test_facet_to_fsh_sushi -v
```

SUSHI is a Node package. The tests look for a `sushi` executable, try
`npm install -g fsh-sushi` if it is missing, and skip (rather than fail) when
it cannot be installed — so the suite still works offline. Set
`FACET_SKIP_SUSHI=1` to skip these slower tests explicitly.

You can also run the compile check directly:

```bash
python sushi_runner.py --out-dir ../fhir-us-ndh/input/fsh
```

The first SUSHI run downloads the FHIR R4 core package into `~/.fhir/packages`
and may take a few minutes; later runs take about ten seconds. Only the two
FaCeT files are compiled — the rest of the NDH IG depends on packages that are
outside the scope of this repository.

## Data Dictionary

FACET uses two separate tables: one for **individual-level credentials** (held by clinicians) and one for **organizational-level credentials** (held by healthcare facilities and organizations).

---

### `dctnry.clinical_credential` — Individual-Level Credentials

These are credentials held by individual clinicians — degrees, licenses, board certifications, fellowships, and other personal professional qualifications.

| Column | Type | Description |
|---|---|---|
| `id` | INT | Manually assigned primary key. IDs are intentionally spaced to leave room within groupings by credential category (e.g., physicians are 1–1000, nurses are 1001–10000). Do not change. |
| `credential_abbr` | TEXT | The credential abbreviation as it appears in the wild (e.g., `MD`, `RN`, `DO`). May not be unique across all rows — some abbreviations refer to more than one credential. |
| `unique_credential_abbr` | TEXT | A guaranteed-unique version of `credential_abbr`. For duplicate abbreviations, a numeric suffix is appended (e.g., `AP_1`, `AP_2`, `RN-BC_1`, `RN-BC_2`). Intended for use as a stable machine-readable code or key. |
| `credential_name` | TEXT | Full spelled-out name of the credential (e.g., `Medical Doctor`, `Registered Nurse`). |
| `credentialing_organization_name` | VARCHAR(255) | The single organization that issues this credential, when applicable. NULL for multi-source credentials such as medical degrees that are granted by many different schools. |
| `credentialing_organization_url` | TEXT | Best URL for the credentialing organization or its specific credential/program page. May be just the organization homepage when a direct credential URL is not available. |
| `credential_description` | TEXT | Natural language description of the credential, its requirements, and its clinical purpose. |
| `is_multisource` | BOOLEAN | `TRUE` if many different organizations can issue this credential (e.g., `MD` and `RN` are granted by many schools). `FALSE` for single-source credentials such as board certifications issued by a single body. |
| `is_clinical` | BOOLEAN | `TRUE` if the credential is inherently related to clinical practice. Non-clinical credentials (e.g., CPA, CEO) are `FALSE`. Veterinarian credentials are also treated as `FALSE` for the purposes of this database. |
| `is_board_certification` | BOOLEAN | `TRUE` if this credential represents a board certification — a voluntary, post-graduate credential demonstrating specialized expertise. |
| `is_credential_retired` | BOOLEAN | `TRUE` if the credentialing organization has stopped issuing this credential to new holders, but existing holders may continue to use it. |
| `is_fhir_credential` | BOOLEAN | `TRUE` if this credential appears in the FHIR v2-0360 codeset (`IndividualSpecialtyAndDegreeLicenseCertificateVS` from the [HL7 NDH Implementation Guide](https://build.fhir.org/ig/HL7/fhir-us-ndh/ValueSet-IndividualSpecialtyAndDegreeLicenseCertificateVS.html)). This column will be deprecated if and when FACET itself becomes an official FHIR codeset. |
| `duplicate_abbreviation_code` | INT | `0` = this abbreviation is not shared with any other credential. `1` = this abbreviation is shared with at least one other credential, and this row is the "winning" (most common) meaning used in auto-mapping. `2` or higher = this abbreviation is shared, and this row is a less common meaning that will not be used in auto-mapping. |
| `created_at` | TIMESTAMPTZ | Timestamp set automatically by the database on record creation. Always `NULL` in insert statements. |
| `updated_at` | TIMESTAMPTZ | Timestamp set automatically by the database on record update. Always `NULL` in insert statements. |

---

### `dctnry.org_credential` — Organizational-Level Credentials

These are credentials held by healthcare organizations and facilities — accreditations, certifications, designations, and regulatory designations issued by bodies such as The Joint Commission, DNV Healthcare, and CMS-approved deeming authorities.

A **CMS deeming credential** (`is_cms_deeming_credential = TRUE`) means that the issuing organization has been authorized by CMS to determine whether a healthcare provider meets Medicare Conditions of Participation (CoPs). When a provider holds such an accreditation, CMS "deems" them to be in compliance without conducting its own survey.

| Column | Type | Description |
|---|---|---|
| `id` | BIGINT | Primary key. |
| `category` | TEXT | The broad category of the organizational credential. Common values include `accreditation`, `certification`, `designation`, and `regulatory_designation`. |
| `issuer` | TEXT | The name of the organization that issues this credential (e.g., `The Joint Commission`, `DNV Healthcare`, `ACHC`). |
| `issuer_url` | TEXT | The homepage URL of the issuing organization. |
| `credential_type` | TEXT | A unique, machine-readable slug/code for this specific credential (e.g., `jc_hospital_accreditation`, `dnv_niaho_hospital_accreditation`). Must be globally UNIQUE across all rows in the table. |
| `display` | TEXT | Human-readable display name for this credential (e.g., `Joint Commission Hospital Accreditation`). Suitable for use in user interfaces. |
| `credential_url` | TEXT | URL pointing to the specific credential or accreditation program page at the issuing organization's website. |
| `is_credential_retired` | BOOLEAN | `TRUE` if this credential is no longer being issued or recognized by the issuing organization. |
| `is_cms_deeming_credential` | BOOLEAN | `TRUE` if CMS recognizes this accreditation as meeting Medicare Conditions of Participation, making the issuing body a CMS-approved "deeming authority." See [CMS deeming authority documentation](https://www.cms.gov/medicare/provider-enrollment-and-certification/surveycertificationgeninfo/deeming-authority) for more detail. |
| `created_at` | TIMESTAMPTZ | Timestamp set automatically by the database on record creation. Always `NULL` in insert statements. |
| `updated_at` | TIMESTAMPTZ | Timestamp set automatically by the database on record update. Always `NULL` in insert statements. |

---

## Duplicate Credentials

To see duplicate credentials in the data use the SQL: 

```sql
SELECT * FROM gold_dctnry.clinical_credential
WHERE duplicate_abbreviation_code != 0
ORDER BY  credential_abbr ASC, duplicate_abbreviation_code DESC
```

Which recently resulted in: 

```csv
20042,AP,Acupuncture Physician,2
50035,AP,Advanced Practitioner,1
60033,BT,Behavior Technician,3
50067,BT,Bachelor of Theology,3
1174,CNN,Certified Corrections Nurse,2
1177,CNN,Certified Nephrology Nurse,1
1145,CRN,Certified Radiologic Nurse,2
1214,CRN,Certified Registered Nurse,1
60029,MT,Music Therapist,2
50087,MT,Medical Technician,1
1055,RN-BC,School Nursing,2
1042,RN-BC,Certified Vascular Nurse,2
1043,RN-BC,College Health Nursing,2
1044,RN-BC,Community Health Nursing,2
1045,RN-BC,Faith Community Nursing,2
1047,RN-BC,General Nursing Practice,2
1049,RN-BC,Hemostasis Nursing,2
1050,RN-BC,High-Risk Perinatal Nursing,2
1051,RN-BC,Home Health Nursing,2
1052,RN-BC,Perinatal Nursing,2
1054,RN-BC,Rheumatology Nursing,2
1217,RN-BC,General Nursing Practice Certification,1
```

The duplicate_abbreviation_code shows which is the more common meaning when possible.




## Contributing
Thank you for considering contributing to an Open Source project of the US Government! For more information about our contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

So far I (Fred Trotter, the initial author) have not been able to find something like this available as a prexisting dataset. If there is a better, more comprehensive clinical credential codeset please get in touch. I would be more than happy to retire this effort in favor of something maintained by someone who has time to do a comprehensive job, including supporting more robust support for international clinical credentials. 


