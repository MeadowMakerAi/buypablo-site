# Asset Pipeline Workflow — Claude AI → Gemini → CLI Post-Processing

## Overview

Proven workflow for generating web-quality product renders from packaging print files. Tested March 2026 on PABLO Pre-Roll 2ct Mylar Bag. Produces serviceable web/social assets, not print-quality files.

## Pipeline Steps

### Step 1: Claude AI — Prompt Engineering
Feed Claude AI the packaging print file screenshots (dielines, spec sheets) and ask it to generate a detailed Gemini image generation prompt.

**What Claude produces:**
- Physical specs (dimensions, materials, closure type, finish)
- Panel-by-panel layout descriptions (top to bottom)
- Exact text strings for all copy elements
- Negative instructions ("NO pre-roll imagery", "NO fruit illustrations")
- Compliance element descriptions (NY Universal Symbol, warning blocks, potency stickers)
- Rendering style instructions (lighting, shadow, background, angle)

**Prompt structure that works:**
1. Overall render description (what we're generating)
2. Bag/box specifications (dimensions, materials, colors with PMS/hex)
3. FRONT PANEL layout (element by element, top to bottom)
4. BACK PANEL layout (element by element, top to bottom)
5. RENDERING STYLE (lighting, background, shadow, physical characteristics)

### Step 2: Gemini — Image Generation
Paste the Claude-generated prompt into Gemini along with the packaging print file as a reference image.

**What Gemini does well:**
- 3D volumetric rendering of packaging forms (bags, boxes, jars)
- Material simulation (matte mylar, spot UV gloss, zip-lock closure)
- Brand-level graphics (logo, color blocks, strain badges at large scale)
- Lighting and shadows for photorealistic depth
- Front/back side-by-side flat layouts

**What Gemini fails at:**
- Text smaller than ~14pt — consistently garbled
- Compliance sticker fine print — admits defeat explicitly
- Warning text — generates nonsensical approximations ("RGE RND OLOER" instead of "AGE AND OLDER")
- Terpene profiles, batch data, regulatory text
- Multi-product compositions with text on each item

**Iteration pattern:**
- First pass: ~80% accurate on form/layout, text garbled
- Gemini self-audits and identifies specific corrections
- 3-4 iterations typical to get a serviceable product render
- Text accuracy never reaches 100% — accept or fix in post

### Step 3: Post-Processing (Claude Code / CLI)
Download Gemini output and refine with programmatic tools.

**Pillow/ImageMagick tasks:**
- Crop white backgrounds
- Add/enhance drop shadows for 3D depth
- Resize to web-optimized dimensions
- Composite exact text overlays where Gemini garbled copy
- Generate compliance stickers programmatically (pixel-perfect)

### Step 4: Integration
- Place finished assets in /buypablo.com/assets/images/
- Update HTML references
- Mark completed in SITE-PLAN.md

## Hybrid Approach (Recommended)

| Element | Tool | Rationale |
|---|---|---|
| 3D product form | Gemini | Excellent at volumetric rendering |
| Brand elements (logo, colors, badges) | Gemini | Good at large-scale graphics |
| Product descriptor text (large) | Gemini | Acceptable at 14pt+ |
| Small text / compliance | Pillow/HTML→PNG | Must be exact — regulatory |
| Batch-variable stickers | Programmatic | Changes per production run |
| Drop shadows / cropping | ImageMagick/Pillow | Precise control |
| Family shots / multi-product | Gemini + compositing | Generate individual, composite together |

## Key Learnings

1. **Negative instructions are critical** — Gemini hallucinates objects (pre-rolls, fruit) if not explicitly told NO
2. **Reference images dramatically improve accuracy** — always attach the print file alongside the text prompt
3. **Gemini's self-audit is useful** — it identifies its own errors and suggests corrections
4. **Don't fight Gemini on text** — accept the form render and fix text in post-processing
5. **The prompt is the product** — investing in prompt quality pays off more than iteration count
