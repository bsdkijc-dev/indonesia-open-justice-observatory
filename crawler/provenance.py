"""Provenance tracking and SHA-256 checksum utilities for IOJO."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class ProvenanceRecord:
    job_id: str
    source_id: str
    url: str
    retrieval_timestamp: str
    collection_method: str
    http_status: Optional[int]
    file_checksum: Optional[str]
    file_format: Optional[str]
    extraction_status: str
    validation_status: str
    error_details: Optional[str] = None


def compute_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def record_provenance(record: ProvenanceRecord, log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
