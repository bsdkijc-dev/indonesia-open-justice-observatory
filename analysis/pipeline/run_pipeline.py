"""IOJO Analytical Pipeline (DuckDB primary with SQLite/Pandas fallback)."""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3
from typing import Any, Dict

import pandas as pd

from processing.validation import (
    audit_case_statistics,
    audit_indicators,
    audit_judgment_publications,
)

ROOT = Path(__file__).resolve().parent.parent.parent


def run_pipeline(data_dir: Path | None = None, out_dir: Path | None = None) -> Dict[str, Any]:
    data_dir = data_dir or (ROOT / "data" / "synthetic")
    out_dir = out_dir or (ROOT / "data" / "processed")
    out_dir.mkdir(parents=True, exist_ok=True)

    ds01 = pd.read_csv(data_dir / "ds01_institutions.csv")
    ds02 = pd.read_csv(data_dir / "ds02_case_statistics.csv")
    ds03 = pd.read_csv(data_dir / "ds03_judgment_publication.csv")
    ds06 = pd.read_csv(data_dir / "ds06_public_access_indicators.csv")

    # Save Parquet deliverables
    for name, df in [("ds01_institutions", ds01), ("ds02_case_statistics", ds02), ("ds03_judgment_publication", ds03)]:
        df.to_parquet(out_dir / f"{name}.parquet", index=False)

    # SQL Analytical Engine: DuckDB if available, else SQLite
    engine_used = "sqlite3_fallback"
    query = """
        SELECT
            i.jurisdiction,
            COUNT(DISTINCT i.institution_id) AS court_count,
            SUM(s.incoming_cases) AS total_incoming,
            SUM(s.resolved_cases) AS total_resolved,
            SUM(s.pending_cases) AS total_pending
        FROM ds01 i
        LEFT JOIN ds02 s ON i.institution_id = s.court_id
        GROUP BY i.jurisdiction
        ORDER BY i.jurisdiction
    """
    try:
        import duckdb  # type: ignore

        con = duckdb.connect(":memory:")
        con.register("ds01", ds01)
        con.register("ds02", ds02)
        summary_df = con.execute(query).df()
        con.close()
        engine_used = "duckdb"
    except ImportError:
        con = sqlite3.connect(":memory:")
        ds01.to_sql("ds01", con, index=False, if_exists="replace")
        ds02.to_sql("ds02", con, index=False, if_exists="replace")
        summary_df = pd.read_sql_query(query, con)
        con.close()

    # Compute Case Clearance Rate ONLY where both incoming and resolved are non-null and > 0
    def _calc_clearance(row: pd.Series) -> float | None:
        inc = row["total_incoming"]
        res = row["total_resolved"]
        if pd.isna(inc) or pd.isna(res) or inc <= 0:
            return None
        return round(float(res) / float(inc) * 100.0, 2)

    summary_df["clearance_rate_pct"] = summary_df.apply(_calc_clearance, axis=1)
    summary_df.to_csv(out_dir / "jurisdiction_summary.csv", index=False, encoding="utf-8")

    # Run automated validation audit
    ds01_records = json.loads((data_dir / "ds01_institutions.json").read_text(encoding="utf-8"))
    ds02_records = json.loads((data_dir / "ds02_case_statistics.json").read_text(encoding="utf-8"))
    ds03_records = json.loads((data_dir / "ds03_judgment_publication.json").read_text(encoding="utf-8"))
    ds06_records = json.loads((data_dir / "ds06_public_access_indicators.json").read_text(encoding="utf-8"))

    court_ids = {r["institution_id"] for r in ds01_records}
    quality_report = {
        "engine_used": engine_used,
        "dataset_type": "SYNTHETIC_TEST_FIXTURE",
        "audits": {
            "ds02_case_statistics": audit_case_statistics(ds02_records, court_ids),
            "ds03_judgment_publication": audit_judgment_publications(ds03_records),
            "ds06_public_access_indicators": audit_indicators(ds06_records),
        },
        "missingness": {
            "ds02_resolved_cases_nulls": int(ds02["resolved_cases"].isna().sum()),
            "ds02_pending_cases_nulls": int(ds02["pending_cases"].isna().sum()),
            "ds03_publication_date_nulls": int(ds03["publication_date"].isna().sum()),
        },
    }
    (out_dir / "data_quality_report.json").write_text(
        json.dumps(quality_report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return quality_report


if __name__ == "__main__":
    report = run_pipeline()
    print(json.dumps(report, indent=2))
