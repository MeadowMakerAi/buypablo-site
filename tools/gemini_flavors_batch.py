#!/usr/bin/env python3
"""
PABLO FLAVORS Line — Gemini API Batch Runner

Calls Gemini's image generation API directly to produce NY OCM compliant
packaging renders for the 6 remaining FLAVORS line AIO vapes. Sibling to the
Pillow-based generate_flavor_packaging.py — use this when you want a fresh
render from Gemini rather than an HSV-shifted template.

Usage:
    pip install google-genai
    export GEMINI_API_KEY=...

    python3 gemini_flavors_batch.py --dry-run                 # preview prompts
    python3 gemini_flavors_batch.py --model nano2             # all 6, cheap
    python3 gemini_flavors_batch.py --flavor sundae-grapes    # single, pro model
    python3 gemini_flavors_batch.py --list                    # show targets

Models:
    nano  → gemini-2.5-flash-image         ($0.039/img)
    nano2 → gemini-3.1-flash-image-preview ($0.045/img @ 1K, Feb 2026)
    pro   → gemini-3-pro-image-preview     ($0.134/img, default)
"""

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path

TOOLS_DIR = Path(__file__).parent
ASSETS_DIR = TOOLS_DIR.parent / "assets" / "images"
OUTPUT_DIR = TOOLS_DIR.parent / "output" / "flavor_packaging_gemini"

MODEL_ALIASES = {
    "nano":  "gemini-2.5-flash-image",
    "nano2": "gemini-3.1-flash-image-preview",
    "pro":   "gemini-3-pro-image-preview",
}


@dataclass
class Flavor:
    slug: str
    name: str
    classification: str
    accent_hex: str
    illustration: str
    text_on_accent: str  # "white" or "black"
    base_image: str
    font_size_pt: int = 14
    extra_note: str = ""


# Authoritative per-flavor data from gemini_prompts_all_flavors_ny_compliance.txt.
# brand_config.py has stale classifications and inverted colors (Pie Face/Watermelon) —
# do NOT import FLAVORS from there. Update brand_config.py after this batch lands.
FLAVORS = [
    Flavor("sundae-grapes", "SUNDAE GRAPES", "INDICA HYBRID", "#81288E",
           "Purple grape cluster", "white",
           "pablo_aio_sundae_grapes_ny.jpeg",
           extra_note='"SUNDAE" with -AE spelling, plural "GRAPES"'),
    Flavor("terp-taxi", "TERP TAXI", "INDICA HYBRID", "#FDAA00",
           "Yellow taxi cab silhouette; subtle black checker pattern in badge background",
           "black", "pablo_aio_terp_taxi_ny.jpeg",
           extra_note="Use white-outlined regulatory badges to stand out on yellow"),
    Flavor("mangonada", "MANGONADA", "INDICA HYBRID", "#FDB829",
           "Mango slice — orange/yellow flesh with green skin edge",
           "black", "pablo_aio_mangonada_ny.jpeg"),
    Flavor("marmalade", "MARMALADE", "SATIVA HYBRID", "#FCA311",
           "Orange citrus slice showing pulp and segments",
           "white", "pablo_aio_marmalade_ny.jpeg"),
    Flavor("pie-face", "PIE FACE", "SATIVA HYBRID", "#EE2737",
           "Red strawberry with green leaf top",
           "white", "pablo_aio_pie_face_ny.jpeg"),
    Flavor("watermelon-gusher", "WATERMELON GUSHER", "INDICA HYBRID", "#00855A",
           "Watermelon slice — red flesh, green rind, black seeds",
           "white", "pablo_aio_watermelon_gusher_ny.jpeg", font_size_pt=13),
]

FLAVORS_BY_SLUG = {f.slug: f for f in FLAVORS}


COMMON_SPEC = """\
Transform the provided base product image into NY OCM compliant FLAVORS line packaging.

LAYOUT (vertical label):
- Background: Pablo Blue (#0047BB) — full bleed to all edges
- Product image (AIO vape with yellow cartridge mouthpiece): center-left, keep original hardware detail
- Left spine: "FLAVORS" in white, vertical orientation
- OCM license seal on lower-left spine: circular, white border, "E 3" inside, ~0.5" diameter

TOP SECTION (center, stacked):
- "PABLO" logo — white, hand-brushed graffiti-style script, ~2" wide, upper-center
- Body text: "FLAVOR FORWARD, HIGH POTENCY CANNABIS CONCENTRATE" (white, 10pt, sans-serif)
- Dashed white divider
- "FLAVORS" (yellow #FDDA00, bold, 18pt)
- Dashed white divider

COMPLIANCE STRIP (below flavor badge, full width, on flavor accent color):
Three regulatory badges horizontally centered:
1. THC warning triangle — yellow fill #FDDA00, black border, black cannabis leaf, "THC!" in black
2. 21+ badge — red circle, white border, "21+" in black
3. NY State outline — black fill, white border, "NEW YORK STATE" in white
Spacing: 0.25" between badges. Size: ~0.65" each.

RECHARGEABLE CAPSULE (below compliance strip, on Pablo Blue):
- Rectangle, rounded corners (~6px radius)
- Fill: Pablo Blue #0047BB
- Border: 1.5pt white stroke
- Two lines of white text centered:
  - "RECHARGEABLE ALL-IN-ONE" (bold, 9pt)
  - "NET WT. 1G (0.0353 OZ)" (regular, 8pt)

WARNING TEXT (below capsule, directly on Pablo Blue — NO box, NO border):
- "THIS PRODUCT CONTAINS CANNABIS AND THC. KEEP OUT OF REACH OF CHILDREN AND PETS. FOR USE ONLY BY PERSONS 21 YEARS OF AGE AND OLDER."
- White text, 7pt, justified, generous margins

ILLUSTRATION STYLE (CRITICAL):
- Semi-realistic stylized fruit/icon, premium CPG aesthetic (Olipop / Liquid Death level)
- NOT cartoon. NOT childlike. NOT flat Material Design clipart.
- Clean outlines, saturated color, subtle depth
- Contained in left ~30% of the flavor badge rectangle
- Recognizable at small label size

OUTPUT: 300 DPI PNG, flat color design, no gradients, no shadows, exact hex codes.
"""


def compose_prompt(flavor: Flavor) -> str:
    text_color = "white" if flavor.text_on_accent == "white" else "BLACK (contrast required on light accent)"
    subtext_color = flavor.text_on_accent
    note_line = f"\n- Note: {flavor.extra_note}" if flavor.extra_note else ""
    return f"""\
PABLO AIO FLAVORS — {flavor.name} — NY OCM Compliant Packaging

{COMMON_SPEC}
FLAVOR BADGE (rectangular, rounded corners, center of label):
- Background fill: {flavor.accent_hex}
- Left ~30% of badge: Illustration — {flavor.illustration}. Semi-realistic premium CPG style.
- Right portion: "{flavor.name}" in {text_color}, bold, {flavor.font_size_pt}pt
- Below name: "{flavor.classification}" in {subtext_color}, 8pt{note_line}

COMPLIANCE STRIP BACKGROUND: {flavor.accent_hex}
"""


def run_generation(flavor: Flavor, model: str, client) -> Path | None:
    from google.genai import types

    prompt = compose_prompt(flavor)
    base_path = ASSETS_DIR / flavor.base_image
    parts: list = [prompt]
    if base_path.exists():
        parts.append(types.Part.from_bytes(
            data=base_path.read_bytes(),
            mime_type="image/jpeg",
        ))
    else:
        print(f"  ! base image missing: {base_path.name} — generating from prompt only")

    resp = client.models.generate_content(model=model, contents=parts)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"pablo_aio_{flavor.slug}_compliant.png"
    for part in resp.candidates[0].content.parts:
        inline = getattr(part, "inline_data", None)
        if inline and inline.data:
            out_path.write_bytes(inline.data)
            return out_path
    print(f"  ! no image returned for {flavor.name}")
    return None


def main():
    parser = argparse.ArgumentParser(description="PABLO FLAVORS packaging batch generator (Gemini API)")
    parser.add_argument("--flavor", help="slug of single flavor to run (see --list)")
    parser.add_argument("--model", choices=list(MODEL_ALIASES.keys()), default="pro",
                        help="nano (cheap), nano2 (preview), pro (production) — default: pro")
    parser.add_argument("--dry-run", action="store_true",
                        help="print composed prompts without calling the API")
    parser.add_argument("--list", action="store_true", help="list flavors and exit")
    args = parser.parse_args()

    if args.list:
        for f in FLAVORS:
            base_ok = "✓" if (ASSETS_DIR / f.base_image).exists() else "✗"
            print(f"  {f.slug:20s}  {f.name:20s}  {f.classification:14s}  {f.accent_hex}  base:{base_ok}")
        return

    if args.flavor and args.flavor not in FLAVORS_BY_SLUG:
        sys.exit(f"unknown flavor '{args.flavor}' — use --list to see options")
    targets = [FLAVORS_BY_SLUG[args.flavor]] if args.flavor else FLAVORS

    if args.dry_run:
        for f in targets:
            print(f"\n{'='*70}\n{f.name}  ({f.classification})  base:{f.base_image}\n{'='*70}")
            print(compose_prompt(f))
        return

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        sys.exit("GEMINI_API_KEY (or GOOGLE_API_KEY) not set in environment")

    try:
        from google import genai
    except ImportError:
        sys.exit("google-genai not installed — run: pip install google-genai")

    client = genai.Client(api_key=api_key)
    model_id = MODEL_ALIASES[args.model]
    print(f"Model: {model_id}  |  Output: {OUTPUT_DIR}\n")

    for f in targets:
        print(f"[{f.slug}] {f.name}")
        out = run_generation(f, model_id, client)
        if out:
            print(f"  → {out}")


if __name__ == "__main__":
    main()
