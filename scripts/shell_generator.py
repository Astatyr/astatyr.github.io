"""
shell_generator.py — Generates all shell HTML pages in worldbuilding/.

Uses renderers to produce HTML and writes files to disk.
"""

import os
from renderers import (
    StorylineIndexRenderer,
    ChapterRenderer,
    CharacterRenderer,
    CharacterHubRenderer,
    LocationRenderer,
    CityRenderer,
)


def _detect_image_style(directory: str, basename: str) -> str:
    """Return an inline style string if a matching image is found, else ''."""
    for ext in ['jpg', 'jpeg', 'png', 'webp']:
        path = os.path.join(directory, f'{basename}.{ext}')
        if os.path.exists(path):
            url = f'/{directory}/{basename}.{ext}'
            return f' style="background-image: url({url})"'
    return ''


def write_page(path: str, html: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Written: {path}')


class ShellGenerator:
    """
    Takes the manifest dict and generates all shell pages.
    Overwrites existing pages so templates always stay fresh.
    """

    SHELL_ROOT = 'worldbuilding'

    def __init__(self, manifest: dict):
        self.manifest = manifest

    def run(self) -> None:
        print('\nGenerating shell pages...')
        self._gen_storylines()
        self._gen_characters()
        self._gen_geography()

    # ── storylines ────────────────────────────────────────────────────────────

    def _gen_storylines(self) -> None:
        for sl in self.manifest['storylines']:
            sl_dir = os.path.join(self.SHELL_ROOT, 'storylines', sl['id'])
            write_page(
                os.path.join(sl_dir, 'index.html'),
                StorylineIndexRenderer().render()
            )
            for ch in sl['chapters']:
                write_page(
                    os.path.join(sl_dir, f"{ch['id']}.html"),
                    ChapterRenderer().render()
                )

    # ── characters ────────────────────────────────────────────────────────────

    def _gen_characters(self) -> None:
        # Generate the character hub index page
        write_page(
            os.path.join(self.SHELL_ROOT, 'characters', 'index.html'),
            CharacterHubRenderer().render()
        )
        for char in self.manifest['characters']:
            portrait_style = _detect_image_style(
                'assets/images/characters', char['id']
            )
            write_page(
                os.path.join(self.SHELL_ROOT, 'characters', f"{char['id']}.html"),
                CharacterRenderer(portrait_style).render()
            )

    # ── geography ─────────────────────────────────────────────────────────────

    def _gen_geography(self) -> None:
        for geo in self.manifest['geography']:
            geo_dir = os.path.join(self.SHELL_ROOT, 'geography', geo['id'])
            banner_style = _detect_image_style(
                'assets/images/geography', geo['id']
            )
            write_page(
                os.path.join(geo_dir, 'index.html'),
                LocationRenderer(banner_style).render()
            )
            for loc in geo['locations']:
                city_banner = _detect_image_style(
                    'assets/images/geography', f"{geo['id']}-{loc['id']}"
                )
                write_page(
                    os.path.join(geo_dir, f"{loc['id']}.html"),
                    CityRenderer(city_banner).render()
                )
