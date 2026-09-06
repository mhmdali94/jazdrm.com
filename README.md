# jazdrm.com - Static Website Clone

A complete, 100% offline-functional static clone of [jazdrm.com](https://jazdrm.com/).

## What Was Cloned
- **All Pages (Arabic & English)**:
  - Homepage: `index.html` (Arabic) and `en/index.html` (English)
  - About Us: `about-us/index.html` and `en/about-us/index.html`
  - Contact Us: `contact-us/index.html` and `en/contact-us/index.html`
  - Products Showcase & Catalog: `products/index.html` and `en/products/index.html`
  - Service Request: `service-request/index.html` and `en/service-request/index.html`
  - Technical Support: `technical-support/index.html` and `en/technical-support/index.html`
  - Job Application: `job-application/index.html` and `en/job-application/index.html`
  - Privacy Policy & Terms: `privacy-policy/index.html` and `terms-and-conditions/index.html`
  - All 55+ Product detail pages (`product/<slug>/index.html` and `en/product/<slug>/index.html`)
  - All Product Categories (`product-category/<slug>/index.html` and `en/product-category/<slug>/index.html`)
  - All Brand pages (`العلامة التجارية/<slug>/index.html`)
- **Assets & Media**:
  - Full WordPress Media Library (all 499+ original and thumbnail sizes)
  - High-resolution hero banners, category thumbnails, product galleries
  - Fonts: Cairo, Noto Kufi Arabic, FontAwesome 5/6, Blocksy Icons, Elementor Icons
  - Stylesheets & Scripts: Minified CSS, Blocksy theme runtime, Elementor styles, Swiper sliders
  - Offline relative paths rewritten across all HTML and CSS

---

## How to Run Locally

### Option 1: Using Python
```bash
python3 preview.py
```
Or:
```bash
python3 -m http.server 8080
```
Open [http://localhost:8080](http://localhost:8080) in your browser.

### Option 2: Using NPM
```bash
npm run preview
```

---

## How to Verify Asset Integrity
```bash
python3 check_assets.py
```

---

## Deployment
This folder can be deployed directly to any static web hosting platform:
- **Cloudflare Pages**: Drag and drop or connect via Git.
- **Netlify**: Drag and drop folder into Netlify dashboard.
- **GitHub Pages**: Push branch and set root as GitHub Pages source.
- **Vercel**: Deploy as a static site.
- **Nginx / Apache**: Copy all files to your web root (`/var/www/html/`).
