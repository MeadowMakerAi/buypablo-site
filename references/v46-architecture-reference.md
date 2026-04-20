# V4.6 Canonical Architecture — Quick Reference

## Stack Components

| Component | Role | Status |
|---|---|---|
| Flourish | Ops platform, METRC bridge. Source of truth for inventory, batches, packages, work orders | Live (CCC uses it). API access UNCONFIRMED |
| METRC | State compliance system. Access via Flourish only — never direct | Active. Vendor key UNCONFIRMED |
| Apex Trading | Wholesale CRM. Dave manages deals here | Active |
| Supabase/Postgres | Entity backbone. 33 tables, RLS, canonical views | Live (Pro, $25/mo) |
| n8n | Workflow orchestration. Self-hosted on VPS | Starts May 1 |
| Claude Team | Team interface via MCP. Read-only Supabase access | $25/seat/mo. Seats deferred to mid-April |
| Claude Code | Operator console. Alex's primary dev interface | Installed on M1. Mac Mini arriving April 14 |
| Pistil Data | Market intelligence scraping (pricing, distribution, brand performance) | Phase 2. Recon script ready |

## Core Patterns

### Write-Assist (Template-and-Confirm)
1. Human tells Claude what happened (natural language)
2. Claude generates Flourish API payload
3. Human reviews and confirms
4. n8n submits to Flourish
5. Flourish syncs to METRC

This is NOT fully autonomous. Human confirms every write.

### Trust Graduation Schedule
- Month 1 (May): Read & monitor only
- Month 2 (June-July): Write-assist with confirmation
- Month 3 (August): Financial intelligence, expanded autonomy on proven workflows

### Data Flow
```
Flourish → (API) → n8n → Supabase (raw → validated → canonical)
Pistil → (Playwright scrape) → Claude Code → Supabase (price_observations)
OCM/METRC → (manual/API) → Supabase (compliance tables)
Supabase → (MCP read-only) → Claude Team (team queries)
Supabase → (views) → n8n → Slack (alerts only)
```

### Validation Staging
All external data flows through three stages:
1. `raw` — as received from source
2. `validated` — schema-conformant, deduped, type-checked
3. `canonical` — matched to internal entities, ready for queries

### Key Design Decisions
- Slack = alerts-only push channel from n8n. NOT a bot interface
- Claude Team = team's read interface to Supabase
- pgvector deferred to month 3+
- Provenance columns on all tables (source, ingested_at, validated_at)
- On-demand sync with retry policies
- SPEC.md per workflow (Inputs/Process/Outputs contracts)

## Security & IP
- API keys in env vars ONLY — never in knowledge files, CLAUDE.md, or committed code
- Governance/IP segmentation layer must precede other additions (protect Alex's IP from Phil and other stakeholders)
- Management agreement IP language: infra/automation/intelligence/code = management entity
- CCC retains raw operational data on termination

## Deferred Additions (Need Feasibility Session Before Integrating)
- Master dashboard
- Ops facility dashboard
- Refined team copilot
- Governance/IP segmentation layer (PRIORITY — must precede other additions)
- Process mapping
