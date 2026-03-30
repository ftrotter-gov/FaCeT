-- INSERT statements for Animal Clinician credentials
-- Veterinary medicine and other animal health professionals

INSERT INTO dctnry.clinical_credential
  (id, credential_abbr, unique_credential_abbr, credential_name, credentialing_organization_name,
   credentialing_organization_url, credential_description, is_multisource, is_clinical,
   is_board_certification, is_credential_retired, is_fhir_credential, duplicate_abbreviation_code, created_at, updated_at)
VALUES
  -- Veterinary Medicine (Non-Human Clinical)
  (80000, 'DVM', 'DVM', 'Doctor of Veterinary Medicine',      'Multiple veterinary schools', 'Various', 'Veterinary medicine doctorate', TRUE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL),
  (80001, 'VMD', 'VMD', 'Doctor of Veterinary Medicine',      'Multiple veterinary schools', 'Various', 'Veterinary medicine doctorate (variant of DVM)', TRUE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL),

-- Additional FDA List Veterinary Credentials
  (80002, 'BVScAH', 'BVScAH', 'Bachelor of Veterinary Science and Animal Husbandry', NULL, NULL, 'Bachelor degree in veterinary science with animal husbandry specialization', TRUE, TRUE, FALSE, FALSE, FALSE, 0, NULL, NULL), -- 80002
  (80003, 'CAC', 'CAC', 'Certified Animal Chiropractor', NULL, NULL, 'Certified chiropractor specializing in animal chiropractic care', TRUE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 80003
  (80004, 'CVA', 'CVA', 'Certified Veterinary Acupuncturist', NULL, NULL, 'Certified veterinarian or practitioner specializing in veterinary acupuncture', TRUE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL), -- 80004
  (80005, 'DACVD', 'DACVD', 'Diplomate of the American College of Veterinary Dermatology', 'American College of Veterinary Dermatology', NULL, 'Board certification in veterinary dermatology', FALSE, TRUE, TRUE, FALSE, FALSE, 0, NULL, NULL); -- 80005
