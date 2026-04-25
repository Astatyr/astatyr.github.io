/**
 * character-hub-page.js
 * Controller for the character hub/wiki page.
 * Shows all characters in a compact searchable list.
 */

class CharacterHubPage extends PageController {
  async setup(manifest) {
    const characters = manifest.characters || [];

    NavBuilder.setSection('Characters');
    NavBuilder.setItems([
      { href: '/worldbuilding', label: '← Worldbuilding' },
    ]);

    const list = document.getElementById('char-list');
    const count = document.getElementById('char-count');

    if (!characters.length) {
      list.innerHTML = '<p class="empty-note">No characters yet.</p>';
      return;
    }

    // Render all rows
    list.innerHTML = characters.map(c => `
      <a class="char-row" href="/worldbuilding/characters/${c.id}.html"
         data-name="${c.title.toLowerCase()}"
         data-role="${(c.role || '').toLowerCase()}">
        <span class="char-dot${c.image ? ' has-portrait' : ''}"></span>
        <span class="char-row-name">${c.title}</span>
        <span class="char-row-role">${c.role || ''}</span>
      </a>`).join('');

    this._updateCount(characters.length, characters.length);

    // Expose filter function to the inline oninput handler
    window.filterChars = (query) => {
      const q = query.toLowerCase().trim();
      const rows = list.querySelectorAll('.char-row');
      let visible = 0;
      rows.forEach(row => {
        const match = !q
          || row.dataset.name.includes(q)
          || row.dataset.role.includes(q);
        row.classList.toggle('char-hidden', !match);
        if (match) visible++;
      });
      this._updateCount(visible, characters.length);
    };
  }

  _updateCount(visible, total) {
    const el = document.getElementById('char-count');
    if (el) el.textContent = visible === total
      ? `${total} character${total !== 1 ? 's' : ''}`
      : `${visible} of ${total} characters`;
  }
}
