"""Recipe icon tiles (ingredient image + how many items to bring) and clearer material wording."""
import sys
S = sys.argv[1]
p = S + '/build/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]; s = s.replace(a, b, 1)

rep('''  const k = Math.ceil(q / small.gives);
  return `<li><b>${q} ${esc(res)}</b> = ${k}× ${esc(small.n)} <span class="rs">(${small.gives} each, ${esc(small.w)} lb)</span>${big ? ` <span class="rs">or ${Math.ceil(q / big.gives)}× ${esc(big.n)} (${big.gives} each${big.two ? ", two-handed" : ""})</span>` : ""}''',
'''  const k = Math.ceil(q / small.gives);
  return `<li><b>${esc(res)}: ${q} needed</b> → bring <b>${k}× ${esc(small.n)}</b> <span class="rs">(each gives ${small.gives}, ${esc(small.w)} lb)</span>${big ? ` <span class="rs">or ${Math.ceil(q / big.gives)}× ${esc(big.n)} (each gives ${big.gives}${big.two ? ", two-handed" : ""})</span>` : ""}''')

rep('''function recipeHtml(r){''', '''function recipeTiles(r){
  return `<div class="rtiles">${r.cost.map(([q, res]) => {
    const I = (window.CRAFT.ing[res] || []); const sm = I.find(i => !i.two) || I[0]; if (!sm) return "";
    const k = Math.ceil(q / sm.gives);
    return `<div class="rt" title="${esc(res)}: ${q} needed = ${k}× ${esc(sm.n)} (each gives ${sm.gives})">${sm.img ? `<img src="${sm.img}" alt="" loading="lazy">` : ""}<span class="rq">×${k}</span><small>${esc(sm.n)}</small></div>`;
  }).join("")}</div>`;
}
function recipeHtml(r){''')
rep('''    <ul>${r.cost.map(([q, res]) => matLine(q, res)).join("")}</ul></div>`;''',
    '''    ${recipeTiles(r)}
    <ul>${r.cost.map(([q, res]) => matLine(q, res)).join("")}</ul></div>`;''')
rep('''.recipe ul{margin:2px 0 0;padding-left:18px}''', '''.recipe ul{margin:2px 0 0;padding-left:18px}
.rtiles{display:flex;flex-wrap:wrap;gap:8px;margin:7px 0 4px}
.rt{position:relative;width:72px;text-align:center}
.rt img{width:56px;height:56px;object-fit:contain;display:block;margin:0 auto;padding:4px;border:1px solid var(--line);border-radius:8px;background:var(--panel,#1a1e27)}
.rt .rq{position:absolute;top:36px;right:4px;font:700 13px var(--font-mono);padding:0 5px;border-radius:9px;background:var(--accent);color:#111}
.rt small{display:block;font-size:11px;line-height:1.2;margin-top:3px;color:var(--muted)}''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
