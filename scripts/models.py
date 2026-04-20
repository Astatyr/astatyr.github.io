"""
models.py — Data models for all worldbuilding content types.

Each class knows how to:
  - Detect its own image from assets/
  - Read its optional _meta.txt
  - Serialize itself to a manifest dict
"""

import os


# ── helpers ───────────────────────────────────────────────────────────────────

def to_title(s: str) -> str:
    """Convert kebab-case or snake_case to Title Case words."""
    return s.replace('-', ' ').replace('_', ' ')


def read_meta(folder: str) -> dict:
    """
    Read optional _meta.txt from a content folder.
    Format: one 'key: value' per line.
    """
    meta = {}
    path = os.path.join(folder, '_meta.txt')
    if os.path.exists(path):
        for line in open(path, encoding='utf-8'):
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip()
    return meta


def detect_image(directory: str, basename: str) -> str:
    """
    Look for an image matching basename in directory.
    Returns the public URL path, or empty string if not found.
    """
    for ext in ['jpg', 'jpeg', 'png', 'webp']:
        path = os.path.join(directory, f'{basename}.{ext}')
        if os.path.exists(path):
            return f'/{directory}/{basename}.{ext}'
    return ''


# ── base class ────────────────────────────────────────────────────────────────

class ContentItem:
    """Base class for all content types."""

    IMAGE_DIR = ''  # override in subclasses

    def __init__(self, item_id: str):
        self.id = item_id
        self.title = to_title(item_id)
        self.image = ''

    def detect_image(self) -> None:
        if self.IMAGE_DIR:
            self.image = detect_image(self.IMAGE_DIR, self.id)

    def to_dict(self) -> dict:
        raise NotImplementedError


# ── storyline ─────────────────────────────────────────────────────────────────

class Chapter:
    """A single chapter within a storyline."""

    def __init__(self, chapter_id: str):
        self.id = chapter_id
        self.title = self._extract_title(chapter_id)

    @staticmethod
    def _extract_title(chapter_id: str) -> str:
        """
        Extract a clean title from the chapter filename id.
        'Chapter_1-The-Hevrion-Opening' → 'The Hevrion Opening'
        'Chapter_1'                     → 'Chapter 1' (fallback)
        """
        import re
        cleaned = re.sub(r'^Chapter_\d+[-_]', '', chapter_id, flags=re.IGNORECASE)
        if cleaned == chapter_id:
            return to_title(chapter_id)
        return cleaned.replace('-', ' ').replace('_', ' ')

    def to_dict(self) -> dict:
        return {'id': self.id, 'title': self.title}


class Storyline(ContentItem):
    """A campaign, short story, or other narrative arc."""

    def __init__(self, item_id: str, folder: str):
        super().__init__(item_id)
        meta = read_meta(folder)
        self.title = meta.get('title', to_title(item_id))
        self.type = meta.get('type', 'Storyline')
        self.status = meta.get('status', 'In Progress')
        self.description = meta.get('description', '')
        self.chapters: list[Chapter] = []
        self._scan_chapters(folder)

    def _scan_chapters(self, folder: str) -> None:
        for fname in sorted(os.listdir(folder)):
            if (fname.endswith('.docx')
                    and fname.lower() != 'index.docx'
                    and not fname.startswith('_')
                    and not fname.startswith('~$')):
                self.chapters.append(Chapter(fname[:-5]))

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'status': self.status,
            'description': self.description,
            'chapters': [c.to_dict() for c in self.chapters],
        }


# ── character ─────────────────────────────────────────────────────────────────

class Character(ContentItem):
    """A named character with optional portrait image."""

    IMAGE_DIR = 'assets/images/characters'

    def __init__(self, item_id: str, folder: str):
        super().__init__(item_id)
        # Characters can have an optional _<id>_meta.txt
        meta_path = os.path.join(folder, f'_{item_id}_meta.txt')
        meta = {}
        if os.path.exists(meta_path):
            for line in open(meta_path, encoding='utf-8'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip()] = v.strip()
        self.title = meta.get('title', to_title(item_id))
        self.role = meta.get('role', '')
        self.detect_image()

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'role': self.role,
            'image': self.image,
        }


# ── geography ─────────────────────────────────────────────────────────────────

class CityLocation:
    """A city or sub-location within a geography."""

    IMAGE_DIR = 'assets/images/geography'

    def __init__(self, loc_id: str, geo_id: str):
        self.id = loc_id
        self.title = to_title(loc_id)
        self.geo_id = geo_id
        # City images are named <geo_id>-<city_id>
        self.image = detect_image(self.IMAGE_DIR, f'{geo_id}-{loc_id}')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'image': self.image,
        }


class Geography(ContentItem):
    """A country, region, or top-level location."""

    IMAGE_DIR = 'assets/images/geography'

    def __init__(self, item_id: str, folder: str):
        super().__init__(item_id)
        meta = read_meta(folder)
        self.title = meta.get('title', to_title(item_id))
        self.type = meta.get('type', 'Location')
        self.description = meta.get('description', '')
        self.locations: list[CityLocation] = []
        self.detect_image()
        self._scan_locations(folder)

    def _scan_locations(self, folder: str) -> None:
        for fname in sorted(os.listdir(folder)):
            if (fname.endswith('.docx')
                    and fname.lower() != 'index.docx'
                    and not fname.startswith('_')
                    and not fname.startswith('~$')):
                self.locations.append(CityLocation(fname[:-5], self.id))

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'description': self.description,
            'image': self.image,
            'locations': [loc.to_dict() for loc in self.locations],
        }
