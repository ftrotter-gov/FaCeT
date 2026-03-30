-- INSERT statements for Doctor credentials (non-physician doctors)
-- Doctoral degrees that are not medical practice degrees

INSERT INTO dctnry.clinical_credential
  (id, credential_abbr, unique_credential_abbr, credential_name, credentialing_organization_name,
   credentialing_organization_url, credential_description, is_multisource, is_clinical,
   is_board_certification, is_credential_retired, is_fhir_credential, duplicate_abbreviation_code, created_at, updated_at)
VALUES
  (10000,  'DDS', 'DDS', 'Doctor of Dental Surgery',               'Accredited dental schools', 'https://www.ada.org/education-careers/dental-education/dental-schools', 'Doctoral degree in dentistry qualifying graduates to practice general dentistry', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10000
  (10001,  'DMD', 'DMD', 'Doctor of Medicine in Dentistry',        'Accredited dental schools', 'https://www.ada.org/education-careers/dental-education/dental-schools', 'Doctoral degree in dentistry equivalent to DDS, qualifying graduates to practice general dentistry', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10001
  (10002, 'PharmD', 'PharmD', 'Doctor of Pharmacy',            'ACPE-accredited pharmacy schools', 'https://www.acpe-accredit.org/', 'Professional doctoral degree for pharmacists to provide pharmaceutical care and medication therapy management', TRUE,  TRUE,  FALSE, FALSE, TRUE, 0, NULL, NULL), -- 10002
  (10003, 'PsyD', 'PsyD', 'Doctor of Psychology',          'APA-accredited psychology programs', 'https://www.apa.org/ed/accreditation', 'Professional doctoral degree in psychology emphasizing clinical practice and applied psychology', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10003
  (10004, 'DPT', 'DPT', 'Doctor of Physical Therapy',          'CAPTE-accredited PT programs', 'https://www.capteonline.org/', 'Entry-level doctoral degree for physical therapists to diagnose and treat movement dysfunction', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10004
  (10005, 'DC', 'DC', 'Doctor of Chiropractic',              'CCE-accredited chiropractic colleges', 'https://www.cce-usa.org/', 'Doctoral degree in chiropractic medicine focusing on diagnosis and treatment of neuromuscular disorders', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10005
  (10006, 'OD', 'OD', 'Doctor of Optometry',                 'ACOE-accredited optometry schools', 'https://www.theacoe.org/', 'Doctoral degree in optometry for comprehensive eye and vision care, including diagnosis and treatment of eye diseases', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10006
  (10007, 'DPM', 'DPM', 'Doctor of Podiatric Medicine',        'CPME-accredited podiatric medical schools', 'https://www.cpme.org/', 'Doctoral degree in podiatric medicine for comprehensive foot and ankle care, including surgery', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10007
  (10008, 'AuD', 'AuD', 'Doctor of Audiology',                'CAA-accredited audiology programs', 'https://caa.asha.org/', 'Professional doctoral degree in audiology for diagnosis and treatment of hearing and balance disorders', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10008
  (10009, 'DNP', 'DNP', 'Doctor of Nursing Practice',         'CCNE or ACEN-accredited nursing programs', 'https://www.aacnnursing.org/DNP', 'Practice-focused doctoral degree in nursing for advanced nursing practice and clinical leadership', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10009
  (10010, 'ND', 'ND', 'Doctor of Naturopathic Medicine',    'CNME-accredited naturopathic medical schools', 'https://cnme.org/', 'Doctoral degree in naturopathic medicine emphasizing natural healing methods and preventive care', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10010
  (10011, 'OTD', 'OTD', 'Doctor of Occupational Therapy',     'ACOTE-accredited OT programs', 'https://www.aota.org/education/accreditation', 'Entry-level doctoral degree in occupational therapy for helping people participate in meaningful activities', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10011
  (10012, 'NMD', 'NMD', 'Doctor of Naturopathic Medicine',    'CNME-accredited naturopathic medical schools', 'https://cnme.org/', 'Doctoral degree in naturopathic medicine (alternative abbreviation to ND) emphasizing natural healing methods', TRUE,  TRUE,  FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10012
  (10013, 'OMD', 'OMD', 'Oriental Medicine Doctor',           'ACAOM-accredited acupuncture and oriental medicine programs', 'https://acaom.org/', 'Doctoral degree in Oriental Medicine/Traditional Chinese Medicine including acupuncture and herbal medicine', TRUE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10013

-- Additional FDA List Non-Physician Doctor Credentials

-- Homeopathic Medicine Credentials
  (10014, 'BHMS', 'BHMS', 'Bachelor of Homeopathic Medicine and Surgery', NULL, NULL, 'Bachelor degree in homeopathic medicine and surgical practice', TRUE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 10014
  (10015, 'CCH', 'CCH', 'Certified in Classical Homeopathy', NULL, NULL, 'Certified practitioner of classical homeopathic medicine', TRUE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 10015
  (10016, 'DHANP', 'DHANP', 'Diplomate of the Homeopathic Academy of Naturopathic Physicians', 'Homeopathic Academy of Naturopathic Physicians', NULL, 'Diplomate-level certification in homeopathic medicine for naturopathic physicians', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 10016
  (10017, 'DHt', 'DHt', 'Diplomate in Homeotherapeutics', NULL, NULL, 'Diplomate certification in homeotherapeutic medicine and treatment', TRUE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 10017
  (10018, 'DNBHE', 'DNBHE', 'Diplomate of the National Board of Homeopathic Examiners', 'National Board of Homeopathic Examiners', NULL, 'Diplomate certification from the National Board of Homeopathic Examiners', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 10018
  (10019, 'RS Hom', 'RS Hom', 'Registered with the Society of Homeopaths', 'Society of Homeopaths', NULL, 'Registered homeopath with the Society of Homeopaths', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 10019

-- Chiropractic Specialty Credentials
  (10020, 'CCSP', 'CCSP', 'Certified Chiropractic Sports Physician', NULL, NULL, 'Chiropractor certified in sports medicine and athletic injury treatment', TRUE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 10020
  (10021, 'DACBN', 'DACBN', 'Diplomate of American Chiropractic Board of Nutrition', 'American Chiropractic Board of Nutrition', NULL, 'Diplomate certification in chiropractic nutrition and dietary counseling', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 10021

-- Osteopathic Specialty Credentials
  (10022, 'CSPOMM', 'CSPOMM', 'Certified Specialty of Proficiency in Osteopathic Manipulation Medicine', NULL, NULL, 'Certified specialty in osteopathic manipulative medicine techniques', TRUE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 10022
  (10023, 'AOBSPOMM', 'AOBSPOMM', 'American Osteopathic Board of Special Proficiency in Osteopathic Manipulative Medicine', 'American Osteopathic Board of Special Proficiency in OMM', NULL, 'Board certification in osteopathic manipulative medicine specialty', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 10023

-- Pain Management Credentials
  (10024, 'CAAPM', 'CAAPM', 'Clinical Associate of the American Academy of Pain Management', 'American Academy of Pain Management', NULL, 'Clinical associate certification in pain management', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 10024
  (10025, 'DAAPM', 'DAAPM', 'Diplomate of American Academy of Pain Management', 'American Academy of Pain Management', NULL, 'Diplomate certification in pain management', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 10025

-- Additional FHIR Credentials - Doctoral Degrees
  (10026, 'DBA', 'DBA', 'Doctor of Business Administration', NULL, NULL, 'Doctoral degree in business administration focusing on applied research and advanced business practice', TRUE, FALSE, FALSE, FALSE, TRUE, 0, NULL, NULL), -- 10026
  (10027, 'DED', 'DED', 'Doctor of Education', NULL, NULL, 'Professional doctoral degree in education for advanced educational leadership and practice', TRUE, FALSE, FALSE, FALSE, TRUE, 0, NULL, NULL), -- 10027
  (10028, 'PHE', 'PHE', 'Doctor of Engineering', NULL, NULL, 'Professional doctoral degree in engineering focusing on advanced engineering practice and applied research', TRUE, FALSE, FALSE, FALSE, TRUE, 0, NULL, NULL), -- 10028
  (10029, 'PHD', 'PHD', 'Doctor of Philosophy', NULL, NULL, 'Research doctoral degree representing the highest level of academic achievement in various fields of study', TRUE, FALSE, FALSE, FALSE, TRUE, 0, NULL, NULL), -- 10029
  (10030, 'PHS', 'PHS', 'Doctor of Science', NULL, NULL, 'Research or professional doctoral degree in scientific disciplines', TRUE, FALSE, FALSE, FALSE, TRUE, 0, NULL, NULL), -- 10030
  (10031, 'JD', 'JD', 'Juris Doctor', NULL, NULL, 'Professional doctoral degree in law required for legal practice in most jurisdictions', TRUE, FALSE, FALSE, FALSE, TRUE, 0, NULL, NULL); -- 10031
