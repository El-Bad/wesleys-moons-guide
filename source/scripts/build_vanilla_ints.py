"""Download entrance pictures for the 3 vanilla interiors -> build/data/vints.json (merged into moons.json as 'vintImgs')."""
import sys, json, io, os, time, urllib.request, urllib.parse
from PIL import Image
S = sys.argv[1]
def get(u):
    for i in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'wiki-reader/1.0'}), timeout=60).read()
        except Exception:
            if i == 3: raise
            time.sleep(2 + 2 * i)
FILES = {'facility': 'Factorymainentrance.webp', 'mansion': 'Mansionmainentrance.webp', 'mineshaft': 'MinesEntrance.png'}
out = {}
for k, fn in FILES.items():
    outn = f'V_int_{k}.webp'; path = os.path.join(S, 'build', 'img', outn)
    if not os.path.exists(path):
        info = json.loads(get('https://lethal.miraheze.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&iiurlwidth=640&titles=' + urllib.parse.quote('File:' + fn)))
        ii = next(iter(info['query']['pages'].values())).get('imageinfo', [{}])[0]
        url = ii.get('thumburl') or ii.get('url')
        if not url: print('missing', fn); continue
        img = Image.open(io.BytesIO(get(url))).convert('RGB'); img.thumbnail((640, 640)); img.save(path, 'WEBP', quality=80)
    out[k] = 'img/' + outn
p = S + '/build/data/moons.json'
mj = json.load(open(p, encoding='utf-8')); mj['vintImgs'] = out
json.dump(mj, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(out)
