"""Fail-closed Stage 2 Legal & Privacy Gate for Mahkamah Agung RI PK decisions."""
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple
import jsonschema

# Deterministic regex patterns for high-risk PII & excluded information
NIK_PATTERN = re.compile(r"\b[1-9][0-9]{15}\b")
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_PATTERN = re.compile(r"\b(?:\+62|62|0)8[1-9][0-9]{7,11}\b")
EXCLUDED_KEYWORDS = re.compile(r"\b(advisblaad|musyawarah\s+majelis\s+hakim\s+rahasia|catatan\s+mediasi)\b", re.IGNORECASE)


def scan_text_for_pii_and_exclusions(text: str) -> List[str]:
    """Return deterministic list of privacy or excluded-information flags found in raw text."""
    flags: List[str] = []
    if NIK_PATTERN.search(text):
        flags.append("DETECTED_16_DIGIT_NIK_PATTERN")
    if EMAIL_PATTERN.search(text):
        flags.append("DETECTED_EMAIL_ADDRESS")
    if PHONE_PATTERN.search(text):
        flags.append("DETECTED_INDONESIAN_MOBILE_NUMBER")
    if EXCLUDED_KEYWORDS.search(text):
        flags.append("DETECTED_EXCLUDED_DELIBERATION_OR_MEDIATION_TERM")
    return flags


def validate_privacy_record(record: Dict[str, Any], schema_path: Path, raw_text: str = "") -> Tuple[bool, List[str]]:
    """Validate a PK privacy-assessment record against Stage 2 JSON Schema and fail-closed rules."""
    errors: List[str] = []
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(instance=record, schema=schema)
    except jsonschema.ValidationError as exc:
        errors.append(f"SCHEMA_ERROR: {exc.message}")

    if not record.get("qr_verified", False):
        errors.append("PROVENANCE_ERROR: qr_verified must be True")

    sk = record.get("sk_kma_2_144_assessment", {})
    if sk.get("anonymisation_required") and not sk.get("anonymisation_verified"):
        errors.append("ANONYMISATION_ERROR: anonymisation_required is True but anonymisation_verified is False")

    if raw_text:
        text_flags = scan_text_for_pii_and_exclusions(raw_text)
        errors.extend(text_flags)

    signoff = record.get("human_privacy_signoff", {})
    if not signoff.get("approved_for_research_staging", False):
        errors.append("GOVERNANCE_GATE: human_privacy_signoff.approved_for_research_staging is False")

    return (len(errors) == 0, errors)