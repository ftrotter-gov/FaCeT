#!/usr/bin/env python3
"""Verify that the ``sql/`` -> ``json/`` migration preserved every row of data.

Run with::

    python -m unittest test_sql_to_json -v
"""

from __future__ import annotations

import json
import os
import re
import unittest

import sql_to_json as converter

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SQL_DIR = os.path.join(PROJECT_ROOT, "sql")
JSON_DIR = os.path.join(PROJECT_ROOT, "json")

CLASS_KEY = converter.CREDENTIAL_CLASS_COLUMN
LIST_KEY = "credential_list"

SQL_FILES = converter.iter_insert_files(SQL_DIR)


def json_path_for(sql_path: str) -> str:
    name = os.path.basename(sql_path)[: -len(".sql")] + ".json"
    return os.path.join(JSON_DIR, name)


def load_json(sql_path: str):
    with open(json_path_for(sql_path), encoding="utf-8") as handle:
        return json.load(handle)


def read_sql(sql_path: str) -> str:
    with open(sql_path, encoding="utf-8") as handle:
        return handle.read()


def all_rows(groups) -> list[dict]:
    """Flatten the grouped JSON structure back into a single ordered row list."""
    return [row for group in groups for row in group[LIST_KEY]]


class MigrationTestCase(unittest.TestCase):
    """Assertions about the generated JSON files."""

    def test_sql_files_were_discovered(self):
        self.assertTrue(SQL_FILES, "no insert_*.sql files found in sql/")

    def test_every_sql_file_has_a_json_file(self):
        for sql_path in SQL_FILES:
            with self.subTest(sql=os.path.basename(sql_path)):
                self.assertTrue(
                    os.path.exists(json_path_for(sql_path)),
                    f"missing JSON output for {os.path.basename(sql_path)}",
                )

    def test_json_is_a_list_of_group_objects(self):
        for sql_path in SQL_FILES:
            with self.subTest(sql=os.path.basename(sql_path)):
                groups = load_json(sql_path)
                self.assertIsInstance(groups, list)
                self.assertTrue(groups, "file produced no groups")
                for group in groups:
                    self.assertIsInstance(group, dict)
                    self.assertIn(CLASS_KEY, group)
                    self.assertIn(LIST_KEY, group)
                    self.assertIsInstance(group[LIST_KEY], list)
                    self.assertTrue(group[LIST_KEY], "group has no rows")
                    for row in group[LIST_KEY]:
                        self.assertIsInstance(row, dict)

    def test_row_counts_match_the_sql_source(self):
        """The JSON must contain exactly as many rows as the SQL file declares."""
        for sql_path in SQL_FILES:
            with self.subTest(sql=os.path.basename(sql_path)):
                expected = len(converter.parse_rows(read_sql(sql_path)))
                actual = len(all_rows(load_json(sql_path)))
                self.assertEqual(expected, actual)

    def test_no_rows_were_lost_or_duplicated_overall(self):
        expected = sum(
            len(converter.parse_rows(read_sql(path))) for path in SQL_FILES
        )
        actual = sum(len(all_rows(load_json(path))) for path in SQL_FILES)
        self.assertEqual(expected, actual)
        self.assertEqual(864, actual, "expected 864 credential rows in total")

    def test_every_row_carries_a_credential_class(self):
        for sql_path in SQL_FILES:
            with self.subTest(sql=os.path.basename(sql_path)):
                for group in load_json(sql_path):
                    for row in group[LIST_KEY]:
                        self.assertIn(CLASS_KEY, row)
                        self.assertIsInstance(row[CLASS_KEY], str)
                        self.assertTrue(row[CLASS_KEY].strip())

    def test_row_class_matches_its_group_class(self):
        """The per-row copy of the class must agree with the group it lives in."""
        for sql_path in SQL_FILES:
            with self.subTest(sql=os.path.basename(sql_path)):
                for group in load_json(sql_path):
                    for row in group[LIST_KEY]:
                        self.assertEqual(group[CLASS_KEY], row[CLASS_KEY])

    def test_values_round_trip_from_the_sql(self):
        """Every field of every row must equal the value parsed from the SQL."""
        for sql_path in SQL_FILES:
            with self.subTest(sql=os.path.basename(sql_path)):
                expected_rows = converter.parse_rows(read_sql(sql_path))
                actual_rows = all_rows(load_json(sql_path))
                for expected, actual in zip(expected_rows, actual_rows):
                    clean = {k: v for k, v in expected.items() if k != "_line"}
                    self.assertEqual(clean, actual)

    def test_row_keys_match_the_insert_column_list(self):
        """JSON keys come from the INSERT column names, not positional indexes."""
        for sql_path in SQL_FILES:
            with self.subTest(sql=os.path.basename(sql_path)):
                text = read_sql(sql_path)
                declared = set()
                for match in re.finditer(
                    r"INSERT\s+INTO\s+[\w.]+\s*\(([^)]*)\)", text, re.IGNORECASE
                ):
                    for name in match.group(1).split(","):
                        if name.strip():
                            declared.add(name.strip())

                self.assertIn(CLASS_KEY, declared, "SQL is missing credential_class")
                for row in all_rows(load_json(sql_path)):
                    self.assertEqual(declared, set(row.keys()))

    def test_ids_are_unique_within_each_file(self):
        for sql_path in SQL_FILES:
            with self.subTest(sql=os.path.basename(sql_path)):
                ids = [row["id"] for row in all_rows(load_json(sql_path))]
                self.assertEqual(len(ids), len(set(ids)), "duplicate id values")

    def test_booleans_and_nulls_use_native_json_types(self):
        """TRUE/FALSE must become real booleans and NULL must become null."""
        for sql_path in SQL_FILES:
            with self.subTest(sql=os.path.basename(sql_path)):
                for row in all_rows(load_json(sql_path)):
                    self.assertIsInstance(row["id"], int)
                    for key, value in row.items():
                        if key.startswith("is_"):
                            self.assertIsInstance(value, bool)
                        self.assertNotIn(
                            value,
                            ("TRUE", "FALSE", "NULL"),
                            f"{key} kept a SQL keyword as a string",
                        )


class SpotCheckTestCase(unittest.TestCase):
    """Check specific, hand-verified records survived the migration intact."""

    def rows_by_id(self, json_name: str) -> dict[int, dict]:
        path = os.path.join(JSON_DIR, json_name)
        with open(path, encoding="utf-8") as handle:
            return {row["id"]: row for row in all_rows(json.load(handle))}

    def test_medical_doctor_record(self):
        row = self.rows_by_id("insert_credential_physicians.json")[1]
        self.assertEqual("MD", row["credential_abbr"])
        self.assertEqual("Medical Doctor", row["credential_name"])
        self.assertIsNone(row["credentialing_organization_name"])
        self.assertTrue(row["is_multisource"])
        self.assertTrue(row["is_clinical"])
        self.assertFalse(row["is_board_certification"])
        self.assertTrue(row["is_fhir_credential"])
        self.assertEqual(0, row["duplicate_abbreviation_code"])

    def test_homeopathic_rows_land_in_their_own_class(self):
        rows = self.rows_by_id("insert_credential_physicians.json")
        self.assertEqual("Homeopathic Medical Doctors", rows[19][CLASS_KEY])
        self.assertEqual("Homeopathic Medical Doctors", rows[20][CLASS_KEY])
        self.assertEqual("MD(H)", rows[19]["credential_abbr"])
        # The neighbouring row belongs to a different section.
        self.assertEqual("Physician Board Certifications", rows[21][CLASS_KEY])

    def test_board_certification_row_keeps_its_url(self):
        row = self.rows_by_id("insert_credential_physicians.json")[21]
        self.assertEqual("DABFP", row["credential_abbr"])
        self.assertEqual("https://www.theabfm.org/", row["credentialing_organization_url"])
        self.assertTrue(row["is_board_certification"])

    def test_duplicate_abbreviation_codes_are_preserved(self):
        row = self.rows_by_id("insert_credential_nurses_batch1.json")[1042]
        self.assertEqual("RN-BC", row["credential_abbr"])
        self.assertEqual("RN-BC_1", row["unique_credential_abbr"])
        self.assertEqual(2, row["duplicate_abbreviation_code"])
        self.assertTrue(row["is_credential_retired"])

    def test_non_ascii_credential_names_survive(self):
        row = self.rows_by_id("insert_credential_physicians.json")[10]
        self.assertEqual("醫學士 (Bachelor of Medicine)", row["credential_name"])

    def test_org_credential_multiline_rows(self):
        row = self.rows_by_id("insert_org_credential_snf.json")[10000]
        self.assertEqual("accreditation", row["category"])
        self.assertEqual("Accreditation Commission for Health Care", row["issuer"])
        self.assertEqual("achc_home_health_accreditation", row["credential_type"])
        self.assertFalse(row["is_cms_deeming_credential"])
        self.assertEqual("AHHC", row[CLASS_KEY])

    def test_org_credential_sections_are_split_by_issuer_comment(self):
        rows = self.rows_by_id("insert_org_credential_hospital_accreditation.json")
        self.assertEqual("Joint Commisssion Accreditations", rows[1][CLASS_KEY])
        self.assertEqual("The Joint Commission", rows[1]["issuer"])


class ParserTestCase(unittest.TestCase):
    """Unit tests for the parser itself, using small synthetic SQL snippets."""

    def test_trailing_row_comments_are_not_treated_as_classes(self):
        sql = (
            "-- Real Section\n"
            "INSERT INTO t (id, name) VALUES\n"
            "  (1, 'a'), -- 1\n"
            "  (2, 'b'); -- 2\n"
        )
        rows = converter.parse_rows(sql)
        self.assertEqual(2, len(rows))
        for row in rows:
            self.assertEqual("Real Section", row[CLASS_KEY])

    def test_comment_markers_inside_strings_are_ignored(self):
        sql = (
            "-- Section A\n"
            "INSERT INTO t (id, name) VALUES\n"
            "  (1, 'value with -- dashes inside'),\n"
            "  (2, 'plain');\n"
        )
        rows = converter.parse_rows(sql)
        self.assertEqual("value with -- dashes inside", rows[0]["name"])
        self.assertEqual("Section A", rows[1][CLASS_KEY])

    def test_inline_section_comments_split_a_single_values_block(self):
        sql = (
            "INSERT INTO t (id, name) VALUES\n"
            "  -- First Group\n"
            "  (1, 'a'),\n"
            "  -- Second Group\n"
            "  (2, 'b');\n"
        )
        groups = converter.group_rows(converter.parse_rows(sql))
        self.assertEqual(2, len(groups))
        self.assertEqual("First Group", groups[0][CLASS_KEY])
        self.assertEqual("Second Group", groups[1][CLASS_KEY])

    def test_escaped_quotes_are_decoded(self):
        sql = "-- S\nINSERT INTO t (id, name) VALUES (1, 'O''Brien');\n"
        self.assertEqual("O'Brien", converter.parse_rows(sql)[0]["name"])

    def test_adding_the_column_is_idempotent(self):
        sql = "-- S\nINSERT INTO t (id, name) VALUES (1, 'a');\n"
        once = converter.add_credential_class_to_sql(sql)
        self.assertIn(CLASS_KEY, once)
        self.assertEqual(once, converter.add_credential_class_to_sql(once))

    def test_sql_literal_rendering(self):
        self.assertEqual("NULL", converter.sql_literal(None))
        self.assertEqual("TRUE", converter.sql_literal(True))
        self.assertEqual("FALSE", converter.sql_literal(False))
        self.assertEqual("7", converter.sql_literal(7))
        self.assertEqual("'it''s'", converter.sql_literal("it's"))


if __name__ == "__main__":
    unittest.main()
