"""Fix Font Awesome: patch webfont paths and download missing files."""
import os, ssl, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))

# Fix ../webfonts/ -> webfonts/ in all.min.css
css_path = os.path.join(BASE, 'libs', 'font-awesome', 'all.min.css')
content = open(css_path, encoding='utf-8').read()
count = content.count('../webfonts/')
fixed = content.replace('../webfonts/', 'webfonts/')
open(css_path, 'w', encoding='utf-8').write(fixed)
print(f"Fixed {count} occurrences of ../webfonts/ -> webfonts/ in all.min.css")

# Download missing fa-v4compatibility files
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

wf_dir = os.path.join(BASE, 'libs', 'font-awesome', 'webfonts')
FA_BASE = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/webfonts/'
for fname in ['fa-v4compatibility.woff2', 'fa-v4compatibility.ttf']:
    dest = os.path.join(wf_dir, fname)
    if os.path.exists(dest):
        print(f"  [skip] {fname}")
        continue
    print(f"  [dl]   {fname}")
    try:
        req = urllib.request.Request(FA_BASE + fname, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
            data = r.read()
        open(dest, 'wb').write(data)
        print(f"         OK ({len(data):,} bytes)")
    except Exception as e:
        print(f"         ERROR: {e}")

print("Done.")
