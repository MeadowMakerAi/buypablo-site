#!/usr/bin/env python3
"""Quick analyzer: finds pink-pixel bounding boxes in the approved Pineapple Marker template."""

import numpy as np
from PIL import Image

SRC = "/Users/alexanderclaiborne/workspaces/pablo/site/assets/images/pablo_aio_pineapple_marker_ny.jpeg"
TARGET_HEX = "#EE3680"
TOL = 40  # Tolerance for pink detection

def hex_to_rgb(h):
    return tuple(int(h.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

img = Image.open(SRC).convert("RGB")
arr = np.array(img)
h, w, _ = arr.shape
print(f"Image: {w}x{h}")

tr, tg, tb = hex_to_rgb(TARGET_HEX)
mask = (
    (np.abs(arr[:,:,0].astype(int) - tr) < TOL) &
    (np.abs(arr[:,:,1].astype(int) - tg) < TOL) &
    (np.abs(arr[:,:,2].astype(int) - tb) < TOL)
)
print(f"Pink pixels: {mask.sum()}")

ys, xs = np.where(mask)
if len(xs) > 0:
    print(f"Pink bbox: x={xs.min()}-{xs.max()}, y={ys.min()}-{ys.max()}")
    # Find the connected bands by y-coordinate clustering
    from collections import Counter
    y_counts = Counter(ys)
    sorted_rows = sorted(y_counts.items())
    # Identify gaps to find separate pink bands
    gaps = []
    prev_y = sorted_rows[0][0]
    for y, _ in sorted_rows[1:]:
        if y - prev_y > 5:
            gaps.append((prev_y, y))
        prev_y = y
    print(f"Y-gaps between pink bands: {gaps}")

# Sample a few known regions for color verification
print(f"\nSamples at key points:")
for name, (x, y) in [
    ("upper-center (logo area)", (w//2, 150)),
    ("middle (FLAVORS text)", (w//2, 520)),
    ("flavor badge center", (w//2, 650)),
    ("compliance strip", (w//2, 800)),
    ("warning text area", (w//2, 920)),
]:
    print(f"  {name} ({x},{y}): {tuple(arr[y, x])}")
