#!/usr/bin/env python3
"""
PABLO FLAVORS Packaging Generator v2
Composite real brand badges onto the approved Pineapple Marker template.

Workflow:
  1. Load approved Pineapple Marker NY template
  2. HSV-shift the compliance strip pink to each flavor's accent color
  3. Composite the real brand badge (from SVG extract) over the template badge region
  4. Output 7 hero images

Input: /assets/images/badges/badge_<flavor>.png (one per flavor)
Output: /assets/images/pablo_aio_<flavor>_ny.jpeg
"""

import os
import numpy as np
from PIL import Image
import colorsys

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.dirname(BASE_DIR)
TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_pineapple_marker_original.jpeg")
OUTPUT_DIR = os.path.join(SITE_DIR, "assets/images")
BADGES_DIR = os.path.join(SITE_DIR, "assets/images/badges")

# --- Template regions (measured from pink-mask analysis) ---
BADGE_BBOX = (223, 631, 482, 702)         # Flavor badge region (x1, y1, x2, y2)
COMPLIANCE_BBOX = (0, 740, 687, 837)      # Compliance strip region (full width)

# --- Flavor spec ---
SOURCE_COLOR = "#EE3680"  # Pineapple Marker pink
FLAVORS = {
    "pineapple_marker":  {"color": "#EE3680", "slug": "pineapple_marker"},
    "sundae_grapes":     {"color": "#81288E", "slug": "sundae_grapes"},
    "terp_taxi":         {"color": "#FDAA00", "slug": "terp_taxi"},
    "mangonada":         {"color": "#EE2737", "slug": "mangonada"},
    "marmalade":         {"color": "#FCA311", "slug": "marmalade"},
    "pie_face":          {"color": "#EE3680", "slug": "pie_face"},
    "watermelon_gusher": {"color": "#E80029", "slug": "watermelon_gusher"},
}

def hex_to_rgb(h):
    return tuple(int(h.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hsv_np(arr):
    arr_f = arr.astype(float) / 255.0
    r, g, b = arr_f[:,:,0], arr_f[:,:,1], arr_f[:,:,2]
    maxc = np.max(arr_f, axis=2)
    minc = np.min(arr_f, axis=2)
    v = maxc
    delta = maxc - minc
    s = np.where(maxc > 0, delta / np.where(maxc==0, 1, maxc), 0)
    rc = np.where(delta==0, 0, (maxc - r) / np.where(delta==0, 1, delta))
    gc = np.where(delta==0, 0, (maxc - g) / np.where(delta==0, 1, delta))
    bc = np.where(delta==0, 0, (maxc - b) / np.where(delta==0, 1, delta))
    h = np.where(r == maxc, bc - gc,
         np.where(g == maxc, 2.0 + rc - bc, 4.0 + gc - rc))
    h = (h / 6.0) % 1.0
    return np.stack([h, s, v], axis=2)

def hsv_to_rgb_np(hsv):
    h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]
    i = np.floor(h * 6).astype(int)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6
    r = np.choose(i, [v, q, p, p, t, v])
    g = np.choose(i, [t, v, v, q, p, p])
    b = np.choose(i, [p, p, t, v, v, q])
    rgb = np.stack([r, g, b], axis=2) * 255
    return np.clip(rgb, 0, 255).astype(np.uint8)

def shift_compliance_strip_color(arr, source_hex, target_hex, tol=45):
    """HSV-shift pink pixels ONLY inside the compliance strip y-range."""
    sr, sg, sb = hex_to_rgb(source_hex)
    tr, tg, tb = hex_to_rgb(target_hex)

    # Restrict mask to compliance strip y-range
    _, cy1, _, cy2 = COMPLIANCE_BBOX
    h, w, _ = arr.shape
    y_mask = np.zeros((h, w), dtype=bool)
    y_mask[cy1:cy2, :] = True

    diff_r = np.abs(arr[:,:,0].astype(int) - sr)
    diff_g = np.abs(arr[:,:,1].astype(int) - sg)
    diff_b = np.abs(arr[:,:,2].astype(int) - sb)
    color_mask = (diff_r < tol) & (diff_g < tol) & (diff_b < tol)
    mask = y_mask & color_mask

    source_hsv = colorsys.rgb_to_hsv(sr/255, sg/255, sb/255)
    target_hsv = colorsys.rgb_to_hsv(tr/255, tg/255, tb/255)
    hue_delta = target_hsv[0] - source_hsv[0]
    sat_ratio = target_hsv[1] / source_hsv[1] if source_hsv[1] > 0 else 1
    val_ratio = target_hsv[2] / source_hsv[2] if source_hsv[2] > 0 else 1

    hsv = rgb_to_hsv_np(arr)
    hsv[mask, 0] = (hsv[mask, 0] + hue_delta) % 1.0
    hsv[mask, 1] = np.clip(hsv[mask, 1] * sat_ratio, 0, 1)
    hsv[mask, 2] = np.clip(hsv[mask, 2] * val_ratio, 0, 1)
    return hsv_to_rgb_np(hsv)

def find_perspective_coeffs(src_corners, dst_corners):
    """Compute 8 coefficients for PIL PERSPECTIVE transform (dst -> src mapping)."""
    matrix = []
    for s, t in zip(src_corners, dst_corners):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])
    A = np.array(matrix, dtype=np.float64)
    B = np.array(src_corners, dtype=np.float64).reshape(8)
    res = np.linalg.lstsq(A, B, rcond=None)[0]
    return res.tolist()

# Package tilt: right side is HIGHER than left (reversed from my earlier top-edge measurement,
# which was reading the box lid angle, not the front-face label angle).
TILT_SLOPE = -0.0365

def get_badge_quad():
    """4 destination corners on template that match package front-face perspective tilt."""
    x1, y1, x2, y2 = BADGE_BBOX
    w = x2 - x1
    drop = int(w * TILT_SLOPE)  # negative = right side goes up
    tl = (x1, y1)
    tr = (x2, y1 + drop)
    br = (x2, y2 + drop)
    bl = (x1, y2)
    return [tl, tr, br, bl]

PABLO_BLUE_RGB = (0, 71, 187)

def get_badge_pink_mask(original_template_path):
    """Compute a pixel mask (bool) of where the ORIGINAL Pineapple Marker pink badge is visible.
    The vape cartridge occludes part of the badge — this mask respects that occlusion."""
    orig = Image.open(original_template_path).convert("RGB")
    arr = np.array(orig)
    mask = (
        (arr[:,:,0] > 180) &
        (arr[:,:,1] < 130) &
        (arr[:,:,2] > 80) & (arr[:,:,2] < 200) &
        (arr[:,:,0] > arr[:,:,1] + 20)
    )
    # Restrict to badge y-range (above the compliance strip)
    mask[720:, :] = False
    mask[:600, :] = False
    return mask

# Pre-compute the badge pink mask from the ORIGINAL pineapple marker template.
# We save a copy of the original since we overwrite the main path during regeneration.
ORIGINAL_TEMPLATE_PATH = os.path.join(BASE_DIR, "_pineapple_marker_original.jpeg")
if not os.path.exists(ORIGINAL_TEMPLATE_PATH):
    # First run: save a copy of the current template as the immutable original
    Image.open(TEMPLATE_PATH).save(ORIGINAL_TEMPLATE_PATH, "JPEG", quality=95)

BADGE_PINK_MASK = get_badge_pink_mask(ORIGINAL_TEMPLATE_PATH)

def erase_old_badge(template_img):
    """Repaint the original-pink pixels only (not a rectangular bbox) with Pablo Blue.
    This preserves vape occlusion since the vape pixels were never pink in the original."""
    arr = np.array(template_img.convert("RGB"))
    # Dilate mask slightly so the anti-aliased edge pixels also get cleaned
    from PIL import ImageFilter
    mask_img = Image.fromarray((BADGE_PINK_MASK * 255).astype(np.uint8))
    mask_dilated = mask_img.filter(ImageFilter.MaxFilter(5))  # 2px dilation
    mask_arr = np.array(mask_dilated) > 0
    arr[mask_arr] = PABLO_BLUE_RGB
    return Image.fromarray(arr)

def composite_badge(template_img, badge_path):
    """Warp new badge onto template, masked by the ORIGINAL pink mask (so vape stays in front)."""
    template_img = erase_old_badge(template_img).convert("RGBA")

    badge = Image.open(badge_path).convert("RGBA")

    # Step 1: Lanczos downsample to target rect size
    x1, y1, x2, y2 = BADGE_BBOX
    target_w = x2 - x1
    target_h = y2 - y1
    badge_small = badge.resize((target_w, target_h), Image.LANCZOS)

    # Step 2: Perspective warp the resized badge into the template canvas
    bw, bh = badge_small.size
    src_corners = [(0, 0), (bw, 0), (bw, bh), (0, bh)]
    dst_corners = get_badge_quad()
    coeffs = find_perspective_coeffs(src_corners, dst_corners)

    tw, th = template_img.size
    warped = badge_small.transform((tw, th), Image.PERSPECTIVE, coeffs, Image.BICUBIC)

    # Step 3: Apply the ORIGINAL pink mask to the warped badge alpha so vape occlusion is preserved
    warped_arr = np.array(warped)  # RGBA
    mask_2d = BADGE_PINK_MASK.astype(np.uint8) * 255
    # Multiply existing alpha by the mask (both must agree: pixel is in warped badge AND was pink)
    warped_arr[:, :, 3] = np.minimum(warped_arr[:, :, 3], mask_2d)
    warped = Image.fromarray(warped_arr)

    template_img.paste(warped, (0, 0), warped)
    return template_img

def generate_for_flavor(key, spec):
    template = Image.open(TEMPLATE_PATH).convert("RGB")
    arr = np.array(template)

    # Shift compliance strip color (skip if already source color)
    if spec["color"].upper() != SOURCE_COLOR.upper():
        arr = shift_compliance_strip_color(arr, SOURCE_COLOR, spec["color"])
    template = Image.fromarray(arr).convert("RGBA")

    # Composite new badge
    badge_path = os.path.join(BADGES_DIR, f"badge_{spec['slug']}.png")
    if not os.path.exists(badge_path):
        print(f"  [warn] badge missing: {badge_path}")
        return
    template = composite_badge(template, badge_path)

    # Save as JPEG
    out_path = os.path.join(OUTPUT_DIR, f"pablo_aio_{spec['slug']}_ny.jpeg")
    template.convert("RGB").save(out_path, "JPEG", quality=92)
    print(f"  [ok] {key} → {out_path}")

def main():
    print("Generating NY-compliant FLAVORS packaging with brand badges...")
    for key, spec in FLAVORS.items():
        generate_for_flavor(key, spec)
    print("Done.")

if __name__ == "__main__":
    main()
