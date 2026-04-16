# Gemini Architecture Diagram Prompt — V4.5 Final

> Used to generate the Automation Framework V4.6 diagram PDF via Gemini. Keep for re-generation.

Copy everything below this line and paste into Gemini.

————————————————————————————————————————

Create a clean, professional technical systems architecture diagram on a near-black background (#1A1A1E). Sparingly annotated — only label what's essential. Every word earns its place.

LAYOUT: Layered hub-and-spoke. Three vertical zones: LEFT = data sources and operational systems, CENTER = orchestration and data layer, RIGHT = team surfaces and outbound channels. A horizontal band across the TOP shows intelligence and compliance logic.

CENTER HUB:
Large node: "n8n" with sub-label "VPS · Self-Hosted · Always-On". All data flows pass through this node. It is the center of the diagram. Make it visually prominent.

BELOW CENTER — DATA BACKBONE:
Large node: "Supabase (Postgres)" with sub-label "Entity Backbone · Pro Tier · View-Only Team Access".
Inside Supabase, show four colored horizontal tiers stacked vertically:
  Top tier (sage green #5B8A72 tint): "Operations" — Batches, Packages, COAs, BOMs, Inventory
  Second tier (blue #7BA7C9 tint): "Market Intelligence" — Accounts, Contacts, Deals, Licenses
  Third tier (amber #C4956A tint): "Consumer" — Opt-Ins, Consent, Segments
  Bottom tier (gray #888780 tint): "System" — ai_feedback, workflow_health, llm_audit_log

LEFT SIDE — DATA SOURCES (stacked vertically):
"Flourish" with sub-label "Inventory · BOMs · COAs · Manufacturing · METRC Bridge" — arrow right to n8n labeled "API Sync + Webhooks" (sage green arrow). This is the PRIMARY data source — make it visually the largest left-side node.
"METRC" with sub-label "Tags · Manifests · Compliance Ledger" — arrow INTO Flourish ONLY, labeled "Native Sync" (sage green dashed arrow). CRITICAL: There is NO arrow from METRC to n8n. METRC connects ONLY to Flourish. Flourish is the sole bridge.
"OCM Socrata" with sub-label "Dispensary Licenses" — arrow right to n8n labeled "Weekly Pull" (blue arrow)
"Apex Trading" with sub-label "Orders · CRM · Storefronts" — bidirectional arrow to n8n labeled "Webhook / Poll" (blue arrow)
"Pistil Data" with sub-label "Retail Sales · Brand Share · SKU Velocity" — arrow right to n8n labeled "Market Data Pull" (blue arrow)
Small node: "Clay" with sub-label "Enrichment" — arrow from n8n labeled "Enrichment Requests" (blue arrow)

TOP CENTER — INTELLIGENCE LAYER (dashed box spanning top):
Dashed rounded rectangle labeled "Compliance Automation"
Single row inside: "Manifest Validation · Drift Detection · COA Verification · BOM Pre-Flight"
Arrow from this box down into n8n.
"Claude API" node with sub-label "Reasoning Layer" — bidirectional arrow to n8n labeled "Judgment · Classification · NLP"
DASHED arrow from Claude API into the Compliance box labeled "Powers"
Small annotation near Claude API: "Model-pinned · Canary-monitored · Audit-logged"
These dashed arrows must be visually distinct from solid data-flow arrows — lighter weight or different opacity.

RIGHT SIDE UPPER — TEAM SURFACES:
"Claude Team" with sub-label "Natural Language Ops · 5 Seats" — arrow to Supabase labeled "Canonical Views Only (read-only)"
Three labels beneath: "Ask · Check · Reason"
Small annotation beneath: "Web · Desktop · Mobile"
"Claude Code" with sub-label "Operator Console · Mac Mini" — bidirectional arrow to Supabase labeled "Full Access (admin)"
Small annotation near Claude Code: "CLAUDE.md · ICM-structured context"
DASHED arrow from Claude API to Claude Team labeled "Powers" (same style as Compliance dashed arrow)
"Slack" small node with sub-label "Alerts Only" — arrow FROM n8n labeled "Push Notifications + SMS"
Small annotation near Slack: "No bot — alert channel only"

BOTTOM LEFT — EXTERNAL HEALTH MONITOR:
Small node with warning styling: "Health Monitor" with sub-label "pg_cron + SMS"
Bidirectional arrow to Supabase (specifically the System tier / workflow_health) labeled "Heartbeat Check"
Dashed arrow to Slack labeled "Alert on Silent Failure"
Small annotation: "Catches n8n silent stops"

RIGHT SIDE MIDDLE — OUTBOUND:
"Instantly" with sub-label "Cold Outbound" — arrow from n8n
"Gmail" — arrow from n8n labeled "Procurement"

BOTTOM RIGHT — CONSUMER FUNNELS:
Dashed rectangle with amber tint. Two nodes inside: "PABLO" "Meadow Maker"
Each with tiny sub-label: "QR · Landing · Opt-In"
Arrow into n8n labeled "Consumer Data"
Small annotation: "Phase 3 — Not Active Yet"

BOTTOM ANNOTATION in small italic text spanning full width:
"V4.5 Final — Flourish is the sole METRC bridge. n8n self-hosted on VPS orchestrates all data flows. Claude reasons and powers compliance logic. Team accesses canonical views only via REST. Supabase connects four data tiers: operations, market intelligence, consumer, and system audit. Humans approve all writes to regulated systems. External health monitor catches silent workflow failures."

TRUST GRADUATION — small box in bottom-right corner:
Small rounded rectangle with subtle border:
"Trust Schedule"
"Tier 1 (now): Human approves all"
"Tier 2 (month 6): Auto-promote routine"
"Tier 3 (month 12): Exception-based"

ACCESS CONTROL — small box near Supabase, bottom-left of the backbone:
Small rounded rectangle:
"Access Roles"
"team_read — views only"
"n8n_service — base tables"
"alex_admin — full + break-glass"

STYLE:
Near-black background (#1A1A1E)
Muted sage green (#5B8A72) for operational arrows and Operations tier
Muted blue (#7BA7C9) for market intelligence arrows and Market tier
Warm amber (#C4956A) for consumer arrows, funnels, and Consumer tier
Gray (#888780) for System/audit tier, health monitor, and access control box
White monospaced font for system names
Light gray (#999) sans-serif for sub-labels and annotations
Thin rounded rectangles with subtle borders
Dashed borders on: Compliance box, Consumer Funnels, METRC→Flourish native sync arrow
No gradients, no shadows, no 3D, no icons, no decorative elements
All text fully legible — cut labels before shrinking them
Four-tier color coding must be visually consistent throughout

IF GEMINI CHOKES ON DENSITY, strip in this order:
1. Gmail node (fold into Slack or remove)
2. Consumer Funnels box (just keep annotation "Phase 3")
3. Clay node (fold into OCM flow annotation)
4. Pistil Data node (fold into Market Intelligence tier annotation)
5. Access Roles box (fold into Supabase sub-label)
6. Trust Schedule box (move to bottom annotation text)
Core structure that MUST survive: Flourish→n8n→Supabase, METRC→Flourish only (NO METRC→n8n), Claude Team→Supabase via "Canonical Views Only", Health Monitor→Supabase, four-tier backbone, and Claude API powering compliance automation.
