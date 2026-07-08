/**
 * Cloudflare Pages Function — reverse-proxies /worldbuilding/* to the
 * separate `worldbuilding` GitHub repo, so it appears under this hub's own
 * domain instead of astatyr.github.io/worldbuilding. That repo already
 * builds its internal links relative to a /worldbuilding/ base (see its own
 * assets/js/base.js), so the path is forwarded unchanged — only the host
 * changes.
 *
 * Ships as part of this repo's Cloudflare Pages project: no separate
 * Workers Route needs to be configured by hand, it activates automatically
 * once the repo is connected to Pages.
 */

const WORLDBUILDING_ORIGIN = 'astatyr.github.io';

class GithubPagesProxy {
  constructor(originHost) {
    this.originHost = originHost;
  }

  async handle(request) {
    const url = new URL(request.url);

    // The worldbuilding repo's pages use relative fetch()/href calls (e.g.
    // fetch('generated/manifest.json')), which only resolve against
    // /worldbuilding/ if the browser's address bar actually ends in '/'.
    // Serving directory-style paths without redirecting first means those
    // relative calls silently resolve against the domain root instead.
    if (this._needsTrailingSlash(url.pathname)) {
      const redirectUrl = new URL(url);
      redirectUrl.pathname += '/';
      return Response.redirect(redirectUrl.toString(), 301);
    }

    const targetUrl = `https://${this.originHost}${url.pathname}${url.search}`;

    const originHeaders = new Headers(request.headers);
    originHeaders.delete('host');

    const originResponse = await fetch(targetUrl, {
      method: request.method,
      headers: originHeaders,
      redirect: 'manual',
    });

    return this._buildResponse(originResponse, url);
  }

  _needsTrailingSlash(pathname) {
    const lastSegment = pathname.split('/').pop();
    return !pathname.endsWith('/') && !lastSegment.includes('.');
  }

  _buildResponse(originResponse, requestUrl) {
    const headers = new Headers(originResponse.headers);

    // fetch() already transparently gunzips the origin response — the body
    // we're forwarding is plain bytes, but the original Content-Encoding
    // and Content-Length headers still describe the *compressed* version.
    // Forwarding them unchanged tells the browser to gunzip already-decoded
    // data, which fails silently inside fetch() (curl doesn't catch this —
    // it only decodes when asked, so `curl -I` looks fine either way).
    headers.delete('content-encoding');
    headers.delete('content-length');

    // Don't let a GitHub Pages redirect leak astatyr.github.io into the address bar
    const location = headers.get('location');
    if (location && location.includes(this.originHost)) {
      headers.set('location', location.replace(`https://${this.originHost}`, requestUrl.origin));
    }

    this._applyCacheHeaders(headers, requestUrl.pathname);
    this._applySecurityHeaders(headers);

    return new Response(originResponse.body, {
      status: originResponse.status,
      statusText: originResponse.statusText,
      headers,
    });
  }

  _applyCacheHeaders(headers, pathname) {
    if (pathname.startsWith('/worldbuilding/generated/manifest.json')) {
      headers.set('Cache-Control', 'no-cache');
    } else if (pathname.startsWith('/worldbuilding/generated/media/')) {
      headers.set('Cache-Control', 'public, max-age=2592000');
    } else if (pathname.startsWith('/worldbuilding/generated/')) {
      headers.set('Cache-Control', 'public, max-age=300');
    }
  }

  _applySecurityHeaders(headers) {
    headers.set('X-Content-Type-Options', 'nosniff');
    headers.set('X-Frame-Options', 'DENY');
    headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  }
}

export async function onRequest(context) {
  const proxy = new GithubPagesProxy(WORLDBUILDING_ORIGIN);
  return proxy.handle(context.request);
}
