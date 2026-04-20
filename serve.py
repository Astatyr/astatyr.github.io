"""
serve.py — Local development server.
This file is gitignored and never pushed to the repo.

Mimics GitHub Pages behaviour and runs link checks before serving.

Usage (from repo root):
    python serve.py            # port 8000
    python serve.py 3000       # custom port
"""

import sys
import os
import re
import http.server
import webbrowser
import subprocess

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

# Must match WB_BASE in post_processor.py
WB_BASE = 'worldbuilding'


# ── Step 1: Run generate.py ───────────────────────────────────────────────────

def run_generator():
    print("Running generate.py...")
    result = subprocess.run([sys.executable, "scripts/generate.py"])
    if result.returncode != 0:
        print("\ngenerate.py failed. Fix errors before serving.")
        sys.exit(1)
    print()


# ── Step 2: Check for broken links ───────────────────────────────────────────

LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def resolve_link(url: str) -> bool:
    """Return True if the link resolves to a real file on disk."""
    # Skip external links
    if url.startswith('http') or url.startswith('mailto'):
        return True

    # Absolute links (start with /)
    if url.startswith('/'):
        local = '.' + url.rstrip('/')
    else:
        # Internal worldbuilding link — prepend base
        local = WB_BASE + '/' + url.rstrip('/')

    # Check variations
    for candidate in [local, local + '.html', local + '/index.html']:
        if os.path.isfile(candidate):
            return True

    return False


def extract_links_from_docx(docx_path: str) -> list[tuple[str, str]]:
    """Extract [text](url) links from a docx by reading its XML directly.
    Concatenates all text runs before searching to handle links split across runs.
    """
    try:
        import zipfile
        with zipfile.ZipFile(docx_path) as z:
            xml = z.read('word/document.xml').decode('utf-8')
        # Join all text runs — handles links split across XML runs by Word
        all_text = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', xml))
        return LINK_PATTERN.findall(all_text)
    except Exception:
        return []


def run_link_check():
    print("Checking links in content/...")

    broken = []  # (docx_file, link_text, url)

    for root, dirs, files in os.walk('content'):
        dirs[:] = [d for d in dirs if d != '_font_backup']
        for fname in sorted(files):
            if not fname.endswith('.docx') or fname.startswith('~$'):
                continue
            docx_path = os.path.join(root, fname)
            links = extract_links_from_docx(docx_path)
            for text, url in links:
                # Skip image links from pandoc (media/image*.*)
                if url.startswith('media/'):
                    continue
                if not resolve_link(url):
                    broken.append((docx_path, text, url))

    if not broken:
        print("  All links OK.\n")
        return

    print(f"\n  ⚠  {len(broken)} broken link(s) found:\n")
    by_file: dict[str, list[tuple[str, str]]] = {}
    for source, text, url in broken:
        by_file.setdefault(source, []).append((text, url))

    for source, links in sorted(by_file.items()):
        print(f"  {source}")
        for text, url in links:
            print(f"    ✗  [{text}]({url})")
    print()


# ── Step 3: Serve with GitHub Pages-style URL resolution ─────────────────────

class GitHubPagesHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.path = self._resolve(self.path)
        super().do_GET()

    def _resolve(self, path: str) -> str:
        clean = path.split('?')[0]
        local = '.' + clean
        if os.path.isfile(local):
            return path
        if os.path.isfile(local + '.html'):
            return clean + '.html'
        if os.path.isfile(local.rstrip('/') + '/index.html'):
            return clean.rstrip('/') + '/index.html'
        return path

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, format, *args):
        status = args[1]
        marker = '✗' if status == '404' else ' '
        # Suppress noisy known 404s
        if any(s in self.path for s in ['cdn-cgi', 'favicon']):
            return
        print(f"  {marker} {args[0]} {self.path} → {status}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if not os.path.exists('index.html'):
        print('ERROR: Run from your repo root, not a subfolder.')
        sys.exit(1)

    run_generator()
    run_link_check()

    print(f'Serving at http://localhost:{PORT}')
    print('Press Ctrl+C to stop.\n')
    webbrowser.open(f'http://localhost:{PORT}')

    with http.server.HTTPServer(('', PORT), GitHubPagesHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nStopped.')
