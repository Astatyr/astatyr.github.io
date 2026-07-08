import { Navigation, ScrollSpy } from '/assets/js/site.js';

new Navigation(document.getElementById('site-nav'), [
  { type: 'logo', href: '/', title: 'Astatyr', subtitle: 'Hub Page' },
  { icon: '🔍', label: 'Research', href: '#research', navId: 'research' },
  { icon: '🧑‍💻', label: 'Code Projects', href: '#code', navId: 'code' },
  { icon: '🧮', label: 'Engineering', href: '#engineering', navId: 'engineering' },
  { icon: '✍️', label: 'Writing', href: '#writing', navId: 'writing' },
  { type: 'divider' },
  { icon: '📫', label: 'Contact', href: '#contact', navId: 'contact' },
  { type: 'footer', text: '© 2026 Astatyr', linkText: 'CC BY-NC-ND 4.0', linkHref: 'https://creativecommons.org/licenses/by-nc-nd/4.0/' },
]).render();

new ScrollSpy({ threshold: 0.3 }).observeByNavId();
