#!/usr/bin/env python3
"""
PABLO Live Resin Holographic Strain Sticker Generator
Generates print-ready strain identity stickers for Live Resin packaging.

Design: Holographic background, large stacked strain name in Bebas Neue,
"PABLO AUTHENTIC PRODUCT" subtitle in Space Grotesk, rounded rectangle.
The holographic effect is simulated for screen proofs — tell your vendor
"holographic film substrate" for actual production.

Usage:
    python3 generate_strain_stickers.py                          # All strains, all formats
    python3 generate_strain_stickers.py --strain "Sour Diesel"   # One strain, all formats
    python3 generate_strain_stickers.py --format 510             # All strains, 510 only
    python3 generate_strain_stickers.py --format aio             # All strains, AIO only
    python3 generate_strain_stickers.py --list                   # List configured strains

Output: sticker PNGs in ./output/strain_stickers/
"""

import argparse
import colorsys
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from brand_config import PABLO_BLUE

# --- Strain Definitions ---
LIVE_RESIN_STRAINS = [
    "Sour Diesel",
    "Runtz",
]

# --- Format Specifications ---
# Sticker dimensions per packaging format, in mm.
# 510: BrandMyBags dieline Job #72638 (Mylar pouch sticker area)
# AIO: box front panel sticker area
FORMAT_SPECS = {
    "510": {
        "name": "510 Cartridge Mylar",
        "width_mm": 55,
        "height_mm": 30,
        "corner_radius_mm": 4,
    },
    "aio": {
        "name": "All-In-One Box",
        "width_mm": 38,
        "height_mm": 20,
        "corner_radius_mm": 3,
    },
}

# --- Print Constants ---
DPI = 300
BLEED_MM = 1  # 1mm bleed on all sides

# Project font directory
FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "fonts")


def mm_to_px(mm):
    return int(mm * DPI / 25.4)


def get_font(name, size_px):
    """Load a font by name, with fallback chain."""
    paths = {
        "bebas": [
            os.path.join(FONT_DIR, "BebasNeue-Regular.ttf"),
            "/Library/Fonts/BebasNeue-Bold.ttf",
            "/Users/alexanderclaiborne/Library/Fonts/BebasNeue-Bold.ttf",
        ],
        "space": [
            os.path.join(FONT_DIR, "SpaceGrotesk-Bold.ttf"),
            "/Library/Fonts/SpaceGrotesk-Bold.ttf",
            "/Users/alexanderclaiborne/Library/Fonts/SpaceGrotesk-Bold.ttf",
        ],
    }
    fallbacks = paths.get(name, []) + ["/System/Library/Fonts/Supplemental/Arial Bold.ttf"]
    for path in fallbacks:
        try:
            return ImageFont.truetype(path, size_px)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def create_holographic_background(width, height):
    """
    Generate a holographic/iridescent gradient background.
    Silver-metallic base with subtle rainbow color shifts —
    matches real holographic film stock appearance.
    The actual holographic effect comes from the print substrate;
    this is a screen proof approximation.
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    for y in range(height):
        for x in range(width):
            # Diagonal position for gradient direction
            diag = (x / width * 0.55 + y / height * 0.45)

            # Hue cycles through spectrum but stays subtle
            hue = (diag * 0.9 + 0.08 * math.sin(x * 0.015 + y * 0.01)
                   + 0.04 * math.cos(y * 0.025)) % 1.0

            # Low saturation — silver base with gentle color tint
            sat = 0.12 + 0.10 * math.sin(diag * math.pi * 4)

            # High brightness — metallic silver
            val = 0.88 + 0.06 * math.sin(diag * math.pi * 3 + 0.5)

            r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
            img.putpixel((x, y), (int(r * 255), int(g * 255), int(b * 255), 255))

    # Add fine metallic noise
    noise = Image.new("RGBA", (width, height))
    random.seed(42)
    for y in range(0, height, 2):
        for x in range(0, width, 2):
            n = random.randint(-8, 8)
            c = (128 + n, 128 + n, 128 + n, 15)
            noise.putpixel((x, y), c)
            if x + 1 < width:
                noise.putpixel((x + 1, y), c)
            if y + 1 < height:
                noise.putpixel((x, y + 1), c)
                if x + 1 < width:
                    noise.putpixel((x + 1, y + 1), c)

    img = Image.alpha_composite(img, noise)
    img = img.filter(ImageFilter.GaussianBlur(radius=1.2))
    return img


def create_holographic_border(width, height, corner_radius, border_width):
    """
    Create a holographic border — more saturated rainbow at the sticker edge,
    simulating the foil catch-light visible on real holographic stickers.
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    for y in range(height):
        for x in range(width):
            dist_x = min(x, width - 1 - x)
            dist_y = min(y, height - 1 - y)
            dist = min(dist_x, dist_y)

            if dist < border_width:
                # Hue cycles around the perimeter
                perim = (x + y) / (width + height)
                hue = (perim * 1.8) % 1.0

                edge_ratio = 1.0 - (dist / border_width)
                # More saturated than the background, but still not garish
                sat = 0.3 + 0.25 * edge_ratio
                val = 0.90 + 0.08 * edge_ratio

                r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
                alpha = int(180 * edge_ratio + 40)
                img.putpixel((x, y), (int(r * 255), int(g * 255), int(b * 255), alpha))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    return img


def generate_strain_sticker(strain_name, fmt_key, output_dir):
    """Generate a holographic strain sticker at 300 DPI."""
    spec = FORMAT_SPECS[fmt_key]

    # Dimensions with bleed
    w_px = mm_to_px(spec["width_mm"])
    h_px = mm_to_px(spec["height_mm"])
    bleed_px = mm_to_px(BLEED_MM)

    total_w = w_px + 2 * bleed_px
    total_h = h_px + 2 * bleed_px
    corner_r = mm_to_px(spec["corner_radius_mm"])
    border_w = mm_to_px(1.2)  # 1.2mm holographic border

    # --- Build holographic background ---
    holo_bg = create_holographic_background(total_w, total_h)

    # --- Compose the sticker ---
    img = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))

    # Rounded rectangle mask for the sticker shape
    mask = Image.new("L", (total_w, total_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [bleed_px // 2, bleed_px // 2, total_w - bleed_px // 2 - 1, total_h - bleed_px // 2 - 1],
        radius=corner_r,
        fill=255,
    )

    # Apply holographic background through mask
    img.paste(holo_bg, (0, 0), mask)

    # Add the iridescent border overlay
    border = create_holographic_border(total_w, total_h, corner_r, border_w)
    border_masked = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    border_masked.paste(border, (0, 0), mask)
    img = Image.alpha_composite(img, border_masked)

    # Thin crisp outline
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [bleed_px // 2, bleed_px // 2, total_w - bleed_px // 2 - 1, total_h - bleed_px // 2 - 1],
        radius=corner_r,
        outline=(180, 180, 190, 180),
        width=max(1, mm_to_px(0.25)),
    )

    # --- Typography ---
    # Split strain name into lines (stack multi-word names)
    words = strain_name.upper().split()
    lines = words  # Each word on its own line

    # Calculate vertical layout zones
    # Top ~72% for strain name, bottom ~28% for subtitle
    strain_zone_top = bleed_px + mm_to_px(1.5)
    subtitle_baseline = total_h - bleed_px - mm_to_px(2.5)
    strain_zone_bottom = subtitle_baseline - mm_to_px(1.5)
    strain_zone_h = strain_zone_bottom - strain_zone_top

    # Auto-size strain name font
    target_w = int((total_w - 2 * bleed_px) * 0.85)
    line_count = len(lines)

    # Start with a large font and shrink to fit
    font_size = int(strain_zone_h / line_count * 1.1)
    font = get_font("bebas", font_size)

    # Measure and shrink until all lines fit
    while font_size > mm_to_px(3):
        font = get_font("bebas", font_size)
        max_line_w = 0
        total_text_h = 0
        line_spacing = int(font_size * -0.08)  # Tight leading for Bebas

        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_w = bbox[2] - bbox[0]
            line_h = bbox[3] - bbox[1]
            max_line_w = max(max_line_w, line_w)
            total_text_h += line_h

        total_text_h += line_spacing * (line_count - 1)

        if max_line_w <= target_w and total_text_h <= strain_zone_h:
            break
        font_size -= 1

    # Draw strain name — stacked, centered
    # Measure final layout
    line_metrics = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_metrics.append({
            "text": line,
            "w": bbox[2] - bbox[0],
            "h": bbox[3] - bbox[1],
            "y_offset": bbox[1],
        })

    total_text_h = sum(m["h"] for m in line_metrics) + line_spacing * (line_count - 1)
    y_start = strain_zone_top + (strain_zone_h - total_text_h) // 2

    y_cursor = y_start
    for m in line_metrics:
        text_x = (total_w - m["w"]) // 2

        # Dark shadow for depth/legibility on holographic bg
        shadow_off = max(1, mm_to_px(0.15))
        draw.text(
            (text_x + shadow_off, y_cursor - m["y_offset"] + shadow_off),
            m["text"], fill=(0, 0, 0, 90), font=font,
        )

        # Main text — dark charcoal for contrast on holographic
        draw.text(
            (text_x, y_cursor - m["y_offset"]),
            m["text"], fill=(25, 25, 30, 255), font=font,
        )

        y_cursor += m["h"] + line_spacing

    # --- Subtitle: "PABLO AUTHENTIC PRODUCT" ---
    subtitle = "PABLO AUTHENTIC PRODUCT"
    sub_font_size = max(mm_to_px(1.8), int(font_size * 0.18))

    # Size the subtitle to fit ~70% of sticker width
    sub_target_w = int((total_w - 2 * bleed_px) * 0.72)
    sub_font = get_font("space", sub_font_size)
    sub_bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
    sub_w = sub_bbox[2] - sub_bbox[0]

    while sub_w > sub_target_w and sub_font_size > mm_to_px(1.2):
        sub_font_size -= 1
        sub_font = get_font("space", sub_font_size)
        sub_bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        sub_w = sub_bbox[2] - sub_bbox[0]

    while sub_w < sub_target_w * 0.5 and sub_font_size < mm_to_px(4):
        sub_font_size += 1
        sub_font = get_font("space", sub_font_size)
        sub_bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        sub_w = sub_bbox[2] - sub_bbox[0]

    sub_x = (total_w - sub_w) // 2
    sub_y = subtitle_baseline - (sub_bbox[3] - sub_bbox[1])

    # Subtitle shadow
    draw.text(
        (sub_x + 1, sub_y + 1),
        subtitle, fill=(0, 0, 0, 60), font=sub_font,
    )
    # Subtitle text — slightly lighter than strain name
    draw.text(
        (sub_x, sub_y),
        subtitle, fill=(40, 40, 45, 230), font=sub_font,
    )

    # --- Save outputs ---
    safe_name = strain_name.lower().replace(" ", "_")
    os.makedirs(output_dir, exist_ok=True)

    # 1. Full sticker with bleed (for print production)
    print_filename = f"strain_{safe_name}_{fmt_key}.png"
    print_path = os.path.join(output_dir, print_filename)
    img.save(print_path, dpi=(DPI, DPI))

    # 2. Trimmed to final size (no bleed) for proofing
    trimmed = img.crop((bleed_px // 2, bleed_px // 2,
                        total_w - bleed_px // 2, total_h - bleed_px // 2))
    proof_filename = f"strain_{safe_name}_{fmt_key}_proof.png"
    proof_path = os.path.join(output_dir, proof_filename)

    # White background proof
    proof_bg = Image.new("RGB",
                         (trimmed.width + mm_to_px(6), trimmed.height + mm_to_px(6)),
                         (255, 255, 255))
    proof_bg.paste(trimmed, (mm_to_px(3), mm_to_px(3)),
                   trimmed.split()[3] if trimmed.mode == "RGBA" else None)
    proof_bg.save(proof_path, dpi=(DPI, DPI))

    # 3. On-blue mockup (simulates sticker on Pablo blue packaging)
    mockup_pad = mm_to_px(8)
    blue_rgb = tuple(int(PABLO_BLUE.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    mockup = Image.new("RGB",
                       (trimmed.width + mockup_pad * 2, trimmed.height + mockup_pad * 2),
                       blue_rgb)
    mockup.paste(trimmed, (mockup_pad, mockup_pad),
                 trimmed.split()[3] if trimmed.mode == "RGBA" else None)
    mockup_filename = f"strain_{safe_name}_{fmt_key}_on_blue.png"
    mockup_path = os.path.join(output_dir, mockup_filename)
    mockup.save(mockup_path, dpi=(DPI, DPI))

    return print_path, proof_path, mockup_path


def main():
    parser = argparse.ArgumentParser(description="PABLO Live Resin Holographic Strain Sticker Generator")
    parser.add_argument("--strain", type=str, help="Generate for a specific strain name")
    parser.add_argument("--format", type=str, default="all",
                        choices=list(FORMAT_SPECS.keys()) + ["all"],
                        help="Packaging format (default: all)")
    parser.add_argument("--list", action="store_true", help="List configured strains and formats")
    parser.add_argument("--output", type=str, default=None, help="Output directory")
    args = parser.parse_args()

    if args.list:
        print("PABLO Live Resin Strains:")
        for s in LIVE_RESIN_STRAINS:
            print(f"  • {s}")
        print("\nPackaging Formats:")
        for key, spec in FORMAT_SPECS.items():
            print(f"  • {key}: {spec['name']} ({spec['width_mm']}×{spec['height_mm']}mm)")
        return

    output_dir = args.output or os.path.join(os.path.dirname(__file__), "..", "output", "strain_stickers")
    os.makedirs(output_dir, exist_ok=True)

    strains = [args.strain] if args.strain else LIVE_RESIN_STRAINS
    formats = list(FORMAT_SPECS.keys()) if args.format == "all" else [args.format]

    print("PABLO Live Resin — Holographic Strain Stickers")
    print(f"Output: {output_dir}")
    print(f"Resolution: {DPI} DPI (print-ready)")
    print()

    for strain in strains:
        for fmt in formats:
            spec = FORMAT_SPECS[fmt]
            print(f"  {strain} / {spec['name']} ({spec['width_mm']}×{spec['height_mm']}mm)...")
            print_path, proof_path, mockup_path = generate_strain_sticker(strain, fmt, output_dir)
            img = Image.open(print_path)
            print(f"    ✓ Print:  {os.path.basename(print_path)} ({img.width}×{img.height}px)")
            print(f"    ✓ Proof:  {os.path.basename(proof_path)}")
            print(f"    ✓ Mockup: {os.path.basename(mockup_path)}")

    print()
    print("NOTE: Holographic gradient is a screen proof.")
    print("Specify HOLOGRAPHIC FILM substrate to your print vendor.")
    print(f"Bleed: {BLEED_MM}mm included in print files.")


if __name__ == "__main__":
    main()
