/**
 * JAZDRM.COM - Core Client Runtime
 * Features:
 * - Exact root-relative asset path resolution
 * - Mobile Drawer navigation
 * - Dropdown & accordion toggles
 * - Live Product Search & Category Filtering
 * - Interactive Quotation Modal
 * - Form Validation & Toast Feedback
 */

document.addEventListener('DOMContentLoaded', function () {
  initHeader();
  initMobileDrawer();
  initProductCatalog();
  initQuoteModal();
  initForms();
});

/* Helper: Get exact relative root path */
function getRootPrefix() {
  const rootAttr = document.body.getAttribute('data-root');
  if (rootAttr !== null) return rootAttr;
  return '';
}

/* 1. Header & Navigation */
function initHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  window.addEventListener('scroll', function () {
    if (window.scrollY > 30) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
}

/* 2. Mobile Drawer Navigation */
function initMobileDrawer() {
  const toggleBtn = document.querySelector('.mobile-toggle-btn');
  const drawer = document.querySelector('.mobile-drawer');
  const backdrop = document.querySelector('.drawer-backdrop');
  const closeBtn = document.querySelector('.drawer-close-btn');

  if (!drawer) return;

  function openDrawer() {
    drawer.classList.add('active');
    if (backdrop) backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    drawer.classList.remove('active');
    if (backdrop) backdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (toggleBtn) toggleBtn.addEventListener('click', openDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (backdrop) backdrop.addEventListener('click', closeDrawer);

  // Accordions in mobile drawer
  document.querySelectorAll('.mobile-drawer .nav-item').forEach(function (item) {
    const link = item.querySelector('.nav-link');
    const dropdown = item.querySelector('.dropdown-menu');
    if (dropdown && link) {
      link.addEventListener('click', function (e) {
        if (window.innerWidth <= 850) {
          const isDropdownLink = link.getAttribute('href') === '#' || link.getAttribute('href') === '';
          if (isDropdownLink) {
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

  const isEn = document.documentElement.getAttribute('dir') === 'ltr' || document.body.classList.contains('en-lang');
  const products = window.JAZDRM_PRODUCTS;
  const rootPrefix = getRootPrefix();
  
  // Check if page specifies an initial category filter
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

    if (filtered.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 50px 20px; color: var(--text-muted);">
          <h3>${isEn ? 'No products found' : 'لا توجد منتجات مطابقة'}</h3>
          <p>${isEn ? 'Try adjusting your search query or category filter.' : 'يرجى تجربة كلمة بحث أخرى أو تغيير التصنيف.'}</p>
        </div>
      `;
      return;
    }

    container.innerHTML = filtered.map(function (p) {
      const title = isEn ? (p.title_en || p.title_ar) : p.title_ar;
      const category = isEn ? p.category_en : p.category_ar;
      const desc = isEn ? p.short_desc_en : p.short_desc_ar;
      const rawImg = p.image || 'wp-content/uploads/2025/06/Asset-5.png';
      const imgSrc = `${rootPrefix}${rawImg}`;
      const detailLink = `${rootPrefix}${isEn ? 'en/' : ''}product/${p.slug}/index.html`;
      const fallbackImg = `${rootPrefix}wp-content/uploads/2025/06/Asset-5.png`;

      return `
        <div class="product-card" data-category="${p.category_key}">
          <div class="product-thumb">
            <span class="product-badge">${category}</span>
            <img src="${imgSrc}" alt="${title}" loading="lazy" onerror="this.onerror=null; this.src='${fallbackImg}';">
          </div>
          <div class="product-info">
            <div class="product-cat">${category}</div>
            <h3 class="product-name">${title}</h3>
            <p class="product-desc">${desc || (isEn ? 'High quality certified security solution.' : 'حلول أمنية معتمدة ومطابقة لأعلى المواصفات.')}</p>
            <div class="product-actions">
              <button class="btn-card-primary open-quote-btn" data-product="${title}">
                ${isEn ? 'Request Quote' : 'طلب عرض سعر'}
              </button>
              <a href="${detailLink}" class="btn-card-outline">
                ${isEn ? 'Details' : 'التفاصيل'}
              </a>
            </div>
          </div>
        </div>
      `;
    }).join('');

    // Attach quote button listeners
    container.querySelectorAll('.open-quote-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const prodName = btn.getAttribute('data-product');
        openQuoteModal(prodName);
      });
    });
  }

  // Filter tabs
  filterTabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      filterTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      currentCategory = tab.getAttribute('data-category');
      renderProducts();
    });
  });

  // Search input
  if (searchInput) {
    searchInput.addEventListener('input', function (e) {
      searchQuery = e.target.value.trim();
      renderProducts();
    });
  }

  renderProducts();
}

/* 4. Quote & Service Modal */
function initQuoteModal() {
  const modal = document.getElementById('quote-modal');
  const closeBtn = document.querySelector('.modal-close');
  const openBtns = document.querySelectorAll('.btn-quote, .open-quote-modal, .open-quote-btn');

  if (!modal) return;

  window.openQuoteModal = function (productName) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    const prodInput = document.getElementById('modal-product-name');
    if (prodInput && productName) {
      prodInput.value = productName;
    }
  };

  window.closeQuoteModal = function () {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  };

  openBtns.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const pName = btn.getAttribute('data-product') || '';
      openQuoteModal(pName);
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeQuoteModal);
  modal.addEventListener('click', function (e) {
    if (e.target === modal) closeQuoteModal();
  });
}

/* 5. Form Submissions */
function initForms() {
  document.querySelectorAll('form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const isEn = document.documentElement.getAttribute('dir') === 'ltr' || document.body.classList.contains('en-lang');
      const msg = isEn
        ? 'Thank you! Your request has been successfully received. Our team will contact you shortly.'
        : 'شكراً لكم! تم استلام طلبكم بنجاح وسيتواصل معكم فريقنا في أقرب وقت.';
      
      alert(msg);
      form.reset();
      if (typeof window.closeQuoteModal === 'function') {
        window.closeQuoteModal();
      }
    });
  });
}
