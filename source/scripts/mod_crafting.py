"""Items: recipe, crafting station and where to get each material for every craftable item, plus a crafting guide panel."""
import sys
S = sys.argv[1]
p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]
    s = s.replace(a, b, 1)

CSS = '''
.recipe{margin-top:6px;padding:7px 9px;border:1px solid var(--line);border-radius:6px;background:var(--bg)}
.recipe .rh{font:600 11px var(--font-mono);text-transform:uppercase;letter-spacing:.06em;color:var(--accent);margin-bottom:3px}
.recipe ul{margin:2px 0 0;padding-left:18px}
.recipe li{margin:2px 0}
.recipe .src{color:var(--muted);font-size:12.5px}
.recipe .chip{font-size:11.5px;padding:0 5px}
.craftguide{margin:0 0 12px}
.craftguide h2{font-size:17px;margin:0 0 6px}
.craftguide h3{font:600 12px var(--font-mono);text-transform:uppercase;letter-spacing:.08em;margin:12px 0 4px;color:var(--accent)}
.craftguide table{width:100%;border-collapse:collapse;font-size:13px}
.craftguide td,.craftguide th{border-top:1px solid var(--line);padding:5px 6px;text-align:left;vertical-align:top}
.craftguide th{font:600 11px var(--font-mono);text-transform:uppercase;color:var(--muted)}
'''
rep('@media (prefers-reduced-motion: reduce)', CSS + '\n@media (prefers-reduced-motion: reduce)')

JS = r'''
/* ---------- crafting ---------- */
const STATION = {
  Gratar: "Gratar: the fabricator through the blue fire exit next to the main entrance",
  Galetry: "Galetry: the fabricator behind the locked door in the fire exit left of the ship (open it with a Fabricated key made on Gratar)"
};
const RECIPE_ALIAS = {"untampered operating panel": "operating panel"};
function recipeFor(x){
  const C = window.CRAFT; if (!C) return null;
  const k = RECIPE_ALIAS[x.n.toLowerCase()] || x.n.toLowerCase();
  return C.recipes.find(r => r.n.toLowerCase() === k) || null;
}
function locHtml(l){ const m = l.match(/^(.*?):\s*(.*)$/); if (!m) return esc(l); const n = m[1].trim(); return (M[n] ? moonChip(n) : `<b>${esc(n)}</b>`) + " " + esc(m[2]); }
function matLine(q, res){
  const I = (window.CRAFT.ing[res] || []); const small = I.find(i => !i.two) || I[0]; const big = I.find(i => i !== small);
  if (!small) return `<li><b>${q} ${esc(res)}</b></li>`;
  const k = Math.ceil(q / small.gives);
  return `<li><b>${q} ${esc(res)}</b> = ${k}× ${esc(small.n)} <span class="src">(${small.gives} each, ${esc(small.w)} lb)</span>${big ? ` <span class="src">or ${Math.ceil(q / big.gives)}× ${esc(big.n)} (${big.gives} each, two-handed)</span>` : ""}
    <div class="src">Find it on: ${small.locs.slice(0, 5).map(locHtml).join(", ")}${big ? `; ${esc(big.n)}: ${big.locs.map(locHtml).join(", ")}` : ""}</div></li>`;
}
function recipeHtml(r){
  return `<div class="recipe"><div class="rh">Recipe${r.yield > 1 ? ` · makes ${r.yield}` : ""}</div>
    <div><b>Craft at:</b> ${r.at.map(a => esc(STATION[a])).join("; or ")}${r.at.length === 1 ? ` <span class="src">(${esc(r.at[0])} only)</span>` : ""}</div>
    <ul>${r.cost.map(([q, res]) => matLine(q, res)).join("")}</ul></div>`;
}
function ingredientHtml(x){
  const C = window.CRAFT; if (!C) return "";
  const res = C.res.find(r => (C.ing[r] || []).some(i => i.n.toLowerCase() === x.n.toLowerCase())); if (!res) return "";
  const uses = C.recipes.filter(r => r.cost.some(([q, n]) => n === res)).map(r => r.n);
  return `<div class="recipe"><div class="rh">Material: ${esc(res)}</div><div class="src">Used in: ${uses.map(esc).join(", ")}</div></div>`;
}
function craftGuide(){
  const C = window.CRAFT; if (!C) return "";
  return `<div class="callout craftguide"><h2>How crafting works</h2><ul>
    <li><b>Ingredient items</b> are scrap you put into a fabricator instead of selling. Each one adds resources (for example 1 Plastic stock item = 7 Plastic stock).</li>
    <li>There are two fabricators. <b>${esc(STATION.Gratar)}</b>. <b>${esc(STATION.Galetry)}</b>.</li>
    <li>Both machines share one resource pool, and resources stay saved even after you get fired. You can deposit on Gratar and craft on Galetry.</li>
    <li>Gratar is the only place to craft the <b>Operating panel</b>; Galetry is the only place for the <b>Blank floppy disc</b>. Everything else works at both.</li>
    <li>Gratar unlocks from the Gratar videotape (into Galetry's projector) or by logging Cunningham's visit.</li></ul>
    <h3>Where to find each material</h3>
    <table><thead><tr><th>Resource</th><th>Ingredient item</th><th>Best moons</th></tr></thead><tbody>${C.res.map(r => (C.ing[r] || []).map((i, k) => `<tr>${k ? "" : `<td rowspan="${C.ing[r].length}"><b>${esc(r)}</b></td>`}<td>${esc(i.n)} <span class="src">→ ${i.gives} · ${esc(i.w)} lb${i.two ? " · two-handed" : ""}</span></td><td>${i.locs.slice(0, 6).map(locHtml).join(", ")}</td></tr>`).join("")).join("")}</tbody></table>
    <h3>Floppy disc machines (put a Blank floppy disc in, log the disc you get)</h3>
    <table><thead><tr><th>Machine on</th><th>Where</th><th>Unlocks</th></tr></thead><tbody>${C.floppy.map(([a, w, b]) => `<tr><td>${moonChip(a)}</td><td>${esc(w)}</td><td>${moonChip(b)}</td></tr>`).join("")}</tbody></table></div>`;
}
'''
rep('let itemFilter = {q: "", t: "useful"};', JS + '\nlet itemFilter = {q: "", t: "useful"};')

rep('''<td>${esc(x.d)}${x.link ? ` <a href="${esc(x.link)}" target="_blank" rel="noopener">wiki</a>` : ""}</td>''',
    '''<td>${(() => { const r = recipeFor(x); const d = r ? x.d.replace(/\\s*Recipe:.*$/, "").replace(/\\s*\\(\\d+ Plastic stock[^)]*\\)/, "") : x.d; return esc(d || r.use) + (x.link ? ` <a href="${esc(x.link)}" target="_blank" rel="noopener">wiki</a>` : "") + (r ? recipeHtml(r) : x.t === "Ingredient" ? ingredientHtml(x) : ""); })()}</td>''')
rep('''<div class="tablewrap"><table class="moons items">''', '''${itemFilter.t === "Craftable" || itemFilter.t === "Ingredient" ? craftGuide() : ""}<div class="tablewrap"><table class="moons items">''')
rep('''Descriptions come from the Wesley's Moons and Lethal Company wikis, plus notes from your questions.</p>''',
    '''Descriptions come from the Wesley's Moons and Lethal Company wikis, plus notes from your questions. Pick <b>Craftable</b> for recipes, where to craft and where to find each material.</p>''')
rep('window.ITEMS = mj.items || {};', 'window.ITEMS = mj.items || {}; window.CRAFT = mj.craft || null;')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
