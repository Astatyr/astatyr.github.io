"""
post_processor.py — Post-processes generated HTML files after pandoc conversion.

Handles:
  1. Converting === / ### / ## text markers to proper HTML headings
  2. Fixing image src paths so they work from any URL depth
"""

import os
import re


class PostProcessor:
    """Processes all HTML files in the generated/ folder."""

    GENERATED_ROOT = 'generated'
    SKIP_DIRS = {'media'}

    def run(self) -> None:
        print('\nPost-processing generated HTML...')
        count = 0
        for root, dirs, files in os.walk(self.GENERATED_ROOT):
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]
            for fname in files:
                if not fname.endswith('.html'):
                    continue
                path = os.path.join(root, fname)
                original = open(path, encoding='utf-8').read()
                processed = self._process(original)
                if processed != original:
                    open(path, 'w', encoding='utf-8').write(processed)
                    count += 1
        print(f'  Post-processed {count} file(s).')

    # ── processing pipeline ───────────────────────────────────────────────────

    def _process(self, html: str) -> str:
        html = self._convert_headings(html)
        html = self._convert_bullets(html)
        html = self._fix_image_paths(html)
        return html

    # ── heading conversion ────────────────────────────────────────────────────

    # Convention (type in Word as plain text):
    #   === Title   →  <h2> (section divider with extending line)
    #   ### Title   →  <h3> (serif subheading)
    #   ## Title    →  <h1> (large serif document heading)

    _HEADING_PATTERNS = [
        # === — may have optional <strong> or <em> wrapper around the text
        (re.compile(r'<p>===\s+(?:<[^>]+>)?(.*?)(?:</[^>]+>)?</p>'),
         lambda m: f'<h2><span>{m.group(1)}</span></h2>'),
        (re.compile(r'<p>###\s+(?:<[^>]+>)?(.*?)(?:</[^>]+>)?</p>'),
         lambda m: f'<h3>{m.group(1)}</h3>'),
        (re.compile(r'<p>##\s+(?:<[^>]+>)?(.*?)(?:</[^>]+>)?</p>'),
         lambda m: f'<h1>{m.group(1)}</h1>'),
    ]

    # Bullet list patterns
    # Groups consecutive "- item" paragraphs into a single <ul>
    _BULLET_PATTERN = re.compile(
        r'(?:<p>- (?:<[^>]+>)?(.*?)(?:</[^>]+>)?</p>\n?)+',
        re.DOTALL
    )
    _BULLET_ITEM = re.compile(r'<p>- (?:<[^>]+>)?(.*?)(?:</[^>]+>)?</p>')

    def _convert_headings(self, html: str) -> str:
        for pattern, replacement in self._HEADING_PATTERNS:
            html = pattern.sub(replacement, html)
        return html

    # ── bullet list conversion ───────────────────────────────────────────────

    def _convert_bullets(self, html: str) -> str:
        """
        Convert consecutive <p>- item</p> lines into a proper <ul> list.
        Handles optional bold/italic wrappers around the text.
        """
        def make_list(match):
            block = match.group(0)
            items = self._BULLET_ITEM.findall(block)
            lis = ''.join(f'<li>{item}</li>' for item in items)
            return f'<ul>{lis}</ul>'

        return self._BULLET_PATTERN.sub(make_list, html)

    # ── image path fixing ─────────────────────────────────────────────────────

    _IMG_PATTERNS = [
        # Pandoc sometimes writes relative paths like ../../generated/media/
        (re.compile(r'src="(?:\.\.\/)*generated\/media\/'), 'src="/generated/media/'),
        # Or just media/ relative to the file
        (re.compile(r'src="media\/'), 'src="/generated/media/'),
    ]

    def _fix_image_paths(self, html: str) -> str:
        for pattern, replacement in self._IMG_PATTERNS:
            html = pattern.sub(replacement, html)
        return html
