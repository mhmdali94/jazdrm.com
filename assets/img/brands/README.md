# Authorized-brand logos

Drop the official logo for each brand here and the homepage "العلامات التجارية المعتمدة عالمياً"
wall will use it automatically. Until a file exists, a clean monochrome wordmark is shown instead.

Expected files (exact names):

| File | Brand |
|------|-------|
| `falcon.svg`    | Falcon Safes |
| `diplomat.svg`  | Diplomat |
| `jiabao.svg`    | Jiabao Security |
| `sunpower.svg`  | Sunpower |
| `hikvision.svg` | Hikvision |
| `dahua.svg`     | Dahua Technology |

Guidance:
- **SVG preferred** (crisp at any size). PNG works too: change the extension in
  `build_site.py` -> `get_brand_wall()` and rerun `python3 build_site.py`, or just also
  drop a `<name>.png` and rename it to `.svg` is NOT valid; edit the builder instead.
- Use the **single-colour / mono** version of each logo where the vendor provides one.
  The wall renders every logo greyscale at rest and full colour on hover, so a flat
  one-colour mark reads best.
- Trim whitespace; target roughly 200x64 artboard. The wall caps height at 44px.
- Get official assets from each vendor's brand/press kit, e.g.
  Hikvision and Dahua both publish partner logo packs to authorized dealers.
