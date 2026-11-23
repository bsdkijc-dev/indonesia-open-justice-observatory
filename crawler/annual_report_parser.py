"""Annual report table parser for structured judicial statistics."""

from __future__ import annotations

from typing import Dict, List, Optional


def parse_case_summary_rows(
    rows: List[Dict[str, Optional[int | str]]],
    source_document: str,
    retrieval_date: str,
) -> List[Dict[str, Optional[int | str]]]:
    """Normalize extracted annual report rows without imputing missing counts."""
    normalized = []
    for idx, row in enumerate(rows, start=1):
        normalized.append(
            {
                "statistic_id": f"STAT-AR-{idx:04d}",
                "court_id": row.get("court_id", "INST-MA-000"),
                "reporting_period": str(row.get("reporting_period", "")),
                "case_category": str(row.get("case_category", "Unknown")),
                "incoming_cases": row.get("incoming_cases"),
                "resolved_cases": row.get("resolved_cases"),
                "pending_cases": row.get("pending_cases"),
                "source_document": source_document,
                "source_page": row.get("source_page"),
                "retrieval_date": retrieval_date,
                "validation_status": "VERIFIED" if row.get("source_page") is not None else "UNVERIFIED",
            }
        )
    return normalized
