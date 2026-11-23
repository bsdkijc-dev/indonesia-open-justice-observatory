"""Metadata extraction for public judicial documents (zero-PII compliant)."""

from __future__ import annotations

import re
from typing import Dict, Optional
from bs4 import BeautifulSoup


CASE_NUMBER_RE = re.compile(r"\b\d+\s*[A-Za-z./-]+\s*\d{4}\b")


def extract_judgment_metadata(html: str, source_url: str, retrieval_date: str) -> Dict[str, Optional[str]]:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    text = soup.get_text(" ", strip=True)
    case_match = CASE_NUMBER_RE.search(title) or CASE_NUMBER_RE.search(text)
    return {
        "case_number": case_match.group(0) if case_match else None,
        "title": title or None,
        "source_url": source_url,
        "retrieval_date": retrieval_date,
        "validation_status": "VERIFIED" if case_match else "UNVERIFIED",
    }
