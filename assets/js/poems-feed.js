import { ScrollSpy } from '/assets/js/site.js';

export class PoemsFeed {
  constructor({ scriptUrl, container, navSlot, loadingEl, errorEl, errorDetailEl }) {
    this.scriptUrl = scriptUrl;
    this.container = container;
    this.navSlot = navSlot;
    this.loadingEl = loadingEl;
    this.errorEl = errorEl;
    this.errorDetailEl = errorDetailEl;
    this.scrollSpy = new ScrollSpy({ threshold: 0.5 });
  }

  async load() {
    try {
      const res = await fetch(this.scriptUrl);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      this.loadingEl.style.display = 'none';

      if (!data.poems || data.poems.length === 0) {
        this._showError('No poems found. Check your Google Doc has named tabs.');
        return;
      }

      this._render(data.poems);
    } catch (err) {
      this._showError(err.message);
    }
  }

  _render(poems) {
    this.container.style.display = 'flex';

    poems.forEach((poem, i) => {
      const navBtn = document.createElement('a');
      navBtn.className = 'nav-btn nav-sub-btn';
      navBtn.href = `#poem-${i}`;
      navBtn.textContent = poem.title;
      this.navSlot.appendChild(navBtn);

      const article = this._buildArticle(poem, i);
      this.container.appendChild(article);

      this.scrollSpy.observe(article, navBtn);
    });
  }

  _buildArticle(poem, i) {
    const stanzas = this._splitStanzas(poem.lines);
    const stanzaHTML = stanzas
      .map(s => `<div class="stanza">${s.map(l => `<div>${l}</div>`).join('')}</div>`)
      .join('');

    const el = document.createElement('article');
    el.className = 'poem';
    el.id = `poem-${i}`;
    el.style.animationDelay = `${i * 0.1}s`;
    el.innerHTML = `
      <div class="poem-number">— ${String(i + 1).padStart(2, '0')}</div>
      <h2>${poem.title}</h2>
      ${poem.date ? `<div class="poem-date">${poem.date}</div>` : ''}
      <div class="poem-body">${stanzaHTML}</div>
    `;
    return el;
  }

  _splitStanzas(lines) {
    const stanzas = [];
    let current = [];
    for (const line of lines) {
      if (line === null) {
        if (current.length) { stanzas.push(current); current = []; }
      } else {
        current.push(line);
      }
    }
    if (current.length) stanzas.push(current);
    return stanzas;
  }

  _showError(msg) {
    this.loadingEl.style.display = 'none';
    this.errorEl.style.display = 'block';
    this.errorDetailEl.textContent = msg;
  }
}
