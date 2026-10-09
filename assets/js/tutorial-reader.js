'use strict';

(() => {
  const reader = document.querySelector('.tutorial-reader');
  if (!reader) return;

  // The source template retains the complete example, including layout notes.
  reader.querySelectorAll('[data-code-card]').forEach(card => {
    const copy = card.querySelector('[data-code-copy]');
    const wrap = card.querySelector('[data-code-wrap]');
    const expand = card.querySelector('[data-code-expand]');
    const status = card.querySelector('[data-code-status]');
    let feedbackTimer;
    const feedback = message => {
      clearTimeout(feedbackTimer);
      status.textContent = message;
      feedbackTimer = setTimeout(() => { status.textContent = ''; }, 2600);
    };
    copy.addEventListener('click', async () => {
      const source = card.querySelector('[data-code-source]').content.textContent;
      try {
        await navigator.clipboard.writeText(source);
        feedback('Copied complete example');
      } catch (_) {
        feedback('Copy unavailable. Use the download button.');
      }
    });
    wrap.addEventListener('click', () => {
      const wrapped = card.classList.toggle('is-wrapped');
      wrap.setAttribute('aria-pressed', String(wrapped));
    });
    if (expand) {
      const original = expand.innerHTML;
      expand.addEventListener('click', () => {
        const collapsed = card.classList.toggle('is-collapsed');
        expand.setAttribute('aria-expanded', String(!collapsed));
        expand.innerHTML = collapsed ? original : 'Collapse code <span aria-hidden="true">↑</span>';
        // Keep the code header reachable when collapsing a long example.
        if (collapsed && card.getBoundingClientRect().top < 0) card.scrollIntoView({ block: 'start' });
      });
    }
  });
  if (window.hljs) reader.querySelectorAll('.lesson-code-scroll code').forEach(code => window.hljs.highlightElement(code));

  const preparation = reader.querySelector('.lesson-preparation > details:last-child');
  const showPreparation = window.matchMedia('(min-width: 768px)');
  const configurePreparation = () => { preparation.open = showPreparation.matches; };
  configurePreparation();
  showPreparation.addEventListener('change', configurePreparation);

  const outline = reader.querySelector('[data-lesson-outline]');
  const wide = window.matchMedia('(min-width: 1250px)');
  const configureOutline = () => { outline.open = wide.matches; };
  configureOutline();
  wide.addEventListener('change', configureOutline);
  outline.addEventListener('toggle', () => { if (wide.matches && !outline.open) outline.open = true; });
  const tocLinks = [...reader.querySelectorAll('[data-lesson-toc]')];
  const sections = [...reader.querySelectorAll('.lesson-section')];
  const updateChapter = () => {
    let current = sections[0];
    const top = window.innerWidth >= 1024 ? 120 : 80;
    for (const section of sections) if (section.getBoundingClientRect().top <= top) current = section;
    tocLinks.forEach(link => {
      if (link.hash === '#' + current.id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  };
  let framePending = false;
  window.addEventListener('scroll', () => {
    if (framePending) return;
    framePending = true;
    requestAnimationFrame(() => { updateChapter(); framePending = false; });
  }, { passive: true });
  updateChapter();
  tocLinks.forEach(link => link.addEventListener('click', () => { if (!wide.matches) outline.open = false; }));

  const viewer = document.querySelector('[data-lesson-viewer]');
  const full = viewer.querySelector('[data-image-full]');
  const stage = viewer.querySelector('[data-image-stage]');
  const title = viewer.querySelector('#lesson-image-title');
  const fit = viewer.querySelector('[data-image-fit]');
  const zoom = viewer.querySelector('[data-image-read]');
  const original = viewer.querySelector('[data-image-original]');
  let opener;
  let zoomed = false;
  let drag;
  const sizeFigure = () => {
    if (!viewer.open || !full.naturalWidth) return;
    const padding = window.innerWidth < 768 ? 30 : 48;
    const ratio = Math.min((stage.clientWidth - padding) / full.naturalWidth, (stage.clientHeight - padding) / full.naturalHeight, 1);
    const width = zoomed ? Math.max(full.naturalWidth, Math.round(full.naturalWidth * ratio * 2)) : Math.round(full.naturalWidth * ratio);
    full.style.width = width + 'px';
    full.style.height = 'auto';
    viewer.classList.toggle('is-zoomed', zoomed);
    fit.setAttribute('aria-pressed', String(!zoomed));
    zoom.setAttribute('aria-pressed', String(zoomed));
  };
  const resetPosition = () => { stage.scrollTop = 0; stage.scrollLeft = 0; };
  full.addEventListener('load', () => { sizeFigure(); resetPosition(); });
  new ResizeObserver(sizeFigure).observe(stage);
  reader.querySelectorAll('[data-lesson-image]').forEach(button => {
    button.addEventListener('click', () => {
      opener = button;
      zoomed = false;
      const caption = window.SiteLanguage.sourceAttribute(button, 'data-image-caption');
      title.textContent = caption;
      full.alt = caption;
      full.style.setProperty('--figure-background', button.dataset.imageBackground);
      original.href = button.dataset.imageSrc;
      full.src = button.dataset.imageSrc;
      viewer.showModal();
      document.documentElement.classList.add('lesson-viewer-open');
      sizeFigure();
      resetPosition();
      viewer.querySelector('[data-image-close]').focus();
    });
  });
  fit.addEventListener('click', () => { zoomed = false; sizeFigure(); resetPosition(); });
  zoom.addEventListener('click', () => { zoomed = true; sizeFigure(); resetPosition(); });
  viewer.querySelector('[data-image-close]').addEventListener('click', () => viewer.close());
  viewer.addEventListener('click', event => { if (event.target === viewer) viewer.close(); });
  viewer.addEventListener('close', () => {
    document.documentElement.classList.remove('lesson-viewer-open');
    viewer.classList.remove('is-dragging');
    drag = undefined;
    if (opener) opener.focus({ preventScroll: true });
  });
  // Native touch scrolling stays available. A mouse can pan a zoomed figure.
  stage.addEventListener('pointerdown', event => {
    if (!zoomed || event.pointerType !== 'mouse' || event.button !== 0) return;
    event.preventDefault();
    drag = { x: event.clientX, y: event.clientY, left: stage.scrollLeft, top: stage.scrollTop };
    stage.setPointerCapture(event.pointerId);
    viewer.classList.add('is-dragging');
  });
  stage.addEventListener('pointermove', event => {
    if (!drag) return;
    stage.scrollLeft = drag.left + drag.x - event.clientX;
    stage.scrollTop = drag.top + drag.y - event.clientY;
  });
  const stopDrag = () => { drag = undefined; viewer.classList.remove('is-dragging'); };
  stage.addEventListener('pointerup', stopDrag);
  stage.addEventListener('pointercancel', stopDrag);
})();
