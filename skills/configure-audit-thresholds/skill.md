---
tags: [reliability, audit, configuration, thresholds]
owners: []
last_reviewed: 2026-02-05
---

# Configure Audit Thresholds

## When to use
- Adjust performance, scoping, or complexity thresholds for a specific workspace.
- Calibrate scoring weights and grade cutoffs.
- Restrict audits to a subset of Applications or date ranges.

## Outcome
- Updated thresholds and filters applied to audit runs.
- Scoring behavior aligned with workspace expectations.

## Prerequisites
- Access to the reliability audit config files.
- Agreement on target thresholds with workspace owners.

## Inputs
- Threshold values for performance, views, computed rows, and dimensions.
- Scoping targets for FullyScoped and NoChange percentages.
- Optional filters for Applications, dates, or excluded metrics.

## Procedure
1. Open `pigment-agent-skills/reliability-audit/config/thresholds.yaml` and adjust watch/warning/critical thresholds. Why: thresholds drive severity classification. Failure modes: YAML syntax errors; diagnose by validating with `python -c "import yaml,sys;yaml.safe_load(open('...'))"`.
2. Adjust scoping and scoring values in `thresholds.yaml`. Why: scoping targets and scoring weights affect the total score. Failure modes: weights not summing to 100; diagnose by adding the four weight values and confirming the total.
3. If needed, copy and edit `config.example.yaml` to `config.yaml` for filters and output settings. Why: filters scope the audit to relevant apps and time ranges. Failure modes: no data after filters; diagnose by checking filter values against actual application IDs in your CSVs.
4. Run a dry audit with the updated config. Why: confirm that thresholds and filters are applied. Failure modes: unexpected score changes or missing findings; diagnose by comparing output to a baseline run.

## Verification
- `thresholds.yaml` loads without YAML errors.
- Audit output reflects updated thresholds (e.g., changes in watch/warning/critical counts).
- If filters are set, outputs include only the intended Applications or dates.

## Edge cases & recovery
- If thresholds are too strict and generate noise, revert to defaults from version control and iterate with smaller changes.
- If filters exclude all data, temporarily clear filters and re-run to validate the pipeline.
- Do not set scoring weights that exceed 100; the score will be skewed.

## References
- `pigment-agent-skills/reliability-audit/config/thresholds.yaml` (Threshold defaults)
- `pigment-agent-skills/reliability-audit/config/config.example.yaml` (Filters and output settings)
- `pigment-agent-skills/reliability-audit/src/config.py` (Threshold and config loading logic)
