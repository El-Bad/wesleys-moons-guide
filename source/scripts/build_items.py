import sys, re, json
S = sys.argv[1]
W = {p.split('\n', 1)[0]: p for p in open(S + '/dump/wesley.txt', encoding='utf-8').read().split('\n\n######## ')[1:]}
L = {p.split('\n', 1)[0]: p for p in open(S + '/dump/lethal.txt', encoding='utf-8').read().split('\n\n######## ')[1:]}

def strip(t):
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    t = re.sub(r'<ref[^>]*/>|<ref[^>]*>.*?</ref>', '', t, flags=re.S)
    t = re.sub(r'\{\{\s*[Ss]poiler\s*\|((?:(?!\{\{|\}\}).)*)\}\}', lambda m: m.group(1), t, flags=re.S)
    for _ in range(6):
        t2 = re.sub(r'\{\{[^{}]*\}\}', '', t)
        if t2 == t: break
        t = t2
    t = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[https?://\S+ ([^\]]+)\]', r'\1', t)
    t = re.sub(r'<br\s*/?>', '; ', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = t.replace("'''", '').replace("''", '')
    t = re.sub(r'\s+', ' ', t).strip()
    return t.replace('.;', '.').replace('. ;', '.')

items = {}
def add(name, typ, does, **kw):
    name = strip(name)
    if not name: return
    k = name.lower()
    cur = items.get(k)
    entry = {'n': name, 't': typ, 'd': does}
    entry.update({a: b for a, b in kw.items() if b})
    PRI = {'Destiny item': 9, 'Key item': 8, 'Craftable': 7, 'Videotape': 6, 'Loggable': 5, 'Ingredient': 4, 'Reward': 3, 'Action figure': 2, 'Vanilla': 1, 'Scrap': 0}
    if cur:
        if PRI.get(typ, 1) > PRI.get(cur['t'], 1): items[k] = {**cur, **entry}
        else:
            for a, b in entry.items(): cur.setdefault(a, b)
    else:
        items[k] = entry

it = W['Items']
def section(title):
    i = it.find('== ' + title); j = it.find('\n== ', i + 5)
    return it[i:j if j > 0 else None]
PREV = {}
def rows(sec):
    out = []
    for r in sec.split('|-'):
        if '||' not in r: continue
        pm = re.search(r'\{\{Item Preview\|([^}|]+)', r)
        r = re.sub(r'\{\{Item Preview\|[^}]*\}\}', '', r)
        r = r.strip().lstrip('|').strip()
        if pm:
            nm0 = strip(re.split(r'\|\|', r)[0]).lower()
            PREV.setdefault(nm0, pm.group(1).strip())
        r = r.split('\n|}')[0]
        c = [x.strip() for x in re.split(r'\|\|', r)]
        out.append(c)
    return out
def val(c, i):
    # handle colspan="3" | N
    return strip(c[i]) if i < len(c) else ''

for c in rows(section("Wesley's Scrap")):
    if len(c) < 8: continue
    mn, av, mx = val(c, 4), val(c, 5), val(c, 6)
    add(c[0], 'Scrap', f'Scrap to sell (about {av} credits, range {mn}–{mx}). No special use listed on the wiki.',
        v=f'{mn}–{mx}', w=val(c, 3), two=val(c, 7), where=val(c, 8))
for c in rows(section('Loggable Items')):
    if len(c) < 8: continue
    un = val(c, 7)
    add(c[0], 'Loggable', ('Take it to a log translator to read it. ' + (f'Translating it unlocks {un}.' if un and un != '-' else 'Story only, no unlock.')) + ' Can also be sold.',
        v=f'{val(c,4)}–{val(c,6)}', w=val(c, 3), where=val(c, 8))
for c in rows(section('Videotapes')):
    if len(c) < 6: continue
    un = val(c, 5)
    add(c[0], 'Videotape', f'Play it in the projector on Galetry\'s top floor. Unlocks {un}.' if un and un != '-' else 'Videotape for the Galetry projector.',
        v=f'{val(c,2)}–{val(c,4)}', where=val(c, 6))
for c in rows(section('Ingredient Items')):
    if len(c) < 8: continue
    add(c[0], 'Ingredient', f'Crafting material. Deposit it in a fabricator (Gratar, or Galetry\'s fire exit) for {val(c,7)}. Or sell it.',
        v=f'{val(c,4)}–{val(c,6)}', w=val(c, 3), where=val(c, 8))
for c in rows(section('Key Items')):
    if len(c) < 9: continue
    add(c[0], 'Key item', f'Needed on {val(c,9)}. Found: {val(c,8)}.', v=f'{val(c,4)}–{val(c,6)}', w=val(c, 3), two=val(c, 7))
for c in rows(section('Reward Items')):
    if len(c) < 6: continue
    add(c[0], 'Reward', f'Puzzle or trial reward from {c[-1] and strip(c[-1])}. Sell it.', w=val(c, 3))
for c in rows(section('Destiny Items')):
    if len(c) < 8: continue
    add(c[0], 'Destiny item', f'Put it in the destiny slot of the abandoned ship on Repress to get the "{val(c,8)}" ending. Don\'t sell it.',
        v=f'{val(c,4)}–{val(c,6)}', w=val(c, 3), where=val(c, 7))
for c in rows(section('Action Figures')):
    if len(c) < 3: continue
    add(c[0], 'Action figure', 'Used in the Action Figure Battle board in Galetry\'s gift shop.')

# crafting recipes (Gratar page)
g = W['Gratar']
i = g.find('Crafting Recipes'); j = g.find('|}', i)
for c in rows(g[i:j]):
    if len(c) < 5: continue
    nm = re.sub(r'\s+\d+x$', '', strip(c[0]))
    add(nm, 'Craftable', strip(c[4]) + f' Recipe: {strip(c[3])}.', w=val(c, 2))
    if nm == 'Operating panel': add('Untampered operating panel', 'Key item', 'Repairs the abandoned ship on Repress (needed for every ending). 7000 in the Galetry gift shop, crafted on Gratar, or found on Hyx/Empra. Recipe: ' + strip(c[3]) + '.')

# vanilla items from the Lethal Company wiki
for t, p in L.items():
    if '/' in t or '{{autoinfobox item' not in p: continue
    body = re.sub(r'<!--T:\d+-->|</?translate>', '', p)
    body = re.sub(r'\{\{\s*[Tt]erminal.*?\}\}', '', body, flags=re.S)
    raw = re.split(r'\n\s*\n', body)
    pref = [x for x in raw if "'''" in x and not x.strip().startswith(('{', '|', '!', '='))]
    paras = [strip(x) for x in (pref or raw)]
    paras = [x for x in paras if len(x) > 40 and not x.startswith('=') and 'Company description' not in x]
    if len(paras) > 1 and len(paras[0]) < 160: paras[0] = paras[0] + ' ' + paras[1]
    if not paras: continue
    d = paras[0]
    if len(d) > 420: d = d[:420].rsplit('. ', 1)[0] + '.'
    add(t, 'Vanilla', d, link='https://lethal.miraheze.org/wiki/' + t.replace(' ', '_'))

# notes from our own research (override/extend)
NOTES = {
 'Chainsaw': ('Weapon + scrap', 'A melee weapon since mod v5.0.0 (damage not documented). Sells for ~82. Sold in the Galetry gift shop; common on Gloom.'),
 'Hairdryer': ('Vanilla', 'Noisemaker: makes a loud sound (10 uses on its battery) that players and sound-hunting enemies hear. Can lure Eyeless Dogs away, but also gives you away. Otherwise sell (~80).'),
 'Homemade spore-emitter': ('Scrap', 'Scrap worth 12–36. The wiki lists no use for it. Not the same as the crafted Pulatrum spore emitter (which heals).'),
 'BIO-HXNV7': ('Scrap', 'Valuable scrap (128–200) on Asteroid-13. Lore: the bio-weapon behind the Coil-Heads. Picking it up is harmless. Sell it.'),
 'Golden mask': ('Scrap', 'Valuable scrap (116–136, 38 lb). Lore item from Junic\'s Desmond notes. Not needed for the ritual (that needs Jack\'s skull). Sell it.'),
 "Jack's skull": ('Key item', 'Hold it while stepping into Junic\'s ritual circle to survive. Opens a shortcut and reveals the cubic skull that unlocks Roart. Spawns inside Junic or in the Galetry gift shop.'),
 'Mrov Sauce': ('Scrap', 'MorvDonalds\' main scrap: about 101 credits each at 7 lb. The reason that moon is great money.'),
 "Beholder's eye": ('Apparatus', 'The Atlantean Citadel\'s apparatus: 180 credits, two-handed, 36 lb. Behind a door that needs a Dungeon key. Taking the first one floods the interior for ~2 minutes. On Thalasso it opens the Heart Chamber.'),
 'Dungeon key': ('Key item', 'Opens a Beholder\'s Eye door in the Atlantean Citadel. Two always spawn.'),
 'Floppy disk': ('Loggable', 'Translate it at a log translator to unlock Dreck. Random scrap (best odds: Titan, Galetry gift shop, Roart). Different from the crafted Blank floppy disc.'),
 'Blank floppy disc': ('Craftable', 'Craft on Galetry (2 Plastic stock, 1 Circuit boards, 3 Copper wiring). Insert into a moon\'s Floppy disc machine to make that moon\'s unlock disc (Selector, Dormant, Xenphir, Dune, Spine, Heap).'),
 'Weed killer': ('Vanilla', 'Kills Cadaver Growths and Vain Shrouds; cures an infected teammate before 100% infection (8 damage to them). ~30 s of spray per bottle. Also repairs and boosts the Company Cruiser.'),
 'Failsafe floppy disc': ('Galetry', 'Under the right-hand counter of the Galetry gift shop (mod v7.0.0+). Translate it to re-unlock moons that vanished from your save.'),
 'Quick start floppy disk': ('Galetry', 'On Galetry. Translate it to unlock Asteroid-13, Infernis and Motra at once.'),
 'Apparatus': ('Vanilla', 'Sell for ~80, or keep one for the Repress ship repair (needed for every ending). Pulling it cuts the building\'s power.'),
 'Huge harold': ('Key item', 'Needed on Empra (placed in the cart with an apparatus) for Ending 2.'),
}
for n, (t, d) in NOTES.items():
    k = n.lower()
    if k in items: items[k]['d'] = d; items[k]['t'] = t
    else: add(n, t, d)

IMGMAP = json.load(open(S + '/build/imgmap.json'))
for k, v in items.items():
    cands = [PREV.get(k), v['n'] + '.png', v['n'].capitalize() + '.png', v['n'].title() + '.png', '(Lore) ' + v['n'] + '.png']
    for c in cands:
        if not c: continue
        f = IMGMAP.get(c.replace(' ', '_'))
        if f: v['img'] = 'img/' + f; break
print('with images', sum(1 for v in items.values() if 'img' in v), 'of', len(items))
json.dump(items, open(S + '/build/data/items.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
from collections import Counter
print(len(items), Counter(v['t'] for v in items.values()))
for k in ['pulatrum spore emitter', 'health stim', 'shovel', 'cables', 'ticket teach the disloyal', 'harrington\'s research log 4', 'airhorn', 'acidir videotape']:
    print(k, '->', items.get(k))
