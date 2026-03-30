-- for generating the csv
SELECT
    unique_credential_abbr AS code,
    credential_abbr AS abbr,
    credential_name,
    credentialing_organization_name,
    credentialing_organization_url,
    credential_description,
    is_multisource,
    is_clinical,
    is_board_certification
FROM dctnry.clinical_credential