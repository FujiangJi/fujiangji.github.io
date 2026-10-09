'use strict';

(() => {
  if (document.getElementById('mapmyvisitors')) return;
  const host = document.querySelector('[data-visitor-map]');

  function counterScript(width) {
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.id = 'mapmyvisitors';
    script.async = true;
    const light = document.documentElement.getAttribute('data-theme') === 'light';
    const colors = light ? 'co=f3f5f8&cl=b9c9dc&ct=444c59' : 'co=202632&cl=8397b3&ct=d5dbe5';
    script.src = `https://mapmyvisitors.com/map.js?d=UBwb8LAJgIolX9pV6082rkMXWOmFI37z0qyVBqTbJFw&${colors}&w=${width}`;
    return script;
  }

  if (!host) {
    // The official widget records the page when it loads, regardless of visibility.
    // Give its renderer a measurable size without adding content or footer space.
    const tracker = document.createElement('div');
    tracker.id = 'visitor-tracker';
    tracker.setAttribute('aria-hidden', 'true');
    tracker.setAttribute('inert', '');
    tracker.style.cssText = 'position:fixed;left:-10000px;top:0;width:180px;height:120px;overflow:hidden;visibility:hidden;pointer-events:none;';
    document.body.append(tracker);
    tracker.append(counterScript(180));
    return;
  }

  const status = host.querySelector('[data-visitor-status]');
  const message = status.querySelector('p');
  let ready = false;
  let timeout;

  function themeMarkers() {
    const palette = getComputedStyle(host);
    const markerColor = palette.getPropertyValue('--visitor-marker').trim();
    const oceanColor = palette.getPropertyValue('--visitor-ocean').trim();
    host.querySelectorAll('.jvectormap-marker').forEach(marker => {
      const active = marker.getAttribute('fill')?.toLowerCase() === '#f8a400';
      marker.style.fill = active ? '#f8a400' : markerColor;
      marker.style.stroke = oceanColor;
    });
  }

  function checkMap() {
    const widget = host.querySelector('#mapmyvisitors-widget');
    const map = widget?.querySelector('.mapmyvisitors-map svg, .mapmyvisitors-map canvas');
    if (!map) return;
    if (ready) {
      themeMarkers();
      return;
    }
    ready = true;
    clearTimeout(timeout);
    host.classList.add('is-ready');
    host.classList.remove('is-unavailable');
    status.hidden = true;
    const date = widget.querySelector('.mapmyvisitors-date');
    if (date) {
      const original = date.textContent.trim();
      date.title = original;
      date.textContent = original
        .replace(/\b([A-Za-z]{3})\.?\s+0?(\d{1,2})(?:st|nd|rd|th)?\b/g, '$1 $2')
        .replace(/\s+-\s+/g, ' – ');
    }
    const open = document.createElement('span');
    open.className = 'visitor-map-open';
    open.textContent = 'View map ↗';
    // The whole provider widget already links to its interactive statistics page.
    // Replace the tiny controls drawn into the background with an honest link cue.
    widget.querySelector('.mapmyvisitors-map').append(open);
    widget.setAttribute('aria-label', 'View visitor locations and website statistics on MapMyVisitors');
    widget.setAttribute('rel', 'noopener noreferrer');
    if (widget.getAttribute('href')?.startsWith('http://mapmyvisitors.com/')) {
      widget.setAttribute('href', widget.getAttribute('href').replace('http://', 'https://'));
    }
    themeMarkers();
  }

  function unavailable() {
    if (ready) return;
    message.textContent = 'The visitor map is temporarily unavailable. Please try again later.';
    host.classList.add('is-unavailable');
  }

  // The provider inserts the map beside this script in the page itself.
  // Load immediately, even when the footer has not been scrolled into view.
  const observer = new MutationObserver(checkMap);
  observer.observe(host, { childList: true, subtree: true });
  // Repaint existing and later live dots; theme changes never run the counter again.
  window.addEventListener('site-theme-change', themeMarkers);
  const script = counterScript('a');
  script.addEventListener('load', checkMap);
  script.addEventListener('error', unavailable);
  timeout = setTimeout(unavailable, 15000);
  host.append(script);
})();
