# Supabase Schema Reference

> Current state as of March 23, 2026. Project: kmqwjjiogdfqnfwtivvv

## Deployed Tables (33 total, 7 migrations)

### Core Entity Tables (Migration 001)
- `account` — Dispensary accounts (license_number, name, city, apex_id, enrichment_status)
- `contact` — People at dispensaries (account_id FK, email, phone, source)
- `deal` — Sales pipeline tracking (account_id FK, stage enum, apex_deal_id, value)
- `batch` — Flourish inventory batches (flourish_batch_id unique, metrc_tag, quantity, status)
- `metrc_package` — METRC package records (metrc_tag unique, quantity, lab_results_linked)
- `coa` — Certificates of Analysis (batch_id FK, lab_name, thc_pct, passed, file_url)
- `event` — Audit trail for every system action (entity_type, entity_id, event_type, payload JSONB)
- `workflow_run` — n8n workflow execution log (workflow_name, status, error_message, correlation_id)
- `exception` — Failures requiring human attention
- `ai_feedback` — AI audit logging

### Flourish Sync Tables (Migrations 002-004)
- `items` — Product catalog from Flourish
- `inventory` — Current inventory state
- `packages` — Package records
- `work_orders` — Manufacturing work orders
- `shipments` — Transfer/shipment records
- `lab_results` — Lab testing results

### Compliance & Financial (Migrations 003-005)
- Financial tracking tables
- Compliance monitoring tables
- Canonical views (12 total)

### Dispensary Intelligence (Migration 007)
- `dispensary_intelligence` — 60-column targeting database. 30 rows loaded (A+/A/B+ targets). 498 remaining records need loading via XLSX.

## NOT YET Deployed (Migrations 008-011 — Commercial Intelligence Layer)
- `stores` — Dispensary store records from Pistil
- `brands` — Brand entities from Pistil
- `price_observations` — Time-series pricing data (designed for 76K+ rows from Pistil)
- `brand_performance` — Aggregated brand metrics
- `store_brand_matrix` — Store × brand cross-reference
- `sales_signals` — Derived signals from pricing/availability patterns
- 8 intelligence views
- Python loader with fuzzy name matching

## Schema Merge Plan
Deploy 008-011 AFTER:
1. Full 528 dispensary records loaded via Claude Code
2. Schema alignment checked against Pistil recon output
3. No table name conflicts with deployed schema

## RLS
Enabled on all tables. V4.7 addition: "CCC reporting" role — read-only views, revocable in one SQL statement.

## Connection
- MCP: `https://mcp.supabase.com/mcp?project_ref=kmqwjjiogdfqnfwtivvv&read_only=true`
- Direct Postgres connection string: stored in env var, not in any file
