'use strict';

(() => {
  const anchor = document.querySelector('.desktop-nav-anchor');
  if (!anchor) return;

  const desktop = window.matchMedia('(min-width: 1024px)');
  const tools = anchor.querySelector('.navbar-tools');
  const themeButton = document.querySelector('.theme-toggle-btn');
  const sidebar = document.querySelector('[data-sidebar]');
  const contactButton = sidebar?.querySelector('[data-sidebar-btn]');
  const contacts = sidebar?.querySelector('.sidebar-info_more');
  let themeHome;
  let contactHome;
  let mobileToolbar;
  let mobileTools;
  let scheduled = false;

  // Move the existing controls to retain their listeners and language state.
  if (themeButton && !themeButton.hasAttribute('data-desktop-only')) {
    themeHome = document.createComment('Mobile theme toggle position');
    themeButton.before(themeHome);
  }

  if (sidebar && themeHome) {
    mobileToolbar = document.createElement('div');
    mobileToolbar.className = 'profile-toolbar';
    mobileToolbar.hidden = true;
    mobileTools = document.createElement('div');
    mobileTools.className = 'profile-toolbar-preferences';
    mobileTools.setAttribute('data-mobile-profile-tools', '');
    mobileToolbar.append(mobileTools);
    sidebar.prepend(mobileToolbar);
    if (contactButton) {
      contactHome = document.createComment('Desktop contact toggle position');
      contactButton.before(contactHome);
      contactButton.setAttribute('type', 'button');
      contactButton.setAttribute('aria-label', 'Show Contacts');
      if (contacts) {
        contacts.id ||= 'profile-contacts';
        contactButton.setAttribute('aria-controls', contacts.id);
      }
      const updateContactState = () => contactButton.setAttribute('aria-expanded', String(sidebar.classList.contains('active')));
      updateContactState();
      new MutationObserver(updateContactState).observe(sidebar, {attributes: true, attributeFilter: ['class']});
    }
  }

  function updateThemePlacement() {
    if (!themeHome || !tools) return;
    if (desktop.matches) {
      tools.append(themeButton);
      if (contactHome) contactHome.after(contactButton);
      if (mobileToolbar) mobileToolbar.hidden = true;
    } else if (mobileToolbar) {
      mobileToolbar.hidden = false;
      mobileTools.prepend(themeButton);
      if (contactButton) mobileToolbar.append(contactButton);
    } else themeHome.after(themeButton);
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
