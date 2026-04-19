"""
serve.py — Local development server.
This file is gitignored and never pushed to the repo.

Runs generate.py first, then serves the site at localhost.

Usage (from repo root):
    python serve.py            # serves on port 8000
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


# ── Step 2: Serve ─────────────────────────────────────────────────────────────

class DevHandler(http.server.SimpleHTTPRequestHandler):

    def end_headers(self):
        # No caching — see changes immediately on refresh
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, format, *args):
        # Clean log: method + path + status code
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

    with http.server.HTTPServer(('', PORT), DevHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nStopped.')
