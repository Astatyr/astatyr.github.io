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
    const targetUrl = this._resolveTargetUrl(url);

    const originHeaders = new Headers(request.headers);
    originHeaders.delete('host');

    const originResponse = await fetch(targetUrl, {
      method: request.method,
      headers: originHeaders,
      redirect: 'manual',
    });

    return this._buildResponse(originResponse, url);
  }

  _resolveTargetUrl(url) {
    let pathname = url.pathname;
    const lastSegment = pathname.split('/').pop();
    // GitHub Pages needs a trailing slash on directory-style paths to serve their index.html
    if (!pathname.endsWith('/') && !lastSegment.includes('.')) {
      pathname += '/';
    }
    return `https://${this.originHost}${pathname}${url.search}`;
  }

  _buildResponse(originResponse, requestUrl) {
    const headers = new Headers(originResponse.headers);

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
