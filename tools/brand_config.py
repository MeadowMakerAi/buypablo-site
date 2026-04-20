"""
PABLO Brand Config — single source of truth for colors, flavors, compliance text, typography.
All asset pipeline tools import from here.
"""
import os

# --- Font Paths ---
_FONT_BASE = os.path.join(os.path.dirname(__file__), "..", "fonts")
FONT_DIR_BRAND = os.path.join(_FONT_BASE, "brand")
FONT_DIR_PACKAGING = os.path.join(_FONT_BASE, "packaging")
FONT_DIR_REFERENCE = os.path.join(_FONT_BASE, "reference")

FONTS = {
    "space_grotesk_bold": {
        "path": os.path.join(FONT_DIR_BRAND, "SpaceGrotesk-Bold.ttf"),
        "role": "primary_brand",
        "usage": "Headlines, body, UI — primary Pablo identity font",
    },
    "bebas_neue": {
        "path": os.path.join(FONT_DIR_BRAND, "BebasNeue-Regular.ttf"),
        "role": "secondary_brand",
        "usage": "Display, accent text, packaging headers",
    },
    "cubano_sharp": {
        "path": None,  # NOT YET SOURCED — needs .otf/.ttf file
        "role": "product_line",
        "usage": "LIVE RESIN product line text only (bold rounded display)",
    },
    "helvetica_neue_bd_cn": {
        "path": os.path.join(FONT_DIR_PACKAGING, "HelveticaNeueLTStd-BdCn.otf"),
        "role": "packaging_production",
        "usage": "Packaging body copy (bold condensed) — print files",
    },
    "helvetica_neue_cn": {
        "path": os.path.join(FONT_DIR_PACKAGING, "HelveticaNeueLTStd-Cn.otf"),
        "role": "packaging_production",
        "usage": "Packaging body copy (condensed) — print files",
    },
    "poligraxxiv": {
        "path": os.path.join(FONT_DIR_PACKAGING, "POLIGRAXXIV-930587474.otf"),
        "role": "packaging_display",
        "usage": "Packaging display text — from designer files",
    },
    "raskolnikov": {
        "path": os.path.join(FONT_DIR_PACKAGING, "RaskolnikovRegular-9225049.otf"),
        "role": "packaging_display",
        "usage": "Packaging display text — from designer files",
    },
    "trench_rounded_bold": {
        "path": os.path.join(FONT_DIR_PACKAGING, "TrenchRoundedBold-5406884.otf"),
        "role": "packaging_display",
        "usage": "Packaging display text — from designer files",
    },
}

# Convenience accessors for pipeline tools
FONT_BEBAS = FONTS["bebas_neue"]["path"]
FONT_SPACE_GROTESK = FONTS["space_grotesk_bold"]["path"]
FONT_REFERENCE_IMG = os.path.join(FONT_DIR_REFERENCE, "font_reference_live_resin.png")

# --- Brand Colors ---
PABLO_BLUE = "#0047BB"       # PMS 2728C
PABLO_YELLOW = "#FDDA00"
PABLO_WHITE = "#FFFFFF"

# --- Flavor Definitions ---
# Canonical list. Each tool derives its own format from this.
FLAVORS = [
    {"name": "Pineapple Marker", "color": "#EE3680", "classification": "SATIVA HYBRID"},
    {"name": "Sunday Grape",     "color": "#81288E", "classification": "INDICA HYBRID"},
    {"name": "Terp Taxi",        "color": "#FDAA00", "classification": "SATIVA"},
    {"name": "Watermelon Gusher","color": "#E80029", "classification": "INDICA"},
    {"name": "Marmalade",        "color": "#FCA311", "classification": "HYBRID"},
    {"name": "Mangonada",        "color": "#FDB829", "classification": "SATIVA HYBRID"},
    {"name": "Pie Face",         "color": "#189849", "classification": "INDICA HYBRID"},
]

# Keyed lookup for prompt generator
FLAVOR_COLORS = {f["name"]: {"color": f["color"], "classification": f["classification"]} for f in FLAVORS}

# --- Logo ---
LOGO_DESCRIPTION = """PABLO logo — large, white, hand-brushed/graffiti-style script logo. The logo is distinctive with a flowing, street-art quality. It should be prominent and clearly readable."""

# --- Compliance Text (NY OCM §128.5) ---
NY_UNIVERSAL_SYMBOL = """NY Universal Symbol — the official New York State cannabis universal symbol. Three connected icons in a row:
(a) yellow triangle with black border, black cannabis leaf silhouette, and "THC!" text in black
(b) circle with red border and "21+" in black
(c) dark navy rectangle with white New York State outline and "NEW YORK STATE" text
Small, approximately 0.5" tall in horizontal format."""

WARNING_TEXT = "THIS PRODUCT CONTAINS CANNABIS AND THC. KEEP OUT OF REACH OF CHILDREN AND PETS. FOR USE ONLY BY PERSONS 21 YEARS OF AGE AND OLDER."

ROTATING_WARNINGS = {
    "A": "Cannabis can be addictive.",
    "B": "Cannabis can impair concentration and coordination. Do not operate a vehicle or machinery under the influence of cannabis.",
    "C": "There may be health risks associated with consumption of this product.",
}

# --- Processor Info ---
PROCESSOR_NAME = "Meadow Maker Wellness LLC"   # PLACEHOLDER — Alex to confirm
PROCESSOR_CITY = "New York"                     # PLACEHOLDER — Alex to confirm
PROCESSOR_LICENSE = "OCM-PROC-24-000058-P1"
PROCESSOR_EMAIL = "info@buypablo.com"

# --- Product Ingredients ---
PRODUCT_INGREDIENTS = {
    "preroll": "Cannabis flower, cannabis concentrate, cannabis terpenes",
    "live-resin-aio": "Cannabis concentrate",
    "live-resin-510": "Cannabis concentrate",
    "live-resin-concentrate": "Cannabis concentrate",
    "flavors-aio": "Cannabis concentrate, natural terpenes",
    "flavors-510": "Cannabis concentrate, natural terpenes",
}
