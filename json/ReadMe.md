# JSON Credential Data

This directory holds the JSON representation of the credential data that also
lives in [`../sql/`](../sql). One `.json` file is generated per `insert_*.sql`
file, and the two are kept in sync by [`../sql_to_json.py`](../sql_to_json.py).

## Structure

Each file is a JSON **list of credential-class objects**. Every object has a
`credential_class` (taken from the `--` section comments in the SQL) and a
`credential_list` of rows, keyed by the INSERT column names:

```json
[
  {
    "credential_class": "Homeopathic Medical Doctors",
    "credential_list": [
      {
        "id": 19,
        "credential_abbr": "MD(H)",
        "unique_credential_abbr": "MD(H)",
        "credential_name": "Homeopathic Medical Doctor (Arizona)",
        "credentialing_organization_name": null,
        "credentialing_organization_url": null,
        "credential_description": "Medical doctor with homeopathic specialization licensed in Arizona",
        "is_multisource": true,
        "is_clinical": true,
        "is_board_certification": false,
        "is_credential_retired": false,
        "is_fhir_credential": false,
        "duplicate_abbreviation_code": 0,
        "created_at": null,
        "updated_at": null,
        "credential_class": "Homeopathic Medical Doctors"
      }
    ]
  }
]
```

`credential_class` appears both on the group object and on every row, so the
data can be used either grouped or flattened row by row. 



