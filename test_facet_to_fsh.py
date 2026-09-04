#!/usr/bin/env python3
"""Verify that ``facet_to_fsh.py`` faithfully compiles ``json/`` into FSH.

Run with::

    python -m unittest test_facet_to_fsh -v
"""

from __future__ import annotations

import os
import re
import tempfile
import unittest

import facet_to_fsh as compiler

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(PROJECT_ROOT, "json")

CODE_RE = re.compile(r"^\* concept\[\+\]\.code = #(.*)$")
DISPLAY_RE = re.compile(r"^\* concept\[=\]\.display = \"(.*)\"$")
DEFINITION_RE = re.compile(r"^\* concept\[=\]\.definition = \"(.*)\"$")
PROP_CODE_RE = re.compile(r"^\* concept\[=\]\.property\[\+\]\.code = \S+#(\S+)$")
PROP_STRING_RE = re.compile(r"^\* concept\[=\]\.property\[=\]\.valueString = \"(.*)\"$")
PROP_BOOLEAN_RE = re.compile(r"^\* concept\[=\]\.property\[=\]\.valueBoolean = (\S+)$")


def generated_lines(text: str) -> list[str]:
    """Return the generated concept block, excluding the hand-authored preamble."""
    _, _, generated = text.partition("\n// FaCeT ")
    return generated.split("\n")


def parse_concepts(text: str) -> list[dict]:
    """Re-parse generated FSH back into concept dictionaries.

    This lets the tests assert a real round trip rather than string matching.
    """
    concepts: list[dict] = []
    pending: str | None = None

    for line in generated_lines(text):
        match = CODE_RE.match(line)
        if match:
            concepts.append({"code": match.group(1), "properties": {}})
            pending = None
            continue
        if not concepts:
            continue
        current = concepts[-1]

        match = DISPLAY_RE.match(line)
        if match:
            current["display"] = match.group(1)
            continue
        match = DEFINITION_RE.match(line)
        if match:
            current["definition"] = match.group(1)
            continue
        match = PROP_CODE_RE.match(line)
        if match:
            pending = match.group(1)
            continue
        match = PROP_STRING_RE.match(line)
        if match:
            current["properties"][pending] = match.group(1)
            pending = None
            continue
        match = PROP_BOOLEAN_RE.match(line)
        if match:
            current["properties"][pending] = match.group(1) == "true"
            pending = None

    return concepts


class CredentialFshTests(unittest.TestCase):
    """Tests for the individual clinician credential file."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = compiler.load_credential_rows(JSON_DIR)
        cls.text = compiler.build_credentials(JSON_DIR)
        cls.concepts = parse_concepts(cls.text)

    def test_every_row_becomes_one_concept(self) -> None:
        self.assertEqual(len(self.concepts), len(self.rows))
        self.assertEqual(compiler.concept_count(self.text), len(self.rows))

    def test_rows_are_ordered_by_id(self) -> None:
        ids = [row["id"] for row in self.rows]
        self.assertEqual(ids, sorted(ids))
        # Ids are a manually curated primary key, so they must be unique.
        self.assertEqual(len(set(ids)), len(ids))

    def test_codes_are_unique_and_have_no_whitespace(self) -> None:
        codes = [concept["code"] for concept in self.concepts]
        self.assertEqual(len(set(codes)), len(codes))
        for code in codes:
            self.assertTrue(code, "empty concept code")
            self.assertNotIn(" ", code, f"FSH codes cannot contain spaces: {code!r}")

    def test_codes_match_unique_credential_abbr(self) -> None:
        for row, concept in zip(self.rows, self.concepts):
            expected = row["unique_credential_abbr"].replace(" ", "_")
            self.assertEqual(concept["code"], expected)

    def test_display_and_definition_round_trip(self) -> None:
        for row, concept in zip(self.rows, self.concepts):
            self.assertEqual(concept["display"], row["credential_abbr"])
            self.assertEqual(concept["definition"], row["credential_name"])

    def test_string_properties_round_trip(self) -> None:
        for row, concept in zip(self.rows, self.concepts):
            for key, prop in compiler.CREDENTIAL_STRING_PROPERTIES:
                value = row.get(key)
                sentinel = (
                    prop == "cred_url"
                    and str(value).strip() in compiler.SKIP_URL_SENTINELS
                )
                if not compiler.has_value(value) or sentinel:
                    self.assertNotIn(
                        prop,
                        concept["properties"],
                        f"{concept['code']}: {prop} should have been omitted",
                    )
                else:
                    self.assertEqual(concept["properties"][prop], str(value).strip())

    def test_boolean_properties_round_trip(self) -> None:
        for row, concept in zip(self.rows, self.concepts):
            for key in compiler.CREDENTIAL_BOOLEAN_PROPERTIES:
                self.assertEqual(concept["properties"][key], bool(row.get(key)))

    def test_various_url_sentinel_is_omitted(self) -> None:
        sentinel_rows = [
            row
            for row in self.rows
            if str(row.get("credentialing_organization_url")).strip()
            in compiler.SKIP_URL_SENTINELS
        ]
        self.assertTrue(sentinel_rows, "expected at least one 'Various' URL in the data")
        by_code = {concept["code"]: concept for concept in self.concepts}
        for row in sentinel_rows:
            code = row["unique_credential_abbr"].replace(" ", "_")
            self.assertNotIn("cred_url", by_code[code]["properties"])

    def test_unicode_is_preserved(self) -> None:
        # The README promises unicode credentials, e.g. the Chinese Bachelor of
        # Medicine. Guard against mojibake regressions.
        self.assertIn("醫學士 (Bachelor of Medicine)", self.text)
        self.assertNotIn("\ufffd", self.text)

    def test_preamble_is_preserved(self) -> None:
        self.assertTrue(self.text.startswith(compiler.CREDENTIAL_PREAMBLE))
        self.assertIn("ValueSet: FaCeTcredentialVS", self.text)
        self.assertIn("Instance: FaCeT-credentialCS", self.text)

    def test_file_ends_with_single_newline(self) -> None:
        self.assertTrue(self.text.endswith("\n"))
        self.assertFalse(self.text.endswith("\n\n"))

    def test_known_concept_renders_exactly(self) -> None:
        cs = compiler.CREDENTIAL_PROPERTIES_CS
        expected = "\n".join(
            [
                "* concept[+].code = #DVM",
                '* concept[=].display = "DVM"',
                '* concept[=].definition = "Doctor of Veterinary Medicine"',
                f"* concept[=].property[+].code = {cs}#cred_org",
                '* concept[=].property[=].valueString = "Multiple veterinary schools"',
                f"* concept[=].property[+].code = {cs}#description",
                '* concept[=].property[=].valueString = "Veterinary medicine doctorate"',
                f"* concept[=].property[+].code = {cs}#is_multisource",
                "* concept[=].property[=].valueBoolean = true",
                f"* concept[=].property[+].code = {cs}#is_clinical",
                "* concept[=].property[=].valueBoolean = true",
                f"* concept[=].property[+].code = {cs}#is_board_certification",
                "* concept[=].property[=].valueBoolean = false",
            ]
        )
        self.assertIn(expected, self.text)


class OrgCredentialFshTests(unittest.TestCase):
    """Tests for the organizational credential file."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = compiler.load_org_rows(JSON_DIR)
        cls.text = compiler.build_org_credentials(JSON_DIR)
        cls.concepts = parse_concepts(cls.text)

    def test_every_row_becomes_one_concept(self) -> None:
        self.assertEqual(len(self.concepts), len(self.rows))

    def test_rows_are_ordered_by_id(self) -> None:
        ids = [row["id"] for row in self.rows]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(len(set(ids)), len(ids))

    def test_code_is_the_id(self) -> None:
        for row, concept in zip(self.rows, self.concepts):
            self.assertEqual(concept["code"], str(row["id"]))

    def test_display_round_trips_and_no_definition(self) -> None:
        for row, concept in zip(self.rows, self.concepts):
            self.assertEqual(concept["display"], row["display"])
            # Organizational concepts intentionally carry no definition.
            self.assertNotIn("definition", concept)

    def test_string_properties_round_trip(self) -> None:
        for row, concept in zip(self.rows, self.concepts):
            for key, prop in compiler.ORG_STRING_PROPERTIES:
                value = row.get(key)
                if compiler.has_value(value):
                    self.assertEqual(concept["properties"][prop], str(value).strip())
                else:
                    self.assertNotIn(prop, concept["properties"])

    def test_boolean_properties_round_trip(self) -> None:
        for row, concept in zip(self.rows, self.concepts):
            for key in compiler.ORG_BOOLEAN_PROPERTIES:
                self.assertEqual(concept["properties"][key], bool(row.get(key)))

    def test_credential_type_is_unique(self) -> None:
        # credential_type is declared UNIQUE in create_org_credential.sql.
        types = [row["credential_type"] for row in self.rows]
        self.assertEqual(len(set(types)), len(types))

    def test_preamble_is_preserved(self) -> None:
        self.assertTrue(self.text.startswith(compiler.ORG_PREAMBLE))
        self.assertIn("ValueSet: FaCeTorganizationCredentialVS", self.text)
        self.assertIn("Instance: FaCeT-org-credentialCS", self.text)

    def test_known_concept_renders_exactly(self) -> None:
        cs = compiler.ORG_PROPERTIES_CS
        url = (
            "https://www.jointcommission.org/accreditation-and-certification"
            "/health-care-settings/hospital/"
        )
        expected = "\n".join(
            [
                "* concept[+].code = #1",
                '* concept[=].display = "Joint Commission Hospital Accreditation"',
                f"* concept[=].property[+].code = {cs}#credential_category",
                '* concept[=].property[=].valueString = "accreditation"',
                f"* concept[=].property[+].code = {cs}#issuer",
                '* concept[=].property[=].valueString = "The Joint Commission"',
                f"* concept[=].property[+].code = {cs}#issuer_url",
                '* concept[=].property[=].valueString = "https://www.jointcommission.org"',
                f"* concept[=].property[+].code = {cs}#credential_type",
                '* concept[=].property[=].valueString = "jc_hospital_accreditation"',
                f"* concept[=].property[+].code = {cs}#credential_url",
                f'* concept[=].property[=].valueString = "{url}"',
                f"* concept[=].property[+].code = {cs}#is_credential_retired",
                "* concept[=].property[=].valueBoolean = false",
                f"* concept[=].property[+].code = {cs}#is_cms_deeming_credential",
                "* concept[=].property[=].valueBoolean = false",
            ]
        )
        self.assertIn(expected, self.text)


class EmitterTests(unittest.TestCase):
    """Unit tests for the low-level FSH emitters."""

    def test_fsh_code_replaces_spaces(self) -> None:
        self.assertEqual(compiler.fsh_code("RS Hom"), "RS_Hom")
        self.assertEqual(compiler.fsh_code("DAc (RI)"), "DAc_(RI)")
        self.assertEqual(compiler.fsh_code(1), "1")

    def test_fsh_string_escapes_quotes_and_backslashes(self) -> None:
        self.assertEqual(compiler.fsh_string('a "b"'), 'a \\"b\\"')
        self.assertEqual(compiler.fsh_string("a\\b"), "a\\\\b")

    def test_fsh_string_folds_newlines(self) -> None:
        self.assertEqual(compiler.fsh_string("a\nb"), "a b")
        self.assertEqual(compiler.fsh_string("a\r\nb"), "a b")

    def test_has_value(self) -> None:
        self.assertFalse(compiler.has_value(None))
        self.assertFalse(compiler.has_value(""))
        self.assertFalse(compiler.has_value("   "))
        self.assertTrue(compiler.has_value("x"))

    def test_boolean_property_renders_bare_literals(self) -> None:
        lines = compiler.boolean_property("CS", "is_clinical", True)
        self.assertEqual(lines[1], "* concept[=].property[=].valueBoolean = true")
        lines = compiler.boolean_property("CS", "is_clinical", False)
        self.assertEqual(lines[1], "* concept[=].property[=].valueBoolean = false")
        # None is falsey and must still render as a valid FSH boolean.
        lines = compiler.boolean_property("CS", "is_clinical", None)
        self.assertEqual(lines[1], "* concept[=].property[=].valueBoolean = false")


class CliTests(unittest.TestCase):
    """Tests for the command line interface."""

    def test_out_dir_is_required(self) -> None:
        with self.assertRaises(SystemExit):
            compiler.parse_args([])

    def test_writes_both_files_and_then_passes_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            exit_code = compiler.main(["--out-dir", tmp, "--json-dir", JSON_DIR])
            self.assertEqual(exit_code, 0)
            for name in (compiler.CREDENTIAL_FSH_NAME, compiler.ORG_FSH_NAME):
                self.assertTrue(os.path.exists(os.path.join(tmp, name)), name)

            self.assertEqual(
                compiler.main(["--out-dir", tmp, "--json-dir", JSON_DIR, "--check"]), 0
            )

    def test_check_detects_staleness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                compiler.main(["--out-dir", tmp, "--json-dir", JSON_DIR, "--check"]), 1
            )

    def test_check_does_not_create_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = os.path.join(tmp, "nested")
            compiler.main(["--out-dir", out_dir, "--json-dir", JSON_DIR, "--check"])
            self.assertFalse(os.path.exists(out_dir))

    def test_only_credentials_writes_one_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            compiler.main(
                ["--out-dir", tmp, "--json-dir", JSON_DIR, "--only", "credentials"]
            )
            self.assertTrue(
                os.path.exists(os.path.join(tmp, compiler.CREDENTIAL_FSH_NAME))
            )
            self.assertFalse(os.path.exists(os.path.join(tmp, compiler.ORG_FSH_NAME)))

    def test_missing_json_dir_returns_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code = compiler.main(
                ["--out-dir", tmp, "--json-dir", os.path.join(tmp, "nope")]
            )
            self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
