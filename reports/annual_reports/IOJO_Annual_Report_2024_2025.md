# Indonesia Open Justice Annual Report (2024–2025 Empirical Baseline)

**Project:** Indonesia Open Justice Observatory (IOJO) — *Justice You Can Verify*  
**Research Director:** Cecep Mustafa, Ph.D.  
**Date:** 2026-11-23  
**Independence Notice:** IOJO is an independent academic research initiative and is not an official Mahkamah Agung RI publication.

## 1. Empirical Findings (2024 vs. 2025 Apex Registry Reports)
Data were extracted from [LaptahKepaniteraan2024.pdf](https://kepaniteraan.mahkamahagung.go.id/images/Glosarium/LaptahKepaniteraan2024.pdf) and [Laporan-Tahunan-Kepaniteraan-TA-2025.pdf](https://kepaniteraan.mahkamahagung.go.id/images/Laporan-Tahunan-Kepaniteraan-TA-2025.pdf) using DuckDB (`engine_used: duckdb`) under strict zero-imputation rules:

| Metric | 2024 | 2025 |
|---|---:|---:|
| Extracted DS02 Rows | 180 | 110 |
| Header-Verified Rows (`VERIFIED`) | 119 | 69 |
| Metadata Completeness (`IND-06`, `DERIVED`) | 94.07% | 69.09% |
| Source Verifiability (`IND-07`, `DERIVED`) | 66.11% | 62.73% |

## 2. Unanswerable Questions Under Current Public PDFs (RQ10)
The following IOJO indicators remain **`null` (`UNVERIFIED`)** when relying solely on apex annual report PDFs:
- **IND-01 (Publication Completeness):** Requires satker-level decided-case denominators paired with Direktori Putusan counts.
- **IND-02 (Publication Timeliness):** Requires case-level `decision_date` and `publication_date`.
- **IND-05 (Case Duration):** Requires case-level `registration_date` and `decision_date`.
- **IND-08 & IND-09 (Geographic Coverage & Accessibility):** Apex reports aggregate national Supreme Court chambers rather than regional first-instance/appellate satkers.

## 3. Policy Opinions & Recommendations (Clearly Separated from Empirical Findings)
1. **Publish Machine-Readable CSV/Parquet Companion Tables:** Releasing annual report tables alongside PDFs would raise `IND-06` and `IND-07` toward 100%.
2. **Standardize Clearance-Rate Definitions:** Explicitly distinguish `resolved / incoming` from `resolved / (incoming + prior_year_pending)` in all public summaries.
