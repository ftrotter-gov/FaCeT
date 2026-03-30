-- INSERT statements for Non-clinical credentials
-- Includes all credentials where is_clinical = FALSE: academic degrees, administrative roles, legal credentials, veterinary, etc.

INSERT INTO dctnry.clinical_credential
  (id, credential_abbr, unique_credential_abbr, credential_name, credentialing_organization_name,
   credentialing_organization_url, credential_description, is_multisource, is_clinical,
   is_board_certification, is_credential_retired, is_fhir_credential, duplicate_abbreviation_code, created_at, updated_at)
VALUES
  -- Academic Degrees - Doctoral Level
  (90001, 'EdD', 'EdD', 'Doctor of Education',                 NULL, NULL, 'Professional doctoral degree for advanced practice in education leadership and policy', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90001
  (90002, 'DPH', 'DPH', 'Doctor of Public Health',           NULL, NULL, 'Professional doctoral degree focusing on population health, policy, and public health practice', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90002
  
  -- Academic Degrees - Master's Level
  (90003, 'MS', 'MS', 'Master of Science',                      NULL, NULL, 'Graduate degree in scientific, technical, or mathematical fields', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90003
  (90004, 'MPH', 'MPH', 'Master of Public Health',                NULL, NULL, 'Professional masters degree in public health practice and research', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90004
  (90005, 'MA', 'MA', 'Master of Arts',                NULL, NULL, 'Graduate degree in liberal arts, humanities, and social sciences', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90005
  (90006, 'MBA', 'MBA', 'Master of Business Administration', NULL, NULL, 'Professional masters degree in business management and administration', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90006
  (90007, 'MSW', 'MSW', 'Master of Social Work',               NULL, NULL, 'Professional masters degree for clinical and macro social work practice', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90007
  (90008, 'MSED', 'MSED', 'Master of Science in Education',     NULL, NULL, 'Graduate degree focusing on educational theory, research, and practice', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90008
  (90009, 'MED', 'MED', 'Master of Education',                NULL, NULL, 'Professional masters degree for educational leadership and teaching', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90009
  (90010, 'MPA', 'MPA', 'Master of Public Administration',   NULL, NULL, 'Professional masters degree for public sector management and policy', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90010
  (90011, 'MHA', 'MHA', 'Master of Health Administration',    NULL, NULL, 'Professional masters degree for healthcare management and administration', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90011
  (90012, 'MASTERS', 'MASTERS', 'Masters Degree',                    NULL, NULL, 'General masters level academic degree', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90012
  
  -- Academic Degrees - Bachelor's Level
  (90013, 'BA', 'BA', 'Bachelor of Arts',              NULL, NULL, 'Undergraduate degree in liberal arts, humanities, and social sciences', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90013
  (90014, 'BS', 'BS', 'Bachelor of Science',           NULL, NULL, 'Undergraduate degree in scientific, technical, or mathematical fields', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90014
  (90015, 'BSW', 'BSW', 'Bachelor of Social Work',            NULL, NULL, 'Professional undergraduate degree for entry-level social work practice', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90015
  
  -- Academic Degrees - Associate Level
  (90016, 'AA', 'AA', 'Associate of Arts',                   NULL, NULL, 'Two-year undergraduate degree in liberal arts and general studies', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90016
  
  -- Professional Certifications - Non-Clinical
  (90017, 'CPA', 'CPA', 'Certified Public Accountant',        'American Institute of CPAs', 'https://www.aicpa.org/', 'Professional certification for accounting and auditing practice', FALSE, FALSE, TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 90017
  (90018, 'CSFA', 'CSFA', 'Certified School Food Administrator', 'School Nutrition Association', 'https://schoolnutrition.org/', 'Professional certification for school food service management', FALSE, FALSE, TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 90018
  
  -- Health Information and Administrative Roles
  (90019, 'HIS', 'HIS', 'Health Information Specialist',       NULL, NULL, 'Professional specializing in health information management and systems', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90019
  (90020, 'CEO', 'CEO', 'Chief Executive Officer',             NULL, NULL, 'Executive leadership position responsible for organizational management', FALSE, FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90020
  (90021, 'LNHA', 'LNHA', 'Licensed Nursing Home Administrator', NULL, NULL, 'State-licensed administrator for long-term care facilities', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90021
  (90022, 'AO', 'AO', 'Administrative Officer',             NULL, NULL, 'Administrative professional responsible for organizational operations', FALSE, FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90022
  (90023, 'CRM', 'CRM', 'Certified Risk Manager',             'Risk and Insurance Management Society', 'https://www.rims.org/', 'Professional certification in organizational risk management', FALSE, FALSE, TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 90023
  (90024, 'NHA', 'NHA', 'Nursing Home Administrator',         NULL, NULL, 'Administrator responsible for nursing home operations and compliance', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90024
  (90025, 'ADMINISTRATOR', 'ADMINISTRATOR', 'Administrator',               NULL, NULL, 'General administrative role in healthcare or organizational settings', FALSE, FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90025
  (90026, 'STUDENT', 'STUDENT', 'Student',                           NULL, NULL, 'Individual enrolled in educational or training programs', FALSE, FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90026
  (90027, 'CMP', 'CMP', 'Certified Meeting Professional',     'Events Industry Council', 'https://www.eventscouncil.org/', 'Professional certification for meeting and event planning', FALSE, FALSE, TRUE,  FALSE, FALSE, 0, NULL, NULL), -- 90027
  
  -- Legal Credentials
  (90029, 'ESQ', 'ESQ', 'Esquire',                            NULL, NULL, 'Professional title for licensed attorneys admitted to the bar', TRUE,  FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90029
  

-- Additional Academic Degrees
  (90030, 'AAS', 'AAS', 'Associate of Applied Science',       NULL, NULL, 'Two-year degree typically in technical or applied fields', TRUE, FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90030

-- Study Groups and Professional Leagues (Non-Clinical)
  (90031, 'ASG', 'ASG', 'Affiliated Study Group',             NULL, NULL, 'Member of affiliated study group in medical specialty', TRUE, FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90031
  (90032, 'HASG', 'HASG', 'Homeopathic Affiliated Study Group', NULL, NULL, 'Member of homeopathic affiliated study group', TRUE, FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90032
  (90033, 'HSG', 'HSG', 'Homoeopathic Study Group',           NULL, NULL, 'Member of homeopathic study group', TRUE, FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90033
  (90034, 'SG', 'SG', 'Study Group',                        NULL, NULL, 'Member of medical specialty study group', TRUE, FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90034
  (90035, 'LL', 'LL', 'Laymens League',                     NULL, NULL, 'Member of medical laymens league', TRUE, FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 90035
  (90036, 'HLL', 'HLL', 'Homoeopathic Laymens League',        NULL, NULL, 'Member of homeopathic laymens league', TRUE, FALSE, FALSE, FALSE, FALSE, 0, NULL, NULL); -- 90036
