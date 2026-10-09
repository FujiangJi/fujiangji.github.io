'use strict';

(() => {
  const anchor = document.querySelector('.desktop-nav-anchor');
  if (!anchor) return;

  const desktop = window.matchMedia('(min-width: 1024px)');
  const tools = anchor.querySelector('.navbar-tools');
  const themeButton = document.querySelector('.theme-toggle-btn');
  let themeHome;
  let scheduled = false;

  // Move the existing button so its theme listener and mobile placement are retained.
  if (themeButton && !themeButton.hasAttribute('data-desktop-only')) {
    themeHome = document.createComment('Mobile theme toggle position');
    themeButton.before(themeHome);
  }

  function updateThemePlacement() {
    if (!themeHome || !tools) return;
    if (desktop.matches) tools.append(themeButton);
    else themeHome.after(themeButton);
  }

  // CSS handles pinning; this class only changes the floating bar's appearance.
  function updateAppearance() {
    anchor.classList.toggle('is-stuck', desktop.matches && anchor.getBoundingClientRect().top <= 1);
  }

  function scheduleUpdate() {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(() => {
      scheduled = false;
      updateAppearance();
    });
  }

  window.addEventListener('scroll', scheduleUpdate, { passive: true });
  window.addEventListener('resize', scheduleUpdate);
  desktop.addEventListener('change', () => {
    updateThemePlacement();
    scheduleUpdate();
  });
  updateThemePlacement();
  updateAppearance();
})();
