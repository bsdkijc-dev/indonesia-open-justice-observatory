"""Synthetic test dataset generator for IOJO Datasets 01-08.

All generated records are explicitly tagged as SYNTHETIC_TEST_FIXTURE and are used
strictly to validate schemas, zero-imputation rules, quality controls, and pipelines.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, List

import pandas as pd


def generate_synthetic_datasets(output_dir: Path) -> Dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    files: Dict[str, Path] = {}

    # DS01: Judicial Institutions (Synthetic Fixture mirroring real court tiers)
    ds01 = [
        {
            "institution_id": "INST-MA-000",
            "court_name": "Mahkamah Agung Republik Indonesia",
            "court_type": "Mahkamah Agung",
            "jurisdiction": "Mahkamah Agung",
            "province": "DKI Jakarta",
            "district": "Jakarta Pusat",
            "official_source": "Portal Resmi Mahkamah Agung RI (Synthetic Fixture)",
            "source_url": "https://www.mahkamahagung.go.id",
            "last_verified": "2026-11-23",
            "validation_status": "VERIFIED",
        },
        {
            "institution_id": "INST-PN-JKT-SEL",
            "court_name": "Pengadilan Negeri Jakarta Selatan",
            "court_type": "Tingkat Pertama",
            "jurisdiction": "Umum",
            "province": "DKI Jakarta",
            "district": "Jakarta Selatan",
            "official_source": "Ditjen Badilum MA RI (Synthetic Fixture)",
            "source_url": "https://badilum.mahkamahagung.go.id/statistik-perkara.html",
            "last_verified": "2026-11-23",
            "validation_status": "VERIFIED",
        },
        {
            "institution_id": "INST-PA-BDG",
            "court_name": "Pengadilan Agama Bandung",
            "court_type": "Tingkat Pertama",
            "jurisdiction": "Agama",
            "province": "Jawa Barat",
            "district": "Kota Bandung",
            "official_source": "Ditjen Badilag MA RI (Synthetic Fixture)",
            "source_url": "https://badilag.mahkamahagung.go.id/",
            "last_verified": "2026-11-23",
            "validation_status": "VERIFIED",
        },
        {
            "institution_id": "INST-PTUN-MKS",
            "court_name": "Pengadilan Tata Usaha Negara Makassar",
            "court_type": "Tingkat Pertama",
            "jurisdiction": "Tata Usaha Negara",
            "province": "Sulawesi Selatan",
            "district": "Kota Makassar",
            "official_source": "Ditjen Badilmiltun MA RI (Synthetic Fixture)",
            "source_url": "https://ditjenmiltun.mahkamahagung.go.id/donwload-post/",
            "last_verified": "2026-11-23",
            "validation_status": "VERIFIED",
        },
        {
            "institution_id": "INST-PN-JPR",
            "court_name": "Pengadilan Negeri Jayapura",
            "court_type": "Tingkat Pertama",
            "jurisdiction": "Umum",
            "province": "Papua",
            "district": "Kota Jayapura",
            "official_source": "Ditjen Badilum MA RI (Synthetic Fixture)",
            "source_url": "https://badilum.mahkamahagung.go.id/statistik-perkara.html",
            "last_verified": "2026-11-23",
            "validation_status": "UNVERIFIED",
        },
    ]

    # DS02: Judicial Case Statistics (with intentional null to test zero-imputation)
    ds02 = [
        {
            "statistic_id": "STAT-SYN-0001",
            "court_id": "INST-MA-000",
            "reporting_period": "2024",
            "case_category": "Kasasi & PK (Synthetic)",
            "incoming_cases": 30000,
            "resolved_cases": 29500,
            "pending_cases": 1200,
            "source_document": "SYNTHETIC_TEST_FIXTURE_LAPTAH_2024",
            "source_page": "16",
            "retrieval_date": "2026-11-23",
            "validation_status": "VERIFIED",
        },
        {
            "statistic_id": "STAT-SYN-0002",
            "court_id": "INST-PN-JKT-SEL",
            "reporting_period": "2024",
            "case_category": "Perdata",
            "incoming_cases": 1850,
            "resolved_cases": 1620,
            "pending_cases": 410,
            "source_document": "SYNTHETIC_TEST_FIXTURE_BADILUM_2024",
            "source_page": "4",
            "retrieval_date": "2026-11-23",
            "validation_status": "VERIFIED",
        },
        {
            "statistic_id": "STAT-SYN-0003",
            "court_id": "INST-PA-BDG",
            "reporting_period": "2024",
            "case_category": "Perdata Agama",
            "incoming_cases": 4200,
            "resolved_cases": 3980,
            "pending_cases": 390,
            "source_document": "SYNTHETIC_TEST_FIXTURE_BADILAG_2024",
            "source_page": "11",
            "retrieval_date": "2026-11-23",
            "validation_status": "VERIFIED",
        },
        {
            "statistic_id": "STAT-SYN-0004",
            "court_id": "INST-PTUN-MKS",
            "reporting_period": "2024",
            "case_category": "Tata Usaha Negara",
            "incoming_cases": 145,
            "resolved_cases": 128,
            "pending_cases": 27,
            "source_document": "SYNTHETIC_TEST_FIXTURE_MILTUN_2024",
            "source_page": "8",
            "retrieval_date": "2026-11-23",
            "validation_status": "VERIFIED",
        },
        {
            "statistic_id": "STAT-SYN-0005",
            "court_id": "INST-PN-JPR",
            "reporting_period": "2024",
            "case_category": "Pidana",
            "incoming_cases": 410,
            "resolved_cases": None,  # Intentional null: must NEVER become 0
            "pending_cases": None,
            "source_document": "SYNTHETIC_TEST_FIXTURE_MISSING_REPORT",
            "source_page": None,
            "retrieval_date": "2026-11-23",
            "validation_status": "UNVERIFIED",
        },
    ]

    # DS03: Judgment Publication (Synthetic anonymized metadata)
    ds03 = [
        {
            "publication_id": "PUB-SYN-0001",
            "case_number": "123 K/Pdt/2024 (SYNTHETIC)",
            "court_name": "Mahkamah Agung Republik Indonesia",
            "decision_date": "2024-05-14",
            "publication_date": "2024-06-20",
            "document_url": "https://putusan3.mahkamahagung.go.id/direktori/putusan/synthetic-0001.html",
            "document_type": "Putusan",
            "document_hash": hashlib.sha256(b"synthetic-0001").hexdigest(),
            "source_url": "https://putusan3.mahkamahagung.go.id",
            "retrieval_date": "2026-11-23",
            "validation_status": "VERIFIED",
        },
        {
            "publication_id": "PUB-SYN-0002",
            "case_number": "45/Pdt.G/2024/PN Jkt.Sel (SYNTHETIC)",
            "court_name": "Pengadilan Negeri Jakarta Selatan",
            "decision_date": "2024-07-02",
            "publication_date": "2024-07-18",
            "document_url": "https://putusan3.mahkamahagung.go.id/direktori/putusan/synthetic-0002.html",
            "document_type": "Putusan",
            "document_hash": hashlib.sha256(b"synthetic-0002").hexdigest(),
            "source_url": "https://putusan3.mahkamahagung.go.id",
            "retrieval_date": "2026-11-23",
            "validation_status": "VERIFIED",
        },
        {
            "publication_id": "PUB-SYN-0003",
            "case_number": "88/Pdt.G/2024/PA.Bdg (SYNTHETIC)",
            "court_name": "Pengadilan Agama Bandung",
            "decision_date": "2024-08-11",
            "publication_date": None,  # Missing publication date
            "document_url": None,
            "document_type": "Putusan",
            "document_hash": None,
            "source_url": "https://putusan3.mahkamahagung.go.id",
            "retrieval_date": "2026-11-23",
            "validation_status": "UNVERIFIED",
        },
    ]

    # DS04: Judicial Service Information
    ds04 = [
        {
            "service_id": "SVC-SYN-0001",
            "court_id": "INST-MA-000",
            "service_category": "e-Court",
            "service_description": "Pendaftaran perkara dan persidangan elektronik (memerlukan akun terdaftar).",
            "official_url": "https://ecourt.mahkamahagung.go.id",
            "accessibility_status": "RESTRICTED",
            "last_verified": "2026-11-23",
            "validation_status": "VERIFIED",
        },
        {
            "service_id": "SVC-SYN-0002",
            "court_id": "INST-MA-000",
            "service_category": "Laporan Tahunan",
            "service_description": "Publikasi PDF Laporan Tahunan Kepaniteraan Mahkamah Agung RI.",
            "official_url": "https://kepaniteraan.mahkamahagung.go.id/id/publikasi/laporan-tahunan",
            "accessibility_status": "ACCESSIBLE",
            "last_verified": "2026-11-23",
            "validation_status": "VERIFIED",
        },
    ]

    # DS05: Judicial Regulations (verified PERMA references from public search)
    ds05 = [
        {
            "regulation_id": "REG-PERMA-2025-002",
            "regulation_number": "2 Tahun 2025",
            "regulation_year": 2025,
            "regulation_type": "PERMA",
            "title": "Pedoman Mengadili Perkara Penyandang Disabilitas (Akomodasi yang Layak)",
            "effective_date": None,
            "status": "BERLAKU",
            "official_source": "Peraturan BPK / MA RI",
            "source_url": "https://peraturan.bpk.go.id/Download/413027/2025perma002.pdf",
            "verification_status": "VERIFIED",
        },
        {
            "regulation_id": "REG-PERMA-2025-003",
            "regulation_number": "3 Tahun 2025",
            "regulation_year": 2025,
            "regulation_type": "PERMA",
            "title": "Pedoman Penanganan Perkara Tindak Pidana di Bidang Perpajakan",
            "effective_date": None,
            "status": "BERLAKU",
            "official_source": "Peraturan BPK / MA RI",
            "source_url": "https://peraturan.bpk.go.id/Download/413028/2025perma003.pdf",
            "verification_status": "VERIFIED",
        },
    ]

    # DS06: Public Access Indicators (Derived from DS02/DS03)
    ds06 = [
        {
            "indicator_id": "IND-03-SYN-001",
            "court_id": "INST-PN-JKT-SEL",
            "reporting_period": "2024",
            "indicator_name": "Case Clearance Rate (resolved / incoming)",
            "indicator_value": round(1620 / 1850 * 100, 2),
            "unit": "percent",
            "denominator": "1850",
            "source": "DS02:STAT-SYN-0002",
            "calculation_method": "(resolved_cases / incoming_cases) * 100",
            "validation_status": "DERIVED",
        },
        {
            "indicator_id": "IND-02-SYN-001",
            "court_id": "INST-MA-000",
            "reporting_period": "2024",
            "indicator_name": "Publication Timeliness",
            "indicator_value": 37.0,
            "unit": "days",
            "denominator": "1",
            "source": "DS03:PUB-SYN-0001",
            "calculation_method": "publication_date - decision_date",
            "validation_status": "DERIVED",
        },
    ]

    # DS07: Data Quality Register
    ds07 = [
        {
            "record_id": "DQR-SYN-0001",
            "dataset_name": "DS02_case_statistics",
            "source": "SYNTHETIC_TEST_FIXTURE",
            "missing_fields": "resolved_cases;pending_cases;source_page (STAT-SYN-0005)",
            "duplicate_status": "NO_DUPLICATES",
            "validation_status": "VERIFIED",
            "reviewer": "VALIDATION_AGENT",
            "review_date": "2026-11-23",
            "correction_notes": "Preserved nulls per zero-imputation policy; STAT-SYN-0005 marked UNVERIFIED.",
        }
    ]

    # DS08: Public Research Metadata
    ds08 = [
        {
            "research_id": "RES-PILOT-001",
            "dataset_id": "DS01-DS07",
            "research_question": "RQ01;RQ02;RQ03;RQ04;RQ07;RQ10",
            "methodology": "Descriptive audit, zero-imputation missingness profiling, and reproducible indicator derivation.",
            "limitations": "Pilot phase uses synthetic fixtures for schema/pipeline verification; live bulk collection awaits human approval.",
            "publication_date": None,
            "repository_url": "https://github.com/bsdkijc-dev/indonesia-open-justice-observatory",
            "citation": "Mustafa, C. (2026). Indonesia Open Justice Observatory (IOJO) v1.0-pilot.",
        }
    ]

    datasets = {
        "ds01_institutions": ds01,
        "ds02_case_statistics": ds02,
        "ds03_judgment_publication": ds03,
        "ds04_judicial_services": ds04,
        "ds05_judicial_regulations": ds05,
        "ds06_public_access_indicators": ds06,
        "ds07_data_quality_register": ds07,
        "ds08_research_metadata": ds08,
    }

    for name, rows in datasets.items():
        json_path = output_dir / f"{name}.json"
        csv_path = output_dir / f"{name}.csv"
        json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        pd.DataFrame(rows).to_csv(csv_path, index=False, encoding="utf-8")
        files[name] = json_path

    return files


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "data" / "synthetic"
    generated = generate_synthetic_datasets(out)
    print(f"Generated {len(generated)} synthetic datasets in {out}")
