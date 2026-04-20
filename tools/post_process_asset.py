#!/usr/bin/env python3
"""
PABLO Asset Post-Processor
Takes raw Gemini output images and prepares them for web use.

Usage:
    python3 post_process_asset.py input.png                    # Auto-process with defaults
    python3 post_process_asset.py input.png --shadow            # Add drop shadow
    python3 post_process_asset.py input.png --crop-white        # Trim white borders
    python3 post_process_asset.py input.png --resize 800x600   # Resize to dimensions
    python3 post_process_asset.py input.png --web               # Full web optimization (crop + shadow + resize + compress)
    python3 post_process_asset.py input.png --hero              # Hero image preset (crop + 1920px wide + compress)
    python3 post_process_asset.py input.png --card              # Product card preset (crop + shadow + 600px wide + compress)
    python3 post_process_asset.py input.png --badge             # Badge strip preset (crop + 1400px wide + compress)

Output: processed images in ./output/processed/ (or --output path)
"""

import argparse
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps


def crop_white_background(img, threshold=240, padding=20):
    """Remove white/near-white borders from an image."""
    # Convert to RGB if needed
    if img.mode == "RGBA":
        # Create white background composite for analysis
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        analyze = bg
    else:
        analyze = img.convert("RGB")

    pixels = analyze.load()
    w, h = analyze.size

    # Find bounding box of non-white content
    left, top, right, bottom = w, h, 0, 0

    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            if r < threshold or g < threshold or b < threshold:
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    if left >= right or top >= bottom:
        return img  # No content found or all white

    # Add padding
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(w, right + padding)
    bottom = min(h, bottom + padding)

    return img.crop((left, top, right, bottom))


def add_drop_shadow(img, offset=(8, 8), shadow_color=(0, 0, 0, 80), blur_radius=15, bg_color=(255, 255, 255, 255)):
    """Add a drop shadow to an image with transparency or white background."""
    # Ensure RGBA
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Create a larger canvas for the shadow
    expand = blur_radius * 2 + max(abs(offset[0]), abs(offset[1]))
    new_w = img.width + expand * 2
    new_h = img.height + expand * 2

    # Shadow layer
    shadow = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))

    # Create shadow mask from image alpha or from non-white pixels
    alpha = img.split()[3]

    # If the image doesn't have meaningful alpha (all opaque), create mask from white detection
    alpha_data = list(alpha.getdata())
    if sum(1 for a in alpha_data if a > 250) / len(alpha_data) > 0.95:
        # Mostly opaque — create mask from non-white pixels
        rgb = img.convert("RGB")
        pixels = rgb.load()
        mask = Image.new("L", img.size, 0)
        mask_pixels = mask.load()
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                if r < 245 or g < 245 or b < 245:
                    mask_pixels[x, y] = 255
        alpha = mask

    # Place shadow color where the product is
    shadow_fill = Image.new("RGBA", img.size, shadow_color)
    shadow_positioned = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
    shadow_positioned.paste(shadow_fill, (expand + offset[0], expand + offset[1]), alpha)

    # Blur the shadow
    shadow_blurred = shadow_positioned.filter(ImageFilter.GaussianBlur(blur_radius))

    # Create result with background
    result = Image.new("RGBA", (new_w, new_h), bg_color)
    result = Image.alpha_composite(result, shadow_blurred)

    # Paste original image on top
    result.paste(img, (expand, expand), img.split()[3] if img.mode == "RGBA" else None)

    return result


def resize_image(img, target_size):
    """Resize image to target dimensions, maintaining aspect ratio.
    target_size can be 'WxH' (exact), 'Ww' (width only), or 'Hh' (height only).
    """
    if "x" in target_size.lower():
        parts = target_size.lower().split("x")
        target_w, target_h = int(parts[0]), int(parts[1])
        img.thumbnail((target_w, target_h), Image.LANCZOS)
    elif target_size.endswith("w"):
        target_w = int(target_size[:-1])
        ratio = target_w / img.width
        target_h = int(img.height * ratio)
        img = img.resize((target_w, target_h), Image.LANCZOS)
    elif target_size.endswith("h"):
        target_h = int(target_size[:-1])
        ratio = target_h / img.height
        target_w = int(img.width * ratio)
        img = img.resize((target_w, target_h), Image.LANCZOS)
    else:
        # Assume width-only
        target_w = int(target_size)
        ratio = target_w / img.width
        target_h = int(img.height * ratio)
        img = img.resize((target_w, target_h), Image.LANCZOS)

    return img


def optimize_for_web(img, output_path, quality=85):
    """Save image optimized for web — JPEG for photos, PNG for graphics with transparency."""
    if img.mode == "RGBA":
        # Check if we actually need alpha
        alpha = img.split()[3]
        if alpha.getextrema() == (255, 255):
            # Fully opaque — save as JPEG
            img = img.convert("RGB")
            if not output_path.lower().endswith(".jpg"):
                output_path = os.path.splitext(output_path)[0] + ".jpg"
            img.save(output_path, "JPEG", quality=quality, optimize=True)
        else:
            if not output_path.lower().endswith(".png"):
                output_path = os.path.splitext(output_path)[0] + ".png"
            img.save(output_path, "PNG", optimize=True)
    else:
        if not output_path.lower().endswith(".jpg"):
            output_path = os.path.splitext(output_path)[0] + ".jpg"
        img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=quality, optimize=True)

    return output_path


def process_image(input_path, operations, output_dir):
    """Apply a sequence of operations to an image."""
    img = Image.open(input_path)
    basename = os.path.splitext(os.path.basename(input_path))[0]

    print(f"  Input: {input_path} ({img.width}x{img.height}, {img.mode})")

    for op, params in operations:
        if op == "crop_white":
            img = crop_white_background(img)
            print(f"  ✓ Cropped white borders → {img.width}x{img.height}")
        elif op == "shadow":
            img = add_drop_shadow(img)
            print(f"  ✓ Added drop shadow → {img.width}x{img.height}")
        elif op == "resize":
            img = resize_image(img, params)
            print(f"  ✓ Resized → {img.width}x{img.height}")

    output_path = os.path.join(output_dir, f"{basename}_processed.png")
    output_path = optimize_for_web(img, output_path)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"  ✓ Saved: {output_path} ({size_kb:.0f} KB)")

    return output_path


# --- Presets ---

PRESETS = {
    "hero": [("crop_white", None), ("resize", "1920w")],
    "card": [("crop_white", None), ("shadow", None), ("resize", "600w")],
    "badge": [("crop_white", None), ("resize", "1400w")],
    "family": [("crop_white", None), ("shadow", None), ("resize", "1200w")],
    "web": [("crop_white", None), ("shadow", None), ("resize", "800w")],
}


def main():
    parser = argparse.ArgumentParser(description="PABLO Asset Post-Processor")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("--crop-white", action="store_true", help="Trim white borders")
    parser.add_argument("--shadow", action="store_true", help="Add drop shadow")
    parser.add_argument("--resize", type=str, help="Resize (e.g., '800x600', '1920w', '600h')")
    parser.add_argument("--hero", action="store_true", help="Hero image preset")
    parser.add_argument("--card", action="store_true", help="Product card preset")
    parser.add_argument("--badge", action="store_true", help="Badge strip preset")
    parser.add_argument("--family", action="store_true", help="Family shot preset")
    parser.add_argument("--web", action="store_true", help="General web preset")
    parser.add_argument("--output", type=str, default=None, help="Output directory")
    args = parser.parse_args()

    output_dir = args.output or os.path.join(os.path.dirname(__file__), "..", "output", "processed")
    os.makedirs(output_dir, exist_ok=True)

    # Determine operations
    operations = []

    if args.hero:
        operations = PRESETS["hero"]
    elif args.card:
        operations = PRESETS["card"]
    elif args.badge:
        operations = PRESETS["badge"]
    elif args.family:
        operations = PRESETS["family"]
    elif args.web:
        operations = PRESETS["web"]
    else:
        if args.crop_white:
            operations.append(("crop_white", None))
        if args.shadow:
            operations.append(("shadow", None))
        if args.resize:
            operations.append(("resize", args.resize))

    if not operations:
        print("No operations specified. Use --hero, --card, --badge, --family, --web, or individual flags.")
        print("Run with --help for usage.")
        sys.exit(1)

    print(f"Processing asset...")
    process_image(args.input, operations, output_dir)


if __name__ == "__main__":
    main()
