# buypablo.com Launch Plan — Week of 2026-04-16

## Status: CODE COMPLETE, ASSETS BLOCKING

The site is code-complete and deployment-ready. Six pages, all functional, all responsive. What's blocking launch is **2 asset re-renders** and **1 deployment action**.

---

## CRITICAL PATH (must do before launch)

### 1. Deploy to Vercel (30 min)
- [ ] Push this git repo to GitHub (`gh repo create buypablo --private --push`)
- [ ] Connect to Vercel (import from GitHub, zero-config static site)
- [ ] Point buypablo.com DNS to Vercel (update GoDaddy nameservers)
- [ ] Verify HTTPS + custom domain
- [ ] Test age gate, all nav links, product images, mobile

### 2. Fix Pineapple Marker AIO Render (Gemini re-render)
**Problem:** Strain badge has pixelated pineapple emoji artifact and garbled text  
**Fix:** Re-render in Gemini using the packaging dieline as reference  
**Prompt approach:** Use `tools/generate_gemini_prompts.py` prompt #1 (AIO box render), specify Pineapple Marker, reference the clean Terp Taxi render as style guide  
**Post-process:** Run through `tools/post_process_asset.py --card` to size for web  
**Replace:** `assets/images/pablo_aio_pineapple_marker_ny.jpeg`  
**Impact:** Shows on homepage hero rotation, flavors page hero rotation, flavors AIO card rotation

### 3. Fix Live Resin AIO "LIVE RESIN" Font (Gemini re-render)
**Problem:** The "LIVE RESIN" text on the AIO box render uses wrong typeface — should be Cubano Sharp per brand spec  
**Fix:** Same Gemini re-render approach, using the 510 mylar bag (which has correct font) as the style reference  
**Replace:** `assets/images/pablo_aio_live_resin_sour_diesel_ny.jpeg`  
**Impact:** Shows on live-resin.html hero, live-resin.html product card, homepage Live Resin product card, experience.html hardware scene

---

## NICE TO HAVE (post-launch week)

### Asset Improvements
- [ ] **Family shot** — all product formats (AIO + 510 + concentrate) in one hero image. Replace the `brandbook_p13` images used as placeholders on wholesale page
- [ ] **Lifestyle photography** — greenhouse/cultivation shots for the process section. Alex may have DSLR photos
- [ ] **Flavor badges cleanup** — current `flavor-badges.jpeg` (removed from site but referenced in brand materials) has emojis and unfiled ™ marks. Clean Pillow-generated badges exist in `assets/images/badges/`
- [ ] **Concentrate jar render** — current image is a flat digital label, not a 3D jar render. Lower priority since concentrate is a smaller SKU

### Feature Additions
- [ ] **Store locator** — Jaunty has a Google Maps-based locator with geolocation. Build once Pablo has confirmed dispensary placements. Can use dispensary_intelligence table data. Implementation: embed Google Maps with custom markers, ~2 hours of work
- [ ] **Lab results page** — dedicated page with batch-specific COAs (PDF links or embedded). Currently just "scan QR code" reference
- [ ] **Social links** — Instagram, X handles in footer once social accounts are active
- [ ] **Newsletter signup** — email capture for drops/new flavors. Pair with info@buypablo.com
- [ ] **FAQ page** — Jaunty has tabbed FAQ. Worth building once you get real customer questions

### Nav Restructure (when product catalog grows)
- [ ] "Products" mega dropdown housing Live Resin + Flavors + future lines (pre-rolls, gummies)
- [ ] Currently 4 nav items works fine for 2 product lines

---

## COMPETITIVE POSITION vs JAUNTY

| Dimension | Jaunty | Pablo | Winner |
|-----------|--------|-------|--------|
| Age gate | None | Full-screen 21+ gate | **Pablo** |
| Typography | Generic Google Fonts | Space Grotesk + Bebas Neue (brand identity) | **Pablo** |
| Color system | Budget yellow-cream | Flavor-specific accent colors (7 distinct) | **Pablo** |
| Product specs on cards | None (no THC, no weight) | Weight + type + features on every card | **Pablo** |
| Product images | Flat 300x300 squares | 3D package renders with packaging detail | **Pablo** |
| Brand experience | Scroll page, no interactivity | Cinematic 11-scene scroll-snap with parallax | **Pablo** |
| Strain profiles | None on product pages | Sour Diesel + Runtz with effects/terpene notes | **Pablo** |
| Store locator | Google Maps + geolocation | "Find Pablo" CTA + email (locator post-launch) | Jaunty |
| Content depth | Blog, events, merch, FAQ | Product pages + experience (blog/FAQ post-launch) | Jaunty |
| Compliance | No age gate, no warnings | Age gate + NY OCM §128.5 warnings on packaging | **Pablo** |

**Pablo wins 8 of 10 dimensions.** The two gaps (store locator, content depth) are post-launch additions that don't block a credible launch.

---

## DEPLOYMENT CHECKLIST

```
[ ] git push to GitHub
[ ] Vercel import + build
[ ] DNS: buypablo.com → Vercel
[ ] HTTPS verified
[ ] Hard refresh all pages in Chrome + Safari + mobile Safari
[ ] Age gate works
[ ] All nav links work (desktop + mobile hamburger)
[ ] All product images load (no cached hemp renders)
[ ] Flavor rotators work without white flash
[ ] Flavor bands animate on scroll
[ ] Experience page scroll-snap works
[ ] Contact email links work (info@buypablo.com, wholesale@buypablo.com)
[ ] OG tags render correct preview when shared on social
[ ] Mobile responsive: hero, product cards, flavor bands, footer
```
