/**
 * activity — marketing web client script
 *
 * Žiadne dependencies, žiadny build. Vanilla JavaScript.
 * Funkčnosti:
 *   1. Injekcia hlavičky a päty cez fetch (DRY - jeden zdroj v partials/)
 *   2. Mobile menu toggle
 *   3. Highlight aktívnej položky v menu podľa URL
 */

(function () {
  'use strict';

  /**
   * Inject HTML partial into element with given id.
   * @param {string} url - partial URL (e.g. '/partials/header.html')
   * @param {string} targetId - element id to inject into
   * @returns {Promise}
   */
  async function injectPartial(url, targetId) {
    const target = document.getElementById(targetId);
    if (!target) return;
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`Failed to load ${url}`);
      const html = await res.text();
      target.innerHTML = html;
    } catch (err) {
      console.error('Partial injection failed:', err);
      target.innerHTML = `<!-- partial load failed: ${url} -->`;
    }
  }

  /**
   * Highlight active nav link based on current pathname.
   */
  function highlightActiveNav() {
    const path = window.location.pathname.replace(/\/$/, '') || '/index.html';
    const filename = path.substring(path.lastIndexOf('/') + 1) || 'index.html';
    const navLinks = document.querySelectorAll('.site-nav a[data-page]');
    navLinks.forEach((link) => {
      const page = link.getAttribute('data-page');
      // Match: index.html with '/' or 'index.html', otherwise compare filename without .html
      const normalized = filename.replace('.html', '') || 'index';
      if (
        page === normalized ||
        (page === 'index' && (filename === '' || filename === 'index.html'))
      ) {
        link.classList.add('active');
      }
    });
  }

  /**
   * Mobile menu toggle button.
   */
  function setupMobileMenu() {
    const toggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.site-nav');
    if (!toggle || !nav) return;
    toggle.addEventListener('click', () => {
      const isOpen = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(isOpen));
    });
    // Close on link click (mobile)
    nav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /**
   * Initialize after DOM ready.
   */
  async function init() {
    // Inject partials in parallel
    await Promise.all([
      injectPartial('/partials/header.html', 'site-header'),
      injectPartial('/partials/footer.html', 'site-footer'),
    ]);

    // Setup interactivity (after partials are in DOM)
    highlightActiveNav();
    setupMobileMenu();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
