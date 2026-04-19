/**
 * manifest-store.js
 * Singleton that fetches and caches manifest.json for the browser session.
 * Uses sessionStorage so navigation between pages never re-fetches.
 */

class ManifestStore {
  static #CACHE_KEY = 'astatyr_manifest';
  static #MANIFEST_URL = '/generated/manifest.json';

  /**
   * Get the manifest. Fetches once per session, then serves from cache.
   * @returns {Promise<Object>} The manifest object.
   * @throws {Error} If the manifest cannot be fetched.
   */
  static async get() {
    const cached = sessionStorage.getItem(this.#CACHE_KEY);
    if (cached) {
      try {
        return JSON.parse(cached);
      } catch {
        sessionStorage.removeItem(this.#CACHE_KEY);
      }
    }

    const res = await fetch(this.#MANIFEST_URL);
    if (!res.ok) throw new Error(`Manifest fetch failed: HTTP ${res.status}`);
    const data = await res.json();
    sessionStorage.setItem(this.#CACHE_KEY, JSON.stringify(data));
    return data;
  }

  /** Force a fresh fetch on the next get() call (e.g. after a push). */
  static invalidate() {
    sessionStorage.removeItem(this.#CACHE_KEY);
  }
}
