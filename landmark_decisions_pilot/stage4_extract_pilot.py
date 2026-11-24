"""Stage 4 deterministic pilot extraction across all 32 MA RI decisions."""
import csv
import json
import re
from pathlib import Path
import jsonschema
import pypdf

OUT_DIR = Path("artifacts/file_generation/ttl=63d/output")
MANIFEST_PATH = OUT_DIR / "stage1_all_decisions_manifest.csv"
SCHEMA_PATH = OUT_DIR / "stage3_annotation_schema.json"

PII_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PII_PHONE_RE = re.compile(r"\b(?:\+62|62|0)8[1-9][0-9]{7,11}\b")
PII_NIK_RE = re.compile(r"\b[1-9][0-9]{15}\b")

LOWER_COURT_RE = re.compile(
    r"\b\d+/[A-Za-z0-9.\-]+/\d{4}/(?:PN|PA|PT|PTA|PTUN|PT\.TUN|PM|Dilmil)[A-Za-z0-9.\s\-]{0,20}",
    re.IGNORECASE,
)
STATUTE_RE = re.compile(
    r"(?:Undang-Undang(?:\s+Nomor)?\s+\d+\s+Tahun\s+\d{4}|"
    r"PERMA\s+Nomor\s+\d+\s+Tahun\s+\d{4}|"
    r"SEMA\s+Nomor\s+\d+\s+Tahun\s+\d{4}|"
    r"SK\s+KMA\s+Nomor\s+[A-Za-z0-9\-/]+|"
    r"Pasal\s+\d+[A-Za-z0-9\s\(\)ayat\-]{0,35}?(?:KUHP|KUHPerdata|KUHAP|KUHPM|UU\s+No\.?\s*\d+\s+Tahun\s+\d{4}))",
    re.IGNORECASE,
)
PRECEDENT_RE = re.compile(
    r"(?:Putusan\s+(?:Mahkamah\s+Agung|Mahkamah\s+Konstitusi)\s+(?:RI\s+)?Nomor\s+[A-Za-z0-9./\-]+|"
    r"Yurisprudensi\s+(?:Mahkamah\s+Agung\s+)?Nomor\s+[A-Za-z0-9./\-]+)",
    re.IGNORECASE,
)
DECISION_DATE_RE = re.compile(
    r"Demikian\s+diputuskan\s+dalam\s+rapat\s+(?:permusyawaratan|musyawarah)\s+Majelis\s+Hakim\s+pada\s+hari\s+[^\n.]{5,90}",
    re.IGNORECASE,
)


def mask_pii(text: str) -> str:
    text = PII_NIK_RE.sub("[REDACTED_NIK]", text)
    text = PII_EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = PII_PHONE_RE.sub("[REDACTED_PHONE]", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_section(text: str, start_patterns: list[str], max_chars: int = 700) -> str | None:
    for pat in start_patterns:
        m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
        if m:
            snippet = text[m.start() : m.start() + max_chars]
            return mask_pii(snippet)
    return None


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = list(csv.DictReader(f))

    records = []
    csv_rows = []
    schema_errors = 0

    for row in manifest:
        pdf_path = Path("downloads") / row["pdf_filename"]
        reader = pypdf.PdfReader(str(pdf_path))
        full_text = "\n".join((p.extract_text() or "") for p in reader.pages)

        lower_refs = sorted(set(mask_pii(x) for x in LOWER_COURT_RE.findall(full_text)))[:12]
        statutes = sorted(set(mask_pii(x) for x in STATUTE_RE.findall(full_text)))[:15]
        precedents = sorted(set(mask_pii(x) for x in PRECEDENT_RE.findall(full_text)))[:10]

        date_m = DECISION_DATE_RE.search(full_text)
        decision_date_text = mask_pii(date_m.group(0)) if date_m else None

        legal_issues = extract_section(full_text, [r"alasan(?:-alasan)?\s+(?:kasasi|peninjauan\s+kembali)", r"permohonan\s+uji\s+pendapat"])
        parties_args = extract_section(full_text, [r"Memori\s+(?:Kasasi|Peninjauan\s+Kembali)", r"dalam\s+gugatannya\s+memohon"])
        reasoning = extract_section(full_text, [r"Menimbang,?\s+bahwa\s+terhadap\s+(?:alasan|keberatan)", r"Mahkamah\s+Agung\s+berpendapat"])
        holdings = extract_section(full_text, [r"Menimbang,?\s+bahwa\s+(?:berdasarkan|oleh\s+karena\s+itu)", r"kaidah\s+hukum"])
        amar = extract_section(full_text, [r"M\s*E\s*N\s*G\s*A\s*D\s*I\s*L\s*I\s*:", r"MENGADILI\s*:"])

        core_fields = [decision_date_text, legal_issues, parties_args, reasoning, holdings, amar]
        populated = sum(1 for x in core_fields if x) + (1 if lower_refs else 0) + (1 if statutes else 0) + (1 if precedents else 0)

        rec = {
            "record_id": row["record_id"],
            "provenance": {
                "decision_number": row["decision_number"],
                "proceeding_level": row["proceeding_level"],
                "chamber": row["chamber"],
                "decision_year": int(row["decision_year"]),
                "pages": int(row["pages"]),
                "drive_source_url": row["drive_source_url"],
                "sha256_checksum": row["sha256_checksum"],
                "privacy_gate_status": row["privacy_gate_status"],
            },
            "official_judicial_content": {
                "case_identification_and_history": {
                    "lower_court_references": lower_refs,
                    "decision_date_text": decision_date_text,
                },
                "legal_issues_excerpt": legal_issues,
                "parties_arguments_excerpt": parties_args,
                "applicable_legal_provisions": statutes,
                "judicial_reasoning_excerpt": reasoning,
                "legal_holdings_excerpt": holdings,
                "final_disposition_amar": amar,
                "relevant_precedents_cited": precedents,
            },
            "independent_research_commentary": {
                "is_official_ma_position": False,
                "privacy_and_redaction_note": f"Stage 2 gate: {row['privacy_gate_status']} ({row['detected_flags']}).",
                "observatory_tag": f"{row['proceeding_level']} | {row['chamber']} | {row['decision_year']}",
            },
            "completeness_flags": {
                "fields_populated": populated,
                "fields_total": 9,
                "extraction_method": "deterministic_pypdf_regex_zero_imputation",
            },
        }

        try:
            jsonschema.validate(instance=rec, schema=schema)
        except jsonschema.ValidationError as exc:
            schema_errors += 1
            print(f"SCHEMA ERROR on {row['record_id']}: {exc.message}")

        records.append(rec)
        csv_rows.append({
            "record_id": row["record_id"],
            "decision_number": row["decision_number"],
            "proceeding_level": row["proceeding_level"],
            "chamber": row["chamber"],
            "decision_year": row["decision_year"],
            "pages": row["pages"],
            "privacy_gate_status": row["privacy_gate_status"],
            "fields_populated": populated,
            "fields_total": 9,
            "lower_court_count": len(lower_refs),
            "statutes_count": len(statutes),
            "precedents_count": len(precedents),
            "has_amar": bool(amar),
            "has_reasoning": bool(reasoning),
            "decision_date_text": decision_date_text or "",
            "applicable_legal_provisions": " | ".join(statutes),
            "final_disposition_amar": amar or "",
            "drive_source_url": row["drive_source_url"],
            "sha256_checksum": row["sha256_checksum"],
        })

    (OUT_DIR / "stage4_pilot_annotated_32.json").write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    with open(OUT_DIR / "stage4_pilot_annotated_32.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        writer.writeheader()
        writer.writerows(csv_rows)

    qa = {
        "total_decisions": len(records),
        "schema_validation_errors": schema_errors,
        "avg_fields_populated_out_of_9": round(sum(r["completeness_flags"]["fields_populated"] for r in records) / len(records), 2),
        "decisions_with_amar": sum(1 for r in records if r["official_judicial_content"]["final_disposition_amar"]),
        "decisions_with_reasoning": sum(1 for r in records if r["official_judicial_content"]["judicial_reasoning_excerpt"]),
        "decisions_with_statutes": sum(1 for r in records if r["official_judicial_content"]["applicable_legal_provisions"]),
        "decisions_with_lower_court_history": sum(1 for r in records if r["official_judicial_content"]["case_identification_and_history"]["lower_court_references"]),
    }
    (OUT_DIR / "stage4_pilot_qa_summary.json").write_text(json.dumps(qa, indent=2), encoding="utf-8")
    print(json.dumps(qa, indent=2))


if __name__ == "__main__":
    main()
