Credentialing Organizations
==========================

Need to make sure that all "deeming authorities" for CMS in their different clinical organizations is reflected.

**CMS-approved deeming organizations** are private accreditation bodies that the **Centers for Medicare & Medicaid Services (CMS)** has authorized to determine whether healthcare providers meet Medicare requirements.

If a provider is accredited by one of these organizations, CMS **“deems”** the provider to meet the **Medicare Conditions of Participation (CoPs)** or other Medicare regulatory standards.

---

# The basic idea

Normally:

```text
CMS → surveys a provider → determines Medicare compliance
```

With deeming:

```text
Accreditation organization surveys provider
        ↓
If accredited → CMS accepts it as meeting Medicare requirements
```

So the accreditor acts as a **CMS-recognized regulator for compliance purposes**.


# Major CMS deeming organizations

These vary by provider type.

## Hospitals

| organization         |
| -------------------- |
| The Joint Commission |
| DNV Healthcare       |
| ACHC                 |
| CIHQ                 |

These organizations perform surveys and grant accreditation that CMS recognizes.

---

## Clinical laboratories

| organization                           |
| -------------------------------------- |
| COLA                                   |
| CAP (College of American Pathologists) |
| Joint Commission                       |
| AABB                                   |

These operate under **CLIA deeming authority**.

---

## Home health / hospice

| organization     |
| ---------------- |
| ACHC             |
| CHAP             |
| Joint Commission |



# CMS-Approved Deeming Organizations (Core List)

These organizations currently have **CMS deeming authority for one or more provider types**.

| Organization                                                            | Typical Abbreviation |
| ----------------------------------------------------------------------- | -------------------- |
| The Joint Commission                                                    | TJC                  |
| DNV Healthcare                                                          | DNV                  |
| Accreditation Commission for Health Care                                | ACHC                 |
| Center for Improvement in Healthcare Quality                            | CIHQ                 |
| Accreditation Association for Ambulatory Health Care                    | AAAHC                |
| American Association for Accreditation of Ambulatory Surgery Facilities | AAAASF               |
| Community Health Accreditation Partner                                  | CHAP                 |
| The Compliance Team                                                     | TCT                  |
| Healthcare Facilities Accreditation Program                             | HFAP                 |

These organizations accredit providers such as:

* Hospitals
* Critical Access Hospitals
* Home Health Agencies
* Hospices
* Ambulatory Surgical Centers
* Outpatient therapy providers
* Rural Health Clinics ([Centers for Medicare & Medicaid Services][1])

---

# CLIA Deeming Organizations (Clinical Laboratories)

CMS also grants **deeming authority under CLIA** to laboratory accreditors.

| Organization                                               | Abbreviation |
| ---------------------------------------------------------- | ------------ |
| AABB                                                       | AABB         |
| American Association for Laboratory Accreditation          | A2LA         |
| American Society for Histocompatibility and Immunogenetics | ASHI         |
| COLA                                                       | COLA         |
| College of American Pathologists                           | CAP          |
| The Joint Commission                                       | TJC          |
| Healthcare Facilities Accreditation Program                | HFAP         |

These organizations certify that laboratories meet **CLIA quality standards for testing**. ([Centers for Medicare & Medicaid Services][1])

---

# Combined Master List

If you merge both sets, the **full list of CMS-recognized accrediting organizations with deeming authority** looks like this:

| Organization                                                                     |
| -------------------------------------------------------------------------------- |
| The Joint Commission                                                             |
| DNV Healthcare                                                                   |
| Accreditation Commission for Health Care (ACHC)                                  |
| Center for Improvement in Healthcare Quality (CIHQ)                              |
| Accreditation Association for Ambulatory Health Care (AAAHC)                     |
| American Association for Accreditation of Ambulatory Surgery Facilities (AAAASF) |
| Community Health Accreditation Partner (CHAP)                                    |
| The Compliance Team (TCT)                                                        |
| Healthcare Facilities Accreditation Program (HFAP)                               |
| AABB                                                                             |
| American Association for Laboratory Accreditation (A2LA)                         |
| American Society for Histocompatibility and Immunogenetics (ASHI)                |
| COLA                                                                             |
| College of American Pathologists (CAP)                                           |

---

# Important structural note for your dataset

In your `org_credential` vocabulary, these organizations would typically appear as **issuers of accreditation credentials** such as:

```text
jc_hospital_accreditation
dnv_niaho_hospital_accreditation
achc_home_health_accreditation
chap_hospice_accreditation
aaahc_ambulatory_surgery_center_accreditation
cap_clinical_laboratory_accreditation
cola_clinical_laboratory_accreditation
```

