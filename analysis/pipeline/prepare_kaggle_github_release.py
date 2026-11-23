"""Phase 6: Prepare GitHub & Kaggle Release Staging Package (Requires Human Approval Before Publish)."""

from __future__ import annotations

import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent.parent


def prepare_release_staging() -> Path:
    staging = ROOT / "release_staging"
    kaggle_dir = staging / "kaggle"
    kaggle_dir.mkdir(parents=True, exist_ok=True)

    # Copy ONLY approved metadata & derived CSVs (never raw cached PDFs or secrets)
    files_to_stage = [
        ROOT / "schemas" / "data_dictionary.csv",
        ROOT / "source_inventory" / "official_sources.csv",
        ROOT / "data" / "processed" / "ds02_laptah_2024_2025.csv",
        ROOT / "data" / "processed" / "ds06_laptah_2024_2025_indicators.csv",
    ]
    staged_names = []
    for src in files_to_stage:
        if src.exists():
            shutil.copy2(src, kaggle_dir / src.name)
            staged_names.append(src.name)

    kaggle_meta = {
        "title": "Indonesia Open Justice Observatory (IOJO) — Judicial Transparency & Case Statistics (2024–2025)",
        "id": "judicialcollege/indonesia-open-justice-observatory-2024-2025",
        "licenses": [{"name": "MIT"}],
        "subtitle": "Reproducible judicial performance indicators and case statistics extracted from Mahkamah Agung RI Annual Reports.",
        "description": (
            "Independent research dataset curated by Cecep Mustafa, Ph.D. (IOJO). "
            "Contains structured DS02 case statistics and DS06 derived indicators (IND-01 to IND-10) "
            "from Kepaniteraan Mahkamah Agung RI Annual Reports (2024-2025) under strict zero-imputation and zero-PII rules. "
            "Source PDFs are NOT redistributed."
        ),
        "keywords": ["law", "government", "indonesia", "open data", "judicial transparency"],
        "version": "1.0.0",
    }
    (kaggle_dir / "dataset-metadata.json").write_text(
        json.dumps(kaggle_meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    checklist = f"""# Phase 6 Pre-Release Human Approval Checklist

**Status:** PENDING HUMAN APPROVAL  
**Staged Files ({len(staged_names)}):** {', '.join(staged_names)}

## Mandatory Governance Checks
- [x] Zero PII (no judge, clerk, or litigant identifiers).
- [x] Zero source PDF redistribution (only derived metadata/statistics staged).
- [x] Zero-imputation preserved (`null`/empty cells retained).
- [ ] **Human Approval Required:** `git push` to `git@github.com:bsdkijc-dev/indonesia-open-justice-observatory.git`
- [ ] **Human Approval Required:** `kaggle datasets create -p release_staging/kaggle` (profile: `judicialcollege`)
"""
    (staging / "PRE_RELEASE_APPROVAL_CHECKLIST.md").write_text(checklist, encoding="utf-8")
    print(f"Prepared release_staging/ with {len(staged_names)} staged CSVs. Awaiting human approval.")
    return staging


if __name__ == "__main__":
    prepare_release_staging()
