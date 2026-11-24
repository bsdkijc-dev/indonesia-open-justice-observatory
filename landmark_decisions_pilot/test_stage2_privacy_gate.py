"""Unit tests for Stage 2 Legal & Privacy Gate."""
import unittest
from pathlib import Path
from stage2_privacy_gate import scan_text_for_pii_and_exclusions, validate_privacy_record

SCHEMA_PATH = Path(__file__).parent / "stage2_privacy_verification_schema.json"


def _valid_record():
    return {
        "pk_record_id": "PK-2026-001",
        "decision_number": "123 PK/Pdt/2025",
        "official_source_url": "https://putusan3.mahkamahagung.go.id/direktori/putusan/sample.html",
        "qr_verified": True,
        "sk_kma_2_144_assessment": {
            "anonymisation_category": "NONE_GENERAL_OPEN",
            "anonymisation_required": False,
            "anonymisation_verified": True,
            "dati_2_address_only": True,
        },
        "excluded_information_screen": {
            "contains_advisblaad_or_deliberation": False,
            "contains_mediation_notes": False,
            "contains_hearing_minutes_or_raw_exhibits": False,
            "contains_sanctioned_or_whistleblower_id": False,
        },
        "pii_redaction_checks": {
            "no_unredacted_nik_or_passport": True,
            "no_unredacted_full_address": True,
            "no_unredacted_workplace_or_school": True,
            "no_unredacted_evidence_doc_numbers": True,
            "no_unredacted_personal_phone_or_email": True,
        },
        "uu_pdp_sensitive_data_screen": {
            "no_unredacted_health_or_biometric": True,
            "no_unredacted_child_data": True,
            "no_unredacted_personal_financial_account": True,
        },
        "human_privacy_signoff": {
            "reviewer_role": "Legal Privacy Reviewer",
            "reviewed_at_iso": "2026-11-24T13:30:00+07:00",
            "approved_for_research_staging": True,
        },
        "publication_eligibility": "STAGED_PRIVATE_PENDING_HUMAN_APPROVAL",
    }


class TestStage2PrivacyGate(unittest.TestCase):
    def test_valid_clean_record_passes(self):
        ok, errs = validate_privacy_record(_valid_record(), SCHEMA_PATH, "Putusan mengabulkan permohonan PK.")
        self.assertTrue(ok)
        self.assertEqual(errs, [])

    def test_detects_nik_and_phone_in_text(self):
        flags = scan_text_for_pii_and_exclusions("NIK 3171012345678901 telp 081234567890")
        self.assertIn("DETECTED_16_DIGIT_NIK_PATTERN", flags)
        self.assertIn("DETECTED_INDONESIAN_MOBILE_NUMBER", flags)

    def test_blocks_unverified_anonymisation(self):
        rec = _valid_record()
        rec["sk_kma_2_144_assessment"]["anonymisation_category"] = "CAT_3_JUVENILE_ABH"
        rec["sk_kma_2_144_assessment"]["anonymisation_required"] = True
        rec["sk_kma_2_144_assessment"]["anonymisation_verified"] = False
        ok, errs = validate_privacy_record(rec, SCHEMA_PATH)
        self.assertFalse(ok)
        self.assertTrue(any("ANONYMISATION_ERROR" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
