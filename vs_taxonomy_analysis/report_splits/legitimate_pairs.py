#!/usr/bin/env python3
"""
legitimate_pairs.py
-------------------
Allow-list of credential x taxonomy pairings that are **correct**, even though the
chosen taxonomy code lives in the NUCC "Allopathic & Osteopathic Physicians" grouping.

Why this exists
---------------
The mismatch report is built on the assumption:

    non-physician credential + physician-grouping taxonomy code == data error

That assumption is wrong for dual-degree clinicians. The clearest case is oral &
maxillofacial surgery: OMFS practitioners routinely hold BOTH a dental and a medical
degree (DMD/MD, DDS/MD), and NUCC itself files the code under the physician grouping
while naming it "Oral & Maxillofacial Surgery (D.M.D.)" -- the dental degree is in the
code's own display name. A DDS or DMD choosing 204E00000X is correct, not a mismatch.

Without this allow-list, 1,072 correctly-coded dental providers were being reported as
errors (DDS 641, DMD 419, BDS 10, OMFS 2).

Maintaining this file
---------------------
Add an entry when a credential legitimately maps to a physician-grouping code. Prefer
being conservative: only add pairings that are defensible on scope-of-practice or
dual-degree grounds. Anything speculative belongs in the mismatch report where a human
will look at it.
"""

import re

# ── Oral & Maxillofacial Surgery ─────────────────────────────────────────────
# NUCC display name: "Oral & Maxillofacial Surgery (D.M.D.)"
OMFS_CODE = "204E00000X"

# Dental credentials for which OMFS is the correct taxonomy.
# Matched case-insensitively against facetCredentialCode.
OMFS_DENTAL_CREDENTIALS = {
    "DDS",   # Doctor of Dental Surgery
    "DMD",   # Doctor of Medicine in Dentistry / Doctor of Dental Medicine
    "BDS",   # Bachelor of Dental Surgery (common non-US dental degree)
    "OMFS",  # Oral and Maxillofacial Surgeon (names the specialty outright)
    "OMS",   # Oral & Maxillofacial Surgery -- see caveat below
}

# `OMS` is ambiguous in the FaCeT credential list: it is used both for "Oral &
# Maxillofacial Surgery" and for "Ostomy Management Specialist". Only treat it as
# legitimate when the credential NAME actually refers to oral/maxillofacial work,
# so the single Ostomy Management Specialist row still surfaces for review.
RE_ORAL_MAXILLOFACIAL = re.compile(r"oral|maxillofacial|dent", re.IGNORECASE)

AMBIGUOUS_CREDENTIALS = {"OMS"}

# ── Registry ─────────────────────────────────────────────────────────────────
# code -> set of credential codes that legitimately use it
LEGITIMATE_PAIRS: dict[str, set[str]] = {
    OMFS_CODE: OMFS_DENTAL_CREDENTIALS,
}


def is_legitimate_pair(credential_code: str, credential_name: str,
                       taxonomy_code: str) -> bool:
    """
    Return True when this credential is *correctly* using this physician-grouping
    taxonomy code, and therefore must NOT be reported as a mismatch.

    Args:
        credential_code: facetCredentialCode, e.g. "DDS".
        credential_name: facetCredentialName, used to disambiguate overloaded codes.
        taxonomy_code:   chosenTaxonomyCode, e.g. "204E00000X".

    Returns:
        True if the pairing is on the allow-list.
    """
    allowed = LEGITIMATE_PAIRS.get(taxonomy_code.strip().upper())
    if not allowed:
        return False

    cred = credential_code.strip().upper()
    if cred not in allowed:
        return False

    # Overloaded credential codes must also match on name.
    if cred in AMBIGUOUS_CREDENTIALS:
        return bool(RE_ORAL_MAXILLOFACIAL.search(credential_name))

    return True
