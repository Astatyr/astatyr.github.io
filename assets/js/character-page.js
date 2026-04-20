/**
 * character-page.js
 * Controller for character profile pages.
 * Sets name, role, sidebar, and loads character content.
 */

class CharacterPage extends PageController {
  async setup(manifest) {
    const charId = decodeURIComponent(this.currentId);
    const char = manifest.characters.find(c => c.id === charId);

    if (!char) {
      ContentLoader.showError(
        'char-name',
        'Character not found',
        `No character with id "${charId}" exists in the manifest.`
      );
      return;
    }

    // Page metadata
    document.title = `${char.title} \u2014 Astatyr`;
    document.getElementById('char-name').textContent = char.title;
    document.getElementById('char-role-text').textContent = char.role || '';

    // Sidebar
    NavBuilder.forCharacters(manifest.characters, charId);

    // Character content
    await ContentLoader.load(
      `/generated/characters/${charId}.html`,
      'char-content',
      `Content not found — push ${charId}.docx to content/characters/ and wait for the Action.`
    );
  }
}
