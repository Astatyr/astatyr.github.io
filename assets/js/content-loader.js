/**
 * content-loader.js
 * Fetches generated HTML content fragments and handles error/loading states.
 * Also provides the base PageController class all page types extend.
 */

class ContentLoader {
  /**
   * Fetch a generated HTML fragment and inject it into a target element.
   * Shows a styled error box if the fetch fails or returns non-200.
   *
   * @param {string} url         URL of the generated HTML fragment
   * @param {string} targetId    ID of the element to inject into
   * @param {string} emptyMsg    Message to show if content is not found
   */
  static async load(url, targetId, emptyMsg = 'Content not found.') {
    const el = document.getElementById(targetId);
    if (!el) return;

    try {
      const res = await fetch(url);
      if (res.ok) {
        el.innerHTML = await res.text();
      } else {
        el.innerHTML = ContentLoader.#emptyNote(emptyMsg);
      }
    } catch (err) {
      el.innerHTML = ContentLoader.#errorBox(
        'Failed to load content',
        `Could not reach ${url}. Check your connection or try refreshing.`
      );
    }
  }

  // ── HTML helpers ──────────────────────────────────────────────────────────

  static #emptyNote(msg) {
    return `<p class="empty-note">${msg}</p>`;
  }

  static #errorBox(title, detail) {
    return `
      <div class="error-box">
        <div class="error-title">&#9888; ${title}</div>
        <div>${detail}</div>
      </div>`;
  }

  /** Show a visible error box in a target element. */
  static showError(targetId, title, detail = '') {
    const el = document.getElementById(targetId);
    if (el) el.innerHTML = ContentLoader.#errorBox(title, detail);
  }
}


/**
 * PageController — base class for all page type controllers.
 *
 * Subclasses override setup() to add their page-specific logic.
 * All manifest fetching, error handling, and loading state is handled here.
 */
class PageController {
  /**
   * Entry point. Call this once on page load.
   * Loads the manifest then calls setup().
   */
  async init() {
    try {
      const manifest = await ManifestStore.get();
      await this.setup(manifest);
    } catch (err) {
      this.onManifestError(err);
    }
  }

  /**
   * Override in subclasses with page-specific setup logic.
   * @param {Object} manifest The full manifest object.
   */
  async setup(manifest) {
    throw new Error('setup() must be implemented by subclass');
  }

  /**
   * Called when the manifest cannot be loaded.
   * Override to customise error handling.
   */
  onManifestError(err) {
    console.error('Manifest load failed:', err);
    ContentLoader.showError(
      'page-title',
      'Could not load page data',
      'The site manifest is unavailable. Try refreshing, or check back in a minute.'
    );
  }

  // ── URL parsing helpers ───────────────────────────────────────────────────

  /** Get URL path segments, stripping trailing slash. */
  get pathParts() {
    return window.location.pathname.replace(/\/$/, '').split('/');
  }

  /** Last path segment without .html extension. */
  get currentId() {
    return this.pathParts[this.pathParts.length - 1].replace('.html', '');
  }

  /** Second-to-last path segment (parent folder). */
  get parentId() {
    return this.pathParts[this.pathParts.length - 2];
  }
}
