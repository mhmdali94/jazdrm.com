#!/usr/bin/env python3
"""
Comprehensive Website Builder for jazdrm.com
Generates all Arabic and English pages with the exact brand colors, modern architecture,
complete product catalog, and interactive forms.
"""

import os
import json
from pathlib import Path

ROOT_DIR = Path("/Users/macbook-pro/Desktop/Development/jazdrm.com/jazdrm.com")

with open(ROOT_DIR / "assets" / "data" / "products.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

def get_header(is_en=False, depth=0):
    rel = "../" * depth
    lang_toggle_url = f"{rel}en/index.html" if not is_en else f"{rel}index.html"
    lang_label = "EN" if not is_en else "العربية"
    lang_target = "English" if not is_en else "العربية"

    t = {
        "phone": "920028440",
        "phone_display": "920028440",
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
          <img src="{rel}wp-content/uploads/2025/06/Asset-5.png" alt="{t['brand_title']}">
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
        <img src="{rel}wp-content/uploads/2025/06/Asset-5.png" alt="{t['brand_title']}" style="height: 38px;">
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
      <div style="margin-top: 15px;">
        <a href="{lang_toggle_url}" class="btn-primary" style="width: 100%; justify-content: center;">
          <span>{lang_target}</span>
        </a>
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
        "about_p": "شركة أحلام الجزيرة للمقاولات والصيانة - رواد تزويد وتركيب الخزائن والأبواب الأمنية المحصنة، وأنظمة المراقبة والتحكم، والأقفال الذكية لكبرى البنوك والشركات والمؤسسات في المملكة." if not is_en else "Aljazeera Dreams Contracting & Security - Pioneers in security safes, bunker vault doors, surveillance, and smart locks for major banks and corporations across Saudi Arabia.",
        "nav_title": "روابط سريعة" if not is_en else "Quick Links",
        "cats_title": "التصنيفات" if not is_en else "Categories",
        "contact_title": "تواصل معنا" if not is_en else "Contact Us",
        "address": "الرياض (الفرع الرئيسي) - حي الروابي، شارع طاهر الدباغ" if not is_en else "Riyadh (Main HQ) - Al-Rawabi, Taher Al-Dabbagh St.",
        "branches": "فروعنا: الرياض، جدة، المدينة المنورة، تبوك، بريدة، الطائف" if not is_en else "Branches: Riyadh, Jeddah, Medina, Tabuk, Buraydah, Taif",
        "copyright": "جميع الحقوق محفوظة © 2026 - شركة أحلام الجزيرة للمقاولات والصيانة" if not is_en else "All Rights Reserved © 2026 - Aljazeera Dreams Co.",
        "privacy": "سياسة الخصوصية" if not is_en else "Privacy Policy",
        "terms": "الشروط والأحكام" if not is_en else "Terms & Conditions",
    }

    return f"""
  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-about">
          <div class="brand-logo" style="margin-bottom: 12px;">
            <img src="{rel}wp-content/uploads/2025/06/Asset-5.png" alt="أحلام الجزيرة" style="height: 48px;">
            <span class="brand-title" style="color: #fff; font-size: 1.2rem;">{'أحلام الجزيرة' if not is_en else 'Aljazeera Dreams'}</span>
          </div>
          <p>{t['about_p']}</p>
        </div>
        <div>
          <h4 class="footer-title">{t['nav_title']}</h4>
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
          <h4 class="footer-title">{t['cats_title']}</h4>
          <div class="footer-links">
            <a href="{safes_url}">{'الخزائن والأبواب الأمنية' if not is_en else 'Safes & Vault Doors'}</a>
            <a href="{surveillance_url}">{'أنظمة المراقبة والأمن' if not is_en else 'Surveillance Systems'}</a>
            <a href="{locks_url}">{'الأقفال الأمنية الذكية' if not is_en else 'Security Locks'}</a>
            <a href="{safes_url}">{'خزائن الإيداع والغرف المحصنة' if not is_en else 'Deposit & Vault Lockers'}</a>
          </div>
        </div>
        <div>
          <h4 class="footer-title">{t['contact_title']}</h4>
          <div class="footer-links">
            <p style="color: rgba(255,255,255,0.7); font-size: 0.88rem; margin-bottom: 8px;">{t['address']}</p>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.88rem; margin-bottom: 12px;">{t['branches']}</p>
            <a href="tel:+966920028440" style="color: var(--accent-cyan); font-weight: 700; font-size: 1.1rem;">920028440</a>
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
    <a href="https://wa.me/966554890900" target="_blank" class="floating-btn floating-whatsapp" title="WhatsApp">
      <svg viewBox="0 0 24 24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0012.04 2z"/></svg>
    </a>
    <a href="tel:+966920028440" class="floating-btn floating-phone" title="Call Us">
      <svg viewBox="0 0 24 24"><path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24 11.72 11.72 0 003.68.59 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1 11.72 11.72 0 00.59 3.68 1 1 0 01-.24 1.02l-2.23 2.09z"/></svg>
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
"""

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
  <meta name="description" content="{'شركة أحلام الجزيرة للمقاولات والصيانة - حلول الخزائن والأبواب الأمنية، أنظمة المراقبة، والأقفال الذكية' if not is_en else 'Aljazeera Dreams - Premium security safes, vault doors, CCTV surveillance, and biometric locks in Saudi Arabia'}">
  <link rel="icon" href="{rel}wp-content/uploads/2025/06/cropped-favicon-32x32.png" sizes="32x32">
  <link rel="icon" href="{rel}wp-content/uploads/2025/06/cropped-favicon-192x192.png" sizes="192x192">
  <link rel="apple-touch-icon" href="{rel}wp-content/uploads/2025/06/cropped-favicon-180x180.png">
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
        "prod_tag": "معرض المنتجات" if not is_en else "Product Showcase",
        "prod_h2": "تصفح أحدث الخزائن وأنظمة الأمان" if not is_en else "Explore Our High-Security Product Lines",
        "tab_all": "جميع المنتجات" if not is_en else "All Products",
        "tab_safes": "الخزائن والأبواب" if not is_en else "Safes & Doors",
        "tab_surv": "المراقبة والكاميرات" if not is_en else "Surveillance & CCTV",
        "tab_locks": "الأقفال الذكية" if not is_en else "Smart Locks",
        "search_ph": "ابحث عن موديل أو منتج..." if not is_en else "Search model or product name...",
        "partners_tag": "شركاء النجاح" if not is_en else "Partners of Success",
        "partners_h2": "العلامات التجارية المعتمدة عالمياً" if not is_en else "Globally Authorized Brands",
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
            <img src="{rel}wp-content/uploads/2025/06/IMG_0055_0171-500x500.webp" alt="SSM 130 Vault Door">
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

    <!-- Services Section -->
    <section class="section" id="services">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">{t['srv_tag']}</span>
          <h2 class="section-title">{t['srv_h2']}</h2>
        </div>
        <div class="services-grid">
          <div class="service-card">
            <div class="service-icon-box">
              <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zM7 10h2v7H7zm4-3h2v10h-2zm4 6h2v4h-2z"/></svg>
            </div>
            <h3 class="service-title">{t['srv1_title']}</h3>
            <p class="service-desc">{t['srv1_desc']}</p>
            <button class="service-link open-quote-modal" style="cursor: pointer;">
              <span>{t['quote_btn']}</span>
              <svg width="12" height="12" viewBox="0 0 10 6"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>
            </button>
          </div>
          <div class="service-card">
            <div class="service-icon-box">
              <svg viewBox="0 0 24 24"><path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/></svg>
            </div>
            <h3 class="service-title">{t['srv2_title']}</h3>
            <p class="service-desc">{t['srv2_desc']}</p>
            <button class="service-link open-quote-modal" style="cursor: pointer;">
              <span>{t['quote_btn']}</span>
              <svg width="12" height="12" viewBox="0 0 10 6"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>
            </button>
          </div>
          <div class="service-card">
            <div class="service-icon-box">
              <svg viewBox="0 0 24 24"><path d="M20 8h-3V4H3c-1.1 0-2 .9-2 2v11h2c0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h2v-5l-3-4zM6 18.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm13.5-9l1.96 2.5H17V9.5h2.5zm-1.5 9c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>
            </div>
            <h3 class="service-title">{t['srv3_title']}</h3>
            <p class="service-desc">{t['srv3_desc']}</p>
            <button class="service-link open-quote-modal" style="cursor: pointer;">
              <span>{t['quote_btn']}</span>
              <svg width="12" height="12" viewBox="0 0 10 6"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>
            </button>
          </div>
          <div class="service-card">
            <div class="service-icon-box">
              <svg viewBox="0 0 24 24"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
            </div>
            <h3 class="service-title">{t['srv4_title']}</h3>
            <p class="service-desc">{t['srv4_desc']}</p>
            <button class="service-link open-quote-modal" style="cursor: pointer;">
              <span>{t['quote_btn']}</span>
              <svg width="12" height="12" viewBox="0 0 10 6"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Product Showcase Catalog Section -->
    <section class="section" style="background: var(--bg-surface);" id="products">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">{t['prod_tag']}</span>
          <h2 class="section-title">{t['prod_h2']}</h2>
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

    <!-- Brands & Partners -->
    <section class="brands-section" id="partners">
      <div class="container">
        <div class="section-header" style="margin-bottom: 30px;">
          <span class="section-tag">{t['partners_tag']}</span>
          <h2 class="section-title" style="font-size: 1.75rem;">{t['partners_h2']}</h2>
        </div>
        <div class="brands-grid">
          <div class="brand-item">FALCON SAFES</div>
          <div class="brand-item">DIPLOMAT</div>
          <div class="brand-item">JIABAO SECURITY</div>
          <div class="brand-item">SUNPOWER</div>
          <div class="brand-item">HIKVISION</div>
          <div class="brand-item">DAHUA TECHNOLOGY</div>
        </div>
      </div>
    </section>

    <!-- Branches Directory -->
    <section class="section" style="background: var(--bg-page);">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">{t['branches_tag']}</span>
          <h2 class="section-title">{t['branches_h2']}</h2>
        </div>
        <div class="branches-grid">
          <div class="branch-card">
            <h4 class="branch-name">{'الرياض (الفرع الرئيسي)' if not is_en else 'Riyadh (Main HQ)'}</h4>
            <p class="branch-status">{'حي الروابي - شارع طاهر الدباغ' if not is_en else 'Al-Rawabi District'}</p>
          </div>
          <div class="branch-card">
            <h4 class="branch-name">{'جدة' if not is_en else 'Jeddah'}</h4>
            <p class="branch-status">{'المنطقة الغربية' if not is_en else 'Western Region'}</p>
          </div>
          <div class="branch-card">
            <h4 class="branch-name">{'المدينة المنورة' if not is_en else 'Medina'}</h4>
            <p class="branch-status">{'فرع المدينة' if not is_en else 'Medina Branch'}</p>
          </div>
          <div class="branch-card">
            <h4 class="branch-name">{'تبوك' if not is_en else 'Tabuk'}</h4>
            <p class="branch-status">{'المنطقة الشمالية' if not is_en else 'Northern Region'}</p>
          </div>
          <div class="branch-card">
            <h4 class="branch-name">{'بريدة (القصيم)' if not is_en else 'Buraydah (Qassim)'}</h4>
            <p class="branch-status">{'منطقة القصيم' if not is_en else 'Qassim Region'}</p>
          </div>
          <div class="branch-card">
            <h4 class="branch-name">{'الطائف' if not is_en else 'Taif'}</h4>
            <p class="branch-status">{'فرع الطائف' if not is_en else 'Taif Branch'}</p>
          </div>
        </div>
      </div>
    </section>
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
        "h1": "شركة أحلام الجزيرة للمقاولات والصيانة" if not is_en else "Aljazeera Dreams Contracting & Security",
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
      </div>
    </section>
    """

    html = generate_base_html(
        title="اتصل بنا" if not is_en else "Contact Us",
        body_content=body,
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
        body_content=body,
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
            <p style="font-size: 1.3rem; font-weight: 800; color: var(--primary); margin: 10px 0;">920028440</p>
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
        body_content=body,
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
        body_content=body,
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
            desc = p["short_desc_en"] if is_en else p["short_desc_ar"]
            img = f"{rel}{p['image']}" if p["image"] else f"{rel}wp-content/uploads/2025/06/Asset-5.png"

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
                    <img src="{img}" alt="{title}" onerror="this.onerror=null; this.src='{rel}wp-content/uploads/2025/06/Asset-5.png';" style="max-height: 420px; margin: 0 auto; object-fit: contain;">
                  </div>
                  <div>
                    <span class="product-badge" style="position: static; display: inline-block; margin-bottom: 12px;">{cat}</span>
                    <h1 style="font-size: 2rem; font-weight: 800; color: var(--text-main); margin-bottom: 15px; line-height: 1.3;">{title}</h1>
                    <p style="color: var(--text-muted); font-size: 1rem; line-height: 1.8; margin-bottom: 25px;">
                      {desc or ('حل أمني متطور من شركة أحلام الجزيرة مصمم وفق أعلى معايير الجودة والمواصفات المعتمدة.' if not is_en else 'High security solution engineered to international standards by Aljazeera Dreams.')}
                    </p>

                    <div style="background: var(--primary-tint); border: 1px solid var(--primary-light); padding: 20px; border-radius: var(--radius-md); margin-bottom: 30px;">
                      <h4 style="font-size: 1rem; font-weight: 700; color: var(--primary-dark); margin-bottom: 10px;">{'المواصفات والضمان' if not is_en else 'Specifications & Warranty'}</h4>
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
    cats = [
        ("الخزائن-والأبواب-الأمنية", "الخزائن والأبواب الأمنية", "Safes and Security Doors", "safes"),
        ("أنظمة-المراقبة-والأمن", "أنظمة المراقبة والأمن", "Surveillance and Security Systems", "surveillance"),
        ("الأقفال-الأمنية", "الأقفال الأمنية", "Security Locks", "locks"),
    ]

    for slug, title_ar, title_en, cat_key in cats:
        for is_en in [False, True]:
            rel = "../../../" if is_en else "../../"
            depth = 3 if is_en else 2
            title = title_en if is_en else title_ar

            body = f"""
            <section class="section" style="padding-top: 50px;">
              <div class="container">
                <div class="section-header">
                  <span class="section-tag">{'تصنيف المنتجات' if not is_en else 'Product Category'}</span>
                  <h1 class="section-title">{title}</h1>
                  <p class="section-subtitle">{'تصفح أفضل منتجاتنا وحلولنا في هذا التصنيف' if not is_en else 'Browse our specialized product range in this category'}</p>
                </div>

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
    
    print("All pages built successfully!")

if __name__ == "__main__":
    main()
