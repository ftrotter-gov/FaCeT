
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

-- Joint Commission Certifications
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
        1000,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_acute_myocardial_infarction_certification',
        'Joint Commission Acute Myocardial Infarction Certification',
        'https://www.jointcommission.org/en-us/certification/cardiac'
    ),
    (
        1001,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_chest_pain_certification',
        'Joint Commission Chest Pain Certification',
        'https://www.jointcommission.org/en-us/certification/cardiac'
    ),
    (
        1002,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_heart_failure_certification',
        'Joint Commission Heart Failure Certification',
        'https://www.jointcommission.org/en-us/certification/cardiac'
    ),
    (
        1003,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_comprehensive_cardiac_center_certification',
        'Joint Commission Comprehensive Cardiac Center Certification',
        'https://www.jointcommission.org/en-us/certification/cardiac'
    ),
    (
        1004,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_comprehensive_heart_attack_center_certification',
        'Joint Commission Comprehensive Heart Attack Center Certification',
        'https://www.jointcommission.org/en-us/certification/cardiac'
    ),
    (
        1005,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_advanced_heart_failure_certification',
        'Joint Commission Advanced Heart Failure Certification',
        'https://www.jointcommission.org/en-us/certification/cardiac'
    ),
    (
        1006,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_acute_heart_attack_ready_certification',
        'Joint Commission Acute Heart Attack Ready Certification',
        'https://www.jointcommission.org/en-us/certification/cardiac'
    ),
    (
        1007,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_primary_heart_attack_center_certification',
        'Joint Commission Primary Heart Attack Center Certification',
        'https://www.jointcommission.org/en-us/certification/cardiac'
    ),
    (
        1008,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_ventricular_assist_device_certification',
        'Joint Commission Ventricular Assist Device Certification',
        'https://www.jointcommission.org/en-us/certification/cardiac'
    ),
    (
        1009,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_centralized_sterilization_services_certification',
        'Joint Commission Centralized Sterilization Services Certification',
        'https://www.jointcommission.org/en-us/certification/centralized-sterilization-services'
    ),
    (
        1010,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_advanced_inpatient_diabetes_certification',
        'Joint Commission Advanced Inpatient Diabetes Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1011,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_bariatric_surgery_certification',
        'Joint Commission Bariatric Surgery Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1012,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_brain_tumor_certification',
        'Joint Commission Brain Tumor Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1013,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_lung_cancer_certification',
        'Joint Commission Lung Cancer Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1014,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_sepsis_certification',
        'Joint Commission Sepsis Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1015,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_wound_care_certification',
        'Joint Commission Wound Care Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1016,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_pneumonia_certification',
        'Joint Commission Pneumonia Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1017,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_tuberculosis_certification',
        'Joint Commission Tuberculosis Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1018,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_medication_compounding_certification',
        'Joint Commission Medication Compounding Certification',
        'https://www.jointcommission.org/en-us/certification/medication-compounding'
    ),
    (
        1019,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_hip_fracture_certification',
        'Joint Commission Hip Fracture Certification',
        'https://www.jointcommission.org/en-us/certification/orthopedic'
    ),
    (
        1020,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_joint_replacement_hip_certification',
        'Joint Commission Joint Replacement (Hip) Certification',
        'https://www.jointcommission.org/en-us/certification/orthopedic'
    ),
    (
        1021,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_joint_replacement_knee_certification',
        'Joint Commission Joint Replacement (Knee) Certification',
        'https://www.jointcommission.org/en-us/certification/orthopedic'
    ),
    (
        1022,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_joint_replacement_shoulder_certification',
        'Joint Commission Joint Replacement (Shoulder) Certification',
        'https://www.jointcommission.org/en-us/certification/orthopedic'
    ),
    (
        1023,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_spinal_fusion_certification',
        'Joint Commission Spinal Fusion Certification',
        'https://www.jointcommission.org/en-us/certification/orthopedic'
    ),
    (
        1024,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_spine_surgery_certification',
        'Joint Commission Spine Surgery Certification',
        'https://www.jointcommission.org/en-us/certification/orthopedic'
    ),
    (
        1025,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_advanced_spine_surgery_certification',
        'Joint Commission Advanced Spine Surgery Certification',
        'https://www.jointcommission.org/en-us/certification/orthopedic'
    ),
    (
        1026,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_advanced_total_hip_knee_replacement_certification',
        'Joint Commission Advanced Total Hip and Knee Replacement Certification',
        'https://www.jointcommission.org/en-us/certification/orthopedic'
    ),
    (
        1027,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_palliative_care_certification',
        'Joint Commission Palliative Care Certification',
        'https://www.jointcommission.org/en-us/certification/palliative-care'
    ),
    (
        1028,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_patient_blood_management_certification',
        'Joint Commission Patient Blood Management Certification',
        'https://www.jointcommission.org/en-us/certification/patient-blood-management'
    ),
    (
        1029,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_pediatric_asthma_certification',
        'Joint Commission Pediatric Asthma Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1030,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_outcomes_driven_perinatal_care_certification',
        'Joint Commission Outcomes-Driven Certification in Perinatal Care',
        'https://www.jointcommission.org/en-us/certification/perinatal-care'
    ),
    (
        1031,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_advanced_perinatal_care_certification',
        'Joint Commission Advanced Certification in Perinatal Care',
        'https://www.jointcommission.org/en-us/certification/perinatal-care'
    ),
    (
        1032,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_amputee_rehabilitation_certification',
        'Joint Commission Amputee Rehabilitation Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1033,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_brain_injury_rehabilitation_certification',
        'Joint Commission Brain Injury Rehabilitation Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1034,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_cardiac_rehabilitation_certification',
        'Joint Commission Cardiac Rehabilitation Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1035,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_hip_fracture_rehabilitation_certification',
        'Joint Commission Hip Fracture Rehabilitation Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1036,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_parkinsons_disease_rehabilitation_certification',
        'Joint Commission Parkinson''s Disease Rehabilitation Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1037,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_pulmonary_rehabilitation_certification',
        'Joint Commission Pulmonary Rehabilitation Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1038,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_spinal_cord_injury_rehabilitation_certification',
        'Joint Commission Spinal Cord Injury Rehabilitation Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1039,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_stroke_rehabilitation_certification',
        'Joint Commission Stroke Rehabilitation Certification',
        'https://www.jointcommission.org/en-us/certification/stroke'
    ),
    (
        1040,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_copd_certification',
        'Joint Commission COPD Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1041,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_integrated_care_certification',
        'Joint Commission Integrated Care Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1042,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_respiratory_failure_certification',
        'Joint Commission Respiratory Failure Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1043,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_lung_volume_reduction_surgery_certification',
        'Joint Commission Lung Volume Reduction Surgery Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1044,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_advanced_copd_certification',
        'Joint Commission Advanced COPD Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1045,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_chronic_kidney_disease_certification',
        'Joint Commission Chronic Kidney Disease Certification',
        'https://www.jointcommission.org/en-us/certification/disease-specific-care'
    ),
    (
        1046,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_acute_stroke_ready_hospital_certification',
        'Joint Commission Acute Stroke Ready Hospital Certification',
        'https://www.jointcommission.org/en-us/certification/stroke'
    ),
    (
        1047,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_comprehensive_stroke_center_certification',
        'Joint Commission Comprehensive Stroke Center Certification',
        'https://www.jointcommission.org/en-us/certification/stroke'
    ),
    (
        1048,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_primary_stroke_center_certification',
        'Joint Commission Primary Stroke Center Certification',
        'https://www.jointcommission.org/en-us/certification/stroke'
    ),
    (
        1049,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_thrombectomy_capable_stroke_center_certification',
        'Joint Commission Thrombectomy-Capable Stroke Center Certification',
        'https://www.jointcommission.org/en-us/certification/stroke'
    ),
    (
        1050,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_primary_care_medical_home_certification',
        'Joint Commission Primary Care Medical Home Certification',
        'https://www.jointcommission.org/en-us/certification/primary-care-medical-home'
    ),
    (
        1051,
        'certification',
        'The Joint Commission',
        'https://www.jointcommission.org',
        'jc_responsible_use_of_health_data_certification',
        'Joint Commission Responsible Use of Health Data Certification',
        'https://www.jointcommission.org/en-us/certification/responsible-use-of-health-data'
    );

-- American College of Surgeons
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
    1100,
    'certification',
    'American College of Surgeons',
    'https://www.facs.org',
    'acs_trauma_center_level_1_verification',
    'ACS Level I Trauma Center Verification',
    'https://www.facs.org/quality-programs/trauma/verification-review-and-consultation-program/'
),
(
    1101,
    'certification',
    'American College of Surgeons',
    'https://www.facs.org',
    'acs_trauma_center_level_2_verification',
    'ACS Level II Trauma Center Verification',
    'https://www.facs.org/quality-programs/trauma/verification-review-and-consultation-program/'
),
(
    1102,
    'certification',
    'American College of Surgeons',
    'https://www.facs.org',
    'acs_trauma_center_level_3_verification',
    'ACS Level III Trauma Center Verification',
    'https://www.facs.org/quality-programs/trauma/verification-review-and-consultation-program/'
),
(
    1103,
    'certification',
    'American College of Surgeons',
    'https://www.facs.org',
    'acs_trauma_center_level_4_verification',
    'ACS Level IV Trauma Center Verification',
    'https://www.facs.org/quality-programs/trauma/verification-review-and-consultation-program/'
),
(
    1104,
    'certification',
    'American College of Surgeons',
    'https://www.facs.org',
    'acs_commission_on_cancer_accreditation',
    'ACS Commission on Cancer Accredited Program',
    'https://www.facs.org/quality-programs/cancer-programs/commission-on-cancer/'
),
(
    1105,
    'certification',
    'American College of Surgeons',
    'https://www.facs.org',
    'acs_breast_center_accreditation',
    'ACS National Accreditation Program for Breast Centers (NAPBC)',
    'https://www.facs.org/quality-programs/cancer-programs/national-accreditation-program-for-breast-centers/'
),
(
    1106,
    'certification',
    'American College of Surgeons',
    'https://www.facs.org',
    'acs_rectal_cancer_program_accreditation',
    'ACS National Accreditation Program for Rectal Cancer (NAPRC)',
    'https://www.facs.org/quality-programs/cancer-programs/national-accreditation-program-for-rectal-cancer/'
),
(
    1107,
    'certification',
    'American College of Surgeons',
    'https://www.facs.org',
    'acs_bariatric_surgery_center_accreditation',
    'ACS MBSAQIP Accredited Bariatric Surgery Center',
    'https://www.facs.org/quality-programs/mbsaqip/'
),
(
    1108,
    'certification',
    'American College of Surgeons',
    'https://www.facs.org',
    'acs_childrens_surgery_center_verification',
    'ACS Children''s Surgery Center Verification',
    'https://www.facs.org/quality-programs/childrens-surgery-verification/'
);

-- American Heart Association
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
    1200,
    'certification',
    'American Heart Association',
    'https://www.heart.org',
    'aha_cardiac_care_certification',
    'American Heart Association Cardiac Care Certification',
    'https://www.heart.org/en/professional/quality-improvement/healthcare-certification'
),
(
    1201,
    'certification',
    'American Heart Association',
    'https://www.heart.org',
    'aha_heart_failure_certification',
    'American Heart Association Heart Failure Certification',
    'https://www.heart.org/en/professional/quality-improvement/healthcare-certification'
),
(
    1202,
    'certification',
    'American Heart Association',
    'https://www.heart.org',
    'aha_acute_coronary_syndrome_certification',
    'American Heart Association Acute Coronary Syndrome Certification',
    'https://www.heart.org/en/professional/quality-improvement/healthcare-certification'
),
(
    1203,
    'certification',
    'American Heart Association',
    'https://www.heart.org',
    'aha_stroke_system_of_care_certification',
    'American Heart Association Stroke System of Care Certification',
    'https://www.heart.org/en/professional/quality-improvement/healthcare-certification'
),
(
    1204,
    'certification',
    'American Heart Association',
    'https://www.heart.org',
    'aha_cardiac_rehabilitation_certification',
    'American Heart Association Cardiac Rehabilitation Certification',
    'https://www.heart.org/en/professional/quality-improvement/healthcare-certification'
);

-- American College of Radiology
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
    1300,
    'certification',
    'American College of Radiology',
    'https://www.acr.org',
    'acr_computed_tomography_accreditation',
    'ACR Computed Tomography (CT) Accreditation',
    'https://www.acraccreditation.org/modalities/ct'
),
(
    1301,
    'certification',
    'American College of Radiology',
    'https://www.acr.org',
    'acr_magnetic_resonance_imaging_accreditation',
    'ACR Magnetic Resonance Imaging (MRI) Accreditation',
    'https://www.acraccreditation.org/modalities/mri'
),
(
    1302,
    'certification',
    'American College of Radiology',
    'https://www.acr.org',
    'acr_mammography_accreditation',
    'ACR Mammography Accreditation',
    'https://www.acraccreditation.org/modalities/mammography'
),
(
    1303,
    'certification',
    'American College of Radiology',
    'https://www.acr.org',
    'acr_nuclear_medicine_accreditation',
    'ACR Nuclear Medicine Accreditation',
    'https://www.acraccreditation.org/modalities/nuclear-medicine'
),
(
    1304,
    'certification',
    'American College of Radiology',
    'https://www.acr.org',
    'acr_pet_accreditation',
    'ACR PET Accreditation',
    'https://www.acraccreditation.org/modalities/pet'
),
(
    1305,
    'certification',
    'American College of Radiology',
    'https://www.acr.org',
    'acr_radiation_oncology_accreditation',
    'ACR Radiation Oncology Accreditation',
    'https://www.acraccreditation.org/modalities/radiation-oncology'
),
(
    1306,
    'certification',
    'American College of Radiology',
    'https://www.acr.org',
    'acr_stereotactic_breast_biopsy_accreditation',
    'ACR Stereotactic Breast Biopsy Accreditation',
    'https://www.acraccreditation.org/modalities/stereotactic-breast-biopsy'
),
(
    1307,
    'certification',
    'American College of Radiology',
    'https://www.acr.org',
    'acr_ultrasound_accreditation',
    'ACR Ultrasound Accreditation',
    'https://www.acraccreditation.org/modalities/ultrasound'
),
(
    1308,
    'certification',
    'American College of Radiology',
    'https://www.acr.org',
    'acr_breast_imaging_center_of_excellence',
    'ACR Breast Imaging Center of Excellence',
    'https://www.acraccreditation.org/accreditation/bicoe'
);

-- American Nurses Credentialing Center
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
    1400,
    'certification',
    'American Nurses Credentialing Center',
    'https://www.nursingworld.org/ancc',
    'ancc_magnet_recognition',
    'ANCC Magnet Recognition Program',
    'https://www.nursingworld.org/organizational-programs/magnet/'
),
(
    1401,
    'certification',
    'American Nurses Credentialing Center',
    'https://www.nursingworld.org/ancc',
    'ancc_pathway_to_excellence',
    'ANCC Pathway to Excellence Designation',
    'https://www.nursingworld.org/organizational-programs/pathway/'
);

