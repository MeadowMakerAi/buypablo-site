#!/usr/bin/env python3
"""Crop the flavor badge region from the template so we can see exact dimensions."""
from PIL import Image

SRC = "/Users/alexanderclaiborne/workspaces/pablo/site/assets/images/pablo_aio_pineapple_marker_ny.jpeg"
img = Image.open(SRC)
# Full badge area: crop generously
crop = img.crop((180, 600, 540, 760))
crop.save("/tmp/badge_crop.png")
print(f"Saved crop: {crop.size}")

# Print white pixel locations in this region
import numpy as np
arr = np.array(crop.convert("RGB"))
white = (arr[:,:,0] > 200) & (arr[:,:,1] > 200) & (arr[:,:,2] > 200)
ys, xs = np.where(white)
if len(xs) > 0:
    print(f"White pixels in crop: x={xs.min()}-{xs.max()}, y={ys.min()}-{ys.max()}")
    print(f"In full-image coords: x={xs.min()+180}-{xs.max()+180}, y={ys.min()+600}-{ys.max()+600}")
