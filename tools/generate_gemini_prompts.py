#!/usr/bin/env python3
"""
PABLO Gemini Prompt Generator
Generates detailed image generation prompts for web assets.

Usage:
    python3 generate_gemini_prompts.py                  # Generate all 9 Tier 1 prompts
    python3 generate_gemini_prompts.py --asset 1        # Generate prompt for asset #1 only
    python3 generate_gemini_prompts.py --list            # List all assets

Output: prompt .txt files in ./output/prompts/
"""

import argparse
import os
import textwrap

from brand_config import (
    PABLO_BLUE, PABLO_YELLOW, PABLO_WHITE,
    FLAVOR_COLORS, LOGO_DESCRIPTION,
    NY_UNIVERSAL_SYMBOL, WARNING_TEXT,
)

RENDERING_STYLE_HERO = """RENDERING STYLE:
- Clean white background
- Soft studio lighting from upper left, creating natural shadows
- Slight drop shadow beneath the product for 3D depth and realism
- The product should appear to be sitting on a surface, not floating
- Photorealistic — should look like a professional product photograph
- The overall impression should be premium, clean, adult-oriented
- Deep blue packaging with white and yellow brand elements"""

RENDERING_STYLE_CARD = """RENDERING STYLE:
- Clean white or transparent background
- Soft, even studio lighting — no harsh shadows
- Slight drop shadow beneath for depth
- Product centered in frame with breathing room on all sides
- Photorealistic product photography style
- Image should work as a product card on a website (roughly square aspect ratio)"""

RENDERING_STYLE_FAMILY = """RENDERING STYLE:
- Clean white background
- Soft studio lighting, slightly dramatic — products arranged as a curated group
- Each product casts a subtle shadow
- Arrangement should feel intentional and premium — like an editorial product spread
- All products at consistent scale relative to each other
- Photorealistic — professional product photography aesthetic"""

# --- Prompt Templates ---

def prompt_1_hero_index():
    return {
        "id": 1,
        "name": "Hero product image (index)",
        "target": "index.html hero section",
        "prompt": f"""Gemini Image Generation Prompt — PABLO Landing Page Hero Image

Generate a photorealistic 3D product render of a premium cannabis vape product — a standing box (All-In-One vape packaging) shown at a slight angle on a clean white background.

PRODUCT: PABLO Live Resin All-In-One vape box
This is the flagship product for a premium NY cannabis brand.

BOX SPECIFICATIONS:
- Small rectangular box, approximately 144mm tall × 48.5mm wide × 18mm deep
- Color: deep royal blue ({PABLO_BLUE} / Pantone 2728 C) across the entire box surface
- Material: rigid cardboard with matte finish and spot UV gloss on the logo

FRONT PANEL (visible face, shown at slight angle):
{LOGO_DESCRIPTION}
- Below the logo: "LIVE RESIN" in bold white text
- Below that: "ALL-IN-ONE" in smaller white text
- Product descriptor: "FRESH FROZEN LIVE RESIN CONCENTRATE" in small white caps
- Strain name badge — a horizontal rounded-rectangle badge. Use a holographic/iridescent silver finish for Live Resin products
- Potency sticker zone — a small white rounded-rectangle sticker near the bottom reading "THC: [XX]% · CBD: [XX]%" in small black text. This should look like a physical sticker applied to the box, slightly raised
- {NY_UNIVERSAL_SYMBOL}
- Warning block — at the very bottom, a small white rectangle with rounded corners containing:
  Red text header: "WARNING:"
  Black text: "{WARNING_TEXT}"
  Text is small, dense, left-aligned inside the white box

SIDE PANEL (partially visible at angle):
- Pablo blue background
- Minimal text — just the PABLO logo repeated vertically or brand tagline

{RENDERING_STYLE_HERO}

IMPORTANT NOTES:
- NO cannabis leaf imagery on the box (other than the small NY Universal Symbol)
- NO hemp-era language — no "CBD", no "THC-P", no hemp warnings
- The box should look like it could sit on a dispensary shelf
- Show the box standing upright at approximately 15-20 degree angle
- The drop shadow should ground it convincingly on the surface
- Aspect ratio: landscape (approximately 16:9) for website hero placement"""
    }


def prompt_2_live_resin_card():
    return {
        "id": 2,
        "name": "Live Resin product card image",
        "target": "index.html Live Resin card",
        "prompt": f"""Gemini Image Generation Prompt — PABLO Live Resin Product Card

Generate a photorealistic product render of a PABLO Live Resin mylar bag, shown standing upright on a clean white background.

PRODUCT: PABLO Live Resin 510 Cartridge mylar bag
This is for a product card on a website — needs to be clean and immediately readable.

BAG SPECIFICATIONS:
- Dimensions: 76mm wide × 210mm tall
- Material: matte finish mylar with slight sheen
- Color: deep royal blue ({PABLO_BLUE} / Pantone 2728 C) across the entire bag surface
- 26mm zip-lock closure at the top
- 46mm hang hole flap above the zip
- Circular hang hole punched at top center

FRONT PANEL:
{LOGO_DESCRIPTION}
- "LIVE RESIN" in bold white and yellow text below the logo
- "510 CARTRIDGE" below that in white text
- Product descriptor: "FRESH FROZEN LIVE RESIN CONCENTRATE" in small white caps
- Strain name badge with holographic/iridescent silver background
- Potency sticker: small white rectangle, "THC: [XX]% · CBD: [XX]%"
- {NY_UNIVERSAL_SYMBOL}

{RENDERING_STYLE_CARD}

IMPORTANT:
- Show only the FRONT of the bag — single face, not front and back
- The bag should stand upright naturally
- NO cannabis leaf imagery except in the tiny NY Universal Symbol
- The hang hole and zip-lock should be visible at the top for realism"""
    }


def prompt_3_flavors_card():
    return {
        "id": 3,
        "name": "Flavors product card image",
        "target": "index.html Flavors card",
        "prompt": f"""Gemini Image Generation Prompt — PABLO Flavors Product Card

Generate a photorealistic product render of a PABLO Flavors mylar bag, shown standing upright on a clean white background.

PRODUCT: PABLO Flavors All-In-One vape mylar bag — Pineapple Marker flavor
This is for a product card on a website.

BAG SPECIFICATIONS:
- Dimensions: 76mm wide × 210mm tall
- Material: matte finish mylar
- Color: deep royal blue ({PABLO_BLUE}) across the entire bag surface
- 26mm zip-lock closure at the top
- 46mm hang hole flap above the zip
- Circular hang hole punched at top center
- A horizontal accent color band across the bag in the flavor's color: muted/dusty pink ({FLAVOR_COLORS["Pineapple Marker"]["color"]})

FRONT PANEL:
{LOGO_DESCRIPTION}
- "FLAVORS" in bold white and yellow text below the logo
- "ALL-IN-ONE" below that in white text
- Product descriptor: "FLAVOR FORWARD, HIGH POTENCY CANNABIS CONCENTRATE" in small white caps
- Strain name badge — horizontal rounded-rectangle badge with muted/dusty pink background ({FLAVOR_COLORS["Pineapple Marker"]["color"]}) and subtle crosshatch pattern. Text reads "PINEAPPLE MARKER" in bold white type. NO pineapple fruit illustration — text only.
- To the right of the badge: small "{FLAVOR_COLORS["Pineapple Marker"]["classification"]}" classification tag in white text
- Potency sticker: small white rectangle, "THC: [XX]% · CBD: [XX]%"
- {NY_UNIVERSAL_SYMBOL}

{RENDERING_STYLE_CARD}

IMPORTANT:
- Show only the FRONT of the bag
- The flavor accent band should be clearly visible — it differentiates Flavors from Live Resin
- NO fruit illustrations — this is a compliance concern (kid-appeal rules)
- NO cannabis leaf imagery except in the NY Universal Symbol"""
    }


def prompt_4_live_resin_hero():
    return {
        "id": 4,
        "name": "Live Resin hero image",
        "target": "live-resin.html hero",
        "prompt": f"""Gemini Image Generation Prompt — PABLO Live Resin Page Hero

Generate a photorealistic hero image showing a PABLO Live Resin All-In-One vape box as the centerpiece, with a mylar bag partially visible behind it, on a clean white background.

COMPOSITION:
- Primary product (foreground, center-right): PABLO Live Resin All-In-One box, standing upright at slight angle
- Secondary product (background, left): PABLO Live Resin 510 mylar bag, partially obscured, adding depth

PRIMARY PRODUCT — AIO BOX:
- Small rectangular box, ~144mm × 48.5mm × 18mm
- Deep royal blue ({PABLO_BLUE})
- {LOGO_DESCRIPTION}
- "LIVE RESIN" in bold white/yellow text
- "ALL-IN-ONE" below
- Holographic strain badge
- NY Universal Symbol and warning block at bottom
- Spot UV gloss on logo

SECONDARY PRODUCT — 510 BAG:
- Standing behind the box, offset to the left
- Same Pablo blue, visible PABLO logo
- "LIVE RESIN" text visible
- Partially cut off by the frame — this is background context, not the hero

{RENDERING_STYLE_HERO}

ASPECT RATIO: Wide landscape (approximately 21:9 or 2:1) for hero banner placement.
Products should occupy the right 60% of the frame, with clean white space on the left for text overlay.

IMPORTANT:
- This should feel like a premium product launch image
- No cannabis imagery except the small NY Universal Symbol
- The two products together communicate "multiple formats available"
- Both products are deep royal blue with white/yellow text — maintain brand consistency"""
    }


def prompt_5_flavors_hero():
    return {
        "id": 5,
        "name": "Flavors hero image",
        "target": "flavors.html hero",
        "prompt": f"""Gemini Image Generation Prompt — PABLO Flavors Page Hero

Generate a photorealistic hero image showing 3 PABLO Flavors mylar bags fanned out on a clean white background, each with a different flavor accent color band.

COMPOSITION:
- Three bags arranged in a fan/cascade from left to right, slightly overlapping
- Each bag is the same deep royal blue ({PABLO_BLUE}) but with a different colored accent band
- The arrangement should feel dynamic and colorful

BAG SPECIFICATIONS (all three identical except accent color):
- Dimensions: 76mm wide × 210mm tall
- Material: matte finish mylar
- Deep royal blue background
- Circular hang hole at top

BAG 1 (left, slightly behind):
- Flavor: Pineapple Marker
- Accent band color: pink ({FLAVOR_COLORS["Pineapple Marker"]["color"]})

BAG 2 (center, slightly forward):
- Flavor: Terp Taxi
- Accent band color: yellow/gold ({FLAVOR_COLORS["Terp Taxi"]["color"]})

BAG 3 (right, slightly behind):
- Flavor: Sunday Grape
- Accent band color: purple ({FLAVOR_COLORS["Sunday Grape"]["color"]})

ALL BAGS HAVE:
- {LOGO_DESCRIPTION}
- "FLAVORS" in bold white/yellow text
- Strain name badge in the respective accent color
- Small compliance elements at bottom (don't need to be legible — just present for realism)

{RENDERING_STYLE_HERO}

ASPECT RATIO: Wide landscape (approximately 21:9 or 2:1) for hero banner.
Products should occupy the right 60%, with clean white space on left for text overlay.

IMPORTANT:
- The three different accent colors are the star — they communicate variety and flavor options
- NO fruit illustrations anywhere — text-only strain names
- The overall impression is colorful but cohesive (all unified by the Pablo blue base)"""
    }


def prompt_6_live_resin_formats():
    return {
        "id": 6,
        "name": "Live Resin 3-format images (AIO, 510, Concentrate)",
        "target": "live-resin.html product cards",
        "prompt": f"""Gemini Image Generation Prompt — PABLO Live Resin Individual Product Cards (3 images)

Generate THREE separate photorealistic product renders, each on a clean white background. These are for individual product cards on a website — they need to be consistently sized and styled.

--- IMAGE 1: ALL-IN-ONE VAPE ---

Product: PABLO Live Resin All-In-One vape box
- Small rectangular box standing upright, ~144mm × 48.5mm × 18mm
- Deep royal blue ({PABLO_BLUE}), matte with spot UV on logo
- {LOGO_DESCRIPTION}
- "LIVE RESIN" + "ALL-IN-ONE" in white/yellow text
- Holographic strain badge
- NY Universal Symbol and compliance elements at bottom
- Show at very slight angle (5-10 degrees) for dimension

--- IMAGE 2: 510 CARTRIDGE ---

Product: PABLO Live Resin 510 Cartridge mylar bag
- Standing upright, 76mm × 210mm
- Deep royal blue matte mylar
- Hang hole at top, zip-lock visible
- {LOGO_DESCRIPTION}
- "LIVE RESIN" + "510 CARTRIDGE" in white/yellow text
- Holographic strain badge
- NY Universal Symbol at bottom

--- IMAGE 3: CONCENTRATE ---

Product: PABLO Live Resin Concentrate jar box
- Small square-ish box for a 1g glass jar
- Deep royal blue, same brand treatment
- {LOGO_DESCRIPTION}
- "LIVE RESIN" + "CONCENTRATE" in white/yellow text
- "1G POP-VAC GLASS JAR" descriptor
- Holographic strain badge
- NY Universal Symbol at bottom

{RENDERING_STYLE_CARD}

CRITICAL: All three products must be:
- Same visual style (lighting, shadow, background)
- Same relative scale (the box is smaller than the bag — show this accurately)
- Consistently framed with equal padding
- Shot from the same camera angle
- These will sit side by side on the website — visual consistency is everything"""
    }


def prompt_7_flavors_formats():
    return {
        "id": 7,
        "name": "Flavors 2-format images (AIO, 510)",
        "target": "flavors.html product cards",
        "prompt": f"""Gemini Image Generation Prompt — PABLO Flavors Individual Product Cards (2 images)

Generate TWO separate photorealistic product renders, each on a clean white background. These are for product cards on the Flavors page.

--- IMAGE 1: FLAVORS ALL-IN-ONE ---

Product: PABLO Flavors All-In-One vape box — Pineapple Marker
- Small rectangular box standing upright, ~144mm × 48.5mm × 18mm
- Deep royal blue ({PABLO_BLUE}), matte with spot UV on logo
- Accent color band: pink ({FLAVOR_COLORS["Pineapple Marker"]["color"]})
- {LOGO_DESCRIPTION}
- "FLAVORS" + "ALL-IN-ONE" in white/yellow text
- Strain badge: "PINEAPPLE MARKER" on pink background, text only — NO fruit
- "{FLAVOR_COLORS["Pineapple Marker"]["classification"]}" classification tag
- NY Universal Symbol and compliance at bottom
- Show at very slight angle for dimension

--- IMAGE 2: FLAVORS 510 CARTRIDGE ---

Product: PABLO Flavors 510 Cartridge mylar bag — Pineapple Marker
- Standing upright, 76mm × 210mm
- Deep royal blue matte mylar
- Accent color band: pink ({FLAVOR_COLORS["Pineapple Marker"]["color"]})
- Hang hole at top, zip-lock visible
- {LOGO_DESCRIPTION}
- "FLAVORS" + "510 CARTRIDGE" in white/yellow text
- Strain badge: "PINEAPPLE MARKER" on pink background, text only
- NY Universal Symbol at bottom

{RENDERING_STYLE_CARD}

CRITICAL:
- Both products must match in style, lighting, scale, and framing
- The accent color band is what differentiates Flavors from Live Resin — make it clearly visible
- NO fruit illustrations — compliance concern
- These sit side by side on the website"""
    }


def prompt_8_family_shot():
    return {
        "id": 8,
        "name": "Family shot (updated)",
        "target": "'The Pablo Difference' + 'The Standard' sections",
        "prompt": f"""Gemini Image Generation Prompt — PABLO Product Family Shot

Generate a photorealistic product photography image showing the full PABLO product lineup arranged together on a clean white background.

PRODUCTS IN THE SHOT (5 items, arranged as an editorial product spread):

1. PABLO Live Resin All-In-One box (standing, slight angle)
2. PABLO Live Resin 510 mylar bag (standing, behind the AIO box)
3. PABLO Live Resin Concentrate jar box (small, in front)
4. PABLO Flavors All-In-One box with pink accent band (standing, right side)
5. PABLO Flavors 510 mylar bag with pink accent band (standing, behind the Flavors box)

ALL PRODUCTS share:
- Deep royal blue ({PABLO_BLUE}) base color
- White PABLO hand-brushed script logo
- White and yellow text elements
- NY Universal Symbol (small, at bottom of each)
- Premium matte finish

DIFFERENTIATION:
- Live Resin products (items 1-3): holographic/silver strain badges, NO accent band
- Flavors products (items 4-5): colored accent band (pink for Pineapple Marker), text-only strain badge on colored background

ARRANGEMENT:
- Products grouped with Live Resin on the left, Flavors on the right
- Tallest items (bags) in back, shorter items (boxes) in front
- Natural, editorial arrangement — not a rigid lineup
- All products visible and identifiable, slight overlapping is OK for depth

{RENDERING_STYLE_FAMILY}

ASPECT RATIO: Landscape, approximately 3:2

CRITICAL:
- NO text reading "15% cannabis terpenes" — this is outdated
- NO "THC-P" anywhere — this is from hemp era
- The terpene percentage on packaging should read "10% CANNABIS TERPENES" if visible (NY cap)
- NO fruit illustrations on any product
- This shot needs to communicate: "this is a complete, professional product line"
- Small text does NOT need to be legible — just visually present for realism"""
    }


def prompt_9_flavor_badges():
    return {
        "id": 9,
        "name": "Flavor badges (clean)",
        "target": "flavors.html 'All Seven Flavors' section",
        "prompt": f"""Gemini Image Generation Prompt — PABLO Seven Flavors Badge Strip

Generate a clean, horizontal graphic showing all seven PABLO flavor badges arranged in a row on a white background.

THIS IS A GRAPHIC/BADGE DESIGN — not a product photo. Think of it as a flavor menu strip.

LAYOUT:
- 7 badges arranged horizontally in a single row with equal spacing
- Each badge is a horizontal rounded-rectangle (pill shape)
- All badges are the same size
- White background
- Slight drop shadow on each badge for depth

BADGE DESIGN (same shape for all, different colors):

1. PINEAPPLE MARKER — background: {FLAVOR_COLORS["Pineapple Marker"]["color"]} (pink)
2. SUNDAY GRAPE — background: {FLAVOR_COLORS["Sunday Grape"]["color"]} (purple)
3. TERP TAXI — background: {FLAVOR_COLORS["Terp Taxi"]["color"]} (yellow/gold)
4. WATERMELON GUSHER — background: {FLAVOR_COLORS["Watermelon Gusher"]["color"]} (red)
5. MARMALADE — background: {FLAVOR_COLORS["Marmalade"]["color"]} (orange)
6. MANGONADA — background: {FLAVOR_COLORS["Mangonada"]["color"]} (golden yellow)
7. PIE FACE — background: {FLAVOR_COLORS["Pie Face"]["color"]} (green)

EACH BADGE CONTAINS:
- Flavor name in BOLD WHITE ALL-CAPS text, centered
- Subtle crosshatch or texture pattern on the background (very subtle, not busy)
- That's it — no emoji, no fruit illustrations, no icons, no trademark symbols

TEXT RULES:
- Font: clean, bold sans-serif (like Bebas Neue or similar)
- All caps
- White text on colored background
- NO emojis of any kind — compliance concern (kid-appeal rules)
- NO trademark ™ symbols — trademarks were never filed

{RENDERING_STYLE_CARD}

ASPECT RATIO: Wide horizontal (approximately 7:1 or 6:1) — this spans the full width of a web page.

CRITICAL:
- This must be CLEAN — no sloppy edges, no black borders, no artifacts
- Each badge color must be distinct and vibrant
- The seven colors together should create a rainbow-like visual impact
- This is a key brand asset — the flavor lineup is a selling point"""
    }


ALL_PROMPTS = [
    prompt_1_hero_index,
    prompt_2_live_resin_card,
    prompt_3_flavors_card,
    prompt_4_live_resin_hero,
    prompt_5_flavors_hero,
    prompt_6_live_resin_formats,
    prompt_7_flavors_formats,
    prompt_8_family_shot,
    prompt_9_flavor_badges,
]


def main():
    parser = argparse.ArgumentParser(description="PABLO Gemini Prompt Generator")
    parser.add_argument("--asset", type=int, help="Generate prompt for specific asset number (1-9)")
    parser.add_argument("--list", action="store_true", help="List all assets")
    parser.add_argument("--output", type=str, default=None, help="Output directory")
    args = parser.parse_args()

    if args.list:
        print("PABLO Tier 1 Web Assets:\n")
        for fn in ALL_PROMPTS:
            p = fn()
            print(f"  [{p['id']}] {p['name']} → {p['target']}")
        return

    output_dir = args.output or os.path.join(os.path.dirname(__file__), "..", "output", "prompts")
    os.makedirs(output_dir, exist_ok=True)

    if args.asset:
        prompts = [ALL_PROMPTS[args.asset - 1]]
    else:
        prompts = ALL_PROMPTS

    for fn in prompts:
        p = fn()
        filename = f"prompt_{p['id']:02d}_{p['name'].lower().replace(' ', '_').replace('(', '').replace(')', '')}.txt"
        filepath = os.path.join(output_dir, filename)

        header = f"ASSET #{p['id']}: {p['name']}\nTARGET: {p['target']}\n{'='*60}\n\n"

        with open(filepath, "w") as f:
            f.write(header + p["prompt"])

        print(f"  [{p['id']}] {p['name']} → {filepath}")

    print(f"\nAll prompts saved to: {output_dir}")
    print("Copy each prompt into Gemini along with the relevant packaging print file as a reference image.")


if __name__ == "__main__":
    main()
