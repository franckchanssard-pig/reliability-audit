---
tags: [reliability, audit, cli, reporting]
owners: []
last_reviewed: 2026-02-05
---

# Run Reliability Audit CLI

## When to use
- Generate a reliability score and report from Pigment performance CSVs.
- Produce CSV and HTML reports for a workspace reliability audit.
- Run a repeatable audit workflow with configurable thresholds.

## Outcome
- Audit reports generated in `output/` (CSV summary, findings, HTML report).
- Console summary with total score and grade.

## Prerequisites
- Python 3 environment with dependencies in `pigment-agent-skills/reliability-audit/requirements.txt`.
- Performance CSV exports for executions and views.
- Optional: ARMSET/UPMSET CSV.

## Inputs
- Paths to executions, views, and ARMSET/UPMSET CSV files.
- Optional `config.yaml` and thresholds overrides.
- Output format selection (`csv`, `html`, or `all`).

## Procedure
1. Install dependencies from `requirements.txt`. Why: the CLI depends on pandas and PyYAML. Failure modes: `ModuleNotFoundError` for `pandas` or `yaml`; diagnose by running `python -m pip show pandas` and confirming install.
   ```bash
   python -m pip install -r pigment-agent-skills/reliability-audit/requirements.txt
   ```
2. Create a config file or pass CSV paths directly. Why: default config points to sample file names that may not exist in this repo. Failure modes: “No data loaded” errors; diagnose by confirming file paths and that the CSVs exist.
   ```bash
   cp pigment-agent-skills/reliability-audit/config/config.example.yaml \
      pigment-agent-skills/reliability-audit/config/config.yaml
   ```
3. Run the audit CLI with explicit CSV paths when needed. Why: explicit paths avoid mismatches with default sample names. Failure modes: wrong CSV format or missing headers; diagnose by checking CSV headers against expected columns like `execution_time`, `metric_id`, and `nb_dims`.
   ```bash
   python -m src.main \
     --executions "sample-data/1. Executions.csv" \
     --views "sample-data/6. Views Executions.csv" \
     --armset "sample-data/2. Armset and Upmset Executions.csv" \
     --format all
   ```
4. Review the console score summary and generated outputs. Why: the CLI prints the grade and recommendations. Failure modes: missing output files; diagnose by checking the `output/` directory and ensuring write permissions.

## Verification
- `output/` contains `audit_summary_*.csv` and, if enabled, `audit_report_*.html`.
- Console output includes a total score and grade with component breakdown.

## Edge cases & recovery
- If only executions or views data is available, the tool still runs but scores will be partial; note this in the report.
- If your CSVs are large, use filters in `config.yaml` to limit by application or date range.
- Do not store API keys in committed config files; use environment-specific copies.

## References
- `pigment-agent-skills/reliability-audit/src/main.py` (CLI options and defaults)
- `pigment-agent-skills/reliability-audit/src/data_loader.py` (Expected columns and CSV handling)
- `pigment-agent-skills/reliability-audit/src/report_generator.py` (Output files)
- `pigment-agent-skills/reliability-audit/requirements.txt` (Dependencies)
- `pigment-agent-skills/reliability-audit/config/config.example.yaml` (Config template)
