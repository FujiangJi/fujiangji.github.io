'use strict';

(() => {
  const dialog = document.getElementById('poster-viewer');
  if (!dialog) return;
  const stage = dialog.querySelector('[data-poster-stage]');
  const canvas = dialog.querySelector('[data-poster-canvas]');
  const image = dialog.querySelector('[data-poster-image]');
  const status = dialog.querySelector('[data-poster-status]');
  const zoomValue = dialog.querySelector('[data-poster-zoom-value]');
  const readButton = dialog.querySelector('[data-poster-read]');
  const zoomIn = dialog.querySelector('[data-poster-zoom-in]');
  const zoomOut = dialog.querySelector('[data-poster-zoom-out]');
  const pdfLink = dialog.querySelector('[data-poster-pdf]');
  const imageLink = dialog.querySelector('[data-poster-original]');
  const manifestUrl = new URL('../data/posters.json?v=20261008-posters79-final', document.currentScript.src);
  let manifestPromise;
  let posters;
  let poster;
  let index = 0;
  let request = 0;
  let lastTrigger;
  let scale = 1;
  let fitScale = 1;
  let fullReady = false;
  let mouseDrag;

  function calculateFit() {
    return Math.min((stage.clientWidth - 32) / poster.width, (stage.clientHeight - 32) / poster.height, 1);
  }

  function resizePoster(nextScale, anchor = {x: stage.clientWidth / 2, y: stage.clientHeight / 2}) {
    if (!poster) return;
    const point = {
      x: (stage.scrollLeft + anchor.x - image.offsetLeft) / scale,
      y: (stage.scrollTop + anchor.y - image.offsetTop) / scale
    };
    scale = Math.max(fitScale, Math.min(nextScale, 2));
    const width = Math.round(poster.width * scale);
    const height = Math.round(poster.height * scale);
    canvas.style.width = `${Math.max(stage.clientWidth, width + 32)}px`;
    canvas.style.height = `${Math.max(stage.clientHeight, height + 32)}px`;
    image.style.width = `${width}px`;
    image.style.height = `${height}px`;
    stage.scrollLeft = point.x * scale + image.offsetLeft - anchor.x;
    stage.scrollTop = point.y * scale + image.offsetTop - anchor.y;
    stage.classList.toggle('is-zoomed', scale > fitScale + .001);
    zoomValue.textContent = `${Math.round(scale * 100)}%`;
    zoomOut.disabled = scale <= fitScale + .001;
    zoomIn.disabled = scale >= 2;
  }

  function fitPoster() {
    if (!poster) return;
    fitScale = calculateFit();
    resizePoster(fitScale);
    stage.scrollLeft = 0;
    stage.scrollTop = 0;
  }

  function showPoster(nextIndex) {
    index = (nextIndex + posters.length) % posters.length;
    poster = posters[index];
    const currentRequest = ++request;
    fullReady = false;
    readButton.disabled = true;
    image.hidden = false;
    image.alt = `${poster.fullTitle} — ${poster.venue} ${poster.year}`;
    image.width = poster.width;
    image.height = poster.height;
    image.src = poster.preview;
    dialog.querySelector('[data-poster-title]').textContent = poster.fullTitle;
    dialog.querySelector('[data-poster-meta]').textContent = `${poster.venue} ${poster.year} · ${poster.location}`;
    dialog.querySelector('[data-poster-counter]').textContent = `${index + 1} / ${posters.length}`;
    pdfLink.href = poster.pdf;
    pdfLink.download = `${poster.id}.pdf`;
    pdfLink.title = `Download original PDF (${(poster.pdfBytes / 1_000_000).toFixed(1)} MB)`;
    imageLink.href = poster.full;
    pdfLink.hidden = imageLink.hidden = false;
    status.textContent = 'Loading high-resolution poster…';
    fitPoster();
    const full = new Image();
    full.onload = () => {
      if (!dialog.open || currentRequest !== request) return;
      fullReady = true;
      image.src = poster.full;
      readButton.disabled = false;
      status.textContent = '';
    };
    full.onerror = () => {
      if (dialog.open && currentRequest === request) status.textContent = 'High-resolution image unavailable. Open the original PDF below.';
    };
    full.src = poster.full;
  }

  async function openPoster(id, trigger) {
    lastTrigger = trigger;
    const openingRequest = ++request;
    poster = null;
    image.removeAttribute('src');
    image.hidden = true;
    pdfLink.hidden = imageLink.hidden = true;
    readButton.disabled = true;
    zoomIn.disabled = zoomOut.disabled = true;
    dialog.querySelector('[data-poster-title]').textContent = 'Conference poster';
    dialog.querySelector('[data-poster-meta]').textContent = '';
    status.textContent = 'Loading poster…';
    document.documentElement.classList.add('poster-viewer-open');
    if (!dialog.open) dialog.showModal();
    try {
      if (!manifestPromise) {
        manifestPromise = fetch(manifestUrl).then(response => {
          if (!response.ok) throw new Error('Poster data unavailable');
          return response.json();
        }).catch(error => { manifestPromise = null; throw error; });
      }
      posters = await manifestPromise;
      if (!dialog.open || openingRequest !== request) return;
      const selected = posters.findIndex(item => item.id === id);
      if (selected < 0) throw new Error('Poster not found');
      showPoster(selected);
    } catch {
      if (dialog.open && openingRequest === request) {
        imageLink.href = trigger.href;
        imageLink.hidden = false;
        status.textContent = 'Unable to load the reader. Open the poster image below.';
      }
    }
  }

  document.querySelectorAll('[data-view-poster]').forEach(trigger => {
    trigger.addEventListener('click', event => {
      if (!dialog.showModal || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      openPoster(trigger.dataset.viewPoster, trigger);
    });
  });
  dialog.querySelector('[data-poster-close]').addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-poster-fit]').addEventListener('click', fitPoster);
  zoomIn.addEventListener('click', () => resizePoster(scale * Math.SQRT2));
  zoomOut.addEventListener('click', () => resizePoster(scale / Math.SQRT2));
  readButton.addEventListener('click', () => { if (fullReady) resizePoster(Math.max(fitScale, 3200 / poster.width)); });
  dialog.querySelector('[data-poster-prev]').addEventListener('click', () => { if (poster) showPoster(index - 1); });
  dialog.querySelector('[data-poster-next]').addEventListener('click', () => { if (poster) showPoster(index + 1); });
  dialog.addEventListener('keydown', event => {
    if (!poster || event.ctrlKey || event.metaKey || event.altKey) return;
    if (event.key === '+' || event.key === '=') { event.preventDefault(); resizePoster(scale * Math.SQRT2); }
    if (event.key === '-') { event.preventDefault(); resizePoster(scale / Math.SQRT2); }
    if (event.key.toLowerCase() === 'f') { event.preventDefault(); fitPoster(); }
    if (event.key === 'PageDown' || event.key === 'PageUp') {
      event.preventDefault(); showPoster(index + (event.key === 'PageDown' ? 1 : -1));
    }
    if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
      event.preventDefault();
      if (scale > fitScale + .001) {
        stage.scrollLeft += event.key === 'ArrowLeft' ? -80 : event.key === 'ArrowRight' ? 80 : 0;
        stage.scrollTop += event.key === 'ArrowUp' ? -80 : event.key === 'ArrowDown' ? 80 : 0;
      } else if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') showPoster(index + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  stage.addEventListener('wheel', event => {
    if (!poster || !(event.ctrlKey || event.metaKey)) return;
    event.preventDefault();
    const rect = stage.getBoundingClientRect();
    resizePoster(scale * Math.exp(-event.deltaY * .003), {x: event.clientX - rect.left, y: event.clientY - rect.top});
  }, {passive: false});
  stage.addEventListener('pointerdown', event => {
    if (event.pointerType !== 'mouse' || event.button !== 0 || scale <= fitScale + .001) return;
    event.preventDefault();
    mouseDrag = {id: event.pointerId, x: event.clientX, y: event.clientY, left: stage.scrollLeft, top: stage.scrollTop};
    stage.setPointerCapture(event.pointerId);
    stage.classList.add('is-dragging');
  });
  stage.addEventListener('pointermove', event => {
    if (!mouseDrag || mouseDrag.id !== event.pointerId) return;
    stage.scrollLeft = mouseDrag.left - (event.clientX - mouseDrag.x);
    stage.scrollTop = mouseDrag.top - (event.clientY - mouseDrag.y);
  });
  function endDrag() { mouseDrag = null; stage.classList.remove('is-dragging'); }
  stage.addEventListener('pointerup', endDrag);
  stage.addEventListener('pointercancel', endDrag);
  new ResizeObserver(() => {
    if (!dialog.open || !poster) return;
    const wasFit = Math.abs(scale - fitScale) < .001;
    fitScale = calculateFit();
    if (wasFit) fitPoster();
    else resizePoster(scale);
  }).observe(stage);
  dialog.addEventListener('close', () => {
    ++request;
    poster = null;
    endDrag();
    image.removeAttribute('src');
    document.documentElement.classList.remove('poster-viewer-open');
    lastTrigger?.focus({preventScroll: true});
  });

  function openLinkedPoster() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const trigger = document.getElementById(id);
    if (!trigger?.matches('.poster-card[data-view-poster]')) return;
    trigger.scrollIntoView({block: 'center'});
    openPoster(trigger.dataset.viewPoster, trigger);
  }
  window.addEventListener('hashchange', openLinkedPoster);
  openLinkedPoster();
})();
