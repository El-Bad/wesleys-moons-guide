import sys, shutil, os
B, OUT = sys.argv[1], sys.argv[2]
h = open(B + '/index.html', encoding='utf-8').read()
pj = open(B + '/data/pages.json', encoding='utf-8').read().replace('</', '<\\/')
mj = open(B + '/data/moons.json', encoding='utf-8').read().replace('</', '<\\/')
a = 'const [pj, mj] = await Promise.all([fetch("data/pages.json").then(r => r.json()), fetch("data/moons.json").then(r => r.json())]);'
assert a in h
h = h.replace(a, 'const pj = JSON.parse(document.getElementById("pages-data").textContent), mj = JSON.parse(document.getElementById("moons-data").textContent);')
h = h.replace('<script>\n"use strict";', '<script type="application/json" id="pages-data">' + pj + '</script>\n<script type="application/json" id="moons-data">' + mj + '</script>\n<script>\n"use strict";', 1)
os.makedirs(OUT, exist_ok=True)
open(OUT + '/index.html', 'w', encoding='utf-8').write(h)
if os.path.exists(OUT + '/img'): shutil.rmtree(OUT + '/img')
shutil.copytree(B + '/img', OUT + '/img')
print(os.path.getsize(OUT + '/index.html'), len(os.listdir(OUT + '/img')))
