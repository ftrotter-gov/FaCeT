#!/usr/bin/env python3
"""Compile the FaCeT credential data in ``json/`` into FHIR Shorthand (FSH).

FHIR Shorthand (FSH) is the plain-text source language used to author HL7 FHIR
Implementation Guides.  The NDH IG carries FaCeT as two FSH files::

    input/fsh/facet_credentials.fsh     # individual clinician credentials
    input/fsh/facet_org_credential.fsh  # organizational credentials

Each file contains a hand-authored preamble (a ``ValueSet``, a "properties"
``CodeSystem`` that names the metadata properties, and the ``CodeSystem``
metadata plus its ``property`` declarations) followed by a large generated
block of concepts written with FSH soft indexing (``[+]`` appends a new entry,
``[=]`` refers to the most recently appended one).

This script regenerates that concept block from ``json/``.  The preamble is
reproduced verbatim so that hand-authored IG metadata is never clobbered.

Concepts are emitted in ``id`` order.  FaCeT ids are manually assigned and
deliberately grouped (physicians 1-1000, nurses 1001-10000, and so on), so
ordering by id keeps related credentials adjacent in the generated FSH and
makes the output stable no matter how the rows are split across JSON files.

Field mapping for the individual credentials::

    unique_credential_abbr           -> concept.code    (spaces become '_')
    credential_abbr                  -> concept.display
    credential_name                  -> concept.definition
    credentialing_organization_name  -> property #cred_org               (string)
    credentialing_organization_url   -> property #cred_url               (string)
    credential_description           -> property #description            (string)
    is_multisource                   -> property #is_multisource         (boolean)
    is_clinical                      -> property #is_clinical            (boolean)
    is_board_certification           -> property #is_board_certification (boolean)

Field mapping for the organizational credentials::

    id                        -> concept.code
    display                   -> concept.display
    category                  -> property #credential_category          (string)
    issuer                    -> property #issuer                       (string)
    issuer_url                -> property #issuer_url                   (string)
    credential_type           -> property #credential_type              (string)
    credential_url            -> property #credential_url               (string)
    is_credential_retired     -> property #is_credential_retired        (boolean)
    is_cms_deeming_credential -> property #is_cms_deeming_credential    (boolean)

Empty/``null`` string fields are omitted entirely rather than emitted as empty
strings, and the placeholder URL ``Various`` is treated as "no URL".

Usage::

    python facet_to_fsh.py --out-dir ../fhir-us-ndh/input/fsh
    python facet_to_fsh.py --out-dir /tmp/fsh --only credentials
    python facet_to_fsh.py --out-dir ../fhir-us-ndh/input/fsh --check
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_JSON_DIR = os.path.join(PROJECT_ROOT, "json")

# ``json/insert_credentials_clinical_adjacent.json`` also matches this prefix,
# while the organizational files (``insert_org_credential_*``) do not.
CREDENTIAL_FILE_PREFIX = "insert_credential"
ORG_FILE_PREFIX = "insert_org_credential"

# Key holding the rows inside each credential-class group object.
LIST_KEY = "credential_list"

# The names of the generated FSH files.
CREDENTIAL_FSH_NAME = "facet_credentials.fsh"
ORG_FSH_NAME = "facet_org_credential.fsh"

# The "properties" code systems that every property code is drawn from.
CREDENTIAL_PROPERTIES_CS = "FaCeT-credentialPropertiesCS"
ORG_PROPERTIES_CS = "FaCeT-org-credentialPropertiesCS"

# Placeholder values that mean "there is no real URL here".
SKIP_URL_SENTINELS = frozenset({"Various"})

# --- Preambles -------------------------------------------------------------
# Copied verbatim from the hand-authored FSH.  Everything above the generated
# concept block is IG metadata that this compiler must preserve untouched.

CREDENTIAL_PREAMBLE = r'''
ValueSet: FaCeTcredentialVS
Title: "FaCeT Practitioner Credential Properties Value Set"
Description: """This value set defines FaCeT practitioner credential concepts used to represent standardized practitioner credentials and related qualification terms in NDH content.
"""
* ^experimental = false
* codes from system FaCeT-credentialCS

Instance: FaCeT-credentialPropertiesCS
InstanceOf: CodeSystem
Title: "CodeSystem properties for FaCeT Practitioner Credentials"
Description: """
This code system defines metadata property codes for FaCeT practitioner credentials, including credentialing organization, source URL, descriptive text, and boolean indicators for multisource, clinical, and board-certification status.
"""
Usage: #definition
* status = #active
* experimental = false
* caseSensitive = true
* content = #complete
* name = "FaCeTCredentialPropertiesCS"
* concept[+].code = #cred_org
* concept[=].display = "Credentialing Organization"
* concept[=].definition = "Organization responsible for credentialing the practitioner"
* concept[+].code = #cred_url
* concept[=].display = "URL for Credential Organization"
* concept[=].definition = "URL for the organization responsible for credentialing the practitioner"
* concept[+].code = #description
* concept[=].display = "Description of the credential"
* concept[=].definition = "Description of the credential"
* concept[+].code = #is_multisource
* concept[=].display = "Indicates whether the credential is offered by multiple organizations"
* concept[=].definition = "Indicates whether the credential is offered by multiple organizations"
* concept[+].code = #is_clinical
* concept[=].display = "Indicates whether the credential is clinical in nature"
* concept[=].definition = "Indicates whether the credential is clinical in nature"
* concept[+].code = #is_board_certification
* concept[=].display = "Indicates whether the credential is a board certification"
* concept[=].definition = "Indicates whether the credential is a board certification"

/* Source

Github file: https://github.com/ftrotter-gov/FaCeT/blob/main/csv/FACET_credential_codeset.csv

code -> .code
abbr -> .display
credential_name -> .definition
credentialing_organization_name -> .property.code #cred_org
credentialing_organization_url -> .property.code #cred_url
credential_description -> .property.code #description
is_multisource -> .property.code #is_multisource
is_clinical -> .property.code #is_clinical
is_board_certification -> .property.code #is_board_certification
*/
Instance: FaCeT-credentialCS
InstanceOf: CodeSystem
Title: "FaCeT Credential Code System"
Description: """
This code system defines FaCeT practitioner credential concepts and associated properties used to publish normalized credential abbreviations, definitions, issuing-organization context, and classification attributes.
"""
Usage: #definition
* status = #active
* experimental = false
* caseSensitive = true
* title = "FaCeT Credential Code System"
* name = "FaCeTCredentialCS"
* description = """
This code system defines FaCeT practitioner credential concepts and associated properties used to publish normalized credential abbreviations, definitions, issuing-organization context, and classification attributes.
"""
* content = #complete
//* url = "https://github.com/ftrotter-gov/FaCeT/blob/main/csv/FACET_credential_codeset.csv"
* version = "0.1.0"
* jurisdiction[0] = http://unstats.un.org/unsd/methods/m49/m49.htm#840 "United States of America"
* caseSensitive = true
* property[+].code = FaCeT-credentialPropertiesCS#cred_org
* property[=].description = "Credentialing Organization"
* property[=].type = #string
* property[+].code = FaCeT-credentialPropertiesCS#cred_url
* property[=].description = "URL for Credential Organization"
* property[=].type = #string
* property[+].code = FaCeT-credentialPropertiesCS#description
* property[=].description = "Description of the credential"
* property[=].type = #string
* property[+].code = FaCeT-credentialPropertiesCS#is_multisource
* property[=].description = "Indicates whether the credential is offered by multiple organizations"
* property[=].type = #boolean
* property[+].code = FaCeT-credentialPropertiesCS#is_clinical
* property[=].description = "Indicates whether the credential is clinical in nature"
* property[=].type = #boolean
* property[+].code = FaCeT-credentialPropertiesCS#is_board_certification
* property[=].description = "Indicates whether the credential is a board certification"
* property[=].type = #boolean
'''

ORG_PREAMBLE = r'''
ValueSet: FaCeTorganizationCredentialVS
Title: "FaCeT Organizational Credential Properties Value Set"
Description: """
This value set defines FaCeT organizational credential concepts used to represent standardized accreditation, certification, and related organizational credential terms in NDH content.
"""
* ^experimental = false
* codes from system FaCeT-org-credentialCS

Instance: FaCeT-org-credentialPropertiesCS
InstanceOf: CodeSystem
Title: "CodeSystem properties for FaCeT Organizational Credential"
Description: """
This code system defines metadata property codes for FaCeT organizational credentials, including credential category, issuer details, credential type, credential URL, retirement status, and CMS deeming-recognition indicator.
"""
Usage: #definition
* status = #active
* experimental = false
* caseSensitive = true
* content = #complete
* name = "FaCeTOrganizationalCredentialPropertiesCS"
* concept[+].code = #credential_category
* concept[=].display = "Credential Category"
* concept[=].definition = "Category of the credential (e.g., accreditation, certification, license, etc.)"
* concept[+].code = #issuer
* concept[=].display = "Issuer Organization"
* concept[=].definition = "Organization responsible for credentialing the practitioner"
* concept[+].code = #issuer_url
* concept[=].display = "URL for Issuer Organization"
* concept[=].definition = "URL for the organization responsible for credentialing the practitioner"
* concept[+].code = #credential_type
* concept[=].display = "Credential Type"
* concept[=].definition = "Type of the credential (e.g., accreditation, certification, license, etc.)"
* concept[+].code = #credential_url
* concept[=].display = "URL for Credential Information"
* concept[=].definition = "URL for the credential information"
* concept[+].code = #is_credential_retired
* concept[=].display = "Indicates whether the credential is retired and should no longer be used"
* concept[=].definition = "Indicates whether the credential is retired and should no longer be used"
* concept[+].code = #is_cms_deeming_credential
* concept[=].display = "Indicates whether the credential is recognized by CMS as a deeming credential for Medicare/Medicaid provider enrollment purposes"
* concept[=].definition = "Indicates whether the credential is recognized by CMS as a deeming credential for Medicare/Medicaid provider enrollment purposes"

// https://github.com/ftrotter-gov/FaCeT/blob/main/csv/FACET_org_credential.csv
Instance: FaCeT-org-credentialCS
InstanceOf: CodeSystem
Title: "FaCeT Organizational Credential Code System"
Description: """
This code system defines FaCeT organizational credential concepts and associated properties used to publish normalized organizational accreditation and certification identifiers with issuer and lifecycle metadata.
"""
Usage: #definition
* status = #active
* experimental = false
* caseSensitive = true
* title = "FaCeT Organizational Credential Code System"
* name = "FaCeTOrganizationalCredentialCS"
* description = """
This code system defines FaCeT organizational credential concepts and associated properties used to publish normalized organizational accreditation and certification identifiers with issuer and lifecycle metadata.
"""
* content = #complete
//* url = "https://github.com/ftrotter-gov/FaCeT/blob/main/csv/FACET_org_credential.csv"
* version = "0.1.0"
* jurisdiction[0] = http://unstats.un.org/unsd/methods/m49/m49.htm#840 "United States of America"
* caseSensitive = true
* property[+].code = FaCeT-org-credentialPropertiesCS#credential_category
* property[=].description = "Category"
* property[=].type = #string
* property[+].code = FaCeT-org-credentialPropertiesCS#issuer
* property[=].description = "Issuer Organization"
* property[=].type = #string
* property[+].code = FaCeT-org-credentialPropertiesCS#issuer_url
* property[=].description = "URL for Issuer Organization"
* property[=].type = #string
* property[+].code = FaCeT-org-credentialPropertiesCS#credential_type
* property[=].description = "Credential Type"
* property[=].type = #string
* property[+].code = FaCeT-org-credentialPropertiesCS#credential_url
* property[=].description = "URL for Credential Information"
* property[=].type = #string
* property[+].code = FaCeT-org-credentialPropertiesCS#is_credential_retired
* property[=].description = "Indicates whether the credential is retired and should no longer be used"
* property[=].type = #boolean
* property[+].code = FaCeT-org-credentialPropertiesCS#is_cms_deeming_credential
* property[=].description = "Indicates whether the credential is recognized by CMS as a deeming credential for Medicare/Medicaid provider enrollment purposes"
* property[=].type = #boolean
'''


# --- Loading ---------------------------------------------------------------


def iter_json_files(json_dir: str, prefix: str, exclude_prefix: str | None = None) -> list[str]:
    """Return the data files matching ``prefix``, sorted by name."""
    names = sorted(
        name
        for name in os.listdir(json_dir)
        if name.startswith(prefix)
        and name.endswith(".json")
        and not (exclude_prefix and name.startswith(exclude_prefix))
    )
    return [os.path.join(json_dir, name) for name in names]


def load_rows(paths: list[str]) -> list[dict[str, Any]]:
    """Flatten the credential-class groups in ``paths`` into one row list.

    Rows are returned ordered by their ``id`` column.  The FaCeT ids are
    manually assigned and deliberately grouped (physicians 1-1000, nurses
    1001-10000, and so on), so ordering by id keeps related credentials
    together in the generated FSH regardless of which file they live in.
    """
    rows: list[dict[str, Any]] = []
    for path in paths:
        with open(path, encoding="utf-8") as handle:
            groups = json.load(handle)
        for group in groups:
            rows.extend(group[LIST_KEY])

    ids = [row["id"] for row in rows]
    if len(set(ids)) != len(ids):
        duplicates = sorted({i for i in ids if ids.count(i) > 1})
        raise ValueError(f"duplicate FaCeT ids in source data: {duplicates}")

    rows.sort(key=lambda row: row["id"])
    return rows


def load_credential_rows(json_dir: str) -> list[dict[str, Any]]:
    """Load the individual clinician credential rows."""
    return load_rows(iter_json_files(json_dir, CREDENTIAL_FILE_PREFIX, ORG_FILE_PREFIX))


def load_org_rows(json_dir: str) -> list[dict[str, Any]]:
    """Load the organizational credential rows."""
    return load_rows(iter_json_files(json_dir, ORG_FILE_PREFIX))


# --- FSH emitters ----------------------------------------------------------


def fsh_code(value: Any) -> str:
    """Render ``value`` as an FSH code token.

    FSH codes cannot contain whitespace, so spaces become underscores; this is
    what turns ``RS Hom`` into ``#RS_Hom`` and ``DAc (RI)`` into ``#DAc_(RI)``.
    """
    return str(value).strip().replace(" ", "_")


def fsh_string(value: Any) -> str:
    """Render ``value`` as the inside of an FSH double-quoted string."""
    text = str(value)
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    # Concept text is emitted on a single line; fold any stray newlines.
    text = text.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    return text


def has_value(value: Any) -> bool:
    """Return True when ``value`` is a non-empty string worth emitting."""
    return value is not None and str(value).strip() != ""


def string_property(properties_cs: str, prop: str, value: Any) -> list[str]:
    """Emit the two-line ``property`` block for a string-valued property."""
    return [
        f"* concept[=].property[+].code = {properties_cs}#{prop}",
        f'* concept[=].property[=].valueString = "{fsh_string(str(value).strip())}"',
    ]


def boolean_property(properties_cs: str, prop: str, value: Any) -> list[str]:
    """Emit the two-line ``property`` block for a boolean-valued property."""
    return [
        f"* concept[=].property[+].code = {properties_cs}#{prop}",
        f"* concept[=].property[=].valueBoolean = {'true' if value else 'false'}",
    ]


# --- Concept rendering -----------------------------------------------------

# (row key, property code) for the string properties, in emission order.
CREDENTIAL_STRING_PROPERTIES = (
    ("credentialing_organization_name", "cred_org"),
    ("credentialing_organization_url", "cred_url"),
    ("credential_description", "description"),
)

CREDENTIAL_BOOLEAN_PROPERTIES = (
    "is_multisource",
    "is_clinical",
    "is_board_certification",
)

ORG_STRING_PROPERTIES = (
    ("category", "credential_category"),
    ("issuer", "issuer"),
    ("issuer_url", "issuer_url"),
    ("credential_type", "credential_type"),
    ("credential_url", "credential_url"),
)

ORG_BOOLEAN_PROPERTIES = (
    "is_credential_retired",
    "is_cms_deeming_credential",
)


def credential_concept(row: dict[str, Any]) -> list[str]:
    """Render one clinician credential row as FSH lines."""
    lines = [
        f"* concept[+].code = #{fsh_code(row['unique_credential_abbr'])}",
        f"* concept[=].display = \"{fsh_string(row['credential_abbr'])}\"",
        f"* concept[=].definition = \"{fsh_string(row['credential_name'])}\"",
    ]
    for key, prop in CREDENTIAL_STRING_PROPERTIES:
        value = row.get(key)
        if not has_value(value):
            continue
        # "Various" is a placeholder meaning the credential has no single URL.
        if prop == "cred_url" and str(value).strip() in SKIP_URL_SENTINELS:
            continue
        lines.extend(string_property(CREDENTIAL_PROPERTIES_CS, prop, value))
    for key in CREDENTIAL_BOOLEAN_PROPERTIES:
        lines.extend(boolean_property(CREDENTIAL_PROPERTIES_CS, key, row.get(key)))
    return lines


def org_concept(row: dict[str, Any]) -> list[str]:
    """Render one organizational credential row as FSH lines."""
    lines = [
        f"* concept[+].code = #{fsh_code(row['id'])}",
        f"* concept[=].display = \"{fsh_string(row['display'])}\"",
    ]
    for key, prop in ORG_STRING_PROPERTIES:
        value = row.get(key)
        if not has_value(value):
            continue
        if prop.endswith("url") and str(value).strip() in SKIP_URL_SENTINELS:
            continue
        lines.extend(string_property(ORG_PROPERTIES_CS, prop, value))
    for key in ORG_BOOLEAN_PROPERTIES:
        lines.extend(boolean_property(ORG_PROPERTIES_CS, key, row.get(key)))
    return lines


def render(preamble: str, banner: str, rows: list[dict[str, Any]], renderer) -> str:
    """Assemble a complete FSH document from ``preamble`` and ``rows``."""
    parts = [preamble, "\n", banner, "\n"]
    for row in rows:
        parts.append("\n".join(renderer(row)))
        parts.append("\n\n")
    return "".join(parts)


CREDENTIAL_BANNER = "// FaCeT credential concepts generated from json/ by facet_to_fsh.py"
ORG_BANNER = (
    "// FaCeT organizational credential concepts generated from json/ by facet_to_fsh.py"
)


def build_credentials(json_dir: str) -> str:
    """Compile ``facet_credentials.fsh``."""
    rows = load_credential_rows(json_dir)
    text = render(CREDENTIAL_PREAMBLE, CREDENTIAL_BANNER, rows, credential_concept)
    # The published file ends with a single newline.
    return text.rstrip("\n") + "\n"


def build_org_credentials(json_dir: str) -> str:
    """Compile ``facet_org_credential.fsh``."""
    rows = load_org_rows(json_dir)
    text = render(ORG_PREAMBLE, ORG_BANNER, rows, org_concept)
    # The published file ends with a blank line after the last concept.
    return text.rstrip("\n") + "\n\n"


# --- CLI -------------------------------------------------------------------


TARGETS = {
    "credentials": (CREDENTIAL_FSH_NAME, build_credentials),
    "org": (ORG_FSH_NAME, build_org_credentials),
}


def concept_count(text: str) -> int:
    """Count the generated concepts in an FSH document.

    Only the block below the generated banner is counted; the preamble also
    contains ``concept[+]`` rules that define the property vocabulary.
    """
    _, _, generated = text.partition("\n// FaCeT ")
    return sum(
        1 for line in generated.split("\n") if line.startswith("* concept[+].code")
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compile the FaCeT json/ data into FHIR Shorthand (FSH) files.",
    )
    parser.add_argument(
        "--out-dir",
        required=True,
        help=(
            "Directory the .fsh files are written to, e.g. the input/fsh "
            "directory of the NDH implementation guide."
        ),
    )
    parser.add_argument(
        "--json-dir",
        default=DEFAULT_JSON_DIR,
        help="Directory holding the FaCeT JSON data (default: %(default)s).",
    )
    parser.add_argument(
        "--only",
        choices=("credentials", "org", "both"),
        default="both",
        help="Which FSH file to build (default: %(default)s).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Do not write anything; exit non-zero if the files on disk differ "
            "from what would be generated."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if not os.path.isdir(args.json_dir):
        print(f"error: no such json directory: {args.json_dir}", file=sys.stderr)
        return 2

    selected = TARGETS if args.only == "both" else {args.only: TARGETS[args.only]}

    if not args.check:
        os.makedirs(args.out_dir, exist_ok=True)

    stale = False
    for name, builder in selected.values():
        text = builder(args.json_dir)
        out_path = os.path.join(args.out_dir, name)

        if args.check:
            current = None
            if os.path.exists(out_path):
                with open(out_path, encoding="utf-8") as handle:
                    current = handle.read()
            if current == text:
                print(f"ok      {out_path} ({concept_count(text)} concepts)")
            else:
                stale = True
                state = "missing" if current is None else "out of date"
                print(f"STALE   {out_path} is {state}")
            continue

        with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        print(f"wrote   {out_path} ({concept_count(text)} concepts)")

    if stale:
        print("\nRegenerate with: python facet_to_fsh.py --out-dir <dir>", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

