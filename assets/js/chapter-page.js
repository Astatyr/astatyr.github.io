/**
 * chapter-page.js
 * Controller for individual chapter pages.
 * Handles title, prev/next navigation, and content loading.
 */

class ChapterPage extends PageController {
  async setup(manifest) {
    const chId = this.currentId;
    const slId = this.parentId;

    const sl = manifest.storylines.find(s => s.id === slId);
    if (!sl) {
      ContentLoader.showError(
        'ch-title',
        'Storyline not found',
        `Could not find storyline "${slId}" in the manifest.`
      );
      return;
    }

    document.title = `${sl.title} \u2014 Astatyr`;
    NavBuilder.forStoryline(sl, chId);

    const chIdx = sl.chapters.findIndex(c => c.id === chId);
    const ch = sl.chapters[chIdx];

    if (!ch) {
      ContentLoader.showError(
        'ch-title',
        'Chapter not found',
        `Chapter "${chId}" does not exist in this storyline.`
      );
      return;
    }

    // Chapter heading
    document.getElementById('ch-label').textContent = `Chapter ${chIdx + 1}`;
    document.getElementById('ch-title').textContent = ch.title;

    // Prev / Next navigation
    const prev = chIdx > 0 ? sl.chapters[chIdx - 1] : null;
    const next = chIdx < sl.chapters.length - 1 ? sl.chapters[chIdx + 1] : null;
    document.getElementById('ch-nav').innerHTML =
      (prev
        ? `<a href="${prev.id}.html">
             <span class="dir">&larr; Previous</span>
             <span class="ch-title">${prev.title}</span>
           </a>`
        : '<span></span>') +
      (next
        ? `<a class="next" href="${next.id}.html">
             <span class="dir">Next &rarr;</span>
             <span class="ch-title">${next.title}</span>
           </a>`
        : '<span></span>');

    // Chapter content
    await ContentLoader.load(
      `/generated/storylines/${slId}/${chId}.html`,
      'ch-content',
      `Content not found — push ${chId}.docx to content/storylines/${slId}/ and wait for the Action.`
    );
  }
}
