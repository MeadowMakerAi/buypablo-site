#!/usr/bin/env python3
"""Consolidate Pablo product renders into a single organized directory for web use."""

import os
import shutil
from pathlib import Path
from PIL import Image

# Paths
BASE = Path.home() / "workspaces/pablo/site/assets/images"
DOWNLOADS = Path.home() / "Downloads/PABLO NY WEB RENDERS "  # trailing space
AIO_DIR = BASE / "PABLO AIO WEB RENDERS"
TARGET = BASE / "renders"

TARGET.mkdir(exist_ok=True)

# Mapping: target_filename -> source_path
# Flavor slug mapping for 510 PNGs from Downloads
FLAVOR_MAP_510 = {
    "510 Flavors Pineapple Marker.png": "flavors_510_pineapple-marker",
    "510 Flavors Sunday Grape.png": "flavors_510_sundae-grapes",  # Note: source says "Sunday Grape"
    "510 Flavors Terp Taxi.png": "flavors_510_terp-taxi",
    "510 Flavors Mangonada.png": "flavors_510_mangonada",
    "510 Flavors Marmalade.png": "flavors_510_marmalade",
    "510 Flavors Pie Face.png": "flavors_510_pie-face",
    "510 Flavors Watermelon Gusher.png": "flavors_510_watermelon-gusher",
}

# AIO JPEGs
FLAVOR_MAP_AIO = {
    "pablo_aio_pineapple_marker_ny.jpeg": "flavors_aio_pineapple-marker",
    "pablo_aio_sundae_grapes_ny.jpeg": "flavors_aio_sundae-grapes",
    "pablo_aio_terp_taxi_ny.jpeg": "flavors_aio_terp-taxi",
    "pablo_aio_mangonada_ny.jpeg": "flavors_aio_mangonada",
    "pablo_aio_marmalade_ny.jpeg": "flavors_aio_marmalade",
    "pablo_aio_pie_face_ny.jpeg": "flavors_aio_pie-face",
    "pablo_aio_watermelon_gusher_ny.jpeg": "flavors_aio_watermelon-gusher",
}

MAX_WIDTH = 1200
JPEG_QUALITY = 85

results = []


def process_image(src_path: Path, target_stem: str, source_label: str):
    """Copy image to renders/, resize if >1200px wide, save as JPEG."""
    target_path = TARGET / f"{target_stem}.jpg"

    img = Image.open(src_path)
    orig_w, orig_h = img.size

    if img.mode in ("RGBA", "P"):
        # Convert transparency to white background for JPEG
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[3])
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")

    if orig_w > MAX_WIDTH:
        ratio = MAX_WIDTH / orig_w
        new_h = int(orig_h * ratio)
        img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)

    final_w, final_h = img.size
    img.save(target_path, "JPEG", quality=JPEG_QUALITY)

    file_size = target_path.stat().st_size
    results.append({
        "filename": target_path.name,
        "source": source_label,
        "orig_dims": f"{orig_w}x{orig_h}",
        "final_dims": f"{final_w}x{final_h}",
        "size_kb": round(file_size / 1024, 1),
    })


# 1. Process 510 Flavors PNGs from Downloads (high-quality, prefer these)
for src_name, target_stem in FLAVOR_MAP_510.items():
    src = DOWNLOADS / src_name
    if src.exists():
        process_image(src, target_stem, "Downloads/510 PNGs")
    else:
        print(f"WARNING: Missing {src}")

# 2. Process Live Resin 510 from Downloads
lr_src = DOWNLOADS / "Live Resin 510.png"
if lr_src.exists():
    process_image(lr_src, "live-resin_510_sour-diesel", "Downloads/Live Resin 510")
else:
    print(f"WARNING: Missing {lr_src}")

# 3. Process AIO JPEGs
for src_name, target_stem in FLAVOR_MAP_AIO.items():
    src = AIO_DIR / src_name
    if src.exists():
        process_image(src, target_stem, "AIO WEB RENDERS")
    else:
        print(f"WARNING: Missing {src}")

# 4. Process the panel crop (live resin sour diesel winner)
panel_src = BASE / "pablo_510_live_resin_sour_diesel_winner.png"
if panel_src.exists():
    process_image(panel_src, "live-resin_510_sour-diesel-panel", "assets/images root")
else:
    print(f"WARNING: Missing {panel_src}")

# Print summary table
print(f"\n{'='*90}")
print(f"Consolidated {len(results)} renders into {TARGET}")
print(f"{'='*90}")
print(f"{'Filename':<45} {'Source':<22} {'Original':<12} {'Final':<12} {'Size':>8}")
print(f"{'-'*45} {'-'*22} {'-'*12} {'-'*12} {'-'*8}")
for r in results:
    print(f"{r['filename']:<45} {r['source']:<22} {r['orig_dims']:<12} {r['final_dims']:<12} {r['size_kb']:>7.1f}KB")

total_kb = sum(r["size_kb"] for r in results)
print(f"\nTotal: {len(results)} files, {total_kb:.0f}KB ({total_kb/1024:.1f}MB)")
