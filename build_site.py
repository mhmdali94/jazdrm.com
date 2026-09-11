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
    "Shelves(pc.)", "Fire Class", "Fire Rating",
    "Dimension", "Dimensions", "Outside", "Inside", "Overall", "Weight",
    "Capacity", "Shelves", "Shelf", "Boxes", "Drawers", "Locking", "Lock",
    "EMD", "Colour", "Color", "Material", "Body", "Door",
]
_SPEC_LABELS_AR = {
    "Dimension": "الأبعاد", "Dimensions": "الأبعاد", "Overall": "الأبعاد الكلية",
    "Outside": "الأبعاد الخارجية", "Inside": "الأبعاد الداخلية",
    "Outside(mm)": "الأبعاد الخارجية (مم)", "Inside(mm)": "الأبعاد الداخلية (مم)",
    "Weight": "الوزن", "Weight(kg)": "الوزن (كجم)", "Capacity": "السعة",
    "Shelf": "الأرفف", "Shelves": "الأرفف", "Boxes": "الأدراج", "Drawers": "الأدراج",
    "Locking": "نظام الإغلاق", "Lock": "القفل", "EMD": "فتحة الطوارئ (EMD)",
    "Fire Class": "مقاومة الحريق", "Fire Rating": "تصنيف الحريق",
    "Colour": "اللون", "Color": "اللون", "Material": "الخامة",
    "Body": "الهيكل", "Door": "الباب",
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
        rows.append((disp, val))
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
        "brand_title": "أحلام الجزيرة" if not is_en else "Aljazeera Dreams",
        "brand_sub": "للمقاولات والصيانة والأمن" if not is_en else "Contracting, Maintenance & Security",
        "home": "الرئيسية" if not is_en else "Home",
        "services": "خدماتنا" if not is_en else "Our Services",
        "products": "منتجاتنا" if not is_en else "Products",
        "partners": "عملاؤنا" if not is_en else "Clients & Partners",
        "about": "نبذة عنا" if not is_en else "About Us",
        "contact": "اتصل بنا" if not is_en else "Contact Us",
        "quote_btn": "طلب تسعير" if not is_en else "Request Quote",
        "cat_safes": "الخزائن والأبواب الأمنية" if not is_en else "Safes & Security Doors",
        "cat_surveillance": "أنظمة المراقبة والأمن" if not is_en else "Surveillance & Security",
        "cat_locks": "الأقفال الأمنية" if not is_en else "Security Locks",
        "sub_vault": "أبواب الخزائن المحصنة" if not is_en else "Vault & Bunker Doors",
        "sub_fireproof": "خزائن مقاومة للحريق" if not is_en else "Fireproof Safes",
        "sub_deposit": "خزائن الإيداع" if not is_en else "Deposit Lockers",
        "sub_filing": "دواليب الملفات الأمنية" if not is_en else "Security File Cabinets",
        "sub_cctv": "كاميرات مراقبة (Hikvision / Dahua)" if not is_en else "CCTV Cameras (Hikvision/Dahua)",
        "sub_dvr": "أنظمة تسجيل DVR / NVR" if not is_en else "DVR / NVR Recording Systems",
        "sub_screens": "شاشات مراقبة وتحكم" if not is_en else "Control & Monitor Screens",
        "sub_intercom": "أنظمة الإنتركوم الذكية" if not is_en else "Smart Intercom Systems",
        "sub_attendance": "أجهزة الحضور والانصراف" if not is_en else "Biometric Attendance Systems",
        "sub_digital_locks": "أقفال رقمية ذكية" if not is_en else "Smart Digital Locks",
        "sub_bio_locks": "أقفال بصمة الإصبع" if not is_en else "Fingerprint Locks",
        "sub_face_locks": "أقفال التعرف على الوجه" if not is_en else "Facial Recognition Locks",
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
    contact_url = f"{prefix}contact-us/index.html"
    service_req_url = f"{prefix}service-request/index.html"
    tech_support_url = f"{prefix}technical-support/index.html"
    careers_url = f"{prefix}job-application/index.html"

    safes_url = f"{prefix}product-category/الخزائن-والأبواب-الأمنية/index.html"
    surveillance_url = f"{prefix}product-category/أنظمة-المراقبة-والأمن/index.html"
    locks_url = f"{prefix}product-category/الأقفال-الأمنية/index.html"

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
          <img src="{rel}wp-content/uploads/2025/06/Asset-5.png" alt="{t['brand_title']}" width="468" height="374">
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
            <a href="{home_url}#services" class="nav-link">
              <span>{t['services']}</span>
              <svg class="arrow" viewBox="0 0 10 6"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>
            </a>
            <div class="dropdown-menu">
              <a href="{home_url}#services" class="dropdown-item">{t['sub_vault']}</a>
              <a href="{home_url}#services" class="dropdown-item">{t['sub_fireproof']}</a>
              <a href="{home_url}#services" class="dropdown-item">{t['sub_cctv']}</a>
              <a href="{service_req_url}" class="dropdown-item">{t['service_req']}</a>
            </div>
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
          <div class="nav-item">
            <a href="{safes_url}" class="nav-link">
              <span>{t['cat_safes']}</span>
              <svg class="arrow" viewBox="0 0 10 6"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>
            </a>
            <div class="dropdown-menu">
              <a href="{safes_url}" class="dropdown-item">{t['sub_vault']}</a>
              <a href="{safes_url}" class="dropdown-item">{t['sub_fireproof']}</a>
              <a href="{safes_url}" class="dropdown-item">{t['sub_deposit']}</a>
              <a href="{safes_url}" class="dropdown-item">{t['sub_filing']}</a>
            </div>
          </div>
          <div class="nav-item">
            <a href="{surveillance_url}" class="nav-link">
              <span>{t['cat_surveillance']}</span>
              <svg class="arrow" viewBox="0 0 10 6"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>
            </a>
            <div class="dropdown-menu">
              <a href="{surveillance_url}" class="dropdown-item">{t['sub_cctv']}</a>
              <a href="{surveillance_url}" class="dropdown-item">{t['sub_dvr']}</a>
              <a href="{surveillance_url}" class="dropdown-item">{t['sub_screens']}</a>
              <a href="{surveillance_url}" class="dropdown-item">{t['sub_intercom']}</a>
              <a href="{surveillance_url}" class="dropdown-item">{t['sub_attendance']}</a>
            </div>
          </div>
          <div class="nav-item">
            <a href="{locks_url}" class="nav-link">
              <span>{t['cat_locks']}</span>
              <svg class="arrow" viewBox="0 0 10 6"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>
            </a>
            <div class="dropdown-menu">
              <a href="{locks_url}" class="dropdown-item">{t['sub_digital_locks']}</a>
              <a href="{locks_url}" class="dropdown-item">{t['sub_bio_locks']}</a>
              <a href="{locks_url}" class="dropdown-item">{t['sub_face_locks']}</a>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </header>

  <!-- Mobile Drawer -->
  <div class="drawer-backdrop"></div>
  <div class="mobile-drawer" id="mobile-drawer" aria-label="{t['nav_drawer']}" aria-hidden="true">
    <div class="mobile-drawer-header">
      <div class="brand-logo">
        <img src="{rel}wp-content/uploads/2025/06/Asset-5.png" alt="{t['brand_title']}" width="468" height="374" style="height: 38px;">
        <span class="brand-title" style="font-size: 1.1rem;">{t['brand_title']}</span>
      </div>
      <button type="button" class="drawer-close-btn" aria-label="{t['close']}">&times;</button>
    </div>
    <nav class="mobile-drawer-body" aria-label="{t['nav_drawer']}">
      <a href="{home_url}" class="nav-link">{t['home']}</a>
      <a href="{products_url}" class="nav-link">{t['products']}</a>
      <a href="{safes_url}" class="nav-link">{t['cat_safes']}</a>
      <a href="{surveillance_url}" class="nav-link">{t['cat_surveillance']}</a>
      <a href="{locks_url}" class="nav-link">{t['cat_locks']}</a>
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
    contact_url = f"{prefix}contact-us/index.html"
    privacy_url = f"{prefix}privacy-policy/index.html"
    terms_url = f"{prefix}terms-and-conditions/index.html"
    service_req_url = f"{prefix}service-request/index.html"
    tech_support_url = f"{prefix}technical-support/index.html"

    safes_url = f"{prefix}product-category/الخزائن-والأبواب-الأمنية/index.html"
    surveillance_url = f"{prefix}product-category/أنظمة-المراقبة-والأمن/index.html"
    locks_url = f"{prefix}product-category/الأقفال-الأمنية/index.html"

    t = {
        "about_p": "شركة أحلام الجزيرة للمقاولات والصيانة: رواد تزويد وتركيب الخزائن والأبواب الأمنية المحصنة، وأنظمة المراقبة والتحكم، والأقفال الذكية لكبرى البنوك والشركات والمؤسسات في المملكة." if not is_en else "Aljazeera Dreams Contracting & Maintenance: pioneers in security safes, bunker vault doors, surveillance, and smart locks for major banks and corporations across Saudi Arabia.",
        "nav_title": "روابط سريعة" if not is_en else "Quick Links",
        "cats_title": "التصنيفات" if not is_en else "Categories",
        "contact_title": "تواصل معنا" if not is_en else "Contact Us",
        "address": "الرياض (الفرع الرئيسي)، حي الروابي، شارع طاهر الدباغ" if not is_en else "Riyadh (Main HQ), Al-Rawabi, Taher Al-Dabbagh St.",
        "branches": "فروعنا: الرياض، جدة، المدينة المنورة، تبوك، بريدة، الطائف" if not is_en else "Branches: Riyadh, Jeddah, Medina, Tabuk, Buraydah, Taif",
        "copyright": "جميع الحقوق محفوظة © 2026 · شركة أحلام الجزيرة للمقاولات والصيانة" if not is_en else "All Rights Reserved © 2026 · Aljazeera Dreams Co.",
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
            <img src="{rel}wp-content/uploads/2025/06/Asset-5.png" alt="أحلام الجزيرة" width="468" height="374" style="height: 48px;">
            <span class="brand-title" style="color: #fff; font-size: 1.2rem;">{'أحلام الجزيرة' if not is_en else 'Aljazeera Dreams'}</span>
          </div>
          <p>{t['about_p']}</p>
        </div>
        <div>
          <h3 class="footer-title">{t['nav_title']}</h3>
          <div class="footer-links">
            <a href="{home_url}">{'الرئيسية' if not is_en else 'Home'}</a>
            <a href="{about_url}">{'نبذة عنا' if not is_en else 'About Us'}</a>
            <a href="{products_url}">{'منتجاتنا' if not is_en else 'Products'}</a>
            <a href="{service_req_url}">{'طلب خدمة' if not is_en else 'Service Request'}</a>
            <a href="{tech_support_url}">{'الدعم الفني' if not is_en else 'Technical Support'}</a>
            <a href="{contact_url}">{'اتصل بنا' if not is_en else 'Contact Us'}</a>
          </div>
        </div>
        <div>
          <h3 class="footer-title">{t['cats_title']}</h3>
          <div class="footer-links">
            <a href="{safes_url}">{'الخزائن والأبواب الأمنية' if not is_en else 'Safes & Vault Doors'}</a>
            <a href="{surveillance_url}">{'أنظمة المراقبة والأمن' if not is_en else 'Surveillance Systems'}</a>
            <a href="{locks_url}">{'الأقفال الأمنية الذكية' if not is_en else 'Security Locks'}</a>
            <a href="{safes_url}">{'خزائن الإيداع والغرف المحصنة' if not is_en else 'Deposit & Vault Lockers'}</a>
          </div>
        </div>
        <div>
          <h3 class="footer-title">{t['contact_title']}</h3>
          <div class="footer-links">
            <p style="color: rgba(255,255,255,0.7); font-size: 0.88rem; margin-bottom: 8px;">{t['address']}</p>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.88rem; margin-bottom: 12px;">{t['branches']}</p>
            <a href="tel:+966920028440" style="color: var(--accent-cyan); font-weight: 700; font-size: 1.1rem;">+966920028440</a>
            <a href="https://wa.me/966554890900" target="_blank" style="color: #25d366; font-weight: 600;">+966 55 489 0900 (WhatsApp)</a>
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


def generate_base_html(title, body_content, is_en=False, depth=0):
    rel = "../" * depth
    dir_attr = 'dir="ltr" lang="en"' if is_en else 'dir="rtl" lang="ar"'
    body_cls = 'en-lang' if is_en else 'ar-lang'
    skip_label = 'تخطي إلى المحتوى' if not is_en else 'Skip to content'

    header = get_header(is_en=is_en, depth=depth)
    footer = get_footer(is_en=is_en, depth=depth)

    return f"""<!DOCTYPE html>
<html {dir_attr}>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {'شركة أحلام الجزيرة' if not is_en else 'Aljazeera Dreams Co.'}</title>
  <meta name="description" content="{'شركة أحلام الجزيرة للمقاولات والصيانة: حلول الخزائن والأبواب الأمنية، أنظمة المراقبة، والأقفال الذكية' if not is_en else 'Aljazeera Dreams: premium security safes, vault doors, CCTV surveillance, and biometric locks in Saudi Arabia'}">
  <link rel="icon" href="{rel}wp-content/uploads/2025/06/cropped-favicon-32x32.png" sizes="32x32">
  <link rel="icon" href="{rel}wp-content/uploads/2025/06/cropped-favicon-192x192.png" sizes="192x192">
  <link rel="apple-touch-icon" href="{rel}wp-content/uploads/2025/06/cropped-favicon-180x180.png">
  <link rel="preload" href="{rel}assets/fonts/{'cairo-latin.woff2' if is_en else 'cairo-arabic.woff2'}" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{rel}assets/css/style.css">
</head>
<body class="{body_cls}" data-root="{rel}">
  <a class="skip-link" href="#main-content">{skip_label}</a>
  {header}
  <main id="main-content" tabindex="-1">
    {body_content}
  </main>
  {footer}

  <script src="{rel}assets/js/products-data.js"></script>
  <script src="{rel}assets/js/main.js"></script>
</body>
</html>
"""

def get_brand_wall(is_en=False, rel=""):
    """Monochrome wordmark wall for the globally-authorized product brands."""
    cat_prefix = f"{rel}en/" if is_en else f"{rel}"
    safes_cat = f"{cat_prefix}product-category/الخزائن-والأبواب-الأمنية/index.html"
    surv_cat = f"{cat_prefix}product-category/أنظمة-المراقبة-والأمن/index.html"
    view = "استعراض المنتجات" if not is_en else "View products"

    G = {
        "vault": '<rect x="3.5" y="4.5" width="17" height="15" rx="1.5"/><circle cx="10" cy="12" r="3"/><path d="M10 12l1.8-1.8"/><path d="M16.5 9.2v5.6"/>',
        "shield": '<path d="M12 3.2l7 2.6v4.9c0 4.3-2.9 7.6-7 8.9-4.1-1.3-7-4.6-7-8.9V5.8z"/><path d="M9 12l2.1 2.1L15.2 10"/>',
        "fingerprint": '<path d="M12 4.6c-4 0-7 2.9-7 7.1 0 1.4.2 2.7.6 3.8"/><path d="M8.5 12c0-1.9 1.5-3.4 3.5-3.4s3.5 1.5 3.5 3.4c0 2 0 4-1 5.8"/><path d="M12 12v3.2c0 1.4-.3 2.7-.8 3.9"/><path d="M18.4 15.6c.4-1.2.6-2.4.6-3.6 0-1.6-.5-3-1.4-4.2"/>',
        "sun": '<circle cx="12" cy="12" r="3.6"/><path d="M12 3.5v2M12 18.5v2M4.7 4.7l1.4 1.4M17.9 17.9l1.4 1.4M3.5 12h2M18.5 12h2M4.7 19.3l1.4-1.4M17.9 6.1l1.4-1.4"/>',
        "bullet_cam": '<rect x="3" y="8" width="12.5" height="6.5" rx="2"/><path d="M15.5 9.5l4.5-2.2v9.4l-4.5-2.2z"/><path d="M7 14.5v4.5"/><path d="M5 19h4"/>',
        "dome_cam": '<path d="M4.5 12a7.5 7.5 0 0115 0z"/><circle cx="12" cy="11.4" r="2.1"/><path d="M12 12.2V19"/><path d="M9.5 19h5"/>',
    }

    brands = [
        ("falcon",    "falcon.png",    "FALCON",   "SAFES",      G["vault"],       safes_cat),
        ("diplomat",  "diplomat.png",  "DIPLOMAT", "",           G["shield"],      safes_cat),
        ("jiabao",    "jiabao.svg",    "JIABAO",   "SECURITY",   G["fingerprint"], safes_cat),
        ("sunpower",  "sunpower.svg",  "SUNPOWER", "",           G["sun"],         safes_cat),
        ("hik",       "hikvision.svg", "HIKVISION","",           G["bullet_cam"],  surv_cat),
        ("dahua",     "dahua.svg",     "DAHUA",    "TECHNOLOGY", G["dome_cam"],    surv_cat),
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
    """Trusted-by strip: client logos carried over from the original site's
    'شركاؤنا في النجاح' section (files already in the media library)."""
    clients = [
        ("01", "شركة عبدالله عثمان المبحر وأولاده للصرافة", "Abdullah Othman Almbher Exchange"),
        ("02", "السبيعي للصرافة", "Al Subaie Exchange"),
        ("03", "البنك العربي الوطني", "Arab National Bank"),
        ("04", "بنك الجزيرة", "Bank AlJazira"),
        ("05", "بنك البلاد", "Bank Albilad"),
        ("06", "بنك مسقط", "Bank Muscat"),
        ("07", "البنك السعودي الفرنسي", "Banque Saudi Fransi"),
        ("08", "بنك الخليج الدولي", "Gulf International Bank"),
        ("09", "البنك السعودي للاستثمار", "The Saudi Investment Bank"),
        ("10", "البنك الأهلي السعودي", "Saudi National Bank"),
        ("11", "بنك الرياض", "Riyad Bank"),
        ("12", "بنك الإمارات دبي الوطني", "Emirates NBD"),
        ("13", "ماكدونالدز", "McDonald's"),
        ("14", "إرسال لتحويل الأموال", "Ersal Money Transfer"),
        ("15", "مصرف الإنماء", "Alinma Bank"),
    ]
    return "\n".join(
        f'          <li class="client-logo">'
        f'<img src="{rel}assets/img/clients/client-{n}.png" alt="{en if is_en else ar}" width="200" height="150" '
        f'loading="lazy" decoding="async" '
        f'onerror="this.closest(\'.client-logo\').remove()"></li>'
        for n, ar, en in clients
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
            f'          <img src="{rel}assets/img/banners/banner-clients.jpg" alt="{alt}" width="1024" height="426" loading="lazy">\n'
            f'        </div>')


def division_card(img, alt, tag, title, desc, href, btn, comment=""):
    cmt = f"          <!-- {comment} -->\n" if comment else ""
    return f"""{cmt}          <article class="division-card">
            <div class="division-media">
              <img src="{img}" alt="{alt}" width="1024" height="426" loading="lazy">
            </div>
            <div class="division-body">
              <span class="division-tag">{tag}</span>
              <h3 class="division-title">{title}</h3>
              <p class="division-desc">{desc}</p>
              <a href="{href}" class="division-btn">
                <span>{btn}</span>
                {_ARROW_SVG}
              </a>
            </div>
          </article>"""


def _division_cards(is_en, banner_rel, cat_rel):
    """banner_rel: prefix to assets/  ·  cat_rel: prefix to product-category/"""
    b = f"{banner_rel}assets/img/banners/"
    safes_href = f"{cat_rel}product-category/الخزائن-والأبواب-الأمنية/index.html"
    surv_href = f"{cat_rel}product-category/أنظمة-المراقبة-والأمن/index.html"
    if is_en:
        return (
            division_card(f"{b}banner-safes.jpg", "Security Safes and Vault Doors",
                "Safes & Vault Doors", "Heavy Commercial & Banking Safes",
                "Reinforced bank safes, vault doors, and deposit boxes engineered and tested against burglary and fire to SAMA-compliant standards.",
                safes_href, "Explore Safes Catalog", "Division 1: Safes & Vaults"),
            division_card(f"{b}banner-cctv.jpg", "Smart CCTV and Surveillance Systems",
                "Smart Surveillance", "Advanced Surveillance Systems (Dahua)",
                "Enterprise IP cameras, PTZ, night-vision dome sensors, and high-performance NVR network recorders with comprehensive warranty.",
                surv_href, "Explore Surveillance Catalog", "Division 2: CCTV Surveillance"),
        )
    return (
        division_card(f"{b}banner-safes.jpg", "الخزائن والأبواب الأمنية المحصنة",
            "خزائن وأبواب محصنة", "الخزائن والأبواب المصرفية المحصنة",
            "خزائن مصرفية ثقيلة، أبواب غرف محصنة، وخزائن أمانات مصممة ومختبرة لمقاومة السطو والحرائق وفق أعلى المعايير المعتمدة لكبرى البنوك والمؤسسات.",
            safes_href, "استعراض منتجات الخزائن", "Division 1: Safes & Vaults"),
        division_card(f"{b}banner-cctv.jpg", "أنظمة المراقبة والكاميرات الذكية",
            "مراقبة وتحكم ذكي", "أنظمة المراقبة المتطورة (Dahua)",
            "منظومات مراقبة شبكية متقدمة تشمل كاميرات PTZ، كاميرات القبة والرؤية الليلية الذكية، وأجهزة التسجيل الشبكية NVR بأعلى دقة وتكامل سحابي.",
            surv_href, "استعراض أنظمة المراقبة", "Division 2: CCTV Surveillance"),
    )


def get_divisions_section(is_en=False, rel=""):
    tag = "أبرز قطاعاتنا الأمنية" if not is_en else "Specialized Divisions"
    h2 = ("حلول الأمان المصرفي والمراقبة المتطورة" if not is_en
          else "Banking Security Solutions & Smart Surveillance")
    sub = ("نوفر تجهيزات متكاملة تلبي أعلى اشتراطات الأمان المعتمدة في المملكة" if not is_en
           else "Delivering turnkey installations meeting the highest national security and compliance standards")
    # homepage sits at its language root: category links are same-dir relative
    c1, c2 = _division_cards(is_en, rel, "")
    return f"""    <!-- Flagship Security Divisions -->
    <section class="section" style="background: var(--bg-surface); border-top: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color);">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">{tag}</span>
          <h2 class="section-title">{h2}</h2>
          <p class="section-subtitle">{sub}</p>
        </div>

        <div class="divisions-grid">
{c1}

{c2}
        </div>
      </div>
    </section>"""


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
    cat = "../"
    safes_href = f"{cat}product-category/الخزائن-والأبواب-الأمنية/index.html"
    surv_href = f"{cat}product-category/أنظمة-المراقبة-والأمن/index.html"
    if is_en:
        p_tag, p_h2 = "Accredited by Top Financial Institutions", "Trusted Security Partner for Saudi Banking"
        banner_alt = "Banking Accreditations - Top Banks in Saudi Arabia"
        d_tag, d_h2 = "Core Expertise", "Integrated Security Divisions"
        c1 = division_card(f"{assets}assets/img/banners/banner-safes.jpg", "Security Safes and Vault Doors",
            "Safes & Vault Doors", "Commercial & Banking Safes",
            "Turnkey fitting of financial institutions with heavy certified vaults meeting SAMA security standards.",
            safes_href, "Explore Products")
        c2 = division_card(f"{assets}assets/img/banners/banner-cctv.jpg", "Smart CCTV Systems",
            "Smart Surveillance", "Smart Surveillance Systems",
            "Advanced enterprise Dahua cameras and recording networks for critical infrastructure defense.",
            surv_href, "Explore Products")
    else:
        p_tag, p_h2 = "اعتمادات كبرى المصارف", "شريك الأمان المعتمد لدى البنوك السعودية"
        banner_alt = "اعتمادات مصرفية - كبرى البنوك والمصارف"
        d_tag, d_h2 = "مجالات التميز والتخصص", "أقسامنا وحلولنا المتكاملة"
        c1 = division_card(f"{assets}assets/img/banners/banner-safes.jpg", "الخزائن والأبواب الأمنية المحصنة",
            "خزائن وأبواب محصنة", "الخزائن والأبواب المصرفية",
            "تجهيز كامل لغرف البنوك والمصارف بخزائن ثقيلة وأبواب محصنة مطابقة لمعايير SAMA العالمية.",
            safes_href, "استعراض المنتجات")
        c2 = division_card(f"{assets}assets/img/banners/banner-cctv.jpg", "أنظمة المراقبة والكاميرات الذكية",
            "مراقبة وتحكم ذكي", "أنظمة المراقبة الذكية",
            "كاميرات متقدمة وشبكات تسجيل Dahua عالية الدقة لضمان الحماية الشاملة للمنشآت والمواقع الحيوية.",
            surv_href, "استعراض المنتجات")
    return f"""        <!-- Banking Partners & Trust Showcase -->
        <div class="section-header" style="margin-top: 50px; margin-bottom: 25px;">
          <span class="section-tag">{p_tag}</span>
          <h2 class="section-title">{p_h2}</h2>
        </div>
        <div class="clients-banner-wrapper" style="margin-bottom: 50px;">
          <img src="{assets}assets/img/banners/banner-clients.jpg" alt="{banner_alt}" width="1024" height="426" loading="lazy">
        </div>

        <!-- Core Divisions -->
        <div class="section-header" style="margin-bottom: 25px;">
          <span class="section-tag">{d_tag}</span>
          <h2 class="section-title">{d_h2}</h2>
        </div>
        <div class="divisions-grid" style="margin-bottom: 50px;">
{c1}
{c2}
        </div>"""


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
        "sub": "نقدم خدمات التوريد والتركيب والصيانة الدورية للخزائن والأبواب المصرفية المحصنة، كاميرات المراقبة، والأقفال الرقمية المتطورة لكبرى البنوك والمؤسسات في كافة أنحاء المملكة." if not is_en else "Supplying, installing, and maintaining fortified bank vault doors, fireproof safes, AI video surveillance, and biometric locks for enterprises across Saudi Arabia.",
        "explore_btn": "استكشف المنتجات" if not is_en else "Explore Products",
        "quote_btn": "طلب عرض سعر" if not is_en else "Request Quote",
        "stat_years": "+15" if not is_en else "15+",
        "stat_years_lbl": "عاماً من الخبرة" if not is_en else "Years Experience",
        "stat_proj": "+500" if not is_en else "500+",
        "stat_proj_lbl": "مشروع مصرفي وتجاري" if not is_en else "Banking & Enterprise Projects",
        "stat_branches": "6" if not is_en else "6",
        "stat_branches_lbl": "فروع بالمملكة" if not is_en else "Branches in KSA",
        "floating_cert": "معتمدون لدى كبرى البنوك" if not is_en else "Certified by Major Banks",
        "srv_tag": "خدماتنا المتميزة" if not is_en else "Our Core Services",
        "srv_h2": "حلول مقاولات وأمن شاملة بأعلى المعايير" if not is_en else "Comprehensive Contracting & Security Standards",
        "srv1_title": "تجهيز غرف الصراف والبنوك" if not is_en else "ATM & Vault Room Setup",
        "srv1_desc": "تجهيز وتصفيح غرف الصراف الآلي (ATM) وغرف الخزائن الرئيسية وفق اشتراطات البنك المركزي السعودي." if not is_en else "Armor plating and custom engineering for bank ATM enclosures and vault rooms meeting central bank standards.",
        "srv2_title": "صيانة دورية وعقود تشغيل" if not is_en else "Periodic Maintenance Contracts",
        "srv2_desc": "عقود صيانة معتمدة لضمان استمرارية عمل الأبواب المحصنة، أجهزة الإنذار، وأنظمة المراقبة 24/7." if not is_en else "Certified SLA maintenance ensuring 24/7 reliability for fortified doors, alarms, and CCTV systems.",
        "srv3_title": "نقل وتركيب الخزائن الثقيلة" if not is_en else "Heavy Safe Relocation & Install",
        "srv3_desc": "معدات متخصصة لنقل وتركيب الخزائن والأبواب المحصنة ذات الأوزان العالية بأمان تام." if not is_en else "Specialized heavy equipment for transporting and anchoring multi-ton vaults and safes securely.",
        "srv4_title": "أنظمة المراقبة والتحكم الذكي" if not is_en else "AI Surveillance & Access Control",
        "srv4_desc": "كاميرات مراقبة متطورة بدقة 4K مع تقنيات التعرف على الوجوه والتكامل السحابي." if not is_en else "Advanced 4K AI surveillance with facial recognition, motion tracking, and remote cloud management.",
        "srv_lead": "من تصفيح غرف الصراف الآلي إلى عقود الصيانة طويلة الأمد، نغطّي دورة حياة المنشأة الأمنية بالكامل تحت سقف واحد." if not is_en else "From armor-plating ATM rooms to long-term maintenance contracts, we cover the full lifecycle of a secure facility under one roof.",
        "srv_cta": "تحدث إلى مهندس" if not is_en else "Talk to an Engineer",
        "partners_tag": "شركاء النجاح" if not is_en else "Partners of Success",
        "partners_h2": "العلامات التجارية المعتمدة عالمياً" if not is_en else "Globally Authorized Brands",
        "partners_sub": "نورّد ونركّب أنظمة ومنتجات أمنية أصلية من كبرى المصنّعين العالميين، باعتماد رسمي وضمان معتمد." if not is_en else "We supply and install original security systems and hardware from the world's leading manufacturers, under official authorization and warranty.",
        "branches_tag": "تغطية شاملة" if not is_en else "Nationwide Coverage",
        "branches_h2": "فروعنا في جميع أنحاء المملكة" if not is_en else "Our Branches Across Saudi Arabia",
    }

    products_page_url = f"{rel}products/index.html" if not is_en else f"{rel}en/products/index.html"

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
            <img src="{rel}wp-content/uploads/2025/06/IMG_0055_0171-500x500.webp" alt="SSM 130 Vault Door" width="500" height="500">
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
    <section class="clients">
      <div class="container">
        <div class="clients-head">
          <span class="section-tag">{'ثقة مؤسسية' if not is_en else 'Institutional trust'}</span>
          <h2 class="section-title">{'شركاؤنا في النجاح' if not is_en else 'Partners in Success'}</h2>
          <p class="section-subtitle">{'تعتمد كبرى البنوك والمصارف والمؤسسات في المملكة والخليج على أنظمة أحلام الجزيرة الأمنية.' if not is_en else 'Leading banks and institutions across Saudi Arabia and the Gulf rely on Aljazeera Dreams security systems.'}</p>
          <p class="clients-count"><strong>+15</strong> {'جهة مصرفية ومؤسسية' if not is_en else 'banking &amp; institutional clients'}</p>
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
          </ol>
        </div>
      </div>
    </section>

{get_divisions_section(is_en, rel)}

    <!-- Brands & Partners -->
    <section class="brands-section" id="partners">
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

def build_products_page(is_en=False):
    t = {
        "tag": "كتالوج المنتجات" if not is_en else "Product Catalog",
        "h1": "جميع الخزائن وأنظمة الأمان والمراقبة" if not is_en else "All Security Safes, Vaults & Surveillance",
        "sub": "تصفح تشكيلتنا الشاملة من الخزائن المصرفية المقاومة للحريق والسرقة، كاميرات المراقبة، والأقفال الذكية." if not is_en else "Explore our full catalog of fireproof bank vaults, ATM safes, 4K CCTV systems, and biometric locks.",
        "tab_all": "جميع المنتجات" if not is_en else "All Products",
        "tab_safes": "الخزائن والأبواب" if not is_en else "Safes & Doors",
        "tab_surv": "المراقبة والكاميرات" if not is_en else "Surveillance & CCTV",
        "tab_locks": "الأقفال الذكية" if not is_en else "Smart Locks",
        "search_ph": "ابحث عن موديل أو منتج..." if not is_en else "Search model or product name...",
    }

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
            <button class="filter-tab active" data-category="all">{t['tab_all']}</button>
            <button class="filter-tab" data-category="safes">{t['tab_safes']}</button>
            <button class="filter-tab" data-category="surveillance">{t['tab_surv']}</button>
            <button class="filter-tab" data-category="locks">{t['tab_locks']}</button>
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
        depth=2 if is_en else 1
    )
    
    out_path = ROOT_DIR / ("en/products/index.html" if is_en else "products/index.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

def build_about_page(is_en=False):
    t = {
        "tag": "من نحن" if not is_en else "About Us",
        "h1": "شركة أحلام الجزيرة للمقاولات والصيانة" if not is_en else "Aljazeera Dreams Contracting & Maintenance",
        "sub": "أكثر من 15 عاماً من الخبرة والتميز في تزويد وتركيب أحدث تقنيات الخزائن والأبواب الأمنية والحلول المصرفية في المملكة العربية السعودية." if not is_en else "Over 15 years of excellence delivering high-security safes, vault doors, and smart banking solutions across Saudi Arabia.",
        "vision_title": "رؤيتنا" if not is_en else "Our Vision",
        "vision_desc": "أن نكون الخيار الأول والموثوق في المملكة العربية السعودية والخليج لتوريد وتركيب وصيانة أحدث حلول الأمان والخزائن المحصنة." if not is_en else "To be the leading and most trusted provider of advanced security safes, fortified vault doors, and contracting solutions in the region.",
        "mission_title": "رسالتنا" if not is_en else "Our Mission",
        "mission_desc": "تقديم منتجات وخدمات أمنية متفوقة تلتزم بأعلى المعايير والمواصفات العالمية، مع توفير دعم فني وصيانة مستمرة على مدار الساعة." if not is_en else "Delivering superior security products compliant with international standards, supported by 24/7 technical support and SLA maintenance.",
    }

    body = f"""
    <section class="section" style="padding-top: 50px;">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">{t['tag']}</span>
          <h1 class="section-title">{t['h1']}</h1>
          <p class="section-subtitle">{t['sub']}</p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; margin-bottom: 60px;">
          <div class="form-card" style="margin: 0; max-width: 100%;">
            <div class="service-icon-box">
              <svg viewBox="0 0 24 24"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/></svg>
            </div>
            <h3 style="font-size: 1.4rem; font-weight: 800; color: var(--primary-dark); margin-bottom: 12px;">{t['vision_title']}</h3>
            <p style="color: var(--text-muted); line-height: 1.8;">{t['vision_desc']}</p>
          </div>
          <div class="form-card" style="margin: 0; max-width: 100%;">
            <div class="service-icon-box">
              <svg viewBox="0 0 24 24"><path d="M12 2L1 21h22L12 2zm0 3.8l7.53 13.2H4.47L12 5.8z"/></svg>
            </div>
            <h3 style="font-size: 1.4rem; font-weight: 800; color: var(--primary-dark); margin-bottom: 12px;">{t['mission_title']}</h3>
            <p style="color: var(--text-muted); line-height: 1.8;">{t['mission_desc']}</p>
          </div>
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
                <option value="cctv">{'تركيب وصيانة أنظمة مراقبة وأمن' if not is_en else 'CCTV & Security System Installation'}</option>
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
        "sub": "نقدم الدعم الفني المتواصل على مدار الساعة لضمان استقرار وحماية أنظمتكم الأمنية." if not is_en else "24/7 dedicated support for emergency safe opening, lock reset, and CCTV diagnostics.",
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
            <div class="service-icon-box" style="margin: 0 auto 15px; background: #e8f5e9; color: #2e7d32;">
              <svg viewBox="0 0 24 24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0012.04 2z"/></svg>
            </div>
            <h3 class="branch-name">{'دعم الواتساب الفوري' if not is_en else 'Instant WhatsApp Help'}</h3>
            <p style="font-size: 1.1rem; font-weight: 800; color: #2e7d32; margin: 10px 0;">+966 55 489 0900</p>
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
                <option value="camera">{'عطل في كاميرات المراقبة أو جهاز التسجيل' if not is_en else 'CCTV / DVR technical fault'}</option>
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
                  <option value="cctv_eng">{'مهندس أنظمة مراقبة وأمن' if not is_en else 'CCTV & Security Engineer'}</option>
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
                    f'<h2 class="product-specs-title">{"المواصفات الفنية" if not is_en else "Technical Specifications"}</h2>'
                    f'<dl class="spec-list">'
                    + "".join(f'<div class="spec-row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in spec_rows)
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
                      <ul style="font-size: 0.9rem; color: var(--text-body); line-height: 1.8;">
                        <li>✓ {'مطابق لاشتراطات البنك المركزي والجهات الأمنية' if not is_en else 'Compliant with security & banking regulations'}</li>
                        <li>✓ {'ضمان شامل وقطع غيار أصلية متوفرة' if not is_en else 'Comprehensive warranty & genuine spare parts'}</li>
                        <li>✓ {'تركيب وتدريب فني معتمد من قبل مهندسينا' if not is_en else 'Professional installation & technical support'}</li>
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
    # (slug, ar, en, key, banner_img | None, banner_alt_ar, banner_alt_en)
    cats = [
        ("الخزائن-والأبواب-الأمنية", "الخزائن والأبواب الأمنية", "Safes and Security Doors", "safes",
         "banner-safes.jpg", "خزائن وأبواب أمنية من أحلام الجزيرة", "Aljazeera Dreams safes and vault doors"),
        ("أنظمة-المراقبة-والأمن", "أنظمة المراقبة والأمن", "Surveillance and Security Systems", "surveillance",
         "banner-cctv.jpg", "أنظمة مراقبة وأمن من أحلام الجزيرة", "Aljazeera Dreams surveillance and security systems"),
        ("الأقفال-الأمنية", "الأقفال الأمنية", "Security Locks", "locks", None, "", ""),
    ]

    for slug, title_ar, title_en, cat_key, banner_img, alt_ar, alt_en in cats:
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

            body = f"""
            <section class="section" style="padding-top: 50px;">
              <div class="container">
                <div class="section-header">
                  <span class="section-tag">{'تصنيف المنتجات' if not is_en else 'Product Category'}</span>
                  <h1 class="section-title">{title}</h1>
                  <p class="section-subtitle">{'تصفح أفضل منتجاتنا وحلولنا في هذا التصنيف' if not is_en else 'Browse our specialized product range in this category'}</p>
                </div>{banner}

                <div class="catalog-controls">
                  <div class="filter-tabs">
                    <button class="filter-tab active" data-category="{cat_key}">{title}</button>
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
                depth=depth
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
                 ("نلتزم في شركة أحلام الجزيرة للمقاولات والصيانة بحماية خصوصية بيانات عملائنا وزوّار موقعنا، وفق الأنظمة المعمول بها في المملكة العربية السعودية.",
                  "Aljazeera Dreams Contracting & Maintenance is committed to protecting the privacy of our clients and website visitors, in line with the regulations in force in Saudi Arabia.")),
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
                 ("تخضع الخزائن والأبواب والأقفال وأنظمة المراقبة لضمان الوكيل المعتمد، ووفق اتفاقيات مستوى الخدمة (SLA) المبرمة مع العميل.",
                  "Safes, doors, locks, and surveillance systems are covered by the authorized manufacturer warranty and by the Service Level Agreement (SLA) signed with the client.")),
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


def main():
    print("Building all Arabic and English pages...")
    build_homepage(is_en=False)
    build_homepage(is_en=True)
    
    build_products_page(is_en=False)
    build_products_page(is_en=True)
    
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

    print("All pages built successfully!")

if __name__ == "__main__":
    main()
