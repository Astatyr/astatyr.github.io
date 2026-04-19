"""
generate.py — Entry point for the worldbuilding site generator.

Run by the GitHub Actions workflow after pandoc converts .docx to HTML.

Pipeline:
  1. ManifestBuilder  — scan content/, write generated/manifest.json
  2. PostProcessor    — fix headings and image paths in generated HTML
  3. ShellGenerator   — write worldbuilding/ shell pages
  4. GarbageCollector — delete stale files no longer in manifest
"""

import sys
import os

# Ensure the scripts/ directory is on the path when run from repo root
sys.path.insert(0, os.path.dirname(__file__))

from manifest_builder import ManifestBuilder
from post_processor import PostProcessor
from shell_generator import ShellGenerator
from garbage_collector import GarbageCollector


def main() -> None:
    print('=== Astatyr Site Generator ===\n')

    print('Step 1: Building manifest...')
    manifest = ManifestBuilder().build()

    print('\nStep 2: Post-processing generated HTML...')
    PostProcessor().run()

    print('\nStep 3: Generating shell pages...')
    ShellGenerator(manifest).run()

    print('\nStep 4: Garbage collection...')
    GarbageCollector(manifest).run()

    print('\n=== Done ===')


if __name__ == '__main__':
    main()
