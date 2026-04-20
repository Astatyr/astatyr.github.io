"""
serve.py — Local development server.
This file is gitignored and never pushed to the repo.

Mimics GitHub Pages behaviour:
  /worldbuilding     → serves worldbuilding.html
  /worldbuilding/    → serves worldbuilding/index.html
  /poetry            → serves poetry.html

Usage (from repo root):
    python serve.py            # port 8000
    python serve.py 3000       # custom port
"""

import sys
import os
import http.server
import webbrowser
import subprocess

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


# ── Step 1: Run generate.py ───────────────────────────────────────────────────

def run_generator():
    print("Running generate.py...")
    result = subprocess.run([sys.executable, "scripts/generate.py"])
    if result.returncode != 0:
        print("\ngenerate.py failed. Fix errors before serving.")
        sys.exit(1)
    print()


# ── Step 2: Serve with GitHub Pages-style URL resolution ─────────────────────

class GitHubPagesHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        # Try to resolve the path like GitHub Pages would
        self.path = self._resolve(self.path)
        super().do_GET()

    def _resolve(self, path: str) -> str:
        # Strip query string
        clean = path.split('?')[0]

        # Check if the path maps directly to a file
        local = '.' + clean
        if os.path.isfile(local):
            return path

        # Try appending .html (e.g. /worldbuilding → worldbuilding.html)
        if os.path.isfile(local + '.html'):
            return clean + '.html'

        # Try appending /index.html (e.g. /worldbuilding/ → worldbuilding/index.html)
        if os.path.isfile(local.rstrip('/') + '/index.html'):
            return clean.rstrip('/') + '/index.html'

        # Fall through to default (will 404 or directory list)
        return path

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, format, *args):
        print(f"  {args[0]} {self.path} → {args[1]}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if not os.path.exists('index.html'):
        print('ERROR: Run from your repo root, not a subfolder.')
        sys.exit(1)

    run_generator()

    print(f'Serving at http://localhost:{PORT}')
    print('Press Ctrl+C to stop.\n')
    webbrowser.open(f'http://localhost:{PORT}')

    with http.server.HTTPServer(('', PORT), GitHubPagesHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nStopped.')