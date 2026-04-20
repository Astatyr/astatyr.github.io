/**
 * manifest-store.js
 * Singleton that fetches and caches manifest.json for the browser session.
 *
 * Uses a two-key strategy:
 *   - astatyr_manifest_etag  — stores the Last-Modified header from the last fetch
 *   - astatyr_manifest       — stores the cached manifest JSON
 *
 * On each get(), it sends a HEAD request to check if the manifest has changed.
 * If unchanged, serves from cache. If changed, fetches fresh and updates cache.
 * This means one tiny HEAD request per page load instead of downloading the
 * full manifest every time, while still always serving fresh data.
 */

class ManifestStore {
  static #URL        = '/generated/manifest.json';
  static #KEY_DATA   = 'astatyr_manifest';
  static #KEY_ETAG   = 'astatyr_manifest_etag';

  static async get() {
    try {
      // Check if the manifest has changed since we last cached it
      const head = await fetch(this.#URL, { method: 'HEAD' });
      const etag = head.headers.get('Last-Modified') || head.headers.get('ETag') || '';
      const cachedEtag = sessionStorage.getItem(this.#KEY_ETAG);
      const cachedData = sessionStorage.getItem(this.#KEY_DATA);

      if (etag && etag === cachedEtag && cachedData) {
        // Manifest unchanged — serve from cache
        return JSON.parse(cachedData);
      }

      // Manifest changed or not cached — fetch fresh
      const res  = await fetch(this.#URL);
      if (!res.ok) throw new Error(`Manifest fetch failed: HTTP ${res.status}`);
      const data = await res.json();

      sessionStorage.setItem(this.#KEY_DATA, JSON.stringify(data));
      sessionStorage.setItem(this.#KEY_ETAG, etag);
      return data;

    } catch (err) {
      // Network error — try serving stale cache rather than failing completely
      const stale = sessionStorage.getItem(this.#KEY_DATA);
      if (stale) {
        console.warn('ManifestStore: network error, serving stale cache.', err);
        return JSON.parse(stale);
      }
      throw err;
    }
  }

  /** Force a fresh fetch on the next get() call. */
  static invalidate() {
    sessionStorage.removeItem(this.#KEY_DATA);
    sessionStorage.removeItem(this.#KEY_ETAG);
  }
}
