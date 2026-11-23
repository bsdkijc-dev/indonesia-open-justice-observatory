"""Automated validation, schema, crawler, and pipeline tests for IOJO v1.0."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from crawler.official_source_checker import is_official_domain
from crawler.polite_collector import PoliteCollector
from processing.normalization import normalize_int_preserve_null
from processing.synthetic_generator import generate_synthetic_datasets
from processing.validation import (
    audit_case_statistics,
    audit_indicators,
    audit_judgment_publications,
    validate_against_schema,
)

ROOT = Path(__file__).resolve().parent.parent


class TestIOJOFoundation(unittest.TestCase):
    def test_zero_imputation_preserves_null(self) -> None:
        self.assertIsNone(normalize_int_preserve_null(None))
        self.assertIsNone(normalize_int_preserve_null(""))
        self.assertIsNone(normalize_int_preserve_null("N/A"))
        self.assertEqual(normalize_int_preserve_null("1.250"), 1250)

    def test_official_domain_allowlist(self) -> None:
        self.assertTrue(is_official_domain("https://www.mahkamahagung.go.id/id"))
        self.assertTrue(is_official_domain("https://putusan3.mahkamahagung.go.id"))
        self.assertFalse(is_official_domain("https://example.com/fake-court"))

    def test_synthetic_datasets_match_schemas(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            syn_dir = Path(tmp)
            generate_synthetic_datasets(syn_dir)

            ds01 = json.loads((syn_dir / "ds01_institutions.json").read_text(encoding="utf-8"))
            ds02 = json.loads((syn_dir / "ds02_case_statistics.json").read_text(encoding="utf-8"))
            ds03 = json.loads((syn_dir / "ds03_judgment_publication.json").read_text(encoding="utf-8"))
            ds06 = json.loads((syn_dir / "ds06_public_access_indicators.json").read_text(encoding="utf-8"))

            self.assertEqual(validate_against_schema(ds01, ROOT / "schemas" / "institutions_schema.json"), [])
            self.assertEqual(validate_against_schema(ds02, ROOT / "schemas" / "statistics_schema.json"), [])
            self.assertEqual(validate_against_schema(ds03, ROOT / "schemas" / "publication_schema.json"), [])
            self.assertEqual(validate_against_schema(ds06, ROOT / "schemas" / "indicator_schema.json"), [])

            court_ids = {r["institution_id"] for r in ds01}
            self.assertTrue(audit_case_statistics(ds02, court_ids)["passed"])
            self.assertTrue(audit_judgment_publications(ds03)["passed"])
            self.assertTrue(audit_indicators(ds06)["passed"])

    def test_validation_catches_bad_records(self) -> None:
        bad_stats = [
            {
                "statistic_id": "STAT-BAD-1",
                "court_id": "INST-UNKNOWN",
                "reporting_period": "2024",
                "case_category": "Perdata",
                "incoming_cases": -5,
                "resolved_cases": 10,
                "pending_cases": None,
                "source_document": "",
                "retrieval_date": "bad-date",
                "validation_status": "INVALID",
            }
        ]
        res = audit_case_statistics(bad_stats, {"INST-MA-000"})
        self.assertFalse(res["passed"])
        self.assertGreaterEqual(res["issues_count"], 5)

    def test_polite_collector_stops_on_403_and_caches_200(self) -> None:
        class FakeResp:
            def __init__(self, status_code: int, content: bytes = b"ok") -> None:
                self.status_code = status_code
                self.content = content

            def raise_for_status(self) -> None:
                if self.status_code >= 400:
                    raise RuntimeError("HTTP error")

        with tempfile.TemporaryDirectory() as tmp:
            cache_dir = Path(tmp) / "cache"
            prov_log = Path(tmp) / "prov.jsonl"

            # 403 must halt without retry bypass
            c_block = PoliteCollector(cache_dir, prov_log, min_delay_sec=0.0, http_get=lambda *a, **k: FakeResp(403))
            self.assertIsNone(c_block.fetch("https://www.mahkamahagung.go.id/blocked", "SRC-001", "JOB-1"))

            # 200 must cache and hit cache on second call
            calls = {"n": 0}

            def ok_get(*a, **k):
                calls["n"] += 1
                return FakeResp(200, b"<html><title>123 K/Pdt/2024</title></html>")

            c_ok = PoliteCollector(cache_dir, prov_log, min_delay_sec=0.0, http_get=ok_get)
            first = c_ok.fetch("https://www.mahkamahagung.go.id/ok", "SRC-001", "JOB-2")
            second = c_ok.fetch("https://www.mahkamahagung.go.id/ok", "SRC-001", "JOB-3")
            self.assertEqual(first, second)
            self.assertEqual(calls["n"], 1)


if __name__ == "__main__":
    unittest.main()
