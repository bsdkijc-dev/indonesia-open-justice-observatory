# Changelog

All notable changes to the Indonesia Open Justice Observatory (IOJO) will be documented in this file.

## [1.0.0-pilot] - 2026-11-23
### Added
- Initialized repository structure (`governance/`, `research/`, `schemas/`, `source_inventory/`, `crawler/`, `processing/`, `analysis/`, `reports/`, `dashboard/`, `tests/`, `.github/workflows/`).
- Authored 5 governance documents and 4 research protocol/methodology documents covering RQ01–RQ12 and Indicators 01–10.
- Defined JSON Schemas for Datasets 01–08 and unified `data_dictionary.csv`.
- Registered verified official Indonesian judicial sources in `source_inventory/official_sources.csv` with access-condition assessments.
- Implemented modular collection engine (`crawler/`), normalization/deduplication/validation (`processing/`), and synthetic test dataset generator.
- Built DuckDB/Python analytical pipeline (with SQLite/Pandas fallback), 10 Jupyter notebooks, lightweight Bahasa Indonesia dashboard, and Technical Pilot Report.
