-- This table is hosted from https://github.com/ftrotter-gov/npd_credential_codeset
-- Which is a project to create a clinical credentials data set by miining the 
-- raw credentials that are found in NPPES

-- Column explinations: 
-- *  id - should be left alone, these were manually created to leave space between sections of the file
-- *  credential_abbr - the credential abbreviation should already be set
-- *  credential_name - the name of the credential spellout out, like "Medical Doctor" for M.D. and "Registered Nurse" for RN
-- *  credentialing_organization_name - not every organization has a single source, but when it does list it here.
-- *  credentialing_organization_url - the best url for that credential. Sometimes the best that can be gotten is the link to the credentialing organization home page.
-- *  credential_description - a natural language of the credential and its purpose.
-- *  is_multisource - lots of schools will grant an M.D. or an RN. These are multi-source credentials.
-- *  is_clinical - there are plenty of credentials, like CPA or CEO that have nothing to do with clinical practice. For the purposes of the database, we consider Veterinarian as non-clinical.
-- *  is_board_certification - should this credential be considered "board certified"
-- *  is_credential_retired - sometimes a credentialling organization will stop issuing a credential to new clinicians, but allow previous credential holders to continue using the credential.
-- *  created_at - should always be NULL so that the database can set
-- *  updated_at - should always be NULL so that the database can set.


CREATE TABLE IF NOT EXISTS dctnry.clinical_credential (
  id                          INT PRIMARY KEY,
  credential_abbr             TEXT        NOT NULL,  -- e.g., MD, DO, PhD
  unique_credential_abbr      TEXT        NOT NULL,  -- unique version with _1, _2 suffixes for duplicates
  credential_name             TEXT        NOT NULL,  -- e.g., Medical Doctor
  credentialing_organization_name VARCHAR(255),
  credentialing_organization_url  TEXT,
  credential_description      TEXT NULL,

  is_multisource              BOOLEAN     NOT NULL DEFAULT FALSE, -- many issuing orgs (e.g., MD)
  is_clinical                 BOOLEAN     NOT NULL DEFAULT FALSE, -- TRUE for inherently clinical creds
  is_board_certification      BOOLEAN     NOT NULL DEFAULT FALSE,
  is_credential_retired       BOOLEAN     NOT NULL DEFAULT FALSE, -- TRUE when a credential is no longer issued for some reason
  is_fhir_credential          BOOLEAN     NOT NULL DEFAULT FALSE, -- TRUE when a credential appears in the FHIR spec.
  duplicate_abbreviation_code INT NOT NULL DEFAULT 0, -- 0 means it is not a duplicate. 1 means it is a duplicate but it is winning, it will be used in the auto-mapping. 2 means that it is duplicate but will not be used in the mapping. 
  created_at                  TIMESTAMPTZ,
  updated_at                  TIMESTAMPTZ
);


CREATE TABLE IF NOT EXISTS clinical_credential_map
(
    incoming_credential_string text,
    outgoing_credential_string text
);


