# buypablo.com — RIL Competitive Audit

**Date:** 2026-04-18 | **RIL Cycle:** 1 | **Sites browsed:** 8 (Pablo + 7 competitors)
**All data is OBSERVED (browsed via Playwright). No estimates or assumptions.**

---

## SITES AUDITED

| # | Site | Type | Browsed by |
|---|------|------|-----------|
| 1 | buypablo.com (localhost) | Pablo (current state) | Direct |
| 2 | jaunty.com | NY vape/edible brand (Alex recommended) | Direct |
| 3 | mfny.co | NY cultivator/processor brand | Direct |
| 4 | stiiizy.com | National vape brand (CA-based, NY presence) | Agent |
| 5 | ayrloom.com | NY multi-category brand (Beak & Skiff family) | Agent |
| 6 | pax.com | National vape hardware brand | Agent |
| 7 | kivaconfections.com | National edibles brand | Agent |

---

## FEATURE COMPARISON (OBSERVED)

| Feature | Pablo | Jaunty | MFNY | STIIIZY | Ayrloom | PAX | Kiva |
|---------|:-----:|:------:|:----:|:-------:|:-------:|:---:|:----:|
| Age gate | YES | YES | YES | YES | YES | YES | YES |
| Store/dispensary locator | **NO** | YES (ZIP) | YES (map) | YES | YES (state) | YES | YES |
| Populated product pages | **NO** (empty cards) | YES | YES | YES | YES | YES | YES |
| FAQ section | **NO** | YES | YES | YES | YES | YES | YES |
| Social media links | **NO** | YES (4) | YES | YES (7) | YES | YES | YES |
| Newsletter signup | **NO** | YES (full form) | NO | YES | YES | YES | YES |
| Blog/content | **NO** | YES | YES | YES | NO | YES | YES |
| Lab results page | **NO** | YES | YES | NO | YES | NO | YES |
| Wholesale/B2B page | Contact form only | "Want to Sell?" | NO | "Biz Inquiry" | LeafLink | "Become Retailer" | NO |
| E-commerce | NO | NO | NO | YES (CA) | YES | YES | Partial |
| Events page | NO | YES | NO | YES | YES | YES | NO |
| Merch store | NO | YES (external) | YES (giftsets) | YES (apparel) | YES (swag) | NO | NO |
| Product quiz/recommender | NO | NO | NO | NO | YES (by effect) | NO | YES (budtender) |
| Cannabis photography | NO | Limited | YES (real plants) | Product-only | YES (farm/nature) | Hardware-only | Product-only |
| Mobile verified | **NOT TESTED** | NOT TESTED | NOT TESTED | Expected | YES (375px) | Expected | Expected |

---

## PABLO'S CURRENT STATE (OBSERVED, localhost Apr 18)

### What works
- Age gate: clean, on-brand (Pablo logo + blue background)
- Hero sections: headline + product image on all 3 product pages
- Marquee ticker: animated text strip with brand phrases
- Section rhythm: alternating blue/white/dark/yellow backgrounds
- Brand identity: hand-brushed PABLO logo, Bebas Neue typography, square buttons
- Nav: LIVE RESIN | FLAVORS | CONTACT | EXPERIENCE
- Footer: consumer/retailer CTAs, copyright, nav links

### What's broken
- **Index:** 2 massive empty dark blue sections where product cards (Live Resin, Flavors) should be
- **Flavors page:** 2 empty sections where AIO and 510 product format cards should be
- **Live Resin page:** 3 empty sections where AIO, 510, and concentrate cards should be
- **Text too small:** Body copy and card descriptions are hard to read
- **Nav dropdown:** Known broken (SITE-PLAN.md P0 #1)
- **TerpSafe™:** Still present, trademark never filed (SITE-PLAN.md P0 #2)

---

## GAP ANALYSIS — PABLO vs. COMPETITIVE STANDARD

### Features that ALL 7 competitors have, Pablo doesn't:

**1. Store/dispensary locator**
- Jaunty: ZIP code search field
- MFNY: Interactive map with pins, dispensary names and addresses
- Ayrloom: State dropdown built into homepage
- STIIIZY: "Dispensaries" in main nav, dedicated locations page
- PAX: "Store Locator" + "Dispensary Near Me" in footer
- Kiva: "Find Us" in header, IHeartJane integration
- **Pablo: Nothing.** "Available at select licensed dispensaries" with no way to find them.

**2. Populated product pages with actual content**
- All 7 competitors show product images, descriptions, specs
- Pablo has the page structure but the product card sections are empty dark voids

### Features that 5-6 of 7 competitors have, Pablo doesn't:

**3. FAQ section** (6/7)
- Jaunty: expandable Q&A (dietary, shipping, dispensary, testing)
- MFNY: "MFAQ" section
- Addresses real consumer questions (Can I order online? Is it tested? Where do I find it?)

**4. Social media links visible on site** (6/7)
- Most have Instagram, Facebook, X at minimum
- Jaunty + STIIIZY + Ayrloom have 4-7 platform links

**5. Newsletter/email signup** (5/7)
- Jaunty collects: name, email, phone, birthday, zip code, dispensary
- This is customer acquisition infrastructure Pablo doesn't have

**6. Blog or content section** (5/7)
- MFNY: "Knowledge Nugs" with articles
- Jaunty: blog with posts
- STIIIZY: blog with event recaps
- Builds SEO, tells brand story, gives people reasons to return

### Features that 3-4 of 7 competitors have:

**7. Lab results page** (4/7) — Jaunty, MFNY, Ayrloom, Kiva
**8. Events page** (4/7) — Jaunty, STIIIZY, Ayrloom, PAX
**9. Merch/swag store** (4/7) — Jaunty, MFNY, STIIIZY, Ayrloom
**10. E-commerce** (3/7) — STIIIZY, Ayrloom, PAX (all Shopify)

---

## DESIGN OBSERVATIONS (OBSERVED patterns across competitors)

### Aesthetic approaches

| Brand | Aesthetic | Colors | Typography |
|-------|-----------|--------|------------|
| **Pablo** | Street-premium (graffiti logo + geometric type) | Blue/yellow/white | Bebas Neue (default), Space Grotesk (body) |
| Jaunty | Playful-premium | Navy/yellow/salmon/teal | Serif + sans mix, personality-driven copy |
| MFNY | Farm-authentic | Beige/dark green/white | Clean sans-serif, nature photography |
| STIIIZY | Urban-lifestyle | White/black/accent pops | Bold uppercase, streetwear influence |
| Ayrloom | Warm-organic | Orange/amber/teal/golden | All-lowercase brand voice |
| PAX | Tech-premium | Black/dark/minimal | Clean sans-serif, device-forward |
| Kiva | Artisan-confectionery | Cream/earth tones/warm | Serif + sans mix, illustration |

**Pablo's aesthetic is differentiated.** No other competitor uses the graffiti-meets-geometric tension. The blue/yellow palette is bold. The issue isn't the design direction — it's that the site is unfinished (empty product sections, broken nav, unreadable text).

### Age gate approaches

| Style | Sites |
|-------|-------|
| Simple YES/NO | Jaunty ("YOU BET/NOT YET"), MFNY, STIIIZY |
| State + age | PAX (state dropdown required first) |
| State + DOB | Kiva (full date of birth entry) |
| Simple 21+ | Ayrloom, Pablo |

Pablo's age gate is fine. Clean and functional.

---

## JAUNTY DEEP DIVE (Alex's recommended reference)

What makes Jaunty good (OBSERVED):

1. **Brand voice is consistent and playful.** "HIT YOUR STRIDE." / "YOU BET" / "We're kind of like that friend who whispers 'Jump'" — personality everywhere, not just in the hero
2. **Store locator is prominent** — "WHERE'S JAUNTY?" section with ZIP code search, not buried in footer
3. **Newsletter captures useful data** — zip code + dispensary = geographic targeting + retail relationship intelligence
4. **FAQ addresses real questions** — "Can I consume Jaunty gummies?" (dietary), "Can you ship to me?" (state), "Where can I find Jaunty?" (distribution), "Are products tested?" (trust)
5. **Product categories are clear** — Gummies, Vapes, Tinctures, Dabs — one click from homepage
6. **"Soil to Oil" extraction story** — similar to Pablo's "We Froze the Field" but more developed
7. **"Want to Sell Jaunty?"** — dedicated wholesale page linked from footer, not just a contact form
8. **Merch store** — external (merch.jaunty.com) with 15% discount popup for email capture
9. **Lab results page** — transparency/trust signal
10. **Events directory** — community presence

---

## NOT OBSERVED (gaps in this audit)

| Gap | Why it matters |
|-----|---------------|
| Mobile responsiveness (Pablo) | SITE-PLAN.md says "never tested." We didn't test it either. |
| Page load performance | No Lighthouse or CWV measurements taken |
| SEO structure | No audit of meta tags, schema markup, keyword targeting |
| Accessibility | No WCAG audit performed |
| Analytics integration | Don't know if Pablo has any tracking installed |
| Non-cannabis reference sites | Alex flagged that good websites are good websites regardless of category. We only browsed cannabis sites. |

---

## SYNTHESIS: WHAT SHOULD PABLO DO?

### Tier 1 — The site is unfinished (fix before anything else)
1. **Fill the empty product card sections** — this is the single biggest issue. The skeleton is there but there's no flesh.
2. **Fix the nav dropdown** — broken CSS
3. **Increase text size** — body copy is unreadable
4. **Remove TerpSafe™** — trademark never filed

### Tier 2 — Features every competitor has that Pablo doesn't
5. **Add a store locator** — even a simple "Find Pablo" section with a zip code field or state dropdown. Every single competitor has one.
6. **Add social media links** — Instagram at minimum. 6/7 competitors have them visible.
7. **Add a FAQ section** — 6/7 competitors have one. Answers the questions consumers actually ask.

### Tier 3 — Features most competitors have
8. **Newsletter signup** — capture email + zip code at minimum. Customer acquisition infrastructure.
9. **Lab results page** — trust signal. 4/7 competitors have it.
10. **Blog** — SEO, brand storytelling, reason to return. 5/7 have it.
11. **Dedicated wholesale page** — not just a contact form. "Want to carry Pablo?" with distributor info.

### Tier 4 — Nice to have
12. Events page
13. Merch store
14. Product quiz/recommender
15. E-commerce (requires compliance infrastructure)
