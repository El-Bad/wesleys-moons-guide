"""Est. loot for vanilla moons from the Lethal Company wiki loot tables -> moons.json.
est = average scrap count x spawn-chance-weighted mean item value (same formula as the mod moons).
Run after post_build.py:  python -X utf8 scripts/build_vanilla_loot.py .
"""
import sys, json, re, time, urllib.request, urllib.parse
from bs4 import BeautifulSoup
S = sys.argv[1]
def get(u):
    for i in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'wiki-reader/1.0'}), timeout=60).read()
        except Exception:
            if i == 3: raise
            time.sleep(2 + 2 * i)
num = lambda t: float(re.sub(r'[^\d.]', '', t) or 'nan')
p = S + '/build/data/moons.json'
mj = json.load(open(p, encoding='utf-8'))
for n, m in mj['moons'].items():
    if not m.get('vanilla') or not m.get('scrap') or not m['scrap'][1]: continue
    h = json.loads(get('https://lethal.miraheze.org/w/api.php?action=parse&format=json&formatversion=2&prop=text&page=' + urllib.parse.quote(n)))['parse']['text']
    hd = BeautifulSoup(h, 'lxml').find(id='Loot_table')
    if not hd: print('no loot table', n); continue
    tot = w = 0
    for r in hd.find_next('table').find_all('tr'):
        c = [x.get_text(' ', strip=True) for x in r.find_all(['td', 'th'])]
        if len(c) >= 5 and c[1].endswith('%'):
            ch, mean = num(c[1]), num(c[3])
            if ch == ch and mean == mean: tot += ch * mean; w += ch
    if w:
        avg = tot / w; mn, mx = m['scrap']
        m['avgItem'] = round(avg); m['est'] = round(avg * (mn + mx) / 2)
    print(n, m['scrap'], m['avgItem'], m['est'])
json.dump(mj, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
