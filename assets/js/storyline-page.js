/**
 * storyline-page.js
 * Controller for the storyline overview/index page.
 * Shows storyline metadata, chapter list, and index.docx content.
 */

class StorylinePage extends PageController {
  async setup(manifest) {
    const slId = this.currentId === 'index' ? this.parentId : this.currentId;
    const sl = manifest.storylines.find(s => s.id === slId);

    if (!sl) {
      document.getElementById('page-title').textContent =
        slId.replace(/[-_]/g, ' ');
      ContentLoader.showError(
        'overview-content',
        'Storyline not found',
        `No storyline with id "${slId}" exists in the manifest.`
      );
      return;
    }

    // Page metadata
    document.title = `${sl.title} \u2014 Astatyr`;
    document.getElementById('page-title').textContent = sl.title;
    document.getElementById('page-meta').textContent =
      [sl.type, sl.status].filter(Boolean).join(' \u00b7 ');
    document.getElementById('page-desc').textContent = sl.description || '';

    // Sidebar
    NavBuilder.forStoryline(sl, 'index');

    // Chapter list
    const cl = document.getElementById('chapter-list');
    if (!sl.chapters.length) {
      cl.innerHTML = `<p class="empty-note">No chapters yet — add .docx files to content/storylines/${slId}/</p>`;
    } else {
      cl.innerHTML = sl.chapters.map((ch, i) => `
        <a class="chapter-link" href="${ch.id}.html">
          <span class="ch-num">Chapter ${i + 1}</span>
          <span class="ch-title">${ch.title}</span>
          <span>&rarr;</span>
        </a>`).join('');
    }

    // Overview content from index.docx
    await ContentLoader.load(
      `/generated/storylines/${slId}/index.html`,
      'overview-content',
      `Add index.docx to content/storylines/${slId}/ to show an overview here.`
    );
  }
}
