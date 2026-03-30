Abbreviation as code
====================

Please read the README.md to see the short list of abbreviations that do not function as unique identifiers already.

Then read all of the code in sql/ to ensure and /csv to ensure that you understand how the project works.

We need to create a new column right after credential_abbr called unique_credential_abbr.

* First, in all of the sql files, simply copy the current abbreviation

```sql
'this_abrv', 
```

and make it

```sql
'this_abrv','this_abrv',
```

in all of the sql files.

Make sure that you also add it to the INSERT INTO statement as an additional column andme and addit to the CREATE TABLE statement in sql/create_credential.sql

Then find all of the repeating abbreviations and an _1, _2, _3 etc to them.

So AP will become AP_1 and AP_2 in the new unique_credential_abbr column.

RN-BC is going to get alot!!!

Do not consider the "winner" construct as you name.. just add digits in any random order.

Then use merge_sql.py to create the merged SQL.

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