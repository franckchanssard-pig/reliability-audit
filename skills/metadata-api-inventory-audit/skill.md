---
tags: [reliability, audit, metadata, api]
owners: []
last_reviewed: 2026-02-05
---

# Metadata API Inventory Audit

## When to use
- Build a structural inventory of a Pigment workspace.
- Check naming conventions, block counts, and dimensional complexity at scale.
- Identify oversized Applications or inconsistent block structures.

## Outcome
- Inventory of Applications and Blocks with counts by type.
- Naming convention violations identified for Metrics and Dimension Lists.
- List of large Applications and high-dimension Metrics.

## Prerequisites
- Metadata API key with Modeler+ access.
- Ability to call Pigment APIs and store JSON results.

## Inputs
- `METADATA_API_KEY`.
- Target workspace environment.
- Naming patterns to enforce (from workspace standards).

## Procedure
1. List all Applications via the Metadata API. Why: the Application list is the primary inventory anchor. Failure modes: empty list or 401; diagnose by verifying the key and endpoint.
   ```bash
   curl -H "Authorization: Bearer ${METADATA_API_KEY}" \
     "https://pigment.app/api/v1/applications"
   ```
2. For each Application, list Blocks and capture `id`, `name`, `type`, and `dimensions`. Why: block metadata powers structural and complexity audits. Failure modes: missing blocks or partial data; diagnose by checking the `applicationId` parameter and pagination if present.
   ```bash
   curl -H "Authorization: Bearer ${METADATA_API_KEY}" \
     "https://pigment.app/api/v1/blocks?applicationId=${APP_ID}"
   ```
3. Build an inventory summary. Why: summary counts show oversized apps and imbalanced block types. Failure modes: incorrect totals; diagnose by comparing total block counts to per-app sums.
4. Check naming convention compliance. Why: inconsistent naming reduces maintainability. Failure modes: false positives from incorrect regex; diagnose by validating patterns against known good block names. Example patterns from internal guidance:
   ```python
   naming_patterns = {
       "Metric": r"^[A-Z][a-z]+(_[A-Z][a-z]+)*$",
       "DimensionList": r"^[A-Z][a-z]+$",
   }
   ```
5. Flag large Applications and high-dimension Metrics. Why: oversized apps and high dimensionality are reliability risks. Failure modes: missing `dimensions`; diagnose by ensuring `dimensions` is populated for Metric blocks.
6. Export a findings report with per-app summaries and violations. Why: downstream remediation depends on a clear list of targets. Failure modes: missing references to block IDs; diagnose by confirming each violation includes `applicationId` and `blockId`.

## Verification
- Inventory includes all Applications and total block counts.
- Naming violations list includes block IDs and expected patterns.
- Large Application list uses a defined threshold (e.g., >200 blocks).

## Edge cases & recovery
- If an Application has zero blocks returned, re-check permissions and whether it is archived.
- If the API omits dimensions for certain block types, restrict dimensional checks to Metrics only.
- Metadata API does not reveal formula content; document manual review needs separately.

## References
- `pigment-agent-skills/reliability-audit/12-programmatic-audit-apis.md` (Metadata API endpoints and examples)
