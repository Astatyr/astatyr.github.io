"""
html_builder.py — Shared HTML fragments used by all page renderers.
"""

from css_provider import FONTS, CSS


class HTMLBuilder:
    """Produces shared HEAD, NAV, and FOOT HTML strings."""

    SITE_TITLE = 'Astatyr'
    FOOTER_TEXT = '&copy; 2025 Justin Adrian Halim'

    @staticmethod
    def head(page_title: str = 'Astatyr') -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{page_title}</title>
  {FONTS}
  <style>{CSS}</style>
</head>
<body>"""

    @staticmethod
    def nav() -> str:
        return """\
<nav>
  <a class="nav-logo" href="/">Astatyr<span>Hub Page</span></a>
  <a class="nav-btn" href="/worldbuilding">&#127758; Worldbuilding</a>
  <div class="nav-divider"></div>
  <div class="nav-section-label" id="nav-section-title">Loading...</div>
  <div id="nav-items"></div>
  <div class="nav-footer">&copy; 2025 Justin Adrian Halim</div>
</nav>"""

    @staticmethod
    def foot() -> str:
        return '\n</body>\n</html>'

    @staticmethod
    def js_tags(*script_paths: str) -> str:
        """Generate <script src="..."> tags for given asset paths."""
        return '\n'.join(
            f'  <script src="{p}"></script>' for p in script_paths
        )
