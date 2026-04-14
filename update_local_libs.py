"""
Rewrites every HTML file in the project to load libraries from the local
libs/ folder instead of CDN URLs.

Run once from the project root:  python update_local_libs.py
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
LIBS = os.path.join(ROOT, "libs")

# ── helpers ──────────────────────────────────────────────────────────────────

def lib_rel(html_path, *lib_subpath):
    """Return a URL-style relative path from an HTML file to a libs/ sub-path."""
    abs_lib = os.path.join(LIBS, *lib_subpath)
    rel = os.path.relpath(abs_lib, os.path.dirname(html_path))
    return rel.replace("\\", "/")

def update(html_path, old, new):
    """Replace first/all occurrences; returns changed text."""
    return old

# ── per-file rewrite ──────────────────────────────────────────────────────────

def rewrite(html_path):
    with open(html_path, encoding="utf-8") as f:
        src = f.read()

    original = src

    # --- compute relative lib paths for this specific file ----------------
    R = lambda *p: lib_rel(html_path, *p)

    # Tailwind Play CDN (JS)
    src = re.sub(
        r'https://cdn\.tailwindcss\.com',
        R("tailwind.cdn.js"),
        src,
    )

    # Tailwind v2 CSS (jsdelivr)
    src = re.sub(
        r'https://cdn\.jsdelivr\.net/npm/tailwindcss@2[\w.\-]*/dist/tailwind\.min\.css',
        R("tailwind.v2.min.css"),
        src,
    )

    # React 18 UMD
    src = re.sub(
        r'https://unpkg\.com/react@18/umd/react\.production\.min\.js',
        R("react.production.min.js"),
        src,
    )
    src = re.sub(
        r'https://unpkg\.com/react@18/umd/react\.development\.js',
        R("react.production.min.js"),
        src,
    )

    # ReactDOM 18 UMD
    src = re.sub(
        r'https://unpkg\.com/react-dom@18/umd/react-dom\.production\.min\.js',
        R("react-dom.production.min.js"),
        src,
    )
    src = re.sub(
        r'https://unpkg\.com/react-dom@18/umd/react-dom\.development\.js',
        R("react-dom.production.min.js"),
        src,
    )

    # Babel standalone
    src = re.sub(
        r'https://unpkg\.com/@babel/standalone/babel\.min\.js',
        R("babel.min.js"),
        src,
    )

    # Lucide React UMD
    src = re.sub(
        r'https://unpkg\.com/lucide-react(?:@[\w.\-]*)?/dist/umd/lucide-react\.min\.js',
        R("lucide-react.min.js"),
        src,
    )

    # Lucide vanilla UMD (non-react version)
    src = re.sub(
        r'https://unpkg\.com/lucide(?:@latest)?(?:/dist/umd/lucide\.min\.js)?(?=["\s])',
        R("lucide.min.js"),
        src,
    )

    # framer-motion UMD
    src = re.sub(
        r'https://unpkg\.com/framer-motion@[\w.\-]*/dist/framer-motion\.js',
        R("framer-motion.js"),
        src,
    )

    # Font Awesome CSS
    src = re.sub(
        r'https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[\w.\-]*/css/all\.min\.css',
        R("font-awesome", "all.min.css"),
        src,
    )

    # reveal.js 5 from jsdelivr
    src = re.sub(
        r'https://cdn\.jsdelivr\.net/npm/reveal\.js@5/dist/reveal\.css',
        R("reveal", "dist", "reveal.css"),
        src,
    )
    src = re.sub(
        r'https://cdn\.jsdelivr\.net/npm/reveal\.js@5/dist/reveal\.js',
        R("reveal", "dist", "reveal.js"),
        src,
    )
    src = re.sub(
        r'https://cdn\.jsdelivr\.net/npm/reveal\.js@5/dist/theme/([\w\-]+\.css)',
        lambda m: R("reveal", "dist", "theme", m.group(1)),
        src,
    )
    src = re.sub(
        r'https://cdn\.jsdelivr\.net/npm/reveal\.js@5/plugin/highlight/highlight\.js',
        R("reveal", "plugin", "highlight", "highlight.js"),
        src,
    )
    src = re.sub(
        r'https://cdn\.jsdelivr\.net/npm/reveal\.js@5/plugin/highlight/monokai\.css',
        R("reveal", "plugin", "highlight", "monokai.css"),
        src,
    )
    src = re.sub(
        r'https://cdn\.jsdelivr\.net/npm/reveal\.js@5/plugin/markdown/markdown\.js',
        R("reveal", "plugin", "markdown", "markdown.js"),
        src,
    )
    src = re.sub(
        r'https://cdn\.jsdelivr\.net/npm/reveal\.js@5/plugin/notes/notes\.js',
        R("reveal", "plugin", "notes", "notes.js"),
        src,
    )
    src = re.sub(
        r'https://cdn\.jsdelivr\.net/npm/reveal\.js@5/plugin/zoom/zoom\.js',
        R("reveal", "plugin", "zoom", "zoom.js"),
        src,
    )
    src = re.sub(
        r'https://cdn\.jsdelivr\.net/npm/reveal\.js@5/plugin/search/search\.js',
        R("reveal", "plugin", "search", "search.js"),
        src,
    )
    src = re.sub(
        r'https://cdn\.jsdelivr\.net/npm/reveal\.js@5/plugin/math/math\.js',
        R("reveal", "plugin", "math", "math.js"),
        src,
    )

    # ── ESM importmap handling ───────────────────────────────────────────
    filename = os.path.basename(html_path)

    if filename in ("03stack-and-queue.html", "05sets.html"):
        src = _convert_importmap_to_umd(src, html_path)

    if filename == "08recursion-spa.html":
        # Replace dynamic esm.sh lucide import with UMD global access
        src = re.sub(
            r'const loadLucide\s*=\s*\(\)\s*=>\s*import\s*\(\s*["\']https://esm\.sh/lucide-react[^"\']*["\']\s*\)',
            (
                "// lucide-react loaded from local UMD build\n"
                "    const loadLucide = () => Promise.resolve(window.LucideReact)"
            ),
            src,
        )
        # Add local lucide-react UMD script tag before the main script if not present
        if R("lucide-react.min.js") not in src:
            # Insert after babel script tag
            babel_tag = re.search(
                r'(<script[^>]+babel\.min\.js[^>]*></script>)',
                src,
            )
            if babel_tag:
                insert_pos = babel_tag.end()
                inject = (
                    "\n  <!-- lucide-react UMD -->\n"
                    "  <script>\n"
                    "    window.react = window.React; // needed by lucide-react UMD\n"
                    "  </script>\n"
                    f'  <script src="{R("lucide-react.min.js")}"></script>\n'
                )
                src = src[:insert_pos] + inject + src[insert_pos:]

    if src != original:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(src)
        print(f"  [updated] {os.path.relpath(html_path, ROOT)}")
    else:
        print(f"  [no change] {os.path.relpath(html_path, ROOT)}")


def _convert_importmap_to_umd(src, html_path):
    """
    For files that use <script type="importmap"> + import statements:
    1. Remove the importmap block
    2. Inject UMD script tags (react, react-dom, framer-motion, lucide-react)
       before existing babel/babel-adjacent tags
    3. Strip ES6 import lines from the babel script body
    4. Change data-type="module" → remove that attribute
    """
    R = lambda *p: lib_rel(html_path, *p)

    # 1. Remove the importmap block
    src = re.sub(
        r'<script\s+type=["\']importmap["\'][^>]*>.*?</script>\s*',
        '', src, flags=re.DOTALL
    )

    # 2. The UMD shims to inject
    umd_block = (
        '\n  <!-- Local UMD libraries (replaces importmap) -->\n'
        f'  <script crossorigin src="{R("react.production.min.js")}"></script>\n'
        f'  <script crossorigin src="{R("react-dom.production.min.js")}"></script>\n'
        '  <script>\n'
        '    window.react = window.React; // needed by lucide-react UMD\n'
        '  </script>\n'
        f'  <script src="{R("framer-motion.js")}"></script>\n'
        f'  <script src="{R("lucide-react.min.js")}"></script>\n'
    )

    # Insert before the babel script tag
    babel_pos = re.search(r'<script\s[^>]*babel\.min\.js[^>]*></script>', src)
    if babel_pos:
        src = src[:babel_pos.start()] + umd_block + src[babel_pos.start():]
    else:
        # fallback: insert before </head>
        src = src.replace('</head>', umd_block + '</head>', 1)

    # 3. Remove ES6 import lines from inside the babel script
    def strip_imports(m):
        body = m.group(0)
        # Remove static import lines
        body = re.sub(r'\s*import\s+.*?from\s+[\'"][^\'"]+[\'"]\s*;?\n?', '', body)
        # Add UMD global destructuring right after <script ...> opening tag
        # Find opening tag end
        tag_end = re.search(r'<script[^>]*>', body)
        if tag_end:
            insert_at = tag_end.end()
            shims = (
                '\n'
                '    // UMD globals (importmap replaced with local UMD builds)\n'
                '    const { useState, useEffect, useMemo, useRef, useCallback, useContext } = React;\n'
                '    const { createRoot } = ReactDOM;\n'
                '    const { motion, AnimatePresence } = Motion;\n'
                '    const LucideIcons = LucideReact;\n'
            )
            body = body[:insert_at] + shims + body[insert_at:]
        return body

    src = re.sub(
        r'<script\s[^>]*type=["\']text/babel["\'][^>]*>.*?</script>',
        strip_imports,
        src, flags=re.DOTALL,
    )

    # 4. Remove data-type="module" attribute from babel scripts
    src = re.sub(r'\s+data-type=["\']module["\']', '', src)

    return src


# ── main ──────────────────────────────────────────────────────────────────────

html_files = []
for dirpath, _, filenames in os.walk(ROOT):
    for fname in filenames:
        if fname.endswith(".html"):
            html_files.append(os.path.join(dirpath, fname))

print(f"Processing {len(html_files)} HTML files...\n")
for p in sorted(html_files):
    rewrite(p)

print("\nDone.")
