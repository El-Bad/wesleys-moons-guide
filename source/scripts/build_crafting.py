"""Crafting data -> moons.json 'craft': recipes (Gratar/Galetry fabricators), ingredient items per resource, floppy disc machines.
Run after build_items.py:  python -X utf8 scripts/build_crafting.py .
"""
import sys, json, re
S = sys.argv[1]
W = {p.split('\n', 1)[0]: p for p in open(S + '/dump/wesley.txt', encoding='utf-8').read().split('\n\n######## ')[1:]}

RES = ['Plastic stock', 'Steel', 'Circuit board', 'Copper wiring', 'Lithium', 'Rubber', 'Cables', 'Chemicals']
def res(name):
    n = name.strip().lower()
    for r in RES:
        if n.startswith(r.lower()) or (r == 'Cables' and n.startswith('cable')) or (r == 'Chemicals' and n.startswith('chemical')): return r
    raise ValueError(name)

def clean(t):
    t = re.sub(r'\{\{spoiler\|(.*?)\}\}', r'\1', t)
    t = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[https?://\S+ ([^\]]+)\]', r'\1', t)
    t = re.sub(r"'''?", '', t).replace('<br>', ' ')
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', t)).strip()

def recipes(page):
    t = W[page]; i = t.find('! Equipment Name'); j = t.find('|}', i)
    out = {}
    for line in t[i:j].split('\n'):
        if not line.startswith('| ') : continue
        c = [x.strip() for x in line[2:].split('||')]
        m = re.match(r'(.*?)\s+(\d+)x$', c[0])
        cost = [[int(q), res(r)] for q, r in re.findall(r'(\d+)\s+([A-Za-z ]+?)(?=<br>|$)', c[3])]
        out[m.group(1)] = {'n': m.group(1), 'yield': int(m.group(2)), 'w': c[2], 'cost': cost, 'use': clean(c[4])}
    return out

gal, gra = recipes('Galetry'), recipes('Gratar')
R = []
for n in list(gra) + [k for k in gal if k not in gra]:
    r = dict(gra.get(n) or gal[n]); r['at'] = [s for s, d in (('Gratar', gra), ('Galetry', gal)) if n in d]
    R.append(r)

# ingredient items (Items page)
t = W['Items']; i = t.find('! Ingredient Name'); j = t.find('|}', i)
ING = {r: [] for r in RES}
for line in t[i:j].split('\n'):
    if not line.startswith('| '): continue
    c = [x.strip() for x in line[2:].split('||')]
    q, rn = re.match(r'(\d+)\s+(.*)', c[7]).groups()
    locs = [clean(x) for x in c[8].split('<br>') if x.strip()]
    ING[res(rn)].append({'n': c[0], 'gives': int(q), 'w': c[3], 'two': c[0].lower().startswith('large'), 'locs': locs})

FLOPPY = [
    ['Fission-C', 'outside', 'Selector'],
    ['Selector', 'outside, at the bottom of the chasm (take an elevator behind the ship)', 'Dormant'],
    ['Dormant', 'through the lone interior fire exit, across a mined, overgrown area (jetpack or TZP helps)', 'Xenphir'],
    ['Etern', 'outside', 'Dune'],
    ['Chasm', 'outside', 'Spine'],
    ['Trite', 'outside', 'Heap'],
]
for a, w, b in FLOPPY:  # sanity check against the dump
    assert re.search(r'[Ff]loppy disc machine.{0,120}' + re.escape(a) + r'.{0,80}' + re.escape(b), W[b], re.S) or b in W[a], (a, b)

mj = json.load(open(S + '/build/data/moons.json', encoding='utf-8'))
for L in ING.values():
    for i in L: i['img'] = (mj.get('items', {}).get(i['n'].lower()) or {}).get('img', '')
mj['craft'] = {'recipes': R, 'ing': ING, 'res': RES, 'floppy': FLOPPY}
json.dump(mj, open(S + '/build/data/moons.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(R), 'recipes;', {k: len(v) for k, v in ING.items()})
for r in R: print(r['n'], r['yield'], r['at'], r['cost'])
