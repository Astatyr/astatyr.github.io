/**
 * Shared sidebar navigation + scroll-spy, used by every page on the hub.
 * Each page builds its own nav config and mounts these against its own DOM —
 * markup for the sidebar itself is never duplicated across pages.
 */

export class Navigation {
  constructor(root, items) {
    this.root = root;
    this.items = items;
  }

  render() {
    this.root.innerHTML = '';
    for (const item of this.items) {
      this.root.appendChild(this._buildItem(item));
    }
    return this;
  }

  _buildItem(item) {
    switch (item.type) {
      case 'logo': {
        const a = document.createElement('a');
        a.className = 'nav-logo';
        a.href = item.href;
        a.innerHTML = `${item.title}<span>${item.subtitle}</span>`;
        return a;
      }
      case 'divider': {
        const div = document.createElement('div');
        div.className = 'nav-divider';
        return div;
      }
      case 'label': {
        const div = document.createElement('div');
        div.className = 'nav-section-label';
        div.textContent = item.text;
        return div;
      }
      case 'footer': {
        const div = document.createElement('div');
        div.className = 'nav-footer';
        div.textContent = item.text;
        if (item.linkText && item.linkHref) {
          div.append(' · ');
          const a = document.createElement('a');
          a.href = item.linkHref;
          a.target = '_blank';
          a.rel = 'license noopener';
          a.textContent = item.linkText;
          div.appendChild(a);
        }
        return div;
      }
      case 'slot': {
        // Empty container a page can look up by id and fill in later
        // (e.g. poem links added once fetched content resolves).
        const div = document.createElement('div');
        div.id = item.id;
        return div;
      }
      default: {
        const a = document.createElement('a');
        a.className = 'nav-btn' + (item.sub ? ' nav-sub-btn' : '');
        a.href = item.href;
        a.innerHTML = item.icon ? `<span class="icon">${item.icon}</span> ${item.label}` : item.label;
        if (item.navId) a.dataset.navId = item.navId;
        return a;
      }
    }
  }
}

export class ScrollSpy {
  constructor({ threshold = 0.3 } = {}) {
    this.pairs = [];
    this.observer = new IntersectionObserver(this._onIntersect.bind(this), { threshold });
  }

  observe(sectionEl, linkEl) {
    if (!sectionEl || !linkEl) return this;
    this.pairs.push({ sectionEl, linkEl });
    this.observer.observe(sectionEl);
    return this;
  }

  observeByNavId(root = document) {
    root.querySelectorAll('[id]').forEach(sectionEl => {
      const linkEl = document.querySelector(`[data-nav-id="${sectionEl.id}"]`);
      if (linkEl) this.observe(sectionEl, linkEl);
    });
    return this;
  }

  _onIntersect(entries) {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const pair = this.pairs.find(p => p.sectionEl === entry.target);
      if (!pair) return;
      this.pairs.forEach(p => p.linkEl.classList.remove('active'));
      pair.linkEl.classList.add('active');
    });
  }
}
