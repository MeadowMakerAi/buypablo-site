# buypablo.com — Site Plan & Asset Inventory

## ASSETS NEEDED

### Tier 1: Must-Have for Launch (blocks deployment)

| # | Asset | Where It Goes | What's Wrong Now | Fix |
|---|---|---|---|---|
| 1 | **Hero product image (index)** | Landing page hero | Hemp render — says "12% cannabis terpenes" (NY cap is 10%), has hemp THC warning icon instead of NY symbol | Option A: Edit existing render (swap terpene %, swap warning icon). Option B: New render from updated packaging files. Either way needs drop shadow for 3D realism |
| 2 | **Live Resin product card image** | index.html "Fresh Frozen Live Resin" card | Hemp render | Need NY-compliant Live Resin product image |
| 3 | **Flavors product card image** | index.html "Flavors" card | Hemp render | Need NY-compliant Flavors product image |
| 4 | **Live Resin hero image** | live-resin.html hero | Hemp render | NY Live Resin hero |
| 5 | **Flavors hero image** | flavors.html hero | Hemp render | NY Flavors hero |
| 6 | **Live Resin 3-format images** | live-resin.html product cards (AIO, 510, Concentrate) | Hemp renders, inconsistent sizing | 3 individual NY product shots, properly sized |
| 7 | **Flavors 2-format images** | flavors.html product cards (AIO, 510) | Hemp renders | 2 individual NY product shots |
| 8 | **Family shot (updated)** | "The Pablo Difference" section + "The Standard" section | Hemp family shot — says "15% cannabis terpenes", "THC-P" | Remove THC-P text, fix terpene %, or create new family shot |
| 9 | **Flavor badges (clean)** | flavors.html "All Seven Flavors" section | Sloppy screen grab with black edges, has emojis (kid-appeal concern), unfiled ™ symbols | Clean horizontal asset, remove emojis and ™ marks |

### Tier 2: Important But Not Blocking Launch

| # | Asset | Notes |
|---|---|---|
| 10 | Rotating hero images (multiple products) | Nice-to-have: hero cycles through different packaging |
| 11 | Cannabis/greenhouse photography | For Live Resin page — plant-to-product story. Alex may have DSLR greenhouse photos |
| 12 | Gummies placeholder/coming soon imagery | For Flavors page when gummies section gets built out |
| 13 | Pre-roll assets | Have packaging print files, could generate renders |
| 14 | Dispensary locator feature | Beyond a simple "Find Pablo" — needs zip code search |

---

## SITE ISSUES — ORGANIZED BY PRIORITY

### P0: Fix Before Launch

1. **Nav dropdown broken** — hover/click doesn't reliably let you select items from dropdown. CSS hover state issue
2. **Drop TerpSafe™ everywhere** — trademark never filed. Remove ™ symbol from all pages
3. **Font size too small** — product card text, features strip descriptions, copy blocks are hard to read on laptop, worse on mobile
4. **"Seven Flavors" section on index is empty** — dark background with heading but no content below. Either build it out or remove it
5. **Mobile optimization** — never tested or discussed. Needs responsive audit
6. **Flavor badges asset has black edges** — replace with cleaner crop Alex uploaded
7. **Flavors page has garbage placeholder image** — black brand book image in "The Approach" section needs replacement

### P1: Fix Soon After Launch

8. **Copy: "The Pablo Difference"** — currently only speaks to fresh frozen extraction. Needs nuance for Flavors line (water clear terps). Not launch-blocking but should be updated
9. **Copy: Concentrate description** — "Nectar Badder and Nectar & Diamonds" is hemp vestigial. Should say something like "Fresh frozen live resin, ready to dab"
10. **Copy: "Pure experience" cross-link on Flavors page** — "nothing added, nothing removed" subtly disses the Flavors line. Rework to "Want the fresh frozen experience?" without implying Flavors is impure
11. **Nav restructure for growing product catalog** — current: Live Resin | Flavors | Contact | Experience. Need to accommodate pre-rolls, gummies, concentrates. Consider a "Products" dropdown that houses all categories
12. **Product card text balance** — "Fresh Frozen Live Resin" (4 words) vs "Flavors" (1 word) feels unbalanced. Consider "Live Resin" and "Pablo Flavors" or similar
13. **Flavors marquee** — yellow background with flavor names. Would look better with white background and each flavor name in its accent color
14. **Cannabis imagery SEO/compliance audit** — analyze whether cannabis keywords, leaf imagery, etc. create SEO throttling, payment processor issues, or ad platform restrictions

### P2: Polish / Future

15. **Dispensary locator with zip code search** — upgrade from simple "Find Pablo" to interactive feature
16. **Gummies section in Flavors page** — either "Coming Soon" card or full product section when packaging exists
17. **Pre-rolls placement** — TBD whether they go under Live Resin, Flavors, or need own category
18. **Contact page + Experience page review** — Alex hasn't reviewed these yet
19. **Cannabis greenhouse photography integration** — Alex may have DSLR photos from old greenhouse operation

---

## ASSET PIPELINE — HOW WE BUILD THESE

### Approach for Product Renders

**Source:** Packaging print files (AI dielines) already uploaded as screenshots
**Problem:** We don't have 3D mockup renders of the NY packaging
**Options:**

1. **Gemini image generation** — Feed it the dieline screenshots + reference hemp renders, ask it to generate product mockup renders with the updated packaging. Fast but may need iteration for accuracy
2. **Edit existing hemp renders** — Use Pillow/ImageMagick to:
   - Swap "12% cannabis terpenes" → "10% cannabis terpenes"
   - Replace hemp THC warning triangle with NY symbol
   - Remove "THC-P" from family shots
   - Add drop shadows for 3D depth
3. **Figma MCP** — Use the connected Figma integration to create web-optimized product cards from the print file assets
4. **Hybrid** — Edit simple text swaps with CLI tools, use Gemini for full re-renders where needed

### Recommended Sequence

1. Fix nav dropdown, font sizes, TerpSafe™ removal, empty sections (pure code — no assets needed)
2. Clean up flavor badges asset (replace with Alex's cleaner upload)
3. Edit existing hemp renders for quick wins (terpene %, warning icon swaps)
4. Use Gemini to generate hero-quality product renders from packaging dieline references
5. Build out missing sections (gummies coming soon, nav restructure)

---

## WHAT I CAN DO RIGHT NOW (while Alex is away)

### Safe to Execute:
- [ ] Fix nav dropdown CSS
- [ ] Remove TerpSafe™ from all pages
- [ ] Increase font sizes on product cards, features strip, copy blocks
- [ ] Fix or remove empty "Seven Flavors" section on index
- [ ] Replace flavor badges with cleaner asset
- [ ] Fix copy: concentrate description
- [ ] Fix copy: "pure experience" cross-link wording
- [ ] Mobile responsive audit + fixes
- [ ] Balance "Fresh Frozen Live Resin" vs "Flavors" text

### Needs Alex's Input:
- Nav restructure (Products dropdown vs current setup)
- Gummies placement decision
- Cannabis imagery inclusion (cost-benefit)
- SEO/compliance audit scope
- Which greenhouse photos to use
- Final copy for "The Pablo Difference" section
- Hero image strategy (edit existing vs new renders)
