-- INSERT statements for Psychosocial Therapist credentials
-- Social workers, behavioral, art, psychological therapy, mental health counselors, and addiction counselors

INSERT INTO dctnry.clinical_credential
  (id, credential_abbr, unique_credential_abbr, credential_name, credentialing_organization_name,
   credentialing_organization_url, credential_description, is_multisource, is_clinical,
   is_board_certification, is_credential_retired, is_fhir_credential, duplicate_abbreviation_code, created_at, updated_at)
VALUES
  (60000, 'LICSW', 'LICSW', 'Licensed Independent Clinical Social Worker', NULL, NULL, 'Advanced clinical social worker licensed to practice independently, providing psychotherapy and clinical services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60001, 'LCSW', 'LCSW', 'Licensed Clinical Social Worker',     NULL, NULL, 'Clinical social worker licensed to provide therapeutic services, mental health treatment, and psychosocial interventions.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60002, 'LPC', 'LPC', 'Licensed Professional Counselor',     NULL, NULL, 'Licensed mental health professional providing counseling and psychotherapy services for various psychological conditions.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60003, 'RBT', 'RBT', 'Registered Behavior Technician',      'Behavior Analyst Certification Board', 'https://www.bacb.com/', 'Paraprofessional who implements behavior analysis services under the supervision of a BCBA or BCaBA.', FALSE,  TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL),
  (60004, 'LMFT', 'LMFT', 'Licensed Marriage and Family Therapist', NULL, NULL, 'Licensed therapist specializing in relationship counseling, family therapy, and couples counseling.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60005, 'LMHC', 'LMHC', 'Licensed Mental Health Counselor',    NULL, NULL, 'Licensed professional counselor providing mental health services, therapy, and psychological support.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60006, 'BCBA', 'BCBA', 'Board Certified Behavior Analyst',    'Behavior Analyst Certification Board', 'https://www.bacb.com/', 'Board certified professional who designs, implements, and evaluates behavior analytic interventions.', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL),
  (60007, 'LSW', 'LSW', 'Licensed Social Worker',             NULL, NULL, 'Entry-level licensed social worker providing basic social work services and case management.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60008, 'LCPC', 'LCPC', 'Licensed Clinical Professional Counselor', NULL, NULL, 'Clinical counselor licensed to provide psychotherapy and mental health treatment services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60009, 'MFT', 'MFT', 'Marriage and Family Therapist',      NULL, NULL, 'Mental health professional specializing in relationship and family counseling and therapy.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL),
  (60010, 'LPCC', 'LPCC', 'Licensed Professional Clinical Counselor', NULL, NULL, 'Clinical counselor licensed to provide comprehensive mental health and psychotherapy services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60011, 'LCSW-C', 'LCSW-C', 'Licensed Clinical Social Worker - Clinical', NULL, NULL, 'Clinical social worker with specialized clinical endorsement for advanced therapeutic services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60012, 'LISW', 'LISW', 'Licensed Independent Social Worker', NULL, NULL, 'Independent social worker licensed to practice without supervision, providing advanced social work services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60013, 'LLMSW', 'LLMSW', 'Limited Licensed Master Social Worker', NULL, NULL, 'Master-level social worker with limited licensure requiring supervision for clinical practice.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60014, 'CDCA', 'CDCA', 'Certified Drug and Alcohol Counselor', NULL, NULL, 'Certified professional specializing in substance abuse counseling and addiction treatment services.', TRUE,  TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL),
  (60015, 'AMFT', 'AMFT', 'Associate Marriage and Family Therapist', NULL, NULL, 'Entry-level marriage and family therapist working under supervision to gain clinical experience.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60016, 'CSW', 'CSW', 'Clinical Social Worker',             NULL, NULL, 'Social worker with clinical training and experience in providing therapeutic and mental health services.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL),
  (60017, 'LCSW-R', 'LCSW-R', 'Licensed Clinical Social Worker - Registered', NULL, NULL, 'Registered clinical social worker with specific state registration for clinical practice.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60018, 'MHPP', 'MHPP', 'Mental Health Paraprofessional',     NULL, NULL, 'Paraprofessional providing support services in mental health settings under professional supervision.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60019, 'LCSWA', 'LCSWA', 'Licensed Clinical Social Worker Associate', NULL, NULL, 'Associate-level clinical social worker working under supervision toward independent practice.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60020, 'LCMHC', 'LCMHC', 'Licensed Clinical Mental Health Counselor', NULL, NULL, 'Clinical mental health counselor licensed to provide comprehensive psychological and therapeutic services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60021, 'ASW', 'ASW', 'Associate Social Worker',             NULL, NULL, 'Entry-level social worker working under supervision to gain experience toward full licensure.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60022, 'LADC', 'LADC', 'Licensed Alcohol and Drug Counselor', NULL, NULL, 'Licensed professional specializing in alcohol and drug addiction counseling and treatment.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60023, 'CADC', 'CADC', 'Certified Alcohol and Drug Counselor', NULL, NULL, 'Certified counselor specializing in substance abuse treatment and addiction recovery services.', TRUE,  TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL),
  (60024, 'LPCA', 'LPCA', 'Licensed Professional Counselor Associate', NULL, NULL, 'Associate-level professional counselor working under supervision toward full licensure.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL);

INSERT INTO dctnry.clinical_credential
  (id, credential_abbr, unique_credential_abbr, credential_name, credentialing_organization_name,
   credentialing_organization_url, credential_description, is_multisource, is_clinical,
   is_board_certification, is_credential_retired, is_fhir_credential, duplicate_abbreviation_code, created_at, updated_at)
VALUES
  (60025, 'QMHS', 'QMHS', 'Qualified Mental Health Specialist',  NULL, NULL, 'Mental health professional meeting state qualifications to provide specialized mental health services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60026, 'LISW-S', 'LISW-S', 'Licensed Independent Social Worker - Supervisor', NULL, NULL, 'Independent social worker with supervisory credentials for overseeing other social workers and clinical staff.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60027, 'MT-BC', 'MT-BC', 'Music Therapist Board Certified',    'Certification Board for Music Therapists', 'https://www.cbmt.org/', 'Board certified music therapist qualified to use music interventions for therapeutic purposes.', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL),
  (60028, 'LGSW', 'LGSW', 'Licensed Graduate Social Worker',    NULL, NULL, 'Graduate-level social worker with licensure to practice under supervision toward independent practice.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60029, 'MT', 'MT_1', 'Music Therapist',                     NULL, NULL, 'Professional who uses music-based interventions to address therapeutic goals in healthcare and educational settings.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 2, NULL, NULL),
  (60030, 'LLPC', 'LLPC', 'Limited Licensed Professional Counselor', NULL, NULL, 'Professional counselor with limited licensure requiring supervision for clinical practice.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60031, 'LGPC', 'LGPC', 'Licensed Graduate Professional Counselor', NULL, NULL, 'Graduate-level professional counselor working under supervision toward full licensure.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60032, 'ACSW', 'ACSW', 'Academy of Certified Social Workers', 'National Association of Social Workers', 'https://www.socialworkers.org/', 'NASW certification recognizing advanced competency and experience in social work practice.', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL),
  (60033, 'BT', 'BT_1', 'Behavior Technician',                NULL, NULL, 'Paraprofessional providing direct behavioral services under supervision of behavior analyst.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 3, NULL, NULL),
  (60034, 'LSCSW', 'LSCSW', 'Licensed Specialist Clinical Social Worker', NULL, NULL, 'Specialized clinical social worker with advanced licensure for independent clinical practice.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60035, 'BCABA', 'BCABA', 'Board Certified Assistant Behavior Analyst', 'Behavior Analyst Certification Board', 'https://www.bacb.com/', 'Board certified assistant who provides behavior analytic services under BCBA supervision.', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL),
  (60036, 'LMHCA', 'LMHCA', 'Licensed Mental Health Counselor Associate', NULL, NULL, 'Associate-level mental health counselor working under supervision toward full licensure.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60037, 'LCDC', 'LCDC', 'Licensed Chemical Dependency Counselor', NULL, NULL, 'Licensed counselor specializing in chemical dependency and substance abuse treatment.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60038, 'MFTI', 'MFTI', 'Marriage and Family Therapist Intern', NULL, NULL, 'Intern-level marriage and family therapist gaining supervised clinical experience.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60039, 'LCMHCA', 'LCMHCA', 'Licensed Clinical Mental Health Counselor Associate', NULL, NULL, 'Associate-level clinical mental health counselor working under supervision.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60040, 'LPC-A', 'LPC-A', 'Licensed Professional Counselor Associate', NULL, NULL, 'Associate-level professional counselor working under supervision toward independent practice.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60041, 'LBSW', 'LBSW', 'Licensed Bachelor Social Worker',    NULL, NULL, 'Bachelor-level social worker licensed to provide basic social work services under supervision.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60042, 'CTRS', 'CTRS', 'Certified Therapeutic Recreation Specialist', 'National Council for Therapeutic Recreation Certification', 'https://www.nctrc.org/', 'Certified professional using recreational activities to improve functioning and independence.', FALSE, TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL),
  (60043, 'CASAC', 'CASAC', 'Credentialed Alcoholism and Substance Abuse Counselor', NULL, NULL, 'State-credentialed counselor specializing in alcoholism and substance abuse treatment services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60044, 'QMHA', 'QMHA', 'Qualified Mental Health Associate',  NULL, NULL, 'Mental health professional meeting state qualifications to provide associate-level mental health services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60045, 'QBHP', 'QBHP', 'Qualified Behavioral Health Professional', NULL, NULL, 'Professional qualified to provide behavioral health services in various clinical settings.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60046, 'LPCC-S', 'LPCC-S', 'Licensed Professional Clinical Counselor - Supervisor', NULL, NULL, 'Clinical counselor with supervisory credentials for overseeing other mental health professionals.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60047, 'MHC', 'MHC', 'Mental Health Counselor',           NULL, NULL, 'Professional counselor providing mental health services and psychological support.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL),
  (60048, 'PSS', 'PSS', 'Peer Support Specialist',           NULL, NULL, 'Individual with lived experience providing peer support services in mental health and recovery settings.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60049, 'SA-C', 'SA-C', 'Substance Abuse Counselor Certified', NULL, NULL, 'Certified counselor specializing in substance abuse treatment and addiction recovery services.', TRUE,  TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL);

INSERT INTO dctnry.clinical_credential
  (id, credential_abbr, unique_credential_abbr, credential_name, credentialing_organization_name,
   credentialing_organization_url, credential_description, is_multisource, is_clinical,
   is_board_certification, is_credential_retired, is_fhir_credential, duplicate_abbreviation_code, created_at, updated_at)
VALUES
  (60050, 'PLMHP', 'PLMHP', 'Provisionally Licensed Mental Health Practitioner', NULL, NULL, 'Mental health practitioner with provisional licensure working toward full licensure requirements.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60051, 'LPC-MHSP', 'LPC-MHSP', 'Licensed Professional Counselor - Mental Health Service Provider', NULL, NULL, 'Licensed professional counselor designated as qualified mental health service provider.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60052, 'LISW-CP', 'LISW-CP', 'Licensed Independent Social Worker - Clinical Practice', NULL, NULL, 'Independent social worker licensed with specific authorization for clinical practice.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60053, 'LCSW-A', 'LCSW-A', 'Licensed Clinical Social Worker Associate', NULL, NULL, 'Associate-level clinical social worker working under supervision toward independent practice.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60054, 'SOCIAL-WORKER', 'SOCIAL-WORKER', 'Social Worker',              NULL, NULL, 'Professional who provides social services, case management, and psychosocial support to individuals and families.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL),
  (60055, 'MHC-LP', 'MHC-LP', 'Mental Health Counselor - Limited Permit', NULL, NULL, 'Mental health counselor with limited permit working under supervision.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60056, 'LAPC', 'LAPC', 'Licensed Associate Professional Counselor', NULL, NULL, 'Associate professional counselor licensed to practice under supervision.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60057, 'QMHP', 'QMHP', 'Qualified Mental Health Professional', NULL, NULL, 'Mental health professional meeting state qualifications to provide mental health services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60058, 'PSYCHOLOGIST', 'PSYCHOLOGIST', 'Psychologist',               NULL, NULL, 'Doctoral-level professional who studies behavior and mental processes, provides psychological assessment and therapy.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL),
  (60059, 'LMSW-CC', 'LMSW-CC', 'Licensed Master Social Worker - Clinical Certification', NULL, NULL, 'Master social worker with clinical certification endorsement for therapeutic services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60060, 'LLBSW', 'LLBSW', 'Limited Licensed Bachelor Social Worker', NULL, NULL, 'Bachelor-level social worker with limited licensure requiring supervision.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60061, 'LP', 'LP', 'Licensed Psychologist',             NULL, NULL, 'Doctoral-level psychologist licensed to practice psychology independently, including assessment and therapy.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60062, 'CASAC-T', 'CASAC-T', 'Credentialed Alcoholism and Substance Abuse Counselor - Trainee', NULL, NULL, 'Trainee-level substance abuse counselor working under supervision toward full credentialing.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60063, 'LCSWR', 'LCSWR', 'Licensed Clinical Social Worker - Restricted', NULL, NULL, 'Clinical social worker with restricted licensure requiring specific practice limitations.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60064, 'LPC-S', 'LPC-S', 'Licensed Professional Counselor - Supervisor', NULL, NULL, 'Professional counselor with supervisory credentials for overseeing other mental health professionals.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60065, 'LLP', 'LLP', 'Limited Licensed Psychologist',      NULL, NULL, 'Psychologist with limited licensure working under supervision toward full psychology licensure.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60066, 'APSW', 'APSW', 'Advanced Practice Social Worker',    NULL, NULL, 'Social worker with advanced practice credentials for specialized clinical and therapeutic services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60067, 'MHP', 'MHP', 'Mental Health Professional',         NULL, NULL, 'General credential for professionals providing mental health and behavioral health services.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL),
  (60068, 'CMHC', 'CMHC', 'Community Mental Health Counselor',  NULL, NULL, 'Mental health counselor specializing in community-based mental health services and programs.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL),
  (60069, 'LPC-IT', 'LPC-IT', 'Licensed Professional Counselor - In Training', NULL, NULL, 'Professional counselor in training working under supervision toward full licensure.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60070, 'CSAC', 'CSAC', 'Certified Substance Abuse Counselor', NULL, NULL, 'Certified counselor specializing in substance abuse treatment and addiction recovery services.', TRUE,  TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL),
  (60071, 'PPS', 'PPS', 'Peer Support Specialist',            NULL, NULL, 'Individual with lived experience providing peer support services in mental health and recovery settings.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60072, 'LMHP', 'LMHP', 'Licensed Mental Health Practitioner', NULL, NULL, 'Licensed practitioner providing comprehensive mental health services and therapeutic interventions.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60073, 'APCC', 'APCC', 'Associate Professional Clinical Counselor', NULL, NULL, 'Associate-level clinical counselor working under supervision toward independent practice.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60074, 'CPSS', 'CPSS', 'Certified Peer Support Specialist',  NULL, NULL, 'Certified peer support specialist with training to provide recovery-oriented services.', TRUE,  TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL);

INSERT INTO dctnry.clinical_credential
  (id, credential_abbr, unique_credential_abbr, credential_name, credentialing_organization_name,
   credentialing_organization_url, credential_description, is_multisource, is_clinical,
   is_board_certification, is_credential_retired, is_fhir_credential, duplicate_abbreviation_code, created_at, updated_at)
VALUES
  (60075, 'MSSW', 'MSSW', 'Master of Science in Social Work',   NULL, NULL, 'Graduate degree in social work with emphasis on scientific research and evidence-based practice.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL),
  (60076, 'COUNSELOR', 'COUNSELOR', 'Counselor',                       NULL, NULL, 'General professional designation for individuals providing counseling and therapeutic services.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL),
  (60077, 'LPC-ASSOCIATE', 'LPC-ASSOCIATE', 'Licensed Professional Counselor Associate', NULL, NULL, 'Associate-level professional counselor working under supervision toward independent licensure.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60078, 'LAMFT', 'LAMFT', 'Licensed Associate Marriage and Family Therapist', NULL, NULL, 'Associate-level marriage and family therapist licensed to practice under supervision.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60079, 'RMHCI', 'RMHCI', 'Registered Mental Health Counselor Intern', NULL, NULL, 'Registered intern working under supervision toward full mental health counselor licensure.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60080, 'PRSS', 'PRSS', 'Peer Recovery Support Specialist',   NULL, NULL, 'Individual with lived recovery experience providing peer support services in substance abuse treatment.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60081, 'SAC-IT', 'SAC-IT', 'Substance Abuse Counselor - In Training', NULL, NULL, 'Substance abuse counselor in training working under supervision toward full certification.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60082, 'BHRS', 'BHRS', 'Behavioral Health Rehabilitation Services', NULL, NULL, 'Professional providing behavioral health rehabilitation and recovery services to individuals with mental health conditions.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60083, 'SW', 'SW', 'Social Worker',                      NULL, NULL, 'Professional who provides social services, advocacy, and support to individuals, families, and communities.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL),
  (60084, 'CADC-II', 'CADC-II', 'Certified Alcohol and Drug Counselor II', NULL, NULL, 'Advanced level certified alcohol and drug counselor with enhanced training and experience requirements.', TRUE,  TRUE,  TRUE,  FALSE, FALSE, 0, NULL, NULL),
  (60085, 'DT', 'DT', 'Dance Therapist',                    NULL, NULL, 'Professional who uses movement and dance as therapeutic interventions to promote emotional, social, and physical health.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL),
  (60086, 'ALC', 'ALC', 'Addiction Licensed Counselor',       NULL, NULL, 'Licensed counselor specializing in addiction treatment and substance abuse recovery services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60087, 'LCADC', 'LCADC', 'Licensed Clinical Alcohol and Drug Counselor', NULL, NULL, 'Clinical-level licensed counselor specializing in comprehensive alcohol and drug addiction treatment.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60088, 'LCAS', 'LCAS', 'Licensed Clinical Addiction Specialist', NULL, NULL, 'Clinical specialist licensed to provide advanced addiction treatment and substance abuse counseling services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),
  (60089, 'LPA', 'LPA', 'Licensed Psychological Associate',   NULL, NULL, 'Licensed associate working under psychologist supervision to provide psychological services.', TRUE,  TRUE,  FALSE,  FALSE, FALSE, 0, NULL, NULL),

-- Additional Art and Creative Therapy Credentials
  (60090, 'ATR-BC', 'ATR-BC', 'Art Therapist Registered - Board Certified', 'Art Therapy Credentials Board', 'https://www.atcb.org', 'Board certified art therapist registered to use visual arts and creative processes for therapeutic purposes.', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL),
  (60091, 'LPAT', 'LPAT', 'Licensed Professional Art Therapist', NULL, NULL, 'State licensed professional art therapist authorized to practice art therapy independently.', TRUE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL),
  (60092, 'LCPAT', 'LCPAT', 'Licensed Clinical Professional Art Therapist', NULL, NULL, 'Clinical-level state licensed art therapist providing advanced art therapy services.', TRUE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL),

-- Specialized Psychotherapy Credentials
  (60093, 'EMDR', 'EMDR', 'Eye Movement Desensitization and Reprocessing', 'EMDR International Association', 'https://www.emdria.org', 'Specialized psychotherapy technique certification for treating trauma and PTSD using bilateral stimulation.', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL),

-- Neuropsychology Credentials
  (60094, 'NEUROPSYCHOLOGIST', 'NEUROPSYCHOLOGIST', 'Neuropsychologist', 'American Board of Professional Psychology', 'https://www.abpp.org', 'Board certified psychologist specializing in brain-behavior relationships, cognitive assessment, and neurological conditions.', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL),

-- Additional FDA List Mental Health Credentials
  (60095, 'MFCC', 'MFCC', 'Marriage, Family and Child Counselor', NULL, NULL, 'Licensed counselor specializing in marriage, family, and child therapy', TRUE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL); -- 60095
