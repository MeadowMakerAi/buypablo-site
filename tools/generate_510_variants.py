#!/usr/bin/env python3
"""
PABLO 510 Variant Generator — Option B (luminosity-blend)
Per Chat's brief: preserve 3D lighting by reconstructing each band from the original
luminosity channel × target RGB. Beats naive HSV swap on photorealistic renders.

Master render: _pablo_510_master.png (Pineapple Marker 510, locked immutable)
Bands detected:
  - Strain badge:  y=1558-1734, x=552-1205
  - Compliance:    y=1826-2064, x=372-1328

Output: /assets/images/pablo_510_<slug>_ny.jpeg  (687x1024)
"""

import os
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.dirname(BASE_DIR)
MASTER = os.path.join(BASE_DIR, "_pablo_510_master.png")
BADGES_DIR = os.path.join(SITE_DIR, "assets/images/badges")
OUT_DIR = os.path.join(SITE_DIR, "assets/images")

# Full-resolution zones (1696x2528 master)
STRAIN_BAND = {"y": (1540, 1750), "x": (487, 1334)}       # pink strain pill area
COMPLIANCE_BAND = {"y": (1810, 2080), "x": (0, 1696)}      # edge-to-edge pink strip

# Per-SKU luminosity multiplier — tuned for each flavor's natural brightness
# Bright targets (yellow, orange) need lower mult; dark targets (purple, green) need higher
FLAVORS = {
    "pineapple_marker":  {"hex": "#EA698C", "lum": 1.00, "badge": "badge_pineapple_marker.png"},
    "pie_face":          {"hex": "#EE2737", "lum": 1.50, "badge": "badge_pie_face.png"},
    "mangonada":         {"hex": "#FC4C02", "lum": 1.35, "badge": "badge_mangonada.png"},
    "marmalade":         {"hex": "#FCA311", "lum": 1.25, "badge": "badge_marmalade.png"},
    "terp_taxi":         {"hex": "#FFCD00", "lum": 1.10, "badge": "badge_terp_taxi.png"},
    "watermelon_gusher": {"hex": "#00855A", "lum": 1.90, "badge": "badge_watermelon_gusher.png"},
    "sunday_grapes":     {"hex": "#6E3FA3", "lum": 1.95, "badge": "badge_sundae_grapes.png"},
}

def hex_to_rgb(h):
    return tuple(int(h.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

def luminosity_blend_band(arr, band, target_rgb, lum_mult):
    """Reconstruct a band using target_rgb × original luminosity channel.
    Preserves the 3D highlights and shadows baked into the original render."""
    y1, y2 = band["y"]
    x1, x2 = band["x"]
    tr, tg, tb = target_rgb

    region = arr[y1:y2, x1:x2, :3].astype(float)
    lum = (0.299*region[:,:,0] + 0.587*region[:,:,1] + 0.114*region[:,:,2]) / 255.0

    # Boost luminosity to compensate for the original pink being brighter than most targets
    lum_scaled = np.clip(lum * lum_mult, 0, 1)

    out = np.zeros_like(region)
    out[:,:,0] = np.clip(tr * lum_scaled, 0, 255)
    out[:,:,1] = np.clip(tg * lum_scaled, 0, 255)
    out[:,:,2] = np.clip(tb * lum_scaled, 0, 255)

    # Mask: only blend where the original region was pinkish (avoid touching white text, logos, etc.)
    orig_r, orig_g, orig_b = region[:,:,0], region[:,:,1], region[:,:,2]
    pink_mask = (orig_r > 150) & (orig_g < 180) & (orig_r > orig_g + 30)
    result = region.copy()
    result[pink_mask] = out[pink_mask]

    arr[y1:y2, x1:x2, :3] = result.astype(np.uint8)
    return arr

def composite_flavor_badge(img, badge_path):
    """Paste the flat flavor badge over the strain badge region. Keep it simple — no lighting transfer,
    which was making the color muddy."""
    if not os.path.exists(badge_path):
        print(f"  [warn] missing badge: {badge_path}")
        return img
    badge = Image.open(badge_path).convert("RGBA")
    x1, y1, x2, y2 = 487, 1540, 1334, 1750
    resized = badge.resize((x2 - x1, y2 - y1), Image.LANCZOS)
    img.paste(resized, (x1, y1), resized)
    return img

def generate(slug, spec):
    master = Image.open(MASTER).convert("RGBA")
    original_arr = np.array(master).copy()  # snapshot for lighting transfer
    arr = np.array(master)
    target = hex_to_rgb(spec["hex"])
    lum_mult = spec["lum"]

    if slug != "pineapple_marker":
        arr = luminosity_blend_band(arr, COMPLIANCE_BAND, target, lum_mult)
        arr = luminosity_blend_band(arr, STRAIN_BAND, target, lum_mult)

    img = Image.fromarray(arr)

    badge_path = os.path.join(BADGES_DIR, spec["badge"])
    if slug != "pineapple_marker":
        img = composite_flavor_badge(img, badge_path)

    out_path = os.path.join(OUT_DIR, f"pablo_510_{slug}_ny.jpeg")
    img.convert("RGB").resize((687, 1024), Image.LANCZOS).save(out_path, "JPEG", quality=95)
    print(f"  [ok] {slug} -> {out_path}")

def main():
    print("Generating PABLO 510 variants via luminosity-blend...")
    for slug, spec in FLAVORS.items():
        generate(slug, spec)
    print("Done.")

if __name__ == "__main__":
    main()
