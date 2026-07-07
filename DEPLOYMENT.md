# Deployment notes

This repo is meant to be served by **Cloudflare Pages**, not GitHub Pages — the
`_headers` file and `functions/` directory only take effect on Cloudflare Pages.
GitHub Pages (astatyr.github.io) can stay as a fallback/preview but won't apply
either of those.

## Connecting the repo

1. Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git → select this repo.
2. Build settings: framework preset **None**, build command **empty**, output directory `/`.
   There's no build step — it's plain static HTML/CSS/JS plus one Pages Function.
3. Deploy. Cloudflare auto-detects `functions/worldbuilding/[[path]].js` and wires it up —
   no manual Workers Route needed.
4. Add a custom domain under the Pages project's **Custom domains** tab once you're ready
   (currently planned: `astatyr.com`, but nothing in this repo hardcodes that — every
   internal link is root-relative, so the domain can change freely later).

## How /worldbuilding routing works

The `worldbuilding` content lives in a **separate repo** (`Astatyr/worldbuilding`),
deployed via plain GitHub Pages at `astatyr.github.io/worldbuilding/`. That repo
already builds all of its internal links relative to a `/worldbuilding/` base
(see its own `assets/js/base.js`), so `functions/worldbuilding/[[path]].js` here
proxies the path unchanged — swaps only the hostname — and it resolves correctly.

If the `worldbuilding` repo's hosting ever moves, update the single
`WORLDBUILDING_ORIGIN` constant at the top of that function file — nothing else
needs to change.

**Known gap:** proxied `/worldbuilding/*` responses only get three baseline
headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`) — no CSP.
That's intentional for now: the `worldbuilding` repo's pages still use inline
`<script>` blocks, and a strict `script-src` would break them. If that repo gets
the same inline-script-to-module refactor this one just got, CSP can be added
to the proxy function too.

## Local preview

Plain static pages (no Function involved) — any static server works:

```
python -m http.server 8000
```

Then open `http://localhost:8000/`. Note: opening `index.html` directly via
`file://` won't work — `<script type="module">` imports are blocked under that
protocol, it needs a real (even local) HTTP server.

To also exercise the Pages Functions (`/worldbuilding` proxy, `/api/poems`) and
the `_headers` rules exactly as Cloudflare would apply them, use Wrangler
instead (requires Node.js):

```
npx wrangler pages dev . --port 8788
```

Then open `http://localhost:8788/`. This is what was used to verify this pass —
including catching and fixing the CSP bug described below.

## Cloudflare dashboard checklist (manual, one-time)

These aren't things a file in this repo can configure — set them after connecting:

- **SSL/TLS mode**: Full (Strict).
- **Edge Certificates → Always Use HTTPS**: on.
- **Edge Certificates → HSTS**: on, start with a short max-age (e.g. a few days) before
  committing to a long one or preload — HSTS mistakes are hard to walk back quickly.
- **Edge Certificates → Minimum TLS Version**: 1.2.
- **Security → Bot Fight Mode**: on (free tier is fine for a personal site).

## CSP gotcha found while testing (already fixed, worth knowing about)

Cloudflare Pages merges `_headers` rules from every path pattern that matches a
request rather than letting a more specific rule override a general one. Two
`Content-Security-Policy` values on overlapping paths get sent together and
enforced as an intersection — the stricter one always wins, regardless of
which was "meant" to apply. This is why `poetry.html` no longer fetches
`script.google.com` directly from the browser: it now goes through
`functions/api/poems.js`, a same-origin Function that calls the Apps Script
endpoint server-side. That keeps a single strict CSP (`connect-src 'self'`)
everywhere with zero per-path exceptions — if a future page needs to reach a
third-party API, route it through a Function the same way rather than adding
another `_headers` carve-out.

As a side benefit, the Apps Script URL itself is no longer present in any
client-side source — it's still worth confirming on your end that the Apps
Script deployment is **read-only** (no write/edit endpoints exposed under
"Anyone" access), but it's no longer discoverable by just viewing page source.
