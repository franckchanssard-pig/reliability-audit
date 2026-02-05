---
tags: [reliability, performance, complexity, modeling]
owners: []
last_reviewed: 2026-02-05
---

# Dimensional Complexity Audit

## When to use
- Identify over-dimensioned Metrics that impact performance.
- Quantify average dimensionality and correlation to execution time.
- Support model refactoring decisions.

## Outcome
- Distribution of Metrics by `nb_dims`.
- List of high-dimension Metrics with severity levels.
- Correlation metrics between dimensions and execution time.

## Prerequisites
- Executions CSV export with `nb_dims`, `metric_id`, `metric_name`, and `execution_time`.
- Thresholds from `pigment-agent-skills/reliability-audit/config/thresholds.yaml`.

## Inputs
- Executions CSV path.
- Optional application filters.

## Procedure
1. Load executions and filter rows with valid `nb_dims` values. Why: missing or zero dimensions invalidate complexity analysis. Failure modes: all `nb_dims` null; diagnose by checking CSV headers and export settings.
2. Aggregate to unique metrics with their `nb_dims`, average execution time, and computed rows. Why: dimensionality is a per-metric property. Failure modes: multiple dimension counts per metric; diagnose by checking for inconsistent `nb_dims` values across executions.
3. Apply thresholds to classify severity. Why: severity levels drive prioritization. Failure modes: thresholds not aligned to workspace norms; diagnose by comparing with `thresholds.yaml` defaults (watch >5, warning >6, critical >10).
4. Calculate correlation between `nb_dims` and `execution_time`. Why: correlation quantifies impact and supports decisions. Failure modes: too few data points; diagnose by confirming at least ~5 metrics with valid execution times.
5. Produce a remediation list with highest-dimension Metrics and their average execution time. Why: actionable list accelerates model refactoring. Failure modes: missing `metric_id`; diagnose by verifying the executions export includes it.

## Verification
- Distribution of dimensions is populated and totals match the number of unique Metrics.
- Severity counts align with thresholds.
- Correlation values are reported when enough data exists.

## Edge cases & recovery
- If dimension counts are inflated by redundant dimensions, verify whether properties can replace dimensions.
- If only a few metrics have `nb_dims`, broaden the time window or re-export data.
- Do not apply dimension thresholds to non-metric blocks.

## References
- `pigment-agent-skills/reliability-audit/src/analyzers/complexity_analyzer.py` (Complexity logic)
- `pigment-agent-skills/reliability-audit/13-performance-data-analysis.md` (Dimension impact analysis)
