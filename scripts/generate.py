import os, json

# ── helpers ──────────────────────────────────────────────────────────────────

def to_title(s):
    return s.replace('-', ' ').replace('_', ' ')

def read_meta(folder):
    meta = {}
    path = os.path.join(folder, '_meta.txt')
    if os.path.exists(path):
        for line in open(path, encoding='utf-8'):
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip()
    return meta

def write_page(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Written: {path}")

# ── shared pieces ─────────────────────────────────────────────────────────────

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"/><link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet"/>'

CSS = """*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root { --white: #ffffff; --off-white: #f7f6f3; --ink: #1a1a1a; --muted: #888; --border: #e4e2dc; --nav-w: 220px; --hover-bg: #f0ede6; }
html { scroll-behavior: smooth; }
body { font-family: 'DM Sans', sans-serif; background: var(--white); color: var(--ink); display: flex; min-height: 100vh; }
nav { position: fixed; top: 0; left: 0; width: var(--nav-w); height: 100vh; background: var(--off-white); border-right: 1px solid var(--border); display: flex; flex-direction: column; padding: 2.5rem 1.5rem; gap: 0.4rem; z-index: 100; overflow-y: auto; }
.nav-logo { font-family: 'DM Serif Display', serif; font-size: 1.4rem; letter-spacing: -0.02em; color: var(--ink); margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border); line-height: 1.2; text-decoration: none; display: block; }
.nav-logo span { display: block; font-family: 'DM Sans', sans-serif; font-size: 0.72rem; font-weight: 300; color: var(--muted); letter-spacing: 0.08em; text-transform: uppercase; margin-top: 0.3rem; }
.nav-btn { display: flex; align-items: center; gap: 0.6rem; padding: 0.55rem 0.8rem; border-radius: 8px; text-decoration: none; color: var(--muted); font-size: 0.82rem; font-weight: 400; transition: background 0.18s, color 0.18s; border: none; background: transparent; width: 100%; text-align: left; }
.nav-btn:hover, .nav-btn.active { background: var(--hover-bg); color: var(--ink); }
.nav-divider { height: 1px; background: var(--border); margin: 0.8rem 0; }
.nav-section-label { font-size: 0.63rem; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; color: #ccc; padding: 0.3rem 0.8rem; }
.nav-sub-btn { font-size: 0.77rem; padding-left: 1.8rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.nav-footer { margin-top: auto; font-size: 0.7rem; color: var(--muted); padding-top: 1rem; }
main { margin-left: var(--nav-w); flex: 1; padding: 4rem 5rem; max-width: 820px; }
.back-link { display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.75rem; color: var(--muted); text-decoration: none; margin-bottom: 1.5rem; transition: color 0.15s; }
.back-link:hover { color: var(--ink); }
.section-label { font-size: 0.68rem; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted); margin-bottom: 1.2rem; display: flex; align-items: center; gap: 0.6rem; }
.section-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }
.wb-section { margin-bottom: 3.5rem; }
.doc-content h1, .doc-content h2 { font-family: 'DM Serif Display', serif; font-weight: 400; color: var(--ink); margin-bottom: 0.6rem; margin-top: 1.6rem; }
.doc-content h1 { font-size: 1.5rem; }
.doc-content h2 { font-size: 1.2rem; }
.doc-content h3 { font-size: 1rem; font-weight: 500; margin-bottom: 0.4rem; margin-top: 1.2rem; }
.doc-content p { font-size: 0.9rem; color: #3a3a3a; line-height: 1.85; font-weight: 300; margin-bottom: 1rem; }
.doc-content ul, .doc-content ol { padding-left: 1.4rem; margin-bottom: 0.8rem; }
.doc-content li { font-size: 0.9rem; color: #3a3a3a; line-height: 1.8; font-weight: 300; margin-bottom: 0.3rem; }
.doc-content strong { font-weight: 500; color: var(--ink); }
.doc-content em { font-style: italic; }
.doc-content blockquote { border-left: 2px solid var(--border); padding-left: 1.2rem; margin: 1rem 0; color: #666; font-style: italic; }
.doc-content table { width: 100%; border-collapse: collapse; margin-bottom: 1rem; font-size: 0.87rem; border: 1px solid var(--border); }
.doc-content th { font-weight: 500; text-align: center; padding: 0.4rem 0.8rem; border: 1px solid var(--border); background: var(--off-white); color: var(--ink); }
.doc-content td { padding: 0.4rem 0.8rem; border: 1px solid var(--border); color: #3a3a3a; font-weight: 300; vertical-align: top; }
.doc-content td p { margin-bottom: 0.4rem; font-size: 0.87rem; }
.doc-content td p:last-child { margin-bottom: 0; }
.doc-content td ul, .doc-content td ol { margin-bottom: 0.4rem; }
.doc-content table table { margin-bottom: 0; border: 1px solid var(--border); }
.doc-content tr:last-child td { border-bottom: 1px solid var(--border); }
.doc-content > *:first-child { margin-top: 0; }
.chapter-list { display: flex; flex-direction: column; gap: 0.6rem; }
.chapter-link { display: flex; align-items: center; padding: 1rem 1.2rem; border: 1px solid var(--border); border-radius: 10px; text-decoration: none; color: var(--ink); transition: box-shadow 0.2s, transform 0.2s; background: var(--white); gap: 1rem; }
.chapter-link:hover { box-shadow: 0 3px 16px rgba(0,0,0,0.07); transform: translateY(-1px); }
.chapter-link .ch-num { font-size: 0.65rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); min-width: 70px; flex-shrink: 0; }
.chapter-link .ch-title { font-family: 'DM Serif Display', serif; font-size: 1rem; font-weight: 400; flex: 1; }
.ch-nav { display: flex; justify-content: space-between; gap: 1rem; margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--border); }
.ch-nav a { display: flex; flex-direction: column; gap: 0.2rem; text-decoration: none; padding: 0.8rem 1rem; border: 1px solid var(--border); border-radius: 10px; transition: background 0.15s; max-width: 48%; }
.ch-nav a:hover { background: var(--off-white); }
.ch-nav .dir { font-size: 0.65rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); }
.ch-nav .ch-title { font-family: 'DM Serif Display', serif; font-size: 0.95rem; color: var(--ink); }
.ch-nav .next { text-align: right; margin-left: auto; }
.page-title { font-family: 'DM Serif Display', serif; font-size: 2.4rem; letter-spacing: -0.03em; line-height: 1.1; margin-bottom: 0.4rem; }
.page-meta { font-size: 0.75rem; color: var(--muted); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.8rem; }
.page-desc { font-size: 0.9rem; color: var(--muted); font-weight: 300; line-height: 1.7; margin-bottom: 2.5rem; }
.char-portrait { width: 200px; aspect-ratio: 3/4; border-radius: 12px; background-color: var(--off-white); background-size: cover; background-position: center top; border: 1px solid var(--border); margin-bottom: 1.5rem; }
.loc-banner { width: 100%; height: 240px; background-color: var(--off-white); background-size: cover; background-position: center; position: relative; }
.loc-banner-overlay { position: absolute; inset: 0; background: linear-gradient(to top, rgba(26,26,26,0.5) 0%, transparent 60%); }
.loc-banner-title { position: absolute; bottom: 2rem; left: 2rem; color: #fff; }
.loc-type-label { font-size: 0.68rem; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; opacity: 0.8; margin-bottom: 0.3rem; }
.content-area { padding: 3rem 4rem 4rem; max-width: 820px; }
.loading { font-size: 0.82rem; color: var(--muted); font-style: italic; }
.empty-note { font-size: 0.82rem; color: #ccc; font-style: italic; }
@keyframes fadeUp { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
@media (max-width: 768px) { nav { display: none; } main { margin-left: 0; padding: 2rem 1.5rem; } .content-area { padding: 2rem 1.5rem; } }"""

def head(title="Astatyr"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title}</title>
  {FONTS}
  <style>{CSS}</style>
</head>
<body>"""

NAV = """<nav>
  <a class="nav-logo" href="/index.html">Astatyr<span>Hub Page</span></a>
  <a class="nav-btn" href="/worldbuilding.html">&#127758; Worldbuilding</a>
  <div class="nav-divider"></div>
  <div class="nav-section-label" id="nav-section-title">Loading...</div>
  <div id="nav-items"></div>
  <div class="nav-footer">&copy; 2025 Justin Adrian Halim</div>
</nav>"""

FOOT = "\n</body>\n</html>"

# ── page builders ─────────────────────────────────────────────────────────────

def make_storyline_index():
    return head() + NAV + """
<main style="animation:fadeUp .4s ease both">
  <a class="back-link" href="/worldbuilding.html">&larr; Worldbuilding</a>
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
</main>
<script>
var parts = window.location.pathname.replace(/\/$/, '').split('/');
var slId = parts[parts.length - 1];
if (slId === 'index.html') slId = parts[parts.length - 2];
async function init() {
  var manifest;
  try { manifest = await (await fetch('/generated/manifest.json')).json(); } catch(e) { return; }
  var sl = manifest.storylines.find(function(s) { return s.id === slId; });
  if (!sl) { document.getElementById('page-title').textContent = slId.replace(/[-_]/g, ' '); return; }
  document.title = sl.title + ' \u2014 Astatyr';
  document.getElementById('page-title').textContent = sl.title;
  document.getElementById('page-meta').textContent = [sl.type, sl.status].filter(Boolean).join(' \u00b7 ');
  document.getElementById('page-desc').textContent = sl.description || '';
  document.getElementById('nav-section-title').textContent = sl.title;
  var ni = '<a class="nav-btn nav-sub-btn active" href="index.html">Overview</a>';
  sl.chapters.forEach(function(ch, i) {
    ni += '<a class="nav-btn nav-sub-btn" href="' + ch.id + '.html">Ch.' + (i+1) + ' \u2014 ' + ch.title + '</a>';
  });
  document.getElementById('nav-items').innerHTML = ni;
  var cl = document.getElementById('chapter-list');
  if (!sl.chapters.length) {
    cl.innerHTML = '<p class="empty-note">No chapters yet. Add .docx files to content/storylines/' + slId + '/</p>';
  } else {
    cl.innerHTML = sl.chapters.map(function(ch, i) {
      return '<a class="chapter-link" href="' + ch.id + '.html"><span class="ch-num">Chapter ' + (i+1) + '</span><span class="ch-title">' + ch.title + '</span><span>&rarr;</span></a>';
    }).join('');
  }
  try {
    var r = await fetch('/generated/storylines/' + slId + '/index.html');
    if (r.ok) document.getElementById('overview-content').innerHTML = await r.text();
    else document.getElementById('overview-content').innerHTML = '<p class="empty-note">Add index.docx to content/storylines/' + slId + '/</p>';
  } catch(e) {}
}
init();
</script>""" + FOOT


def make_chapter():
    return head() + NAV + """
<main style="animation:fadeUp .4s ease both">
  <a class="back-link" href="/worldbuilding.html">&larr; Worldbuilding</a>
  <div id="ch-label" class="page-meta">Chapter</div>
  <div id="ch-title" class="page-title">Loading&hellip;</div>
  <div style="margin-top:2rem" id="ch-content" class="doc-content"><p class="loading">Loading&hellip;</p></div>
  <div class="ch-nav" id="ch-nav"></div>
</main>
<script>
var parts = window.location.pathname.replace(/\/$/, '').split('/');
var chId = parts[parts.length - 1].replace('.html', '');
var slId = parts[parts.length - 2];
async function init() {
  var manifest;
  try { manifest = await (await fetch('/generated/manifest.json')).json(); } catch(e) {}
  var sl = manifest && manifest.storylines.find(function(s) { return s.id === slId; });
  if (sl) {
    document.title = sl.title + ' \u2014 Astatyr';
    document.getElementById('nav-section-title').textContent = sl.title;
    var chIdx = sl.chapters.findIndex(function(c) { return c.id === chId; });
    var ch = sl.chapters[chIdx];
    if (ch) {
      document.getElementById('ch-label').textContent = 'Chapter ' + (chIdx + 1);
      document.getElementById('ch-title').textContent = ch.title;
      var ni = '<a class="nav-btn nav-sub-btn" href="index.html">Overview</a>';
      sl.chapters.forEach(function(c, i) {
        ni += '<a class="nav-btn nav-sub-btn' + (c.id === chId ? ' active' : '') + '" href="' + c.id + '.html">Ch.' + (i+1) + ' \u2014 ' + c.title + '</a>';
      });
      document.getElementById('nav-items').innerHTML = ni;
      var prev = chIdx > 0 ? sl.chapters[chIdx - 1] : null;
      var next = chIdx < sl.chapters.length - 1 ? sl.chapters[chIdx + 1] : null;
      document.getElementById('ch-nav').innerHTML =
        (prev ? '<a href="' + prev.id + '.html"><span class="dir">&larr; Previous</span><span class="ch-title">' + prev.title + '</span></a>' : '<span></span>') +
        (next ? '<a class="next" href="' + next.id + '.html"><span class="dir">Next &rarr;</span><span class="ch-title">' + next.title + '</span></a>' : '<span></span>');
    }
  }
  try {
    var r = await fetch('/generated/storylines/' + slId + '/' + chId + '.html');
    if (r.ok) document.getElementById('ch-content').innerHTML = await r.text();
    else document.getElementById('ch-content').innerHTML = '<p class="empty-note">Content not found. Push the .docx and wait for the Action to run.</p>';
  } catch(e) {}
}
init();
</script>""" + FOOT


def make_character():
    return head() + NAV + """
<main style="animation:fadeUp .4s ease both">
  <a class="back-link" href="/worldbuilding.html">&larr; Worldbuilding</a>
  <div class="char-portrait" id="char-portrait"></div>
  <div class="page-title" id="char-name">Loading&hellip;</div>
  <div class="page-meta" id="char-role-text"></div>
  <div class="wb-section" style="margin-top:2rem">
    <div class="section-label">About</div>
    <div id="char-content" class="doc-content"><p class="loading">Loading&hellip;</p></div>
  </div>
</main>
<script>
var parts = window.location.pathname.split('/');
var charId = parts[parts.length - 1].replace('.html', '');
async function init() {
  var manifest;
  try { manifest = await (await fetch('/generated/manifest.json')).json(); } catch(e) {}
  var ch = manifest && manifest.characters.find(function(c) { return c.id === charId; });
  if (ch) {
    document.title = ch.title + ' \u2014 Astatyr';
    document.getElementById('char-name').textContent = ch.title;
    document.getElementById('char-role-text').textContent = ch.role || '';
    document.getElementById('nav-section-title').textContent = 'Characters';
    document.getElementById('nav-items').innerHTML = manifest.characters.map(function(c) {
      return '<a class="nav-btn nav-sub-btn' + (c.id === charId ? ' active' : '') + '" href="' + c.id + '.html">' + c.title + '</a>';
    }).join('');
  }
  try {
    var r = await fetch('/generated/characters/' + charId + '.html');
    if (r.ok) document.getElementById('char-content').innerHTML = await r.text();
    else document.getElementById('char-content').innerHTML = '<p class="empty-note">Content not found. Push the .docx and wait for the Action to run.</p>';
  } catch(e) {}
}
init();
</script>""" + FOOT


def make_location():
    return head() + """<nav>
  <a class="nav-logo" href="/index.html">Astatyr<span>Hub Page</span></a>
  <a class="nav-btn" href="/worldbuilding.html">&#127758; Worldbuilding</a>
  <div class="nav-divider"></div>
  <div class="nav-section-label" id="nav-section-title">Geography</div>
  <div id="nav-items"></div>
  <div class="nav-footer">&copy; 2025 Justin Adrian Halim</div>
</nav>
<main style="padding:0;max-width:none;margin-left:var(--nav-w)">
  <div class="loc-banner">
    <div class="loc-banner-overlay"></div>
    <div class="loc-banner-title">
      <div class="loc-type-label" id="loc-type">Location</div>
      <div style="font-family:'DM Serif Display',serif;font-size:2.2rem;letter-spacing:-.03em" id="loc-name">Loading&hellip;</div>
    </div>
  </div>
  <div class="content-area">
    <a class="back-link" href="/worldbuilding.html">&larr; Worldbuilding</a>
    <div class="wb-section">
      <div class="section-label">Overview</div>
      <div id="loc-content" class="doc-content"><p class="loading">Loading&hellip;</p></div>
    </div>
  </div>
</main>
<script>
var parts = window.location.pathname.replace(/\/$/, '').split('/');
var geoId = parts[parts.length - 1];
async function init() {
  var manifest;
  try { manifest = await (await fetch('/generated/manifest.json')).json(); } catch(e) {}
  var geo = manifest && manifest.geography.find(function(g) { return g.id === geoId; });
  if (geo) {
    document.title = geo.title + ' \u2014 Astatyr';
    document.getElementById('loc-name').textContent = geo.title;
    document.getElementById('loc-type').textContent = geo.type;
    document.getElementById('nav-section-title').textContent = 'Geography';
    document.getElementById('nav-items').innerHTML = manifest.geography.map(function(g) {
      return '<a class="nav-btn nav-sub-btn' + (g.id === geoId ? ' active' : '') + '" href="/worldbuilding/geography/' + g.id + '/">' + g.title + '</a>';
    }).join('');
  }
  try {
    var r = await fetch('/generated/geography/' + geoId + '/index.html');
    if (r.ok) document.getElementById('loc-content').innerHTML = await r.text();
    else document.getElementById('loc-content').innerHTML = '<p class="empty-note">Content not found. Push index.docx and wait for the Action to run.</p>';
  } catch(e) {}
}
init();
</script>""" + FOOT


# ── build manifest ────────────────────────────────────────────────────────────

manifest = {"storylines": [], "characters": [], "geography": []}

sl_root = "content/storylines"
if os.path.exists(sl_root):
    for sl_name in sorted(os.listdir(sl_root)):
        sl_path = os.path.join(sl_root, sl_name)
        if not os.path.isdir(sl_path):
            continue
        meta = read_meta(sl_path)
        chapters = []
        for f in sorted(os.listdir(sl_path)):
            if f.endswith('.docx') and f.lower() != 'index.docx' and not f.startswith('_'):
                chapters.append({"id": f[:-5], "title": to_title(f[:-5])})
        manifest['storylines'].append({
            "id": sl_name,
            "title": meta.get('title', to_title(sl_name)),
            "type": meta.get('type', 'Storyline'),
            "status": meta.get('status', 'In Progress'),
            "description": meta.get('description', ''),
            "chapters": chapters
        })

ch_root = "content/characters"
if os.path.exists(ch_root):
    for f in sorted(os.listdir(ch_root)):
        if f.endswith('.docx') and not f.startswith('_'):
            ch_id = f[:-5]
            meta = {}
            meta_path = os.path.join(ch_root, f'_{ch_id}_meta.txt')
            if os.path.exists(meta_path):
                for line in open(meta_path, encoding='utf-8'):
                    if ':' in line:
                        k, v = line.split(':', 1)
                        meta[k.strip()] = v.strip()
            manifest['characters'].append({
                "id": ch_id,
                "title": meta.get('title', to_title(ch_id)),
                "role": meta.get('role', '')
            })

geo_root = "content/geography"
if os.path.exists(geo_root):
    for country_name in sorted(os.listdir(geo_root)):
        country_path = os.path.join(geo_root, country_name)
        if not os.path.isdir(country_path):
            continue
        meta = read_meta(country_path)
        locations = []
        for f in sorted(os.listdir(country_path)):
            if f.endswith('.docx') and f.lower() != 'index.docx' and not f.startswith('_'):
                locations.append({"id": f[:-5], "title": to_title(f[:-5])})
        manifest['geography'].append({
            "id": country_name,
            "title": meta.get('title', to_title(country_name)),
            "type": meta.get('type', 'Location'),
            "description": meta.get('description', ''),
            "locations": locations
        })

os.makedirs("generated", exist_ok=True)
with open("generated/manifest.json", "w", encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)
print("manifest.json written.")

# Fix image paths in all generated HTML files
# Pandoc writes src="generated/media/..." but served from a subpath,
# the browser resolves it relative to the HTML file location.
# We rewrite to absolute /generated/media/... paths.
import re
for root, dirs, files in os.walk("generated"):
    for fname in files:
        if not fname.endswith(".html"):
            continue
        fpath = os.path.join(root, fname)
        html = open(fpath, encoding="utf-8").read()
        # Rewrite any src that points into generated/media
        fixed = re.sub(
            r'src="(?:\.\.\/)*generated\/media\/',
            'src="/generated/media/',
            html
        )
        # Also handle pandoc sometimes writing just media/
        fixed = re.sub(
            r'src="media\/',
            'src="/generated/media/',
            fixed
        )
        if fixed != html:
            open(fpath, "w", encoding="utf-8").write(fixed)
            print(f"  Fixed image paths: {fpath}")
print(json.dumps(manifest, indent=2))

# ── generate shell pages ──────────────────────────────────────────────────────

print("\nGenerating shell pages...")

for sl in manifest['storylines']:
    sl_dir = f"worldbuilding/storylines/{sl['id']}"
    write_page(f"{sl_dir}/index.html", make_storyline_index())
    for ch in sl['chapters']:
        write_page(f"{sl_dir}/{ch['id']}.html", make_chapter())

for char in manifest['characters']:
    write_page(f"worldbuilding/characters/{char['id']}.html", make_character())

for geo in manifest['geography']:
    write_page(f"worldbuilding/geography/{geo['id']}/index.html", make_location())

print("Done.")
