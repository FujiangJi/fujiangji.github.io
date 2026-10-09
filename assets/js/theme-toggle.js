'use strict';

(function () {
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  let preference = readPreference();

  function readPreference() {
    try {
      const saved = localStorage.getItem('theme');
      return saved === 'light' || saved === 'dark' ? saved : null;
    } catch {
      return null;
    }
  }

  function applyTheme() {
    const root = document.documentElement;
    const next = preference || (systemTheme.matches ? 'dark' : 'light');
    const previous = root.getAttribute('data-theme');
    root.setAttribute('data-theme', next);
    if (previous !== next) {
      window.dispatchEvent(new CustomEvent('site-theme-change', { detail: { theme: next } }));
    }
  }

  // Run from the document head so the first paint uses the visitor's theme.
  applyTheme();

  systemTheme.addEventListener('change', function () {
    if (!preference) applyTheme();
  });

  // Keep open pages in sync when a visitor changes or clears their preference.
  window.addEventListener('storage', function (event) {
    if (event.key !== 'theme' && event.key !== null) return;
    preference = readPreference();
    applyTheme();
  });

  document.addEventListener('DOMContentLoaded', function () {
    const btn = document.querySelector('.theme-toggle-btn');
    if (!btn) return;

    btn.addEventListener('click', function () {
      const current = document.documentElement.getAttribute('data-theme');
      preference = current === 'light' ? 'dark' : 'light';
      try {
        localStorage.setItem('theme', preference);
      } catch {
        // The toggle still works for this visit when storage is unavailable.
      }
      applyTheme();
    });
  });
})();
