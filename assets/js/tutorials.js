'use strict';

(() => {
  const page = document.querySelector('article.tutorials');
  if (!page) return;
  const cards = [...page.querySelectorAll('[data-tutorial-category]')];
  const filters = [...page.querySelectorAll('[data-tutorial-filter]')];
  const summary = page.querySelector('[data-tutorial-summary]');
  const status = page.querySelector('[data-tutorial-status]');

  function filterTutorials(button) {
    const category = button.dataset.tutorialFilter;
    filters.forEach(filter => filter.setAttribute('aria-pressed', String(filter === button)));
    cards.forEach(card => { card.hidden = category !== 'all' && card.dataset.tutorialCategory !== category; });
    const count = cards.filter(card => !card.hidden).length;
    const labelNode = button.querySelector('[data-filter-label]');
    const label = category === 'all' ? 'All topics' : window.SiteLanguage.sourceText(labelNode);
    summary.textContent = `${count} ${count === 1 ? 'guide' : 'guides'} · ${label}`;
    status.textContent = `${count} ${count === 1 ? 'guide' : 'guides'} shown. ${label}.`;
  }

  filters.forEach(button => {
    const category = button.dataset.tutorialFilter;
    button.querySelector('.tutorial-filter-count').textContent = cards.filter(card => category === 'all' || card.dataset.tutorialCategory === category).length;
    button.addEventListener('click', () => filterTutorials(button));
  });
  filterTutorials(filters.find(button => button.getAttribute('aria-pressed') === 'true') || filters[0]);
})();
