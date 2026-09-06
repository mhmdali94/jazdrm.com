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

Notes:

- Pure `#000` is never used. `#fff` appears only as text on saturated teal or dark grounds, where a tint would look dirty.
- Color strategy: **Committed** - teal carries identity across headers, buttons, and section framing; neutrals do the rest.
- Removed in the retheme: the invented `--accent-gold` / `--accent-amber` / `--gradient-gold` (off-brand, "security + gold" cliche), `--shadow-glow`, and the `--transition-bounce` easing.

## Typography

| Language | Family | Fallback | Use |
|---|---|---|---|
| Arabic (primary) | **Cairo** | `'Noto Kufi Arabic', system-ui, sans-serif` | All Arabic UI and content. Headings and body. |
| English | **Cairo** (Latin subset) or **Roboto** | `system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif` | All English UI and content. Keep one family across both languages if Cairo Latin is acceptable. |
| Icons | Font Awesome 5 | - | Existing icon set; keep or replace wholesale, not piecemeal. |

- Cairo weights available: 400 (body), 600 (emphasis, subheads), 700 (headings), 800/900 (hero display only).
- Hierarchy through scale + weight, ratio >=1.25 between steps. Suggested scale (rem): 0.875 / 1 / 1.25 / 1.5 / 1.875 / 2.5 / 3.25.
- Body: 1rem (16px) minimum on the redesign - the current site runs 12-15px, which is too small for the audience. Line height 1.6 for Arabic body, 1.5 for English.
- Body line length capped at 65-75ch (Arabic counts similarly).

## Spacing & Layout

- Content container: **~1280px** max width (current site: 1290px), centered, with comfortable gutters.
- Spacing scale (px): 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96. Vary it for rhythm; do not pad everything equally.
- Border radius: **10px** default for cards/inputs/buttons, **20px** for large feature panels, **9999px** for pills/tags. (Derived from theme `--theme-border-radius` 10/12/20px.) Avoid the 2-3px woo-commerce defaults.
- Direction: RTL is the authored default. Use logical properties (`margin-inline`, `padding-inline`, `inset-inline`) so the English LTR mirror is free.
- Avoid identical card grids and blanket containerization (see PRODUCT.md anti-references).

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

Primary button (solid teal, white text, 10px radius), secondary button (teal outline), quote-request CTA block, product card, category tile, service card, brand/logo grid, branch/location list, bilingual header with language switch, footer with quick links + contact. Firm these up in `shape`.
