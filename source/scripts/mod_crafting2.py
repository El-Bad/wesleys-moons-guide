"""Crafting follow-up: compact recipe layout, shorter 'Craft at', Craftable filter also shows recipe items of other types (Weed killer, Untampered operating panel)."""
import sys
S = sys.argv[1]
p = S + '/build/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:80]; s = s.replace(a, b, 1)
rep('.recipe .src{color:var(--muted);font-size:12.5px}', '.recipe .rs{color:var(--muted);font-size:12.5px;display:inline}\n.recipe .rf{color:var(--muted);font-size:12.5px;margin:1px 0 3px}\n.craftguide .rs{color:var(--muted)}')
i = s.find('/* ---------- crafting ---------- */'); j = s.find('let itemFilter = {q: "", t: "useful"};')
blk = s[i:j].replace('class="src"', 'class="rs"')
blk = blk.replace('<div class="rs">Find it on: ', '<div class="rf">Find it on: ').replace('<div class="rs">Used in: ', '<div class="rf">Used in: ')
blk = blk.replace('''<div><b>Craft at:</b> ${r.at.map(a => esc(STATION[a])).join("; or ")}${r.at.length === 1 ? ` <span class="rs">(${esc(r.at[0])} only)</span>` : ""}</div>''',
 '''<div><b>Craft at:</b> ${r.at.length === 1 ? `<b>${esc(r.at[0])} only</b> <span class="rs">(${esc(STATION[r.at[0]].split(": ")[1])})</span>` : `Gratar or Galetry fabricator <span class="rs">(see "How crafting works" above the list)</span>`}</div>''')
s = s[:i] + blk + s[j:]
rep('''const list = I.filter(x => itemFilter.t === "all" ? true : itemFilter.t === "useful" ? useful(x) : x.t === itemFilter.t)''',
    '''const list = I.filter(x => itemFilter.t === "all" ? true : itemFilter.t === "useful" ? useful(x) : itemFilter.t === "Craftable" ? (x.t === "Craftable" || !!recipeFor(x)) : x.t === itemFilter.t)''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
# follow-up applied by hand: big-item "two-handed" label now uses big.two
