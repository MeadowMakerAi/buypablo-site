# Issues Needing Alex's Decision

## 1. Flavor Accent Colors — CSS vs Brand System

The CSS uses colors from the outdated v2-3 spec (3/18). The brand system has newer colors from the 3/25 Barry thread marked as "provisional." Here's the mismatch:

| Flavor | CSS (current) | Brand System (3/25) | Match? |
|---|---|---|---|
| Pineapple Marker | #EA698C | #EE3680 | NO |
| Sunday Grape | #6E3FA3 | #81288E | NO |
| Terp Taxi | #FFCD00 | #FDAA00 | NO |
| Mangonada | #FC4C02 | #FDB829 | NO |
| Marmalade | #FCA311 | gradient (TBD) | NO |
| Pie Face | #EE2737 | #189849 | NO (red vs green) |
| Watermelon Gusher | #00855A | #E80029 | NO (green vs red) |

**Pie Face and Watermelon Gusher appear swapped** between CSS and brand system. CSS has Watermelon=green, Pie Face=red. Brand system says the opposite.

**Decision needed:** Should I update to the 3/25 brand system colors, or are the CSS colors the ones that match the actual packaging Barry delivered? Verify against the .ai files.

## 2. Flavor Naming — "Sundae Grapes" vs "Sunday Grape"

- HTML uses: "Sundae Grapes" (with 'ae', plural)
- Brand system uses: "Sunday Grape" (with 'ay', singular)

**Decision needed:** Which is the canonical name on the packaging?

## 3. Footer Entity Name

Changed from "Meadow Maker Wellness LLC" to "PABLO" since MMW is a dormant entity name. If there's a preferred legal entity for the copyright line, let me know.

## 4. experience.html Color Variables

The experience.html has its own inline color variables that also differ from the brand system:

```
--pm: #EA698C (Pineapple Marker)
--sg: #6E3FA3 (Sundae Grapes)
--tt: #FFCD00 (Terp Taxi)
--mn: #FC4C02 (Mangonada)
--mm: #FCA311 (Marmalade)
--pf: #EE2737 (Pie Face)
--wg: #00855A (Watermelon Gusher)
```

Same mismatch as index.html. When we resolve #1, I'll update both files.

## 5. "Module 5" HTML File

There's a file called `Module 5 - Content: Applied Agentic AI for Organizational Transformation.html` in the project root. This appears to be unrelated course material. Should I remove it?

## 6. TerpSafe™ Trademark

The site uses "TerpSafe™" throughout. Is this an actual trademark filing, or aspirational? If not filed, consider whether to keep the ™ symbol on the public site.
