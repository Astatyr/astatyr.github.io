"""
renderers.py — Page renderer classes.

Each renderer produces a complete HTML shell page string.
Shell pages are lightweight: they contain structure and JS includes only.
All data loading happens at runtime via the JS page controllers.
"""

from html_builder import HTMLBuilder

H = HTMLBuilder()

# JS asset paths — all pages load these
_JS_BASE = [
    '/assets/js/manifest-store.js',
    '/assets/js/nav-builder.js',
    '/assets/js/content-loader.js',
]


class PageRenderer:
    """Abstract base renderer."""

    def render(self) -> str:
        raise NotImplementedError

    def _shell(self, body_html: str, js_paths: list[str], init_call: str) -> str:
        """Assemble a complete page from parts."""
        js_tags = H.js_tags(*(_JS_BASE + js_paths))
        return (
            H.head()
            + '\n' + H.nav()
            + '\n' + body_html
            + '\n' + js_tags
            + f'\n  <script>{init_call}</script>'
            + H.foot()
        )


# ── storyline index ───────────────────────────────────────────────────────────

class StorylineIndexRenderer(PageRenderer):
    """Overview page for a storyline — lists chapters and shows index.docx content."""

    def render(self) -> str:
        body = """\
<main style="animation:fadeUp .4s ease both">
  <a class="back-link" href="/worldbuilding">&larr; Worldbuilding</a>
  <div class="page-title" id="page-title">Loading&hellip;</div>
  <div class="page-meta" id="page-meta"></div>
  <div class="page-desc" id="page-desc"></div>
  <div class="wb-section">
    <div class="section-label">Overview</div>
    <div id="overview-content" class="doc-content"><p class="loading">Loading&hellip;</p></div>
  </div>
  <div class="wb-section">
    <div class="section-label">Chapters</div>
    <div id="chapter-list" class="chapter-list"><p class="loading">Loading&hellip;</p></div>
  </div>
</main>"""
        return self._shell(body, ['/assets/js/storyline-page.js'], 'new StorylinePage().init();')


# ── chapter ───────────────────────────────────────────────────────────────────

class ChapterRenderer(PageRenderer):
    """Individual chapter page with prev/next navigation."""

    def render(self) -> str:
        body = """\
<main style="animation:fadeUp .4s ease both">
  <a class="back-link" href="/worldbuilding">&larr; Worldbuilding</a>
  <div id="ch-label" class="page-meta">Chapter</div>
  <div id="ch-title" class="page-title">Loading&hellip;</div>
  <div style="margin-top:2rem" id="ch-content" class="doc-content">
    <p class="loading">Loading&hellip;</p>
  </div>
  <div class="ch-nav" id="ch-nav"></div>
</main>"""
        return self._shell(body, ['/assets/js/chapter-page.js'], 'new ChapterPage().init();')


# ── character ─────────────────────────────────────────────────────────────────

class CharacterRenderer(PageRenderer):
    """Character profile page with portrait and content sections."""

    def __init__(self, portrait_style: str = ''):
        self.portrait_style = portrait_style

    def render(self) -> str:
        body = f"""\
<main style="animation:fadeUp .4s ease both">
  <a class="back-link" href="/worldbuilding">&larr; Worldbuilding</a>
  <div class="char-portrait" id="char-portrait"{self.portrait_style}></div>
  <div class="page-title" id="char-name">Loading&hellip;</div>
  <div class="page-meta" id="char-role-text"></div>
  <div class="wb-section" style="margin-top:2rem">
    <div class="section-label">About</div>
    <div id="char-content" class="doc-content"><p class="loading">Loading&hellip;</p></div>
  </div>
</main>"""
        return self._shell(body, ['/assets/js/character-page.js'], 'new CharacterPage().init();')


# ── location (country/region) ─────────────────────────────────────────────────

class LocationRenderer(PageRenderer):
    """Top-level geography page with banner image and cities grid."""

    def __init__(self, banner_style: str = ''):
        self.banner_style = banner_style

    def render(self) -> str:
        # Location pages use full-width layout — override main padding
        body = f"""\
<main style="padding:0;max-width:none;margin-left:var(--nav-w)">
  <div class="loc-banner"{self.banner_style}>
    <div class="loc-banner-overlay"></div>
    <div class="loc-banner-title">
      <div class="loc-type-label" id="loc-type">Location</div>
      <div style="font-family:'DM Serif Display',serif;font-size:2.2rem;letter-spacing:-.03em"
           id="loc-name">Loading&hellip;</div>
    </div>
  </div>
  <div class="content-area">
    <a class="back-link" href="/worldbuilding">&larr; Worldbuilding</a>
    <div class="wb-section">
      <div class="section-label">Overview</div>
      <div id="loc-content" class="doc-content"><p class="loading">Loading&hellip;</p></div>
    </div>
    <div class="wb-section" id="cities-section" style="display:none">
      <div class="section-label">Cities &amp; Locations</div>
      <div id="cities-grid" class="loc-grid"></div>
    </div>
  </div>
</main>"""
        return self._shell(body, ['/assets/js/location-page.js'], 'new LocationPage().init();')


# ── city ──────────────────────────────────────────────────────────────────────

class CityRenderer(PageRenderer):
    """City or sub-location page within a geography."""

    def __init__(self, banner_style: str = ''):
        self.banner_style = banner_style

    def render(self) -> str:
        body = f"""\
<main style="padding:0;max-width:none;margin-left:var(--nav-w)">
  <div class="loc-banner"{self.banner_style}>
    <div class="loc-banner-overlay"></div>
    <div class="loc-banner-title">
      <div class="loc-type-label" id="city-type">City</div>
      <div style="font-family:'DM Serif Display',serif;font-size:2.2rem;letter-spacing:-.03em"
           id="city-name">Loading&hellip;</div>
    </div>
  </div>
  <div class="content-area">
    <div class="breadcrumb" id="breadcrumb">
      <a href="/worldbuilding">Worldbuilding</a>
      <span class="sep">/</span>
      <a id="country-link" href="#">Country</a>
      <span class="sep">/</span>
      <span id="city-breadcrumb">City</span>
    </div>
    <div class="wb-section">
      <div class="section-label">Overview</div>
      <div id="city-content" class="doc-content"><p class="loading">Loading&hellip;</p></div>
    </div>
  </div>
</main>"""
        return self._shell(body, ['/assets/js/city-page.js'], 'new CityPage().init();')
