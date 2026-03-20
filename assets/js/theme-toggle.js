'use strict';

(function () {
  const saved = localStorage.getItem('theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
  }

  document.addEventListener('DOMContentLoaded', function () {
    const btn = document.querySelector('.theme-toggle-btn');
    if (!btn) return;

    btn.addEventListener('click', function () {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      if (document.getElementById('clustrmaps-wrap')) {
        location.reload();
      }
    });
  });
})();
