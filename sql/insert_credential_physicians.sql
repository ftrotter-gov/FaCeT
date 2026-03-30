-- INSERT statements for Physician credentials
-- Medical doctors who can practice medicine independently


INSERT INTO dctnry.clinical_credential
  (id, credential_abbr, unique_credential_abbr, credential_name, credentialing_organization_name,
   credentialing_organization_url, credential_description, is_multisource, is_clinical,
   is_board_certification, is_credential_retired, is_fhir_credential, duplicate_abbreviation_code, created_at, updated_at)
VALUES
  (1,  'MD', 'MD', 'Medical Doctor',                         NULL, NULL, 'Doctor of Medicine degree from accredited medical school, enabling independent practice of medicine after residency training.', TRUE,  TRUE,  FALSE, FALSE, TRUE, 0, NULL, NULL), -- 1
  (2, 'DO', 'DO', 'Doctor of Osteopathic Medicine',       NULL, NULL, 'Doctor of Osteopathic Medicine degree emphasizing holistic approach and manipulative treatment, equivalent to MD for medical practice.', TRUE,  TRUE,  FALSE, FALSE, TRUE, 0, NULL, NULL), -- 2
  (3, 'MBBS', 'MBBS', 'Bachelor of Medicine, Bachelor of Surgery', NULL, NULL, 'British and Commonwealth medical degree combining medicine and surgery training, equivalent to North American MD.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 3
  (4, 'MBChB', 'MBChB', 'Bachelor of Medicine, Bachelor of Surgery', NULL, NULL, 'British medical degree variant (Medicine, Surgery) granted by certain UK and Commonwealth universities, equivalent to MBBS.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 4
  (5, 'DR-MED', 'DR-MED', 'Doktor der Medizin', NULL, NULL, 'German medical doctorate degree, typically requiring dissertation, qualifying holder for medical practice in German-speaking countries.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 5
  (6, 'DOCTEUR', 'DOCTEUR', 'Docteur en Médecine', NULL, NULL, 'French medical doctorate degree qualifying holder to practice medicine in France and French-speaking countries.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 6
  (7, 'LAUREA-MED', 'LAUREA-MED', 'Laurea in Medicina e Chirurgia', NULL, NULL, 'Italian medical degree in Medicine and Surgery, qualifying holder for medical practice in Italy after specialization.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 7
  (8, 'LIC-MED', 'LIC-MED', 'Licenciado en Medicina', NULL, NULL, 'Spanish and Latin American medical licentiate degree qualifying holder for medical practice after completion of medical studies.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 8
  (9, 'MED-CIR', 'MED-CIR', 'Médico Cirujano', NULL, NULL, 'Latin American medical degree combining medicine and surgery, qualifying holder for general medical practice.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 9
  (10, 'YI-XUE-SHI', 'YI-XUE-SHI', '醫學士 (Bachelor of Medicine)', NULL, NULL, 'Chinese medical bachelor degree, foundational qualification for medical practice in Chinese-speaking regions.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10
  (11, 'YI-XUE-BO-SHI', 'YI-XUE-BO-SHI', '醫學博士 (Doctor of Medicine)', NULL, NULL, 'Chinese medical doctorate degree, advanced qualification for medical practice and research in Chinese-speaking regions.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 11
  (12, 'IRYO-GAKUSHI', 'IRYO-GAKUSHI', 'Iryō-gakushi (Bachelor of Medicine)', NULL, NULL, 'Japanese medical bachelor degree, qualifying holder for medical practice in Japan after passing national examinations.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 12
  (13, 'BMBS', 'BMBS', 'Bachelor of Medicine, Bachelor of Surgery (Cambridge)', NULL, NULL, 'Cambridge University variant of British medical degree, equivalent to other MBBS degrees for medical practice.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 13
  (14, 'MBBCH', 'MBBCH', 'Bachelor of Medicine, Bachelor of Surgery (Oxford)', NULL, NULL, 'Oxford University variant of British medical degree, equivalent to other MBBS degrees for medical practice.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 14
  (15, 'BMED', 'BMED', 'Bachelor of Medicine', NULL, NULL, 'Medical bachelor degree variant used by some universities, foundational qualification for medical practice.', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 15

-- Physician Fellowship Credentials
  (16, 'FAAP', 'FAAP', 'Fellow of the American Academy of Pediatrics', 'American Academy of Pediatrics', 'https://www.aap.org', 'Fellowship recognizing distinguished service and contributions to pediatric medicine and child health advocacy.', FALSE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 16
  (17, 'FAAOS', 'FAAOS', 'Fellow of the American Academy of Orthopedic Surgeons', 'American Academy of Orthopedic Surgeons', 'https://www.aaos.org', 'Fellowship recognizing significant contributions to orthopedic surgery, education, and musculoskeletal health.', FALSE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 17
  (18, 'FAAFP', 'FAAFP', 'Fellow of the American Academy of Family Physicians', 'American Academy of Family Physicians', 'https://www.aafp.org', 'Fellowship recognizing excellence and leadership in family medicine practice, education, and community service.', FALSE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 18

-- Homeopathic Medical Doctors
  (19, 'MD(H)', 'MD(H)', 'Homeopathic Medical Doctor (Arizona)', NULL, NULL, 'Medical doctor with homeopathic specialization licensed in Arizona', TRUE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 19
  (20, 'HMD', 'HMD', 'Homeopathic Medical Doctor (Nevada)', NULL, NULL, 'Homeopathic medical doctor licensed specifically in Nevada', TRUE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 20

-- Physician Board Certifications
  (21, 'DABFP', 'DABFP', 'Diplomate of the American Board of Family Practice', 'American Board of Family Medicine', 'https://www.theabfm.org/', 'Board certification in family medicine practice', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 21
  (22, 'DABIM', 'DABIM', 'Diplomate of the American Board of Internal Medicine', 'American Board of Internal Medicine', 'https://www.abim.org/', 'Board certification in internal medicine', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 22
  (23, 'ABFP', 'ABFP', 'American Board of Family Practitioners', 'American Board of Family Medicine', 'https://www.theabfm.org/', 'Board certification by American Board of Family Practitioners', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 23
  (24, 'ABO', 'ABO', 'American Board of Otolaryngology', 'American Board of Otolaryngology', 'https://www.aboto.org/', 'Board certification in otolaryngology (ENT) medicine', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 24
  (25, 'ABPN', 'ABPN', 'American Board of Psychiatry and Neurology', 'American Board of Psychiatry and Neurology', 'https://www.abpn.com/', 'Board certification in psychiatry and neurology', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 25
  (26, 'AOBFP', 'AOBFP', 'American Osteopathic Board of Family Physicians', 'American Osteopathic Board of Family Physicians', NULL, 'Board certification in osteopathic family medicine', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 26

-- Additional Physician Fellowship Credentials
  (27, 'FACFO', 'FACFO', 'Fellow of the American College of Foot Orthopedics', 'American College of Foot and Ankle Orthopedics and Medicine', NULL, 'Fellowship in foot orthopedics and podiatric medicine', FALSE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 27
  (28, 'FACOG', 'FACOG', 'Fellow of the American College of Obstetrics and Gynecology', 'American College of Obstetricians and Gynecologists', 'https://www.acog.org/', 'Fellowship in obstetrics and gynecology', FALSE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 28
  (29, 'FAAEM', 'FAAEM', 'Fellow of the American Academy of Environmental Medicine', 'American Academy of Environmental Medicine', 'https://aaemonline.org/', 'Fellowship in environmental medicine', FALSE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL), --29
  (30, 'FAAC', 'FAAC', 'Fellow of the American College of Cardiology', 'American College of Cardiology', 'https://www.acc.org/', 'Fellowship in cardiology', FALSE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL) --30
  ; 
