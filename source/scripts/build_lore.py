"""Collect every page's Lore (and story-spoiler) sections -> moons.json 'lore'.
Run after post_build.py:  python -X utf8 scripts/build_lore.py .
"""
import sys, json, re, html
S = sys.argv[1]
pj = json.load(open(S + '/build/data/pages.json', encoding='utf-8'))
P, NAV = pj['pages'], pj['nav']
W = {p.split('\n', 1)[0]: p for p in open(S + '/dump/wesley.txt', encoding='utf-8').read().split('\n\n######## ')[1:]}

def wiki_prose(t):
    """Plain prose lines from a wikitext block (skips tables/files), for pages whose rendered sections were lost."""
    cur = {'h': '', 'lvl': 3, 'html': ''}; out = [cur]
    for line in t.split('\n'):
        h = re.match(r'^(=+)\s*(.*?)\s*=+\s*$', line)
        if h:
            cur = {'h': re.sub(r'^>\s*', '', h.group(2)), 'lvl': len(h.group(1)), 'html': ''}; out.append(cur); continue
        if not line.strip() or line.lstrip().startswith(('{|', '|', '!', '[[File', 'File:', '{{', '}}')): continue
        x = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', line)
        x = re.sub(r"'''?", '', re.sub(r'<[^>]+>', '', x)).strip().lstrip('-').strip()
        if len(x) > 20 and cur is not None: cur['html'] += '<p>' + html.escape(x) + '</p>'
    return [s for s in out if s['html'] or s['lvl'] <= 3]

order = {s: i for i, (t, s) in enumerate(NAV.get('moon', []))}
lore = []
for slug, pg in P.items():
    if pg['kind'] not in ('moon', 'entity'): continue
    secs, on = [], False
    for s in pg['sections']:
        if s['lvl'] == 2: on = s['h'].strip().lower() == 'lore'
        if (on and s['h'].strip().lower() != 'lore') or s['h'].startswith('Major Story Spoilers'):
            secs.append({'h': s['h'], 'lvl': s['lvl'], 'html': s['html']})
        elif on and s['html'].strip():
            secs.append({'h': '', 'lvl': 3, 'html': s['html']})
    if not secs or all(not x['html'].strip() for x in secs):
        wt = W.get(pg['title'], '')
        m = re.search(r'^==\s*>?\s*Lore\s*==\s*$(.*?)(?=^==\s*>?\s*(?:Trivia|Gallery)|\Z)', wt, re.S | re.M)
        if m: secs = wiki_prose(m.group(1))
    secs = [s for s in secs if 'Unfinished Section' not in s['html'] and (s['html'].strip() or s['lvl'] <= 3)]
    text = ' '.join(re.sub(r'<[^>]+>', ' ', s['html']) for s in secs)
    if len(text.strip()) < 40 or re.search(r'does not (contain|have) any lore', text): continue
    intro = pg['sections'][0]['html'] if pg['sections'] and not pg['sections'][0]['h'] else ''
    lore.append({'slug': slug, 'title': pg['title'], 'kind': pg['kind'], 'intro': intro, 'secs': secs})
lore.sort(key=lambda x: (x['kind'] != 'moon', x['title'].lower()))
mj = json.load(open(S + '/build/data/moons.json', encoding='utf-8'))
mj['lore'] = lore
json.dump(mj, open(S + '/build/data/moons.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(lore), [x['title'] for x in lore])
