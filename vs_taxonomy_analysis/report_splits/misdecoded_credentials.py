#!/usr/bin/env python3
"""
misdecoded_credentials.py
-------------------------
Credential abbreviations that FaCeT has expanded to the WRONG profession.

How this differs from legitimate_pairs.py
-----------------------------------------
Three distinct things can be wrong with a credential/taxonomy row:

  1. Nothing -- the pairing is correct despite looking odd (DDS + Oral &
     Maxillofacial Surgery). Handled by `legitimate_pairs.py`.

  2. The CREDENTIAL is decoded wrong. The provider picked a sensible taxonomy code;
     FaCeT simply mistranslated their abbreviation. Handled here.

  3. The TAXONOMY choice is wrong. The provider is a nurse practitioner who selected a
     physician code. This is the mismatch report's original purpose.

Case 2 is the dangerous one, because the remediation is *upstream*: renaming the
credential in FaCeT's dictionary. Treating it as a taxonomy problem would remap the
provider while leaving the bad credential name in place to mislead the next analysis.

Evidence standard
-----------------
An abbreviation is only listed here when the provider population's own taxonomy choices
corroborate the correct reading. "AA" decoded as *Associate of Arts* would be scattered
across all of medicine; instead 97.8% of AA providers sit on anesthesiology codes, which
is only explicable if they are *Anesthesiologist Assistants*.

Each entry therefore carries a `corroborating_pattern`. Rows whose chosen taxonomy
matches it are treated as confirmed misdecodes and given an ETL target. Rows that do NOT
match stay in the normal mismatch report for human review -- an "AA" on a Family Medicine
code might genuinely be an Associate of Arts, and we must not silently convert it.
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class MisdecodedCredential:
    """A credential abbreviation FaCeT expands incorrectly."""

    code: str                   # facetCredentialCode, e.g. "AA"
    wrong_name: str             # what FaCeT currently says it means
    correct_name: str           # what it actually means
    correct_taxonomy: str       # NUCC code these providers should carry
    correct_taxonomy_name: str  # display name for that code
    corroborating_pattern: str  # regex over chosenTaxonomyDescription
    note: str = ""

    @property
    def pattern(self) -> re.Pattern:
        return re.compile(self.corroborating_pattern, re.IGNORECASE)

    def corroborates(self, taxonomy_description: str) -> bool:
        """True when the provider's taxonomy choice supports the corrected reading."""
        return bool(self.pattern.search(taxonomy_description))


# ── Registry ─────────────────────────────────────────────────────────────────
# Keyed by facetCredentialCode (upper-case).
MISDECODED: dict[str, MisdecodedCredential] = {
    "AA": MisdecodedCredential(
        code="AA",
        wrong_name="Associate of Arts",
        correct_name="Anesthesiologist Assistant",
        correct_taxonomy="367H00000X",
        correct_taxonomy_name="Anesthesiologist Assistant",
        corroborating_pattern=r"anesthesiol",
        note="183 providers, 97.8% on anesthesiology codes. An Associate of Arts "
             "degree would not cluster on anesthesiology.",
    ),
    "CAA": MisdecodedCredential(
        code="CAA",
        wrong_name="Certified Audiologist Assistant",
        correct_name="Certified Anesthesiologist Assistant",
        correct_taxonomy="367H00000X",
        correct_taxonomy_name="Anesthesiologist Assistant",
        corroborating_pattern=r"anesthesiol",
        note="94 providers, 100% on anesthesiology codes. Zero audiology signal.",
    ),
    "CSFA": MisdecodedCredential(
        code="CSFA",
        wrong_name="Certified School Food Administrator",
        correct_name="Certified Surgical First Assistant",
        correct_taxonomy="246ZC0007X",
        correct_taxonomy_name="Surgical Assistant",
        corroborating_pattern=r"surg",
        note="95 providers, 97.9% on surgical codes. School food administration "
             "would not appear in a clinical taxonomy at all.",
    ),
}


def lookup(credential_code: str) -> MisdecodedCredential | None:
    """Return the misdecode record for a credential code, if one is known."""
    return MISDECODED.get(credential_code.strip().upper())


def is_confirmed_misdecode(credential_code: str, taxonomy_description: str) -> bool:
    """
    True when this row is a known misdecoded credential AND the provider's taxonomy
    choice corroborates it.

    Rows returning False -- including known-misdecoded credentials whose taxonomy does
    not corroborate -- must remain in the mismatch report for human review.
    """
    entry = lookup(credential_code)
    return bool(entry and entry.corroborates(taxonomy_description))
