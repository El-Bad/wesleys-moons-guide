"""Vanilla entity list from the Lethal Company wiki -> build/data/vents.json, images into build/img.
Run after build.py/post_build.py:  python -X utf8 scripts/build_vanilla_ents.py .
"""
import sys, re, json, os, io, hashlib, urllib.request, urllib.parse, time
from bs4 import BeautifulSoup
from PIL import Image
S = sys.argv[1]
UA = {'User-Agent': 'wiki-reader/1.0'}
def get(u):
    for i in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
        except Exception:
            if i == 3: raise
            time.sleep(2 + 2 * i)

L = {p.split('\n', 1)[0]: p for p in open(S + '/dump/lethal.txt', encoding='utf-8').read().split('\n\n######## ')[1:]}
h = json.loads(get('https://lethal.miraheze.org/w/api.php?action=parse&page=Entities&prop=text&format=json&formatversion=2'))['parse']['text']
soup = BeautifulSoup(h, 'lxml')

def strip(t):
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    t = re.sub(r'</?translate>|<tvar[^>]*>|</tvar>', '', t)
    t = re.sub(r'<ref[^>]*/>|<ref[^>]*>.*?</ref>', '', t, flags=re.S)
    for _ in range(6):
        t2 = re.sub(r'\{\{[^{}]*\}\}', '', t)
        if t2 == t: break
        t = t2
    t = re.sub(r'\[\[(?:File|Image):[^\]]*\]\]', '', t)
    t = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[https?://\S+ ([^\]]+)\]', r'\1', t)
    t = re.sub(r'<br\s*/?>', ' ', t); t = re.sub(r'<[^>]+>', '', t)
    t = t.replace("'''", '').replace("''", '')
    t = re.sub(r'(?m)^\s*[*#:]+\s*', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()
def paras(block):
    block = re.sub(r'<!--.*?-->|</?translate>', '', block, flags=re.S)
    block = '\n'.join(l for l in block.split('\n') if not re.fullmatch(r'\s*\{\{[^{}]*\}\}\s*', l))
    out = []
    for x in re.split(r'\n\s*\n', block):
        x = x.strip()
        if not x or x.startswith(('{|', '|', '!', '[[File', '[[Category', '{{')): continue
        y = strip(x)
        if len(y) > 40: out.append(y)
    return out
def cut(t, n):
    if len(t) <= n: return t
    t = t[:n]; return (t.rsplit('. ', 1)[0] + '.') if '. ' in t else t.rsplit(' ', 1)[0] + '…'
def section(p, name):
    m = re.search(r'^==\s*' + name + r'\s*==.*?$(.*?)(?=^==[^=]|\Z)', p, re.S | re.M)
    return m.group(1) if m else ''

def safe(n):
    b = re.sub(r'[^A-Za-z0-9._-]', '_', n.rsplit('.', 1)[0])[:60]
    return b + '-' + hashlib.md5(n.encode()).hexdigest()[:6]

MANUAL = {
 'Backwater Gunkfish': 'Lives in water. Stay out of deep water where you can and kill it with a weapon or shovel (4 HP) if it comes for you.',
 'Cadaver Bloom': 'What an infected employee becomes. Spray Weed killer on infected teammates before 100% infection to cure them. If a Bloom appears, keep distance and fight it as a group; shotguns only do 1 damage to it.',
 'Cadaver Growth': 'Plants that infect you. Spray them with Weed killer to destroy them and avoid walking through patches. Cure infected teammates with Weed killer before they reach 100%.',
 'Mask Hornets': 'Guard a hive. Leave the hive alone unless you want it as scrap; if you grab it, run straight for the ship without stopping.',
 'Feiopar': 'Fast outdoor predator at night. Get back to the ship before dark, move in groups and carry a weapon (4 HP).',
 'Kidnapper Fox': 'Hides in the biggest patch of Vain Shrouds. Spray shrouds with Weed killer to prevent it and stay out of large patches. If its tongue grabs you, teammates should hit it to make it let go.',
 'Manticoil': 'Harmless bird. Ignore it, or kill it with one shovel hit for its body as scrap.',
 'Roaming Locusts': 'Harmless swarm that scatters when you get close. Just walk through.',
}
out = []
GROUPS = {'Indoor': 'Indoor', 'Nighttime (Outdoor)': 'Outdoor (night)', 'Daytime (Outdoor)': 'Outdoor (day)'}
for hd in soup.find_all(['h3']):
    g = GROUPS.get(hd.get_text(strip=True))
    if not g: continue
    tb = hd.find_next('table')
    head = [c.get_text(' ', strip=True) for c in tb.find('tr').find_all(['th', 'td'])]
    for r in tb.find_all('tr')[1:]:
        c = r.find_all(['th', 'td'])
        if len(c) < len(head): continue
        cell = dict(zip(head, c))
        name = re.sub(r'\s*\[.*?\]', '', cell['Name'].get_text(' ', strip=True)).strip()
        a = cell['Name'].find('a'); title = urllib.parse.unquote(a['href'].split('/wiki/')[-1]).replace('_', ' ') if a and '/wiki/' in a.get('href', '') else name
        hp = cell['Health'].get_text(' ', strip=True)
        hp = re.sub(r'\s*\[.*?\]', '', hp)
        if 'Multiplayer' in hp: hp = '8 (2 solo)'
        elif 'Baby' in hp: hp = '∞ baby, 5 adult'
        else: hp = hp.split(' ')[0]
        stun = 'Yes' in cell['Stunnable'].get_text()
        p = L.get(title) or next((v for k, v in L.items() if k.lower() == title.lower()), '')
        intro = paras(re.split(r'^==', re.sub(r'\{\{Infobox.*?\n\}\}', '', p, flags=re.S), flags=re.M)[0])
        strat = paras(section(p, 'Strategy'))
        e = {'n': name, 'g': g, 'hp': hp, 'stun': stun, 'd': cut(intro[0], 300) if intro else '',
             's': cut(' '.join(strat), 420) if strat else '',
             'link': 'https://lethal.miraheze.org/wiki/' + urllib.parse.quote(title.replace(' ', '_'))}
        im = cell.get('Image') and cell['Image'].find('img')
        if im:
            fn = urllib.parse.unquote(re.search(r'/(?:thumb/)?[0-9a-f]/[0-9a-f]{2}/([^/?]+)', im['src']).group(1)) if re.search(r'/[0-9a-f]/[0-9a-f]{2}/', im['src']) else None
            if fn:
                outn = safe('V_' + fn) + '.webp'; path = os.path.join(S, 'build', 'img', outn)
                if not os.path.exists(path):
                    info = json.loads(get('https://lethal.miraheze.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&iiurlwidth=420&titles=' + urllib.parse.quote('File:' + fn)))
                    pg = next(iter(info['query']['pages'].values()))
                    url = pg.get('imageinfo', [{}])[0].get('thumburl') or pg.get('imageinfo', [{}])[0].get('url')
                    if url:
                        img = Image.open(io.BytesIO(get(url)))
                        img = img.convert('RGBA') if img.mode in ('P', 'LA') else img
                        img.thumbnail((420, 420)); img.save(path, 'WEBP', quality=80)
                if os.path.exists(path): e['img'] = 'img/' + outn
        if name == 'Backwater Gunkfish': e['d'] = 'A fish-like creature that lives in water inside the facility (added in v80).'
        if not e['s'] and name in MANUAL: e['s'] = MANUAL[name]
        out.append(e)
        print(g, name, hp, stun, 'img' in e, len(e['d']), len(e['s']))
json.dump(out, open(S + '/build/data/vents.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
mj = json.load(open(S + '/build/data/moons.json', encoding='utf-8'))
mj['vents'] = out
json.dump(mj, open(S + '/build/data/moons.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(out), 'vanilla entities')
