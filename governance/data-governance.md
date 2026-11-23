# Data Governance Policy — Indonesia Open Justice Observatory (IOJO)

**Effective Date:** 2026-11-23  
**Research Director:** Cecep Mustafa, Ph.D.  
**Status:** Active (v1.0-pilot)

## 1. Purpose and Scope
This policy governs the discovery, collection, normalization, validation, storage, and release of all data managed by the Indonesia Open Justice Observatory (IOJO).

## 2. Independence & Non-Endorsement
IOJO is an independent, evidence-based judicial research initiative. No dataset, indicator, or report may claim official Mahkamah Agung RI endorsement or institutional authorship unless formally authorized in writing.

## 3. Zero-Imputation & No-Fabrication Standard
- **Zero-Imputation:** Missing values must remain `null` (or empty cells in UTF-8 CSV exports) with explicit completeness flags. Missing values must **never** be converted to `0`.
- **No Fabrication:** Unavailable statistics, dates, or court identifiers must never be invented or extrapolated.
- **Original Figures Preserved:** Source-reported figures are stored separately from derived indicators, with variances logged in `data_quality_register`.

## 4. Validation States
Every record in IOJO datasets must carry one of three validation states:
1. `VERIFIED`: Directly supported by a traceable, verified official source.
2. `DERIVED`: Calculated using a documented, reproducible method from `VERIFIED` source data.
3. `UNVERIFIED`: Insufficiently supported, incomplete, or pending verification; **never** published as established fact.

## 5. Human Approval Gates
Human approval from the Research Director is mandatory before:
- Accessing restricted or authenticated information.
- Increasing automated collection intensity materially.
- Publishing datasets to Kaggle, GitHub, or GitHub Pages.
- Publishing reports as external outputs.
- Deleting core datasets or overwriting existing repositories.
