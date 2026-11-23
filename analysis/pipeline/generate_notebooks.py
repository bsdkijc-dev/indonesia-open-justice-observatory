"""Generate the 10 reproducible IOJO Jupyter notebooks (01 to 10)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
NB_DIR = ROOT / "analysis" / "notebooks"

NOTEBOOKS = [
    ("01_source_inventory.ipynb", "01. Official Source Inventory & Access Assessment", "RQ01, RQ06", "df = pd.read_csv('../../source_inventory/official_sources.csv')\nprint(df[['source_id', 'source_name', 'robots_txt_status', 'redistribution_permitted']])"),
    ("02_judicial_institutions.ipynb", "02. Judicial Institutions Registry", "RQ03, RQ09", "df = pd.read_csv('../../data/synthetic/ds01_institutions.csv')\nprint(df.groupby(['jurisdiction', 'court_type']).size())"),
    ("03_case_statistics.ipynb", "03. Judicial Case Statistics (Zero-Imputation)", "RQ03, RQ04", "df = pd.read_csv('../../data/synthetic/ds02_case_statistics.csv')\nprint(df[['statistic_id', 'court_id', 'incoming_cases', 'resolved_cases', 'validation_status']])"),
    ("04_judgment_publication.ipynb", "04. Judgment Publication Completeness & Timeliness", "RQ06, RQ07", "df = pd.read_csv('../../data/synthetic/ds03_judgment_publication.csv')\nprint(df[['publication_id', 'case_number', 'decision_date', 'publication_date', 'validation_status']])"),
    ("05_public_access.ipynb", "05. Public Access & Judicial Services", "RQ01, RQ09, RQ11", "df = pd.read_csv('../../data/synthetic/ds04_judicial_services.csv')\nprint(df[['service_id', 'service_category', 'accessibility_status']])"),
    ("06_data_quality.ipynb", "06. Data Quality & Missingness Audit", "RQ02, RQ10", "import json\nreport = json.loads(open('../../data/processed/data_quality_report.json').read())\nprint(json.dumps(report['missingness'], indent=2))"),
    ("07_regional_distribution.ipynb", "07. Regional Distribution & Geographic Coverage", "RQ09", "df = pd.read_csv('../../data/synthetic/ds01_institutions.csv')\nprint(df.groupby('province').size())"),
    ("08_performance_indicators.ipynb", "08. Standardized Performance Indicators (IND-01 to IND-10)", "RQ04, RQ05", "df = pd.read_csv('../../data/synthetic/ds06_public_access_indicators.csv')\nprint(df[['indicator_id', 'indicator_name', 'indicator_value', 'unit', 'validation_status']])"),
    ("09_temporal_trends.ipynb", "09. Temporal Trends & Appeal/Review Patterns", "RQ03, RQ08", "df = pd.read_csv('../../data/synthetic/ds02_case_statistics.csv')\nprint(df.groupby('reporting_period')[['incoming_cases', 'resolved_cases']].sum(min_count=1))"),
    ("10_research_limitations.ipynb", "10. Unanswered Questions & Research Limitations", "RQ10, RQ12", "df = pd.read_csv('../../data/synthetic/ds08_research_metadata.csv')\nprint(df[['research_id', 'research_question', 'limitations']])"),
]


def make_notebook(title: str, rqs: str, code: str) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11.2"},
        },
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# {title}\n",
                    f"**Research Questions:** {rqs}  \n",
                    "**Note:** Pilot execution uses `SYNTHETIC_TEST_FIXTURE` data under strict zero-imputation rules.\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["import pandas as pd\n", code + "\n"],
            },
        ],
    }


def main() -> None:
    NB_DIR.mkdir(parents=True, exist_ok=True)
    for fname, title, rqs, code in NOTEBOOKS:
        nb_path = NB_DIR / fname
        nb_path.write_text(json.dumps(make_notebook(title, rqs, code), indent=2), encoding="utf-8")
    print(f"Generated {len(NOTEBOOKS)} notebooks in {NB_DIR}")


if __name__ == "__main__":
    main()
