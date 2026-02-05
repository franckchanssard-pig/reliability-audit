---
tags: [reliability, audit, security, api]
owners: []
last_reviewed: 2026-02-05
---

# Audit Logs API Monitoring

## When to use
- Build continuous monitoring of Pigment workspace activity for reliability or compliance.
- Investigate security changes, role updates, or unusual access patterns.
- Feed audit events into SIEM or internal dashboards.

## Outcome
- Audit Logs API ingestion running for the target period with pagination handled.
- Parsed event set categorized into activity, security, and change volume signals.
- Monitoring summary with actionable anomalies and thresholds.

## Prerequisites
- Security Admin access to generate an Audit Logs API key.
- Ability to call Pigment APIs from your environment.
- Decision on storage target for events (SIEM, database, or files).

## Inputs
- `AUDIT_LOG_API_KEY` with read access.
- `ingestedSince` timestamp (ISO-8601) for the starting window.
- Optional filters: event types or applications of interest.

## Procedure
1. Obtain an Audit Logs API key with Security Admin permissions. Why: the Audit Logs API requires elevated access. Failure modes: 401/403 errors; diagnose by confirming the key and role.
2. Pull events from the Audit Logs API with pagination. Why: the API returns up to 1,000 events per request and requires paging. Failure modes: missing events or early termination; diagnose by checking for `pagination.nextCursor` and looping until it is empty. Use:
   ```bash
   curl -H "Authorization: Bearer ${AUDIT_LOG_API_KEY}" \
     "https://pigment.app/api/audit/v1/events?ingestedSince=2024-01-01T00:00:00Z"
   ```
3. Respect API constraints and rate limits. Why: the API enforces a 180-day lookback and 500 requests per 5 minutes. Failure modes: 400s for invalid date ranges or 429s for rate limits; diagnose by inspecting response codes and reducing request volume.
4. Categorize events into monitoring buckets. Why: event categories drive actionable monitoring signals. Failure modes: incomplete categorization; diagnose by comparing against expected event types such as `UserLoggedIn`, `RoleChanged`, `BlockModified`, and `AccessRightsChanged`.
5. Run reliability checks on activity and change volume. Why: spikes or unusual access patterns indicate reliability or security risk. Failure modes: false positives due to baseline mismatch; diagnose by comparing recent counts to a rolling 30-day baseline.
6. Emit alerts or a summary report. Why: monitoring is only useful if it surfaces actionable changes. Failure modes: noisy alerts; diagnose by validating thresholds against historical activity.

## Verification
- Event ingestion returns records for the target period and includes expected categories.
- Pagination completes without missing cursors.
- Monitoring report includes counts for logins, role changes, block changes, and API key events.

## Edge cases & recovery
- If you need >180 days of history, run incremental backfills in 180-day windows and store results.
- If rate-limited, throttle requests and back off; do not retry in a tight loop.
- Audit Logs do not include data values or formula content; document manual review steps when needed.

## References
- `pigment-agent-skills/reliability-audit/12-programmatic-audit-apis.md` (Audit Logs API usage and constraints)
