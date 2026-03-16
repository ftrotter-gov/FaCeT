-- Hospital org credentials: designation
-- Split from insert_org_credential_hospital.sql

-- NCI
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
    2000,
    'designation',
    'National Cancer Institute',
    'https://www.cancer.gov',
    'nci_cancer_center_designation',
    'NCI Designated Cancer Center',
    'https://www.cancer.gov/research/infrastructure/cancer-centers'
),
(
    2001,
    'designation',
    'National Cancer Institute',
    'https://www.cancer.gov',
    'nci_comprehensive_cancer_center_designation',
    'NCI Designated Comprehensive Cancer Center',
    'https://www.cancer.gov/research/infrastructure/cancer-centers'
),
(
    2002,
    'designation',
    'National Cancer Institute',
    'https://www.cancer.gov',
    'nci_basic_laboratory_cancer_center_designation',
    'NCI Designated Basic Laboratory Cancer Center',
    'https://www.cancer.gov/research/infrastructure/cancer-centers'
);


-- Trauma Centers
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
    3000,
    'designation',
    'American College of Surgeons',
    'https://www.facs.org',
    'trauma_center_level_1',
    'Level I Trauma Center',
    'https://www.facs.org/quality-programs/trauma/verification-review-and-consultation-program/'
),
(
    3001,
    'designation',
    'American College of Surgeons',
    'https://www.facs.org',
    'trauma_center_level_2',
    'Level II Trauma Center',
    'https://www.facs.org/quality-programs/trauma/verification-review-and-consultation-program/'
),
(
    3002,
    'designation',
    'American College of Surgeons',
    'https://www.facs.org',
    'trauma_center_level_3',
    'Level III Trauma Center',
    'https://www.facs.org/quality-programs/trauma/verification-review-and-consultation-program/'
),
(
    3003,
    'designation',
    'American College of Surgeons',
    'https://www.facs.org',
    'trauma_center_level_4',
    'Level IV Trauma Center',
    'https://www.facs.org/quality-programs/trauma/verification-review-and-consultation-program/'
);


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
    3005,
    'designation',
    'Association of American Medical Colleges',
    'https://www.aamc.org',
    'academic_medical_center',
    'Academic Medical Center',
    'https://www.aamc.org/what-we-do/mission-areas/academic-medicine'
);


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
    3006,
    'designation',
    'Centers for Medicare & Medicaid Services',
    'https://www.cms.gov',
    'teaching_hospital',
    'Teaching Hospital',
    'https://www.cms.gov/medicare/payment/prospective-payment-systems/acute-inpatient-pps/indirect-medical-education-ime'
),
(
    3007,
    'designation',
    'Centers for Medicare & Medicaid Services',
    'https://www.cms.gov',
    'major_teaching_hospital',
    'Major Teaching Hospital',
    'https://www.cms.gov/medicare/payment/prospective-payment-systems/acute-inpatient-pps/indirect-medical-education-ime'
);


-- American Burn Association
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
    3010,
    'designation',
    'American Burn Association',
    'https://ameriburn.org',
    'burn_center_adult',
    'Adult Burn Center',
    'https://ameriburn.org/quality-care/burn-center-verification/'
),
(
    3011,
    'designation',
    'American Burn Association',
    'https://ameriburn.org',
    'burn_center_pediatric',
    'Pediatric Burn Center',
    'https://ameriburn.org/quality-care/burn-center-verification/'
),
(
    3012,
    'designation',
    'American Burn Association',
    'https://ameriburn.org',
    'burn_center_adult_pediatric',
    'Adult and Pediatric Burn Center',
    'https://ameriburn.org/quality-care/burn-center-verification/'
);
