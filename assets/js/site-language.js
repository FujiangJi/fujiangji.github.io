'use strict';

// Keep English HTML as the source and translate text nodes without replacing
// interactive elements. Language belongs to the URL, never local storage.
(() => {
  const scriptUrl = document.currentScript.src;
  const localeRoot = new URL('../i18n/zh/', scriptUrl);
  const path = location.pathname;
  const page = path.endsWith('/') || path.endsWith('/index.html') ? 'about' : path.split('/').pop().replace(/\.html$/, '');
  const pages = new Set(['about', 'research', 'publications', 'tutorials', 'blogs', 'contact', 'data_visualization', 'global_forest_edge_mapping', 'hpc', 'rs_data_processing', 'scatter_line_plot', 'vcs']);
  let language = 'en';
  let dictionary = {};
  let localePromise;
  let revision = 0;
  let ready = false;
  const texts = new WeakMap();
  const attributes = new WeakMap();
  const links = new WeakMap();
  const translatedAttributes = ['title', 'alt', 'placeholder', 'aria-label', 'data-image-caption', 'data-album-title'];
  const skip = 'script, style, pre, code, template, [data-language-control], [data-i18n-keep]';
  const normalize = value => value.replace(/\s+/g, ' ').trim();
  const readLanguage = () => new URL(location.href).searchParams.get('lang') === 'zh' ? 'zh' : 'en';

  function translate(value) {
    if (language !== 'zh') return value;
    const key = normalize(value);
    if (Object.hasOwn(dictionary, key)) return dictionary[key];
    let match;
    if ((match = key.match(/^Toggle abstract: (.+)$/))) return '切换摘要：' + match[1];
    if ((match = key.match(/^Toggle study details: (.+)$/))) return '展开或收起研究详情：' + match[1];
    if ((match = key.match(/^Open poster: (.+)$/))) return '打开海报：' + match[1];
    if ((match = key.match(/^Enlarge figure: (.+)$/))) return '放大图片：' + translate(match[1]);
    if ((match = key.match(/^Toggle line wrapping for (.+)$/))) return '切换 ' + match[1] + ' 的自动换行';
    if ((match = key.match(/^Copy (.+\.(?:py|sh))$/))) return '复制 ' + match[1];
    if ((match = key.match(/^Download (.+\.(?:py|sh))$/))) return '下载 ' + match[1];
    if ((match = key.match(/^(.+\.(?:py|sh)) code$/))) return match[1] + ' 代码';
    if ((match = key.match(/^Expand code · (\d+) lines$/))) return '展开代码 · ' + match[1] + ' 行';
    if ((match = key.match(/^(.+) · Click to enlarge$/))) return translate(match[1]) + ' · 点击放大';
    if ((match = key.match(/^JCR (Q[1-4]|\d{4}) · (.+)$/))) return 'JCR ' + match[1] + ' · ' + translate(match[2]);
    if ((match = key.match(/^Under Review — (.+)$/))) return '审稿中 — ' + match[1];
    if ((match = key.match(/^Journal Impact Factor; (\d{4})\. Source: (.+)$/))) return '期刊影响因子；' + match[1] + '年。来源：' + match[2];
    if ((match = key.match(/^Journal Impact Factor; current publisher value, checked 8 Oct 2026\. Source: (.+)$/))) return '期刊影响因子；出版商当前数值，核对日期2026年10月8日。来源：' + match[1];
    if ((match = key.match(/^Showing (\d+) of (\d+) journal articles$/))) return '显示 ' + match[1] + ' / ' + match[2] + ' 篇期刊论文';
    if ((match = key.match(/^Showing (\d+) of (\d+) presentations$/))) return '显示 ' + match[1] + ' / ' + match[2] + ' 项会议报告';
    if ((match = key.match(/^Showing (\d+) of (\d+)$/))) return '显示 ' + match[1] + ' / ' + match[2] + ' 条';
    if ((match = key.match(/^Show all (\d+) presentations$/))) return '查看全部 ' + match[1] + ' 项会议报告';
    if ((match = key.match(/^(\d+) articles?$/))) return match[1] + ' 篇论文';
    if ((match = key.match(/^(\d+) collections? shown$/))) return '显示 ' + match[1] + ' 个相册';
    if ((match = key.match(/^(\d+) photos?$/))) return match[1] + ' 张照片';
    if ((match = key.match(/^Show photo (\d+) of (\d+)$/))) return '查看第 ' + match[1] + ' 张照片，共 ' + match[2] + ' 张';
    if ((match = key.match(/^(\d+) guides? · (.+)$/))) return match[1] + ' 篇教程 · ' + translate(match[2]);
    if ((match = key.match(/^(\d+) guides? shown\. (.+)\.$/))) return '显示 ' + match[1] + ' 篇教程。' + translate(match[2]) + '。';
    if ((match = key.match(/^(.+) \((\d+)\)$/)) && Object.hasOwn(dictionary, match[1])) return dictionary[match[1]] + '（' + match[2] + '）';
    if ((match = key.match(/^Download original PDF \(([\d.]+) MB\)$/))) return '下载原始 PDF（' + match[1] + ' MB）';
    if ((match = key.match(/^(.+) — (?:photo|photograph) (\d+)$/))) return translate(match[1]) + ' · 第 ' + match[2] + ' 张照片';
    if ((match = key.match(/^(.+) (\d{4}) · (.+)$/)) && Object.hasOwn(dictionary, match[1])) return dictionary[match[1]] + ' ' + match[2] + ' · ' + translate(match[3]);
    if ((match = key.match(/^([A-Z][a-z]+) (\d+), (\d{4})$/))) {
      const months = {Jan:1, Feb:2, Mar:3, Apr:4, May:5, Jun:6, Jul:7, Aug:8, Sep:9, Oct:10, Nov:11, Dec:12};
      if (months[match[1]]) return match[3] + '年' + months[match[1]] + '月' + match[2] + '日';
    }
    return value;
  }

  function translatedValue(source) {
    const translated = translate(source);
    if (translated === source) return source;
    const leading = source.match(/^\s*/)[0];
    const trailing = source.match(/\s*$/)[0];
    return leading + translated + trailing;
  }

  function visitText(node) {
    if (!node.parentElement || node.parentElement.closest(skip)) return;
    let record = texts.get(node);
    if (!record || (node.data !== record.last && node.data !== record.en)) record = { en: node.data, last: node.data };
    const next = language === 'zh' ? translatedValue(record.en) : record.en;
    record.last = next;
    texts.set(node, record);
    if (node.data !== next) node.data = next;
  }

  function flowRoot(element) {
    // Separate buttons, badges and block layout; join ordinary inline emphasis.
    while (element.parentElement && ['inline', 'contents'].includes(getComputedStyle(element).display)) element = element.parentElement;
    return element;
  }

  function formatChineseRuns(root) {
    if (language !== 'zh') return;
    const element = root.nodeType === Node.TEXT_NODE ? root.parentElement : root;
    if (!element || element.nodeType !== Node.ELEMENT_NODE || element.closest(skip)) return;
    const scope = flowRoot(element);
    const han = /[\u3400-\u9fff]/;
    const opening = /[（【《「『“]/;
    const closing = /[，。！？；：、）】》」』”]/;
    const separator = /[，。！？；：、]/;
    const punctuation = {'.': '。', ',': '，', ';': '；', ':': '：', '!': '！', '?': '？'};
    const flows = new WeakMap();
    const walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT);
    let current;
    let run = [];

    function finish() {
      if (!run.length) return;
      if (han.test(current.textContent)) {
        const base = run.map(node => {
          if (!texts.has(node)) texts.set(node, {en: node.data, last: node.data});
          return translatedValue(texts.get(node).en);
        });
        const joined = base.join('');
        let position = 0;
        const values = run.map((node, index) => {
          // Localize standalone sentence punctuation, never decimal points,
          // filenames, full English titles or punctuation inside code.
          const original = normalize(texts.get(node).en);
          const before = joined.slice(0, position).trim().slice(-1);
          position += base[index].length;
          const after = joined.slice(position).trim()[0] || '';
          const numericComma = original === ',' && /\d/.test(before) && /\d/.test(after);
          const technicalDot = original === '.' && /[A-Za-z0-9_]/.test(after);
          return Object.hasOwn(punctuation, original) && !numericComma && !technicalDot ? base[index].replace(original, punctuation[original]) : base[index];
        });
        const value = values.join('');
        const remove = new Set();
        for (const match of value.matchAll(/\s+/g)) {
          const left = value[match.index - 1] || '';
          const right = value[match.index + match[0].length] || '';
          if (!left || !right) continue;
          if (closing.test(right) || opening.test(left) || separator.test(left) ||
              (han.test(left) && (han.test(right) || opening.test(right))) ||
              (closing.test(left) && han.test(right))) {
            for (let i = match.index; i < match.index + match[0].length; i++) remove.add(i);
          }
        }
        let offset = 0;
        run.forEach((node, index) => {
          // These text runs use UTF-16 offsets, including any emoji pairs.
          let formatted = '';
          for (let i = 0; i < values[index].length; i++) if (!remove.has(offset + i)) formatted += values[index][i];
          offset += values[index].length;
          texts.get(node).last = formatted;
          if (node.data !== formatted) node.data = formatted;
        });
      }
      run = [];
    }

    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (node.parentElement.closest(skip)) { finish(); current = null; continue; }
      let flow = flows.get(node.parentElement);
      if (!flow) { flow = flowRoot(node.parentElement); flows.set(node.parentElement, flow); }
      if (flow !== current) { finish(); current = flow; }
      run.push(node);
    }
    finish();
  }

  function visitAttributes(element) {
    if (element.closest(skip)) return;
    let records = attributes.get(element);
    if (!records) { records = {}; attributes.set(element, records); }
    const names = element.matches('meta[name="description"], meta[property="og:title"], meta[property="og:description"], meta[property="og:image:alt"], meta[name="twitter:title"], meta[name="twitter:description"], meta[name="twitter:image:alt"]') ? [...translatedAttributes, 'content'] : translatedAttributes;
    names.forEach(name => {
      if (!element.hasAttribute(name)) return;
      const current = element.getAttribute(name);
      let record = records[name];
      if (!record || (current !== record.last && current !== record.en)) record = { en: current, last: current };
      const next = language === 'zh' ? translate(record.en) : record.en;
      record.last = next;
      records[name] = record;
      if (current !== next) element.setAttribute(name, next);
    });
  }

  function href(value, nextLanguage = language) {
    const url = new URL(value, location.href);
    if (url.origin !== location.origin) return value;
    const key = url.pathname.endsWith('/') || url.pathname.endsWith('/index.html') ? 'about' : url.pathname.split('/').pop().replace(/\.html$/, '');
    if (!pages.has(key)) return value;
    if (nextLanguage === 'zh') url.searchParams.set('lang', 'zh');
    else url.searchParams.delete('lang');
    return url.href;
  }

  function visitLink(link) {
    const current = link.getAttribute('href');
    if (!current || current.startsWith('#')) return;
    let record = links.get(link);
    if (!record || (current !== record.last && current !== record.en)) record = {en: current, last: current};
    const next = language === 'zh' ? href(record.en) : record.en;
    record.last = next;
    links.set(link, record);
    if (current !== next) link.setAttribute('href', next);
  }

  function apply(root = document.documentElement) {
    if (root.nodeType === Node.TEXT_NODE) { visitText(root); formatChineseRuns(root); return; }
    if (root.nodeType !== Node.ELEMENT_NODE || root.closest(skip)) return;
    visitAttributes(root);
    if (root.matches('a[href]')) visitLink(root);
    root.querySelectorAll('*').forEach(element => {
      visitAttributes(element);
      if (element.matches('a[href]')) visitLink(element);
    });
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) visitText(walker.currentNode);
    formatChineseRuns(root);
  }

  async function loadLocale() {
    if (!localePromise) {
      localePromise = Promise.all(['common', page].map(name => fetch(new URL(name + '.json?v=20261009-zh93', localeRoot)).then(response => {
        if (!response.ok) throw new Error('Translation unavailable');
        return response.json();
      }))).then(([common, current]) => { dictionary = {...common, ...current}; }).catch(error => { localePromise = null; throw error; });
    }
    return localePromise;
  }

  function updateControl() {
    document.querySelectorAll('[data-language-value]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.languageValue === language)));
    const control = document.querySelector('[data-language-control]');
    if (control) control.setAttribute('aria-label', language === 'zh' ? '选择页面语言' : 'Select page language');
    const localeMeta = document.querySelector('meta[property="og:locale"]');
    if (localeMeta) localeMeta.content = language === 'zh' ? 'zh_CN' : 'en_US';
  }

  async function setLanguage(next, { history = false, preservePosition = true } = {}) {
    const token = ++revision;
    const control = document.querySelector('[data-language-control]');
    if (control) control.setAttribute('aria-busy', 'true');
    try {
      if (next === 'zh') await loadLocale();
      if (token !== revision) return;
      const point = preservePosition && !document.querySelector('dialog[open]') ? document.elementFromPoint(Math.round(innerWidth * .55), innerWidth >= 1024 ? 130 : 100) : null;
      const previousTop = point?.getBoundingClientRect().top;
      language = next;
      document.documentElement.lang = next === 'zh' ? 'zh-CN' : 'en';
      if (history) window.history.pushState({}, '', href(location.href, next));
      apply();
      updateControl();
      document.dispatchEvent(new CustomEvent('site:languagechange', {detail: {language}}));
      if (point?.isConnected && previousTop !== undefined) requestAnimationFrame(() => window.scrollBy(0, point.getBoundingClientRect().top - previousTop));
      document.querySelector('[data-language-status]').textContent = next === 'zh' ? '已切换为中文' : 'Switched to English';
    } catch (error) {
      document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
      document.querySelector('[data-language-status]').textContent = '中文暂时未能加载，请稍后重试。';
    } finally {
      if (token === revision && control) control.removeAttribute('aria-busy');
    }
  }

  window.SiteLanguage = {
    href,
    translate,
    chinese(value) { return dictionary[normalize(value)] || value; },
    get language() { return language; },
    sourceText(element) {
      if (!element) return '';
      const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
      let value = '';
      while (walker.nextNode()) value += texts.get(walker.currentNode)?.en || walker.currentNode.data;
      return normalize(value);
    },
    sourceAttribute(element, name) { return attributes.get(element)?.[name]?.en || element.getAttribute(name); }
  };

  // Set the correct font before first paint; bare URLs always use English.
  document.documentElement.lang = readLanguage() === 'zh' ? 'zh-CN' : 'en';
  if (readLanguage() === 'zh') loadLocale().catch(() => {});
  document.addEventListener('DOMContentLoaded', () => {
    ready = true;
    const slot = document.querySelector('[data-language-slot]');
    slot.removeAttribute('aria-hidden');
    slot.setAttribute('data-language-control', '');
    slot.setAttribute('role', 'group');
    slot.innerHTML = '<button type="button" lang="en" data-language-value="en" aria-pressed="true">EN</button><button type="button" lang="zh-CN" data-language-value="zh" aria-pressed="false">中文</button>';
    const status = document.createElement('span');
    status.className = 'language-status';
    status.setAttribute('data-language-status', '');
    status.setAttribute('data-i18n-keep', '');
    status.setAttribute('role', 'status');
    document.body.append(status);
    slot.querySelectorAll('button').forEach(button => button.addEventListener('click', () => {
      if (button.dataset.languageValue !== language) setLanguage(button.dataset.languageValue, {history: true});
    }));
    const desktop = matchMedia('(min-width: 1024px)');
    const themeButton = document.querySelector('.theme-toggle-btn');
    const home = document.createComment('Desktop language switch position');
    slot.before(home);
    const placeControl = () => {
      if (desktop.matches || !themeButton) home.after(slot);
      else themeButton.after(slot);
    };
    desktop.addEventListener('change', placeControl);
    placeControl();
    new MutationObserver(records => {
      if (language !== 'zh') return;
      const flows = new Set();
      records.forEach(record => {
        if (record.type === 'characterData') {
          // Ignore our own translation/spacing edits, retaining the English
          // source for switching back and avoiding a normalization loop.
          if (texts.get(record.target)?.last === record.target.data) return;
          visitText(record.target);
          if (record.target.parentElement) flows.add(flowRoot(record.target.parentElement));
        }
        else if (record.type === 'attributes') {
          visitAttributes(record.target);
          if (record.attributeName === 'href') visitLink(record.target);
        } else record.addedNodes.forEach(node => apply(node));
      });
      flows.forEach(formatChineseRuns);
    }).observe(document.documentElement, {subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: [...translatedAttributes, 'content', 'href']});
    setLanguage(readLanguage(), {preservePosition: false});
  });
  window.addEventListener('popstate', () => { if (ready) setLanguage(readLanguage(), {preservePosition: false}); });
})();
