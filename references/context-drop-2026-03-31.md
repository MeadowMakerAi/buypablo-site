# Context Drop — March 31, 2026

## What This Is
Operational context snapshot from Claude.ai conversations. Drop this into your Claude Code project's `references/` directory to keep Claude Code oriented on current priorities and decisions.

---

## Active Priority Stack (ordered)

1. **PABLO vape launch** — the key to making money. 4/20 target shelf date.
2. **buypablo.com** — ~75% done. BLOCKER: domain printed on all packaging. Must be live before product ships.
3. **MIT homework** — Applied Agentic AI module. Overdue, trying to finish today (3/31).
4. **Miguel call** — tonight (3/31). Montgomery, NY cultivator. Potential strategic partnership.
5. **PABLO Gummies scoping** — secondary to vape launch but high-leverage portfolio expansion.

---

## Key Decisions Made This Session

### PABLO Launch: Reduced Initial SKU Drop
- **Was:** 14 distillate SKUs (7 flavors × 2 formats)
- **Now:** 6 SKUs (3 AIO flavors + 3 cart/510 flavors)
- **Why:** Testing costs ~$600/flavor. At 600-unit batches = ~$1/unit testing vs ~$2.50 at 240-unit batches. Smaller initial SKU set reduces total upfront spend.
- **Marketing play:** Staggered flavor drops (weekly/biweekly) create content cadence. "Sunday Grape dropping this week." Turns a constraint into a launch narrative.
- **Still open:** Which 3 flavors for AIO, which 3 for carts. Decision scheduled for April 2.
- **LR SKUs (9 total):** Unchanged.

### PABLO Gummies — New Initiative
- **Product:** 25mg potency gummy, 4ml mold, scores into 4 segments (~6.25mg each)
- **Flavor strategy:** Line-extend existing 7 PABLO flavors
- **Flavor sourcing:** Check Melt to Make (melttomake.com) and Altamaker for ready-to-use flavors
- **COGS baseline:** Ask Max for Phil's Nice Gummies COGS breakdown, adjust for PABLO inputs
- **Investments:** Molds, gummy base (Melt to Make), print assets/packaging
- **Why gummies > prerolls right now:** Max is sole mfg employee, no scale preroll experience, bandwidth constrained. Gummies are operationally closer.
- **Risk:** Rushing flavors to market before they're good. Mitigated by potency/price positioning (not artisan flavor play).
- **Priority:** Secondary to vape launch. Don't let this derail.

---

## Infrastructure State (unchanged from prior drops)

- **Supabase:** Live, Pro tier, 33 tables, 7 migrations deployed, 30 dispensary records
- **Claude Code:** Working on M1 (PATH resolved v2.1.86). VS Code extension next.
- **Mac Mini (M4 Pro, 48GB):** Arriving ~April 14
- **n8n:** Self-hosted on VPS, starts May 1
- **498 dispensary records:** Still not loaded — needs Claude Code + XLSX
- **Schema merge:** Migrations 008-011 (commercial intelligence layer) not deployed
- **Flourish API access:** Unconfirmed
- **METRC vendor key:** Unconfirmed

---

## Open Blockers

| # | Blocker | Status |
|---|---------|--------|
| 1 | buypablo.com dead | ~75% done, pushing to finish |
| 2 | 498 dispensary records not loaded | Needs Claude Code + XLSX |
| 3 | Schema merge (migrations 008-011) | Not deployed |
| 4 | Flourish API access | Unconfirmed |
| 5 | METRC vendor key | Unconfirmed |
| 6 | Work tracker fragmented | Two disconnected files, need Google Sheet consolidation |
| 7 | CCC management agreement | Agreed but NOT signed — must get ink before Europe (mid-late May) |
| 8 | GS1 renewal (MMW) | Due TODAY 3/31 — may be overdue |

---

## Action Items (this week)

- [ ] Message Max — Phil's Nice Gummies COGS (April 1)
- [ ] Browse Melt to Make — gummy base + flavor options (April 1)
- [ ] buypablo.com push-to-launch sprint (April 1)
- [ ] Lock initial PABLO drop flavors — 3 AIO + 3 cart (April 2)
- [ ] MIT homework fallback block (April 3 if not done today)
- [ ] GS1 renewal — check if handled (TODAY)
- [ ] Miguel call debrief → update Claude context (after tonight's call)

---

## Claude Code <> Claude.ai Context Sync (Open Question)

Alex wants to establish a pattern for keeping Claude Code's project context current with decisions and context that emerge in Claude.ai conversations. Current approach: manual context drops like this file into `references/`. Needs a more systematic solution — potentially:
- Standardized context drop format (this file is a prototype)
- CLAUDE.md section that references `references/` for latest context
- Trigger phrase in Claude.ai ("generate context drop") that produces an updated file
- Eventually: automated via n8n webhook or Supabase row that both interfaces can read

This is an open design question, not a blocker.
