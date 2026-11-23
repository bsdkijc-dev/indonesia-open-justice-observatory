"""Phase 3 Automated Extractor for Laporan Tahunan Kepaniteraan MA RI (TA 2025).

Locates the cached PDF in data/cache/, scans for target judicial performance sections
(Keadaan Perkara, Rasio Produktivitas Memutus, Rasio Penyelesaian Perkara, Rerata Waktu
Memutus, Rerata Waktu Minutasi, Perkara Belum Minutasi), preserves raw extracted tables
verbatim, and maps header-verified Masuk/Putus/Sisa columns into DS02 without imputation.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from crawler.provenance import utc_now_iso
from processing.normalization import normalize_int_preserve_null
from processing.validation import audit_case_statistics

ROOT = Path(__file__).resolve().parent.parent
LAPTAH_2025_URL = "https://kepaniteraan.mahkamahagung.go.id/images/Laporan-Tahunan-Kepaniteraan-TA-2025.pdf"

TARGET_SECTIONS = [
    ("KEADAAN PERKARA PADA KAMAR PERDATA", "Kamar Perdata"),
    ("KEADAAN PERKARA PADA KAMAR PIDANA", "Kamar Pidana"),
    ("KEADAAN PERKARA PADA KAMAR AGAMA", "Kamar Agama"),
    ("KEADAAN PERKARA PADA KAMAR MILITER", "Kamar Militer"),
    ("KEADAAN PERKARA PADA KAMAR TATA USAHA NEGARA", "Kamar Tata Usaha Negara"),
    ("RASIO PRODUKTIVITAS MEMUTUS", "Rasio Produktivitas Memutus"),
    ("RASIO PENYELESAIAN PERKARA", "Rasio Penyelesaian Perkara (Clearance Rate)"),
    ("RERATA WAKTU MEMUTUS", "Rerata Waktu Memutus"),
    ("RERATA WAKTU MINUTASI", "Rerata Waktu Minutasi"),
    ("PERKARA BELUM MINUTASI", "Perkara Belum Minutasi"),
]


def find_cached_pdf(cache_dir: Path, url: str = LAPTAH_2025_URL) -> Optional[Path]:
    key = hashlib.sha256(url.encode("utf-8")).hexdigest()
    candidate = cache_dir / f"{key}.pdf"
    if candidate.exists():
        return candidate
    pdfs = sorted(cache_dir.glob("*.pdf"))
    return pdfs[0] if pdfs else None


def detect_target_pages(page_texts: List[str]) -> Dict[str, List[int]]:
    matches: Dict[str, List[int]] = {label: [] for _, label in TARGET_SECTIONS}
    for page_num, text in enumerate(page_texts, start=1):
        upper = " ".join(text.upper().split())
        for pattern, label in TARGET_SECTIONS:
            if pattern in upper:
                matches[label].append(page_num)
    return matches


def _parse_int_cell(cell: Optional[str]) -> Optional[int]:
    if cell is None:
        return None
    text = str(cell).strip()
    if not text or text in ("-", "–", "—"):
        return None
    # Reject pure year headers like 2024 or 2025 when standalone
    if text in ("2021", "2022", "2023", "2024", "2025", "2026"):
        return None
    cleaned = re.sub(r"[^\d]", "", text)
    return normalize_int_preserve_null(cleaned) if cleaned else None


def _detect_column_roles(table: List[List[Optional[str]]]) -> Tuple[int, Dict[str, int]]:
    """Inspect top header rows to locate Masuk, Putus, and Sisa column indices."""
    header_depth = min(3, len(table))
    max_cols = max((len(r) for r in table[:header_depth]), default=0)
    col_headers: List[str] = []
    for c_idx in range(max_cols):
        parts = []
        for r_idx in range(header_depth):
            val = table[r_idx][c_idx] if c_idx < len(table[r_idx]) else None
            if val:
                parts.append(str(val).strip().lower())
        col_headers.append(" ".join(parts))

    roles: Dict[str, int] = {}
    for idx, h in enumerate(col_headers):
        if "masuk" in h and "incoming" not in roles:
            roles["incoming"] = idx
        elif "putus" in h and "resolved" not in roles:
            roles["resolved"] = idx
        elif ("sisa akhir" in h or (h == "sisa" or "sisa " in h)) and "pending" not in roles:
            # Prefer later 'sisa' column if both Sisa Awal and Sisa Akhir exist
            roles["pending"] = idx
        elif "sisa" in h:
            roles["pending"] = idx

    # Determine where data rows begin (skip rows containing header keywords or years)
    data_start = 1
    for r_idx in range(min(4, len(table))):
        row_text = " ".join(str(c or "").lower() for c in table[r_idx])
        if any(k in row_text for k in ("masuk", "putus", "sisa", "uraian", "jenis", "2024", "2025")):
            data_start = r_idx + 1
    return data_start, roles


def extract_numeric_candidates_from_table(
    table: List[List[Optional[str]]],
    page_num: int,
    table_idx: int,
    section_label: str,
    retrieval_date: str,
) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    if not table or len(table) < 2:
        return records

    data_start, roles = _detect_column_roles(table)
    has_explicit_roles = "incoming" in roles or "resolved" in roles

    for row_idx, row in enumerate(table[data_start:], start=1):
        cells = [str(c).strip() if c is not None else "" for c in row]
        if not any(cells):
            continue

        # Pick first non-numeric descriptive label (skipping leading row numbers like '1', '2')
        label = ""
        for c in cells:
            if c and not re.fullmatch(r"\d+\.?", c):
                label = c
                break
        if not label:
            label = f"Row {row_idx}"

        if has_explicit_roles:
            inc = _parse_int_cell(cells[roles["incoming"]]) if "incoming" in roles and roles["incoming"] < len(cells) else None
            res = _parse_int_cell(cells[roles["resolved"]]) if "resolved" in roles and roles["resolved"] < len(cells) else None
            pend = _parse_int_cell(cells[roles["pending"]]) if "pending" in roles and roles["pending"] < len(cells) else None
            val_status = "VERIFIED"
        else:
            # Fallback for tables without explicit Masuk/Putus headers: preserve nulls, mark UNVERIFIED
            nums = [_parse_int_cell(c) for c in cells[1:]]
            nums = [n for n in nums if n is not None]
            inc = nums[0] if len(nums) > 0 else None
            res = nums[1] if len(nums) > 1 else None
            pend = nums[2] if len(nums) > 2 else None
            val_status = "UNVERIFIED"

        if inc is not None or res is not None or pend is not None:
            records.append(
                {
                    "statistic_id": f"STAT-LAP25-P{page_num:03d}-T{table_idx:02d}-R{row_idx:03d}",
                    "court_id": "INST-MA-000",
                    "reporting_period": "2025",
                    "case_category": f"{section_label} [p.{page_num} t.{table_idx}]: {label[:70]}",
                    "incoming_cases": inc,
                    "resolved_cases": res,
                    "pending_cases": pend,
                    "source_document": "Laporan Tahunan Kepaniteraan MA RI TA 2025",
                    "source_page": str(page_num),
                    "retrieval_date": retrieval_date,
                    "validation_status": val_status,
                }
            )
    return records


def run_laptah_2025_extraction(
    cache_dir: Path | None = None,
    out_dir: Path | None = None,
) -> Dict[str, Any]:
    cache_dir = cache_dir or (ROOT / "data" / "cache")
    out_dir = out_dir or (ROOT / "data" / "processed")
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = find_cached_pdf(cache_dir)
    if pdf_path is None:
        raise FileNotFoundError(f"No cached Laptah 2025 PDF found in {cache_dir}")

    import pdfplumber  # type: ignore

    retrieval_date = utc_now_iso()[:10]
    page_texts: List[str] = []
    extracted_records: List[Dict[str, Any]] = []
    raw_tables: List[Dict[str, Any]] = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for p in pdf.pages:
            page_texts.append(p.extract_text() or "")

        section_pages = detect_target_pages(page_texts)
        target_page_set = {pg for pages in section_pages.values() for pg in pages}

        for page_num in sorted(target_page_set):
            page = pdf.pages[page_num - 1]
            active_labels = [lbl for lbl, pgs in section_pages.items() if page_num in pgs]
            section_label = active_labels[0] if active_labels else "Laptah 2025"
            tables = page.extract_tables() or []
            for t_idx, tbl in enumerate(tables, start=1):
                raw_tables.append(
                    {
                        "page": page_num,
                        "table_index": t_idx,
                        "section": section_label,
                        "rows": tbl,
                    }
                )
                extracted_records.extend(
                    extract_numeric_candidates_from_table(tbl, page_num, t_idx, section_label, retrieval_date)
                )

    (out_dir / "laptah_2025_raw_tables.json").write_text(
        json.dumps(raw_tables, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    out_json = out_dir / "ds02_laptah_2025_extracted.json"
    out_csv = out_dir / "ds02_laptah_2025_extracted.csv"
    out_json.write_text(json.dumps(extracted_records, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.DataFrame(extracted_records).to_csv(out_csv, index=False, encoding="utf-8")

    audit = audit_case_statistics(extracted_records, {"INST-MA-000"})
    verified_count = sum(1 for r in extracted_records if r["validation_status"] == "VERIFIED")
    summary = {
        "pdf_path": str(pdf_path),
        "total_pages": total_pages,
        "section_pages": section_pages,
        "raw_tables_count": len(raw_tables),
        "extracted_records_count": len(extracted_records),
        "verified_records_count": verified_count,
        "unverified_records_count": len(extracted_records) - verified_count,
        "audit": audit,
    }
    (out_dir / "laptah_2025_extraction_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    res = run_laptah_2025_extraction()
    print(json.dumps(res, indent=2, ensure_ascii=False))
