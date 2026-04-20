#!/usr/bin/env python3
"""
PABLO Compliance Sticker Generator
Generates print-ready potency and compliance stickers per NY OCM §128.5.

Usage:
    python3 generate_stickers.py
    python3 generate_stickers.py --thc 32.4 --cbd 0.1 --lot PM-2026-0301A --exp 09/01/2026 --warning A
    python3 generate_stickers.py --terpenes "β-Caryophyllene:1.2,Limonene:0.9,Myrcene:0.8"
    python3 generate_stickers.py --product preroll  (default)
    python3 generate_stickers.py --product flavors-510
    python3 generate_stickers.py --product live-resin-aio

Output: sticker PNGs in ./output/stickers/
"""

import argparse
import os
import sys
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
import qrcode

from brand_config import (
    ROTATING_WARNINGS, PRODUCT_INGREDIENTS,
    PROCESSOR_NAME, PROCESSOR_CITY, PROCESSOR_LICENSE, PROCESSOR_EMAIL,
)

# --- Constants ---

# Print resolution: 300 DPI
DPI = 300

def mm_to_px(mm):
    """Convert millimeters to pixels at 300 DPI."""
    return int(mm * DPI / 25.4)

# Font paths (macOS)
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

# §128.5(h): minimum 6pt. We use 7-8pt for potency, 6pt minimum for compliance.
def pt_to_px(pt):
    """Convert points to pixels at 300 DPI."""
    return int(pt * DPI / 72)


def create_front_potency_sticker(thc: float, cbd: float, output_dir: str) -> str:
    """
    Generate the front potency sticker.
    Dimensions: 40mm x 12mm at 300 DPI.
    Content: THC: XX.X% · CBD: X.X%
    §128.5(a)(2), §128.5(c) — minimum 6pt, we use 8pt bold.
    """
    width = mm_to_px(40)
    height = mm_to_px(12)

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Border — thin black outline
    draw.rectangle([0, 0, width - 1, height - 1], outline="black", width=2)

    # Text
    font_size = pt_to_px(8)
    font = ImageFont.truetype(ARIAL_BOLD, font_size)
    text = f"THC: {thc:.1f}%  ·  CBD: {cbd:.1f}%"

    # Center the text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) // 2
    y = (height - text_h) // 2 - bbox[1]  # Adjust for font baseline offset

    draw.text((x, y), text, fill="black", font=font)

    path = os.path.join(output_dir, "sticker_front_potency.png")
    img.save(path, dpi=(DPI, DPI))
    return path


def create_back_compliance_sticker(
    thc: float,
    cbd: float,
    lot: str,
    exp: str,
    warning_version: str,
    terpenes: dict,
    product: str,
    output_dir: str,
) -> str:
    """
    Generate the back compliance sticker.
    Dimensions: 50mm wide, height dynamic (target ~55mm, may grow).
    All text Arial, minimum 6pt, black on white per §128.5(h).
    """
    width = mm_to_px(50)
    margin = mm_to_px(2)
    content_width = width - 2 * margin

    # Fonts
    font_6 = ImageFont.truetype(ARIAL, pt_to_px(6))
    font_6_bold = ImageFont.truetype(ARIAL_BOLD, pt_to_px(6))
    font_7 = ImageFont.truetype(ARIAL, pt_to_px(7))
    font_7_bold = ImageFont.truetype(ARIAL_BOLD, pt_to_px(7))

    # QR code size
    qr_size = mm_to_px(12)

    # --- Pre-render to calculate height ---
    # We'll build a list of drawing operations, then render

    sections = []

    # SECTION 1: Rotating warning
    warning_text = ROTATING_WARNINGS[warning_version]
    sections.append(("bold", f"WARNING: ", "regular", warning_text))

    # SECTION 2: Fixed warnings
    sections.append(("separator",))
    sections.append(("regular", "Warning: Do not use if pregnant or nursing."))
    sections.append(("regular", "Poison Center 1-800-222-1222"))
    sections.append(("regular", "Warning: Smoking or vaping is hazardous to health."))

    # SECTION 3: Processor info
    sections.append(("separator",))
    sections.append(("regular", f"{PROCESSOR_NAME} · {PROCESSOR_CITY}, NY"))
    sections.append(("regular", f"OCM Lic #: {PROCESSOR_LICENSE}"))
    sections.append(("regular", PROCESSOR_EMAIL))

    # SECTION 4: Ingredients
    sections.append(("separator",))
    ingredients = PRODUCT_INGREDIENTS.get(product, PRODUCT_INGREDIENTS["preroll"])
    sections.append(("regular", f"Ingredients: {ingredients}"))

    # SECTION 5: Batch data
    sections.append(("separator",))
    sections.append(("regular", f"THC: {thc:.1f}% | CBD: {cbd:.1f}%"))
    sections.append(("regular", f"LOT: {lot}"))
    sections.append(("regular", f"EXP: {exp}"))
    sections.append(("regular", "Store in a cool, dry place."))

    # SECTION 6: QR + terpene profile (rendered separately below)
    sections.append(("separator",))

    # --- Calculate height ---
    # Create a temporary image to measure text
    tmp_img = Image.new("RGB", (width, 2000), "white")
    tmp_draw = ImageDraw.Draw(tmp_img)

    y_cursor = margin
    line_spacing = pt_to_px(2)
    separator_spacing = pt_to_px(3)

    def wrapped_text_height(draw_obj, text, font, max_width):
        """Calculate height of wrapped text."""
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = draw_obj.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        if not lines:
            lines = [""]
        line_h = draw_obj.textbbox((0, 0), "Ag", font=font)[3]
        return line_h * len(lines) + line_spacing * (len(lines) - 1), lines

    for section in sections:
        if section[0] == "separator":
            y_cursor += separator_spacing
        elif section[0] == "bold" and len(section) == 4:
            # Combined bold prefix + regular text
            full_text = section[1] + section[3]
            h, _ = wrapped_text_height(tmp_draw, full_text, font_6, content_width)
            y_cursor += h + line_spacing
        else:
            style, text = section[0], section[1]
            font = font_6_bold if style == "bold" else font_6
            h, _ = wrapped_text_height(tmp_draw, text, font, content_width)
            y_cursor += h + line_spacing

    # QR + terpene section
    terpene_lines = ["TERPENE PROFILE:"] + [f"{k}: {v}%" for k, v in terpenes.items()]
    terpene_text_h = (pt_to_px(6) + line_spacing) * len(terpene_lines)
    qr_section_h = max(qr_size, terpene_text_h)
    y_cursor += qr_section_h + mm_to_px(1)

    # "Scan for COA" label
    y_cursor += pt_to_px(6) + line_spacing

    total_height = y_cursor + margin

    # --- Render ---
    img = Image.new("RGB", (width, total_height), "white")
    draw = ImageDraw.Draw(img)

    # Border
    draw.rectangle([0, 0, width - 1, total_height - 1], outline="black", width=2)

    y_cursor = margin

    def draw_wrapped_text(draw_obj, text, font, x, y, max_width, fill="black"):
        """Draw word-wrapped text, return new y position."""
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = draw_obj.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        if not lines:
            lines = [""]

        line_h = draw_obj.textbbox((0, 0), "Ag", font=font)[3]
        for line in lines:
            draw_obj.text((x, y), line, fill=fill, font=font)
            y += line_h + line_spacing
        return y

    def draw_warning_line(draw_obj, bold_prefix, regular_text, x, y, max_width):
        """Draw a line with bold prefix and regular continuation, word-wrapped."""
        full_text = bold_prefix + regular_text
        words = full_text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = draw_obj.textbbox((0, 0), test_line, font=font_6)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        line_h = draw_obj.textbbox((0, 0), "Ag", font=font_6)[3]
        for i, line in enumerate(lines):
            if i == 0:
                # First line: bold prefix then regular
                prefix_bbox = draw_obj.textbbox((0, 0), bold_prefix, font=font_6_bold)
                prefix_w = prefix_bbox[2] - prefix_bbox[0]
                draw_obj.text((x, y), bold_prefix, fill="black", font=font_6_bold)
                remainder = line[len(bold_prefix):]
                draw_obj.text((x + prefix_w, y), remainder, fill="black", font=font_6)
            else:
                draw_obj.text((x, y), line, fill="black", font=font_6)
            y += line_h + line_spacing
        return y

    def draw_separator(draw_obj, y, x_start, x_end):
        """Draw a thin hairline rule."""
        y += pt_to_px(1)
        draw_obj.line([(x_start, y), (x_end, y)], fill="#999999", width=1)
        y += pt_to_px(2)
        return y

    for section in sections:
        if section[0] == "separator":
            y_cursor = draw_separator(draw, y_cursor, margin, width - margin)
        elif section[0] == "bold" and len(section) == 4:
            y_cursor = draw_warning_line(
                draw, section[1], section[3], margin, y_cursor, content_width
            )
        else:
            style, text = section[0], section[1]
            font = font_6_bold if style == "bold" else font_6
            y_cursor = draw_wrapped_text(draw, text, font, margin, y_cursor, content_width)

    # QR Code
    qr = qrcode.QRCode(version=1, box_size=4, border=1)
    # COA URL — placeholder, would be batch-specific in production
    coa_url = f"https://buypablo.com/coa/{lot}"
    qr.add_data(coa_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)
    img.paste(qr_img, (margin, y_cursor))

    # "Scan for COA" under QR
    scan_font = ImageFont.truetype(ARIAL, pt_to_px(5))
    draw.text((margin, y_cursor + qr_size + pt_to_px(1)), "Scan for COA", fill="black", font=scan_font)

    # Terpene profile to the right of QR
    terp_x = margin + qr_size + mm_to_px(2)
    terp_y = y_cursor
    draw.text((terp_x, terp_y), "TERPENE PROFILE:", fill="black", font=font_6_bold)
    terp_y += pt_to_px(6) + line_spacing
    for name, pct in terpenes.items():
        draw.text((terp_x, terp_y), f"{name}: {pct}%", fill="black", font=font_6)
        terp_y += pt_to_px(6) + line_spacing

    path = os.path.join(output_dir, "sticker_back_compliance.png")
    img.save(path, dpi=(DPI, DPI))
    return path


def create_combined_preview(front_path: str, back_path: str, output_dir: str) -> str:
    """Create a side-by-side preview of both stickers at actual relative size."""
    front = Image.open(front_path)
    back = Image.open(back_path)

    padding = mm_to_px(5)
    total_w = front.width + back.width + padding * 3
    total_h = max(front.height, back.height) + padding * 2

    preview = Image.new("RGB", (total_w, total_h), "#F0F0F0")

    # Center vertically
    front_y = (total_h - front.height) // 2
    back_y = (total_h - back.height) // 2

    preview.paste(front, (padding, front_y))
    preview.paste(back, (padding * 2 + front.width, back_y))

    # Labels
    label_font = ImageFont.truetype(ARIAL_BOLD, pt_to_px(8))
    draw = ImageDraw.Draw(preview)
    draw.text((padding, padding // 2), "FRONT POTENCY", fill="#666666", font=label_font)
    draw.text((padding * 2 + front.width, padding // 2), "BACK COMPLIANCE", fill="#666666", font=label_font)

    path = os.path.join(output_dir, "sticker_preview_combined.png")
    preview.save(path, dpi=(DPI, DPI))
    return path


def main():
    parser = argparse.ArgumentParser(description="PABLO Compliance Sticker Generator")
    parser.add_argument("--thc", type=float, default=32.4, help="THC percentage (default: 32.4)")
    parser.add_argument("--cbd", type=float, default=0.1, help="CBD percentage (default: 0.1)")
    parser.add_argument("--lot", type=str, default="PM-2026-0301A", help="Lot number")
    parser.add_argument("--exp", type=str, default="09/01/2026", help="Expiration date MM/DD/YYYY")
    parser.add_argument("--warning", type=str, default="B", choices=["A", "B", "C"],
                        help="Rotating warning version (A, B, or C)")
    parser.add_argument("--terpenes", type=str,
                        default="β-Caryophyllene:1.2,Limonene:0.9,Myrcene:0.8",
                        help="Terpene profile as 'Name:Pct,Name:Pct'")
    parser.add_argument("--product", type=str, default="preroll",
                        choices=list(PRODUCT_INGREDIENTS.keys()),
                        help="Product type (affects ingredient list)")
    parser.add_argument("--output", type=str, default=None, help="Output directory")

    args = parser.parse_args()

    # Parse terpenes
    terpenes = {}
    if args.terpenes:
        for pair in args.terpenes.split(","):
            name, pct = pair.rsplit(":", 1)
            terpenes[name.strip()] = float(pct.strip())

    # Output directory
    output_dir = args.output or os.path.join(os.path.dirname(__file__), "..", "output", "stickers")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Generating PABLO compliance stickers...")
    print(f"  Product: {args.product}")
    print(f"  THC: {args.thc}% | CBD: {args.cbd}%")
    print(f"  LOT: {args.lot} | EXP: {args.exp}")
    print(f"  Warning version: {args.warning}")
    print(f"  Terpenes: {terpenes}")
    print()

    front_path = create_front_potency_sticker(args.thc, args.cbd, output_dir)
    print(f"  ✓ Front potency sticker: {front_path}")

    back_path = create_back_compliance_sticker(
        args.thc, args.cbd, args.lot, args.exp,
        args.warning, terpenes, args.product, output_dir
    )
    print(f"  ✓ Back compliance sticker: {back_path}")

    preview_path = create_combined_preview(front_path, back_path, output_dir)
    print(f"  ✓ Combined preview: {preview_path}")

    print()
    print(f"All stickers saved to: {output_dir}")
    print(f"Resolution: {DPI} DPI (print-ready)")


if __name__ == "__main__":
    main()
