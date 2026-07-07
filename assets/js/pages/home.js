import { Navigation, ScrollSpy } from '/assets/js/site.js';

new Navigation(document.getElementById('site-nav'), [
  { type: 'logo', href: '/', title: 'Astatyr', subtitle: 'Hub Page' },
  { icon: '🔍', label: 'Research', href: '#research', navId: 'research' },
  { icon: '🧑‍💻', label: 'Code Projects', href: '#code', navId: 'code' },
  { icon: '🧮', label: 'Engineering', href: '#engineering', navId: 'engineering' },
  { icon: '✍️', label: 'Writing', href: '#writing', navId: 'writing' },
  { type: 'divider' },
  { icon: '📫', label: 'Contact', href: '#contact', navId: 'contact' },
  { type: 'footer', text: '© 2025 Justin Adrian Halim' },
]).render();

new ScrollSpy({ threshold: 0.3 }).observeByNavId();
