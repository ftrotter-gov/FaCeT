# FACET - Framework for Accreditation & Credential Enumeration Taxonomy 

[![BETA](https://img.shields.io/badge/-BETA-red?style=for-the-badge&labelColor=red)](#)

FACET is a taxonomy of clinical credentials derived from the real-world [NPPES data](https://download.cms.gov/nppes/NPI_Files.html), the information that clinicians have actually typed themselves over the course of the almost 20 years that NPPES has been in existence. The data set is designed specifically to account for clinical credentials that appear repeatedly in the wild. Its purpose is to ensure that every clinician that has a legitimate clinical credential can represent their legitimate credential in the various provider directories that they will participate in. 

## FACET Features

* FACET is comprehensive. It has over 500 credentials, built from what actual clinicians have typed into NPPES over the last 20 years or so, this is representative of what actual in the wild credentials look like.
* It is properly segmented into different classes of credentials (mid-levels vs physicians). It does through simple segmentation of ids (physicians are 1-1000, Nurses are 1001-10000 etc) 
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

