#!/bin/bash
# Retry the AIO Live Resin font fix when Gemini API quota resets.
# Run manually: bash retry_gemini_font_fix.sh
# The script will retry every 5 min until it succeeds or you kill it.

export GEMINI_API_KEY="${GEMINI_API_KEY:-AQ.Ab8RN6KPorJ58X_fO9yyLX2kmPrWdGyLWLBacgP7HXVIiNQqVg}"

/tmp/gemini-venv/bin/python3 - <<'PYEOF'
import os, sys, time
from google import genai
from google.genai import types
from pathlib import Path

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

aio = Path(os.path.expanduser("~/Downloads/AIO LIVE RESIN (ALMOST THERE - NEEDS FONT CHANGE) .png"))
ref = Path(os.path.expanduser("~/workspaces/pablo/site/tools/font_reference_live_resin.png"))

prompt = """Edit the packaging image to match the fonts shown in the reference image.
Replace ONLY "fresh frozen" and "LIVE RESIN" text on the front face of the box:
- "fresh frozen" → match the top font in reference (white, geometric sans-serif, NOT italic)
- "LIVE RESIN" → match the bottom font in reference (yellow, bold rounded display)
Remove all text from the left spine — leave spine as clean blue.
Change NOTHING else. Same box, angle, badge, compliance icons, everything."""

parts = [prompt,
    types.Part.from_bytes(data=aio.read_bytes(), mime_type="image/png"),
    types.Part.from_bytes(data=ref.read_bytes(), mime_type="image/png"),
]

out = Path(os.path.expanduser("~/workspaces/pablo/site/assets/images/pablo_aio_live_resin_sour_diesel_ny_v2.png"))

for attempt in range(20):
    print(f"Attempt {attempt+1}...")
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash-image", contents=parts,
            config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
        )
        for part in resp.candidates[0].content.parts:
            inline = getattr(part, "inline_data", None)
            if inline and inline.data:
                out.write_bytes(inline.data)
                print(f"SUCCESS → {out} ({len(inline.data)} bytes)")
                # Also make web-optimized version
                from PIL import Image
                img = Image.open(out).convert("RGB")
                w, h = img.size
                if w > 1200:
                    img = img.resize((1200, int(h * 1200 / w)), Image.LANCZOS)
                web = out.parent / "pablo_aio_live_resin_sour_diesel_ny.jpeg"
                img.save(web, "JPEG", quality=85)
                print(f"Web version → {web}")
                sys.exit(0)
        print("No image in response")
    except Exception as e:
        print(f"  {str(e)[:120]}")
    print("Retrying in 5 min...")
    time.sleep(300)

print("Gave up after 20 attempts")
PYEOF
