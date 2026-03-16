-- Hospital org credentials: accreditation
-- Split from insert_org_credential_hospital.sql

-- Joint Commisssion Accreditations
INSERT INTO org_credential (
    id,
    category,
    issuer,
    issuer_url,
    credential_type,
    display,
    credential_url
) VALUES
    (
        1,
        'accreditation',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_hospital_accreditation',
        'Joint Commission Hospital Accreditation',
        'https://www.jointcommission.org/accreditation-and-certification/health-care-settings/hospital/'
    ),
    (
        2,
        'accreditation',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_critical_access_hospital_accreditation',
        'Joint Commission Critical Access Hospital Accreditation',
        'https://www.jointcommission.org/accreditation-and-certification/health-care-settings/critical-access-hospital/'
    ),
    (
        3,
        'accreditation',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_ambulatory_health_care_accreditation',
        'Joint Commission Ambulatory Health Care Accreditation',
        'https://www.jointcommission.org/accreditation-and-certification/health-care-settings/ambulatory-health-care/'
    ),
    (
        4,
        'accreditation',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_behavioral_health_accreditation',
        'Joint Commission Behavioral Health Care and Human Services Accreditation',
        'https://www.jointcommission.org/accreditation-and-certification/health-care-settings/behavioral-health-care-and-human-services/'
    ),
    (
        5,
        'accreditation',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_home_care_accreditation',
        'Joint Commission Home Care Accreditation',
        'https://www.jointcommission.org/accreditation-and-certification/health-care-settings/home-care/'
    ),
    (
        6,
        'accreditation',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_laboratory_accreditation',
        'Joint Commission Laboratory Accreditation',
        'https://www.jointcommission.org/accreditation-and-certification/health-care-settings/laboratory/'
    ),
    (
        7,
        'accreditation',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_nursing_care_center_accreditation',
        'Joint Commission Nursing Care Center Accreditation',
        'https://www.jointcommission.org/accreditation-and-certification/health-care-settings/nursing-care-center/'
    ),
    (
        8,
        'accreditation',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_office_based_surgery_accreditation',
        'Joint Commission Office-Based Surgery Accreditation',
        'https://www.jointcommission.org/accreditation-and-certification/health-care-settings/office-based-surgery/'
    );


-- DNV Healthcare
INSERT INTO org_credential (
    id,
    category,
    issuer,
    issuer_url,
    credential_type,
    display,
    credential_url
) VALUES
    (
        9,
        'accreditation',
        'DNV Healthcare',
        'https://www.dnv.us',
        'dnv_niaho_hospital_accreditation',
        'DNV NIAHO Hospital Accreditation (Acute Care)',
        'https://www.dnv.us/services/niaho-accreditation-for-hospitals2/'
    ),
    (
        10,
        'accreditation',
        'DNV Healthcare',
        'https://www.dnv.us',
        'dnv_niaho_critical_access_hospital_accreditation',
        'DNV NIAHO Critical Access Hospital Accreditation',
        'https://www.dnv.com/services/niaho-accreditation-for-critical-access-hospitals/'
    ),
    (
        11,
        'accreditation',
        'DNV Healthcare',
        'https://www.dnv.us',
        'dnv_niaho_psychiatric_hospital_accreditation',
        'DNV NIAHO Psychiatric Hospital Accreditation',
        'https://www.dnv.us/life-sciences/healthcare/ac/'
    );


-- ACHC
INSERT INTO org_credential (
    id,
    category,
    issuer,
    issuer_url,
    credential_type,
    display,
    credential_url
) VALUES
    (
        12,
        'accreditation',
        'ACHC',
        'https://www.achc.org',
        'achc_acute_care_hospital_accreditation',
        'ACHC Acute Care Hospital Accreditation',
        'https://www.achc.org/acute-care-hospitals/'
    ),
    (
        13,
        'accreditation',
        'ACHC',
        'https://www.achc.org',
        'achc_critical_access_hospital_accreditation',
        'ACHC Critical Access Hospital Accreditation',
        'https://www.achc.org/acute-care-hospitals/'
    );


-- CIHQ
INSERT INTO org_credential (
    id,
    category,
    issuer,
    issuer_url,
    credential_type,
    display,
    credential_url
) VALUES
    (
        14,
        'accreditation',
        'CIHQ',
        'https://cihq.org',
        'cihq_hospital_accreditation',
        'CIHQ Hospital Accreditation',
        'https://cihq.org/accreditation-programs/hospitals/'
    );
