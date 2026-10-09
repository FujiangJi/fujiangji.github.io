'use strict';

(() => {
  const page = document.querySelector('article.research');
  if (!page) return;

  function setDirection(card, open) {
    card.classList.toggle('open', open);
    card.querySelector('.direction-papers').classList.toggle('open', open);
    card.querySelector('.direction-expand-btn').setAttribute('aria-expanded', String(open));
  }
  function setStudy(card, open) {
    card.classList.toggle('open', open);
    card.querySelector('.paper-detail-toggle').setAttribute('aria-expanded', String(open));
    if (open) {
      card.querySelectorAll('img[data-src]').forEach(img => {
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
      });
    }
  }
  page.querySelectorAll('.direction-cover').forEach(cover => {
    cover.addEventListener('click', () => {
      const card = cover.closest('.research-direction-card');
      setDirection(card, !card.classList.contains('open'));
    });
  });
  page.querySelectorAll('.paper-card-header').forEach(header => {
    header.addEventListener('click', event => {
      if (event.target.closest('a')) return;
      const card = header.closest('.paper-card');
      setStudy(card, !card.classList.contains('open'));
    });
  });
  // Preserve existing links from the overview and homepage.
  window.openResearchTheme = id => {
    const card = document.getElementById(id);
    if (card) setDirection(card, true);
  };
  function revealLinkedStudy() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    const direction = target?.closest('.research-direction-card');
    if (!direction) return;
    setDirection(direction, true);
    const study = target.closest('.paper-card');
    if (study) setStudy(study, true);
    requestAnimationFrame(() => target.scrollIntoView({block: 'start'}));
  }
  window.addEventListener('hashchange', revealLinkedStudy);
  revealLinkedStudy();

  const dialog = document.getElementById('research-figure-viewer');
  const stage = dialog.querySelector('[data-figure-stage]');
  const canvas = dialog.querySelector('[data-figure-canvas]');
  const image = dialog.querySelector('[data-figure-image]');
  const status = dialog.querySelector('[data-figure-status]');
  const zoomValue = dialog.querySelector('[data-figure-zoom]');
  const zoomIn = dialog.querySelector('[data-figure-in]');
  const zoomOut = dialog.querySelector('[data-figure-out]');
  let trigger;
  let scale = 1;
  let fitScale = 1;
  let width = 1;
  let height = 1;
  function resize(nextScale) {
    const x = (stage.scrollLeft + stage.clientWidth / 2 - image.offsetLeft) / scale;
    const y = (stage.scrollTop + stage.clientHeight / 2 - image.offsetTop) / scale;
    scale = Math.max(fitScale, Math.min(nextScale, 2));
    const w = Math.round(width * scale);
    const h = Math.round(height * scale);
    canvas.style.width = `${Math.max(stage.clientWidth, w + 32)}px`;
    canvas.style.height = `${Math.max(stage.clientHeight, h + 32)}px`;
    image.style.width = `${w}px`;
    image.style.height = `${h}px`;
    stage.scrollLeft = x * scale + image.offsetLeft - stage.clientWidth / 2;
    stage.scrollTop = y * scale + image.offsetTop - stage.clientHeight / 2;
    zoomValue.textContent = `${Math.round(scale * 100)}%`;
    zoomOut.disabled = scale <= fitScale + .001;
    zoomIn.disabled = scale >= 2;
  }
  function fit() {
    fitScale = Math.min((stage.clientWidth - 32) / width, (stage.clientHeight - 32) / height, 1);
    resize(fitScale);
    stage.scrollLeft = stage.scrollTop = 0;
  }
  image.addEventListener('load', () => { status.textContent = ''; fit(); });
  image.addEventListener('error', () => { status.textContent = 'Unable to load this figure. Try the original image link.'; });
  page.querySelectorAll('.research-figure-open').forEach(button => {
    button.addEventListener('click', () => {
      const source = button.querySelector('img');
      trigger = button;
      width = Number(source.getAttribute('width'));
      height = Number(source.getAttribute('height'));
      image.alt = window.SiteLanguage.sourceAttribute(source, 'alt');
      image.width = width;
      image.height = height;
      dialog.querySelector('[data-figure-title]').textContent = window.SiteLanguage.sourceAttribute(source, 'alt');
      dialog.querySelector('[data-figure-original]').href = source.src;
      status.textContent = 'Loading figure…';
      dialog.showModal();
      image.src = source.src;
      fit();
    });
  });
  zoomIn.addEventListener('click', () => resize(scale * 1.5));
  zoomOut.addEventListener('click', () => resize(scale / 1.5));
  dialog.querySelector('[data-figure-fit]').addEventListener('click', fit);
  dialog.querySelector('[data-figure-actual]').addEventListener('click', () => resize(1));
  dialog.querySelector('[data-figure-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => { image.removeAttribute('src'); trigger?.focus(); });
  window.addEventListener('resize', () => { if (dialog.open) fit(); });
})();
