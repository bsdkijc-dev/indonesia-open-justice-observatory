"""Deterministic deduplication utilities for judicial records."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def deduplicate_records(
    records: Iterable[Dict[str, Any]],
    key_fields: Tuple[str, ...],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Return (unique_records, duplicate_records) preserving first occurrence."""
    seen = set()
    unique: List[Dict[str, Any]] = []
    duplicates: List[Dict[str, Any]] = []

    for rec in records:
        key = tuple(rec.get(k) for k in key_fields)
        if key in seen:
            duplicates.append(rec)
        else:
            seen.add(key)
            unique.append(rec)
    return unique, duplicates
