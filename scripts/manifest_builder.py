"""
manifest_builder.py — Scans content/ folders and builds the manifest.json.
"""

import os
import json
from models import Storyline, Character, Geography


class ManifestBuilder:
    """
    Walks the content/ directory tree, instantiates content models,
    and writes generated/manifest.json.
    """

    CONTENT_ROOT = 'content'
    OUTPUT_PATH = 'generated/manifest.json'

    def __init__(self):
        self.manifest: dict = {
            'storylines': [],
            'characters': [],
            'geography': [],
        }

    def build(self) -> dict:
        """Scan all content, build manifest, write to disk. Returns manifest dict."""
        self._scan_storylines()
        self._scan_characters()
        self._scan_geography()
        self._write()
        return self.manifest

    # ── scanners ─────────────────────────────────────────────────────────────

    def _scan_storylines(self) -> None:
        root = os.path.join(self.CONTENT_ROOT, 'storylines')
        if not os.path.exists(root):
            return
        for name in sorted(os.listdir(root)):
            folder = os.path.join(root, name)
            if not os.path.isdir(folder):
                continue
            sl = Storyline(name, folder)
            self.manifest['storylines'].append(sl.to_dict())
            print(f'  Storyline: {sl.title} ({len(sl.chapters)} chapters)')

    def _scan_characters(self) -> None:
        root = os.path.join(self.CONTENT_ROOT, 'characters')
        if not os.path.exists(root):
            return
        for fname in sorted(os.listdir(root)):
            if not fname.endswith('.docx') or fname.startswith('_'):
                continue
            char = Character(fname[:-5], root)
            self.manifest['characters'].append(char.to_dict())
            image_note = f' [image: {char.image}]' if char.image else ''
            print(f'  Character: {char.title}{image_note}')

    def _scan_geography(self) -> None:
        root = os.path.join(self.CONTENT_ROOT, 'geography')
        if not os.path.exists(root):
            return
        for name in sorted(os.listdir(root)):
            folder = os.path.join(root, name)
            if not os.path.isdir(folder):
                continue
            geo = Geography(name, folder)
            self.manifest['geography'].append(geo.to_dict())
            image_note = f' [image: {geo.image}]' if geo.image else ''
            print(f'  Geography: {geo.title}{image_note} ({len(geo.locations)} locations)')

    # ── output ───────────────────────────────────────────────────────────────

    def _write(self) -> None:
        os.makedirs(os.path.dirname(self.OUTPUT_PATH), exist_ok=True)
        with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.manifest, f, indent=2)
        print(f'\nmanifest.json written → {self.OUTPUT_PATH}')
