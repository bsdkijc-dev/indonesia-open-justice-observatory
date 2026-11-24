# Mahkamah Agung RI — Landmark Decisions Pilot (Stage 6 Staging Package)

* **Target GitHub Repository**: `bsdkijc-dev/indonesia-open-justice-observatory` (extension module)

* **Target Kaggle Dataset**: `judicialcollege/ma-ri-landmark-decisions-pilot` (`isPrivate: true`, license `CC-BY-4.0`)

* **Governance Status**: **STAGED PRIVATE — PENDING EXPLICIT HUMAN APPROVAL**

## Included Files

1. `stage4_pilot_annotated_32.csv` — 32-row UTF-8 tabular dataset (10 PK, 21 Kasasi, 1 Uji Pendapat; 617 pages total).

2. `stage4_pilot_annotated_32.json` — Full 9-part structured JSON validated against `stage3_annotation_schema.json`.

3. `data_dictionary.csv` — Column-level schema and governance rules.

4. `dataset-metadata.json` — Kaggle API metadata (`isPrivate: true`).

5. `stage5_qa_audit_report.json` — Independent Stage 5 QA audit results.

## Mandatory Controls Applied

* **Zero-Imputation**: Missing fields remain empty/`null` with explicit `completeness_flags`.

* **Privacy by Design**: Evaluated against UU No. 27 Tahun 2022 (UU PDP), UU No. 14 Tahun 2008 (UU KIP), and SK KMA 2-144/KMA/SK/VIII/2022; 26 decisions flagged `BLOCKED_NEEDS_ANONYMISATION_REVIEW` must undergo human redaction before any public release.

* **No Institutional Endorsement**: Independent research compilation; `is_official_ma_position` is strictly `false`.