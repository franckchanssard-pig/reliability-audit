---
tags: [reliability, performance, scoping, optimization]
owners: []
last_reviewed: 2026-02-05
---

# Scoping Optimization Audit

## When to use
- Identify Metrics that are not scoped and causing excessive compute.
- Quantify potential performance savings from scoped calculations.
- Prepare a remediation list for model optimization.

## Outcome
- Scoping distribution (% FullyScoped, PartiallyScoped, NoChange).
- Ranked list of NoChange Metrics with high execution time.
- Estimated compute savings from scoping improvements.

## Prerequisites
- Executions CSV export with `jobType`, `scoped_level`, and `execution_time`.
- Thresholds from `pigment-agent-skills/reliability-audit/config/thresholds.yaml`.

## Inputs
- Executions CSV path.
- Optional application filters.

## Procedure
1. Filter the executions data to `jobType = "Formula"`. Why: scoping applies to formula recalculations only. Failure modes: mixed job types inflating counts; diagnose by reviewing `jobType` value distribution.
2. Compute the distribution of `scoped_level` values. Why: this yields FullyScoped, PartiallyScoped, and NoChange percentages. Failure modes: missing `scoped_level` column; diagnose by inspecting the CSV header.
3. Identify NoChange metrics with average execution time > 3,000 ms. Why: these are the highest ROI scoping candidates. Failure modes: false positives from sparse metrics; diagnose by checking execution counts and total execution time.
4. Estimate potential savings using the NoChange total execution time. Why: the baseline analyzer assumes ~50% savings if scoping is applied. Failure modes: overstated savings; diagnose by validating with a before/after sample on a few metrics.
5. Produce a remediation list with metric IDs, names, application, and average execution time. Why: actionability requires precise targets. Failure modes: missing IDs; diagnose by ensuring `metric_id` and `metric_name` are present in the executions export.

## Verification
- Scoping percentages sum to ~100% for applicable executions.
- Output list includes top NoChange metrics sorted by total execution time.
- Estimated potential savings is non-zero when NoChange metrics exist.

## Edge cases & recovery
- If `jobType` or `scoped_level` is absent, re-export the executions CSV with those fields.
- If scoping improvements are risky, start with a pilot on the top 3 candidates and measure before/after.
- Do not treat imports or non-formula jobs as scoping candidates; exclude `jobType != "Formula"`.

## References
- `pigment-agent-skills/reliability-audit/src/analyzers/scoping_analyzer.py` (Scoping logic and thresholds)
- `pigment-agent-skills/reliability-audit/13-performance-data-analysis.md` (Scoping audit patterns)
