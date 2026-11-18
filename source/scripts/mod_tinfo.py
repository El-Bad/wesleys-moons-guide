"""Map: 'Price & hazard' checkbox that labels every moon node. Entities: Wesley's / Vanilla / All filter."""
import sys
S = sys.argv[1]
p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]
    s = s.replace(a, b, 1)

CSS = '''
svg .tinfo text{font:700 14px "IBM Plex Mono",ui-monospace,monospace;paint-order:normal;stroke:none}
svg .tinfo .pr{fill:rgba(12,14,20,.92);stroke:#4a4f5c;stroke-width:1}
svg .node.locked .tinfo{opacity:.75}
.vcard .btxt .meta{display:flex;flex-wrap:wrap;gap:4px;margin:4px 0 2px}
.vcard .btxt p{margin:4px 0 0;font-size:13px}
.vcard .btxt p.how{color:var(--ink)}
.vcard .btxt p.how b{color:var(--ok);font:600 11px var(--font-mono);text-transform:uppercase;letter-spacing:.06em;margin-right:4px}
.vcard .bimg img{object-fit:contain;background:#0b0c10}
.vcard .btxt a.ext{font-size:12px}
'''
rep('@media (prefers-reduced-motion: reduce)', CSS + '\n@media (prefers-reduced-motion: reduce)')

# ---- map price & hazard ----
rep('let tv = null, tsel = null, tAll = false;',
    'let tv = null, tsel = null, tAll = false, tInfo = localStorage.getItem("wm-tinfo") === "1";')
rep('''      <text x="${tx}" y="${ty}" text-anchor="${anchor}" fill="${col}" style="${big ? "font-size:30px" : ""}">${esc(n === "End" ? "Repress / End" : n)}</text>
    </g>`;''',
    '''      <text x="${tx}" y="${ty}" text-anchor="${anchor}" fill="${col}" style="${big ? "font-size:30px" : ""}">${esc(n === "End" ? "Repress / End" : n)}</text>
      ${tInfo ? tInfoBadge(n, x, y, R, lab) : ""}
    </g>`;''')
rep('function treeSvg(){', '''const HZFILL = {h0:"#3f8f5a", h1:"#7d9a2f", h2:"#b8860b", h3:"#cf6a17", h4:"#c0392b", h5:"#8e1f4b", h6:"#5b3fa0"};
function tInfoBadge(n, x, y, R, lab){
  const m = M[n]; if (!m || n === "End") return "";
  const hz = ({"B.. for Bees":"B", "I see you":"??", "Quack":"Qk"})[m.hazard] || m.hazard || "?";
  const pr = m.price ? "▮" + m.price : "Free";
  const cw = 8.6, pad = 6, gap = 3, h = 20;
  const w1 = hz.length * cw + pad * 2, w2 = pr.length * cw + pad * 2, W = w1 + gap + w2;
  const x0 = lab === "r" ? x + 36 : x - W / 2, y0 = lab === "r" ? y + 14 : y + R + 6;
  return `<g class="tinfo" aria-hidden="true"><rect x="${x0}" y="${y0}" width="${w1}" height="${h}" rx="4" fill="${HZFILL[hzClass(m.hazard)]}"/><text x="${x0 + w1 / 2}" y="${y0 + 15}" text-anchor="middle" fill="#fff">${esc(hz)}</text>
    <rect class="pr" x="${x0 + w1 + gap}" y="${y0}" width="${w2}" height="${h}" rx="4"/><text x="${x0 + w1 + gap + w2 / 2}" y="${y0 + 15}" text-anchor="middle" fill="${m.price ? "#f3c27a" : "#5cc28a"}">${esc(pr)}</text></g>`;
}
function treeSvg(){''')
rep('<label><input type="checkbox" id="tall" ${tAll ? "checked" : ""}> Show all alternate routes</label>',
    '<label><input type="checkbox" id="tall" ${tAll ? "checked" : ""}> Show all alternate routes</label><label title="Show each moon\'s route price and hazard level"><input type="checkbox" id="tinfo" ${tInfo ? "checked" : ""}> Price &amp; hazard</label>')
rep('  $("#tall").onchange = e => { tAll = e.target.checked; renderTree(); };',
    '  $("#tall").onchange = e => { tAll = e.target.checked; renderTree(); };\n  $("#tinfo").onchange = e => { tInfo = e.target.checked; localStorage.setItem("wm-tinfo", tInfo ? "1" : "0"); renderTree(); };')

# ---- entities filter ----
rep('function renderList(kind){', '''let entFilter = "wes";
function vanillaCards(){
  return (window.VENTS || []).map(e => `<div class="bcard vcard"><div class="bimg">${e.img ? `<img src="${esc(e.img)}" alt="${esc(e.n)}" loading="lazy">` : ""}</div><div class="btxt"><b>${esc(e.n)}</b>
    <div class="meta"><span class="chip mono">${esc(e.g)}</span><span class="chip mono" title="Health (1 = one shovel hit)">${esc(e.hp)} HP</span><span class="chip mono">${e.stun ? "Stunnable" : "Not stunnable"}</span></div>
    <small>${esc(e.d)}</small>${e.s ? `<p class="how"><b>Handle it</b>${esc(e.s)}</p>` : ""}
    <p><a class="ext" href="${esc(e.link)}" target="_blank" rel="noopener">Lethal Company wiki ↗</a></p></div></div>`).join("");
}
function renderList(kind){''')
rep('''  $("#v-list").innerHTML = `<h1 style="font-size:24px">${esc(titles)}</h1><p style="color:var(--muted);margin:4px 0 14px">${esc(intro)}</p><div class="${big ? "bcards" : "cards"}">${cards}</div>`;''',
    '''  if (k === "entity"){
    const seg = (v, l) => `<button aria-pressed="${entFilter === v}" data-ef="${v}">${l}</button>`;
    const vc = vanillaCards(), nW = NAV[k].length, nV = (window.VENTS || []).length;
    const body = entFilter === "wes" ? cards : entFilter === "van" ? vc
      : `<h2 style="font-size:18px;margin:4px 0 8px">Wesley's Moons</h2><div class="bcards">${cards}</div><h2 style="font-size:18px;margin:16px 0 8px">Vanilla Lethal Company</h2><div class="bcards">${vc}</div>`;
    $("#v-list").innerHTML = `<div class="filters"><h1 style="font-size:24px;margin-right:8px">Entities</h1><div class="seg" role="group" aria-label="Which entities">${seg("wes", `Wesley's (${nW})`)}${seg("van", `Vanilla (${nV})`)}${seg("all", "All")}</div></div>
      <p style="color:var(--muted);margin:4px 0 12px">${entFilter === "van" ? "The base-game creatures, from the Lethal Company Wiki. They still spawn on Wesley's moons." : entFilter === "wes" ? "Creatures and enemy variants added by Wesley's Moons." : "Wesley's creatures first, then the base game's."}</p>
      ${entFilter === "all" ? body : `<div class="bcards">${body}</div>`}`;
    $$("#v-list [data-ef]").forEach(b => b.onclick = () => { entFilter = b.dataset.ef; renderList(kind); });
    return;
  }
  $("#v-list").innerHTML = `<h1 style="font-size:24px">${esc(titles)}</h1><p style="color:var(--muted);margin:4px 0 14px">${esc(intro)}</p><div class="${big ? "bcards" : "cards"}">${cards}</div>`;''')
rep('window.ITEMS = mj.items || {};', 'window.ITEMS = mj.items || {}; window.VENTS = mj.vents || [];')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
