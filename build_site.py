#!/usr/bin/env python3
"""
Comprehensive Website Builder for jazdrm.com
Generates all Arabic and English pages with the exact brand colors, modern architecture,
complete product catalog, and interactive forms.
"""

import re
import json
from pathlib import Path

ROOT_DIR = Path("/Users/macbook-pro/Desktop/Development/jazdrm.com/jazdrm.com")

with open(ROOT_DIR / "assets" / "data" / "products.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

# Single source of truth for real, filterable product categories.
# (category_key, url_slug, name_ar, name_en, banner_img | None)
PRODUCT_CATEGORIES = [
    ("vault-doors", "أبواب-الخزائن-المحصنة",
     "أبواب غرف الخزائن المحصنة", "Vault & Bunker Room Doors", None),
    ("fireproof-safes", "الخزائن-المقاومة-للحريق",
     "خزائن حديدية", "Steel Safes", None),
    ("filing-cabinets", "دواليب-الملفات",
     "دواليب الملفات المقاومة للحريق", "Fireproof Filing Cabinets", None),
    ("deposit-lockers", "خزائن-الإيداع",
     "خزائن الإيداع وصناديق الأمانات", "Deposit Lockers & Safety Deposit Boxes", None),
    ("security-doors", "الأبواب-الأمنية-ومقاومة-الحريق",
     "باب مقاوم للحريق", "Fire-Resistant Doors", None),
]


# ---------------------------------------------------------------------------
# Product content helpers - keep each language's page in that language only
# ---------------------------------------------------------------------------

def _has_arabic(t):
    return any('؀' <= c <= 'ۿ' for c in (t or ""))


def _is_filler(t):
    t = (t or "")
    return ("هذا النص" in t) or ("مولد النص" in t) or t.strip().lower() in ("write here desc", "desc", "")


def product_desc(p, is_en):
    """A prose description in the requested language, or '' if none exists.
    Never returns the other language's text."""
    ta = (p.get("title_ar") or "").strip()
    te = (p.get("title_en") or "").strip()
    sa = (p.get("short_desc_ar") or "").strip()
    se = (p.get("short_desc_en") or "").strip()
    if is_en:
        for c in (se, sa):
            if c and c not in (te, ta) and not _has_arabic(c) and not _is_filler(c) and len(c) > 25:
                return c
        return ""
    for c in (sa,):
        if c and c != ta and _has_arabic(c) and not _is_filler(c) and len(c) > 15:
            return c
    return ""


_SPEC_LABELS = [
    "Outside(mm)", "Inside(mm)", "Weight(kg)", "Shelf(pc.)", "Shelf(pc)",
    "Shelves(pc.)", "Fire Class", "Fire Rating", "Lock System", "Lock Type",
    "Certification", "Burglary Resistance",
    "Dimension", "Dimensions", "Outside", "Inside", "Overall", "Weight",
    "Capacity", "Shelves", "Shelf", "Boxes", "Drawers", "Locking", "Lock",
    "EMD", "Colour", "Color", "Material", "Body", "Door",
]
_SPEC_LABELS_AR = {
    "Dimension": "الأبعاد", "Dimensions": "الأبعاد", "Overall": "الأبعاد الكلية",
    "Outside": "الأبعاد الخارجية", "Inside": "الأبعاد الداخلية",
    "Outside(mm)": "الأبعاد الخارجية (مم)", "Inside(mm)": "الأبعاد الداخلية (مم)",
    "Weight": "الوزن", "Weight(kg)": "الوزن (كجم)", "Capacity": "حجم الخزانة",
    "Shelf": "الأرفف", "Shelves": "الأرفف", "Boxes": "الأدراج", "Drawers": "عدد الرفوف",
    "Locking": "نظام الإغلاق", "Lock": "القفل", "EMD": "فتحة الطوارئ (EMD)",
    "Fire Class": "مقاومة الحريق", "Fire Rating": "مدة مقاومة الحريق",
    "Lock System": "نظام القفل", "Lock Type": "نوع القفل الإختياري",
    "Certification": "الشهادة", "Burglary Resistance": "مقاومة السطو",
    "Colour": "اللون", "Color": "اللون", "Material": "الخامة",
    "Body": "الهيكل", "Door": "الباب",
}

_ICON_BOX = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 7.5L12 3 3 7.5v9L12 21l9-4.5v-9z"/><path d="M3 7.5l9 4.5 9-4.5M12 12v9"/></svg>'
_ICON_WEIGHT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 7a3 3 0 0 1 6 0"/><path d="M6.5 7h11l1.5 13h-14L6.5 7z"/></svg>'
_ICON_LOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>'
_ICON_KEY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="8" cy="15" r="4"/><path d="M10.8 12.2L20 3M20 3v4.5M20 3h-4.5"/></svg>'
_ICON_GRID = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7.5" height="7.5" rx="1"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1"/></svg>'
_ICON_FLAME = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3c-1.5 3-5 5-5 10a5 5 0 0 0 10 0c0-1.5-.5-2.5-1.5-3.5 0 2-1 3-2 2.5 1.5-3.5-.5-6.5-1.5-9z"/></svg>'
_ICON_CERT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="5.5"/><path d="M9 13.5L7 21l5-3 5 3-2-7.5"/></svg>'
_ICON_SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l7.5 3v5.5c0 5-3.2 7.8-7.5 9-4.3-1.2-7.5-4-7.5-9V6L12 3z"/></svg>'
_ICON_PALETTE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.5" fill="currentColor" stroke="none"/></svg>'
_ICON_LAYERS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/></svg>'
_ICON_WINDOW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 12h16M12 4v16"/></svg>'

_SPEC_ICONS = {
    "Dimension": _ICON_BOX, "Dimensions": _ICON_BOX, "Overall": _ICON_BOX,
    "Outside": _ICON_BOX, "Inside": _ICON_BOX, "Outside(mm)": _ICON_BOX, "Inside(mm)": _ICON_BOX,
    "Weight": _ICON_WEIGHT, "Weight(kg)": _ICON_WEIGHT,
    "Locking": _ICON_LOCK, "Lock": _ICON_LOCK, "Lock System": _ICON_LOCK, "Lock Type": _ICON_LOCK,
    "Capacity": _ICON_KEY,
    "Shelf": _ICON_GRID, "Shelves": _ICON_GRID, "Boxes": _ICON_GRID, "Drawers": _ICON_GRID,
    "Shelf(pc.)": _ICON_GRID, "Shelf(pc)": _ICON_GRID, "Shelves(pc.)": _ICON_GRID,
    "Fire Class": _ICON_FLAME, "Fire Rating": _ICON_FLAME,
    "Certification": _ICON_CERT, "Burglary Resistance": _ICON_SHIELD,
    "Colour": _ICON_PALETTE, "Color": _ICON_PALETTE,
    "Material": _ICON_LAYERS, "Body": _ICON_LAYERS, "Door": _ICON_LAYERS,
    "EMD": _ICON_WINDOW,
}


def parse_specs(p, is_en):
    """Turn the run-together spec text in full_desc_ar into [(label, value)] rows.
    This is factual product data (dimensions, weight, lock type) reformatted for reading."""
    fa = (p.get("full_desc_ar") or "").strip()
    if _is_filler(fa) or not re.search(r"\d", fa):
        return []
    # A label only counts as a field boundary when it is followed by a colon.
    pat = re.compile(r"(" + "|".join(re.escape(l) for l in
                     sorted(_SPEC_LABELS, key=len, reverse=True)) + r")\s*:\s*", re.I)
    matches = list(pat.finditer(fa))
    rows, seen = [], set()
    for i, m in enumerate(matches):
        label = m.group(1)
        end = matches[i + 1].start() if i + 1 < len(matches) else len(fa)
        val = re.sub(r"\s+", " ", fa[m.end():end]).strip(" :.,-")
        if not val or len(val) > 70:
            continue
        canon = next((L for L in _SPEC_LABELS if L.lower() == label.lower()), label)
        key = canon.lower()
        if key in seen:
            continue
        seen.add(key)
        disp = canon if is_en else _SPEC_LABELS_AR.get(canon, canon)
        rows.append((disp, val, canon))
    return rows if len(rows) >= 2 else []


_FIELD_RE = re.compile(
    r'(<label class="form-label"[^>]*>)(.*?)(</label>\s*)'
    r'(<(?:input|select|textarea)\b)([^>]*?)(\s*/?>)',
    re.S)


def wire_form(html, prefix):
    """Give every .form-label / .form-control pair a real for/id link in the markup
    (the JS association stays as a fallback for older pages)."""
    counter = [0]

    def repl(m):
        lbl_open, text, close, ctrl, attrs, end = m.groups()
        existing = re.search(r'\bid="([^"]+)"', attrs)
        if existing:
            fid, new_attrs = existing.group(1), attrs
        else:
            counter[0] += 1
            fid = f"{prefix}-{counter[0]}"
            req = ' aria-required="true"' if re.search(r'\brequired\b', attrs) else ''
            new_attrs = f' id="{fid}"{req}{attrs}'
        if "for=" not in lbl_open:
            lbl_open = lbl_open[:-1] + f' for="{fid}">'
        return lbl_open + text + close + ctrl + new_attrs + end

    return _FIELD_RE.sub(repl, html)


def get_header(is_en=False, depth=0):
    rel = "../" * depth
    lang_toggle_url = f"{rel}en/index.html" if not is_en else f"{rel}index.html"
    lang_label = "EN" if not is_en else "العربية"
    lang_target = "English" if not is_en else "العربية"

    t = {
        "phone": "+966920028440",
        "phone_display": "+966920028440",
        "hours": "الأحد - الخميس: 9:00 ص - 5:00 م" if not is_en else "Sun - Thu: 9:00 AM - 5:00 PM",
        "main_branch": "الرياض - المملكة العربية السعودية" if not is_en else "Riyadh - Kingdom of Saudi Arabia",
        "service_req": "طلب خدمة" if not is_en else "Request Service",
        "tech_support": "الدعم الفني" if not is_en else "Tech Support",
        "careers": "التوظيف" if not is_en else "Careers",
        "brand_title": "شركة أحلام الجزيرة" if not is_en else "Aljazeera Dreams",
        "brand_sub": "للمقاولات" if not is_en else "Contracting",
        "home": "الرئيسية" if not is_en else "Home",
        "services": "خدماتنا" if not is_en else "Our Services",
        "products": "منتجاتنا" if not is_en else "Products",
        "partners": "عملاؤنا" if not is_en else "Clients & Partners",
        "about": "نبذة عنا" if not is_en else "About Us",
        "contact": "اتصل بنا" if not is_en else "Contact Us",
        "quote_btn": "طلب تسعير" if not is_en else "Request Quote",
        "menu_label": "فتح القائمة" if not is_en else "Open menu",
        "nav_primary": "التنقل الرئيسي" if not is_en else "Primary",
        "nav_categories": "تصنيفات المنتجات" if not is_en else "Product categories",
        "nav_drawer": "قائمة الجوال" if not is_en else "Mobile menu",
        "close": "إغلاق" if not is_en else "Close",
    }

    prefix = f"{rel}en/" if is_en else f"{rel}"
    home_url = f"{prefix}index.html"
    about_url = f"{prefix}about-us/index.html"
    products_url = f"{prefix}products/index.html"
    services_url = f"{prefix}services/index.html"
    contact_url = f"{prefix}contact-us/index.html"
    service_req_url = f"{prefix}service-request/index.html"
    tech_support_url = f"{prefix}technical-support/index.html"
    careers_url = f"{prefix}job-application/index.html"

    cat_urls = [
        (key, f"{prefix}product-category/{slug}/index.html", name_en if is_en else name_ar)
        for key, slug, name_ar, name_en, _banner in PRODUCT_CATEGORIES
    ]

    return f"""
  <!-- Top Bar -->
  <div class="top-bar">
    <div class="container">
      <div class="top-bar-contact">
        <a href="tel:+966920028440" class="top-bar-item">
          <svg viewBox="0 0 24 24"><path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24 11.72 11.72 0 003.68.59 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1 11.72 11.72 0 00.59 3.68 1 1 0 01-.24 1.02l-2.23 2.09z"/></svg>
          <span>{t['phone_display']}</span>
        </a>
        <div class="top-bar-item">
          <svg viewBox="0 0 24 24"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/></svg>
          <span>{t['hours']}</span>
        </div>
      </div>
      <div class="top-bar-links">
        <a href="{service_req_url}">{t['service_req']}</a>
        <a href="{tech_support_url}">{t['tech_support']}</a>
        <a href="{careers_url}">{t['careers']}</a>
      </div>
    </div>
  </div>

  <!-- Main Header -->
  <header class="site-header">
    <div class="container">
      <div class="main-navbar">
        <a href="{home_url}" class="brand-logo">
          <img src="{rel}assets/img/brand-icon.png" alt="{t['brand_title']}" width="500" height="500">
          <div class="brand-text">
            <span class="brand-title">{t['brand_title']}</span>
            <span class="brand-subtitle">{t['brand_sub']}</span>
          </div>
        </a>

        <!-- Desktop Navigation Menu -->
        <nav class="nav-menu" aria-label="{t['nav_primary']}">
          <div class="nav-item">
            <a href="{home_url}" class="nav-link">{t['home']}</a>
          </div>
          <div class="nav-item">
            <a href="{services_url}" class="nav-link">{t['services']}</a>
          </div>
          <div class="nav-item">
            <a href="{products_url}" class="nav-link">{t['products']}</a>
          </div>
          <div class="nav-item">
            <a href="{home_url}#partners" class="nav-link">{t['partners']}</a>
          </div>
          <div class="nav-item">
            <a href="{about_url}" class="nav-link">{t['about']}</a>
          </div>
          <div class="nav-item">
            <a href="{contact_url}" class="nav-link">{t['contact']}</a>
          </div>
        </nav>

        <!-- Actions -->
        <div class="header-actions">
          <a href="{lang_toggle_url}" class="lang-btn" title="{lang_target}">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12.87 15.07l-2.54-2.51.03-.03A17.52 17.52 0 0014.07 6H17V4h-7V2H8v2H1v2h11.17C11.5 7.92 10.44 9.75 9 11.35 8.07 10.32 7.3 9.19 6.69 8h-2c.73 1.63 1.73 3.17 2.98 4.56l-5.09 5.02L4 19l5-5 3.11 3.11.76-2.04zM18.5 10h-2L12 22h2l1.12-3h4.75L21 22h2l-4.5-12zm-2.62 7l1.62-4.33L19.12 17h-3.24z"/></svg>
            <span>{lang_label}</span>
          </a>
          <button class="btn-quote open-quote-modal">{t['quote_btn']}</button>
          <button type="button" class="mobile-toggle-btn" aria-label="{t['menu_label']}" aria-expanded="false" aria-controls="mobile-drawer">
            <span></span><span></span><span></span>
          </button>
        </div>
      </div>
    </div>

    <!-- Secondary Category Navigation Bar -->
    <nav class="category-nav-bar" aria-label="{t['nav_categories']}">
      <div class="container">
        <div class="category-menu">
{chr(10).join(f'          <div class="nav-item"><a href="{url}" class="nav-link">{name}</a></div>' for _key, url, name in cat_urls)}
        </div>
      </div>
    </nav>
  </header>

  <!-- Mobile Drawer -->
  <div class="drawer-backdrop"></div>
  <div class="mobile-drawer" id="mobile-drawer" aria-label="{t['nav_drawer']}" aria-hidden="true">
    <div class="mobile-drawer-header">
      <div class="brand-logo">
        <img src="{rel}assets/img/brand-icon.png" alt="{t['brand_title']}" width="500" height="500" style="height: 38px;">
        <span class="brand-title" style="font-size: 1.1rem;">{t['brand_title']}</span>
      </div>
      <button type="button" class="drawer-close-btn" aria-label="{t['close']}">&times;</button>
    </div>
    <nav class="mobile-drawer-body" aria-label="{t['nav_drawer']}">
      <a href="{home_url}" class="nav-link">{t['home']}</a>
      <a href="{services_url}" class="nav-link">{t['services']}</a>
      <a href="{products_url}" class="nav-link">{t['products']}</a>
{chr(10).join(f'      <a href="{url}" class="nav-link">{name}</a>' for _key, url, name in cat_urls)}
      <a href="{about_url}" class="nav-link">{t['about']}</a>
      <a href="{service_req_url}" class="nav-link">{t['service_req']}</a>
      <a href="{tech_support_url}" class="nav-link">{t['tech_support']}</a>
      <a href="{careers_url}" class="nav-link">{t['careers']}</a>
      <a href="{contact_url}" class="nav-link">{t['contact']}</a>
      <div class="drawer-cta">
        <button type="button" class="btn-primary open-quote-modal">{t['quote_btn']}</button>
        <a href="{lang_toggle_url}" class="drawer-lang">{lang_target}</a>
      </div>
    </nav>
  </div>
"""

def get_footer(is_en=False, depth=0):
    rel = "../" * depth
    prefix = f"{rel}en/" if is_en else f"{rel}"
    home_url = f"{prefix}index.html"
    about_url = f"{prefix}about-us/index.html"
    products_url = f"{prefix}products/index.html"
    services_url = f"{prefix}services/index.html"
    contact_url = f"{prefix}contact-us/index.html"
    privacy_url = f"{prefix}privacy-policy/index.html"
    terms_url = f"{prefix}terms-and-conditions/index.html"
    service_req_url = f"{prefix}service-request/index.html"
    tech_support_url = f"{prefix}technical-support/index.html"

    cat_urls = [
        (f"{prefix}product-category/{slug}/index.html", name_en if is_en else name_ar)
        for _key, slug, name_ar, name_en, _banner in PRODUCT_CATEGORIES
    ]

    t = {
        "about_p": "شركة أحلام الجزيرة للمقاولات: رواد تزويد وتركيب الخزائن والأبواب الأمنية المحصنة، ودواليب الملفات المقاومة للحريق، والأقفال الذكية لكبرى البنوك والشركات والمؤسسات في المملكة." if not is_en else "Aljazeera Dreams Contracting: pioneers in security safes, bunker vault doors, fireproof filing cabinets, and smart locks for major banks and corporations across Saudi Arabia.",
        "nav_title": "روابط سريعة" if not is_en else "Quick Links",
        "cats_title": "التصنيفات" if not is_en else "Categories",
        "contact_title": "تواصل معنا" if not is_en else "Contact Us",
        "address": "الرياض (الفرع الرئيسي)، حي الروابي، شارع طاهر الدباغ" if not is_en else "Riyadh (Main HQ), Al-Rawabi, Taher Al-Dabbagh St.",
        "branches": "فروعنا: الرياض، جدة، الدمام، المدينة المنورة، بريدة، تبوك، الطائف" if not is_en else "Branches: Riyadh, Jeddah, Dammam, Medina, Buraydah, Tabuk, Taif",
        "copyright": "جميع الحقوق محفوظة © 2026 · شركة أحلام الجزيرة للمقاولات" if not is_en else "All Rights Reserved © 2026 · Aljazeera Dreams Co.",
        "privacy": "سياسة الخصوصية" if not is_en else "Privacy Policy",
        "terms": "الشروط والأحكام" if not is_en else "Terms & Conditions",
    }

    return wire_form(f"""
  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-about">
          <div class="brand-logo" style="margin-bottom: 12px;">
            <img src="{rel}assets/img/brand-icon.png" alt="شركة أحلام الجزيرة" width="500" height="500" style="height: 48px;">
            <span class="brand-title" style="color: #fff; font-size: 1.2rem;">{'شركة أحلام الجزيرة' if not is_en else 'Aljazeera Dreams'}</span>
          </div>
          <p>{t['about_p']}</p>
        </div>
        <div>
          <h3 class="footer-title">{t['nav_title']}</h3>
          <div class="footer-links">
            <a href="{home_url}">{'الرئيسية' if not is_en else 'Home'}</a>
            <a href="{about_url}">{'نبذة عنا' if not is_en else 'About Us'}</a>
            <a href="{services_url}">{'خدماتنا' if not is_en else 'Our Services'}</a>
            <a href="{products_url}">{'منتجاتنا' if not is_en else 'Products'}</a>
            <a href="{service_req_url}">{'طلب خدمة' if not is_en else 'Service Request'}</a>
            <a href="{tech_support_url}">{'الدعم الفني' if not is_en else 'Technical Support'}</a>
            <a href="{contact_url}">{'اتصل بنا' if not is_en else 'Contact Us'}</a>
          </div>
        </div>
        <div>
          <h3 class="footer-title">{t['cats_title']}</h3>
          <div class="footer-links">
{chr(10).join(f'            <a href="{url}">{name}</a>' for url, name in cat_urls)}
          </div>
        </div>
        <div>
          <h3 class="footer-title">{t['contact_title']}</h3>
          <div class="footer-links">
            <p style="color: rgba(255,255,255,0.7); font-size: 0.875rem; margin-bottom: 8px;">{t['address']}</p>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.875rem; margin-bottom: 12px;">{t['branches']}</p>
            <a href="tel:+966920028440" style="color: var(--accent-cyan); font-weight: 700; font-size: 1.1rem;">+966920028440</a>
            <a href="tel:+966114718033" style="color: rgba(255,255,255,0.85); font-weight: 600; font-size: 0.9rem;">+966 11 471 8033</a>
            <a href="https://wa.me/966554890900" target="_blank" style="color: #25d366; font-weight: 600;">+966 55 489 0900 (WhatsApp)</a>
            <a href="mailto:info@jazdrm.com" style="color: rgba(255,255,255,0.85); font-weight: 600; font-size: 0.9rem;">info@jazdrm.com</a>
            <a href="mailto:wafi@jazdrm.com" style="color: rgba(255,255,255,0.85); font-weight: 600; font-size: 0.9rem;">wafi@jazdrm.com</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>{t['copyright']}</p>
        <div style="display: flex; gap: 20px;">
          <a href="{privacy_url}">{t['privacy']}</a>
          <a href="{terms_url}">{t['terms']}</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- Floating Buttons -->
  <div class="floating-actions">
    <a href="https://wa.me/966554890900" target="_blank" rel="noopener" class="floating-btn floating-whatsapp" aria-label="{'تواصل عبر واتساب' if not is_en else 'Chat on WhatsApp'}" title="{'واتساب' if not is_en else 'WhatsApp'}">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
    </a>
    <a href="tel:+966920028440" class="floating-btn floating-phone" aria-label="{'اتصل بنا' if not is_en else 'Call us'}" title="{'اتصل بنا' if not is_en else 'Call us'}">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.28.67-.36 1.02-.25 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
    </a>
  </div>

  <!-- Quote Modal -->
  <div class="modal-overlay" id="quote-modal">
    <div class="modal-content" role="dialog" aria-modal="true" aria-labelledby="quote-modal-title">
      <div class="modal-header">
        <h3 class="modal-title" id="quote-modal-title">{'طلب عرض سعر / تسعير' if not is_en else 'Request a Quotation'}</h3>
        <button type="button" class="modal-close" aria-label="{'إغلاق' if not is_en else 'Close'}">&times;</button>
      </div>
      <div class="modal-body">
        <form>
          <div class="form-group">
            <label class="form-label">{'الاسم الكامل' if not is_en else 'Full Name'} *</label>
            <input type="text" class="form-control" required placeholder="{'مثال: محمد علي' if not is_en else 'e.g. John Doe'}">
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">{'رقم الجوال' if not is_en else 'Phone Number'} *</label>
              <input type="tel" class="form-control" required placeholder="05xxxxxxxx">
            </div>
            <div class="form-group">
              <label class="form-label">{'المدينة / الفرع' if not is_en else 'City / Branch'} *</label>
              <select class="form-control" required>
                <option value="riyadh">{'الرياض (الفرع الرئيسي)' if not is_en else 'Riyadh (Main HQ)'}</option>
                <option value="jeddah">{'جدة' if not is_en else 'Jeddah'}</option>
                <option value="dammam">{'الدمام' if not is_en else 'Dammam'}</option>
                <option value="medina">{'المدينة المنورة' if not is_en else 'Medina'}</option>
                <option value="tabuk">{'تبوك' if not is_en else 'Tabuk'}</option>
                <option value="buraydah">{'بريدة' if not is_en else 'Buraydah'}</option>
                <option value="taif">{'الطائف' if not is_en else 'Taif'}</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">{'المنتج أو الخدمة المطلوبة' if not is_en else 'Required Product / Service'}</label>
            <input type="text" id="modal-product-name" class="form-control" placeholder="{'أدخل اسم المنتج أو نوع الخدمة' if not is_en else 'Enter product name or service'}">
          </div>
          <div class="form-group">
            <label class="form-label">{'تفاصيل إضافية أو متطلبات خاصة' if not is_en else 'Additional Notes'}</label>
            <textarea class="form-control" rows="3" placeholder="{'اكتب تفاصيل طلبك هنا...' if not is_en else 'Write your requirements here...'}"></textarea>
          </div>
          <button type="submit" class="btn-primary" style="width: 100%; justify-content: center; margin-top: 10px;">
            {'إرسال الطلب الآن' if not is_en else 'Submit Request Now'}
          </button>
        </form>
      </div>
    </div>
  </div>
""", "qm")


def _asset_ver(rel_path):
    """Short content hash for cache-busting (?v=...). Without this, browsers and
    dev servers happily keep serving a stale copy of products-data.js/style.css/
    main.js after a rebuild - a real static-site footgun, not a hypothetical one."""
    import hashlib
    full = ROOT_DIR / rel_path
    return hashlib.md5(full.read_bytes()).hexdigest()[:8]


def generate_base_html(title, body_content, is_en=False, depth=0, needs_products=False):
    rel = "../" * depth
    dir_attr = 'dir="ltr" lang="en"' if is_en else 'dir="rtl" lang="ar"'
    body_cls = 'en-lang' if is_en else 'ar-lang'
    skip_label = 'تخطي إلى المحتوى' if not is_en else 'Skip to content'
    v_css = _asset_ver("assets/css/style.css")
    v_main = _asset_ver("assets/js/main.js")
    products_script = ""
    if needs_products:
        v_products = _asset_ver("assets/js/products-data.js")
        products_script = f'\n  <script src="{rel}assets/js/products-data.js?v={v_products}"></script>'

    header = get_header(is_en=is_en, depth=depth)
    footer = get_footer(is_en=is_en, depth=depth)

    return f"""<!DOCTYPE html>
<html {dir_attr}>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {'شركة أحلام الجزيرة' if not is_en else 'Aljazeera Dreams Co.'}</title>
  <meta name="description" content="{'شركة أحلام الجزيرة للمقاولات: حلول الخزائن والأبواب الأمنية، دواليب الملفات المقاومة للحريق، والأقفال الذكية' if not is_en else 'Aljazeera Dreams Contracting: premium security safes, vault doors, fireproof filing cabinets, and smart locks in Saudi Arabia'}">
  <link rel="icon" href="{rel}wp-content/uploads/2025/06/cropped-favicon-32x32.png" sizes="32x32">
  <link rel="icon" href="{rel}wp-content/uploads/2025/06/cropped-favicon-192x192.png" sizes="192x192">
  <link rel="apple-touch-icon" href="{rel}wp-content/uploads/2025/06/cropped-favicon-180x180.png">
  <link rel="preload" href="{rel}assets/fonts/{'cairo-latin.woff2' if is_en else 'cairo-arabic.woff2'}" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{rel}assets/css/style.css?v={v_css}">
</head>
<body class="{body_cls}" data-root="{rel}">
  <a class="skip-link" href="#main-content">{skip_label}</a>
  {header}
  <main id="main-content" tabindex="-1">
    {body_content}
  </main>
  {footer}
{products_script}
  <script src="{rel}assets/js/main.js?v={v_main}"></script>
</body>
</html>
"""

def get_brand_wall(is_en=False, rel=""):
    """Monochrome wordmark wall for the globally-authorized product brands."""
    cat_prefix = f"{rel}en/" if is_en else f"{rel}"
    products_cat = f"{cat_prefix}products/index.html"
    view = "استعراض المنتجات" if not is_en else "View products"

    G = {
        "vault": '<rect x="3.5" y="4.5" width="17" height="15" rx="1.5"/><circle cx="10" cy="12" r="3"/><path d="M10 12l1.8-1.8"/><path d="M16.5 9.2v5.6"/>',
        "shield": '<path d="M12 3.2l7 2.6v4.9c0 4.3-2.9 7.6-7 8.9-4.1-1.3-7-4.6-7-8.9V5.8z"/><path d="M9 12l2.1 2.1L15.2 10"/>',
        "fingerprint": '<path d="M12 4.6c-4 0-7 2.9-7 7.1 0 1.4.2 2.7.6 3.8"/><path d="M8.5 12c0-1.9 1.5-3.4 3.5-3.4s3.5 1.5 3.5 3.4c0 2 0 4-1 5.8"/><path d="M12 12v3.2c0 1.4-.3 2.7-.8 3.9"/><path d="M18.4 15.6c.4-1.2.6-2.4.6-3.6 0-1.6-.5-3-1.4-4.2"/>',
        "lock": '<rect x="5" y="11" width="14" height="9" rx="1.5"/><path d="M8 11V7.5a4 4 0 018 0V11"/><circle cx="12" cy="15.3" r="1.4"/>',
    }

    brands = [
        ("falcon",     "falcon.png",     "FALCON",    "SAFES",             G["vault"],       products_cat),
        ("diplomat",   "diplomat.png",   "DIPLOMAT",  "",                  G["shield"],      products_cat),
        ("jiabao",     "jiabao.svg",     "JIABAO",    "SECURITY",          G["fingerprint"], products_cat),
        ("godrej",     "godrej.png",     "GODREJ",    "SECURITY SOLUTIONS",G["shield"],      products_cat),
        ("xyoungann",  "xyoungann.png",  "X YOUNG ANN","",                 G["vault"],       products_cat),
        ("ooilsafi",   "ooilsafi.png",   "B.I.",      "OOIL SAFI",         G["lock"],        products_cat),
    ]

    cells = []
    for key, fil, name, sub, glyph, href in brands:
        full = f"{name} {sub}".strip()
        sub_html = f'<span class="brand-mark-sub">{sub}</span>' if sub else ""
        cells.append(f"""        <li class="brand-wall-item">
          <a class="brand-mark brand-mark--{key}" href="{href}" aria-label="{full} - {view}">
            <img class="brand-mark-logo" src="{rel}assets/img/brands/{fil}" alt="" width="220" height="52" decoding="async"
                 onload="this.closest('.brand-mark').classList.add('brand-mark--haslogo')" onerror="this.remove()">
            <span class="brand-mark-fallback" aria-hidden="true">
              <svg class="brand-mark-glyph" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{glyph}</svg>
              <span class="brand-mark-text"><span class="brand-mark-name">{name}</span>{sub_html}</span>
            </span>
          </a>
        </li>""")
    return "\n".join(cells)


def get_coverage(is_en=False):
    """Nationwide coverage band: featured HQ + regional branch list."""
    regions = [
        ("جدة", "Jeddah", "المنطقة الغربية", "Western Region"),
        ("الدمام", "Dammam", "المنطقة الشرقية", "Eastern Region"),
        ("المدينة المنورة", "Madinah", "منطقة المدينة المنورة", "Madinah Region"),
        ("تبوك", "Tabuk", "المنطقة الشمالية", "Northern Region"),
        ("بريدة", "Buraydah", "منطقة القصيم", "Qassim Region"),
        ("الطائف", "Taif", "منطقة مكة المكرمة", "Makkah Region"),
    ]
    rows = "\n".join(
        f'            <li class="coverage-branch">'
        f'<span class="coverage-dot" aria-hidden="true"></span>'
        f'<span class="coverage-city">{en if is_en else ar}</span>'
        f'<span class="coverage-region">{ren if is_en else rar}</span></li>'
        for ar, en, rar, ren in regions
    )
    hq_city = "الرياض" if not is_en else "Riyadh"
    hq_tag = "الفرع الرئيسي" if not is_en else "Head Office"
    hq_addr = ("حي الروابي، شارع طاهر الدباغ، الرياض، المملكة العربية السعودية"
               if not is_en else
               "Al-Rawabi District, Taher Al-Dabbagh St., Riyadh, Saudi Arabia")
    hq_hours = "الأحد - الخميس: 9:00 ص - 5:00 م" if not is_en else "Sun - Thu: 9:00 AM - 5:00 PM"
    others = "الفروع الإقليمية" if not is_en else "Regional branches"
    maps_label = "الموقع على الخريطة" if not is_en else "View on the map"
    maps_url = "https://www.google.com/maps/search/?api=1&query=" + \
        "Ahlam+Aljazeera+Al-Rawabi+Taher+Al-Dabbagh+Riyadh"
    pin_svg = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
               '<path d="M12 2a7 7 0 00-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 00-7-7zm0 9.5A2.5 2.5 0 1112 6.5a2.5 2.5 0 010 5z"/></svg>')
    clock_svg = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
                 '<path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 10.6l4 2.3-.9 1.5L11 13V6h2z"/></svg>')
    phone_svg = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
                 '<path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24 11.72 11.72 0 003.68.59 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1 11.72 11.72 0 00.59 3.68 1 1 0 01-.24 1.02l-2.23 2.09z"/></svg>')
    return f"""
        <div class="coverage-grid">
          <div class="coverage-hq">
            <span class="coverage-hq-tag">{hq_tag}</span>
            <h3 class="coverage-hq-city">{hq_city}</h3>
            <p class="coverage-hq-addr">{hq_addr}</p>
            <div class="coverage-hq-meta">
              <p class="coverage-hq-row">{clock_svg}<span>{hq_hours}</span></p>
              <a href="tel:+966920028440" class="coverage-hq-row coverage-hq-phone">{phone_svg}<span>+966920028440</span></a>
              <a href="{maps_url}" target="_blank" rel="noopener" class="coverage-hq-row coverage-hq-map">{pin_svg}<span>{maps_label}</span></a>
            </div>
          </div>
          <div class="coverage-regions">
            <p class="coverage-regions-label">{others}</p>
            <ul class="coverage-list">
{rows}
            </ul>
          </div>
        </div>"""


def get_clients(is_en=False, rel=""):
    """Trusted-by strip: the 17 partners listed on the corporate profile's
    'شركاء النجاح' page (pdf/01-item-01.pdf, page 14)."""
    clients = [
        ("saudi-investment-bank", "البنك السعودي للاستثمار", "The Saudi Investment Bank"),
        ("albilad", "بنك البلاد", "Bank Albilad"),
        ("aljazira", "بنك الجزيرة", "Bank AlJazira"),
        ("alinma", "مصرف الإنماء", "Alinma Bank"),
        ("alrajhi", "مصرف الراجحي", "Al Rajhi Bank"),
        ("fransi", "البنك السعودي الفرنسي", "Banque Saudi Fransi"),
        ("gib", "بنك الخليج الدولي", "Gulf International Bank"),
        ("muscat", "بنك مسقط", "Bank Muscat"),
        ("snb", "البنك الأهلي السعودي", "Saudi National Bank"),
        ("riyad", "بنك الرياض", "Riyad Bank"),
        ("anb", "البنك العربي الوطني", "Arab National Bank"),
        ("ersal", "إرسال لتحويل الأموال", "Ersal Money Transfer"),
        ("amnco", "امنكو", "AMNCO"),
        ("nadheer", "شركة النذير للصرافة", "Al Nadheer Exchange Co."),
        ("emirates-nbd", "بنك الإمارات دبي الوطني", "Emirates NBD"),
        ("omlah", "شركة عملة للصرافة", "Omlah Exchange Co."),
        ("sab", "البنك السعودي الأول", "Saudi Awwal Bank (SAB)"),
        ("enjaz", "بنك انجاز", "Enjaz Bank"),
        ("mahmal", "شركة المحمل لخدمات المرافق", "Mahmal Facilities Services"),
        ("masdar", "شركة مصدر", "Masdar"),
        ("el-seif", "السيف مهندسون مقاولون", "El Seif Engineering Contracting"),
    ]
    return "\n".join(
        f'          <li class="client-logo">'
        f'<img src="{rel}assets/img/clients/{slug}.png" alt="{en if is_en else ar}" width="200" height="150" '
        f'loading="lazy" decoding="async" '
        f'onerror="this.closest(\'.client-logo\').remove()"></li>'
        for slug, ar, en in clients
    )


# ---- Shared page fragments (homepage / about / contact) ----------------------
_ARROW_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">'
              '<path d="M5 12h14M12 5l7 7-7 7"/></svg>')
_WA_GLYPH = (
    "M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966"
    "-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653"
    "-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198"
    ".05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01"
    "-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074"
    ".149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085"
    " 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h"
    "-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51"
    "-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994"
    "c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157"
    " 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554"
    " 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"
)


def get_clients_banner(is_en=False, rel="", style=""):
    alt = ("شركاؤنا في النجاح - كبرى البنوك والمصارف في المملكة" if not is_en
           else "Partners in Success - Leading Banks & Institutions in Saudi Arabia")
    st = f' style="{style}"' if style else ""
    return (f'<div class="clients-banner-wrapper"{st}>\n'
            f'          <img src="{rel}assets/img/banners/banner-clients.jpg" alt="{alt}" width="1200" height="338" loading="lazy">\n'
            f'        </div>')


def division_card(img, alt, tag, title, desc, href, btn, comment="", highlights=None, extra_style=""):
    cmt = f"          <!-- {comment} -->\n" if comment else ""
    style_attr = f' style="{extra_style}"' if extra_style else ""
    highlights_html = ""
    if highlights:
        items = "\n".join(
            f'                <li style="display: flex; align-items: baseline; gap: 8px; font-size: 0.875rem; color: var(--text-body);">'
            f'<span style="color: var(--primary); font-weight: 800;">&check;</span> {h}</li>'
            for h in highlights
        )
        highlights_html = f"""              <ul style="list-style: none; margin: 0 0 20px; padding: 0; display: grid; gap: 8px;">
{items}
              </ul>
"""
    return f"""{cmt}          <article class="division-card"{style_attr}>
            <div class="division-media">
              <img src="{img}" alt="{alt}" width="1024" height="426" loading="lazy">
            </div>
            <div class="division-body">
              <span class="division-tag">{tag}</span>
              <h3 class="division-title">{title}</h3>
              <p class="division-desc">{desc}</p>
{highlights_html}              <a href="{href}" class="division-btn">
                <span>{btn}</span>
                {_ARROW_SVG}
              </a>
            </div>
          </article>"""


def get_contact_wa_cta(is_en=False):
    assets = "../../" if is_en else "../"
    badge = "دعم مباشر وفوري" if not is_en else "Instant Direct Support"
    title = "تواصل أسرع عبر واتساب" if not is_en else "Faster Assistance via WhatsApp"
    desc = ("يمكنك محادثة ممثلي خدمة العملاء والدعم الفني مباشرة والحصول على رد فوري ومباشر لاستفسارك أو طلبك على مدار الساعة." if not is_en
            else "Chat directly with our technical support and customer care team for instant project inquiries or service requests.")
    action = "محادثة واتساب: +966 55 489 0900" if not is_en else "WhatsApp: +966 55 489 0900"
    media_alt = "تواصل مع أحلام الجزيرة عبر واتساب" if not is_en else "Contact Aljazeera Dreams on WhatsApp"
    return f"""        <div style="margin-top: 50px;">
          <div class="cta-whatsapp-card">
            <div class="cta-whatsapp-content">
              <span class="cta-whatsapp-badge">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="{_WA_GLYPH}"/></svg>
                <span>{badge}</span>
              </span>
              <h2 class="cta-whatsapp-title">{title}</h2>
              <p class="cta-whatsapp-desc">{desc}</p>
              <div class="cta-whatsapp-actions">
                <a href="https://wa.me/966554890900" target="_blank" rel="noopener" class="btn-whatsapp-cta">
                  <svg viewBox="0 0 24 24"><path d="{_WA_GLYPH}"/></svg>
                  <span>{action}</span>
                </a>
              </div>
            </div>
            <div class="cta-whatsapp-media">
              <img src="{assets}assets/img/banners/banner-whatsapp.jpg" alt="{media_alt}" width="1024" height="426" loading="lazy">
            </div>
          </div>
        </div>"""


def get_about_showcase(is_en=False):
    assets = "../../" if is_en else "../"
    if is_en:
        p_tag, p_h2 = "Accredited by Top Financial Institutions", "Trusted Security Partner for Saudi Banking"
    else:
        p_tag, p_h2 = "اعتمادات كبرى المصارف", "شريك الأمان المعتمد لدى البنوك السعودية"
    return f"""        <!-- Banking Partners & Trust Showcase -->
        <div class="section-header" style="margin-top: 50px; margin-bottom: 25px;">
          <span class="section-tag">{p_tag}</span>
          <h2 class="section-title">{p_h2}</h2>
        </div>
        <ul class="clients-grid" style="margin-bottom: 50px;">
{get_clients(is_en, assets)}
        </ul>"""


def get_whatsapp_cta(is_en=False, rel=""):
    badge = "خدمة العملاء والاستجابة الفورية" if not is_en else "Instant Support & Consultation"
    title = ("تواصل فوري ومباشر مع فريقنا الهندسي" if not is_en
             else "Connect Directly with Our Engineering Team")
    desc = ("هل تحتاج إلى استشارة هندسية لمشروعك، أو تسعير مخصص، أو متابعة طلب صيانة عاجل؟ مهندسونا جاهزون لخدمتكم عبر واتساب مباشرة على مدار الساعة." if not is_en
            else "Need project specifications, an instant quote, or urgent maintenance support? Our engineers are ready to assist you directly via WhatsApp 24/7.")
    chat = "محادثة فورية عبر واتساب" if not is_en else "Chat on WhatsApp"
    quote = "طلب تسعير رسمي" if not is_en else "Request Official Quote"
    media_alt = "تواصل مع أحلام الجزيرة عبر واتساب" if not is_en else "Contact Aljazeera Dreams on WhatsApp"
    return f"""    <!-- Direct WhatsApp Support CTA -->
    <section class="cta-whatsapp-section">
      <div class="container">
        <div class="cta-whatsapp-card">
          <div class="cta-whatsapp-content">
            <span class="cta-whatsapp-badge">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="{_WA_GLYPH}"/></svg>
              <span>{badge}</span>
            </span>
            <h2 class="cta-whatsapp-title">{title}</h2>
            <p class="cta-whatsapp-desc">{desc}</p>
            <div class="cta-whatsapp-actions">
              <a href="https://wa.me/966554890900" target="_blank" rel="noopener" class="btn-whatsapp-cta">
                <svg viewBox="0 0 24 24"><path d="{_WA_GLYPH}"/></svg>
                <span>{chat}</span>
              </a>
              <button type="button" class="btn-whatsapp-secondary open-quote-modal">
                <span>{quote}</span>
              </button>
            </div>
          </div>
          <div class="cta-whatsapp-media">
            <img src="{rel}assets/img/banners/banner-whatsapp.jpg" alt="{media_alt}" width="1024" height="426" loading="lazy">
          </div>
        </div>
      </div>
    </section>"""


def build_homepage(is_en=False):
    rel = "../" if is_en else ""
    t = {
        "badge": "الريادة في حلول الأمن والمقاولات منذ أكثر من 15 عاماً" if not is_en else "Leading Security & Contracting in Saudi Arabia for 15+ Years",
        "h1": "حلول متكاملة في <span>الخزائن المحصنة</span> وأنظمة الأمان الذكية" if not is_en else "Integrated Solutions for <span>Vault Doors</span> & Smart Security Systems",
        "sub": "نقدم خدمات التوريد والتركيب والصيانة الدورية للخزائن والأبواب المصرفية المحصنة، دواليب الملفات المقاومة للحريق، والأقفال الرقمية المتطورة لكبرى البنوك والمؤسسات في كافة أنحاء المملكة." if not is_en else "Supplying, installing, and maintaining fortified bank vault doors, fireproof safes, fireproof filing cabinets, and biometric locks for enterprises across Saudi Arabia.",
        "explore_btn": "استكشف المنتجات" if not is_en else "Explore Products",
        "explore_services_btn": "اكتشف الخدمات" if not is_en else "Explore Services",
        "quote_btn": "طلب عرض سعر" if not is_en else "Request Quote",
        "stat_years": "+15" if not is_en else "15+",
        "stat_years_lbl": "عاماً من الخبرة" if not is_en else "Years Experience",
        "stat_proj": "+500" if not is_en else "500+",
        "stat_proj_lbl": "مشروع مصرفي وتجاري" if not is_en else "Banking & Enterprise Projects",
        "stat_branches": "7" if not is_en else "7",
        "stat_branches_lbl": "فروع بالمملكة" if not is_en else "Branches in KSA",
        "floating_cert": "معتمدون لدى كبرى البنوك" if not is_en else "Certified by Major Banks",
        "hero_img_alt": "أبواب الخزائن المحصنة، الخزائن الحديدية، دواليب الملفات، خزائن الإيداع، الأبواب الأمنية، والأقفال" if not is_en else "Vault doors, fireproof safes, filing cabinets, deposit lockers, security doors, and locks",
        "srv_tag": "خدماتنا المتميزة" if not is_en else "Our Core Services",
        "srv_h2": "حلول مقاولات وأمن شاملة بأعلى المعايير" if not is_en else "Comprehensive Contracting & Security Standards",
        "srv1_title": "أبواب الخزائن والغرف المحصنة" if not is_en else "Vault & Bunker Room Doors",
        "srv1_desc": "توريد وتركيب أبواب الغرف المحصنة الحاصلة على شهادات اعتماد أمريكية UL وأوروبية EN." if not is_en else "Supply and installation of reinforced vault room doors, certified to American UL and European EN standards.",
        "srv2_title": "الخزائن المقاومة للحريق والسطو" if not is_en else "Fireproof & Burglary-Resistant Safes",
        "srv2_desc": "توريد وتركيب الخزن الحديدية المقاومة للحريق والسطو بمختلف الأحجام والمواصفات." if not is_en else "Supply and installation of fire and burglary-resistant steel safes in all sizes and specifications.",
        "srv3_title": "دواليب الملفات وخزائن الإيداع المحصنة" if not is_en else "Fireproof Filing Cabinets & Deposit Lockers",
        "srv3_desc": "توريد وتركيب الدواليب الحديدية المقاومة للحريق، وصناديق الأمانات، وخزائن الإيداع المصرفية." if not is_en else "Supply and installation of fire-resistant filing cabinets, safety deposit boxes, and banking deposit lockers.",
        "srv4_title": "أبواب الصرافين وأبواب الطوارئ" if not is_en else "Teller, ATM & Emergency Doors",
        "srv4_desc": "تصنيع وتركيب أبواب الصرافين وغرف الصراف الآلي والبيانات وأبواب الطوارئ، حاصلة على شهادة Intertek لمقاومة الحريق UL 10C." if not is_en else "Manufacturing and installation of teller cabinet, ATM, data room, and emergency exit doors, Intertek listed to UL 10C for fire resistance.",
        "srv5_title": "الأقفال الرقمية واليدوية" if not is_en else "Digital & Manual Locks",
        "srv5_desc": "توريد وتركيب جميع أنواع الأقفال الرقمية واليدوية ذات المفاتيح الأمنية والشفرات الرقمية المعتمدة." if not is_en else "Supply and installation of all types of certified digital and manual locks, security keys, and digital combinations.",
        "srv6_title": "الفك والنقل والتركيب والصيانة" if not is_en else "Dismantling, Transport, Installation & Maintenance",
        "srv6_desc": "فك ونقل وتركيب الخزائن وأبواب الغرف المحصنة بسيارات مجهزة ومعدات رفع متخصصة، وتركيب احترافي مع ضبط دقيق واختبار شامل، إلى جانب عقود صيانة دورية تشمل الفحص الشامل وإصلاح الأعطال وتحديث الأنظمة." if not is_en else "Dismantling, transporting, and reinstalling vaults and fortified room doors with fully equipped vehicles and specialized lifting gear, professional installation with precise calibration and comprehensive testing, plus periodic maintenance covering full inspection, fault repair, and system updates.",
        "srv7_title": "تنفيذ وتجهيز غرف ومواقع الصراف الآلي" if not is_en else "ATM Booth Execution & Site Setup",
        "srv7_desc": "تنفيذ وتجهيز غرف الصراف الآلي ومواقعها على الطرق العامة، من الأعمال المدنية والتأسيس إلى التركيب النهائي، بما يضمن موقعاً آمناً وجاهزاً للتشغيل على مدار الساعة." if not is_en else "End-to-end execution and setup of ATM booths and roadside locations, from civil works and foundations to final installation, delivering a secure site ready for round-the-clock operation.",
        "srv_lead": "من توريد وتركيب أبواب الخزائن المحصنة إلى عقود الصيانة والنقل طويلة الأمد، نغطّي دورة حياة المنشأة الأمنية بالكامل تحت سقف واحد." if not is_en else "From supplying and installing fortified vault doors to long-term maintenance and relocation contracts, we cover the full lifecycle of a secure facility under one roof.",
        "srv_cta": "تحدث إلى مهندس" if not is_en else "Talk to an Engineer",
        "partners_tag": "شركاء النجاح" if not is_en else "Partners of Success",
        "partners_h2": "العلامات التجارية المعتمدة عالمياً" if not is_en else "Globally Authorized Brands",
        "partners_sub": "نورّد ونركّب أنظمة ومنتجات أمنية أصلية من كبرى المصنّعين العالميين، باعتماد رسمي وضمان معتمد." if not is_en else "We supply and install original security systems and hardware from the world's leading manufacturers, under official authorization and warranty.",
        "branches_tag": "تغطية شاملة" if not is_en else "Nationwide Coverage",
        "branches_h2": "فروعنا في جميع أنحاء المملكة" if not is_en else "Our Branches Across Saudi Arabia",
    }

    products_page_url = f"{rel}products/index.html" if not is_en else f"{rel}en/products/index.html"
    services_page_url = f"{rel}services/index.html" if not is_en else f"{rel}en/services/index.html"

    body = f"""
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-bg-overlay"></div>
      <div class="container">
        <div class="hero-grid">
          <div class="hero-content">
            <div class="hero-badge">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L1 21h22L12 2zm0 3.8l7.53 13.2H4.47L12 5.8z"/></svg>
              <span>{t['badge']}</span>
            </div>
            <h1 class="hero-title">{t['h1']}</h1>
            <p class="hero-subtitle">{t['sub']}</p>
            <div class="hero-actions">
              <a href="{products_page_url}" class="btn-primary">{t['explore_btn']}</a>
              <a href="{services_page_url}" class="btn-secondary">{t['explore_services_btn']}</a>
              <button class="btn-secondary open-quote-modal">{t['quote_btn']}</button>
            </div>
            <div class="hero-stats">
              <div class="stat-item">
                <span class="stat-number">{t['stat_years']}</span>
                <span class="stat-label">{t['stat_years_lbl']}</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{t['stat_proj']}</span>
                <span class="stat-label">{t['stat_proj_lbl']}</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{t['stat_branches']}</span>
                <span class="stat-label">{t['stat_branches_lbl']}</span>
              </div>
            </div>
          </div>
          <div class="hero-media-card">
            <img src="{rel}assets/img/banners/hero-showcase.jpg" alt="{t['hero_img_alt']}" width="1098" height="932">
            <div class="hero-floating-pill">
              <svg viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/></svg>
              <div>
                <strong style="display: block; font-size: 0.95rem;">{t['floating_cert']}</strong>
                <span style="font-size: 0.8rem; color: var(--text-muted);">SAMA & ISO Compliant</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Trusted by / Clients -->
    <section class="clients" id="partners">
      <div class="container">
        <div class="clients-head">
          <span class="section-tag">{'ثقة مؤسسية' if not is_en else 'Institutional trust'}</span>
          <h2 class="section-title">{'شركاؤنا في النجاح' if not is_en else 'Partners in Success'}</h2>
          <p class="section-subtitle">{'تعتمد كبرى البنوك والمصارف والمؤسسات في المملكة والخليج على أنظمة أحلام الجزيرة الأمنية.' if not is_en else 'Leading banks and institutions across Saudi Arabia and the Gulf rely on Aljazeera Dreams security systems.'}</p>
          <p class="clients-count"><strong>+21</strong> {'جهة مصرفية ومؤسسية' if not is_en else 'banking &amp; institutional clients'}</p>
        </div>
        <ul class="clients-grid">
{get_clients(is_en, rel)}
        </ul>
      </div>
    </section>

    <!-- Services / Capabilities -->
    <section class="section services-section" id="services">
      <div class="container">
        <div class="services-layout">
          <div class="services-intro">
            <span class="section-tag">{t['srv_tag']}</span>
            <h2 class="services-intro-title">{t['srv_h2']}</h2>
            <p class="services-lead">{t['srv_lead']}</p>
            <button type="button" class="btn-primary open-quote-modal">{t['srv_cta']}</button>
          </div>
          <ol class="services-list">
            <li class="service-item">
              <span class="service-num">01</span>
              <div class="service-item-body">
                <h3>{t['srv1_title']}</h3>
                <p>{t['srv1_desc']}</p>
              </div>
            </li>
            <li class="service-item">
              <span class="service-num">02</span>
              <div class="service-item-body">
                <h3>{t['srv2_title']}</h3>
                <p>{t['srv2_desc']}</p>
              </div>
            </li>
            <li class="service-item">
              <span class="service-num">03</span>
              <div class="service-item-body">
                <h3>{t['srv3_title']}</h3>
                <p>{t['srv3_desc']}</p>
              </div>
            </li>
            <li class="service-item">
              <span class="service-num">04</span>
              <div class="service-item-body">
                <h3>{t['srv4_title']}</h3>
                <p>{t['srv4_desc']}</p>
              </div>
            </li>
            <li class="service-item">
              <span class="service-num">05</span>
              <div class="service-item-body">
                <h3>{t['srv5_title']}</h3>
                <p>{t['srv5_desc']}</p>
              </div>
            </li>
            <li class="service-item">
              <span class="service-num">06</span>
              <div class="service-item-body">
                <h3>{t['srv6_title']}</h3>
                <p>{t['srv6_desc']}</p>
              </div>
            </li>
            <li class="service-item">
              <span class="service-num">07</span>
              <div class="service-item-body">
                <h3>{t['srv7_title']}</h3>
                <p>{t['srv7_desc']}</p>
              </div>
            </li>
          </ol>
        </div>
      </div>
    </section>

    <!-- Authorized Brands -->
    <section class="brands-section" id="brands">
      <div class="container">
        <div class="section-header" style="margin-bottom: 34px;">
          <span class="section-tag">{t['partners_tag']}</span>
          <h2 class="section-title" style="font-size: 1.75rem;">{t['partners_h2']}</h2>
          <p class="section-subtitle">{t['partners_sub']}</p>
        </div>
        <ul class="brand-wall">
{get_brand_wall(is_en, rel)}
        </ul>
      </div>
    </section>

    <!-- Nationwide Coverage -->
    <section class="coverage">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">{t['branches_tag']}</span>
          <h2 class="section-title">{t['branches_h2']}</h2>
        </div>
        {get_coverage(is_en)}
      </div>
    </section>

{get_whatsapp_cta(is_en, rel)}
    """

    html = generate_base_html(
        title="الرئيسية - حلول الخزائن والأبواب الأمنية" if not is_en else "Home - Security Safes & Vault Doors",
        body_content=body,
        is_en=is_en,
        depth=1 if is_en else 0
    )
    
    out_path = ROOT_DIR / ("en/index.html" if is_en else "index.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

def build_filter_tabs(active_key, is_en, all_label):
    """Full category tab row (shared by the Products page and every category
    page), so switching categories never requires leaving the page you're on."""
    buttons = [
        f'<button class="filter-tab{" active" if active_key == "all" else ""}" data-category="all">{all_label}</button>'
    ]
    for key, _slug, name_ar, name_en, _banner in PRODUCT_CATEGORIES:
        label = name_en if is_en else name_ar
        active = " active" if key == active_key else ""
        buttons.append(f'<button class="filter-tab{active}" data-category="{key}">{label}</button>')
    return "\n            ".join(buttons)

def build_products_page(is_en=False):
    t = {
        "tag": "منتجات شركة أحلام الجزيرة" if not is_en else "Aljazeera Dreams Company Products",
        "h1": "جميع الخزائن وأنظمة الأمان" if not is_en else "All Security Safes & Vaults",
        "sub": "تصفح تشكيلتنا الشاملة من أبواب الخزائن المحصنة، الخزائن المقاومة للحريق والسطو، دواليب الملفات، خزائن الإيداع، والأبواب الأمنية." if not is_en else "Explore our full catalog of vault doors, fireproof safes, filing cabinets, deposit lockers, and security doors.",
        "tab_all": "الكل" if not is_en else "All",
        "search_ph": "ابحث عن موديل أو منتج..." if not is_en else "Search model or product name...",
    }

    tabs = build_filter_tabs("all", is_en, t['tab_all'])

    body = f"""
    <section class="section" style="padding-top: 50px;">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">{t['tag']}</span>
          <h1 class="section-title">{t['h1']}</h1>
          <p class="section-subtitle">{t['sub']}</p>
        </div>

        <div class="catalog-controls">
          <div class="filter-tabs">
            {tabs}
          </div>
          <div class="search-box">
            <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
            <input type="text" id="product-search-input" placeholder="{t['search_ph']}">
          </div>
        </div>

        <div class="products-grid" id="products-grid-container">
          <!-- Dynamically populated via assets/js/main.js -->
        </div>
      </div>
    </section>
    """

    html = generate_base_html(
        title="منتجاتنا" if not is_en else "Our Products",
        body_content=body,
        is_en=is_en,
        depth=2 if is_en else 1,
        needs_products=True
    )
    
    out_path = ROOT_DIR / ("en/products/index.html" if is_en else "products/index.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

def build_services_page(is_en=False):
    assets = "../../" if is_en else "../"
    cat = "../"
    service_req_href = f"{cat}service-request/index.html"
    img = f"{assets}assets/img/services/"

    t = {
        "tag": "خدماتنا" if not is_en else "Our Services",
        "h1": "خدمات التوريد والتركيب والصيانة الأمنية" if not is_en else "Security Supply, Installation & Maintenance Services",
        "sub": "من أبواب الخزائن المحصنة إلى الصيانة الدورية، نغطي دورة حياة المنشأة الأمنية بالكامل بفرق هندسية متخصصة ومعدات نقل وتركيب مخصصة." if not is_en else "From fortified vault doors to periodic maintenance, we cover the full lifecycle of a secure facility with specialized engineering teams and dedicated transport and installation equipment.",
        "btn": "اطلب هذه الخدمة" if not is_en else "Request This Service",
        "scroll_cue": "اكتشف جميع خدماتنا بالأسفل" if not is_en else "Discover all our services below",
    }

    quote_btn = t["btn"]

    services = [
        (
            f"{img}vault-doors.jpg", "Vault & Bunker Room Doors",
            "أبواب محصنة" if not is_en else "Vault Doors",
            "توريد وتركيب أبواب الخزائن والغرف المحصنة" if not is_en else "Vault & Bunker Room Doors",
            "توريد وتركيب أبواب الغرف المحصنة الحاصلة على شهادات الاعتماد الأمريكي UL وشهادات الاعتماد الأوروبي EN، بمقاسات وتصاميم تناسب متطلبات البنوك ومراكز البيانات والمؤسسات المالية."
            if not is_en else
            "Supply and installation of reinforced vault and bunker room doors, certified to American UL and European EN standards, in sizes and designs suited to banks, data centers, and financial institutions.",
            service_req_href,
            ["معتمدة UL أمريكياً وEN أوروبياً", "مقاسات وتصاميم مخصصة", "مناسبة للبنوك ومراكز البيانات"]
            if not is_en else
            ["Certified to American UL and European EN", "Custom sizes and designs", "Suited to banks and data centers"],
        ),
        (
            f"{img}fireproof-safes.jpg", "Fireproof & Burglary-Resistant Safes",
            "خزائن حديدية" if not is_en else "Fireproof Safes",
            "توريد وتركيب الخزائن المقاومة للحريق والسطو" if not is_en else "Fireproof & Burglary-Resistant Safes",
            "توريد وتركيب الخزن الحديدية المقاومة للحريق والسطو بجميع أنواعها وأحجامها، بما يشمل الخزائن المصرفية والتجارية ذات الأقفال الإلكترونية والميكانيكية."
            if not is_en else
            "Supply and installation of fire and burglary-resistant steel safes in all types and sizes, including banking and commercial safes with electronic and mechanical locking.",
            service_req_href,
            ["مقاومة للحريق والسطو معاً", "جميع الأحجام والمقاسات", "أقفال إلكترونية وميكانيكية"]
            if not is_en else
            ["Both fire- and burglary-resistant", "Every size and specification", "Electronic and mechanical locking"],
        ),
        (
            f"{img}filing-cabinets.jpg", "Fireproof Filing Cabinets",
            "دواليب الملفات" if not is_en else "Filing Cabinets",
            "توريد وتركيب دواليب الملفات المقاومة للحريق" if not is_en else "Fireproof Filing Cabinets",
            "توريد وتركيب الدواليب الحديدية المقاومة للحريق بعدد أدراج يبدأ من درجين وحتى خمسة أدراج، بمختلف أنواع الأقفال الميكانيكية والإلكترونية، لحفظ المستندات والسجلات الهامة."
            if not is_en else
            "Supply and installation of fireproof steel filing cabinets from 2 up to 5 drawers, with a range of mechanical and electronic locks, for safeguarding important documents and records.",
            service_req_href,
            ["من درجين حتى خمسة أدراج", "أقفال ميكانيكية وإلكترونية", "لحفظ المستندات والسجلات الهامة"]
            if not is_en else
            ["From 2 up to 5 drawers", "Mechanical and electronic locks", "For important documents and records"],
        ),
        (
            f"{img}security-doors.jpg", "Teller, ATM, Data Room & Emergency Doors",
            "أبواب الصرافين" if not is_en else "Teller & Emergency Doors",
            "تصنيع وتركيب أبواب الصرافين وأبواب الطوارئ" if not is_en else "Teller, ATM & Emergency Doors",
            "تصنيع وتوريد وتركيب أبواب مقاومة للحريق ومقاومة للرصاص، تشمل أبواب الصرافين ومخارج الطوارئ وأبواب غرف الصراف الآلي (ATM) وغرف الداتا، حاصلة على شهادة مقاومة الحريق المعتمدة من Intertek وفق معيار UL 10C."
            if not is_en else
            "Manufacturing, supply, and installation of fire- and bullet-resistant doors, including teller cabinet doors, emergency exits, ATM room doors, and data room doors, Intertek listed to UL 10C for fire resistance.",
            service_req_href,
            ["مقاومة للحريق ومقاومة للرصاص", "شهادة Intertek وفق UL 10C", "لغرف الصرافين والصراف الآلي والبيانات"]
            if not is_en else
            ["Fire- and bullet-resistant", "Intertek listed to UL 10C", "For teller, ATM, and data rooms"],
        ),
        (
            f"{img}locks.jpg", "Digital & Manual Locks",
            "الأقفال الأمنية" if not is_en else "Security Locks",
            "توريد وتركيب الأقفال الرقمية واليدوية" if not is_en else "Digital & Manual Locks",
            "توريد وتركيب جميع أنواع الأقفال الرقمية واليدوية ذات المفاتيح الأمنية والشفرات الرقمية، الحاصلة على شهادات اختبار معتمدة، مع خدمة إعادة برمجة وتغيير الأقفال."
            if not is_en else
            "Supply and installation of all types of certified digital and manual locks with security keys and digital combinations, plus lock reprogramming and replacement service.",
            service_req_href,
            ["أقفال رقمية ويدوية معتمدة", "شهادات اختبار دولية", "خدمة إعادة برمجة وتغيير الأقفال"]
            if not is_en else
            ["Certified digital and manual locks", "International test certifications", "Reprogramming and replacement service"],
        ),
        (
            f"{img}deposit-lockers.jpg", "Deposit Lockers & Safety Deposit Boxes",
            "خزائن الإيداع" if not is_en else "Deposit Lockers",
            "توريد وتركيب خزائن الإيداع وصناديق الأمانات" if not is_en else "Deposit Lockers & Safety Deposit Boxes",
            "توريد وتركيب جميع أنواع صناديق الأمانات وخزائن الإيداع المصرفية وأقفالها، بالإضافة إلى خدمة ترهيم (إعادة برمجة) الأقفال والأقراص للموديلات القديمة."
            if not is_en else
            "Supply and installation of all types of safety deposit boxes, banking deposit lockers, and their locks, plus re-keying and re-coding of locks and dials for older models.",
            service_req_href,
            ["صناديق أمانات وخزائن إيداع مصرفية", "خدمة ترهيم للموديلات القديمة", "حلول متكاملة للبنوك والمؤسسات"]
            if not is_en else
            ["Safety deposit boxes and bank lockers", "Re-keying service for older models", "Integrated solutions for banks and institutions"],
        ),
        (
            f"{img}atm-booths.jpg", "ATM Booth Execution & Site Setup",
            "الصراف الآلي" if not is_en else "ATM Booths",
            "تنفيذ وتجهيز غرف ومواقع الصراف الآلي" if not is_en else "ATM Booth Execution & Site Setup",
            "تنفيذ وتجهيز غرف الصراف الآلي ومواقعها على الطرق العامة، من الأعمال المدنية والتأسيس إلى التركيب النهائي والإضاءة والتغطية، بما يضمن موقعاً آمناً وجاهزاً للتشغيل على مدار الساعة."
            if not is_en else
            "End-to-end execution and setup of ATM booths and roadside locations, from civil works and foundations to final installation, lighting, and canopy, delivering a secure site ready for round-the-clock operation.",
            service_req_href,
            ["من الأعمال المدنية إلى التشغيل الكامل", "تركيب وإضاءة وتغطية متكاملة", "جاهزية تشغيل على مدار الساعة"]
            if not is_en else
            ["From civil works to full operation", "Integrated installation, lighting, canopy", "Ready for round-the-clock operation"],
        ),
    ]

    cards = "\n\n".join(
        division_card(
            src, alt, tag, title, desc, href, quote_btn, highlights=highlights,
            extra_style="grid-column: 1 / -1; justify-self: center; width: 100%; max-width: 420px;" if len(services) % 3 == 1 and i == len(services) - 1 else "",
        )
        for i, (src, alt, tag, title, desc, href, highlights) in enumerate(services)
    )

    breakdown = [
        (
            "الصيانة" if not is_en else "Maintenance",
            "فحص شامل وصيانة احترافية دورية تشمل إصلاح الأعطال وتحديث الأنظمة، لضمان أعلى مستويات الأمان."
            if not is_en else
            "Comprehensive inspection and professional periodic maintenance, including fault repair and system updates, to ensure the highest levels of security.",
        ),
        (
            "النقل" if not is_en else "Transport",
            "نقل آمن ومخصص لمنشآتك بإرشاد وعمليات متخصصة وسيارات مجهزة بأعلى المستويات، مع تغليف دقيق وحماية متكاملة لتجهيزاتك الثمينة."
            if not is_en else
            "Safe, dedicated transport for your facilities with specialized guidance and top-standard equipped vehicles, plus precise packaging and comprehensive protection for your valuable equipment.",
        ),
        (
            "التركيب" if not is_en else "Installation",
            "تركيب احترافي ودقيق وفق أعلى معايير الأمان والمواصفات، مع ضبط دقيق واختبار شامل لكل وحدة."
            if not is_en else
            "Professional, precise installation to the highest safety standards and specifications, with precise calibration and comprehensive testing for every unit.",
        ),
    ]
    breakdown_html = "\n".join(f"""              <div>
                <h4 style="font-size: 1rem; font-weight: 800; color: var(--primary-dark); margin-bottom: 6px;">{label}</h4>
                <p style="font-size: 0.875rem; color: var(--text-muted); line-height: 1.7; margin: 0;">{desc}</p>
              </div>""" for label, desc in breakdown)

    featured_tag = "خدمتنا الشاملة" if not is_en else "Our Full-Lifecycle Service"
    featured_title = "الفك والنقل والتركيب والصيانة الدورية" if not is_en else "Dismantling, Transport, Installation & Periodic Maintenance"
    featured_lead = (
        "فك ونقل جميع أنواع أبواب الغرف المحصنة ونقل جميع أنواع الخزن والدواليب والقيام بجميع أنواع الصيانة وترهيم الاقفال. وصيانة جميع الاقفال الأمنية بالإضافة الي عقود الصيانة الدورية لجميع أنواع المنتجات من أبواب الغرف المحصنة والابواب المعدنية والخزن الأمنية في جميع انحاء المملكة العربية السعودية."
        if not is_en else
        "Dismantling and transporting all types of vault room doors, safes, and cabinets, performing all types of maintenance and lock re-keying, and servicing all security locks, in addition to periodic maintenance contracts for all vault room doors, metal cabinets, and security safes, across the Kingdom of Saudi Arabia."
    )
    featured_card = f"""          <article class="division-card featured-service-card" style="grid-column: 1 / -1;">
            <div class="division-media">
              <img src="{img}installation-maintenance.jpg" alt="Dismantling, Transport, Installation & Maintenance" width="2950" height="1962" loading="lazy">
            </div>
            <div class="division-body">
              <span class="division-tag">{featured_tag}</span>
              <h2 class="division-title" style="font-size: 1.5rem;">{featured_title}</h2>
              <p class="division-desc">{featured_lead}</p>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin-bottom: 24px;">
{breakdown_html}
              </div>
              <a href="{service_req_href}" class="division-btn">
                <span>{quote_btn}</span>
                {_ARROW_SVG}
              </a>
            </div>
          </article>"""

    body = f"""
    <section class="section" style="padding-top: 50px;">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">{t['tag']}</span>
          <h1 class="section-title">{t['h1']}</h1>
          <p class="section-subtitle">{t['sub']}</p>
        </div>

        <div class="scroll-cue">
          <span>{t['scroll_cue']}</span>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
        </div>

        <div class="divisions-grid">
{featured_card}

{cards}
        </div>
{get_contact_wa_cta(is_en)}
      </div>
    </section>
    """

    html = generate_base_html(
        title="خدماتنا" if not is_en else "Our Services",
        body_content=body,
        is_en=is_en,
        depth=2 if is_en else 1
    )

    out_path = ROOT_DIR / ("en/services/index.html" if is_en else "services/index.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

def build_about_page(is_en=False):
    t = {
        "tag": "من نحن" if not is_en else "About Us",
        "h1": "شركة أحلام الجزيرة للمقاولات" if not is_en else "Aljazeera Dreams Contracting",
        "sub": "أكثر من 15 عاماً من الخبرة والتميز في تزويد وتركيب أحدث تقنيات الخزائن والأبواب الأمنية والحلول المصرفية في المملكة العربية السعودية." if not is_en else "Over 15 years of excellence delivering high-security safes, vault doors, and smart banking solutions across Saudi Arabia.",
        "overview": (
            "شركة أحلام الجزيرة للمقاولات هي شركة سعودية رائدة متخصصة في تصميم وتصنيع وتوريد وتركيب الحلول الأمنية المتكاملة، "
            "حيث تقدم منتجات وخدمات تلبي أعلى معايير الجودة والأمان وفق المواصفات والاعتمادات الدولية. تمتلك الشركة خبرة واسعة "
            "في توفير الحلول الأمنية للقطاعات الحكومية والمؤسسات المالية والمنشآت التجارية والصناعية، مع التركيز على منتجات "
            "موثوقة مصممة لحماية الأصول والممتلكات والأموال والوثائق ذات القيمة العالية. وتتميز منتجاتنا بحصولها على اعتمادات "
            "واختبارات دولية وفق معايير UL الأمريكية والأوروبية EN، بما يضمن أعلى مستويات الحماية والجودة والاعتمادية."
            if not is_en else
            "Aljazeera Dreams Contracting is a leading Saudi company specialized in designing, manufacturing, supplying, and "
            "installing integrated security solutions, delivering products and services that meet the highest quality and "
            "safety standards under international specifications and accreditations. The company has extensive experience "
            "providing security solutions for government sectors, financial institutions, and commercial and industrial "
            "facilities, focused on reliable products designed to protect high-value assets, property, funds, and documents. "
            "Our products are certified and tested to American UL and European EN standards, ensuring the highest levels of "
            "protection, quality, and reliability."
        ),
        "vision_title": "رؤيتنا" if not is_en else "Our Vision",
        "vision_desc": "أن نكون الشريك الأول في المملكة العربية السعودية في تقديم الحلول الأمنية المتكاملة، وأن نساهم في رفع مستوى الأمن والحماية من خلال منتجات معتمدة عالمياً وخدمات احترافية تتجاوز توقعات عملائنا." if not is_en else "To be the leading partner in Saudi Arabia for integrated security solutions, helping raise the standard of security and protection through globally certified products and professional services that exceed our clients' expectations.",
        "mission_title": "رسالتنا" if not is_en else "Our Mission",
        "mission_desc": "توفير حلول أمنية موثوقة ومبتكرة تعتمد على أحدث التقنيات والمعايير الدولية، مع الالتزام بالجودة والاستدامة وخدمة العملاء، بما يحقق أعلى مستويات الحماية والأمان." if not is_en else "To provide reliable and innovative security solutions built on the latest technologies and international standards, upholding quality, sustainability, and customer service to achieve the highest levels of protection and safety.",
        "values_title": "قيمنا" if not is_en else "Our Values",
        "values": [
            ("الجودة والتميز" if not is_en else "Quality & Excellence"),
            ("الموثوقية" if not is_en else "Reliability"),
            ("الابتكار" if not is_en else "Innovation"),
            ("الالتزام" if not is_en else "Commitment"),
        ],
        "chairman_tag": "كلمة رئيس مجلس الإدارة" if not is_en else "Chairman's Message",
        "chairman_quote": (
            "نضع نصب أعيننا هدفاً واضحاً يتمثل في توفير منتجات وخدمات أمنية موثوقة تلبي احتياجات عملائنا في مختلف القطاعات. "
            "إن نجاحنا لم يكن وليد الصدفة، بل هو ثمرة الالتزام بالجودة والحرص على بناء شراكات استراتيجية مع كبرى الشركات "
            "والمصنعين العالميين. نتقدم بجزيل الشكر لعملائنا وشركائنا على ثقتهم الغالية، ونتطلع إلى مستقبل مليء بالنجاحات "
            "والإنجازات المشتركة."
            if not is_en else
            "We have set ourselves a clear goal: to provide reliable security products and services that meet our clients' "
            "needs across every sector. Our success was never a coincidence, it is the fruit of our commitment to quality "
            "and our drive to build strategic partnerships with leading global manufacturers. We thank our clients and "
            "partners for their valued trust, and we look forward to a future full of shared achievements."
        ),
        "chairman_name": "علي عبدالله الحميد" if not is_en else "Ali Abdullah Al-Humaid",
        "chairman_title": "رئيس مجلس الإدارة" if not is_en else "Chairman of the Board",
        "cert_tag": "الشهادات والاعتمادات" if not is_en else "Certifications & Accreditations",
        "cert_h2": "معتمدون وفق أعلى المعايير الدولية" if not is_en else "Certified to the Highest International Standards",
        "cert_sub": "حاصلون على شهادات الأيزو المعتمدة دولياً في إدارة الجودة والبيئة والصحة والسلامة المهنية، الصادرة عن QRO Certification." if not is_en else "Certified to internationally accredited ISO standards for quality, environmental, and occupational health & safety management, issued by QRO Certification.",
    }

    rel = "../../" if is_en else "../"

    cert_no_label = "رقم الشهادة" if not is_en else "Certificate No."
    cert_valid_label = "سارية حتى 3 نوفمبر 2028" if not is_en else "Valid until 3 Nov 2028"
    cert_view_label = "عرض الشهادة كاملة" if not is_en else "View full certificate"
    certs = [
        ("ISO 9001:2015", "نظام إدارة الجودة" if not is_en else "Quality Management System", "305025110470Q", "iso-9001"),
        ("ISO 14001:2015", "نظام الإدارة البيئية" if not is_en else "Environmental Management System", "305025110476E", "iso-14001"),
        ("ISO 45001:2018", "نظام إدارة الصحة والسلامة المهنية" if not is_en else "Occupational Health & Safety Management System", "305025110473HS", "iso-45001"),
    ]
    cert_cards = "\n".join(f"""          <div class="form-card" style="margin: 0; max-width: 100%; text-align: center;">
            <a href="{rel}assets/img/certificates/{img}.jpg" target="_blank" rel="noopener" style="display: block; margin-bottom: 18px;" aria-label="{cert_view_label}: {code}">
              <img src="{rel}assets/img/certificates/{img}.jpg" alt="{code} - {label}" width="700" height="1029" loading="lazy" style="width: 100%; height: auto; border-radius: var(--radius-md); border: 1px solid var(--border-color); box-shadow: var(--shadow-sm);">
            </a>
            <h3 style="font-size: 1.15rem; font-weight: 800; color: var(--primary-dark); margin-bottom: 6px;">{code}</h3>
            <p style="color: var(--text-muted); line-height: 1.7; font-size: 0.875rem; margin-bottom: 14px;">{label}</p>
            <p style="color: var(--text-muted); font-size: 0.875rem; border-top: 1px solid var(--border-color); padding-top: 12px; margin: 0;">
              {cert_no_label}: <bdi>{number}</bdi><br>{cert_valid_label}
            </p>
          </div>""" for code, label, number, img in certs)

    values_list = "\n".join(
        f'<li style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px; color: var(--text-body); font-weight: 600;">'
        f'<span style="color: var(--primary); font-weight: 800;">✓</span> {v}</li>'
        for v in t["values"]
    )

    body = f"""
    <section class="section" style="padding-top: 50px;">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">{t['tag']}</span>
          <h1 class="section-title">{t['h1']}</h1>
          <p class="section-subtitle">{t['sub']}</p>
        </div>

        <p style="max-width: 900px; margin: 0 auto 50px; color: var(--text-body); line-height: 1.9; text-align: center;">{t['overview']}</p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; margin-bottom: 60px;">
          <div class="form-card" style="margin: 0; max-width: 100%;">
            <div class="service-icon-box">
              <svg viewBox="0 0 24 24"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/></svg>
            </div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--primary-dark); margin-bottom: 12px;">{t['vision_title']}</h3>
            <p style="color: var(--text-muted); line-height: 1.8;">{t['vision_desc']}</p>
          </div>
          <div class="form-card" style="margin: 0; max-width: 100%;">
            <div class="service-icon-box">
              <svg viewBox="0 0 24 24"><path d="M12 2L1 21h22L12 2zm0 3.8l7.53 13.2H4.47L12 5.8z"/></svg>
            </div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--primary-dark); margin-bottom: 12px;">{t['mission_title']}</h3>
            <p style="color: var(--text-muted); line-height: 1.8;">{t['mission_desc']}</p>
          </div>
          <div class="form-card" style="margin: 0; max-width: 100%;">
            <div class="service-icon-box">
              <svg viewBox="0 0 24 24"><path d="M12 1l3.09 6.26L22 8.27l-5 4.87 1.18 6.88L12 16.9l-6.18 3.12L7 13.14 2 8.27l6.91-1.01z"/></svg>
            </div>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--primary-dark); margin-bottom: 12px;">{t['values_title']}</h3>
            <ul style="list-style: none; margin: 0; padding: 0;">
{values_list}
            </ul>
          </div>
        </div>

        <!-- Chairman's Message -->
        <div class="section-header" style="margin-bottom: 25px;">
          <span class="section-tag">{t['chairman_tag']}</span>
        </div>
        <div class="form-card" style="max-width: 100%; margin: 0 0 60px; display: flex; flex-wrap: wrap; gap: 36px; align-items: center;">
          <img src="{rel}assets/img/team/chairman-ali-alhumaid.jpg" alt="{t['chairman_name']}" width="700" height="1213" loading="lazy" style="flex: 0 1 220px; width: 100%; max-width: 220px; height: auto; border-radius: var(--radius-lg); object-fit: cover;">
          <div style="flex: 1 1 320px;">
            <p style="color: var(--text-body); line-height: 1.9; font-size: 1.02rem; margin-bottom: 18px;">&ldquo;{t['chairman_quote']}&rdquo;</p>
            <h3 style="font-size: 1.15rem; font-weight: 800; color: var(--primary-dark); margin-bottom: 2px;">{t['chairman_name']}</h3>
            <p style="color: var(--text-muted); font-size: 0.875rem;">{t['chairman_title']}</p>
          </div>
        </div>

        <!-- Certifications -->
        <div class="section-header" style="margin-bottom: 25px;">
          <span class="section-tag">{t['cert_tag']}</span>
          <h2 class="section-title" style="font-size: 1.75rem;">{t['cert_h2']}</h2>
          <p class="section-subtitle">{t['cert_sub']}</p>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 30px; margin-bottom: 60px;">
{cert_cards}
        </div>

{get_about_showcase(is_en)}
      </div>
    </section>
    """

    html = generate_base_html(
        title="نبذة عنا" if not is_en else "About Us",
        body_content=body,
        is_en=is_en,
        depth=2 if is_en else 1
    )
    
    out_path = ROOT_DIR / ("en/about-us/index.html" if is_en else "about-us/index.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

def build_contact_page(is_en=False):
    t = {
        "tag": "تواصل معنا" if not is_en else "Contact Us",
        "h1": "يسعدنا دائماً استقبال استفساراتكم" if not is_en else "We Are Always Here to Assist You",
        "sub": "فريقنا الهندسي المتخصص جاهز لتقديم الاستشارات الفنية وعروض الأسعار في كافة مناطق المملكة." if not is_en else "Our engineering and sales team is ready to assist you across all regions in Saudi Arabia.",
        "info_title": "معلومات التواصل" if not is_en else "Contact Information",
        "unified_label": "الرقم الموحد" if not is_en else "Unified Number",
        "phones_label": "أرقام الهاتف" if not is_en else "Phone Numbers",
        "email_label": "البريد الإلكتروني" if not is_en else "Email",
        "address_label": "العنوان والفروع" if not is_en else "Address & Branches",
        "address_text": "المقر الرئيسي: الرياض، حي الروابي، شارع طاهر الدباغ. فروعنا: جدة، الدمام، المدينة المنورة، بريدة، تبوك، الطائف." if not is_en else "HQ: Riyadh, Al-Rawabi District, Taher Al-Dabbagh St. Branches: Jeddah, Dammam, Medina, Buraydah, Tabuk, Taif.",
    }

    phone_svg = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
                 '<path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24 11.72 11.72 0 003.68.59 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1 11.72 11.72 0 00.59 3.68 1 1 0 01-.24 1.02l-2.23 2.09z"/></svg>')
    mail_svg = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
                '<path d="M4 4h16a2 2 0 012 2v12a2 2 0 01-2 2H4a2 2 0 01-2-2V6a2 2 0 012-2zm0 2v.01L12 12l8-5.99V6H4zm16 12V8.24l-8 6-8-6V18h16z"/></svg>')
    pin_svg = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
               '<path d="M12 2a7 7 0 00-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 00-7-7zm0 9.5A2.5 2.5 0 1112 6.5a2.5 2.5 0 010 5z"/></svg>')

    def info_row(svg, label, content_html):
        return f"""            <div style="display: flex; gap: 14px; align-items: flex-start; margin-bottom: 22px;">
              <div class="service-icon-box" style="width: 42px; height: 42px; margin-bottom: 0; flex-shrink: 0;">
                <span style="width: 20px; height: 20px; display: block;">{svg}</span>
              </div>
              <div>
                <p style="font-size: 0.875rem; color: var(--text-muted); margin-bottom: 4px;">{label}</p>
                {content_html}
              </div>
            </div>"""

    contact_info_card = f"""          <div class="form-card" style="margin: 0; max-width: 100%;">
            <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--primary-dark); margin-bottom: 24px;">{t['info_title']}</h3>
{info_row(phone_svg, t['unified_label'], f'<a href="tel:+966920028440" style="color: var(--text-main); font-weight: 700; font-size: 1.05rem;">+966 92 002 8440</a>')}
{info_row(phone_svg, t['phones_label'], f'<a href="tel:+966554890900" style="color: var(--text-main); font-weight: 700; display: block;">+966 55 489 0900</a><a href="tel:+966114718033" style="color: var(--text-main); font-weight: 700; display: block;">+966 11 471 8033</a>')}
{info_row(mail_svg, t['email_label'], f'<a href="mailto:info@jazdrm.com" style="color: var(--text-main); font-weight: 700; display: block;">info@jazdrm.com</a><a href="mailto:wafi@jazdrm.com" style="color: var(--text-main); font-weight: 700; display: block;">wafi@jazdrm.com</a>')}
{info_row(pin_svg, t['address_label'], f'<p style="color: var(--text-body); line-height: 1.8; font-size: 0.92rem; margin: 0;">{t["address_text"]}</p>')}
          </div>"""

    body = f"""
    <section class="section" style="padding-top: 50px;">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">{t['tag']}</span>
          <h1 class="section-title">{t['h1']}</h1>
          <p class="section-subtitle">{t['sub']}</p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; align-items: start;">
        <div class="form-card" style="margin: 0; max-width: 100%;">
          <form>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">{'الاسم بالكامل' if not is_en else 'Full Name'} *</label>
                <input type="text" class="form-control" required placeholder="{'محمد علي' if not is_en else 'John Doe'}">
              </div>
              <div class="form-group">
                <label class="form-label">{'رقم الجوال' if not is_en else 'Phone Number'} *</label>
                <input type="tel" class="form-control" required placeholder="05xxxxxxxx">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">{'البريد الإلكتروني' if not is_en else 'Email Address'}</label>
                <input type="email" class="form-control" placeholder="name@example.com">
              </div>
              <div class="form-group">
                <label class="form-label">{'المدينة / الفرع' if not is_en else 'City / Branch'}</label>
                <select class="form-control">
                  <option value="riyadh">{'الرياض (الفرع الرئيسي)' if not is_en else 'Riyadh (Main HQ)'}</option>
                  <option value="jeddah">{'جدة' if not is_en else 'Jeddah'}</option>
                  <option value="dammam">{'الدمام' if not is_en else 'Dammam'}</option>
                  <option value="medina">{'المدينة المنورة' if not is_en else 'Medina'}</option>
                  <option value="tabuk">{'تبوك' if not is_en else 'Tabuk'}</option>
                  <option value="buraydah">{'بريدة' if not is_en else 'Buraydah'}</option>
                  <option value="taif">{'الطائف' if not is_en else 'Taif'}</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">{'نص الرسالة أو الاستفسار' if not is_en else 'Message'} *</label>
              <textarea class="form-control" rows="4" required placeholder="{'اكتب استفسارك هنا...' if not is_en else 'Write your inquiry here...'}"></textarea>
            </div>
            <button type="submit" class="btn-primary" style="width: 100%; justify-content: center;">
              {'إرسال الرسالة' if not is_en else 'Send Message'}
            </button>
          </form>
        </div>
{contact_info_card}
        </div>
{get_contact_wa_cta(is_en)}
      </div>
    </section>
    """

    html = generate_base_html(
        title="اتصل بنا" if not is_en else "Contact Us",
        body_content=wire_form(body, "cf"),
        is_en=is_en,
        depth=2 if is_en else 1
    )
    
    out_path = ROOT_DIR / ("en/contact-us/index.html" if is_en else "contact-us/index.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

def build_service_request_page(is_en=False):
    t = {
        "tag": "طلب خدمة" if not is_en else "Service Request",
        "h1": "طلب خدمة صيانة أو تجهيز أو نقل" if not is_en else "Request Maintenance, Setup, or Relocation",
        "sub": "أدخل تفاصيل طلبك وسيقوم فريق العمل بالتواصل معك وتحديد موعد الزيارة الفنية فوراً." if not is_en else "Submit your service request and our technical team will schedule an on-site visit immediately.",
    }

    body = f"""
    <section class="section" style="padding-top: 50px;">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">{t['tag']}</span>
          <h1 class="section-title">{t['h1']}</h1>
          <p class="section-subtitle">{t['sub']}</p>
        </div>

        <div class="form-card">
          <form>
            <div class="form-group">
              <label class="form-label">{'نوع الخدمة المطلوبة' if not is_en else 'Service Type'} *</label>
              <select class="form-control" required>
                <option value="atm">{'تجهيز غرف الصراف والبنوك' if not is_en else 'ATM & Vault Room Setup'}</option>
                <option value="maintenance">{'صيانة دورية أو طارئة' if not is_en else 'Periodic / Emergency Maintenance'}</option>
                <option value="relocation">{'نقل وتركيب خزائن ثقيلة' if not is_en else 'Heavy Safe Relocation & Installation'}</option>
                <option value="filing">{'تركيب دواليب ملفات وخزائن إيداع' if not is_en else 'Filing Cabinet & Deposit Locker Installation'}</option>
                <option value="locks">{'برمجة وتركيب أقفال أمنية' if not is_en else 'Lock Programming & Installation'}</option>
              </select>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">{'اسم المنشأة أو العميل' if not is_en else 'Company / Customer Name'} *</label>
                <input type="text" class="form-control" required>
              </div>
              <div class="form-group">
                <label class="form-label">{'رقم الجوال' if not is_en else 'Phone Number'} *</label>
                <input type="tel" class="form-control" required placeholder="05xxxxxxxx">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">{'المدينة / الفرع الأقرب' if not is_en else 'City / Nearest Branch'}</label>
                <select class="form-control">
                  <option value="riyadh">{'الرياض' if not is_en else 'Riyadh'}</option>
                  <option value="jeddah">{'جدة' if not is_en else 'Jeddah'}</option>
                  <option value="dammam">{'الدمام' if not is_en else 'Dammam'}</option>
                  <option value="medina">{'المدينة المنورة' if not is_en else 'Medina'}</option>
                  <option value="tabuk">{'تبوك' if not is_en else 'Tabuk'}</option>
                  <option value="buraydah">{'بريدة' if not is_en else 'Buraydah'}</option>
                  <option value="taif">{'الطائف' if not is_en else 'Taif'}</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">{'الموعد المفضل للزيارة' if not is_en else 'Preferred Date'}</label>
                <input type="date" class="form-control">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">{'وصف المشكلة أو تفاصيل الطلب' if not is_en else 'Job Details'} *</label>
              <textarea class="form-control" rows="4" required placeholder="{'اكتب تفاصيل الخدمة والموقع بدقة...' if not is_en else 'Provide details regarding location and requirements...'}"></textarea>
            </div>
            <button type="submit" class="btn-primary" style="width: 100%; justify-content: center;">
              {'تقديم طلب الخدمة' if not is_en else 'Submit Service Request'}
            </button>
          </form>
        </div>
      </div>
    </section>
    """

    html = generate_base_html(
        title="طلب خدمة" if not is_en else "Service Request",
        body_content=wire_form(body, "sr"),
        is_en=is_en,
        depth=2 if is_en else 1
    )
    
    out_path = ROOT_DIR / ("en/service-request/index.html" if is_en else "service-request/index.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

def build_tech_support_page(is_en=False):
    t = {
        "tag": "الدعم الفني" if not is_en else "Technical Support",
        "h1": "مركز الدعم الفني وخدمة العملاء" if not is_en else "Technical Support & Customer Care",
        "sub": "نقدم الدعم الفني المتواصل على مدار الساعة لضمان استقرار وحماية أنظمتكم الأمنية." if not is_en else "24/7 dedicated support for emergency safe opening, lock reset, and fireproof cabinet servicing.",
    }

    body = f"""
    <section class="section" style="padding-top: 50px;">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">{t['tag']}</span>
          <h1 class="section-title">{t['h1']}</h1>
          <p class="section-subtitle">{t['sub']}</p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; margin-bottom: 50px;">
          <div class="branch-card" style="text-align: center; padding: 30px;">
            <div class="service-icon-box" style="margin: 0 auto 15px;">
              <svg viewBox="0 0 24 24"><path d="M20 15.5c-1.25 0-2.45-.2-3.57-.57a1.02 1.02 0 00-1.02.24l-2.2 2.2a15.045 15.045 0 01-6.59-6.59l2.2-2.21a.96.96 0 00.25-1A11.36 11.36 0 018.5 4c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1zM19 12h2a9 9 0 00-9-9v2c3.87 0 7 3.13 7 7zm-4 0h2a5 5 0 00-5-5v2c1.66 0 3 1.34 3 3z"/></svg>
            </div>
            <h3 class="branch-name">{'الرقم الموحد للدعم' if not is_en else 'Unified Support Line'}</h3>
            <p style="font-size: 1.3rem; font-weight: 800; color: var(--primary); margin: 10px 0;">+966920028440</p>
            <p style="color: var(--text-muted); font-size: 0.85rem;">{'متاح طوال أيام العمل' if not is_en else 'Available during business hours'}</p>
          </div>
          <div class="branch-card" style="text-align: center; padding: 30px;">
            <div class="service-icon-box" style="margin: 0 auto 15px; background: rgba(37, 211, 102, 0.12); color: #17823f;">
              <svg viewBox="0 0 24 24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0012.04 2z"/></svg>
            </div>
            <h3 class="branch-name">{'دعم الواتساب الفوري' if not is_en else 'Instant WhatsApp Help'}</h3>
            <p style="font-size: 1.1rem; font-weight: 800; color: #17823f; margin: 10px 0;">+966 55 489 0900</p>
            <p style="color: var(--text-muted); font-size: 0.85rem;">{'استجابة سريعة للحالات الطارئة' if not is_en else 'Fast response for emergency inquiries'}</p>
          </div>
        </div>

        <div class="form-card">
          <h3 style="font-size: 1.3rem; font-weight: 800; color: var(--primary-dark); margin-bottom: 20px; text-align: center;">{'فتح تذكرة دعم فني' if not is_en else 'Open Support Ticket'}</h3>
          <form>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">{'اسم العميل أو الجهة' if not is_en else 'Name / Company'} *</label>
                <input type="text" class="form-control" required>
              </div>
              <div class="form-group">
                <label class="form-label">{'رقم الجوال' if not is_en else 'Phone Number'} *</label>
                <input type="tel" class="form-control" required placeholder="05xxxxxxxx">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">{'نوع المشكلة الفنية' if not is_en else 'Issue Type'} *</label>
              <select class="form-control" required>
                <option value="lock">{'مشكلة في فتح قفل الخزنة أو الباب' if not is_en else 'Lock opening / password reset issue'}</option>
                <option value="cabinet">{'عطل في دولاب ملفات أو خزانة إيداع' if not is_en else 'Filing cabinet / deposit locker fault'}</option>
                <option value="door">{'صيانة أبواب الخزائن المحصنة' if not is_en else 'Vault door maintenance'}</option>
                <option value="other">{'أخرى' if not is_en else 'Other'}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">{'شرح تفصيلي للمشكلة' if not is_en else 'Issue Description'} *</label>
              <textarea class="form-control" rows="4" required></textarea>
            </div>
            <button type="submit" class="btn-primary" style="width: 100%; justify-content: center;">
              {'إرسال التذكرة' if not is_en else 'Submit Support Ticket'}
            </button>
          </form>
        </div>
      </div>
    </section>
    """

    html = generate_base_html(
        title="الدعم الفني" if not is_en else "Technical Support",
        body_content=wire_form(body, "ts"),
        is_en=is_en,
        depth=2 if is_en else 1
    )
    
    out_path = ROOT_DIR / ("en/technical-support/index.html" if is_en else "technical-support/index.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

def build_careers_page(is_en=False):
    t = {
        "tag": "التوظيف والمهن" if not is_en else "Careers",
        "h1": "انضم إلى فريق أحلام الجزيرة" if not is_en else "Join Our Professional Team",
        "sub": "نبحث دائماً عن الكفاءات المتميزة في مجالات الهندسة، الفنيين، والمبيعات." if not is_en else "We are always looking for top talent across engineering, security technicians, and sales.",
    }

    body = f"""
    <section class="section" style="padding-top: 50px;">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">{t['tag']}</span>
          <h1 class="section-title">{t['h1']}</h1>
          <p class="section-subtitle">{t['sub']}</p>
        </div>

        <div class="form-card">
          <form>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">{'الاسم الثلاثي' if not is_en else 'Full Name'} *</label>
                <input type="text" class="form-control" required>
              </div>
              <div class="form-group">
                <label class="form-label">{'رقم الجوال' if not is_en else 'Phone Number'} *</label>
                <input type="tel" class="form-control" required placeholder="05xxxxxxxx">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">{'البريد الإلكتروني' if not is_en else 'Email Address'} *</label>
                <input type="email" class="form-control" required>
              </div>
              <div class="form-group">
                <label class="form-label">{'الوظيفة المستهدفة' if not is_en else 'Target Position'} *</label>
                <select class="form-control" required>
                  <option value="tech">{'فني تركيب وصيانة خزائن' if not is_en else 'Security Safe Technician'}</option>
                  <option value="lock_eng">{'فني أقفال رقمية وأنظمة تحكم بالدخول' if not is_en else 'Digital Lock & Access Control Technician'}</option>
                  <option value="sales">{'مسؤول مبيعات ومشاريع' if not is_en else 'Sales & Project Executive'}</option>
                  <option value="admin">{'إدارة وخدمة عملاء' if not is_en else 'Customer Service / Admin'}</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">{'المدينة الحالية' if not is_en else 'Current City'}</label>
              <input type="text" class="form-control" placeholder="{'الرياض، جدة...' if not is_en else 'Riyadh, Jeddah...'}">
            </div>
            <div class="form-group">
              <label class="form-label">{'نبذة عن الخبرات والمهارات' if not is_en else 'Experience & Skills Summary'}</label>
              <textarea class="form-control" rows="4" placeholder="{'اذكر سنوات الخبرة والشهادات...' if not is_en else 'Summarize your experience and certifications...'}"></textarea>
            </div>
            <button type="submit" class="btn-primary" style="width: 100%; justify-content: center;">
              {'تقديم طلب التوظيف' if not is_en else 'Submit Application'}
            </button>
          </form>
        </div>
      </div>
    </section>
    """

    html = generate_base_html(
        title="التوظيف" if not is_en else "Careers",
        body_content=wire_form(body, "jb"),
        is_en=is_en,
        depth=2 if is_en else 1
    )
    
    out_path = ROOT_DIR / ("en/job-application/index.html" if is_en else "job-application/index.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

def build_single_product_pages():
    for p in PRODUCTS:
        slug = p["slug"]
        for is_en in [False, True]:
            rel = "../../../" if is_en else "../../"
            depth = 3 if is_en else 2
            
            title = p["title_en"] if is_en else p["title_ar"]
            cat = p["category_en"] if is_en else p["category_ar"]
            desc = product_desc(p, is_en)
            spec_rows = parse_specs(p, is_en)
            img = f"{rel}{p['image']}" if p["image"] else f"{rel}wp-content/uploads/2025/06/Asset-5.png"

            spec_table = ""
            if spec_rows:
                spec_table = (
                    f'<div class="product-specs">'
                    f'<div class="product-specs-model">{title}</div>'
                    f'<h2 class="product-specs-title">{"المواصفات" if not is_en else "Specifications"}</h2>'
                    f'<dl class="spec-list">'
                    + "".join(
                        f'<div class="spec-row"><dt>{k}</dt><dd>{v}</dd>'
                        f'<span class="spec-icon" aria-hidden="true">{_SPEC_ICONS.get(canon, _ICON_BOX)}</span></div>'
                        for k, v, canon in spec_rows
                    )
                    + "</dl></div>"
                )

            body = f"""
            <section class="section" style="padding-top: 40px;">
              <div class="container">
                <!-- Breadcrumbs -->
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 25px; display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                  <a href="{rel}{'en/' if is_en else ''}index.html" style="color: var(--primary);">{'الرئيسية' if not is_en else 'Home'}</a>
                  <span>/</span>
                  <a href="{rel}{'en/' if is_en else ''}products/index.html" style="color: var(--primary);">{'المنتجات' if not is_en else 'Products'}</a>
                  <span>/</span>
                  <span>{cat}</span>
                  <span>/</span>
                  <span style="color: var(--text-main); font-weight: 600;">{title}</span>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 50px; align-items: start; background: var(--bg-surface); padding: 40px; border-radius: var(--radius-xl); border: 1px solid var(--border-color); box-shadow: var(--shadow-sm);">
                  <div style="background: var(--bg-page); padding: 30px; border-radius: var(--radius-lg); text-align: center; border: 1px solid var(--border-color);">
                    <img src="{img}" alt="{title}" width="420" height="420" onerror="this.onerror=null; this.src='{rel}wp-content/uploads/2025/06/Asset-5.png';" style="max-height: 420px; margin: 0 auto; object-fit: contain;">
                    <button type="button" class="img-enlarge-btn open-image-lightbox" data-img="{img}" data-alt="{title}">{'تكبير صورة المنتج' if not is_en else 'Enlarge product image'}</button>
                  </div>
                  <div>
                    <span class="product-badge" style="position: static; display: inline-block; margin-bottom: 12px;">{cat}</span>
                    <h1 style="font-size: 2rem; font-weight: 800; color: var(--text-main); margin-bottom: 15px; line-height: 1.3;">{title}</h1>
                    <p style="color: var(--text-muted); font-size: 1rem; line-height: 1.8; margin-bottom: 25px;">
                      {desc or ('حل أمني متطور من شركة أحلام الجزيرة مصمم وفق أعلى معايير الجودة والمواصفات المعتمدة.' if not is_en else 'High security solution engineered to international standards by Aljazeera Dreams.')}
                    </p>

                    {spec_table}

                    <div style="background: var(--primary-tint); border: 1px solid var(--primary-light); padding: 20px; border-radius: var(--radius-md); margin: 24px 0 30px;">
                      <h3 style="font-size: 1rem; font-weight: 700; color: var(--primary-dark); margin-bottom: 10px;">{'الضمان والاعتماد' if not is_en else 'Warranty & Compliance'}</h3>
                      <ul style="font-size: 0.9rem; color: var(--text-body); line-height: 1.8; list-style: none; margin: 0; padding: 0;">
                        <li><span style="color: var(--primary-dark); font-weight: 700;">✓</span> {'مطابق لاشتراطات البنك المركزي والجهات الأمنية' if not is_en else 'Compliant with security & banking regulations'}</li>
                        <li><span style="color: var(--primary-dark); font-weight: 700;">✓</span> {'ضمان شامل وقطع غيار أصلية متوفرة' if not is_en else 'Comprehensive warranty & genuine spare parts'}</li>
                        <li><span style="color: var(--primary-dark); font-weight: 700;">✓</span> {'تركيب وتدريب فني معتمد من قبل مهندسينا' if not is_en else 'Professional installation & technical support'}</li>
                      </ul>
                    </div>

                    <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                      <button class="btn-primary open-quote-btn" data-product="{title}">
                        {'طلب تسعير المنتج' if not is_en else 'Request Quote'}
                      </button>
                      <a href="https://wa.me/966554890900?text=استفسار%20عن%20منتج%20{title}" target="_blank" class="btn-secondary" style="background: #25d366; color: #fff; border-color: #25d366;">
                        {'استفسار عبر واتساب' if not is_en else 'Inquire via WhatsApp'}
                      </a>
                    </div>
                  </div>
                </div>
              </div>

              <div class="modal-overlay image-lightbox" id="image-lightbox">
                <div class="image-lightbox-content" role="dialog" aria-modal="true" aria-label="{title}">
                  <button type="button" class="modal-close image-lightbox-close" aria-label="{'إغلاق' if not is_en else 'Close'}">&times;</button>
                  <img src="" alt="">
                </div>
              </div>
            </section>
            """

            html = generate_base_html(
                title=title,
                body_content=body,
                is_en=is_en,
                depth=depth
            )

            p_dir = ROOT_DIR / ("en/product" if is_en else "product") / slug
            p_dir.mkdir(parents=True, exist_ok=True)
            (p_dir / "index.html").write_text(html, encoding="utf-8")

def build_category_pages():
    for cat_key, slug, title_ar, title_en, banner_img in PRODUCT_CATEGORIES:
        alt_ar, alt_en = title_ar, title_en
        for is_en in [False, True]:
            rel = "../../../" if is_en else "../../"
            depth = 3 if is_en else 2
            title = title_en if is_en else title_ar

            banner = ""
            if banner_img:
                banner = (f'\n\n                <div class="category-banner-card">\n'
                          f'                  <img src="{rel}assets/img/banners/{banner_img}" width="1024" height="426" '
                          f'alt="{alt_en if is_en else alt_ar}" class="category-banner-img" loading="lazy">\n'
                          f'                </div>')

            tabs = build_filter_tabs(cat_key, is_en, "الكل" if not is_en else "All")

            body = f"""
            <section class="section" style="padding-top: 50px;">
              <div class="container">
                <div class="section-header">
                  <span class="section-tag">{'منتجات شركة أحلام الجزيرة' if not is_en else 'Aljazeera Dreams Company Products'}</span>
                  <h1 class="section-title">{title}</h1>
                  <p class="section-subtitle">{'تصفح أفضل منتجاتنا وحلولنا في هذا التصنيف' if not is_en else 'Browse our specialized product range in this category'}</p>
                </div>{banner}

                <div class="catalog-controls">
                  <div class="filter-tabs">
                    {tabs}
                  </div>
                  <div class="search-box">
                    <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
                    <input type="text" id="product-search-input" placeholder="{'ابحث في هذا التصنيف...' if not is_en else 'Search in this category...'}">
                  </div>
                </div>

                <div class="products-grid" id="products-grid-container">
                  <!-- Dynamically populated via assets/js/main.js -->
                </div>
              </div>
            </section>
            """

            html = generate_base_html(
                title=title,
                body_content=body,
                is_en=is_en,
                depth=depth,
                needs_products=True
            )

            c_dir = ROOT_DIR / ("en/product-category" if is_en else "product-category") / slug
            c_dir.mkdir(parents=True, exist_ok=True)
            (c_dir / "index.html").write_text(html, encoding="utf-8")

def build_legal_pages():
    """Privacy policy and terms — rebuilt on the shared template so they stay in sync."""
    pages = {
        "privacy-policy": {
            "title": ("سياسة الخصوصية", "Privacy Policy"),
            "updated": ("آخر تحديث: 2026", "Last updated: 2026"),
            "blocks": [
                (("مقدمة", "Introduction"),
                 ("نلتزم في شركة أحلام الجزيرة للمقاولات بحماية خصوصية بيانات عملائنا وزوّار موقعنا، وفق الأنظمة المعمول بها في المملكة العربية السعودية.",
                  "Aljazeera Dreams Contracting is committed to protecting the privacy of our clients and website visitors, in line with the regulations in force in Saudi Arabia.")),
                (("جمع البيانات واستخدامها", "Collection and use of data"),
                 ("تُستخدم البيانات المُدخلة في نماذج طلب عرض السعر والتواصل وطلب الخدمة لغرض الرد على الطلب والتنسيق مع العميل فقط، ولا تتم مشاركتها مع أي طرف ثالث لأغراض تسويقية.",
                  "Information you enter in the quotation, contact, and service-request forms is used only to respond to your request and coordinate with you. It is not shared with third parties for marketing purposes.")),
                (("حماية المعلومات", "Data security"),
                 ("تُحفظ البيانات في بيئة آمنة ويقتصر الوصول إليها على الموظفين المعنيين بتنفيذ الطلب.",
                  "Data is stored securely and access is limited to the staff handling your request.")),
                (("التواصل", "Contact"),
                 ("لأي استفسار يتعلق بالخصوصية يمكنكم التواصل معنا عبر الهاتف <bdi>+966920028440</bdi> أو صفحة اتصل بنا.",
                  "For any privacy question, contact us on <bdi>+966920028440</bdi> or via the Contact Us page.")),
            ],
        },
        "terms-and-conditions": {
            "title": ("الشروط والأحكام", "Terms & Conditions"),
            "updated": ("آخر تحديث: 2026", "Last updated: 2026"),
            "blocks": [
                (("نطاق الاستخدام", "Scope"),
                 ("تحكم هذه الشروط استخدام موقع شركة أحلام الجزيرة والخدمات والمنتجات المعروضة من خلاله. باستخدامك الموقع فإنك توافق على هذه الشروط.",
                  "These terms govern the use of the Aljazeera Dreams website and the services and products presented through it. By using the site you agree to these terms.")),
                (("عروض الأسعار", "Quotations"),
                 ("الأسعار والمواصفات المعروضة استرشادية، ويُعتمد العرض الرسمي الصادر من الشركة بعد المعاينة وتحديد المتطلبات.",
                  "Prices and specifications shown are indicative. The official quotation issued by the company after a site survey and requirement scoping is what applies.")),
                (("الضمان والصيانة", "Warranty and maintenance"),
                 ("تخضع الخزائن والأبواب والأقفال ودواليب الملفات وخزائن الإيداع لضمان الوكيل المعتمد، ووفق اتفاقيات مستوى الخدمة (SLA) المبرمة مع العميل.",
                  "Safes, doors, locks, filing cabinets, and deposit lockers are covered by the authorized manufacturer warranty and by the Service Level Agreement (SLA) signed with the client.")),
                (("التركيب", "Installation"),
                 ("يُنفَّذ النقل والتركيب بواسطة فنيي الشركة أو من تعتمدهم، ويُشترط تجهيز الموقع وفق المتطلبات الفنية المتفق عليها.",
                  "Transport and installation are carried out by company technicians or its approved partners, and require the site to be prepared to the agreed technical specifications.")),
            ],
        },
    }

    for slug, p in pages.items():
        for is_en in (False, True):
            title = p["title"][1] if is_en else p["title"][0]
            updated = p["updated"][1] if is_en else p["updated"][0]
            sections = "\n".join(
                f'          <h2>{h[1] if is_en else h[0]}</h2>\n'
                f'          <p>{b[1] if is_en else b[0]}</p>'
                for h, b in p["blocks"]
            )
            body = f"""
    <section class="section" style="padding-top: 48px;">
      <div class="container">
        <div class="legal">
          <span class="section-tag">{'معلومات قانونية' if not is_en else 'Legal'}</span>
          <h1 class="section-title">{title}</h1>
          <p class="legal-updated">{updated}</p>
          <div class="legal-body">
{sections}
          </div>
        </div>
      </div>
    </section>
    """
            html = generate_base_html(
                title=title, body_content=body, is_en=is_en, depth=2 if is_en else 1
            )
            out_dir = ROOT_DIR / (("en/" if is_en else "") + slug)
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "index.html").write_text(html, encoding="utf-8")


def build_sitemap():
    """sitemap.xml with AR/EN hreflang alternates for every real page. Regenerated
    on every build so it can never drift from the actual page list."""
    from urllib.parse import quote

    BASE = "https://jazdrm.com"

    paths = [""]
    paths += [
        "about-us/", "services/", "products/", "contact-us/",
        "service-request/", "technical-support/", "job-application/",
        "privacy-policy/", "terms-and-conditions/",
    ]
    paths += [f"product-category/{slug}/" for _key, slug, _ar, _en, _banner in PRODUCT_CATEGORIES]
    paths += [f"product/{p['slug']}/" for p in PRODUCTS]

    def url(path, is_en):
        prefix = "en/" if is_en else ""
        return f"{BASE}/{quote(prefix + path, safe='/')}"

    entries = []
    for path in paths:
        ar_url, en_url = url(path, False), url(path, True)
        for loc, alt in ((ar_url, en_url), (en_url, ar_url)):
            entries.append(f"""  <url>
    <loc>{loc}</loc>
    <xhtml:link rel="alternate" hreflang="ar" href="{ar_url}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{ar_url}"/>
  </url>""")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(entries)}
</urlset>
"""
    (ROOT_DIR / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_products_data_js():
    """assets/js/products-data.js drives the client-side catalog grid (main.js
    renderProducts()). It must stay in lockstep with assets/data/products.json -
    the two were allowed to drift before, which is why removed/renamed products
    kept showing up in the catalog grid after products.json was fixed."""
    js = "window.JAZDRM_PRODUCTS = " + json.dumps(PRODUCTS, ensure_ascii=False, indent=2) + ";\n"
    (ROOT_DIR / "assets" / "js" / "products-data.js").write_text(js, encoding="utf-8")


def main():
    print("Building all Arabic and English pages...")
    write_products_data_js()  # must run before any page is built: generate_base_html()
                               # hashes this file's content for the cache-busting ?v= param
    build_homepage(is_en=False)
    build_homepage(is_en=True)
    
    build_products_page(is_en=False)
    build_products_page(is_en=True)

    build_services_page(is_en=False)
    build_services_page(is_en=True)

    build_about_page(is_en=False)
    build_about_page(is_en=True)
    
    build_contact_page(is_en=False)
    build_contact_page(is_en=True)
    
    build_service_request_page(is_en=False)
    build_service_request_page(is_en=True)
    
    build_tech_support_page(is_en=False)
    build_tech_support_page(is_en=True)
    
    build_careers_page(is_en=False)
    build_careers_page(is_en=True)
    
    build_single_product_pages()
    build_category_pages()
    build_legal_pages()
    build_sitemap()

    print("All pages built successfully!")

if __name__ == "__main__":
    main()
