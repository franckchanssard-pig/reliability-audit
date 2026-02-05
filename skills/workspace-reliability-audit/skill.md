---
tags: [reliability, audit, workspace, governance]
owners: []
last_reviewed: 2026-02-05
---

# Workspace Reliability Audit

## When to use
- Run a scheduled weekly/monthly/quarterly workspace reliability review.
- Prepare an executive summary and remediation plan for Pigment workspace health.
- Investigate recurring performance, data integrity, or security issues in a workspace.

## Outcome
- Completed audit checklist across structure, data integrity, performance, maintainability, security, and reliability.
- Prioritized remediation matrix with severity and timelines.
- Executive summary draft with findings and recommended actions.

## Prerequisites
- Pigment workspace access with visibility into Applications, Blocks, Metrics, and Views.
- Ability to review Access Rights Metrics and Role configuration (Security Admin when needed).
- Agreement on audit scope (apps, period, criticality).

## Inputs
- Workspace name and audit period (weekly/monthly/quarterly).
- List of Applications in scope (or confirmation that all are included).
- Current naming conventions and documentation standards used by the workspace.
- Any known high-risk areas or recent incidents.

## Procedure
1. Define the audit scope and frequency (Quick Health Check, Standard Audit, or Comprehensive Audit). Why: scope determines depth and avoids partial, inconsistent reviews. Failure modes: scope drift or missing critical apps; diagnose by comparing the audit list to the full Applications list in the workspace.
2. Perform a Structure Audit across Applications and Libraries. Why: architecture issues create long-term reliability and performance debt. Failure modes: “mega-Applications,” duplicate Dimension Lists, missing Libraries; diagnose by counting blocks per app and confirming shared Dimensions are centralized.
3. Perform a Data Integrity Audit on Dimension Lists, references, and completeness. Why: inaccurate or incomplete Dimensions cascade into incorrect Metrics. Failure modes: duplicate IDs, orphaned items, missing periods; diagnose with Pigment formulas like `ISBLANK(Item.Parent_Property)` and completeness checks such as `COUNT(Revenue FILTER NOT(ISBLANK(Revenue))) / COUNT(Revenue) * 100`.
4. Perform a Performance Audit on slow Metrics and Views. Why: execution and render time directly impact user trust and usability. Failure modes: metrics > 5s, views > 3s, excessive dimensions; diagnose using execution exports and thresholds in `pigment-agent-skills/reliability-audit/config/thresholds.yaml`.
5. Perform a Maintainability Audit (naming, readability, documentation). Why: maintainability prevents fragile models and knowledge loss. Failure modes: inconsistent naming, generic block names, undocumented logic; diagnose by scanning for conventions like `Revenue_Actuals_By_Product` and missing block descriptions.
6. Perform a Security and Reliability Audit (roles, access rights, error handling). Why: access issues are high-risk and can invalidate audit outcomes. Failure modes: over-permissioned roles, missing Access Rights Metrics, formulas without division-by-zero checks; diagnose by reviewing Roles and checking formulas for patterns like `IF(Denominator = 0, 0, Numerator / Denominator)`.
7. Compile the audit report and remediation matrix. Why: actionable output drives follow-up. Failure modes: unclear priorities or missing owners; diagnose by ensuring each finding has severity, impact, and a recommended timeline.

## Verification
- Audit checklist completed for all six dimensions.
- Executive summary includes at least 3 key findings and 3 prioritized actions.
- Remediation matrix maps each finding to a severity and target timeline.

## Edge cases & recovery
- If you lack Security Admin rights, document missing checks and request a Security Admin review before finalizing the report.
- If the workspace is too large for full review, sample by the top 3 applications by compute load and note the sampling method.
- If performance data exports are unavailable, run a manual review and flag the audit as partial.

## References
- `pigment-agent-skills/reliability-audit/11-workspace-reliability-audit.md` (Pigment Workspace Reliability Audit)
- `pigment-agent-skills/reliability-audit/README.md` (Audit workflow overview and thresholds)
- `pigment-agent-skills/reliability-audit/config/thresholds.yaml` (Performance and scoping thresholds)
