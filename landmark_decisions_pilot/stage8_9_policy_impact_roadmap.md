# Stages 8–9: Evidence-Based Judicial Policy Report, Public Trust Impact Framework, and 90-Day Implementation Roadmap

**Scope & Disclaimer:** Independent research synthesis grounded in the 32-decision pilot (`stage4_pilot_annotated_32.csv`, 617 pages) and existing `bsdkijc-dev` / `judicialcollege` baselines. This report does not represent an official position of Mahkamah Agung Republik Indonesia (MA RI).

## 1. Evidence-Based Judicial Policy Report (Stage 8)

### Recommendation 1 — Standardize Pre-Publication Anonymisation Checks for e-Court Filings

* **Supporting Evidence:** 26 of 32 pilot PDFs (81.25%) triggered Stage 2 privacy flags, driven by unredacted full street addresses beyond Dati 2, personal `@gmail.com` / `@yahoo.com` e-Court domisili elektronik addresses in TUN and Agama filings, mobile numbers in criminal evidence lists (`69 PK/Pid/2018`, `78 PK/Pid/2025`), and family-dispute identities (`738 PK/Pdt/2025`) under [SK KMA 2-144/KMA/SK/VIII/2022](https://www.pn-parepare.go.id/berita/artikel-hukum/pengaburan-anonimisasi-data-putusan-dalam-sk-kma-no-2-144-kma-sk-viii-2022) and [UU No. 27 Tahun 2022](https://pasal.id/peraturan/uu/uu-no-27-tahun-2022).

* **Limitations:** Automated regex/rule scans in Stage 2 cannot verify contextual sensitivity (e.g., indirect re-identification in rural land disputes) without human legal review.

* **Implementation Requirements:** Deploy deterministic pre-upload PII screening (extending `stage2_privacy_gate.py`) at court-level minutasi workflows before PDFs reach public portals, masking street-level addresses to Dati 2 and redacting personal e-Court emails.

### Recommendation 2 — Provide Structured Machine-Readable Metadata Feeds Alongside PDFs

* **Supporting Evidence:** `putusan3.mahkamahagung.go.id` blocks automated collection (`HTTP/2 403`), and deterministic regex parsing recovered statutory provisions in only 65.6% (21/32) of PDFs due to inconsistent citation formatting, compared with 90.6% (29/32) for *amar* headers. Benchmarking Estonia's [Riigi Teataja](https://www.riigiteataja.ee/en/eli/502122022001/consolide) and [e-File](https://www.kohus.ee/en) shows that structured metadata fields eliminate downstream parsing errors.

* **Limitations:** Direct institutional API access is outside this project's scope; findings reflect 32 landmark-nominated PDFs rather than all national court filings.

* **Implementation Requirements:** Publish a lightweight, read-only JSON/CSV metadata index (linking canonical `satker` IDs from `indonesia-master-court-registry-2026`) under [UU No. 14 Tahun 2008](https://peraturan.bpk.go.id/Details/39047/uu-no-14-tahun-2008) without centralizing raw case files.

### Recommendation 3 — Separate Official Holdings from Independent Research Commentary

* **Supporting Evidence:** Stage 3–4 schema validation (`stage3_annotation_schema.json`) achieved 0 schema errors across 32 decisions by isolating `official_judicial_content` from `independent_research_commentary` (`is_official_ma_position: false`).

* **Limitations:** Deterministic extraction captures verbatim text spans rather than doctrinal synthesis; human legal experts must verify *ratio decidendi* summaries.

* **Implementation Requirements:** Require `is_official_ma_position: false` and explicit SHA-256 provenance on all GitHub/Kaggle research releases.

### Recommendation 4 — Enforce Zero-Imputation Reporting in Judicial Transparency Scorecards

* **Supporting Evidence:** Stage 4 averaged 6.5 of 9 fields populated per decision; leaving missing fields as `null` prevented artificial inflation of completeness metrics, aligning with `indonesia-open-justice-observatory` (69.09% metadata completeness in 2025 Laptah).

* **Limitations:** Incomplete extraction reflects PDF formatting variance as well as source omissions.

* **Implementation Requirements:** Maintain CI validation gates (`stage5_independent_qa.py`) blocking any PR that converts `null` to `0` or synthetic defaults.

## 2. Public Trust Impact Framework (Stage 9)

Downloads and pageviews are **not** equated with public trust. Impact is tracked through verifiable integrity and reuse indicators:

| Indicator | Pilot Baseline (24 Nov 2026) | 90-Day Target | Verification Method | 
| ----- | ----- | ----- | ----- | 
| Verified decisions processed | 32 (10 PK, 21 Kasasi, 1 UP) | 100+ (min. 50 PK) | `stage1_all_decisions_manifest.csv` | 
| Complete SHA-256 provenance | 100% (32/32) | 100% | `stage5_independent_qa.py` | 
| Privacy gate pass (post-redaction) | 18.8% raw (6/32) | 100% of released rows | Human sign-off + `stage2_privacy_gate.py` | 
| Annotation schema compliance | 100% (0 errors) | 100% | `jsonschema` CI check | 
| Documented corrections & errata | 0 (baseline) | 100% logged in `CHANGELOG` | GitHub issue/PR log | 
| Public legal literacy outputs | 0 (staged) | 3 Bahasa Indonesia guides | PK, Kasasi, and Legal Aid explainers | 

## 3. 90-Day Implementation Roadmap (Rp0 Budget)

* **Days 1–30 (Human Privacy Review & PK Corpus Expansion):** Complete human redaction review on the 26 flagged decisions; collect 40–90 additional manually exported PK PDFs from `putusan3` to reach 50–100 PK decisions; run `stage2_privacy_gate.py`.

* **Days 31–60 (Human Legal Verification & Private Staging Push):** Convene legal reviewers to verify *kaidah hukum* and statutory citations on the expanded PK corpus; execute `deploy_stage6_staging.sh` upon explicit human approval to push to `bsdkijc-dev/indonesia-open-justice-observatory` and private Kaggle `judicialcollege/ma-ri-landmark-decisions-pilot`.

* **Days 61–90 (Observatory Launch & Public Legal Literacy):** Publish the Bahasa Indonesia public legal literacy guides (PK vs. Kasasi, court fees, legal aid), release the Stage 7 Observatory on GitHub Pages, and open Kaggle dataset access only after final human governance sign-off.