"""Data normalization utilities enforcing zero-imputation and ISO-8601 dates."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional


def normalize_int_preserve_null(value: Any) -> Optional[int]:
    """Convert numeric strings to int while strictly preserving missing/null as None (never 0)."""
    if value is None or value == "" or str(value).strip().lower() in ("null", "none", "na", "n/a", "-"):
        return None
    return int(str(value).replace(",", "").replace(".", "").strip())


def normalize_date_iso(value: Any) -> Optional[str]:
    if value is None or str(value).strip() == "":
        return None
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def normalize_court_name(name: str) -> str:
    return " ".join(name.strip().split())


def normalize_statistics_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for r in records:
        row = dict(r)
        row["incoming_cases"] = normalize_int_preserve_null(row.get("incoming_cases"))
        row["resolved_cases"] = normalize_int_preserve_null(row.get("resolved_cases"))
        row["pending_cases"] = normalize_int_preserve_null(row.get("pending_cases"))
        row["retrieval_date"] = normalize_date_iso(row.get("retrieval_date"))
        out.append(row)
    return out
