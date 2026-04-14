"""
Downloads all external libraries used by the project to a local libs/ folder.
Run this script once from the project root:  python download_libs.py
"""

import os
import ssl
import urllib.request
import urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))

# Trust-all SSL context for environments with corporate/self-signed CAs
_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE

def download(url, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    if os.path.exists(dest_path):
        print(f"  [skip] {os.path.relpath(dest_path, BASE)}")
        return
    print(f"  [dl]   {os.path.relpath(dest_path, BASE)}")
    print(f"         <- {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60, context=_ssl_ctx) as r:
            data = r.read()
        with open(dest_path, "wb") as f:
            f.write(data)
        print(f"         OK ({len(data):,} bytes)")
    except Exception as e:
        print(f"         ERROR: {e}")

L = os.path.join(BASE, "libs")

# ── UMD / script-tag libraries ────────────────────────────────────────────────

# React 18 (UMD)
download("https://unpkg.com/react@18/umd/react.production.min.js",
         os.path.join(L, "react.production.min.js"))

# ReactDOM 18 (UMD)
download("https://unpkg.com/react-dom@18/umd/react-dom.production.min.js",
         os.path.join(L, "react-dom.production.min.js"))

# Babel standalone (for JSX)
download("https://unpkg.com/@babel/standalone/babel.min.js",
         os.path.join(L, "babel.min.js"))

# Tailwind Play CDN (v3, the <script> tag version)
download("https://cdn.tailwindcss.com",
         os.path.join(L, "tailwind.cdn.js"))

# Tailwind CSS v2 static stylesheet (used by cms-architect, data-guardian, ORM)
download("https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
         os.path.join(L, "tailwind.v2.min.css"))

# Lucide React (UMD – used by LawAndProperty, 06strings)
download("https://unpkg.com/lucide-react@0.292.0/dist/umd/lucide-react.min.js",
         os.path.join(L, "lucide-react.min.js"))

# Lucide vanilla (IIFE – used by 01arrays, 02list-basics)
download("https://unpkg.com/lucide@latest/dist/umd/lucide.min.js",
         os.path.join(L, "lucide.min.js"))

# framer-motion UMD (used by data-guardian as script tag)
download("https://unpkg.com/framer-motion@10.16.16/dist/framer-motion.js",
         os.path.join(L, "framer-motion.js"))

# Font Awesome 6
download(
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css",
    os.path.join(L, "font-awesome", "all.min.css"),
)
# FA webfonts (all formats used in all.min.css)
FA_BASE = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/webfonts/"
for wf in [
    "fa-brands-400.woff2", "fa-regular-400.woff2", "fa-solid-900.woff2",
    "fa-brands-400.ttf",   "fa-regular-400.ttf",   "fa-solid-900.ttf",
]:
    download(FA_BASE + wf, os.path.join(L, "font-awesome", "webfonts", wf))

# ── reveal.js 5 ───────────────────────────────────────────────────────────────

RV = os.path.join(L, "reveal")
rv_base = "https://cdn.jsdelivr.net/npm/reveal.js@5"

download(f"{rv_base}/dist/reveal.css",                    os.path.join(RV, "dist", "reveal.css"))
download(f"{rv_base}/dist/reveal.js",                     os.path.join(RV, "dist", "reveal.js"))
download(f"{rv_base}/dist/theme/night.css",               os.path.join(RV, "dist", "theme", "night.css"))
download(f"{rv_base}/dist/theme/beige.css",               os.path.join(RV, "dist", "theme", "beige.css"))
download(f"{rv_base}/dist/theme/black.css",               os.path.join(RV, "dist", "theme", "black.css"))
download(f"{rv_base}/dist/theme/blood.css",               os.path.join(RV, "dist", "theme", "blood.css"))
download(f"{rv_base}/dist/theme/league.css",              os.path.join(RV, "dist", "theme", "league.css"))
download(f"{rv_base}/dist/theme/moon.css",                os.path.join(RV, "dist", "theme", "moon.css"))
download(f"{rv_base}/dist/theme/serif.css",               os.path.join(RV, "dist", "theme", "serif.css"))
download(f"{rv_base}/dist/theme/simple.css",              os.path.join(RV, "dist", "theme", "simple.css"))
download(f"{rv_base}/dist/theme/sky.css",                 os.path.join(RV, "dist", "theme", "sky.css"))
download(f"{rv_base}/dist/theme/solarized.css",           os.path.join(RV, "dist", "theme", "solarized.css"))
download(f"{rv_base}/dist/theme/white.css",               os.path.join(RV, "dist", "theme", "white.css"))
download(f"{rv_base}/plugin/highlight/highlight.js",      os.path.join(RV, "plugin", "highlight", "highlight.js"))
download(f"{rv_base}/plugin/highlight/monokai.css",       os.path.join(RV, "plugin", "highlight", "monokai.css"))
download(f"{rv_base}/plugin/markdown/markdown.js",        os.path.join(RV, "plugin", "markdown", "markdown.js"))
download(f"{rv_base}/plugin/notes/notes.js",              os.path.join(RV, "plugin", "notes", "notes.js"))
download(f"{rv_base}/plugin/zoom/zoom.js",                os.path.join(RV, "plugin", "zoom", "zoom.js"))
download(f"{rv_base}/plugin/search/search.js",            os.path.join(RV, "plugin", "search", "search.js"))
download(f"{rv_base}/plugin/math/math.js",                os.path.join(RV, "plugin", "math", "math.js"))

# ── ESM modules (recursive download from esm.sh) ─────────────────────────────
# We recursively fetch each .mjs file and rewrite absolute CDN paths to
# relative paths so everything works without network access.

import re as _re

ESM_BASE = "https://esm.sh"
ESM = os.path.join(L, "esm")

def _url_to_local(url):
    """Map an esm.sh absolute URL to a flat local file path inside libs/esm/.
    Produces a single safe filename (no sub-directories) by hashing the full URL
    into a short prefix and appending the original file extension.
    """
    import hashlib
    path = url.replace(ESM_BASE, "").lstrip("/")
    # Determine extension
    clean_path = path.split("?")[0]  # strip query string for extension detection
    if "." in clean_path.rsplit("/", 1)[-1]:
        ext = "." + clean_path.rsplit(".", 1)[-1]
    else:
        ext = ".js"
    # Build a readable but filesystem-safe stem
    stem = path.replace("?", "__").replace("&", "_").replace("=", "_").replace("/", "_").replace("@", "_at_").replace("^", "_hat_").replace("~", "_tilde_").replace(":", "_")
    # Remove any remaining Windows-invalid chars
    for ch in '<>"|*\\':
        stem = stem.replace(ch, "_")
    # Trim length  
    if len(stem) > 120:
        stem = stem[:80] + "_" + hashlib.md5(stem.encode()).hexdigest()[:8]
    if not stem.endswith(ext):
        stem = stem + ext
    return os.path.join(ESM, stem)

_fetched = set()

def download_esm(url):
    """Fetch one ESM file, rewrite its imports to relative paths, recurse."""
    # Normalise: strip query string from esm.sh module paths that end in .mjs
    dest = _url_to_local(url)
    if dest in _fetched:
        return
    _fetched.add(dest)

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest):
        print(f"  [skip] {os.path.relpath(dest, BASE)}")
        # Still recurse to make sure all deps are present
        try:
            with open(dest, encoding="utf-8") as fh:
                text = fh.read()
            _recurse_esm(url, text)
        except Exception:
            pass
        return

    print(f"  [esm]  {os.path.relpath(dest, BASE)}")
    print(f"         <- {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60, context=_ssl_ctx) as r:
            text = r.read().decode("utf-8")
        print(f"         OK ({len(text):,} chars)")
    except Exception as e:
        print(f"         ERROR: {e}")
        return

    rewritten, deps = _rewrite_esm(url, dest, text)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(rewritten)

    for dep_url in deps:
        download_esm(dep_url)

def _abs_url(base_url, specifier):
    """Resolve a specifier (absolute server-relative or relative) to a full URL."""
    if specifier.startswith("https://") or specifier.startswith("http://"):
        return specifier
    if specifier.startswith("/"):
        return ESM_BASE + specifier
    # relative path
    base_dir = base_url.rsplit("/", 1)[0]
    return base_dir + "/" + specifier

def _rewrite_esm(base_url, dest_path, text):
    """
    Rewrite import/export specifiers in an ESM file to relative local paths.
    Returns (rewritten_text, list_of_absolute_dep_urls).
    """
    deps = []
    pattern = _re.compile(
        r'((?:import|export)[^"\']*?["\'])([^"\']+)(["\'])',
        _re.DOTALL,
    )

    def replacer(m):
        prefix, specifier, quote = m.group(1), m.group(2), m.group(3)
        if not (specifier.startswith("/") or specifier.startswith(".") or specifier.startswith("http")):
            # bare specifier – leave alone
            return m.group(0)
        abs_url = _abs_url(base_url, specifier)
        if not abs_url.startswith(ESM_BASE):
            return m.group(0)
        dep_local = _url_to_local(abs_url)
        deps.append(abs_url)
        # compute relative path from current file to dep (always forward slashes for ESM)
        rel = os.path.relpath(dep_local, os.path.dirname(dest_path)).replace("\\", "/")
        if not rel.startswith("."):
            rel = "./" + rel
        return prefix + rel + quote

    rewritten = pattern.sub(replacer, text)

    # Also handle dynamic import("...")
    dyn_pattern = _re.compile(r'(import\s*\(\s*["\'])([^"\']+)(["\'])')
    def dyn_replacer(m):
        prefix, specifier, quote = m.group(1), m.group(2), m.group(3)
        if not (specifier.startswith("/") or specifier.startswith(".") or specifier.startswith("http")):
            return m.group(0)
        abs_url = _abs_url(base_url, specifier)
        if not abs_url.startswith(ESM_BASE):
            return m.group(0)
        dep_local = _url_to_local(abs_url)
        deps.append(abs_url)
        rel = os.path.relpath(dep_local, os.path.dirname(dest_path)).replace("\\", "/")
        if not rel.startswith("."):
            rel = "./" + rel
        return prefix + rel + quote
    rewritten = dyn_pattern.sub(dyn_replacer, rewritten)

    return rewritten, deps

def _recurse_esm(base_url, text):
    """Parse deps from already-saved file and schedule downloads (no rewrite)."""
    pattern = _re.compile(
        r'(?:import|export)[^"\']*?["\']([^"\']+)["\']', _re.DOTALL)
    dyn_pattern = _re.compile(r'import\s*\(\s*["\']([^"\']+)["\']')
    for m in list(pattern.finditer(text)) + list(dyn_pattern.finditer(text)):
        spec = m.group(1)
        if spec.startswith("/"):
            dep_url = ESM_BASE + spec
            download_esm(dep_url)

# Entry-point modules (these are the importmap targets)
_ENTRY_POINTS = [
    "https://esm.sh/react@18.2.0",
    "https://esm.sh/react-dom@18.2.0/client?deps=react@18.2.0",
    "https://esm.sh/framer-motion@10.16.16?deps=react@18.2.0,react-dom@18.2.0",
    "https://esm.sh/framer-motion@10.16.4?deps=react@18.2.0,react-dom@18.2.0",
    "https://esm.sh/lucide-react@0.292.0?deps=react@18.2.0",
    "https://esm.sh/lucide-react@0.487.0?deps=react@18.2.0",
]

print("\n── ESM modules ──────────────────────────────────────────────────────────")
for ep in _ENTRY_POINTS:
    download_esm(ep)

print("\nDone. All libraries downloaded to libs/")
