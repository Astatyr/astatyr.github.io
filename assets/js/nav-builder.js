/**
 * nav-builder.js
 * Builds sidebar navigation HTML for all page types.
 * Keeps nav logic in one place — change here and every page updates.
 */

class NavBuilder {
  /**
   * Set the section label text in the sidebar.
   * @param {string} text
   */
  static setSection(text) {
    const el = document.getElementById('nav-section-title');
    if (el) el.textContent = text;
  }

  /**
   * Render a list of nav items into #nav-items.
   * @param {Array<{href: string, label: string, active?: boolean}>} items
   */
  static setItems(items) {
    const el = document.getElementById('nav-items');
    if (!el) return;
    el.innerHTML = items.map(({ href, label, active = false }) =>
      `<a class="nav-btn nav-sub-btn${active ? ' active' : ''}" href="${href}">${label}</a>`
    ).join('');
  }

  // ── convenience builders for each page type ──────────────────────────────

  /** Storyline index: Overview + chapter links. */
  static forStoryline(storyline, activeId = 'index') {
    this.setSection(storyline.title);
    const items = [
      { href: 'index.html', label: 'Overview', active: activeId === 'index' },
      ...storyline.chapters.map((ch, i) => ({
        href: `${ch.id}.html`,
        label: `Ch.${i + 1} \u2014 ${ch.title}`,
        active: ch.id === activeId,
      })),
    ];
    this.setItems(items);
  }

  /** Characters: list of all characters with current one active. */
  static forCharacters(characters, activeId) {
    this.setSection('Characters');
    this.setItems(characters.map(c => ({
      href: `${c.id}.html`,
      label: c.title,
      active: c.id === activeId,
    })));
  }

  /** Geography: list of all countries with current one active. */
  static forGeography(geography, activeId) {
    this.setSection('Geography');
    this.setItems(geography.map(g => ({
      href: `/worldbuilding/geography/${g.id}/`,
      label: g.title,
      active: g.id === activeId,
    })));
  }

  /** City: parent country overview + sibling cities. */
  static forCity(geo, activeCityId) {
    this.setSection(geo.title);
    const items = [
      { href: `/worldbuilding/geography/${geo.id}/`, label: 'Overview' },
      ...geo.locations.map(loc => ({
        href: `${loc.id}.html`,
        label: loc.title,
        active: loc.id === activeCityId,
      })),
    ];
    this.setItems(items);
  }
}
