import sys, os, io, re, json, base64
from PIL import Image
B, OUTFILE = sys.argv[1], sys.argv[2]
MAXW_CONTENT, MAXW_MAP, Q = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])

h = open(B + '/index.html', encoding='utf-8').read()
pj = open(B + '/data/pages.json', encoding='utf-8').read()
mj = open(B + '/data/moons.json', encoding='utf-8').read()

# only images actually referenced
used = set(re.findall(r'img/([A-Za-z0-9._()\-]+\.(?:webp|svg))', pj + mj + h))
imgs = {}
total = 0
for fn in sorted(used):
    path = os.path.join(B, 'img', fn)
    if not os.path.exists(path): continue
    if fn.endswith('.svg'):
        data = open(path, 'rb').read(); mime = 'image/svg+xml'
    else:
        im = Image.open(path)
        mw = MAXW_MAP if fn.endswith('-map.webp') else (128 if fn.startswith('icon_') else MAXW_CONTENT)
        if im.width > mw: im = im.resize((mw, round(im.height * mw / im.width)), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, 'WEBP', quality=(85 if fn.startswith('icon_') or im.width <= 128 else Q), method=6)
        data = buf.getvalue(); mime = 'image/webp'
    imgs['img/' + fn] = f'data:{mime};base64,' + base64.b64encode(data).decode()
    total += len(data)

esc = lambda t: t.replace('</', '<\\/')
a = 'const [pj, mj] = await Promise.all([fetch("data/pages.json").then(r => r.json()), fetch("data/moons.json").then(r => r.json())]);'
assert a in h
h = h.replace(a, 'const pj = JSON.parse(document.getElementById("pages-data").textContent), mj = JSON.parse(document.getElementById("moons-data").textContent);')
# swap img/... paths for embedded data whenever anything is rendered
fixer = r'''
const IMGS = JSON.parse(document.getElementById("img-data").textContent);
function fixImgs(root){
  if (!root || !root.querySelectorAll) return;
  root.querySelectorAll('img[src^="img/"]').forEach(i => { const d = IMGS[i.getAttribute("src")]; if (d) i.src = d; });
  root.querySelectorAll('image[href^="img/"]').forEach(i => { const d = IMGS[i.getAttribute("href")]; if (d) i.setAttribute("href", d); });
}
new MutationObserver(ms => ms.forEach(m => { m.addedNodes.forEach(n => { if (n.nodeType === 1){ if (n.matches && n.matches('img[src^="img/"],image[href^="img/"]')) fixImgs(n.parentNode); else fixImgs(n); } }); if (m.type === "attributes") fixImgs(m.target.parentNode); })).observe(document.documentElement, {childList: true, subtree: true, attributes: true, attributeFilter: ["src", "href"]});
'''
h = h.replace('<script>\n"use strict";',
  '<script type="application/json" id="pages-data">' + esc(pj) + '</script>\n'
  '<script type="application/json" id="moons-data">' + esc(mj) + '</script>\n'
  '<script type="application/json" id="img-data">' + esc(json.dumps(imgs, separators=(',', ':'))) + '</script>\n'
  '<script>\n"use strict";' + fixer, 1)
open(OUTFILE, 'w', encoding='utf-8').write(h)
print('images', len(imgs), 'raw MB', round(total / 1e6, 1), 'file MB', round(os.path.getsize(OUTFILE) / 1e6, 1))
