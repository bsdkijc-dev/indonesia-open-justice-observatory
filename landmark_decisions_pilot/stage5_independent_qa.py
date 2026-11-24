"""Stage 5 Independent Quality Assurance audit for the 32-decision pilot corpus."""
import csv
import hashlib
import json
import re
from pathlib import Path
import jsonschema

OUT_DIR = Path("artifacts/file_generation/ttl=63d/output")
JSON_PATH = OUT_DIR / "stage4_pilot_annotated_32.json"
CSV_PATH = OUT_DIR / "stage4_pilot_annotated_32.csv"
MANIFEST_PATH = OUT_DIR / "stage1_all_decisions_manifest.csv"
SCHEMA_PATH = OUT_DIR / "stage3_annotation_schema.json"
KAGGLE_META_PATH = OUT_DIR / "dataset-metadata.json"

NIK_RE = re.compile(r"\b[1-9][0-9]{15}\b")
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"\b(?:\+62|62|0)8[1-9][0-9]{7,11}\b")


def run_qa() -> dict:
    records = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    with open(CSV_PATH, encoding="utf-8") as f:
        csv_rows = list(csv.DictReader(f))
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest_rows = {r["record_id"]: r for r in csv.DictReader(f)}

    checksum_mismatches = 0
    schema_errors = 0
    pii_leaks = 0
    commentary_flag_errors = 0

    for rec in records:
        rid = rec["record_id"]
        try:
            jsonschema.validate(instance=rec, schema=schema)
        except jsonschema.ValidationError:
            schema_errors += 1

        m_row = manifest_rows.get(rid)
        if not m_row:
            checksum_mismatches += 1
        else:
            pdf_file = Path("downloads") / m_row["pdf_filename"]
            actual_sha = hashlib.sha256(pdf_file.read_bytes()).hexdigest()
            if actual_sha != rec["provenance"]["sha256_checksum"]:
                checksum_mismatches += 1

        if rec["independent_research_commentary"]["is_official_ma_position"] is not False:
            commentary_flag_errors += 1

        serialized = json.dumps(rec["official_judicial_content"], ensure_ascii=False)
        if NIK_RE.search(serialized) or EMAIL_RE.search(serialized) or PHONE_RE.search(serialized):
            pii_leaks += 1

    csv_pii_leaks = 0
    for row in csv_rows:
        joined = " ".join(str(v) for v in row.values())
        if NIK_RE.search(joined) or EMAIL_RE.search(joined) or PHONE_RE.search(joined):
            csv_pii_leaks += 1

    kaggle_meta = json.loads(KAGGLE_META_PATH.read_text(encoding="utf-8"))
    title_len = len(kaggle_meta.get("title", ""))
    subtitle_len = len(kaggle_meta.get("subtitle", ""))
    kaggle_valid = (6 <= title_len <= 50) and (20 <= subtitle_len <= 80) and (kaggle_meta.get("isPrivate") is True)

    report = {
        "total_json_records": len(records),
        "total_csv_rows": len(csv_rows),
        "row_count_match": len(records) == len(csv_rows) == 32,
        "checksum_mismatches": checksum_mismatches,
        "schema_errors": schema_errors,
        "json_pii_leaks": pii_leaks,
        "csv_pii_leaks": csv_pii_leaks,
        "commentary_separation_errors": commentary_flag_errors,
        "kaggle_metadata_valid_and_private": kaggle_valid,
        "overall_qa_status": (
            "PASS_READY_FOR_HUMAN_APPROVAL"
            if (
                len(records) == len(csv_rows) == 32
                and checksum_mismatches == 0
                and schema_errors == 0
                and pii_leaks == 0
                and csv_pii_leaks == 0
                and commentary_flag_errors == 0
                and kaggle_valid
            )
            else "FAIL_REVIEW_REQUIRED"
        ),
    }
    (OUT_DIR / "stage5_qa_audit_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    run_qa()
