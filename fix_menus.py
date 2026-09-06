#!/usr/bin/env python3
"""
Fix all menu links, translations, and interactive dropdown behavior across all HTML pages.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT_DIR = Path("/Users/macbook-pro/Desktop/Development/jazdrm.com/jazdrm.com")

def fix_html_page(html_path):
    rel_path = html_path.relative_to(ROOT_DIR)
    is_en = str(rel_path).startswith("en/") or str(rel_path) == "en"
    
    current_dir = html_path.parent
    
    def get_rel(target_rel_to_root):
        target_abs = ROOT_DIR / target_rel_to_root
        return os.path.relpath(target_abs, current_dir)

    home_link = get_rel("en/index.html") if is_en else get_rel("index.html")
    services_link = f"{home_link}#servicess"
    partners_link = f"{home_link}#our-partners"
    products_link = get_rel("en/products/index.html") if is_en else get_rel("products/index.html")
    about_link = get_rel("en/about-us/index.html") if is_en else get_rel("about-us/index.html")
    contact_link = get_rel("en/contact-us/index.html") if is_en else get_rel("contact-us/index.html")
    service_req_link = get_rel("en/service-request/index.html") if is_en else get_rel("service-request/index.html")
    tech_support_link = get_rel("en/technical-support/index.html") if is_en else get_rel("technical-support/index.html")
    job_app_link = get_rel("en/job-application/index.html") if is_en else get_rel("job-application/index.html")
    
    prefix = "en/" if is_en else ""
    safes_cat = get_rel(f"{prefix}product-category/الخزائن-والأبواب-الأمنية/index.html")
    safes_deposit_cat = get_rel(f"{prefix}product-category/الخزائن-والأبواب-الأمنية/safe-lockers/index.html")
    safes_fireproof_cat = get_rel(f"{prefix}product-tag/خزنات-مقاومة-للحريق/index.html")
    surveillance_cat = get_rel(f"{prefix}product-category/أنظمة-المراقبة-والأمن/index.html")
    locks_cat = get_rel(f"{prefix}product-category/الأقفال-الأمنية/index.html")
    
    content = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Update Header Menu 3
    nav3 = soup.find("nav", id="header-menu-3")
    if nav3:
        for a in nav3.find_all("a"):
            txt = a.get_text().strip()
            if "طلب" in txt or "Request" in txt or "service-request" in a.get("href", ""):
                a["href"] = service_req_link
            elif "الدعم" in txt or "support" in txt or "technical-support" in a.get("href", ""):
                a["href"] = tech_support_link
            elif "التوظيف" in txt or "Recruitment" in txt or "job" in a.get("href", ""):
                a["href"] = job_app_link

    # 2. Update Header Menu 1 & Mobile Menu
    for nav in soup.find_all("nav"):
        nav_id = nav.get("id", "")
        nav_classes = nav.get("class", [])
        if nav_id == "header-menu-1" or "mobile-menu" in nav_classes:
            for a in nav.find_all("a"):
                txt = a.get_text().strip()
                href = a.get("href", "")
                
                if "الرئيسية" in txt or "The main" in txt or txt == "Home":
                    a["href"] = home_link
                elif "خدماتنا" in txt or "Our services" in txt or href.endswith("#servicess"):
                    a["href"] = services_link
                elif "منتجاتنا" in txt or "Our products" in txt or href.endswith("#productss") or "products" in href:
                    a["href"] = products_link
                elif "عملاؤنا" in txt or "Our clients" in txt or href.endswith("#our-partners"):
                    a["href"] = partners_link
                elif "نبذة" in txt or "About us" in txt or "about-us" in href:
                    a["href"] = about_link
                elif "اتصل" in txt or "Contact us" in txt or "contact-us" in href:
                    a["href"] = contact_link
                # Submenu items under Services
                elif "الصراف" in txt or "cashier" in txt:
                    a["href"] = services_link
                elif "صيانة" in txt or "maintenance" in txt:
                    a["href"] = services_link
                elif "تركيب" in txt or "installation" in txt:
                    a["href"] = services_link
                elif "مراقبة" in txt or "Control systems" in txt:
                    a["href"] = services_link

    # 3. Update Header Menu 2 (Categories Dropdown Menu)
    nav2 = soup.find("nav", id="header-menu-2")
    if nav2:
        for a in nav2.find_all("a"):
            txt = a.get_text().strip()
            # Category 1: Safes
            if "الخزائن" in txt or "Safes" in txt:
                a["href"] = safes_cat
            elif "المحصنة" in txt or "Fortified" in txt:
                a["href"] = safes_cat
            elif "الحريق" in txt or "Fireproof" in txt:
                a["href"] = safes_fireproof_cat
            elif "الإيداع" in txt or "Deposit" in txt:
                a["href"] = safes_deposit_cat
            elif "الملفات" in txt or "file" in txt:
                a["href"] = safes_cat
            elif "العرافين" in txt or "Clairvoyant" in txt:
                a["href"] = safes_cat
            
            # Category 2: Surveillance & Security Systems
            elif "المراقبة" in txt or "Surveillance and security" in txt:
                a["href"] = surveillance_cat
            elif "Hikvision" in txt or "كاميرات" in txt or "cameras" in txt:
                a["href"] = surveillance_cat
            elif "DVR" in txt or "تسجيل" in txt or "recording" in txt:
                a["href"] = surveillance_cat
            elif "شاشات" in txt or "Monitor" in txt or "screens" in txt:
                a["href"] = surveillance_cat
            elif "الإنتركوم" in txt or "Intercom" in txt:
                a["href"] = surveillance_cat
            elif "الحضور" in txt or "Attendance" in txt:
                a["href"] = surveillance_cat
            
            # Category 3: Security Locks
            elif "الأقفال" in txt or "Security locks" in txt:
                a["href"] = locks_cat
            elif "رقمية" in txt or "Digital locks" in txt:
                a["href"] = locks_cat
            elif "بصمة" in txt or "Fingerprint" in txt:
                a["href"] = locks_cat
            elif "الوجه" in txt or "face" in txt:
                a["href"] = locks_cat
            elif "الدائرية" in txt or "Circular" in txt or "disc" in txt:
                a["href"] = locks_cat

    # 4. Inject Menu Interactive Helper CSS & JS into <head> or <body>
    menu_fix_id = "jaz-menu-interaction-fix"
    existing_fix = soup.find(id=menu_fix_id)
    if not existing_fix:
        style_tag = soup.new_tag("style", id=menu_fix_id)
        style_tag.string = """
/* Ensure dropdown menus display cleanly on hover and focus */
.menu-item-has-children {
    position: relative !important;
}
.menu-item-has-children:hover > .sub-menu,
.menu-item-has-children:focus-within > .sub-menu,
.menu-item-has-children.active > .sub-menu {
    opacity: 1 !important;
    visibility: visible !important;
    transform: translateY(0) !important;
    pointer-events: auto !important;
    display: block !important;
}
.sub-menu {
    transition: opacity 0.2s ease, transform 0.2s ease, visibility 0.2s ease !important;
    z-index: 9999 !important;
}
.sub-menu a {
    display: block !important;
    cursor: pointer !important;
}
.sub-menu a:hover {
    color: #00897b !important;
}
"""
        if soup.head:
            soup.head.append(style_tag)
            
        script_tag = soup.new_tag("script")
        script_tag.string = """
document.addEventListener('DOMContentLoaded', function() {
    // Mobile Drawer Toggle
    document.querySelectorAll('[data-toggle="drawer"], .ct-header-trigger, [aria-label*="menu"], [aria-label*="Menu"]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            var drawer = document.querySelector('.ct-drawer-canvas, #offcanvas, .mobile-menu-drawer');
            if (drawer) {
                drawer.classList.toggle('active');
                if (drawer.hasAttribute('hidden')) drawer.removeAttribute('hidden');
            }
            document.body.classList.toggle('drawer-active');
        });
    });

    // Dropdown Toggles for touch & click devices
    document.querySelectorAll('.menu-item-has-children > a, .ct-toggle-dropdown-desktop-ghost').forEach(function(item) {
        item.addEventListener('click', function(e) {
            var parent = item.closest('.menu-item-has-children');
            if (parent && window.innerWidth <= 1024) {
                var submenu = parent.querySelector('.sub-menu');
                if (submenu) {
                    parent.classList.toggle('active');
                }
            }
        });
    });
});
"""
        if soup.body:
            soup.body.append(script_tag)

    html_path.write_text(str(soup), encoding="utf-8")

def main():
    print("Applying complete menu link and interactivity fixes across all HTML files...")
    count = 0
    for root, _, files in os.walk(ROOT_DIR):
        for f in files:
            if f.endswith(".html"):
                p = Path(root) / f
                fix_html_page(p)
                count += 1
    print(f"Successfully updated menus in {count} HTML files!")

if __name__ == "__main__":
    main()
