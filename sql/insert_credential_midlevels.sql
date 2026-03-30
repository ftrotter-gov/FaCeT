-- INSERT statements for Midlevel Provider credentials
-- Physician Assistants, Nurse Practitioners, and other advanced practice clinicians

INSERT INTO dctnry.clinical_credential
  (id, credential_abbr, unique_credential_abbr, credential_name, credentialing_organization_name,
   credentialing_organization_url, credential_description, is_multisource, is_clinical,
   is_board_certification, is_credential_retired, is_fhir_credential, duplicate_abbreviation_code, created_at, updated_at)
VALUES
  -- Certified Registered Nurse Anesthetists
  (5000, 'CRNA', 'CRNA', 'Certified Registered Nurse Anesthetist', 'National Board of Certification and Recertification for Nurse Anesthetists', 'https://www.nbcrna.com', 'Advanced practice registered nurse specializing in anesthesia care, providing anesthesia services in various healthcare settings', FALSE,  TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5000
  -- Family Nurse Practitioners
  (5001, 'FNP', 'FNP', 'Family Nurse Practitioner',              NULL, NULL, 'Advanced practice registered nurse providing primary care across the lifespan to individuals and families', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 5001
  -- Physician Assistants
  (5002, 'PA-C', 'PA-C', 'Physician Assistant Certified', 'National Commission on Certification of Physician Assistants', 'https://www.nccpa.net', 'Healthcare professional licensed to practice medicine with physician supervision, certified by the national certifying body', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5002
  (5003, 'PA', 'PA', 'Physician Assistant',           NULL, NULL, 'Healthcare professional licensed to practice medicine with physician supervision', TRUE,  TRUE,  FALSE, FALSE, TRUE, 0, NULL, NULL), -- 5003
  -- Advanced Practice Registered Nurses
  (5004, 'APRN-CNP', 'APRN-CNP', 'Advanced Practice Registered Nurse - Certified Nurse Practitioner', NULL, NULL, 'Advanced practice registered nurse with specialized graduate education and national certification in a nurse practitioner role', TRUE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5004
  -- General Nurse Practitioners
  (5005, 'NP', 'NP', 'Nurse Practitioner',                  NULL, NULL, 'Advanced practice registered nurse with graduate education providing healthcare services including diagnosis, treatment, and management of medical conditions', TRUE,  TRUE,  FALSE, FALSE, TRUE, 0, NULL, NULL), -- 5005
  -- Family Nurse Practitioner Certified
  -- Advanced Registered Nurse Practitioners
  (5007, 'ARNP', 'ARNP', 'Advanced Registered Nurse Practitioner', NULL, NULL, 'Advanced practice registered nurse with graduate education and expanded scope of practice', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 5007
  (5008, 'CRNP', 'CRNP', 'Certified Registered Nurse Practitioner', NULL, NULL, 'Certified registered nurse with advanced education and training to provide comprehensive healthcare services', TRUE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5008
  -- Board Certified Family Nurse Practitioners
  (5009, 'FNP-BC', 'FNP-BC', 'Family Nurse Practitioner Board Certified', 'American Nurses Credentialing Center', 'https://www.nursingworld.org/ancc', 'Board certified family nurse practitioner providing comprehensive primary care to individuals and families', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5009
  -- Certified Nurse Practitioners
  (5010, 'NP-C', 'NP-C', 'Nurse Practitioner Certified',       NULL, NULL, 'Nationally certified nurse practitioner with advanced education and training', TRUE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5010
  (5011, 'CNP', 'CNP', 'Certified Nurse Practitioner',       NULL, NULL, 'Certified nurse practitioner with advanced practice nursing education and national certification', TRUE,  TRUE,  TRUE,  FALSE, TRUE, 0, NULL, NULL), -- 5011
  -- Certified Nurse Midwives
  (5012, 'CNM', 'CNM', 'Certified Nurse Midwife',            'American Midwifery Certification Board', 'https://www.amcbmidwife.org', 'Advanced practice registered nurse providing comprehensive reproductive healthcare and midwifery services to women', FALSE,  TRUE,  TRUE,  FALSE, TRUE, 0, NULL, NULL), -- 5012
  -- Advanced Practice Nurses
  (5013, 'APN', 'APN', 'Advanced Practice Nurse',            NULL, NULL, 'Registered nurse with advanced graduate education and clinical training in a specialized area of nursing', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 5013
  -- Psychiatric Mental Health Nurse Practitioners
  (5014, 'PMHNP', 'PMHNP', 'Psychiatric Mental Health Nurse Practitioner', NULL, NULL, 'Advanced practice registered nurse specializing in mental health care, diagnosis and treatment of psychiatric disorders', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 5014
  (5015, 'PMHNP-BC', 'PMHNP-BC', 'Psychiatric Mental Health Nurse Practitioner Board Certified', 'American Nurses Credentialing Center', 'https://www.nursingworld.org/ancc', 'Board certified psychiatric mental health nurse practitioner providing comprehensive mental health services', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5015
  -- Physician Assistant Certified variants
  (5016, 'PAC', 'PAC', 'Physician Assistant Certified',      NULL, NULL, 'Certified physician assistant licensed to practice medicine under physician supervision', TRUE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5016
  -- Pediatric Nurse Practitioners
  (5017, 'CPNP', 'CPNP', 'Certified Pediatric Nurse Practitioner', 'Pediatric Nursing Certification Board', 'https://www.pncb.org', 'Certified nurse practitioner specializing in comprehensive healthcare for infants, children, and adolescents', FALSE, TRUE,  TRUE,  FALSE, TRUE, 0, NULL, NULL), -- 5017
  -- Adult Nurse Practitioners
  (5018, 'ANP', 'ANP', 'Adult Nurse Practitioner',           NULL, NULL, 'Nurse practitioner specializing in healthcare for adults across the adult lifespan', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL); -- 5018

INSERT INTO dctnry.clinical_credential
  (id, credential_abbr, unique_credential_abbr, credential_name, credentialing_organization_name,
   credentialing_organization_url, credential_description, is_multisource, is_clinical,
   is_board_certification, is_credential_retired, is_fhir_credential, duplicate_abbreviation_code, created_at, updated_at)
VALUES
  -- Advanced Practice Registered Nurse variants
  (5020, 'APNP', 'APNP', 'Advanced Practice Nurse Practitioner', NULL, NULL, 'Advanced practice nurse with graduate education providing comprehensive healthcare services', TRUE, TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 5020
  -- Pediatric Nurse Practitioners
  (5021, 'PNP', 'PNP', 'Pediatric Nurse Practitioner',       NULL, NULL, 'Nurse practitioner specializing in healthcare for infants, children, and adolescents', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 5021
  (5022, 'AGACNP-BC', 'AGACNP-BC', 'Adult-Gerontology Acute Care Nurse Practitioner Board Certified', 'American Nurses Credentialing Center', 'https://www.nursingworld.org/ancc', 'Board certified nurse practitioner specializing in acute care for adults and older adults', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5022
  -- Registered Physician Assistant variants
  (5023, 'RPA-C', 'RPA-C', 'Registered Physician Assistant Certified', NULL, NULL, 'Registered and certified physician assistant licensed to practice medicine under physician supervision', TRUE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5023
  -- Acute Care Nurse Practitioners
  (5024, 'ACNP', 'ACNP', 'Acute Care Nurse Practitioner',      NULL, NULL, 'Nurse practitioner specializing in acute and critical care across various healthcare settings', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 5024
  -- Neonatal Nurse Practitioners
  (5025, 'NNP', 'NNP', 'Neonatal Nurse Practitioner',        NULL, NULL, 'Nurse practitioner specializing in the care of newborns, especially high-risk and critically ill neonates', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 5025
  -- Women's Health Nurse Practitioners
  (5026, 'WHNP', 'WHNP', 'Womens Health Nurse Practitioner', NULL, NULL, 'Nurse practitioner specializing in comprehensive healthcare for women across the lifespan', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 5026
  -- Pediatric Nurse Practitioner Primary Care
  (5027, 'CPNP-PC', 'CPNP-PC', 'Certified Pediatric Nurse Practitioner Primary Care', 'Pediatric Nursing Certification Board', 'https://www.pncb.org', 'Certified nurse practitioner providing primary care to infants, children, and adolescents', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5027
  -- Certified Family Nurse Practitioners
  (5029, 'CFNP', 'CFNP', 'Certified Family Nurse Practitioner', NULL, NULL, 'Certified nurse practitioner providing comprehensive primary care to individuals and families', TRUE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5029
  -- Adult-Gerontology Nurse Practitioners
  (5031, 'AGPCNP-BC', 'AGPCNP-BC', 'Adult-Gerontology Primary Care Nurse Practitioner Board Certified', 'American Nurses Credentialing Center', 'https://www.nursingworld.org/ancc', 'Board certified nurse practitioner providing primary care to adults and older adults', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5031
  (5032, 'AGNP', 'AGNP', 'Adult-Gerontology Nurse Practitioner', NULL, NULL, 'Nurse practitioner specializing in healthcare for adults and older adults across care settings', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 5032
  (5033, 'WHNP-BC', 'WHNP-BC', 'Womens Health Nurse Practitioner Board Certified', 'National Certification Corporation', 'https://www.nccwebsite.org', 'Board certified nurse practitioner specializing in comprehensive womens health care', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5033
  -- Physician Assistant Students
  (5034, 'PA-S', 'PA-S', 'Physician Assistant Student',       NULL, NULL, 'Student enrolled in an accredited physician assistant educational program', TRUE, TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 5034
  -- Neonatal Nurse Practitioner Board Certified
  (5035, 'NNP-BC', 'NNP-BC', 'Neonatal Nurse Practitioner Board Certified', 'National Certification Corporation', 'https://www.nccwebsite.org', 'Board certified nurse practitioner specializing in neonatal care and high-risk newborn management', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5035
  -- Adult Nurse Practitioner Board Certified
  (5036, 'ANP-BC', 'ANP-BC', 'Adult Nurse Practitioner Board Certified', 'American Nurses Credentialing Center', 'https://www.nursingworld.org/ancc', 'Board certified nurse practitioner specializing in adult healthcare across the adult lifespan', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5036
  -- Acute Care Nurse Practitioner Board Certified
  (5037, 'ACNP-BC', 'ACNP-BC', 'Acute Care Nurse Practitioner Board Certified', 'American Nurses Credentialing Center', 'https://www.nursingworld.org/ancc', 'Board certified nurse practitioner specializing in acute and critical care management', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5037
  -- Master of Physician Assistant Studies
  (5038, 'MPAS', 'MPAS', 'Master of Physician Assistant Studies', NULL, NULL, 'Masters degree in physician assistant studies from an accredited educational program', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL); -- 5038

INSERT INTO dctnry.clinical_credential
  (id, credential_abbr, unique_credential_abbr, credential_name, credentialing_organization_name,
   credentialing_organization_url, credential_description, is_multisource, is_clinical,
   is_board_certification, is_credential_retired, is_fhir_credential, duplicate_abbreviation_code, created_at, updated_at)
VALUES
  -- Pediatric Nurse Practitioner Acute Care
  (5039, 'CPNP-AC', 'CPNP-AC', 'Certified Pediatric Nurse Practitioner - Acute Care', 'Pediatric Nursing Certification Board', 'https://www.pncb.org', 'Certified nurse practitioner specializing in acute care management for critically ill infants, children, and adolescents', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5039
  -- Adult Gerontology Acute Care Nurse Practitioner
  (5041, 'AGPCNP', 'AGPCNP', 'Adult Gerontology Primary Care Nurse Practitioner', NULL, NULL, 'Nurse practitioner providing primary care services to adults and older adults in outpatient and community settings', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 5041
  -- Registered Nurse Practitioner
  (5042, 'RNP', 'RNP', 'Registered Nurse Practitioner',      NULL, NULL, 'Registered nurse with advanced practice education and licensing to provide comprehensive healthcare services', TRUE,  TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5042
  -- Adult Gerontology Acute Care Nurse Practitioner
  (5043, 'AG-ACNP', 'AG-ACNP', 'Adult Gerontology - Acute Care Nurse Practitioner', NULL, NULL, 'Nurse practitioner specializing in acute care management for adult and geriatric patients in hospital settings', TRUE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5043
  -- Advanced Registered Nurse Practitioner Certified
  (5044, 'ARNP-C', 'ARNP-C', 'Advanced Registered Nurse Practitioner Certified', NULL, NULL, 'Advanced registered nurse practitioner with national certification and expanded scope of practice', TRUE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5044
  -- Adult Nurse Practitioner Certified
  (5045, 'ANP-C', 'ANP-C', 'Adult Nurse Practitioner Certified', NULL, NULL, 'Certified nurse practitioner specializing in comprehensive healthcare for adult patients', TRUE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5045
  -- Registered Physician Assistant
  (5046, 'RPA', 'RPA', 'Registered Physician Assistant',     NULL, NULL, 'Registered physician assistant licensed to practice medicine under physician supervision with expanded clinical privileges', TRUE,  TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 5046

-- Physician Assistant Fellowship Credentials
  (5047, 'FAAPA', 'FAAPA', 'Fellow of the American Academy of Physician Assistants', 'American Academy of Physician Assistants', 'https://www.aapa.org', 'Fellowship recognizing leadership in physician assistant profession', FALSE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL); -- 5047
