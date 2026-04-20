"""
Pablo Fresh Social Config — extends brand_config.py for social content pipeline.
Platform rules, safe language, content pillar definitions.
"""

from brand_config import PABLO_BLUE, PABLO_YELLOW, PABLO_WHITE, FLAVORS, LOGO_DESCRIPTION

# --- Brand Identity (Social) ---
BRAND_NAME = "Pablo Fresh"  # Working name — pending final decision with Ethan
BRAND_TAGLINE = "We Froze the Field"
BRAND_HANDLE_PRIMARY = "@pablofresh"  # Target handle — confirm availability
BRAND_HANDLE_BACKUP = "@freshfrozenterpz"  # Legacy — dormant, redirect only

# --- Platform Strategy ---
PLATFORMS = {
    "instagram": {
        "role": "lifestyle",  # lifestyle brand, zero cannabis signals
        "content_mix": {"reels": 0.60, "carousels": 0.30, "single_image": 0.10},
        "posting_frequency": "5x/week",
        "paid_ads": False,  # cannabis paid ads banned on Meta
        "product_photos": False,  # no product shots showing THC/cannabis
        "direct_links": False,  # bio link to age-gated landing page only
        "safe_link_strategy": "linktree or landing page with 21+ age gate",
    },
    "x": {
        "role": "aggressive",  # product marketing, paid ads, direct links
        "content_mix": {"threads": 0.40, "single_image": 0.30, "video": 0.30},
        "posting_frequency": "3x/week",
        "paid_ads": True,  # X allows cannabis paid ads with age verification
        "product_photos": True,
        "direct_links": True,  # direct links to buypablo.com allowed
    },
    "email": {
        "role": "sales",  # no platform restrictions, owned audience
        "content_mix": {"newsletter": 1.0},
        "posting_frequency": "1x/week",
        "paid_ads": False,
        "product_photos": True,
        "direct_links": True,
    },
}

# --- Safe Language (Instagram) ---
# Words and phrases that ARE safe to use
SAFE_VOCABULARY = {
    "product_descriptors": [
        "flavor-forward",
        "fresh frozen",
        "captured at peak",
        "all glass",
        "all gas",
        "all fresh",
        "crafted",
        "premium",
        "small batch",
        "seven flavors",
        "tasting notes",
        "flavor profile",
        "fresh",
        "frozen",
        "stay fresh",
    ],
    "brand_phrases": [
        "We Froze the Field",
        "All Fresh. All Gas.",
        "All Glass. All Gas.",
        "Try All 7 Fresh Flavors",
        "Stay Fresh",
        "Pablo Fresh presents",
        "Captured at peak",
    ],
    "lifestyle_terms": [
        "ritual",
        "session",
        "experience",
        "vibe",
        "culture",
        "flavor",
        "color",
        "craft",
        "curated",
        "taste",
        "fresh",
    ],
    "flavor_language": [
        "tropical citrus",
        "floral finish",
        "berry forward",
        "tangy",
        "sweet heat",
        "bright",
        "bold",
        "smooth",
        "crisp",
        "layered",
    ],
}

# --- Content Pillars ---
CONTENT_PILLARS = [
    {
        "name": "Fresh Frozen",
        "slug": "fresh-frozen",
        "day": "Thursday",
        "description": "Ice, preservation, peak flavor, the craft of capture",
        "safe_captions": [
            "Captured at peak. Frozen in time.",
            "Fresh frozen flavor — the way nature intended.",
            "Seven flavors. All flash-frozen at harvest.",
        ],
    },
    {
        "name": "NYC Streets",
        "slug": "nyc-streets",
        "day": "Monday",
        "description": "Graffiti, bodegas, stoops, neighborhoods, subway, rooftops",
        "safe_captions": [
            "Monday in the city.",
            "Every block has a flavor.",
            "New York. Always fresh.",
        ],
    },
    {
        "name": "Flavor Culture",
        "slug": "flavor-culture",
        "day": "Tuesday",
        "description": "Tasting notes, food brands, hot sauce, sensory experience",
        "safe_captions": [
            "Flavor-forward. Always.",
            "What does [flavor] taste like?",
            "Tasting notes: [descriptors]",
        ],
    },
    {
        "name": "Hip Hop & Legends",
        "slug": "hiphop-legends",
        "day": "Friday",
        "description": "Quotes, album tributes, classic NYC, street legends",
        "safe_captions": [
            "Friday rotation.",
            "Legends stay fresh.",
        ],
    },
    {
        "name": "The Shoutout",
        "slug": "the-shoutout",
        "day": "Wednesday",
        "description": "Brands we love, things we wear/drive/eat/listen to",
        "safe_captions": [
            "Things we're into this week.",
            "Pablo Fresh picks.",
            "Fresh finds.",
        ],
    },
    {
        "name": "Worldwide",
        "slug": "worldwide",
        "day": None,  # biweekly, no fixed day
        "description": "Global street scenes, flavor cultures, travel",
        "safe_captions": [
            "Fields we froze: [City]",
            "Fresh from [City].",
            "Flavor has no borders.",
        ],
    },
]

# --- Content Quality Test ---
# Every post must pass this before publishing
CONTENT_GATE_QUESTION = (
    "If someone who knows nothing about cannabis saw this, "
    "would they just see a sick NYC lifestyle brand?"
)

# --- Cross-Promo Tiers ---
CROSS_PROMO_STRATEGY = {
    "tier_1_start_here": "20K-300K followers. Independent/founder-led. High probability of mutual engagement.",
    "tier_2_strong_fit": "Above ideal range but strong aesthetic/audience alignment. Worth strategic outreach.",
    "tier_3_aspirational": "500K+. Tag in great content. 1-in-20 chance of repost = jackpot.",
}
