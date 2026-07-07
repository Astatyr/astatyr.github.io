/**
 * Same-origin proxy for the poems feed. poetry.html used to fetch
 * script.google.com directly from the browser, which meant the CSP needed a
 * connect-src carve-out just for that page — except Cloudflare Pages merges
 * _headers rules across every matching path rather than letting a more
 * specific one win, so two Content-Security-Policy values were being sent
 * and enforced together, and the stricter one (connect-src 'self') silently
 * won anyway. Proxying server-side keeps one strict CSP everywhere.
 */

const POEMS_SOURCE_URL = "https://script.google.com/macros/s/AKfycbzMYvRisnvBiKK3DeKPqZ-NPkb7F7vnJD4OJbPPfpKAqjR_rycPlJ2qrpE-QbfyjJBa/exec";

class PoemsSource {
  constructor(url) {
    this.url = url;
  }

  async fetchJSON() {
    const res = await fetch(this.url);
    if (!res.ok) throw new Error(`upstream HTTP ${res.status}`);
    return res.json();
  }
}

export async function onRequestGet() {
  try {
    const data = await new PoemsSource(POEMS_SOURCE_URL).fetchJSON();
    return new Response(JSON.stringify(data), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=60',
      },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 502,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
