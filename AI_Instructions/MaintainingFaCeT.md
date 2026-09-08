Maintaining FaCeT
===================


Facet is a system of clinical credentials as well as credentials that appear alongside clinical credentials frequently, including clinical adjacent and also credentials that people have that they choose to express from their previous academic background alongside their clinical credentials. In order to maintain that, we have a code set which needs to be unique by actual credential code. We do not use dots in the code. We actually have collisions where a given code can be repeated. These are infrequent, but when we have them, we document them in unique credential abbreviation summary and detail how we're reconciling them. We have a unique credential abbreviation, which sometimes has an underscore 1 or _2 following the abbreviation when there is a collision. In general, we try to ensure that, when it's possible, if there is clearly a clinical credential which should kind of own the traditional credential as the unique credential identifier, we try to do that when we can. We also try to maintain the other metadata about a given credential, as explained in the following code block. 

```javascript

    one_credential = {
        "id": 1, // a unuique numeric identifier. We spread these out so that meaningful work can be done on range of ids. 
            //  Each seperate json file should have a seperate range
        "credential_abbr": "MD", //this is the credential without any dots, periods or space, using the preferred capitlization for the credential
        "unique_credential_abbr": "MD", //this is the specifically unique version of the credential and is the lookup for the FHIR codeset, etc. 
            // "For instance a "Certified Corrections Nurse" and a "Certified Nephrology Nurse" both use "CNN" 
            // So the unique_credential_abbr for these are 'CCN_1' and 'CCN_2' in order to allow these to be uniquely identified. 
            // The vast majority of the time credential_abbr and unique_credential_abbr should be identical. 
        "credential_name": "Medical Doctor",
        "credentialing_organization_name": null,
        "credentialing_organization_url": null,
        "credential_description": "Doctor of Medicine degree from accredited medical school, enabling independent practice of medicine after residency training.",
        "is_multisource": true,
        "is_clinical": true,
        "is_board_certification": false,
        "is_credential_retired": false,
        "is_fhir_credential": true,
        "duplicate_abbreviation_code": 0,
        "created_at": null,
        "updated_at": null,
        "credential_class": "Physician credentials Medical doctors who can practice medicine independently"
      },

```


* Choose the correct json file to add your new credential by reading the file name (should be self-explaintory)
* When adding any new credential, you need to verify that the credential is not already in FaCet. 
* Then you need to verify that there is no other credential that has the exact same letters. In this case you will have to create a unique_credential_abbr with the the format {CRED}_1 for the unique_credential_abbr field. You will use the same credential in the credential_abbr field. 
* Fill in the other details of the json credential entry as appropriate.

