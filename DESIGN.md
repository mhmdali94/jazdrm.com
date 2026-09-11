<!-- SEED - derived from the existing jazdrm.com static clone during `/impeccable teach`.
     Run `/impeccable document` for a full token scan of the codebase once the redesign has code. -->

# Design

## Status

Seed document. **Color is settled**: the locked palette and its AA-verified shades are implemented in [assets/css/style.css](assets/css/style.css) (`/impeccable extract`, this session). Fonts are extracted from the live site. Spacing scale, component specs, and motion are still a starting hypothesis to be firmed up during `shape` / `document`.

## Theme

Light. The physical scene: a procurement or facilities manager reviewing a security vendor on an office monitor in daylight, or a homeowner on a phone deciding who to trust with a safe. The mood is calm, institutional, reassuring. No dark mode in scope - the brand reads as daylight-solid, not tactical.

## Color

**LOCKED BY THE OWNER. Do not change, re-tint, or substitute these hues.** The redesign must reuse them exactly. New values are permitted only as tints/shades of these same hues for hover/active/disabled states and surface layering - never a new hue.

The 8 locked hues (Blocksy palette):

| Hex | Name | Role |
|---|---|---|
| `#047E79` | primary | Deep teal. Headers, primary buttons, key links, section accents. |
| `#1FBAB3` | accent | Turquoise. Highlights, icon fills, on-dark emphasis. Fails as text on white (2.4:1) - fills and large text only. |
| `#4F8DA7` | steel blue | Supporting UI, tertiary accents. |
| `#404040` | ink | Body copy. |
| `#E2E7ED` | cloud | Borders, dividers. |
| `#F2F2F2` | mist | Insets, wells. |
| `#F8F9FB` | paper | Page background. |
| `#FFFFFF` | white | Base surface. |
| `#25D366` | whatsapp | Contact affordance ONLY. Never a brand color. |

### Implemented tokens ([assets/css/style.css](assets/css/style.css) `:root`)

Derived steps are shades of `#047E79` only, each checked for WCAG AA:

| Token | Hex | Derivation | Contrast |
|---|---|---|---|
| `--primary` | `#047E79` | locked | 4.92:1 on white (AA normal, tight) |
| `--primary-hover` | `#036B67` | primary x0.85 | 6.3:1 on white |
| `--primary-dark` | `#035B57` | primary x0.72 | 7.96:1 on white - use for teal text on tint chips and for white text on teal bars |
| `--primary-deep` | `#023F3C` | primary x0.50 | 11.8:1 - hero and top-bar grounds |
| `--primary-light` | `#EBF5F4` | primary -> white .92 | pale chip bg (pair with `--primary-dark` or `--ink` text, not `--primary`) |
| `--primary-tint` | `#F0F7F7` | primary -> white .95 | faint hover wash |
| `--accent-cyan` | `#1FBAB3` | locked accent | on-dark / fills only |
| `--secondary` | `#4F8DA7` | locked steel blue | supporting, currently unused |
| `--text-main` | `#2A2A2A` | ink, darker | 14:1 - headings |
| `--text-body` | `#404040` | locked ink | 10:1 |
| `--text-muted` | `#5E6B6A` | teal-tinted gray | 5.5:1 on white, 4.95:1 on mist |
| `--text-light` | `#808C89` | teal-tinted gray | ~3.2:1 - large decorative text only (logo wall) |
| `--bg-dark` | `#14201E` | teal-tinted charcoal | footer; white .75 text = 9:1 |
| `--border-color` | `#E2E7ED` | locked cloud | |

Elevation and rings (all tinted `rgba(2, 63, 60, a)` = deepest brand teal, never flat black):

| Token | Value | Use |
|---|---|---|
| `--shadow-xs … --shadow-xl` | `rgba(2,63,60, .06 → .18)` | cards, panels, modals |
| `--shadow-btn` / `--shadow-btn-hover` | `rgba(2,63,60, .2 / .28)` | pill buttons (`.btn-primary`, `.btn-quote`), active filter tabs |
| `--ring` | `0 0 0 3px rgba(4,126,121, .16)` | soft focus ring on text inputs (the hard `:focus-visible` outline is separate) |

Notes:

- Pure `#000` is never used. `#fff` appears only as text on saturated teal or dark grounds, where a tint would look dirty.
- Color strategy: **Committed** - teal carries identity across headers, buttons, and section framing; neutrals do the rest.
- No bespoke `rgba()` colours in component rules: shadows and rings all reference the tokens above. The one deliberate literal is WhatsApp green `#25D366`.
- Removed in the retheme: the invented `--accent-gold` / `--accent-amber` / `--gradient-gold` (off-brand, "security + gold" cliche), `--shadow-glow`, and the `--transition-bounce` easing. Also swept out (extract pass 2): the pre-retheme Material teal `rgba(0,137,123)` and cyan `rgba(0,188,212)` that had survived in 10 shadow/gradient rules.
- `quieter` pass (two rounds): the goal was fewer competing heavy elements, not less teal. The POV (committed teal) is unchanged.
  - **Hero:** the two-radial cyan/teal glow is now a single faint top-right wash (`rgba(31,186,179,.09)`, transparent by 55%) - the deep-teal ground carries identity, the glow only lights the reading entry point. Decorative `backdrop-filter` is gone from `.hero-badge`, `.btn-secondary`, and `.hero-media-card` (the media card is now a flat `rgba(255,255,255,.05)` panel, shadow `xl`->`lg`; the floating pill also `xl`->`lg`). `.stat-number` weight `900`->`800`; `.hero-title` keeps `900` as the single display anchor.
  - **Dark bands flattened:** `.coverage` lost its dot-texture `background-image` (now flat `--primary-deep`). `.cta-whatsapp-card` lost its `primary-deep`->`primary-dark` gradient (now flat `--primary-deep`) and its shadow `xl`->`md`. Every full-bleed dark region is now a calm plane, not a glossy/textured panel.
  - **Shadows pulled in:** `.clients-banner-wrapper` and `.category-banner-card` from the bespoke `0 8px 24px` literal to `--shadow-sm`; `.division-card:hover` `xl`->`lg`. `.btn-whatsapp-cta` dropped its green (`rgba(37,211,102,a)`) blurred shadow entirely for neutral `--shadow-sm` / `--shadow-md` - a coloured blur on the dark CTA card was reading as an AI-style glow; the bright green fill already identifies the button.
  - **Motion softened:** `.service-card:hover` lift `-6px`->`-4px` (matches `.division-card`), and its icon-box lost the `scale(1.08)` bump (the teal fill is enough feedback).
  - `backdrop-filter` now survives only where functional: the sticky `.site-header`, the `.modal-overlay` scrim, the `.drawer-backdrop` scrim.

## Typography

**One family, both languages: Cairo.** Self-hosted (SIL OFL) at `assets/fonts/` as one variable woff2 per subset (latin / latin-ext / arabic), weight axis 400-900, `font-display: swap`. No external font request; the arabic (RTL) or latin (LTR) subset is `<link rel="preload">`ed per page. `@font-face` is inlined at the top of `style.css`.

| Language | Family | Fallback |
|---|---|---|
| Arabic + English | **Cairo** | `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif` |
| Icons | inline SVG | no icon font |

- Cairo is variable (any weight 400-900). In use: 400 body, 600 emphasis, 700 headings, 800/900 hero display.
- Dropped in the optimize pass: the Google Fonts `@import` and the Outfit + Inter families (Cairo's Latin carries the English pages).
- Hierarchy through scale + weight, ratio >=1.25 between steps. Suggested scale (rem): 0.875 / 1 / 1.25 / 1.5 / 1.875 / 2.5 / 3.25.
- Body: 1rem (16px) minimum on the redesign - the current site runs 12-15px, which is too small for the audience. Line height 1.6 for Arabic body, 1.5 for English.
- Body line length capped at 65-75ch (Arabic counts similarly).

## Spacing & Layout

- Content container: **~1280px** max width (current site: 1290px), centered, with comfortable gutters.
- Spacing scale (px): 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96. Vary it for rhythm; do not pad everything equally.
- Border radius: **10px** default for cards/inputs/buttons, **20px** for large feature panels, **9999px** for pills/tags. (Derived from theme `--theme-border-radius` 10/12/20px.) Avoid the 2-3px woo-commerce defaults.
- Direction: RTL is the authored default. Use logical properties (`margin-inline`, `padding-inline`, `inset-inline`) so the English LTR mirror is free.
- Avoid identical card grids and blanket containerization (see PRODUCT.md anti-references).

### Responsive (`adapt` pass)

- Breakpoints in use: 1024 (hero + footer reflow), 850 (nav collapses to the drawer, top bar hides), 560 (header sheds the quote button, hero pill de-floats), 480 (tighten dense grids).
- **Tap targets**: interactive elements carry a 44px minimum. `.btn-quote` / `.lang-btn` / drawer controls use `min-height: 44px`; footer link lists trade `gap` for `padding-block` so each row is ~44px without visually spreading; `.division-btn` and `.coverage-hq-row` links use `min-height: 44px`. Short text links (footer) clear the 24px AA floor comfortably; exact 44x44 is the target where geometry allows.
- **Mobile header**: below 560px the always-visible `.btn-quote` is hidden (it crowded the row and wrapped). The quote action moves into the drawer footer (`.drawer-cta`: primary quote button + a plain language link). `.header-actions > *` is `flex-shrink: 0` so nothing gets squeezed.
- **Hero on narrow screens**: `.hero-badge` is `max-width: 100%` with a non-shrinking icon so the long eyebrow wraps instead of forcing width; `.hero-title` has `overflow-wrap: break-word`; below 560px the `.hero-floating-pill` drops from absolute (`inset-inline: -20px`, which overhung the card) to static flow beneath the image.
- Chrome headless clamps its viewport at ~500px, so sub-500 widths can't be screenshot-verified here; the fixes above are structural (`max-width`, `flex-shrink`, wrap, static flow) rather than width-tuned.

### Polish pass

- **Copy**: no em-dashes or spaced-hyphen dashes in UI copy. Sentence-level joins use `:` (about lead), Arabic `،` / commas (addresses), or `·` (footer copyright). Day ranges keep the hyphen (`الأحد - الخميس`).
- **Brand name**: English is **Aljazeera Dreams** everywhere (was "Ahlam Aljazeera" in some alt text). The company descriptor is "Contracting & Maintenance" for the name (matches the Arabic legal name `للمقاولات والصيانة`); the header/footer identity line keeps the fuller "Contracting, Maintenance & Security"; `srv_h2` "Comprehensive Contracting & Security Standards" is a service-scope phrase, not the name.
- **Homepage clients section**: dropped the baked `banner-clients.jpg` composite. It duplicated the real `.clients-grid` logo wall right below it (same ~15 logos, twice). The grid is the showcase; the banner stays only on the About page where no grid follows it.
- **Services intro** is `align-self: center` (was `position: sticky`) so the rail sits centred against the taller list instead of top-aligned with a long tail of whitespace.
- `text-wrap: balance` on `.section-title` / `.services-intro-title` / `.hero-title`; `text-wrap: pretty` on lead/subtitle. Progressive - ignored by old engines.
- `.cta-whatsapp-media img` gets `object-position: 28% 42%` so `object-fit: cover` frames the hand and phone and crops out the baked-in corner wordmark that was bleeding at the panel seam.
- Removed the unused `import os` from [build_site.py](build_site.py).

## Iconography

Line icons, consistent stroke weight, `--color-primary` or `--color-ink` fill. Functional only - no decorative clip-art (a current-site problem). One set, used consistently.

## Imagery

Real product and installation photography: safes, vault doors, cashier rooms, CCTV installs, on-site work. Consistent treatment (aspect ratios, subtle duotone or neutral grade toward the teal is acceptable). No generic stock businesspeople. Brand/partner logos shown in a uniform monochrome or original-color lockup grid.

## Motion

- Ease-out only, exponential curves (`ease-out-quart` / `quint`), ~200-320ms. No bounce, no elastic.
- Animate opacity and transform only, never layout properties.
- Honor `prefers-reduced-motion: reduce` - drop transforms, keep instant state changes.
- Motion is confirmation and orientation, not decoration.

## Components (starting set)

Primary button (solid teal, white text, 10px radius), secondary button (teal outline), quote-request CTA block, product card, category tile, brand/logo grid, branch/location list, bilingual header with language switch, footer with quick links + contact. Firm these up in `shape`.

- **Homepage services** are NOT a card grid (`layout` pass). The section is an asymmetric 2-column composition: a sticky intro rail (eyebrow + heading + one lead sentence + a single "Talk to an Engineer" CTA) beside a numbered `01`-`04` capability list with full-width hairline rules between rows. No per-item card, icon box, or per-item button. Collapses to one column at 860px. This replaced 4 identical icon+heading+text+button cards (the "identical card grid" ban).
