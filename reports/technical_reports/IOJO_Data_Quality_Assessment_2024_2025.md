# Judicial Data Quality Assessment (2024–2025 Laptah Kepaniteraan)

- **Total DS02 Records:** 290
- **Total DS06 Indicators:** 132
- **Zero-Imputation Compliance:** 100% (missing counts preserved as `null`/`NaN`, never converted to `0`).
- **Known Extraction Limitation:** Multi-row PDF headers and sub-tables reporting only dispositions (e.g., 2025 p.15) leave `incoming_cases` and `pending_cases` as `null` by design.
