# SPEC.md — [Workflow ID]: [Workflow Name]

**Version:** 1.0
**Last updated:** [date]
**Status:** [draft / active / deprecated]

---

## What this workflow does

[2-3 sentences in plain English. What does it accomplish? What problem does it solve? A non-technical person should understand the purpose after reading this.]

## Data sources and APIs

| Source | Endpoint(s) | Auth Method | Direction |
|---|---|---|---|
| [e.g., Flourish] | [e.g., GetInventory, GetPackages] | [e.g., x-api-key header] | [Read / Write / Both] |

## Trigger

**Type:** [Schedule / Webhook / Manual trigger / After another workflow]
**Schedule:** [e.g., Every 4 hours / Daily at 6 AM ET / After F1 completes]

## Process

Step-by-step description of what the workflow does:

1. [First step — e.g., "Pull current inventory from Flourish API via GetInventory endpoint"]
2. [Second step — e.g., "Clean: normalize date formats, map Flourish field names to Supabase schema"]
3. [Third step — e.g., "Validate: check required fields, verify referential integrity against items table"]
4. [Fourth step — e.g., "Write: upsert to Supabase inventory_snapshots table with validation_status = 'raw'"]
5. [Fifth step — e.g., "Log heartbeat to workflow_health table"]

## Outputs

| Output | Destination | Format |
|---|---|---|
| [e.g., Inventory records] | [e.g., Supabase inventory_snapshots table] | [e.g., JSON via REST upsert] |
| [e.g., Heartbeat] | [e.g., Supabase workflow_health table] | [e.g., workflow_id + timestamp] |
| [e.g., Failure alert] | [e.g., Slack #operations] | [e.g., Text message with error details] |

## Error handling and retries

**Retries:** [e.g., 3 retries with 5-minute backoff]
**On final failure:** [e.g., Log S2 exception to exception table, post alert to Slack, increment data_source_health.consecutive_failures]

## Ownership

| Field | Value |
|---|---|
| **Owner** | [Who is responsible when this breaks — e.g., Alex] |
| **Alert recipient** | [Who gets the SMS — e.g., Alex's phone] |
| **Safe-mode behavior** | [What happens if this workflow is down — choose one:] |

Safe-mode options:
- "Switch to manual — check Flourish directly until restored" (for critical workflows)
- "Degrade gracefully — data up to [X] hours stale is acceptable" (for advisory workflows)
- "Operations stop — fix immediately" (for blocking workflows)

## Severity

**Classification:** [Critical / Advisory]

- **Critical:** Compliance data goes stale or operations are impaired. Fix within hours.
- **Advisory:** Useful but not blocking. Can tolerate 24-48 hours of downtime.

## AI involvement

**Uses Claude API:** [Yes / No]
**If yes:**
- Model version pinned to: [e.g., claude-sonnet-4-20250514]
- Canary prompt implemented: [Yes / No]
- All inputs/outputs logged to llm_audit_log: [Yes / No]

## Agent-native migration note

[What model capability would make this workflow unnecessary? When the model can do X natively, this SPEC.md becomes the prompt and the n8n workflow is deprecated.]

Example: "This workflow exists because Claude cannot currently make authenticated API calls to Flourish on a schedule. If/when Claude can autonomously call APIs on a timer with retry logic, this workflow collapses to a prompt + tool-use connection."

---

## Changelog

| Date | Change | By |
|---|---|---|
| [date] | Initial creation | [name] |
