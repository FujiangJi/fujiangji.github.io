'use strict';

(function () {
  const page = document.querySelector('article.publications');
  if (!page) return;

  const published = Array.from(page.querySelectorAll('[data-pub-kind="published"]'));
  const manuscripts = Array.from(page.querySelectorAll('[data-pub-kind="manuscript"]'));
  const presentations = Array.from(page.querySelectorAll('[data-pub-kind="presentation"]'));
  const totals = {
    published: published.length,
    lead: published.filter(item => item.dataset.pubRole === 'lead').length,
    manuscript: manuscripts.length,
    presentation: presentations.length
  };
  page.querySelectorAll('[data-pub-total]').forEach(node => {
    node.textContent = totals[node.dataset.pubTotal];
  });

  const search = page.querySelector('[data-pub-search]');
  const topicFilter = page.querySelector('[data-pub-topic-filter]');
  Array.from(topicFilter.options).forEach(option => {
    if (option.value === 'all') return;
    const count = published.filter(item => item.dataset.pubTopic === option.value).length;
    option.textContent += ` (${count})`;
  });
  const filters = Array.from(page.querySelectorAll('[data-pub-filter]'));
  const groups = Array.from(page.querySelectorAll('[data-author-group]'));
  const result = page.querySelector('[data-pub-results]');
  const empty = page.querySelector('[data-pub-empty]');
  let role = 'all';
  const searchable = new Map();
  function updateSearchIndex() {
    published.forEach(item => {
      const fields = ['.pub-title', '.pub-authors', '.pub-meta', '.pub-topic', '.pub-abstract p']
        .map(selector => window.SiteLanguage.sourceText(item.querySelector(selector)));
      const bilingual = fields.concat(fields.map(value => window.SiteLanguage.chinese(value)));
      searchable.set(item, bilingual.join(' ').replace(/\s+/g, ' ').toLocaleLowerCase());
    });
  }
  updateSearchIndex();
  document.addEventListener('site:languagechange', () => {
    updateSearchIndex();
    updatePublished();
  });

  function updatePublished() {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    published.forEach(item => {
      const matchesRole = role === 'all' || item.dataset.pubRole === role;
      const matchesTopic = topicFilter.value === 'all' || item.dataset.pubTopic === topicFilter.value;
      const matchesSearch = terms.every(term => searchable.get(item).includes(term));
      item.hidden = !(matchesRole && matchesTopic && matchesSearch);
      if (!item.hidden) visible++;
    });
    groups.forEach(group => {
      const count = Array.from(group.querySelectorAll('[data-pub-kind="published"]')).filter(item => !item.hidden).length;
      group.hidden = count === 0;
      group.querySelector('[data-group-count]').textContent = `${count} ${count === 1 ? 'article' : 'articles'}`;
    });
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.pubFilter === role)));
    result.textContent = `Showing ${visible} of ${published.length} journal articles`;
    empty.hidden = visible !== 0;
  }
  search.addEventListener('input', updatePublished);
  topicFilter.addEventListener('change', updatePublished);
  filters.forEach(button => button.addEventListener('click', () => {
    role = button.dataset.pubFilter;
    updatePublished();
  }));
  updatePublished();

  page.querySelectorAll('[data-pub-abstract]').forEach(button => {
    button.addEventListener('click', () => {
      const panel = document.getElementById(button.getAttribute('aria-controls'));
      const expanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', String(!expanded));
      button.title = expanded ? 'Show abstract' : 'Hide abstract';
      panel.hidden = expanded;
    });
  });

  const more = page.querySelector('[data-presentations-toggle]');
  const presentationStatus = page.querySelector('[data-presentations-status]');
  const previewCount = 4;
  let showAll = false;
  function updatePresentations() {
    presentations.forEach((item, index) => { item.hidden = !showAll && index >= previewCount; });
    const count = showAll ? presentations.length : Math.min(previewCount, presentations.length);
    presentationStatus.textContent = `Showing ${count} of ${presentations.length} presentations`;
    more.hidden = presentations.length <= previewCount;
    more.textContent = showAll ? 'Show fewer presentations' : `Show all ${presentations.length} presentations`;
    more.setAttribute('aria-expanded', String(showAll));
  }
  more.addEventListener('click', () => {
    showAll = !showAll;
    updatePresentations();
  });
  updatePresentations();

  function revealLinkedItem() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    if (!id) return;
    const item = document.getElementById(id);
    if (!item || !item.matches('[data-pub-kind]')) return;
    if (item.dataset.pubKind === 'published') {
      role = 'all';
      search.value = '';
      topicFilter.value = 'all';
      updatePublished();
    }
    if (item.dataset.pubKind === 'presentation') {
      showAll = true;
      updatePresentations();
    }
    item.scrollIntoView({ block: 'start' });
  }
  window.addEventListener('hashchange', revealLinkedItem);
  revealLinkedItem();
})();
