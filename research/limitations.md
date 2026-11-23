# Known Limitations & Methodological Safeguards

1. **Access & Network Constraints:** Automated bulk collection from Indonesian judicial portals may be restricted by `robots.txt`, rate limits, CAPTCHA, or format heterogeneity (e.g., narrative PDFs vs. structured tables).
2. **Denominator Uncertainty:** In judgment publication analysis, the true total universe of decided cases at satker level is not always published alongside judgment portals.
3. **Reporting Convention Differences:** Case clearance definitions in annual reports may differ between *Rasio Penyelesaian Perkara* (which may include carried-over pending cases in the denominator) and standard `resolved / incoming`.
4. **Missingness Bias:** Courts with lower digital publication rates may differ systematically in geographic remoteness or IT capacity; missingness is reported explicitly rather than imputed.
5. **Pilot Scope:** Pilot datasets in v1.0-pilot use synthetic fixtures to validate schemas, quality controls, and pipelines before human-approved live ingestion.
