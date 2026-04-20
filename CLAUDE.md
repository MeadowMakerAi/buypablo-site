# CLAUDE.md

## What We're Building

Two consumer cannabis brands — **PABLO** (vapes, launching 4/20/2026) and **Meadow Maker** (mass-market, in development) — operated through a management entity with partner Ethan. The brands are manufactured at CCC/Saratoga, a licensed processor where Alex and Ethan operate under a management agreement (verbally agreed, NOT signed — must be signed before Alex departs for Europe mid-to-late May 2026).

The management entity's relationship to CCC is deliberately arms-length. Alex and Ethan may participate in CCC's corporate structure, or may keep PABLO as a white-label customer to avoid exposure to Phil's cost structure, debts, and liabilities. This is TBD and a live strategic question — do not assume integration.

An automation and intelligence layer (V4.6) connects Flourish, Supabase, n8n, and Claude Code into an operational backbone.

## Reference Files (Load When Relevant)

Do not load these unless the current task requires them.

- `references/team-and-people.md` — Team, vendors, key contacts, Phil situation, Miguel partnership
- `references/supabase-schema-reference.md` — All tables, migrations, schema merge plan
- `references/v46-architecture-reference.md` — Stack components, data flow, write-assist pattern, trust graduation
- `references/pablo-launch-tracker.md` — SKU matrix, critical path, countdown to 4/20
- `references/pablo-brand-system.md` — Colors, typography, accent bands, packaging specs, pricing, competitive landscape
- `references/meadow-maker-brief.md` — Design system, positioning, blockers, SSOT status
- `references/claude-team-knowledge-files.md` — Knowledge files for Max, Erik, Dave, Alex Claude Team projects
- `references/spec-template.md` — SPEC.md template for n8n workflow contracts
- `references/gemini-diagram-prompt.md` — Prompt to regenerate the V4.6 architecture diagram
- `references/historical-context.md` — PABLO hemp origins, entity evolution, CCC timeline, sourcing strategy, early team
- `references/context-drop-2026-03-31.md` — Priority stack, SKU reduction (14→6 distillate), gummies scoping, blockers, action items

## Active Blockers (Surface Until Resolved)

1. **buypablo.com dead** — Printed on all packaging. Domain + info@ email must be live before press
2. **CCC management agreement unsigned** — Must get ink before Europe (mid-to-late May)
3. **498 dispensary records not loaded** — Needs XLSX processing into Supabase
4. **Flourish API access unconfirmed**
5. **METRC vendor key unconfirmed**
6. **Work tracker fragmented** — Two disconnected local files, neither in Google Drive. Must consolidate into one Google Sheet with fixed URL

## Security

Governance/IP segmentation must precede other infra additions — protect Alex's IP from Phil and other stakeholders.

## Creative Asset Pipeline

Four CLI tools in `tools/`, sharing constants from `tools/brand_config.py`:

1. `generate_gemini_prompts.py` — 9 image-gen prompts for product photography. Feed output to Gemini with packaging dieline as reference.
2. `generate_flavor_badges.py` — Pillow-rendered flavor badge strips (horizontal, grid, vertical).
3. `generate_stickers.py` — NY OCM §128.5 compliance stickers at 300 DPI. Supports all product types.
4. `post_process_asset.py` — Crop/shadow/resize raw Gemini output for web. Presets: `--hero`, `--card`, `--badge`, `--family`.

Workflow: prompts (1) → Gemini (manual) → post-process (4). Badges (2) and stickers (3) are independent.
All output lands in `output/{prompts,badges,stickers,processed}`.

## Design System
Always read DESIGN.md before making any visual or UI decisions.
All font choices, colors, spacing, animation curves, and border radius are defined there.
Do not deviate without explicit user approval.
In QA mode, flag any code that doesn't match DESIGN.md.
Key rules: Bebas Neue is the default font (not Space Grotesk). Buttons are square (0px radius). The signature easing is cubic-bezier(0.16, 1, 0.3, 1).

## Session Start

1. Read this file
2. Ask what we're working on, or run ops-sync
3. Load only the reference files relevant to today's task
4. If touching brand assets → `brand_config.py` is the single source of truth for colors, flavors, compliance text
5. If touching Supabase → check supabase-bridge SKILL.md
6. If touching UI/styles → read DESIGN.md first
