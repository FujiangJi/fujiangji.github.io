'use strict';

(() => {
  const page = document.querySelector('article.blogs');
  const dialog = document.getElementById('blog-gallery');
  if (!page || !dialog) return;
  const cards = [...page.querySelectorAll('[data-album-category]')];
  const filters = [...page.querySelectorAll('[data-blog-filter]')];
  const filterStatus = document.getElementById('blog-filter-status');
  const image = dialog.querySelector('[data-gallery-image]');
  const thumbnails = dialog.querySelector('[data-gallery-thumbnails]');
  const status = dialog.querySelector('[data-gallery-status]');
  const counter = dialog.querySelector('[data-gallery-counter]');
  const original = dialog.querySelector('[data-gallery-original]');
  const stage = dialog.querySelector('.gallery-stage');
  const manifestUrl = new URL('../data/blog-albums.json?v=20261008-blog75', document.currentScript.src);
  let manifestPromise;
  let album;
  let photoIndex = 0;
  let lastTrigger;
  let request = 0;
  let swipeStart;

  function filterCollections(category) {
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.blogFilter === category)));
    cards.forEach(card => {
      card.hidden = category !== 'all' && card.dataset.albumCategory !== category;
      card.classList.remove('is-wide');
    });
    const visible = cards.filter(card => !card.hidden);
    if (visible.length % 2 === 1) visible[visible.length - 1].classList.add('is-wide');
    filterStatus.textContent = `${visible.length} ${visible.length === 1 ? 'collection' : 'collections'} shown`;
  }
  filters.forEach(button => button.addEventListener('click', () => filterCollections(button.dataset.blogFilter)));
  filterCollections('all');

  function showPhoto(index) {
    if (!album) return;
    photoIndex = (index + album.photos.length) % album.photos.length;
    const photo = album.photos[photoIndex];
    status.textContent = 'Loading photo…';
    image.alt = photo.alt;
    image.width = photo.width;
    image.height = photo.height;
    image.src = photo.view;
    counter.textContent = `${photoIndex + 1} / ${album.photos.length}`;
    original.href = photo.original;
    [...thumbnails.children].forEach((button, i) => button.setAttribute('aria-pressed', String(i === photoIndex)));
    thumbnails.children[photoIndex]?.scrollIntoView({block: 'nearest', inline: 'nearest'});
    const next = new Image();
    next.src = album.photos[(photoIndex + 1) % album.photos.length].view;
  }
  image.addEventListener('load', () => { status.textContent = ''; });
  image.addEventListener('error', () => { status.textContent = 'Unable to load this photo. You can open the original below.'; });

  async function openAlbum(id, trigger) {
    const currentRequest = ++request;
    lastTrigger = trigger;
    album = null;
    image.removeAttribute('src');
    image.alt = '';
    thumbnails.replaceChildren();
    counter.textContent = '';
    original.hidden = true;
    dialog.querySelector('[data-gallery-title]').textContent = window.SiteLanguage.sourceAttribute(trigger, 'data-album-title') || 'Photo collection';
    dialog.querySelector('[data-gallery-category]').textContent = 'Photo collection';
    dialog.querySelector('[data-gallery-dates]').textContent = '';
    dialog.querySelector('[data-gallery-location]').textContent = '';
    status.textContent = 'Loading collection…';
    document.documentElement.classList.add('blog-gallery-open');
    dialog.showModal();
    try {
      if (!manifestPromise) {
        manifestPromise = fetch(manifestUrl).then(response => {
          if (!response.ok) throw new Error('Album data unavailable');
          return response.json();
        }).catch(error => { manifestPromise = null; throw error; });
      }
      const collections = await manifestPromise;
      if (!dialog.open || currentRequest !== request) return;
      album = collections.find(collection => collection.id === id);
      if (!album?.photos.length) throw new Error('Collection is empty');
      dialog.querySelector('[data-gallery-title]').textContent = album.title;
      dialog.querySelector('[data-gallery-category]').textContent = album.categoryLabel;
      dialog.querySelector('[data-gallery-dates]').textContent = album.dates;
      dialog.querySelector('[data-gallery-location]').textContent = album.location;
      original.hidden = false;
      const fragment = document.createDocumentFragment();
      album.photos.forEach((photo, i) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'gallery-thumb';
        button.setAttribute('aria-label', `Show photo ${i + 1} of ${album.photos.length}`);
        button.setAttribute('aria-pressed', 'false');
        const thumb = document.createElement('img');
        thumb.src = photo.thumb;
        thumb.alt = '';
        thumb.width = 64;
        thumb.height = 48;
        thumb.loading = 'lazy';
        thumb.decoding = 'async';
        button.append(thumb);
        button.addEventListener('click', () => showPhoto(i));
        fragment.append(button);
      });
      thumbnails.append(fragment);
      showPhoto(0);
    } catch (error) {
      if (dialog.open && currentRequest === request) status.textContent = 'Unable to load this collection. Close and try again.';
    }
  }
  page.querySelectorAll('[data-open-album]').forEach(trigger => trigger.addEventListener('click', event => {
    event.preventDefault();
    openAlbum(trigger.dataset.openAlbum, trigger);
  }));
  dialog.querySelector('[data-gallery-close]').addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-gallery-prev]').addEventListener('click', () => showPhoto(photoIndex - 1));
  dialog.querySelector('[data-gallery-next]').addEventListener('click', () => showPhoto(photoIndex + 1));
  dialog.addEventListener('keydown', event => {
    if (!album) return;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      showPhoto(photoIndex + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    ++request;
    album = null;
    swipeStart = null;
    document.documentElement.classList.remove('blog-gallery-open');
    if (lastTrigger?.isConnected) lastTrigger.focus({preventScroll: true});
  });
  stage.addEventListener('pointerdown', event => {
    if (event.target.closest('button, a') || event.button !== 0) return;
    swipeStart = {x: event.clientX, y: event.clientY, id: event.pointerId};
    stage.setPointerCapture(event.pointerId);
  });
  stage.addEventListener('pointerup', event => {
    if (!swipeStart || swipeStart.id !== event.pointerId) return;
    const dx = event.clientX - swipeStart.x;
    const dy = event.clientY - swipeStart.y;
    swipeStart = null;
    if (Math.abs(dx) >= 44 && Math.abs(dx) > Math.abs(dy) * 1.5) showPhoto(photoIndex + (dx < 0 ? 1 : -1));
  });
  stage.addEventListener('pointercancel', () => { swipeStart = null; });
  const map = page.querySelector('.blog-map');
  const mapToggle = page.querySelector('[data-map-expand]');
  mapToggle.addEventListener('click', () => {
    const expanded = map.classList.toggle('is-expanded');
    mapToggle.setAttribute('aria-expanded', String(expanded));
    mapToggle.textContent = expanded ? 'Reduce map' : 'Expand map';
  });
})();
