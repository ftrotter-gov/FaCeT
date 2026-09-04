#!/usr/bin/env python3
"""Compile the generated FaCeT FSH with SUSHI and validate the FHIR it produces.

These tests are the real proof that ``facet_to_fsh.py`` emits valid FHIR
Shorthand: rather than checking the text structurally, they hand the generated
files to `SUSHI <https://fshschool.org/docs/sushi/>`_, the reference FSH
compiler, and assert that it reports no errors.

SUSHI is a Node package.  If it is missing, the tests try ``npm install -g
fsh-sushi`` once; if that is not possible (no npm, no network) the tests skip
rather than fail, so the rest of the suite still runs offline.

The first SUSHI run downloads the FHIR R4 core package into ``~/.fhir/packages``
and may take several minutes; later runs take roughly ten seconds.

Run with::

    python -m unittest test_facet_to_fsh_sushi -v
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest

import facet_to_fsh as compiler
import sushi_runner

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(PROJECT_ROOT, "json")

# Set FACET_SKIP_SUSHI=1 to skip these slower tests entirely.
SKIP_ENV_VAR = "FACET_SKIP_SUSHI"

# Resources SUSHI is expected to export from the two FaCeT files.
EXPECTED_RESOURCES = {
    "CodeSystem-FaCeT-credentialCS.json",
    "CodeSystem-FaCeT-credentialPropertiesCS.json",
    "CodeSystem-FaCeT-org-credentialCS.json",
    "CodeSystem-FaCeT-org-credentialPropertiesCS.json",
    "ValueSet-FaCeTcredentialVS.json",
    "ValueSet-FaCeTorganizationCredentialVS.json",
}


def sushi_or_skip() -> str:
    """Return a usable sushi path, or skip the test if it cannot be obtained."""
    if os.environ.get(SKIP_ENV_VAR):
        raise unittest.SkipTest(f"{SKIP_ENV_VAR} is set")
    try:
        return sushi_runner.ensure_sushi(auto_install=True)
    except sushi_runner.SushiNotAvailable as exc:
        raise unittest.SkipTest(str(exc)) from exc


class SushiAvailabilityTests(unittest.TestCase):
    """Tests for detecting and installing SUSHI."""

    def test_sushi_can_be_located_or_installed(self) -> None:
        sushi = sushi_or_skip()
        self.assertTrue(os.path.exists(sushi), f"sushi path does not exist: {sushi}")

    def test_missing_sushi_raises_when_install_disabled(self) -> None:
        # With auto-install off and nothing on PATH, ensure_sushi must raise
        # rather than silently succeeding.
        original = sushi_runner.find_sushi
        sushi_runner.find_sushi = lambda: None
        try:
            with self.assertRaises(sushi_runner.SushiNotAvailable):
                sushi_runner.ensure_sushi(auto_install=False)
        finally:
            sushi_runner.find_sushi = original


class SushiCompileTests(unittest.TestCase):
    """Compile the generated FSH with SUSHI once, then assert on the output."""

    project_dir: str
    result: sushi_runner.SushiResult

    @classmethod
    def setUpClass(cls) -> None:
        sushi = sushi_or_skip()

        # Generate the FSH fresh from json/ so the test always reflects the
        # current data rather than whatever happens to be checked in.
        cls._tmp = tempfile.TemporaryDirectory()
        out_dir = os.path.join(cls._tmp.name, "fsh")
        exit_code = compiler.main(["--out-dir", out_dir, "--json-dir", JSON_DIR])
        assert exit_code == 0, "facet_to_fsh.py failed to generate the FSH"

        fsh_files = [
            os.path.join(out_dir, name) for name in sushi_runner.FACET_FSH_NAMES
        ]
        cls.project_dir = os.path.join(cls._tmp.name, "project")
        os.makedirs(cls.project_dir, exist_ok=True)
        cls.result = sushi_runner.run_sushi(fsh_files, cls.project_dir, sushi=sushi)

    @classmethod
    def tearDownClass(cls) -> None:
        if hasattr(cls, "_tmp"):
            cls._tmp.cleanup()

    def load_resource(self, name: str) -> dict:
        path = os.path.join(self.result.resource_dir(), name)
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)

    # --- compilation ---

    def test_sushi_reports_no_errors(self) -> None:
        self.assertTrue(self.result.ok, self.result.summary())
        self.assertEqual(self.result.errors, 0, self.result.summary())

    def test_sushi_reports_no_warnings(self) -> None:
        self.assertEqual(self.result.warnings, 0, self.result.summary())

    def test_expected_resources_are_exported(self) -> None:
        exported = set(self.result.exported_resources())

    # --- the compiled FHIR ---

    def test_credential_codesystem_has_every_concept(self) -> None:
        rows = compiler.load_credential_rows(JSON_DIR)
        resource = self.load_resource("CodeSystem-FaCeT-credentialCS.json")
        self.assertEqual(resource["resourceType"], "CodeSystem")
        self.assertEqual(len(resource["concept"]), len(rows))

    def test_org_codesystem_has_every_concept(self) -> None:
        rows = compiler.load_org_rows(JSON_DIR)
        resource = self.load_resource("CodeSystem-FaCeT-org-credentialCS.json")
        self.assertEqual(resource["resourceType"], "CodeSystem")
        self.assertEqual(len(resource["concept"]), len(rows))

    def test_credential_concepts_survive_the_round_trip(self) -> None:
        rows = compiler.load_credential_rows(JSON_DIR)
        resource = self.load_resource("CodeSystem-FaCeT-credentialCS.json")
        by_code = {concept["code"]: concept for concept in resource["concept"]}

        for row in rows:
            code = row["unique_credential_abbr"].replace(" ", "_")
            self.assertIn(code, by_code)
            concept = by_code[code]
            self.assertEqual(concept["display"], row["credential_abbr"])
            self.assertEqual(concept["definition"], row["credential_name"])

            properties = {p["code"]: p for p in concept.get("property", [])}
            for key in compiler.CREDENTIAL_BOOLEAN_PROPERTIES:
                self.assertEqual(properties[key]["valueBoolean"], bool(row.get(key)))

    def test_org_concepts_survive_the_round_trip(self) -> None:
        rows = compiler.load_org_rows(JSON_DIR)
        resource = self.load_resource("CodeSystem-FaCeT-org-credentialCS.json")
        by_code = {concept["code"]: concept for concept in resource["concept"]}

        for row in rows:
            concept = by_code[str(row["id"])]
            self.assertEqual(concept["display"], row["display"])
            properties = {p["code"]: p for p in concept.get("property", [])}
            self.assertEqual(
                properties["credential_type"]["valueString"], row["credential_type"]
            )
            self.assertEqual(properties["issuer"]["valueString"], row["issuer"])

    def test_declared_properties_are_typed_correctly(self) -> None:
        resource = self.load_resource("CodeSystem-FaCeT-credentialCS.json")
        types = {p["code"]: p["type"] for p in resource["property"]}
        self.assertEqual(types["cred_org"], "string")
        self.assertEqual(types["cred_url"], "string")
        self.assertEqual(types["description"], "string")
        for key in compiler.CREDENTIAL_BOOLEAN_PROPERTIES:
            self.assertEqual(types[key], "boolean")

    def test_every_used_property_is_declared(self) -> None:
        # A concept property the CodeSystem never declares would be invalid
        # FHIR even where SUSHI does not reject it outright.
        for name in (
            "CodeSystem-FaCeT-credentialCS.json",
            "CodeSystem-FaCeT-org-credentialCS.json",
        ):
            resource = self.load_resource(name)
            declared = {p["code"] for p in resource["property"]}
            used = {
                prop["code"]
                for concept in resource["concept"]
                for prop in concept.get("property", [])
            }
            self.assertTrue(
                used <= declared,
                f"{name}: undeclared properties {sorted(used - declared)}",
            )

    def test_valuesets_point_at_the_code_systems(self) -> None:
        value_set = self.load_resource("ValueSet-FaCeTcredentialVS.json")
        systems = [inc["system"] for inc in value_set["compose"]["include"]]
        self.assertTrue(any(s.endswith("FaCeT-credentialCS") for s in systems), systems)

        value_set = self.load_resource("ValueSet-FaCeTorganizationCredentialVS.json")
        systems = [inc["system"] for inc in value_set["compose"]["include"]]
        self.assertTrue(
            any(s.endswith("FaCeT-org-credentialCS") for s in systems), systems
        )

    def test_unicode_survives_compilation(self) -> None:
        resource = self.load_resource("CodeSystem-FaCeT-credentialCS.json")
        definitions = [c.get("definition", "") for c in resource["concept"]]
        self.assertTrue(
            any("醫學士" in d for d in definitions),
            "expected the Chinese Bachelor of Medicine to survive compilation",
        )
        self.assertFalse(any("\ufffd" in d for d in definitions))

    def test_codes_with_punctuation_compile(self) -> None:
        # Codes such as MD(H), CNN/M and DAc_(RI) exercise FSH tokenizing.
        resource = self.load_resource("CodeSystem-FaCeT-credentialCS.json")
        codes = {concept["code"] for concept in resource["concept"]}
        for code in ("MD(H)", "CNN/M", "OTR/L", "DAc_(RI)", "RS_Hom"):
            self.assertIn(code, codes)



class SushiDetectsBrokenFshTests(unittest.TestCase):
    """Prove the harness would actually catch invalid FSH.

    Without this, a silently-passing SUSHI run could hide real breakage.
    """

    def test_invalid_fsh_is_reported_as_an_error(self) -> None:
        sushi = sushi_or_skip()
        broken = "\n".join(
            [
                "Instance: BrokenCS",
                "InstanceOf: CodeSystem",
                "Usage: #definition",
                "* status = #active",
                "* content = #complete",
                "* concept[+].code = #A",
                '* concept[=].thisElementDoesNotExist = "nope"',
                "",
            ]
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "broken.fsh")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(broken)

            project = os.path.join(tmp, "project")
            os.makedirs(project)
            result = sushi_runner.run_sushi([path], project, sushi=sushi)

            self.assertFalse(result.ok)
            self.assertGreater(result.errors, 0, result.summary())


if __name__ == "__main__":
    unittest.main()
