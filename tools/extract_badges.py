#!/usr/bin/env python3
"""Extract PNG from the user's SVG badge composite and split into 7 individual badges."""
import base64
import re
from PIL import Image
import io
import os

SVG_PATH = "/Users/alexanderclaiborne/Downloads/pablo_flavor_badges.svg"
OUT_DIR = "/Users/alexanderclaiborne/workspaces/pablo/site/assets/images/badges"
os.makedirs(OUT_DIR, exist_ok=True)

with open(SVG_PATH, "r") as f:
    svg = f.read()

# Find base64 PNG
match = re.search(r'xlink:href="data:image/png;base64,([^"]+)"', svg)
if not match:
    raise RuntimeError("No base64 PNG found in SVG")

png_data = base64.b64decode(match.group(1))
img = Image.open(io.BytesIO(png_data))
print(f"Extracted PNG: {img.size} mode={img.mode}")

# Save full for reference
img.save(os.path.join(OUT_DIR, "_full_composite.png"))

# Split into 7 horizontal bands
w, h = img.size
band_h = h / 7
flavors = [
    "pineapple_marker",
    "sundae_grapes",
    "terp_taxi",
    "mangonada",
    "marmalade",
    "pie_face",
    "watermelon_gusher",
]
for i, name in enumerate(flavors):
    y1 = int(i * band_h)
    y2 = int((i + 1) * band_h)
    crop = img.crop((0, y1, w, y2))
    path = os.path.join(OUT_DIR, f"badge_{name}.png")
    crop.save(path)
    print(f"  {name}: {crop.size} → {path}")

print("Done.")
