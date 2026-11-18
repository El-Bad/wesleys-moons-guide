import json, sys, re, os, glob, urllib.parse, html as H
from bs4 import BeautifulSoup, NavigableString, Comment

S = sys.argv[1]
B = os.path.join(S, 'build')
imgmap = json.load(open(os.path.join(B, 'imgmap.json')))
maps_raw = json.load(open(os.path.join(B, 'maps.json'), encoding='utf-8'))
wikitext = {p.split('\n', 1)[0]: p for p in open(os.path.join(S, 'dump', 'wesley.txt'), encoding='utf-8').read().split('\n\n######## ')[1:]}

SKIP = {"Wesley's Moons Wiki", "Wesley's Moons Wiki/about", "Wesley's Moons Wiki/contribute",
        "Wesley's Moons Wiki/external", "Wesley's Moons Wiki/pages", "Wesley's Moons Wiki/welcome"}
INTERIORS = ['Art Gallery', 'Asten Lab', 'Atlantean Citadel', 'Carnival', 'Decrepit Store', 'Deep Sewers',
             'Expanded Facility', 'Expanded Mineshaft', 'Fractured Complex', 'Grand Armory', 'Greenhouse',
             'Rubber Rooms', 'Spooky Manor', 'Toy Store']
GUIDES = ['Guidebook', 'Endings', 'Items', 'Weathers', 'Moons', 'Interiors', 'Characters', 'Known Characters']

def slug(t):
    s = re.sub(r'[^a-z0-9]+', '-', t.lower().replace("'", '')).strip('-')
    return 'p-' + s

def kind(t):
    w = wikitext.get(t, '')
    if '{{Moon Infobox' in w: return 'moon'
    if '{{Entity Infobox' in w: return 'entity'
    if t in INTERIORS: return 'interior'
    return 'guide'

pages_in = {}
for f in glob.glob(os.path.join(S, 'parsed', '*.json')):
    d = json.load(open(f, encoding='utf-8'))
    if d['title'] in SKIP: continue
    pages_in[d['title']] = d
TITLE_SLUG = {t: slug(t) for t in pages_in}
VANILLA = ['Experimentation', 'Assurance', 'Vow', 'Offense', 'March', 'Adamance', 'Rend', 'Dine', 'Titan',
           'Embrion', 'Artifice', 'Gordion']
for v in VANILLA: TITLE_SLUG.setdefault(v, slug(v))

def img_local(src):
    m = re.search(r'/images/(?:thumb/)?([^/?]+)', src or '')
    if not m: return None
    n = urllib.parse.unquote(m.group(1)).replace(' ', '_')
    return imgmap.get(n)

ALLOWED = {'p', 'br', 'b', 'strong', 'i', 'em', 'u', 's', 'a', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr',
           'th', 'td', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'div', 'span', 'small', 'big', 'sup', 'sub', 'blockquote',
           'details', 'summary', 'code', 'pre', 'hr', 'caption', 'dl', 'dt', 'dd', 'abbr', 'q', 'figure', 'figcaption'}
KEEP_CLASS = {'spoiler', 'gallery', 'gal-item', 'gal-cap', 'wikitable', 'loot', 'logtable', 'terminal', 'quote'}
MEDIA_RE = re.compile(r'\.(wav|ogg|mp3|mp4|webm|flac)$', re.I)

def link_target(href):
    if not href: return None, False
    if href.startswith('/wiki/'):
        t = urllib.parse.unquote(href[6:].split('#')[0]).replace('_', ' ')
        if t.startswith('File:') or t.startswith('Special:'): return None, False
        if t in TITLE_SLUG and t in pages_in: return '#' + TITLE_SLUG[t], False
        return 'https://wesleysmoons.wiki.gg' + href, True
    if href.startswith('#'): return None, False
    m = re.match(r'https?://wesleysmoons\.wiki\.gg/wiki/([^#?]+)', href)
    if m:
        t = urllib.parse.unquote(m.group(1)).replace('_', ' ')
        if t in pages_in: return '#' + TITLE_SLUG[t], False
    if href.startswith('http'): return href, True
    if href.startswith('//'): return 'https:' + href, True
    return None, False

def clean(node):
    """Sanitize a soup subtree in place."""
    for c in node.find_all(string=lambda x: isinstance(x, Comment)): c.extract()
    for t in node.find_all(['script', 'style', 'noscript', 'audio', 'video', 'source', 'iframe', 'object', 'embed', 'form', 'input', 'button', 'link', 'meta']):
        t.decompose()
    for t in node.select('.toc, #toc, .mw-editsection, .ext-datamaps-container, .mw-empty-elt, .audio-player, .mediaContainer'):
        t.decompose()
    # media links
    for a in node.find_all('a'):
        h = a.get('href', '')
        if MEDIA_RE.search(h) or MEDIA_RE.search(a.get_text()):
            a.decompose()
    # spoilers
    for sp in node.select('.spoiler-content'):
        sp.name = 'span'; sp.attrs = {'class': ['spoiler']}
    # galleries
    for ul in node.select('ul.gallery'):
        new = BeautifulSoup('', 'lxml').new_tag('div'); new['class'] = ['gallery']
        for li in ul.select('li.gallerybox'):
            im = li.find('img'); cap = li.select_one('.gallerytext')
            if not im: continue
            fig = BeautifulSoup('', 'lxml').new_tag('figure'); fig['class'] = ['gal-item']
            im2 = BeautifulSoup('', 'lxml').new_tag('img'); im2['src'] = im.get('src', ''); im2['alt'] = im.get('alt', '')
            fig.append(im2)
            if cap and cap.get_text(strip=True):
                fc = BeautifulSoup('', 'lxml').new_tag('figcaption'); fc.string = cap.get_text(' ', strip=True); fig.append(fc)
            new.append(fig)
        ul.replace_with(new)
    # collapsible tables -> details
    for tb in node.select('table.mw-collapsible'):
        cls = tb.get('class') or []
        cap = tb.find('caption')
        label = cap.get_text(' ', strip=True) if cap else ''
        is_wiki = 'wikitable' in cls
        if not label:
            th = tb.find('th'); label = th.get_text(' ', strip=True) if th else 'Details'
            if not is_wiki and th and th.find_parent('tr') and len(th.find_parent('tr').find_all(['th', 'td'])) == 1:
                th.find_parent('tr').decompose()
        if label in ('Image & Text', 'Text', 'Image', 'Image &amp; Text'): label = 'Show log'
        det = BeautifulSoup('', 'lxml').new_tag('details')
        if is_wiki: det['open'] = ''
        summ = BeautifulSoup('', 'lxml').new_tag('summary'); summ.string = label
        if cap: cap.decompose()
        tb.wrap(det); det.insert(0, summ)
        tb['class'] = (['wikitable'] if is_wiki else ['logtable'])
    # images
    for im in node.find_all('img'):
        loc = img_local(im.get('src'))
        if not loc:
            im.decompose(); continue
        w = im.get('width'); hgt = im.get('height')
        alt = im.get('alt', '')
        icon = 'item-preview' in (im.get('class') or [])
        im.attrs = {'src': 'img/' + loc, 'alt': alt, 'loading': 'lazy'}
        if w and not im.find_parent('figure'): im['width'] = w
        if hgt and not im.find_parent('figure'): im['height'] = hgt
        if icon: im['class'] = ['icon']
    # links
    for a in node.find_all('a'):
        href, ext = link_target(a.get('href'))
        if a.find('img') or not href:
            a.unwrap(); continue
        a.attrs = {'href': href}
        if ext: a['target'] = '_blank'; a['rel'] = 'noopener'
    # tags / attrs
    for t in node.find_all(True):
        if t.name not in ALLOWED:
            t.unwrap(); continue
        keep = {}
        for k, v in t.attrs.items():
            if k in ('href', 'target', 'rel', 'src', 'alt', 'loading', 'width', 'height', 'colspan', 'rowspan', 'open'):
                keep[k] = v
            elif k == 'class':
                cl = [c for c in (v if isinstance(v, list) else [v]) if c in KEEP_CLASS or c == 'icon']
                if cl: keep['class'] = cl
        t.attrs = keep
    for t in node.find_all(['p', 'span', 'div']):
        if not t.get_text(strip=True) and not t.find('img') and not t.find('br') is None and t.name != 'div':
            pass
    return node

def parse_druid(soup):
    box = soup.select_one('.druid-infobox')
    if not box: return None
    out = {'title': '', 'images': [], 'rows': []}
    tt = box.select_one('.druid-title')
    if tt: out['title'] = tt.get_text(' ', strip=True)
    labels = [l.get_text(strip=True) for l in box.select('.druid-main-images-label')]
    for i, f in enumerate(box.select('.druid-main-images-file')):
        im = f.find('img')
        loc = img_local(im.get('src')) if im else None
        if loc: out['images'].append({'label': labels[i] if i < len(labels) else '', 'src': 'img/' + loc})
    if not out['images']:
        for im in box.select('img')[:1]:
            loc = img_local(im.get('src'))
            if loc: out['images'].append({'label': '', 'src': 'img/' + loc})
    for row in box.select('.druid-row'):
        lab = row.select_one('.druid-label'); dat = row.select_one('.druid-data')
        if not lab or not dat: continue
        for im in dat.find_all('img'): im.decompose()
        clean(dat)
        val = dat.decode_contents().strip()
        if val: out['rows'].append([lab.get_text(' ', strip=True), val])
    box.decompose()
    return out

def split_sections(body):
    secs = [{'h': '', 'lvl': 1, 'html': ''}]
    for el in list(body.children):
        if getattr(el, 'name', None) in ('h2', 'h3', 'h4'):
            txt = el.get_text(' ', strip=True).lstrip('>').strip()
            secs.append({'h': txt, 'lvl': int(el.name[1]), 'html': ''})
        else:
            secs[-1]['html'] += str(el)
    return [s for s in secs if s['h'] or BeautifulSoup(s['html'], 'lxml').get_text(strip=True)]

pages = {}
plain = {}
for t, d in pages_in.items():
    soup = BeautifulSoup(d['html'], 'lxml')
    info = parse_druid(soup)
    body = soup.select_one('.mw-parser-output') or soup.body or soup
    clean(soup)
    secs = split_sections(body)
    for s in secs:
        s['html'] = re.sub(r'\n{2,}', '\n', s['html']).strip()
    def _empty(s):
        bs = BeautifulSoup(s['html'], 'lxml')
        return not bs.get_text(strip=True) and not bs.find('img')
    secs = [s for s in secs if not (re.search(r'Ambience|Audio|Music|Sounds', s['h']) and _empty(s))]
    pages[TITLE_SLUG[t]] = {'title': t, 'kind': kind(t), 'info': info, 'sections': secs}
    plain[TITLE_SLUG[t]] = re.sub(r'\s+', ' ', BeautifulSoup(''.join(s['html'] for s in secs), 'lxml').get_text(' '))[:20000]

# ---------- structured moon data ----------
def f(p, k):
    m = re.search(r'\|\s*' + re.escape(k) + r'\s*=([^\n|]*)', p)
    return m.group(1).strip() if m else ''

def num(x):
    try: return float(re.sub(r'[^\d.]', '', x))
    except: return None

moons = {}
for t, p in wikitext.items():
    if '{{Moon Infobox' not in p: continue
    m = re.search(r'Scrap Items(.*?)\|\}', p, re.S); avg = None
    if m:
        tot = w = 0
        for r in m.group(1).split('|-'):
            c = [x.strip() for x in r.split('||')]
            if len(c) >= 8:
                a = num(c[5]); rr = num(c[7].split('\n')[0])
                if a is None or rr is None: continue
                tot += a * rr; w += rr
        if w: avg = tot / w
    mn, mx = num(f(p, 'Minimum Scrap') or ''), num(f(p, 'Maximum Scrap') or '')
    est = round(avg * (mn + mx) / 2) if (avg and mn is not None and mx is not None) else None
    title = f(p, 'title')
    numm = re.match(r'(\d+)', title)
    ints = re.findall(r"(?:''')?([A-Za-z' .()-]+?): ([\d.]+)%", f(p, 'Interiors Spawn Chances').replace('<br>', '\n'))
    ints = sorted([(a.strip(), float(b)) for a, b in ints], key=lambda x: -x[1])
    price = f(p, 'Price')
    moons[t] = {
        'name': t, 'slug': TITLE_SLUG.get(t), 'num': int(numm.group(1)) if numm else None,
        'price': 0 if 'free' in price.lower() else (num(price) or 0),
        'hazard': f(p, 'Hazard Level'), 'weather': f(p, 'Supported Weather(s)'),
        'cruiser': f(p, 'Terrain for Cruiser?'), 'size': f(p, 'Interior Size Multiplier'),
        'scrap': [mn, mx], 'avgItem': round(avg) if avg else None, 'est': est,
        'inPow': num(f(p, 'Interior Power') or ''), 'outPow': num(f(p, 'Exterior Power') or ''),
        'dayPow': num(f(p, 'Daytime Power') or ''),
        'indoor': f(p, 'Dominant Indoor Entity(s)'), 'outdoor': f(p, 'Dominant Outdoor Entity(s)'),
        'interiors': ints[:3], 'vanilla': False,
        'traps': {k: (re.findall(r'\d+', f(p, k)) or [None])[-1] for k in ('Turrets', 'Landmines', 'Spike Traps')},
    }

# unlocked-by / unlocks from rendered sections
def sec_html(sl, name):
    for s in pages[sl]['sections']:
        if s['h'].lower().startswith(name.lower()): return s['html']
    return ''

moon_names = set(moons) | set(VANILLA)
for t, mo in moons.items():
    sl = mo['slug']
    ub = sec_html(sl, 'Unlocked By')
    ul = sec_html(sl, 'Unlocks')
    mo['unlockedByHtml'] = ub
    srcs = []
    for a in BeautifulSoup(ub, 'lxml').find_all('a'):
        h = a.get('href', '')
        nm = None
        if h.startswith('#'):
            for k, v in TITLE_SLUG.items():
                if '#' + v == h: nm = k
        else:
            m = re.search(r'/wiki/([^#?]+)', h)
            if m: nm = urllib.parse.unquote(m.group(1)).replace('_', ' ')
        if nm in moon_names and nm != t and nm not in srcs: srcs.append(nm)
    low = BeautifulSoup(ub, 'lxml').get_text(' ').lower()
    mo['default'] = 'unlocked by default' in low
    mo['sources'] = srcs
    # per-target instructions from Unlocks section
    outs = []
    parts = re.split(r'(<a href="#(p-[a-z0-9-]+)"[^>]*>\s*(?:<big>\s*<b>|<b>\s*<big>|<big>|<b>))', ul)
    i = 1
    while i < len(parts):
        tgt_slug = parts[i + 1]; rest = parts[i + 2] if i + 2 < len(parts) else ''
        tgt = next((k for k, v in TITLE_SLUG.items() if v == tgt_slug), None)
        txt = BeautifulSoup(rest, 'lxml').get_text(' ', strip=True)
        txt = re.sub(r'^[^:]{0,40}:\s*', '', txt) if txt.lower().startswith((tgt or '').lower()) else txt
        if tgt in moons and txt:
            outs.append({'to': tgt, 'how': txt[:600]})
        i += 3
    mo['unlocks'] = outs
    mo['unlocksHtml'] = ul

# rebuild sources from explicit unlock edges (+ vanilla mentions)
for t, mo in moons.items():
    van = [x for x in mo['sources'] if x in VANILLA]
    mo['sources'] = [s2 for s2, m2 in moons.items() if any(u['to'] == t for u in m2['unlocks'])] + van

if not moons['Facto']['sources']:
    moons['Facto']['sources'] = ['Polarus', 'Filitrios', 'Empra', 'Trite', 'Galetry']
    for src in moons['Facto']['sources']:
        moons[src]['unlocks'].append({'to': 'Facto', 'how': 'Facto videotape (random scrap; also sometimes in the Galetry gift shop). Play it in the Galetry projector.'})

# vanilla moons
VDATA = {
 'Experimentation': (41, 0, 'D', [8, 11], 4, 8, 'Factory'),
 'Assurance': (220, 0, 'C', [13, 15], 6, 8, 'Factory'),
 'Vow': (56, 0, 'C', [12, 14], 7, 6, 'Factory'),
 'Offense': (21, 0, 'B', [14, 18], 12, 8, 'Mineshaft'),
 'March': (61, 0, 'B', [13, 16], 14, 12, 'Factory'),
 'Adamance': (20, 0, 'B', [14, 16], 13, 11, 'Factory'),
 'Rend': (85, 550, 'A', [18, 25], 10, 6, 'Mansion'),
 'Dine': (7, 600, 'S', [22, 25], 10, 9, 'Mansion'),
 'Titan': (8, 700, 'S+', [28, 31], 18, 7, 'Factory'),
 'Embrion': (5, 150, 'S', [14, 16], 8, 70, 'Factory'),
 'Artifice': (68, 1500, 'S++', [26, 30], 13, 13, 'Mineshaft'),
 'Gordion': (71, 0, 'Safe', [0, 0], 0, 0, 'The Company Building'),
}
for v, (n, pr, hz, sc, ip, op, lay) in VDATA.items():
    unl = []
    for t, mo in moons.items():
        if v in mo['sources']:
            txt = BeautifulSoup(mo['unlockedByHtml'], 'lxml').get_text(' ', strip=True)
            unl.append({'to': t, 'how': txt[:600]})
    moons[v] = {'name': v, 'slug': None, 'num': n, 'price': pr, 'hazard': hz, 'scrap': sc, 'inPow': ip, 'outPow': op,
                'interiors': [(lay, 100)], 'vanilla': True, 'default': v not in ('Embrion', 'Artifice'),
                'sources': [], 'unlocks': unl, 'est': None, 'avgItem': None,
                'wiki': 'https://lethal.miraheze.org/wiki/' + v}

# maps
def bg_file(n):
    n = n.replace(' ', '_')
    return imgmap.get('MAP:' + n) or imgmap.get(n)
mapsout = {}
for t, m in maps_raw.items():
    crs = m['crs']; order = crs.get('order', 'yx')
    bgs = m.get('backgrounds') or [{'name': 'Terrain', 'image': m.get('background')}]
    bgs = [{'name': b.get('name', 'Terrain'), 'src': 'img/' + bg_file(b['image'])} for b in bgs[:2] if bg_file(b['image'])]
    if order == 'xy':
        X, Y = crs['topLeft']; tf = lambda mk: (mk['x'] / X, 1 - mk['y'] / Y)
    else:
        Y, X = crs['bottomRight']; tf = lambda mk: (mk['x'] / X, mk['y'] / Y)
    groups = {}
    for gk, g in m['groups'].items():
        ic = g.get('icon')
        groups[gk] = {'name': g.get('name', gk), 'icon': ('img/' + imgmap[ic.replace(' ', '_')]) if ic and imgmap.get(ic.replace(' ', '_')) else None,
                      'color': g.get('pinColor') or g.get('fillColor') or '#e8a33d'}
    marks = []
    for gk, ms in m['markers'].items():
        for mk in ms:
            if 'x' not in mk: continue
            x, y = tf(mk)
            marks.append({'g': gk, 'x': round(x * 100, 2), 'y': round(y * 100, 2), 'n': mk.get('name', ''), 'd': mk.get('description', '')})
    mapsout[t] = {'bgs': bgs, 'groups': groups, 'marks': marks}

used_maps = set()
for mm in mapsout.values():
    for b in mm['bgs']: used_maps.add(b['src'][4:])
for fn in os.listdir(os.path.join(B, 'img')):
    if fn.endswith('-map.webp') and fn not in used_maps:
        os.remove(os.path.join(B, 'img', fn))

nav = {'moon': [], 'interior': [], 'entity': [], 'guide': []}
for sl, pg in pages.items(): nav[pg['kind']].append([pg['title'], sl])
for k in nav: nav[k].sort()

os.makedirs(os.path.join(B, 'data'), exist_ok=True)
json.dump({'pages': pages, 'plain': plain, 'nav': nav}, open(os.path.join(B, 'data', 'pages.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump({'moons': moons, 'maps': mapsout}, open(os.path.join(B, 'data', 'moons.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('pages', len(pages), 'moons', len(moons), 'maps', len(mapsout))
print(os.path.getsize(os.path.join(B, 'data', 'pages.json')), os.path.getsize(os.path.join(B, 'data', 'moons.json')))
for t in ['Infernis', 'Junic', 'Atlantica', 'Dreck', 'Galetry', 'MorvDonalds', 'Repress', 'Adamance', 'Vow']:
    mo = moons[t]; print(t, mo.get('default'), mo['sources'], [u['to'] for u in mo['unlocks']])
