import { Navigation } from '/assets/js/site.js';
import { PoemsFeed } from '/assets/js/poems-feed.js';

new Navigation(document.getElementById('site-nav'), [
  { type: 'logo', href: '/', title: 'Astatyr', subtitle: 'Hub Page' },
  { icon: '🔍', label: 'Research', href: '/#research' },
  { icon: '🧑‍💻', label: 'Code Projects', href: '/#code' },
  { icon: '🧮', label: 'Engineering', href: '/#engineering' },
  { icon: '✍️', label: 'Writing', href: '/#writing' },
  { type: 'divider' },
  { type: 'label', text: 'Poems' },
  { type: 'slot', id: 'nav-poems' },
  { type: 'divider' },
  { icon: '📫', label: 'Contact', href: '/#contact' },
  { type: 'footer', text: '© 2025 Justin Adrian Halim' },
]).render();

// Fetched through /api/poems (see functions/api/poems.js) — that Function
// calls the Google Apps Script endpoint server-side, so the browser never
// needs a CSP carve-out to talk to a third-party origin.
new PoemsFeed({
  scriptUrl: '/api/poems',
  container: document.getElementById('poems-container'),
  navSlot: document.getElementById('nav-poems'),
  loadingEl: document.getElementById('state-loading'),
  errorEl: document.getElementById('state-error'),
  errorDetailEl: document.getElementById('error-detail'),
}).load();
