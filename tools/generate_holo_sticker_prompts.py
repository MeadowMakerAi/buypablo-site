#!/usr/bin/env python3
"""
PABLO Holographic Sticker — Precision Gemini Prompt Generator

Generates hyper-detailed image generation prompts that produce print-ready
holographic strain sticker renders matching the approved hero reference.

The prompts specify every dimension, color value, typographic detail, and
spatial relationship so Gemini reproduces the design without text garbling
or layout drift.

Usage:
    python3 generate_holo_sticker_prompts.py                                    # All strains, all formats
    python3 generate_holo_sticker_prompts.py --strain "Sour Diesel"             # One strain, all formats
    python3 generate_holo_sticker_prompts.py --strain "Sour Diesel" --format 510  # One strain, one format
    python3 generate_holo_sticker_prompts.py --mode mockup                      # On-bag mockup render
    python3 generate_holo_sticker_prompts.py --mode sticker                     # Isolated sticker only
    python3 generate_holo_sticker_prompts.py --mode print                       # Flat print-ready artwork
    python3 generate_holo_sticker_prompts.py --list                             # List strains + formats

Output: prompt .txt files in ./output/prompts/holo_stickers/
"""

import argparse
import os
import textwrap

from brand_config import (
    PABLO_BLUE, PABLO_YELLOW, PABLO_WHITE,
    LOGO_DESCRIPTION,
    NY_UNIVERSAL_SYMBOL, WARNING_TEXT,
    PROCESSOR_NAME, PROCESSOR_LICENSE, PROCESSOR_EMAIL,
)

# --- Strain Config ---
# Live Resin strains — update as sourcing confirms new strains.
LIVE_RESIN_STRAINS = {
    "Sour Diesel": {
        "classification": "SATIVA",
        "terpenes": "β-Caryophyllene, Limonene, Myrcene",
        "line_break": ["SOUR", "DIESEL"],  # How the name stacks on the sticker
    },
    "Runtz": {
        "classification": "HYBRID",
        "terpenes": "β-Caryophyllene, Limonene, Linalool",
        "line_break": ["RUNTZ"],
    },
}

# --- Packaging Format Specs ---
FORMAT_SPECS = {
    "510": {
        "name": "510 Cartridge Mylar Bag",
        "sticker_width_mm": 55,
        "sticker_height_mm": 30,
        "sticker_corner_radius_mm": 4,
        "bag_width_mm": 76,
        "bag_height_mm": 210,
        "product_descriptor": "510 THREAD CERAMIC CARTRIDGE",
        "net_weight": "0.5 g",
        "has_hang_hole": True,
        "has_ziplock": True,
    },
    "aio": {
        "name": "All-In-One Vape Box",
        "sticker_width_mm": 38,
        "sticker_height_mm": 20,
        "sticker_corner_radius_mm": 3,
        "box_width_mm": 48.5,
        "box_height_mm": 144,
        "box_depth_mm": 18,
        "product_descriptor": "ALL-IN-ONE DISPOSABLE VAPE",
        "net_weight": "0.5 g",
        "has_hang_hole": False,
        "has_ziplock": False,
    },
}

# --- Design Language (extracted from approved hero render) ---

HOLOGRAPHIC_STICKER_DESIGN = """HOLOGRAPHIC STICKER DESIGN SPECIFICATION:
The sticker is a rounded rectangle applied to the lower-center of the packaging front face.

SHAPE:
- Rounded rectangle with {corner_r}mm corner radius
- Dimensions: {sticker_w}mm wide × {sticker_h}mm tall
- Oriented horizontally (landscape)

BACKGROUND — HOLOGRAPHIC FILM:
- The sticker background is HOLOGRAPHIC / IRIDESCENT film
- Base tone: silver-metallic
- Iridescent color shifts: soft rainbow reflections that change with viewing angle
- The rainbow shifts include: pale blue, pink/magenta, green, gold, lavender
- The iridescent effect is SUBTLE — silver-dominant with color accents, NOT a full rainbow gradient
- There is a slight blue cast from the packaging behind the sticker bleeding through at the edges
- The holographic effect should look like REAL holographic foil, not a digital gradient

BORDER:
- Thin white border outline around the entire rounded rectangle, approximately 0.5mm
- The border separates the holographic surface from the blue packaging
- Clean, crisp, consistent width on all sides
- The border has a very subtle glow/brightness from the holographic film beneath it

TYPOGRAPHY — STRAIN NAME:
- Text: "{sticker_lines}"
- Font: Bold condensed sans-serif (Bebas Neue or very similar)
- Case: ALL CAPS
- Layout: {line_layout}
- Size: LARGE — the strain name dominates the sticker, filling approximately 70-75% of the sticker height
- Color: The text appears to SHOW THROUGH to the holographic film beneath — meaning the letterforms themselves display the iridescent rainbow effect
- This is achieved by the text being cut/printed clear on the opaque layer, letting the holographic substrate show through
- The text should shimmer with the same iridescent colors as the background but more vivid/saturated because it's the focal point
- There is a very subtle dark outline/shadow on the text edges for definition against the holographic background
- Letter spacing: tight but not touching
- The text is horizontally centered on the sticker

TYPOGRAPHY — SUBTITLE:
- Text: "PABLO AUTHENTIC PRODUCT"
- Font: Clean sans-serif (Space Grotesk or similar), medium weight
- Case: ALL CAPS
- Size: Small — approximately 15-18% the height of the strain name text
- Color: Dark charcoal/near-black (#222222), slightly transparent
- Position: Centered horizontally, positioned in the bottom 20% of the sticker
- Letter spacing: slightly tracked out (wider than normal)
- This text is PRINTED ON the holographic surface (opaque ink), NOT showing through like the strain name"""

PACKAGING_510_CONTEXT = """PACKAGING CONTEXT — 510 CARTRIDGE MYLAR BAG:
The sticker sits on the front of a standing mylar bag.

BAG SPECS:
- Dimensions: 76mm wide × 210mm tall (approximately 3" × 8.25")
- Material: Matte finish mylar with slight sheen
- Color: Deep royal blue ({pablo_blue} / Pantone 2728 C) across the entire surface
- Hang hole: Circular die-cut hole at top center, approximately 8mm diameter
- Zip-lock: 26mm closure zone below the hang hole flap
- Tear notch: Small V-notch on each side at the zip-lock line

FRONT FACE LAYOUT (top to bottom):
1. HANG HOLE FLAP (top 46mm) — blue with centered circular hole
2. ZIP-LOCK LINE — subtle horizontal seam
3. PABLO LOGO — large white hand-brushed/graffiti-style script. Positioned in upper third of the visible face below the zip. The logo is distinctive with flowing, street-art quality letterforms. Approximately 50mm wide.
4. "READY TO VAPE CONCENTRATE" — small white caps text, centered below logo, approximately 5pt equivalent
5. "FRESH FROZEN" — white text, slightly smaller than the line below
6. "LIVE RESIN" — BOLD white text, larger than surrounding text, this is the product line identifier. Approximately 12pt equivalent. Centered.
7. >>> HOLOGRAPHIC STRAIN STICKER <<< — positioned here, centered horizontally on the bag face. The sticker occupies approximately 72% of the bag width.
8. NY UNIVERSAL SYMBOL — {ny_symbol_short} — small, positioned below the sticker, left-aligned or centered
9. "{product_descriptor}" — small white text below the universal symbol
10. "NET WEIGHT: {net_weight}" — small white text
11. "BATCH INFO #[XXXX]" — small white text (placeholder)
12. "WARNING:" — small white text (compliance)

BOTTOM AREA:
- Small PABLO circular seal/badge — bottom left corner, approximately 10mm diameter
- The seal has "PABLO" text in a circular arrangement

IMPORTANT SPATIAL RELATIONSHIPS:
- The sticker is positioned roughly in the vertical center of the visible bag face (below zip, above bottom compliance text)
- There is approximately 8-10mm of blue bag visible between the "LIVE RESIN" text and the top edge of the sticker
- There is approximately 12-15mm of blue bag visible between the bottom edge of the sticker and the NY Universal Symbol"""

PACKAGING_AIO_CONTEXT = """PACKAGING CONTEXT — ALL-IN-ONE VAPE BOX:
The sticker sits on the front face of a small rectangular box.

BOX SPECS:
- Dimensions: 48.5mm wide × 144mm tall × 18mm deep
- Material: Rigid cardboard, matte finish with spot UV gloss on the PABLO logo
- Color: Deep royal blue ({pablo_blue} / Pantone 2728 C) across all surfaces
- Opening: Top-tuck flap

FRONT FACE LAYOUT (top to bottom):
1. PABLO LOGO — large white hand-brushed/graffiti-style script. Positioned in upper quarter. The logo is distinctive with flowing, street-art quality letterforms. Approximately 38mm wide, scaled to fit the narrower box.
2. "READY TO VAPE CONCENTRATE" — small white caps text, centered below logo
3. "FRESH FROZEN" — white text, slightly smaller
4. "LIVE RESIN" — BOLD white text, larger, product line identifier
5. >>> HOLOGRAPHIC STRAIN STICKER <<< — positioned here, centered horizontally. The sticker occupies approximately 78% of the box width.
6. NY UNIVERSAL SYMBOL — small, below the sticker
7. "{product_descriptor}" — small white text
8. "NET WEIGHT: {net_weight}" — small white text
9. Bottom compliance text

IMPORTANT SPATIAL RELATIONSHIPS:
- The box is narrower than the bag, so the sticker is proportionally larger relative to the face
- The sticker is vertically centered in the middle third of the front face
- Less breathing room between elements due to narrower width"""


def build_sticker_text_spec(strain_name, strain_info):
    """Build the typography specification for a given strain."""
    lines = strain_info["line_break"]
    if len(lines) == 1:
        line_layout = f'Single line: "{lines[0]}" centered horizontally and vertically'
        sticker_lines = lines[0]
    else:
        line_layout = (
            f'Stacked on {len(lines)} lines:\n'
            + "\n".join(f'  Line {i+1}: "{line}"' for i, line in enumerate(lines))
            + "\n  Lines are vertically stacked with tight leading (minimal line gap)"
            + "\n  Both lines centered horizontally"
            + f"\n  The word \"{lines[0]}\" sits above \"{lines[1]}\""
        )
        sticker_lines = " / ".join(lines)
    return sticker_lines, line_layout


def generate_mockup_prompt(strain_name, fmt_key):
    """
    Generate a prompt for a photorealistic on-packaging mockup render.
    This is the hero shot — sticker shown applied to the actual bag/box
    in a styled product photography setting.
    """
    strain = LIVE_RESIN_STRAINS[strain_name]
    fmt = FORMAT_SPECS[fmt_key]
    sticker_lines, line_layout = build_sticker_text_spec(strain_name, strain)

    sticker_spec = HOLOGRAPHIC_STICKER_DESIGN.format(
        corner_r=fmt["sticker_corner_radius_mm"],
        sticker_w=fmt["sticker_width_mm"],
        sticker_h=fmt["sticker_height_mm"],
        sticker_lines=sticker_lines,
        line_layout=line_layout,
    )

    ny_symbol_short = "Three connected icons: (a) yellow triangle with 'THC!' (b) red circle with '21+' (c) dark rectangle with NY state outline"

    if fmt_key == "510":
        packaging_spec = PACKAGING_510_CONTEXT.format(
            pablo_blue=PABLO_BLUE,
            ny_symbol_short=ny_symbol_short,
            product_descriptor=fmt["product_descriptor"],
            net_weight=fmt["net_weight"],
        )
    else:
        packaging_spec = PACKAGING_AIO_CONTEXT.format(
            pablo_blue=PABLO_BLUE,
            product_descriptor=fmt["product_descriptor"],
            net_weight=fmt["net_weight"],
        )

    camera_angle = (
        "Slight 3/4 angle from above-right (approximately 15-20 degrees from straight-on, "
        "10 degrees downward tilt). This angle shows the front face fully while revealing "
        "just a sliver of the right edge for dimensionality."
    )
    if fmt_key == "510":
        camera_angle += (
            "\nThe bag should appear to be laying flat or propped at a very slight angle "
            "on a dark surface (charcoal/dark gray, subtle texture like felt or matte paper)."
        )
    else:
        camera_angle += (
            "\nThe box should be standing upright on a dark surface "
            "(charcoal/dark gray, subtle texture like felt or matte paper)."
        )

    prompt = f"""Gemini Image Generation Prompt — PABLO Live Resin Holographic Sticker Mockup
Strain: {strain_name} | Format: {fmt["name"]}

=== WHAT TO GENERATE ===
A photorealistic product photography render of a PABLO Live Resin {fmt["name"].lower()} with a holographic strain sticker applied to the front face. This should look like a professional product photograph taken in a studio — not a flat graphic or illustration.

=== CAMERA & LIGHTING ===
CAMERA:
{camera_angle}

LIGHTING:
- Primary: Soft key light from upper-left, creating gentle highlights on the packaging surface
- Secondary: Subtle fill from the right to prevent harsh shadows
- The holographic sticker should show iridescent color shifts as if catching the studio light
- A slight specular highlight on the holographic surface (one bright spot where the light source reflects most directly)
- The blue packaging should appear rich and saturated, not washed out

BACKGROUND:
- Dark charcoal/near-black surface ({PABLO_BLUE} darkened to approximately #1a1a1e)
- Subtle texture — matte paper, felt, or fine fabric
- Slight vignette darkening at the corners
- No other objects in the frame

=== PACKAGING SPECIFICATION ===
{packaging_spec}

=== STICKER SPECIFICATION ===
{sticker_spec}

=== TEXT ACCURACY — CRITICAL ===
This is the most important section. Every text element must be EXACTLY as specified.
Gemini: do NOT paraphrase, abbreviate, misspell, or improvise any text.

STICKER TEXT (2 elements only):
1. Strain name: "{strain_name.upper()}" — {f'stacked as "{strain["line_break"][0]}" over "{strain["line_break"][1]}"' if len(strain["line_break"]) > 1 else f'single line "{strain["line_break"][0]}"'}
2. Subtitle: "PABLO AUTHENTIC PRODUCT" — exactly these three words, in this order

PACKAGING TEXT (verify each one):
- Logo: "PABLO" in hand-brushed script (this is a logo, not typed text)
- "READY TO VAPE CONCENTRATE"
- "FRESH FROZEN"
- "LIVE RESIN"
- "{fmt["product_descriptor"]}"
- "NET WEIGHT : {fmt["net_weight"]}"

DO NOT WRITE:
- "TUREAD" (this is not a word)
- "CADTBIOGE" (this is not a word)
- "CARTBIOGE" (this is not a word)
- Any garbled, misspelled, or hallucinated text
- If you are unsure about a word, OMIT IT rather than guessing wrong

=== ASPECT RATIO ===
{"Landscape, approximately 16:9 (1920×1080px or similar)" if fmt_key == "510" else "Portrait, approximately 3:4 (1080×1440px or similar)"}

=== QUALITY ===
- Photorealistic — this should be indistinguishable from a real product photo
- High resolution, minimum 2048px on the longest edge
- No watermarks, no borders, no text outside the product
- The holographic effect should look convincing — like actual holographic film, with natural iridescent color transitions
- The Pablo blue should be rich and deep, not washed out or faded
- All text must be crisp and legible at the intended viewing size

=== REFERENCE STYLE ===
Think: premium cannabis brand product photography for a brand website hero image.
Comparable to: Houseplant, Beboe, MFNY product shots.
Dark background, dramatic but clean lighting, product as the star.
"""
    return prompt


def generate_isolated_sticker_prompt(strain_name, fmt_key):
    """
    Generate a prompt for an isolated sticker render — no packaging,
    just the holographic sticker on a transparent or white background.
    Useful for compositing onto other mockups or for vendor print proofs.
    """
    strain = LIVE_RESIN_STRAINS[strain_name]
    fmt = FORMAT_SPECS[fmt_key]
    sticker_lines, line_layout = build_sticker_text_spec(strain_name, strain)

    sticker_spec = HOLOGRAPHIC_STICKER_DESIGN.format(
        corner_r=fmt["sticker_corner_radius_mm"],
        sticker_w=fmt["sticker_width_mm"],
        sticker_h=fmt["sticker_height_mm"],
        sticker_lines=sticker_lines,
        line_layout=line_layout,
    )

    prompt = f"""Gemini Image Generation Prompt — PABLO Holographic Sticker (Isolated)
Strain: {strain_name} | Format: {fmt["name"]} ({fmt["sticker_width_mm"]}×{fmt["sticker_height_mm"]}mm)

=== WHAT TO GENERATE ===
A single holographic sticker rendered in isolation on a plain white background. NO packaging — just the sticker itself, as if photographed laying flat on a white surface. This is for print vendor proofing and digital compositing.

=== RENDER STYLE ===
- The sticker is shown FLAT, viewed straight-on (0 degree angle, no perspective)
- Very slight drop shadow beneath the sticker to lift it off the background (2-3px, soft, 20% opacity)
- The holographic surface catches light as if under soft overhead studio lighting
- White or very light gray (#F5F5F5) background
- The sticker fills approximately 80% of the image width

=== STICKER SPECIFICATION ===
{sticker_spec}

=== DIMENSIONS ===
The image should be output at the exact proportions of {fmt["sticker_width_mm"]}mm × {fmt["sticker_height_mm"]}mm.
Aspect ratio: {fmt["sticker_width_mm"]/fmt["sticker_height_mm"]:.2f}:1

=== TEXT ACCURACY — CRITICAL ===
ONLY TWO TEXT ELEMENTS ON THE ENTIRE STICKER:
1. "{strain_name.upper()}" — large, {f'stacked: "{strain["line_break"][0]}" on top, "{strain["line_break"][1]}" below' if len(strain["line_break"]) > 1 else f'single line'}
2. "PABLO AUTHENTIC PRODUCT" — small, at the bottom

That is ALL. No other text. No "live resin", no weight, no batch info.
Do NOT add any text that is not listed above.

=== QUALITY ===
- High resolution: minimum 2048px wide
- Crisp edges on the rounded rectangle
- Holographic effect should be realistic — silver-metallic base with subtle iridescent rainbow shifts
- Text must be perfectly legible and correctly spelled
"""
    return prompt


def generate_print_artwork_prompt(strain_name, fmt_key):
    """
    Generate a prompt for flat print-ready artwork — vector-style,
    no 3D effects, designed for direct output to print vendor.
    """
    strain = LIVE_RESIN_STRAINS[strain_name]
    fmt = FORMAT_SPECS[fmt_key]

    prompt = f"""Gemini Image Generation Prompt — PABLO Holographic Sticker PRINT ARTWORK
Strain: {strain_name} | Format: {fmt["name"]} ({fmt["sticker_width_mm"]}×{fmt["sticker_height_mm"]}mm)

=== WHAT TO GENERATE ===
A flat, 2D print-ready artwork file for a holographic sticker. This is NOT a photograph or 3D render — it is the ARTWORK LAYER that will be printed onto holographic film stock by the vendor.

=== DESIGN ===
CANVAS:
- Exact aspect ratio: {fmt["sticker_width_mm"]}:{fmt["sticker_height_mm"]} ({fmt["sticker_width_mm"]/fmt["sticker_height_mm"]:.2f}:1)
- Rounded rectangle with {fmt["sticker_corner_radius_mm"]}mm corner radius
- Include 1mm bleed beyond the die-cut line on all sides

BACKGROUND:
- The background should represent the holographic film substrate
- Render as a silver-metallic gradient with subtle iridescent color shifts
- Colors cycle gently: silver → pale blue → lavender → pink → gold → green → silver
- The gradient direction is diagonal (upper-left to lower-right)
- Low saturation — predominantly silver with gentle color tints, NOT a vivid rainbow

BORDER:
- Thin white outline (0.5mm) around the rounded rectangle perimeter
- This sits on the die-cut line

STRAIN NAME:
- Text: {f'Line 1: "{strain["line_break"][0]}" / Line 2: "{strain["line_break"][1]}"' if len(strain["line_break"]) > 1 else f'"{strain["line_break"][0]}"'}
- Font: Bebas Neue Bold or equivalent condensed sans-serif, ALL CAPS
- Size: Fills approximately 70% of the sticker area vertically
- Color: The text should appear TRANSPARENT / CLEAR — showing the holographic substrate through the letterforms at higher saturation/vibrancy than the surrounding background
- Alternatively, render as white text with a holographic/rainbow gradient fill
- Position: Centered horizontally and vertically (biased slightly upward to leave room for subtitle)

SUBTITLE:
- Text: "PABLO AUTHENTIC PRODUCT"
- Font: Space Grotesk Medium or equivalent clean sans-serif, ALL CAPS
- Size: Approximately 15% the height of the strain name
- Color: Dark charcoal (#333333)
- Position: Centered horizontally, bottom 18% of the sticker
- Letter spacing: 5-8% tracked out

=== TEXT ACCURACY ===
EXACTLY two text elements. Nothing else.
1. "{strain_name.upper()}"
2. "PABLO AUTHENTIC PRODUCT"

=== OUTPUT ===
- Flat 2D artwork, no shadows, no 3D, no perspective
- High resolution: at least 3000px on the longest edge (for 300 DPI print at actual size)
- Clean edges, no anti-aliasing artifacts on the die-cut boundary
- This file goes directly to the print vendor who will produce it on holographic film stock
"""
    return prompt


# --- Main ---

MODE_GENERATORS = {
    "mockup": generate_mockup_prompt,
    "sticker": generate_isolated_sticker_prompt,
    "print": generate_print_artwork_prompt,
}


def main():
    parser = argparse.ArgumentParser(
        description="PABLO Holographic Sticker — Precision Gemini Prompt Generator"
    )
    parser.add_argument("--strain", type=str, help="Strain name (e.g. 'Sour Diesel')")
    parser.add_argument("--format", type=str, default="all",
                        choices=list(FORMAT_SPECS.keys()) + ["all"])
    parser.add_argument("--mode", type=str, default="all",
                        choices=list(MODE_GENERATORS.keys()) + ["all"],
                        help="Render mode: mockup (on-bag), sticker (isolated), print (flat artwork), all")
    parser.add_argument("--list", action="store_true", help="List strains and formats")
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    if args.list:
        print("PABLO Live Resin Strains:")
        for name, info in LIVE_RESIN_STRAINS.items():
            print(f"  • {name} ({info['classification']}) — stacks as: {' / '.join(info['line_break'])}")
        print("\nPackaging Formats:")
        for key, spec in FORMAT_SPECS.items():
            print(f"  • {key}: {spec['name']} (sticker: {spec['sticker_width_mm']}×{spec['sticker_height_mm']}mm)")
        print("\nRender Modes:")
        print("  • mockup  — Photorealistic on-packaging hero shot (dark bg)")
        print("  • sticker — Isolated sticker on white (for compositing/proofing)")
        print("  • print   — Flat 2D print artwork (for vendor production)")
        return

    output_dir = args.output or os.path.join(
        os.path.dirname(__file__), "..", "output", "prompts", "holo_stickers"
    )
    os.makedirs(output_dir, exist_ok=True)

    strains = [args.strain] if args.strain else list(LIVE_RESIN_STRAINS.keys())
    formats = list(FORMAT_SPECS.keys()) if args.format == "all" else [args.format]
    modes = list(MODE_GENERATORS.keys()) if args.mode == "all" else [args.mode]

    print("PABLO Holographic Sticker — Gemini Prompt Generator")
    print(f"Output: {output_dir}")
    print()

    count = 0
    for strain in strains:
        if strain not in LIVE_RESIN_STRAINS:
            print(f"  ✗ Unknown strain: {strain}")
            continue
        for fmt in formats:
            for mode in modes:
                generator = MODE_GENERATORS[mode]
                prompt = generator(strain, fmt)

                safe_strain = strain.lower().replace(" ", "_")
                filename = f"holo_{safe_strain}_{fmt}_{mode}.txt"
                filepath = os.path.join(output_dir, filename)

                with open(filepath, "w") as f:
                    f.write(prompt)

                print(f"  ✓ {strain} / {FORMAT_SPECS[fmt]['name']} / {mode} → {filename}")
                count += 1

    print(f"\n{count} prompts generated in {output_dir}")
    print()
    print("USAGE:")
    print("  1. Open Google AI Studio or Gemini")
    print("  2. Paste the prompt text")
    print("  3. For mockup mode: attach the hero reference image as a style guide")
    print("  4. For print mode: specify 'output at 300 DPI' in the generation settings")
    print("  5. Review text accuracy FIRST — strain name and subtitle spelling")


if __name__ == "__main__":
    main()
