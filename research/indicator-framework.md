# Performance Indicator Framework (Indicators 01–10)

Every indicator published by IOJO must document: **Definition, Numerator, Denominator, Unit, Reporting Period, Data Source, Calculation Method, Missingness, and Limitations.**

| ID | Indicator Name | Formula / Definition | Safeguard / Constraint |
|---|---|---|---|
| **IND-01** | Publication Completeness | `verified_published_records / known_record_universe` | Calculate **only** when denominator is known. |
| **IND-02** | Publication Timeliness | `publication_date - decision_date` (days) | Use **only** records with both verified dates. |
| **IND-03** | Case Clearance Rate | `resolved_cases / incoming_cases` (or `× 100%`) | Label exact definition; note if pending carryover is included in denominator. |
| **IND-04** | Pending Caseload | Reported `pending_cases` at reporting date | Do not impute missing periods. |
| **IND-05** | Case Duration | `decision_date - registration_date` (days) | **Never** calculate from `publication_date`. |
| **IND-06** | Metadata Completeness | `% of required metadata fields populated with valid values` | Report per-field missingness. |
| **IND-07** | Source Verifiability | `% of records with traceable official sources` | Exclude broken/unverified URLs. |
| **IND-08** | Geographic Coverage | Distribution of verifiable records across jurisdictions & provinces | Stratify by court type. |
| **IND-09** | Public Accessibility | Availability of information via usable public channels | Document login/CAPTCHA/format barriers. |
| **IND-10** | Reproducibility | `% of published indicators with documented data, definitions, and reproducible code` | Must pass CI verification. |
