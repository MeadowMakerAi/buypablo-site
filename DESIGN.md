# Design System — PABLO (buypablo.com)

Extracted from the live site, April 2026. This is the source of truth for all visual decisions. Read this before touching any UI.

## Product Context
- **What this is:** Premium cannabis vape brand website
- **Who it's for:** Cannabis consumers (21+) in the NY adult-use market
- **Space:** Premium cannabis, competing on flavor identity and extraction quality
- **Project type:** Marketing site with age gate, product pages, wholesale contact
- **Pages:** index, live-resin, flavors, experience (full-screen scroll-snap), contact-consumer, contact-wholesale

## Aesthetic Direction
- **Direction:** Street-Premium — graffiti logo energy against disciplined layout
- **Mood:** Confident, bold, direct. Not luxury-quiet, not streetwear-chaotic. The tension between the hand-brushed PABLO logo and the geometric type system IS the brand
- **Section rhythm:** Alternating backgrounds create pace — blue/white/dark/yellow. Every section has a distinct ground color. This is a core pattern, not decoration
- **Decoration:** Minimal. The flavor colors and product photography do the visual work. No icons, no illustrations, no decorative elements beyond the marquee ticker

## Typography

Bebas Neue is the DEFAULT font. The entire site speaks in Bebas. Space Grotesk appears ONLY for body/paragraph text, descriptions, and legal copy.

| Role | Font | Weight | Size | Tracking | Usage |
|------|------|--------|------|----------|-------|
| Default/Headlines | Bebas Neue | 400 | clamp(2.5rem, 5vw, 6.5rem) | 0.02em | Everything unless specified otherwise |
| Section labels | Bebas Neue | 400 | 0.9rem | 0.25em | Yellow overlines ("The Process", "The Menu") |
| Nav links | Bebas Neue | 400 | 1.8rem | 0.12em | All caps, yellow underline on hover |
| Buttons | Bebas Neue | 400 | 1.2rem | 0.15em | All caps |
| Product card names | Bebas Neue | 400 | 1.5rem | 0.08em | All caps |
| Flavor band names | Bebas Neue | 700 | clamp(1.6rem, 3vw, 2.8rem) | 0.08em | All caps, text-shadow |
| Body/paragraphs | Space Grotesk | 400 | 1.2rem | 0.01em | line-height: 1.7, max-width: 540px |
| Card descriptions | Space Grotesk | 400 | 1.1rem | — | line-height: 1.65 |
| Feature descriptions | Space Grotesk | 400 | 1.1rem | — | line-height: 1.65 |
| Footer legal | Space Grotesk | 400 | 0.7rem | 0.05em | opacity: 0.35 |
| Footer tagline | Space Grotesk | 400 | 0.8rem | 0.1em | All caps, opacity: 0.4 |

**Loading:** Google Fonts (Bebas Neue + Space Grotesk 400-700), preconnect to fonts.googleapis.com and fonts.gstatic.com. Self-hosted fallback in /fonts/.

**Product line "LIVE RESIN" on packaging:** Cubano Sharp (bold rounded display). This is packaging-only, not used on the website currently.

## Color

### Brand Core
| Name | Hex | Usage |
|------|-----|-------|
| Pablo Blue | #0047BB | Primary brand, nav scroll bg, CTA text, headings on white sections |
| Pablo Yellow | #FDDA00 | Accent, CTA buttons, section labels, text highlights, marquee bg |
| White | #FFFFFF | Text on dark/blue, white section bg |
| Dark | #0A0A0A | Body text on white sections |
| Deep Blue | #001A4D | Body background, dark section bg, footer bg |
| Off-White | #F5F5F3 | Barely used currently, defined in :root |

### Section Backgrounds (the rhythm)
| Class | Background | Text | When |
|-------|-----------|------|------|
| `section--blue` | #0047BB | white | Process, contact, coming soon |
| `section--white` | #FFFFFF | #0A0A0A | Product line cards |
| `section--dark` | #001A4D | white | Flavor bands menu |
| `section--yellow` | #FDDA00 | #0047BB | Features strip |

### Flavor Colors

**WARNING:** CSS (:root variables) and brand_config.py have DIFFERENT hex values for the same flavors. The CSS values are used on the website; brand_config.py values are used in the asset pipeline tools. These need to be reconciled.

| Flavor | CSS (website) | brand_config.py (tools) | Band gradient |
|--------|--------------|------------------------|---------------|
| Pineapple Marker | #EA698C | #EE3680 | 135deg pink gradient |
| Sunday Grape | #6E3FA3 | #81288E | 135deg lavender gradient, purple text |
| Terp Taxi | #FFCD00 | #FDAA00 | Flat yellow, blue text, checker border |
| Mangonada | #FC4C02 | #FDB829 | 135deg orange-to-amber gradient |
| Marmalade | #FCA311 | #FCA311 | 135deg gold gradient, brown text |
| Pie Face | #EE2737 | #189849 | 135deg red gradient |
| Watermelon Gusher | #00855A | #E80029 | 135deg pink-to-green gradient, dark green text |

Flavor bands use custom gradient backgrounds, NOT flat colors. Each band has its own text color matched to contrast. Terp Taxi has a unique checker-pattern bottom border.

## Buttons
- **NO border-radius.** Buttons are completely square (0px radius). This is deliberate.
- `.btn--yellow` — Yellow bg (#FDDA00), blue text (#0047BB). Hover: white bg, blue text
- `.btn--outline` — Transparent, 2px white border. Hover: white bg, blue text
- Padding: 0.8rem 2.5rem
- All caps, Bebas Neue, 0.15em tracking
- Transition: 0.3s ease

## Border Radius
| Element | Radius | Notes |
|---------|--------|-------|
| Buttons | 0px | Square. Non-negotiable |
| Product cards | 2px | Nearly square |
| Nav dropdown | 4px | Subtle rounding |
| Section images | 4px | Subtle rounding |
| Dispensary photo | 8px | One-off inline style exception |

The site is sharp by default. Rounding is rare and always subtle.

## Animation System

This is the site's signature and what makes it feel premium. The primary easing curve is `cubic-bezier(0.16, 1, 0.3, 1)` — a spring-like overshoot that settles.

### Entrance Animations (scroll-triggered via IntersectionObserver)
| Element | Transform | Duration | Easing | Delay |
|---------|-----------|----------|--------|-------|
| Section headings | translateY(60px) skewY(2deg) | 1s | cubic-bezier(0.16, 1, 0.3, 1) | 0.1s |
| Section labels | translateY(40px) | 0.8s | cubic-bezier(0.16, 1, 0.3, 1) | 0s |
| Section body text | translateY(40px) | 1s | cubic-bezier(0.16, 1, 0.3, 1) | 0.25s |
| Section images | scale(0.85) translateY(40px) | 1.2s | cubic-bezier(0.16, 1, 0.3, 1) | 0.3s |
| Product cards | translateY(80px) scale(0.92) rotate(1deg) | 1s | cubic-bezier(0.16, 1, 0.3, 1) | staggered 0.15s |
| Flavor bands | translateX(-100%) | 0.9s | cubic-bezier(0.16, 1, 0.3, 1) | staggered 0.07s |
| Feature strips | translateY(50px) scale(0.9) | 0.9s | cubic-bezier(0.16, 1, 0.3, 1) | staggered 0.15s |
| Generic fade-up | translateY(80px) | 1.2s | cubic-bezier(0.16, 1, 0.3, 1) | — |

### Hero Animations (on page load)
| Element | Animation | Duration | Delay |
|---------|-----------|----------|-------|
| Hero headline | translateY(80px) skewY(3deg) → 0 | 1.2s | 0.3s |
| Yellow span in headline | same as above | 1.2s | 0.5s |
| Hero subtitle | translateY(30px) → 0 | 0.8s | 0.9s |
| Hero CTA button | translateY(30px) → 0 | 0.8s | 1.2s |
| Hero image | translateY(100px) scale(0.9) → 0 | 1.4s | 0.2s |

### Interactive Animations
| Element | Effect | Duration |
|---------|--------|----------|
| Nav links | Yellow underline width 0 → 100% | 0.3s |
| Nav scroll | Transparent → blue bg + shadow | 0.3s |
| Product cards | translateY(-8px) scale(1.02), shadow | 0.4s ease |
| Flavor bands | brightness(1.08) on hover | instant |
| Marquee spans | scale(1.1) on hover | 0.3s |
| Buttons | all 0.3s ease | 0.3s |

### Flavor Rotator
The hero image rotator uses a decelerating spin pattern:
- Starts at 150ms between frames
- Decelerates through: 180, 220, 280, 360, 480, 650, 900, 1200, 1600, 2000, 2400, 2800, 3200ms
- Settles into 3500ms cruise rhythm
- Product card rotators run at steady intervals (2000-2800ms via data-speed attribute)

### Observer Config
```
threshold: 0.1
rootMargin: '0px 0px -5% 0px'
```
Elements observed: `.product-card, .flavors-stack, .section__heading, .section__label, .section__body, .section__img, .section__col--center img, .features-strip .feature, .fade-up`

## Layout

| Property | Value |
|----------|-------|
| Max content width | 1400px |
| Section grid | 2 columns, 4rem gap, centered |
| Product grid | 4 columns at desktop, 2 at 1024px, 1 at 768px |
| Hero | 2-column grid, min-height 100vh, 6rem 3rem padding |
| Section padding | 6rem 3rem (desktop), 3.5rem 1.5rem (mobile) |
| Footer | 3-column grid |

### Experience Page (unique layout)
Full-screen scroll-snap presentation. Each "scene" is 100vh with `scroll-snap-align: start` and `scroll-snap-stop: always`. Film-like progression. Has its own inline styles, does not use styles.css.

## Responsive Breakpoints
| Breakpoint | Changes |
|-----------|---------|
| 1024px | Product grid → 2 columns, features → 2 columns |
| 768px | Nav collapses to hamburger, hero → 1 column (image on top), section grid → 1 column, product grid → 1 column (400px max), footer → 1 column centered |
| 480px | Hero text shrinks to 2.8rem, section headings to 2rem, reduced padding, features → 1 column |

## Spacing
Uses rem units, not a formal token scale. Approximate mapping:

| Rem | Px | Usage |
|-----|-----|-------|
| 0.3rem | ~5px | Tiny margins (tagline) |
| 0.5rem | 8px | Small gaps, label margins |
| 1rem | 16px | Standard gaps, mobile padding |
| 1.5rem | 24px | Nav padding, hero sub margin, body bottom margin |
| 2rem | 32px | Section gaps, mobile menu gaps, CTA top margin |
| 2.5rem | 40px | Button horizontal padding, nav link gaps |
| 3rem | 48px | Section padding (mobile), nav padding, footer padding |
| 4rem | 64px | Section grid gap |
| 6rem | 96px | Section padding (desktop), hero top padding |

## Marquee
Yellow background, blue text. Infinitely scrolling horizontal ticker at 12s per loop. Contains brand phrases: "All Glass. All Gas." / "Fresh Frozen" / "7 Flavors" / "True-to-Plant". Spans scale to 1.1 on hover.

Also: `.marquee--flavors` variant with white background.

## BEM Naming Convention
The site uses BEM: `block__element--modifier`. Examples:
- `.hero__headline`, `.hero__sub`, `.hero__image`
- `.product-card__name`, `.product-card__desc`, `.product-card__img`
- `.section--blue`, `.section--white`, `.section--dark`
- `.btn--yellow`, `.btn--outline`
- `.flavor-band--pineapple-marker`
- `.nav__menu--open`

## Decisions Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04 | Bebas Neue as default font | Site identity IS the condensed type. Headlines, nav, buttons, cards all Bebas |
| 2026-04 | Space Grotesk only for body copy | Geometric sans creates contrast against Bebas. Used sparingly for readability |
| 2026-04 | Square buttons (0px radius) | Matches the sharp, confident brand. No bubbly pill shapes |
| 2026-04 | cubic-bezier(0.16, 1, 0.3, 1) as signature easing | Spring-like overshoot gives the site its premium feel |
| 2026-04 | Alternating section backgrounds | Creates visual pace across the page. Blue/white/dark/yellow rotation |
| 2026-04 | Flavor bands with custom gradients | Each flavor gets its own gradient treatment, text color, and personality |
| 2026-04 | Decelerating hero rotator | Fast initial spin catches attention, settles into browseable rhythm |
| 2026-04 | DESIGN.md formalized from live site | /design-consultation extracted existing patterns rather than inventing new ones |
