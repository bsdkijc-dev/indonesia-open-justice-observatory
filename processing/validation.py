"""Automated Data Quality Controls & 3-State Validation Engine (VERIFIED, DERIVED, UNVERIFIED)."""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Set

import jsonschema

from processing.deduplication import deduplicate_records


VALID_STATES = {"VERIFIED", "DERIVED", "UNVERIFIED"}


def _is_valid_iso_date(val: Any) -> bool:
    if val is None:
        return True
    try:
        datetime.strptime(str(val), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_against_schema(records: List[Dict[str, Any]], schema_path: Path) -> List[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors: List[str] = []
    for idx, rec in enumerate(records):
        try:
            jsonschema.validate(instance=rec, schema=schema)
        except jsonschema.ValidationError as exc:
            errors.append(f"Row {idx}: {exc.message}")
    return errors


def audit_case_statistics(
    records: List[Dict[str, Any]],
    valid_court_ids: Set[str],
) -> Dict[str, Any]:
    findings: List[Dict[str, str]] = []
    _, dupes = deduplicate_records(records, ("court_id", "reporting_period", "case_category"))
    for d in dupes:
        findings.append({"id": str(d.get("statistic_id")), "issue": "DUPLICATE_CASE_STATISTIC"})

    for r in records:
        sid = str(r.get("statistic_id", "UNKNOWN"))
        if r.get("court_id") not in valid_court_ids:
            findings.append({"id": sid, "issue": "INVALID_COURT_ID"})
        if not r.get("source_document"):
            findings.append({"id": sid, "issue": "MISSING_SOURCE_REFERENCE"})
        if not _is_valid_iso_date(r.get("retrieval_date")):
            findings.append({"id": sid, "issue": "INVALID_RETRIEVAL_DATE"})
        if r.get("validation_status") not in VALID_STATES:
            findings.append({"id": sid, "issue": "INVALID_VALIDATION_STATE"})

        for col in ("incoming_cases", "resolved_cases", "pending_cases"):
            val = r.get(col)
            if val is not None and val < 0:
                findings.append({"id": sid, "issue": f"NEGATIVE_COUNT:{col}"})

        inc = r.get("incoming_cases")
        res = r.get("resolved_cases")
        pend = r.get("pending_cases")
        if inc is not None and res is not None and pend is None and res > inc:
            findings.append({"id": sid, "issue": "RESOLVED_EXCEEDS_INCOMING_WITHOUT_CARRYOVER"})

    return {
        "total_records": len(records),
        "issues_count": len(findings),
        "findings": findings,
        "passed": len(findings) == 0,
    }


def audit_judgment_publications(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    findings: List[Dict[str, str]] = []
    _, dupes = deduplicate_records(records, ("case_number", "court_name"))
    for d in dupes:
        findings.append({"id": str(d.get("publication_id")), "issue": "DUPLICATE_CASE_RECORD"})

    for r in records:
        pid = str(r.get("publication_id", "UNKNOWN"))
        if not r.get("source_url") or not str(r.get("source_url")).startswith(("http://", "https://")):
            findings.append({"id": pid, "issue": "MISSING_OR_INVALID_SOURCE_URL"})
        d_date = r.get("decision_date")
        p_date = r.get("publication_date")
        if not _is_valid_iso_date(d_date) or not _is_valid_iso_date(p_date):
            findings.append({"id": pid, "issue": "INVALID_DATE_FORMAT"})
        elif d_date and p_date and p_date < d_date:
            findings.append({"id": pid, "issue": "PUBLICATION_BEFORE_DECISION_DATE"})
        h = r.get("document_hash")
        if h is not None and len(str(h)) != 64:
            findings.append({"id": pid, "issue": "INVALID_CHECKSUM_LENGTH"})

    return {
        "total_records": len(records),
        "issues_count": len(findings),
        "findings": findings,
        "passed": len(findings) == 0,
    }


def audit_indicators(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    findings: List[Dict[str, str]] = []
    for r in records:
        iid = str(r.get("indicator_id", "UNKNOWN"))
        if r.get("indicator_value") is not None and r.get("denominator") is None and r.get("unit") == "percent":
            findings.append({"id": iid, "issue": "MISSING_DENOMINATOR_FOR_RATE"})
        if not r.get("calculation_method"):
            findings.append({"id": iid, "issue": "MISSING_CALCULATION_METHOD"})
    return {
        "total_records": len(records),
        "issues_count": len(findings),
        "findings": findings,
        "passed": len(findings) == 0,
    }
