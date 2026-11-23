# Indonesia Open Justice Observatory (IOJO)

**Tagline:** *Justice You Can Verify.*  
**Research Director:** Cecep Mustafa, Ph.D.  
**Project Period:** 2027–2030  
**Project Type:** Independent, evidence-based judicial research initiative

> **Independence & Attribution Notice:** IOJO is an independent academic and public-interest research infrastructure. It is **not** an official initiative of Mahkamah Agung Republik Indonesia and does not carry institutional endorsement unless formally authorized.

## Mission

IOJO transforms verified, lawfully accessible, public Indonesian judicial information into:
1. Reproducible judicial performance research
2. Public accountability indicators
3. Evidence-based judicial policy intelligence
4. Accessible public information
5. Independent research datasets
6. Public value and institutional learning

## Repository Structure

```text
indonesia-open-justice-observatory/
├── governance/           # Data governance, privacy, source access, publication standard, ethics
├── research/             # Research protocol (RQ01-RQ12), methodology, indicators, limitations
├── schemas/              # JSON Schemas (Datasets 01-08) and unified data dictionary
├── source_inventory/     # Verified official source registry (official_sources.csv)
├── crawler/              # Polite, resumable collection & provenance modules
├── processing/           # Normalization, deduplication, and 3-state validation controls
├── analysis/
│   ├── pipeline/         # DuckDB/Python analytical engine & indicator calculator
│   └── notebooks/        # 10 reproducible Jupyter notebooks (01 to 10)
├── reports/
│   ├── annual_reports/
│   ├── policy_briefs/
│   └── technical_reports/
├── dashboard/            # Lightweight mobile-ready GitHub Pages dashboard (Bahasa Indonesia)
├── tests/                # Automated validation, schema, and pipeline test suite
└── .github/workflows/    # CI/CD for tests, data validation, and dashboard builds
```

## Quick Start

```bash
# 1. Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Generate synthetic test datasets (zero-imputation, strict schema compliance)
python3 -m processing.synthetic_generator

# 3. Run automated data quality & schema validation tests
python3 -m tests.run_all

# 4. Run analytical pipeline (DuckDB with SQLite/Pandas fallback)
python3 -m analysis.pipeline.run_pipeline
```

## Core Principles

- **Zero-Imputation Policy:** Missing values are never converted to `0` or fabricated. Empty/null cells are preserved with explicit completeness flags.
- **Three Validation States:** Every record is tagged `VERIFIED`, `DERIVED`, or `UNVERIFIED`.
- **No Unvalidated Rankings:** No composite national judicial ranking and no ranking of individual judges.
- **Human Approval Gates:** No external dataset publication or high-intensity collection without explicit human approval.
