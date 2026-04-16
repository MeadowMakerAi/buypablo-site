#!/usr/bin/env python3
"""
PABLO Flavor Badges Generator
Generates pixel-perfect flavor badge strip for web use.
No AI needed — these are colored pill shapes with white text.

Usage:
    python3 generate_flavor_badges.py                   # Horizontal strip (default)
    python3 generate_flavor_badges.py --layout grid      # 2-row grid
    python3 generate_flavor_badges.py --layout vertical  # Vertical stack
"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont

from brand_config import FLAVORS as _FLAVORS_RAW

# Derive (UPPER_NAME, color) tuples from canonical config
FLAVORS = [(f["name"].upper(), f["color"]) for f in _FLAVORS_RAW]

# Try Bebas Neue first (brand font), fall back to Arial Bold
FONT_PATHS = [
    "/Library/Fonts/BebasNeue-Bold.ttf",
    "/Library/Fonts/BebasNeue Bold.ttf",
    "/Users/alexanderclaiborne/Library/Fonts/BebasNeue-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]


def get_font(size):
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def draw_pill_badge(draw, x, y, width, height, color, text, font, corner_radius=None):
    """Draw a rounded-rectangle (pill) badge with centered white text."""
    if corner_radius is None:
        corner_radius = height // 2  # Full pill shape

    rgb = hex_to_rgb(color)

    # Draw rounded rectangle
    draw.rounded_rectangle(
        [x, y, x + width, y + height],
        radius=corner_radius,
        fill=rgb,
    )

    # Subtle crosshatch texture overlay (very light, 10% opacity effect)
    # We'll skip actual crosshatch and use a very subtle darker border instead
    # for a cleaner web look
    darker = tuple(max(0, c - 20) for c in rgb)
    draw.rounded_rectangle(
        [x, y, x + width, y + height],
        radius=corner_radius,
        outline=darker,
        width=2,
    )

    # Center text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = x + (width - text_w) // 2
    text_y = y + (height - text_h) // 2 - bbox[1]  # Adjust for baseline

    # Subtle text shadow for depth
    draw.text((text_x + 1, text_y + 1), text, fill=(0, 0, 0, 40), font=font)
    draw.text((text_x, text_y), text, fill="white", font=font)


def generate_horizontal_strip(output_dir, scale=1):
    """Generate a single horizontal row of all 7 badges."""
    badge_w = int(220 * scale)
    badge_h = int(70 * scale)
    spacing = int(20 * scale)
    padding = int(30 * scale)
    font_size = int(28 * scale)

    total_w = len(FLAVORS) * badge_w + (len(FLAVORS) - 1) * spacing + 2 * padding
    total_h = badge_h + 2 * padding

    img = Image.new("RGBA", (total_w, total_h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = get_font(font_size)

    for i, (name, color) in enumerate(FLAVORS):
        x = padding + i * (badge_w + spacing)
        y = padding
        draw_pill_badge(draw, x, y, badge_w, badge_h, color, name, font)

    path = os.path.join(output_dir, "flavor_badges_horizontal.png")
    img.save(path)

    # Also save a white-background version for web
    img_white = Image.new("RGB", (total_w, total_h), (255, 255, 255))
    img_white.paste(img, mask=img.split()[3])
    path_white = os.path.join(output_dir, "flavor_badges_horizontal_white.png")
    img_white.save(path_white, quality=95)

    return path, path_white


def generate_grid(output_dir, scale=1):
    """Generate a 2-row grid (4 top, 3 bottom centered)."""
    badge_w = int(260 * scale)
    badge_h = int(75 * scale)
    spacing_x = int(20 * scale)
    spacing_y = int(18 * scale)
    padding = int(30 * scale)
    font_size = int(30 * scale)

    cols_top = 4
    cols_bottom = 3

    row_w = cols_top * badge_w + (cols_top - 1) * spacing_x
    total_w = row_w + 2 * padding
    total_h = 2 * badge_h + spacing_y + 2 * padding

    img = Image.new("RGBA", (total_w, total_h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = get_font(font_size)

    # Top row — 4 badges
    for i in range(cols_top):
        name, color = FLAVORS[i]
        x = padding + i * (badge_w + spacing_x)
        y = padding
        draw_pill_badge(draw, x, y, badge_w, badge_h, color, name, font)

    # Bottom row — 3 badges, centered
    bottom_row_w = cols_bottom * badge_w + (cols_bottom - 1) * spacing_x
    bottom_offset = (total_w - bottom_row_w) // 2
    for i in range(cols_bottom):
        name, color = FLAVORS[cols_top + i]
        x = bottom_offset + i * (badge_w + spacing_x)
        y = padding + badge_h + spacing_y
        draw_pill_badge(draw, x, y, badge_w, badge_h, color, name, font)

    path = os.path.join(output_dir, "flavor_badges_grid.png")
    img.save(path)

    img_white = Image.new("RGB", (total_w, total_h), (255, 255, 255))
    img_white.paste(img, mask=img.split()[3])
    path_white = os.path.join(output_dir, "flavor_badges_grid_white.png")
    img_white.save(path_white, quality=95)

    return path, path_white


def generate_vertical(output_dir, scale=1):
    """Generate a vertical stack of all 7 badges."""
    badge_w = int(300 * scale)
    badge_h = int(65 * scale)
    spacing = int(12 * scale)
    padding = int(25 * scale)
    font_size = int(28 * scale)

    total_w = badge_w + 2 * padding
    total_h = len(FLAVORS) * badge_h + (len(FLAVORS) - 1) * spacing + 2 * padding

    img = Image.new("RGBA", (total_w, total_h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = get_font(font_size)

    for i, (name, color) in enumerate(FLAVORS):
        x = padding
        y = padding + i * (badge_h + spacing)
        draw_pill_badge(draw, x, y, badge_w, badge_h, color, name, font)

    path = os.path.join(output_dir, "flavor_badges_vertical.png")
    img.save(path)

    img_white = Image.new("RGB", (total_w, total_h), (255, 255, 255))
    img_white.paste(img, mask=img.split()[3])
    path_white = os.path.join(output_dir, "flavor_badges_vertical_white.png")
    img_white.save(path_white, quality=95)

    return path, path_white


def main():
    parser = argparse.ArgumentParser(description="PABLO Flavor Badges Generator")
    parser.add_argument("--layout", choices=["horizontal", "grid", "vertical", "all"],
                        default="all", help="Badge layout style")
    parser.add_argument("--scale", type=float, default=2.0,
                        help="Scale factor (2.0 = retina/high-res)")
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    output_dir = args.output or os.path.join(os.path.dirname(__file__), "..", "output", "badges")
    os.makedirs(output_dir, exist_ok=True)

    layouts = [args.layout] if args.layout != "all" else ["horizontal", "grid", "vertical"]

    for layout in layouts:
        print(f"Generating {layout} layout (scale={args.scale}x)...")
        if layout == "horizontal":
            path, path_white = generate_horizontal_strip(output_dir, args.scale)
        elif layout == "grid":
            path, path_white = generate_grid(output_dir, args.scale)
        elif layout == "vertical":
            path, path_white = generate_vertical(output_dir, args.scale)

        img = Image.open(path_white)
        print(f"  ✓ {path_white} ({img.width}x{img.height})")

    print(f"\nAll badges saved to: {output_dir}")


if __name__ == "__main__":
    main()
