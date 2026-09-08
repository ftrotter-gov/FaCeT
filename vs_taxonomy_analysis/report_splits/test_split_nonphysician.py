#!/usr/bin/env python3
"""Regression tests for the non-physician taxonomy mismatch split.

Run with::

    python -m unittest test_split_nonphysician -v

Guards two defects that were found in the original analysis:

1. Dental credentials (DDS/DMD/BDS) using 204E00000X "Oral & Maxillofacial Surgery
   (D.M.D.)" were reported as mismatches. They are correct -- OMFS practitioners hold
   both dental and medical degrees, and NUCC puts the dental degree in the code's own
   display name. 1,072 providers were affected.

2. Re-running the splitter silently destroyed the hand-authored analysis columns
   (should_use_tax / should_use_tax_description / match_strength), which cannot be
   regenerated from the source data.
"""

from __future__ import annotations

import csv
import os
import unittest

import split_nonphysician as splitter
from legitimate_pairs import is_legitimate_pair
from misdecoded_credentials import MISDECODED, is_confirmed_misdecode, lookup

HERE = os.path.dirname(os.path.abspath(__file__))

OMFS = "204E00000X"
ANESTH_ASSISTANT = "367H00000X"
SURGICAL_ASSISTANT = "246ZC0007X"


class LegitimatePairTests(unittest.TestCase):
    """The allow-list must recognise correct dual-degree pairings."""

    def test_dental_credentials_on_omfs_are_legitimate(self):
        for code, name in [
            ("DDS", "Doctor of Dental Surgery"),
            ("DMD", "Doctor of Medicine in Dentistry"),
            ("BDS", "Bachelor of Dental Surgery"),
            ("OMFS", "Oral and Maxillofacial Surgeon"),
        ]:
            with self.subTest(credential=code):
                self.assertTrue(is_legitimate_pair(code, name, OMFS))

    def test_case_and_whitespace_insensitive(self):
        self.assertTrue(is_legitimate_pair(" dds ", "Doctor of Dental Surgery", " 204e00000x "))

    def test_overloaded_oms_disambiguated_by_name(self):
        # "OMS" is used for BOTH Oral & Maxillofacial Surgery and Ostomy Management
        # Specialist. Only the oral/maxillofacial sense is legitimate.
        self.assertTrue(is_legitimate_pair("OMS", "Oral & Maxillofacial Surgery", OMFS))
        self.assertFalse(is_legitimate_pair("OMS", "Ostomy Management Specialist", OMFS))

    def test_unrelated_credentials_on_omfs_are_still_mismatches(self):
        for code, name in [
            ("PHD", "Doctor of Philosophy"),
            ("PC", "Pharmacist Clinician"),
            ("NP", "Nurse Practitioner"),
            ("MS", "Master of Science"),
        ]:
            with self.subTest(credential=code):
                self.assertFalse(is_legitimate_pair(code, name, OMFS))

    def test_dental_credential_on_other_physician_code_is_a_mismatch(self):
        # The allow-list is pair-scoped, not credential-scoped. A DDS using
        # Family Medicine is still an error.
        self.assertFalse(is_legitimate_pair("DDS", "Doctor of Dental Surgery", "207Q00000X"))


class ClassifyTests(unittest.TestCase):
    """Bucket routing, including the new rule-0 short circuit."""

    def test_legitimate_pairs_bypass_mismatch_buckets(self):
        self.assertEqual(splitter.classify("Doctor of Dental Surgery", "DDS", OMFS), "legit")

    def test_existing_routing_is_unchanged(self):
        self.assertEqual(splitter.classify("Family Nurse Practitioner", "FNP", "207Q00000X"), "np")
        self.assertEqual(splitter.classify("Physician Assistant", "PA", "207Q00000X"), "pa")
        self.assertEqual(splitter.classify("Registered Nurse", "RN", "207Q00000X"), "nurse")
        self.assertEqual(splitter.classify("Master of Science", "MS", "207Q00000X"), "master")
        self.assertEqual(splitter.classify("Physical Therapist", "PT", "208100000X"), "other")

    def test_np_rule_still_wins_over_pa(self):
        self.assertEqual(
            splitter.classify("Master of Physician Assistant Studies", "MPAS", "207Q00000X"),
            "pa",
        )


class MisdecodedCredentialTests(unittest.TestCase):
    """Credential abbreviations FaCeT expands to the wrong profession."""

    def test_known_misdecodes_are_registered(self):
        for code in ("AA", "CAA", "CSFA"):
            with self.subTest(credential=code):
                self.assertIsNotNone(lookup(code))

    def test_corroborated_rows_are_flagged(self):
        self.assertTrue(is_confirmed_misdecode("AA", "ANESTHESIOLOGY PHYSICIAN"))
        self.assertTrue(is_confirmed_misdecode("AA", "PEDIATRIC ANESTHESIOLOGY PHYSICIAN"))
        self.assertTrue(is_confirmed_misdecode("CAA", "ANESTHESIOLOGY PHYSICIAN"))
        self.assertTrue(is_confirmed_misdecode("CSFA", "SURGERY PHYSICIAN"))
        self.assertTrue(is_confirmed_misdecode("CSFA", "NEUROLOGICAL SURGERY PHYSICIAN"))

    def test_uncorroborated_rows_are_NOT_silently_converted(self):
        """
        The whole safety property: an "AA" on a Family Medicine code might really be an
        Associate of Arts, so it must stay in the mismatch report for a human.
        """
        self.assertFalse(is_confirmed_misdecode("AA", "FAMILY MEDICINE PHYSICIAN"))
        self.assertFalse(is_confirmed_misdecode("AA", "EMERGENCY MEDICINE PHYSICIAN"))
        self.assertFalse(is_confirmed_misdecode("CSFA", "FAMILY MEDICINE PHYSICIAN"))

    def test_orthopaedic_trauma_does_not_corroborate_csfa(self):
        """'ORTHOPAEDIC TRAUMA PHYSICIAN' contains no 'surg' -- must not auto-convert."""
        self.assertFalse(is_confirmed_misdecode("CSFA", "ORTHOPAEDIC TRAUMA PHYSICIAN"))

    def test_unknown_credentials_are_unaffected(self):
        self.assertFalse(is_confirmed_misdecode("FNP", "ANESTHESIOLOGY PHYSICIAN"))
        self.assertIsNone(lookup("FNP"))

    def test_case_insensitive(self):
        self.assertTrue(is_confirmed_misdecode(" caa ", "anesthesiology physician"))

    def test_corrections_point_at_real_nucc_codes(self):
        """Guard against typos in the correction targets."""
        nucc = os.path.join(HERE, os.pardir, "nucc_splits", "nucc_taxonomy_recent.csv")
        with open(nucc, newline="", encoding="utf-8-sig") as fh:
            valid = {row[0] for row in csv.reader(fh) if row}
        for code, entry in MISDECODED.items():
            with self.subTest(credential=code):
                self.assertIn(entry.correct_taxonomy, valid)

    def test_classify_routes_corroborated_rows_to_misdec(self):
        self.assertEqual(
            splitter.classify("Associate of Arts", "AA", "207L00000X",
                              "ANESTHESIOLOGY PHYSICIAN"),
            "misdec",
        )
        self.assertEqual(
            splitter.classify("Certified School Food Administrator", "CSFA",
                              "208600000X", "SURGERY PHYSICIAN"),
            "misdec",
        )

    def test_classify_keeps_uncorroborated_rows_in_normal_buckets(self):
        self.assertEqual(
            splitter.classify("Associate of Arts", "AA", "207Q00000X",
                              "FAMILY MEDICINE PHYSICIAN"),
            "other",
        )


class GeneratedOutputTests(unittest.TestCase):
    """Assertions against the committed output files."""

    @classmethod
    def setUpClass(cls):
        cls.files = {}
        for key, path in splitter.OUTPUTS.items():
            if os.path.exists(path):
                with open(path, newline="", encoding="utf-8-sig") as fh:
                    cls.files[key] = list(csv.DictReader(fh))

    def test_no_dental_omfs_rows_in_mismatch_files(self):
        """The 1,072-provider false positive must not reappear."""
        for key, rows in self.files.items():
            if key == "legit":
                continue
            offenders = [
                r for r in rows
                if r.get("chosenTaxonomyCode") == OMFS
                and is_legitimate_pair(
                    r.get("facetCredentialCode", ""),
                    r.get("facetCredentialName", ""),
                    OMFS,
                )
            ]
            with self.subTest(bucket=key):
                self.assertEqual(offenders, [], f"legitimate pairs leaked into {key}")

    def test_legitimate_pairs_file_holds_the_dental_rows(self):
        rows = self.files.get("legit")
        self.assertIsNotNone(rows, "LegitimatePairs.csv should be generated")
        codes = {r["facetCredentialCode"] for r in rows}
        self.assertIn("DDS", codes)
        self.assertIn("DMD", codes)

    def test_genuinely_odd_omfs_rows_still_reported(self):
        """PHD/PC on an OMFS code are unexplained and must stay visible for review."""
        remaining = {
            r["facetCredentialCode"]
            for key, rows in self.files.items() if key != "legit"
            for r in rows if r.get("chosenTaxonomyCode") == OMFS
        }
        self.assertIn("PHD", remaining)

    def test_all_files_carry_annotation_columns(self):
        for key, rows in self.files.items():
            if not rows:
                continue
            with self.subTest(bucket=key):
                for col in splitter.ANNOTATION_COLUMNS:
                    self.assertIn(col, rows[0].keys())

    def test_annotations_survived_regeneration(self):
        """Spot-check a known hand-authored mapping is still present."""
        rows = self.files.get("np", [])
        fnp = [r for r in rows if r["facetCredentialCode"] == "FNP"
               and r["chosenTaxonomyCode"] == "207Q00000X"]
        self.assertTrue(fnp, "expected the FNP / Family Medicine row")
        self.assertEqual(fnp[0]["should_use_tax"], "363LF0000X")
        self.assertEqual(fnp[0]["match_strength"], "3")

    def test_misdecoded_file_has_expected_population(self):
        rows = self.files.get("misdec")
        self.assertIsNotNone(rows, "MisdecodedCredentials.csv should be generated")
        by_cred = {}
        for r in rows:
            by_cred.setdefault(r["facetCredentialCode"], 0)
            by_cred[r["facetCredentialCode"]] += int(r["providerCount"])
        # 372 reported minus 6 uncorroborated singletons held back for review.
        self.assertEqual(by_cred.get("AA"), 179)
        self.assertEqual(by_cred.get("CAA"), 94)
        self.assertEqual(by_cred.get("CSFA"), 93)
        self.assertEqual(sum(by_cred.values()), 366)

    def test_misdecoded_rows_carry_correction_metadata(self):
        for r in self.files.get("misdec", []):
            with self.subTest(credential=r["facetCredentialCode"]):
                self.assertTrue(r["should_use_tax"])
                self.assertTrue(r["corrected_credential_name"])
                self.assertNotEqual(
                    r["current_credential_name"], r["corrected_credential_name"]
                )

    def test_anesthesia_and_surgical_targets_are_correct(self):
        targets = {
            r["facetCredentialCode"]: r["should_use_tax"]
            for r in self.files.get("misdec", [])
        }
        self.assertEqual(targets.get("AA"), ANESTH_ASSISTANT)
        self.assertEqual(targets.get("CAA"), ANESTH_ASSISTANT)
        self.assertEqual(targets.get("CSFA"), SURGICAL_ASSISTANT)

    def test_uncorroborated_misdecodes_remain_for_review(self):
        """The 6 held-back singletons must still be visible in the mismatch report."""
        held = [
            r for key, rows in self.files.items() if key not in ("legit", "misdec")
            for r in rows if r["facetCredentialCode"] in ("AA", "CAA", "CSFA")
        ]
        self.assertEqual(sum(int(r["providerCount"]) for r in held), 6)

    def test_row_total_is_conserved(self):
        """Every source row must land in exactly one output file."""
        with open(splitter.SOURCE, newline="", encoding="utf-8-sig") as fh:
            source_rows = sum(1 for r in csv.reader(fh) if len(r) >= 5) - 1
        written = sum(len(rows) for rows in self.files.values())
        self.assertEqual(written, source_rows)


if __name__ == "__main__":
    unittest.main()
