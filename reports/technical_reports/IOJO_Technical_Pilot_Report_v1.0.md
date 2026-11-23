# Indonesia Open Justice Observatory (IOJO) — Technical Pilot Report v1.0

**Date:** 2026-11-23  
**Research Director:** Cecep Mustafa, Ph.D.  
**Status:** Pilot Infrastructure Complete (Synthetic Fixtures Validated; Live Collection Pending Network & Human Approval)

## 1. Executive Summary
This technical pilot report documents the foundation of the Indonesia Open Justice Observatory (IOJO), an independent judicial research infrastructure (2027–2030). All schemas (`DS01–DS08`), governance policies, automated quality controls, analytical pipelines, 10 reproducible notebooks, CI/CD workflows, and the Bahasa Indonesia public dashboard have been implemented and verified.

## 2. Official Source Discovery & Access Assessment
Ten official Indonesian judicial sources were cataloged in `source_inventory/official_sources.csv`:
- [Portal Resmi Mahkamah Agung RI](https://www.mahkamahagung.go.id)
- [Direktori Putusan MA RI](https://putusan3.mahkamahagung.go.id)
- [Laporan Tahunan Kepaniteraan MA RI](https://kepaniteraan.mahkamahagung.go.id/id/publikasi/laporan-tahunan) (including [Laptah Kepaniteraan 2024](https://kepaniteraan.mahkamahagung.go.id/images/Glosarium/LaptahKepaniteraan2024.pdf) and [Laptah Kepaniteraan TA 2025](https://kepaniteraan.mahkamahagung.go.id/images/Laporan-Tahunan-Kepaniteraan-TA-2025.pdf))
- [Statistik Perkara Ditjen Badilum](https://badilum.mahkamahagung.go.id/statistik-perkara.html)
- [Portal Ditjen Badilag](https://badilag.mahkamahagung.go.id/)
- [Profil & Statistik Peradilan TUN — Ditjen Badilmiltun](https://ditjenmiltun.mahkamahagung.go.id/donwload-post/)
- [JDIH Mahkamah Agung RI](https://jdih.mahkamahagung.go.id) and [Peraturan BPK](https://peraturan.bpk.go.id)
- [e-Court MA RI](https://ecourt.mahkamahagung.go.id) (authentication required; excluded from automated collection)

**Access Constraints:** Automated `robots.txt` inspection on `mahkamahagung.go.id` could not be completed from the sandbox VM (outbound internet disabled) and was inaccessible via automated web browse. Accordingly, `official_sources.csv` records explicit access-verification status and prohibits bulk redistribution without permission.

## 3. Data Architecture & Quality Controls
- **Zero-Imputation Verified:** Synthetic fixture `STAT-SYN-0005` (`resolved_cases=None`, `pending_cases=None`) was preserved as `null` across CSV, JSON, Parquet, and SQL aggregations.
- **Automated Audit Passed:** All 5 unit and schema tests in `tests/test_iojo.py` passed (`OK` in 0.060s), verifying schema conformance, `403` halt behavior, response caching, and detection of negative counts/invalid court IDs.
- **Analytical Engine:** `analysis/pipeline/run_pipeline.py` supports `duckdb` as primary SQL engine with automatic `sqlite3` + `pandas` fallback when `duckdb` is absent in constrained environments.

## 4. Next Steps & Human Approval Gates
1. Enable outbound internet / run in local workstation `.venv` with `duckdb`, `pytest`, and `nbformat` installed.
2. Obtain human approval before any live PDF download from `kepaniteraan.mahkamahagung.go.id` or metadata inspection on `putusan3.mahkamahagung.go.id`.
3. Obtain human approval before publishing datasets to GitHub or Kaggle (`judicialcollege`).
