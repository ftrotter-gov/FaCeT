-- AHHC
INSERT INTO org_credential (
    id,
    category,
    issuer,
    issuer_url,
    credential_type,
    display,
    credential_url,
    is_credential_retired,
    is_cms_deeming_credential,
    created_at,
    updated_at
) VALUES
(
    10000,
    'accreditation',
    'Accreditation Commission for Health Care',
    'https://www.achc.org',
    'achc_home_health_accreditation',
    'ACHC Home Health Accreditation',
    'https://achc.org/home-health/',
    FALSE,
    FALSE,
    NULL,
    NULL
),
(
    10001,
    'accreditation',
    'Accreditation Commission for Health Care',
    'https://www.achc.org',
    'achc_hospice_accreditation',
    'ACHC Hospice Accreditation',
    'https://achc.org/hospice/',
    FALSE,
    FALSE,
    NULL,
    NULL
),
(
    10002,
    'accreditation',
    'Accreditation Commission for Health Care',
    'https://www.achc.org',
    'achc_home_care_accreditation',
    'ACHC Home Care Accreditation',
    'https://achc.org/home-care/',
    FALSE,
    FALSE,
    NULL,
    NULL
);

