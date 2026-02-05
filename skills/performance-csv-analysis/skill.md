---
tags: [reliability, performance, data, audit]
owners: []
last_reviewed: 2026-02-05
---

# Performance CSV Analysis

## When to use
- Analyze execution and view performance using Pigment CSV exports.
- Identify slow Metrics, slow Views, and heavy Applications.
- Quantify scoping effectiveness and dimensional complexity.

## Outcome
- Ranked lists of slow Metrics and slow Views with thresholds applied.
- Scoping distribution and optimization candidates.
- Application workload distribution and peak usage windows.

## Prerequisites
- Access to Pigment performance exports (Executions, Views, ARMSET/UPMSET).
- Python environment with `pandas` installed.
- Agreement on thresholds (watch/warning/critical).

## Inputs
- Paths to the performance CSV files.
- Threshold values from `pigment-agent-skills/reliability-audit/config/thresholds.yaml`.
- Optional filters for Applications or time ranges.

## Procedure
1. Collect the CSV exports and confirm headers match expected columns. Why: analysis depends on specific column names. Failure modes: missing columns like `execution_time` or `metric_id`; diagnose by inspecting the header row. The sample exports in this repo are:
   ```text
   pigment-agent-skills/reliability-audit/sample-data/1. Executions.csv
   pigment-agent-skills/reliability-audit/sample-data/6. Views Executions.csv
   pigment-agent-skills/reliability-audit/sample-data/2. Armset and Upmset Executions.csv
   ```
2. Load the CSVs into pandas and coerce numeric columns. Why: string-typed numbers break aggregation. Failure modes: NaNs from parsing errors; diagnose by checking `df.dtypes` after load.
3. Identify slow Metrics using execution time thresholds. Why: metrics over 5s (warning) or 30s (critical) are reliability risks. Failure modes: outliers due to missing scoping or large computed rows; diagnose by inspecting `scoped_level` and `computed_rows`.
4. Identify slow Views using view render thresholds. Why: view render time drives user experience. Failure modes: view names missing; diagnose by checking `blockId` and `blockName` columns in the views export.
5. Analyze scoping effectiveness. Why: `NoChange` scoped calculations are optimization candidates. Failure modes: `jobType` not filtered to `Formula`; diagnose by checking the `jobType` distribution.
6. Analyze dimensional complexity and workload distribution. Why: high `nb_dims` and heavy apps point to systemic performance risks. Failure modes: `nb_dims` missing; diagnose by verifying the executions export includes `nb_dims`.

## Verification
- Slow metrics list includes `metric_id`, `metric_name`, `execution_time`, and `nb_dims`.
- Slow views list includes `blockId`, `blockName`, and `execution_time`.
- Scoping distribution percentages sum to ~100% for applicable executions.

## Edge cases & recovery
- If exports use different file names, pass explicit paths in the CLI or map headers before analysis.
- If execution timestamps are missing, skip temporal analysis and note the limitation in the report.
- If datasets are large, filter by application or date to keep analysis time manageable.

## References
- `pigment-agent-skills/reliability-audit/13-performance-data-analysis.md` (Analysis patterns and thresholds)
- `pigment-agent-skills/reliability-audit/config/thresholds.yaml` (Threshold values)
