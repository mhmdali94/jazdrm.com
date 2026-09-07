/**
 * JAZDRM.COM - Core Client Runtime
 * Features:
 * - Exact root-relative asset path resolution
 * - Mobile Drawer navigation (keyboard + focus trap)
 * - Dropdown & accordion toggles
 * - Live Product Search & Category Filtering
 * - Interactive Quotation Modal (dialog semantics, Escape, focus return)
 * - Form label association, double-submit guard, accessible toast feedback
 */

document.addEventListener('DOMContentLoaded', function () {
  initA11y();
  initHeader();
  initMobileDrawer();
  initProductCatalog();
  initQuoteModal();
  initForms();
});

/* Helper: exact relative root path */
function getRootPrefix() {
  const rootAttr = document.body.getAttribute('data-root');
  if (rootAttr !== null) return rootAttr;
  return '';
}

function isEnglish() {
  return document.documentElement.getAttribute('dir') === 'ltr' ||
    document.body.classList.contains('en-lang');
}

const FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

function getFocusable(container) {
  return Array.prototype.filter.call(
    container.querySelectorAll(FOCUSABLE),
    function (el) { return el.offsetParent !== null || el === document.activeElement; }
  );
}

/* Keep Tab focus inside an open overlay */
function trapFocus(container, e) {
  if (e.key !== 'Tab') return;
  const focusable = getFocusable(container);
  if (!focusable.length) return;
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (e.shiftKey && document.activeElement === first) {
    e.preventDefault();
    last.focus();
  } else if (!e.shiftKey && document.activeElement === last) {
    e.preventDefault();
    first.focus();
  }
}

function setInert(el, inert) {
  if (!el) return;
  if ('inert' in HTMLElement.prototype) el.inert = inert;
  if (inert) {
    el.setAttribute('aria-hidden', 'true');
  } else {
    el.removeAttribute('aria-hidden');
  }
}

/* 0. Accessibility upgrades that must work even on older pre-built pages */
function initA11y() {
  // Ensure a focus target on <main>
  let main = document.getElementById('main-content');
  if (!main) main = document.querySelector('main');
  if (main) {
    if (!main.id) main.id = 'main-content';
    if (!main.hasAttribute('tabindex')) main.setAttribute('tabindex', '-1');
  }

  // Inject a skip link on legacy pages that were built before it existed
  if (main && !document.querySelector('.skip-link')) {
    const skip = document.createElement('a');
    skip.className = 'skip-link';
    skip.href = '#' + main.id;
    skip.textContent = isEnglish() ? 'Skip to content' : 'تخطي إلى المحتوى';
    document.body.insertBefore(skip, document.body.firstChild);
  }

  // Upgrade any legacy non-button controls (older baked pages used div/span)
  document.querySelectorAll('.mobile-toggle-btn, .drawer-close-btn, .modal-close').forEach(function (el) {
    if (el.tagName === 'BUTTON') return;
    el.setAttribute('role', 'button');
    el.setAttribute('tabindex', '0');
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        el.click();
      }
    });
  });
}

/* 1. Header scroll state */
function initHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  let ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      header.classList.toggle('scrolled', window.scrollY > 30);
      ticking = false;
    });
  }, { passive: true });
}

/* 2. Mobile Drawer Navigation */
function initMobileDrawer() {
  const toggleBtn = document.querySelector('.mobile-toggle-btn');
  const drawer = document.querySelector('.mobile-drawer');
  const backdrop = document.querySelector('.drawer-backdrop');
  const closeBtn = document.querySelector('.drawer-close-btn');

  if (!drawer) return;

  let lastFocused = null;
  setInert(drawer, !drawer.classList.contains('active'));

  function openDrawer() {
    lastFocused = document.activeElement;
    drawer.classList.add('active');
    if (backdrop) backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
    if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'true');
    setInert(drawer, false);
    (closeBtn || getFocusable(drawer)[0] || drawer).focus();
    document.addEventListener('keydown', onKeydown);
  }

  function closeDrawer() {
    drawer.classList.remove('active');
    if (backdrop) backdrop.classList.remove('active');
    document.body.style.overflow = '';
    if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
    setInert(drawer, true);
    document.removeEventListener('keydown', onKeydown);
    if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();
  }

  function onKeydown(e) {
    if (e.key === 'Escape') {
      closeDrawer();
    } else {
      trapFocus(drawer, e);
    }
  }

  if (toggleBtn) toggleBtn.addEventListener('click', function () {
    drawer.classList.contains('active') ? closeDrawer() : openDrawer();
  });
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (backdrop) backdrop.addEventListener('click', closeDrawer);

  // Accordions in mobile drawer
  document.querySelectorAll('.mobile-drawer .nav-item').forEach(function (item) {
    const link = item.querySelector('.nav-link');
    const dropdown = item.querySelector('.dropdown-menu');
    if (dropdown && link) {
      link.addEventListener('click', function (e) {
        if (window.innerWidth <= 850) {
          const href = link.getAttribute('href');
          if (href === '#' || href === '' || href === null) {
            e.preventDefault();
            item.classList.toggle('open');
          }
        }
      });
    }
  });
}

/* 3. Product Catalog Filter & Search */
function initProductCatalog() {
  const container = document.getElementById('products-grid-container');
  if (!container || !window.JAZDRM_PRODUCTS) return;

  const isEn = isEnglish();
  const products = window.JAZDRM_PRODUCTS;
  const rootPrefix = getRootPrefix();

  // On the homepage the grid is a teaser: data-limit caps it and there are no controls.
  const limit = parseInt(container.getAttribute('data-limit'), 10) || 0;

  const initialCategoryTab = document.querySelector('.filter-tab.active');
  let currentCategory = initialCategoryTab ? initialCategoryTab.getAttribute('data-category') || 'all' : 'all';
  let searchQuery = '';

  const searchInput = document.getElementById('product-search-input');
  const filterTabs = document.querySelectorAll('.filter-tab');

  function renderProducts() {
    const filtered = products.filter(function (p) {
      const matchCat = currentCategory === 'all' || p.category_key === currentCategory;
      const title = isEn ? (p.title_en || p.title_ar) : p.title_ar;
      const desc = isEn ? (p.short_desc_en || '') : (p.short_desc_ar || '');
      const matchSearch = !searchQuery ||
        title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        desc.toLowerCase().includes(searchQuery.toLowerCase());
      return matchCat && matchSearch;
    });

    const shown = limit ? filtered.slice(0, limit) : filtered;

    if (shown.length === 0) {
      container.innerHTML = `
        <div role="status" style="grid-column: 1 / -1; text-align: center; padding: 50px 20px; color: var(--text-muted);">
          <h3>${isEn ? 'No products found' : 'لا توجد منتجات مطابقة'}</h3>
          <p>${isEn ? 'Try adjusting your search query or category filter.' : 'يرجى تجربة كلمة بحث أخرى أو تغيير التصنيف.'}</p>
        </div>
      `;
      return;
    }

    container.innerHTML = shown.map(function (p) {
      const title = isEn ? (p.title_en || p.title_ar) : p.title_ar;
      const category = isEn ? p.category_en : p.category_ar;
      const rawImg = p.image || 'wp-content/uploads/2025/06/Asset-5.png';
      const imgSrc = `${rootPrefix}${rawImg}`;
      const detailLink = `${rootPrefix}${isEn ? 'en/' : ''}product/${p.slug}/index.html`;
      const fallbackImg = `${rootPrefix}wp-content/uploads/2025/06/Asset-5.png`;
      const quoteLabel = isEn ? 'Request a quote' : 'طلب عرض سعر';
      const detailsLabel = isEn ? 'Details' : 'التفاصيل';

      return `
        <div class="product-card" data-category="${p.category_key}">
          <a class="product-thumb" href="${detailLink}" aria-label="${title}">
            <span class="product-badge">${category}</span>
            <img src="${imgSrc}" alt="${title}" loading="lazy" width="270" height="240" onerror="this.onerror=null; this.src='${fallbackImg}';">
          </a>
          <div class="product-info">
            <div class="product-cat">${category}</div>
            <h3 class="product-name"><a href="${detailLink}">${title}</a></h3>
            <div class="product-actions">
              <button type="button" class="btn-card-primary open-quote-btn" data-product="${title}" aria-label="${quoteLabel}: ${title}">
                ${isEn ? 'Request Quote' : 'طلب عرض سعر'}
              </button>
              <a href="${detailLink}" class="btn-card-outline">${detailsLabel}</a>
            </div>
          </div>
        </div>
      `;
    }).join('');

    container.querySelectorAll('.open-quote-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        openQuoteModal(btn.getAttribute('data-product'));
      });
    });
  }

  filterTabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      filterTabs.forEach(function (t) {
        t.classList.remove('active');
        t.setAttribute('aria-pressed', 'false');
      });
      tab.classList.add('active');
      tab.setAttribute('aria-pressed', 'true');
      currentCategory = tab.getAttribute('data-category');
      renderProducts();
    });
  });

  if (searchInput) {
    let debounce;
    searchInput.addEventListener('input', function (e) {
      clearTimeout(debounce);
      const value = e.target.value.trim();
      debounce = setTimeout(function () {
        searchQuery = value;
        renderProducts();
      }, 200);
    });
  }

  renderProducts();
}

/* 4. Quote & Service Modal */
function initQuoteModal() {
  const modal = document.getElementById('quote-modal');
  if (!modal) return;

  const dialog = modal.querySelector('.modal-content') || modal;
  const closeBtn = modal.querySelector('.modal-close');
  const openBtns = document.querySelectorAll('.btn-quote, .open-quote-modal, .open-quote-btn');

  // Ensure dialog semantics even on older baked pages
  if (!dialog.getAttribute('role')) dialog.setAttribute('role', 'dialog');
  dialog.setAttribute('aria-modal', 'true');
  if (!dialog.hasAttribute('tabindex')) dialog.setAttribute('tabindex', '-1');
  const title = modal.querySelector('.modal-title');
  if (title) {
    if (!title.id) title.id = 'quote-modal-title';
    dialog.setAttribute('aria-labelledby', title.id);
  }

  let lastFocused = null;
  setInert(modal, !modal.classList.contains('active'));

  window.openQuoteModal = function (productName) {
    lastFocused = document.activeElement;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    setInert(modal, false);
    const prodInput = document.getElementById('modal-product-name');
    if (prodInput && productName) prodInput.value = productName;
    document.addEventListener('keydown', onKeydown);
    window.requestAnimationFrame(function () {
      const firstField = getFocusable(dialog).find(function (el) {
        return !el.classList.contains('modal-close');
      });
      (firstField || closeBtn || dialog).focus();
    });
  };

  window.closeQuoteModal = function () {
    modal.classList.remove('active');
    document.body.style.overflow = '';
    setInert(modal, true);
    document.removeEventListener('keydown', onKeydown);
    if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();
  };

  function onKeydown(e) {
    if (e.key === 'Escape') {
      closeQuoteModal();
    } else {
      trapFocus(dialog, e);
    }
  }

  openBtns.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      openQuoteModal(btn.getAttribute('data-product') || '');
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeQuoteModal);
  modal.addEventListener('click', function (e) {
    if (e.target === modal) closeQuoteModal();
  });
}

/* 5. Forms: label association, validation, no double submit, toast feedback */
function initForms() {
  document.querySelectorAll('.form-group').forEach(function (group, i) {
    const label = group.querySelector('.form-label');
    const field = group.querySelector('.form-control, input, select, textarea');
    if (!label || !field) return;
    if (!field.id) field.id = 'field-' + i + '-' + Math.random().toString(36).slice(2, 7);
    if (!label.getAttribute('for')) label.setAttribute('for', field.id);
    if (field.hasAttribute('required')) {
      field.setAttribute('aria-required', 'true');
    }
  });

  document.querySelectorAll('form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const invalid = form.querySelector(':invalid');
      if (invalid) {
        invalid.focus();
        return;
      }

      const submitBtn = form.querySelector('[type="submit"]');
      if (submitBtn) {
        if (submitBtn.disabled) return;
        submitBtn.disabled = true;
        submitBtn.dataset.label = submitBtn.textContent.trim();
        submitBtn.textContent = isEnglish() ? 'Sending...' : 'جارٍ الإرسال...';
      }

      // No backend on this static build: simulate acceptance
      window.setTimeout(function () {
        showToast(isEnglish()
          ? 'Thank you. Your request has been received; our team will contact you shortly.'
          : 'شكراً لكم. تم استلام طلبكم وسيتواصل معكم فريقنا في أقرب وقت.');
        form.reset();
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = submitBtn.dataset.label || submitBtn.textContent;
        }
        if (typeof window.closeQuoteModal === 'function' && form.closest('#quote-modal')) {
          window.closeQuoteModal();
        }
      }, 600);
    });
  });
}

/* Accessible toast (replaces alert) */
function showToast(message) {
  let region = document.querySelector('.toast-region');
  if (!region) {
    region = document.createElement('div');
    region.className = 'toast-region';
    region.setAttribute('role', 'status');
    region.setAttribute('aria-live', 'polite');
    document.body.appendChild(region);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>' +
    '<span></span>';
  toast.querySelector('span').textContent = message;
  region.appendChild(toast);

  window.requestAnimationFrame(function () {
    toast.classList.add('is-visible');
  });

  window.setTimeout(function () {
    toast.classList.remove('is-visible');
    window.setTimeout(function () { toast.remove(); }, 400);
  }, 6000);
}
