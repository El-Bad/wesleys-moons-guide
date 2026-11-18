import sys, re
S = sys.argv[1]
p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()

def rep(a, b, count=1):
    global s
    assert a in s, 'MISSING: ' + a[:90]
    s = s.replace(a, b, count)

def rep_between(start, end, new, keep_end=True):
    global s
    i = s.index(start); j = s.index(end, i)
    s = s[:i] + new + (s[j:] if keep_end else s[j + len(end):])

# 1. TIPS data
rep_between('const TIPS = {', 'const GOALS = [', open(S + '/scripts/tips.js.txt', encoding='utf-8').read() + '\n')

# 2. helpers (inserted before tree code)
HELP = r'''
/* ---------- shared helpers: unlock sections, guide + hazards, items ---------- */
function waySection(title, cls, arr){
  return arr.length ? `<div class="wsec"><div class="wsh ${cls}">${title} <span>${arr.length}</span></div>${arr.join("")}</div>` : "";
}
function grouped(list, render){
  const g = [], r = [];
  list.forEach(x => (x.random ? r : g).push(render(x)));
  return waySection("Guaranteed", "g", g) + waySection("Random drops", "r", r);
}
function incoming(n){
  return (M[n]?.sources || []).map(src => { const u = (M[src]?.unlocks || []).find(x => x.to === n); return {src, how: u ? u.how : "", random: u ? isRandom(u.how) : false}; });
}
function outgoing(n){ return (M[n]?.unlocks || []).map(u => ({to: u.to, how: u.how, random: isRandom(u.how)})); }
function hazardList(n, m){
  const T = TIPS[n], out = [...(T?.h || [])];
  if (m && !m.vanilla){
    const tr = m.traps || {}; const parts = [];
    if (+tr.Turrets) parts.push(`up to ${tr.Turrets} turrets`); if (+tr.Landmines) parts.push(`${tr.Landmines} landmines`); if (+tr["Spike Traps"]) parts.push(`${tr["Spike Traps"]} spike traps`);
    if (parts.length) out.push("Traps: " + parts.join(", ") + ".");
    if (m.indoor) out.push("Main indoor enemies: " + m.indoor + ".");
    if (m.outdoor) out.push("Main outdoor enemies: " + m.outdoor + ".");
    const bad = (m.weather || "").split(/,\s*/).filter(w => /Eclipsed|Forsaken|Hallowed|Minefield|Hurricane|Flooded/i.test(w));
    if (bad.length) out.push("Rough weather possible: " + bad.join(", ") + ".");
  }
  return out;
}
function guideHazards(n, m, compact){
  const T = TIPS[n]; const hz = hazardList(n, m);
  if (!T && !hz.length) return "";
  const H = compact ? "h3" : "h2";
  const guide = T ? `<div class="callout"><${H}>Guide</${H}><ul>${T.g.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>` : "";
  const haz = hz.length ? `<div class="hazbox"><${H}>Hazards</${H}><ul>${hz.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>` : "";
  return `<div class="gh ${compact ? "compact" : ""}">${guide}${haz}</div>`;
}
const ITEM_KEY = t => String(t || "").replace(/\s+/g, " ").trim().toLowerCase();
function findItem(t){
  const I = window.ITEMS || {}; let k = ITEM_KEY(t);
  if (I[k]) return k;
  k = k.replace(/^\(lore\)\s*/, "").replace(/\s*\(.*?\)$/, "").replace(/\s*\d+x$/, "");
  if (I[k]) return k;
  if (k.endsWith("s") && I[k.slice(0, -1)]) return k.slice(0, -1);
  return null;
}
function showItem(k, el){
  const it = (window.ITEMS || {})[k]; if (!it) return;
  const pop = $("#pop");
  const rows = [it.v && `<dt>Value</dt><dd>${esc(it.v)}</dd>`, it.w && `<dt>Weight</dt><dd>${esc(it.w)} lb</dd>`, it.two && `<dt>Two-handed</dt><dd>${esc(it.two)}</dd>`, it.where && `<dt>Found</dt><dd>${esc(it.where)}</dd>`].filter(Boolean).join("");
  pop.innerHTML = `<button class="pclose" aria-label="Close">×</button><div class="eyebrow">${esc(it.t)}</div><b>${esc(it.n)}</b><p>${esc(it.d)}</p>${rows ? `<dl class="facts">${rows}</dl>` : ""}<div class="plinks">${it.link ? `<a href="${esc(it.link)}" target="_blank" rel="noopener">Lethal Company wiki</a>` : ""}<a href="#item-uses">All items</a></div>`;
  pop.hidden = false;
  const r = el.getBoundingClientRect(); const w = Math.min(360, innerWidth - 16);
  pop.style.width = w + "px"; pop.style.left = Math.max(8, Math.min(r.left, innerWidth - w - 8)) + "px";
  const below = r.bottom + 6, h = pop.offsetHeight;
  pop.style.top = (below + h > innerHeight - 8 ? Math.max(8, r.top - h - 6) : below) + "px";
  $(".pclose", pop).onclick = () => pop.hidden = true;
}
function linkItems(root){
  $$("table", root).forEach(tb => $$("tr", tb).forEach(tr => {
    const td = tr.querySelector("td"); if (!td || td.querySelector(".itemlink")) return;
    const k = findItem(td.textContent); if (!k) return;
    if (td.querySelector("a")) td.insertAdjacentHTML("beforeend", ` <button class="itemlink info" data-item="${esc(k)}" aria-label="What does this item do?">?</button>`);
    else td.innerHTML = `<button class="itemlink" data-item="${esc(k)}" title="What does this item do?">${td.innerHTML}</button>`;
  }));
}
document.addEventListener("click", e => {
  const b = e.target.closest(".itemlink"); if (b){ e.preventDefault(); showItem(b.dataset.item, b); return; }
  if (!e.target.closest("#pop")) { const p = $("#pop"); if (p) p.hidden = true; }
});
document.addEventListener("keydown", e => { if (e.key === "Escape") { const p = $("#pop"); if (p) p.hidden = true; } });

let itemFilter = {q: "", t: "useful"};
function renderItems(){
  const I = Object.values(window.ITEMS || {});
  const types = [...new Set(I.map(x => x.t))];
  const useful = x => x.t !== "Scrap" && x.t !== "Reward" && x.t !== "Action figure";
  const list = I.filter(x => itemFilter.t === "all" ? true : itemFilter.t === "useful" ? useful(x) : x.t === itemFilter.t)
    .filter(x => !itemFilter.q || (x.n + " " + x.d + " " + (x.where || "")).toLowerCase().includes(itemFilter.q))
    .sort((a, b) => a.t.localeCompare(b.t) || a.n.localeCompare(b.n));
  const chip = (k, l) => `<button aria-pressed="${itemFilter.t === k}" data-it="${esc(k)}">${esc(l)}</button>`;
  let cur = "";
  const rows = list.map(x => { const head = x.t !== cur ? `<tr class="grp"><th colspan="4">${esc(x.t)}</th></tr>` : ""; cur = x.t;
    return `${head}<tr><td><b>${esc(x.n)}</b></td><td>${esc(x.d)}${x.link ? ` <a href="${esc(x.link)}" target="_blank" rel="noopener">wiki</a>` : ""}</td><td class="n">${esc(x.v || "")}</td><td class="n">${x.w ? esc(x.w) + " lb" : ""}</td></tr>`; }).join("");
  $("#v-items").innerHTML = `<div class="filters"><h1 style="font-size:22px;margin-right:8px">What items do</h1>
    <input type="search" id="iq" class="tf" style="margin:0;width:min(280px,100%)" placeholder="Search items…" value="${esc(itemFilter.q)}" aria-label="Search items">
    <div class="seg" role="group" aria-label="Item type">${chip("useful", "Usable & special")}${chip("all", "All")}${types.sort().map(t => chip(t, t)).join("")}</div></div>
    <p style="margin:0 0 8px;font-size:13px;color:var(--muted)">${list.length} items. Most of Wesley's regular scrap has no use besides selling. Descriptions come from the Wesley's Moons and Lethal Company wikis, plus notes from your questions.</p>
    <div class="tablewrap"><table class="moons items"><thead><tr><th>Item</th><th>What it does</th><th>Value</th><th>Weight</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  const q = $("#iq"); q.oninput = () => { itemFilter.q = q.value.toLowerCase(); const pos = q.selectionStart; renderItems(); const n = $("#iq"); n.focus(); n.setSelectionRange(pos, pos); };
  $$("#v-items [data-it]").forEach(b => b.onclick = () => { itemFilter.t = b.dataset.it; renderItems(); });
}
'''
rep('/* ---------- progression tree', HELP + '\n/* ---------- progression tree')

# 3. tree side panel
i = s.index('  const ways = (m.sources || []).map(s => {'); j = s.index('\n', s.index('  const tips = TIPS[n] ?', i))
s = s[:i] + '''  const ways = grouped(incoming(n), x => `<div class="way"><b>${isU(x.src) ? "✓ " : ""}From ${esc(x.src)}</b><br>${esc(x.how || "See the moon's page.")}</div>`)
    || `<div class="way">${m.default ? "Unlocked by default." : n === "Hyx" ? "Insert the Bloody, Cosmic and Royal apparatus in Galetry's hidden backstage." : "See the moon's page."}</div>`;
  const outs = grouped(outgoing(n), x => `<div class="way"><b>${esc(x.to)}</b><br>${esc(x.how)}</div>`) || `<div class="way">Doesn't unlock other moons.</div>`;
  const tips = guideHazards(n, m, true);''' + s[j:]
rep('${tips}<h3>How to get here</h3>${ways}<h3>Unlocks from here</h3>${outs}', '${tips}<h3>How to get here</h3>${ways}<h3>Unlocks from here</h3>${outs}')

# 4. home next-up grouped
i = s.index('  const nextHtml = avail.length ? avail.map(n => {'); j = s.index('\n', s.index('Check the moon list for random drops.</p>`;', i))
s = s[:i] + '''  const card = n => {
    const m = M[n];
    const ways = incoming(n).filter(x => isU(x.src));
    const body = grouped(ways, x => `<p><span class="from">From ${esc(x.src)}</span><br>${esc(x.how || "See the moon's page.")}</p>`);
    return `<div class="next-item"><header>${hzPill(m.hazard)}<a href="${esc(moonLink(n))}">${esc(n)}</a><span class="chip mono">${m.price ? "▮" + m.price : "Free"}</span>${m.est ? `<span class="chip mono" title="Estimated loot per day">~${m.est} loot</span>` : ""}<button class="toggle tu" aria-pressed="false" data-u="${esc(n)}" style="margin-left:auto">Mark unlocked</button></header>${body}</div>`;
  };
  const sure = avail.filter(n => incoming(n).some(x => isU(x.src) && !x.random));
  const luck = avail.filter(n => !sure.includes(n));
  const nextHtml = avail.length ? `${sure.length ? `<h3 class="nh g">Guaranteed unlocks (${sure.length})</h3><div class="next-list">${sure.map(card).join("")}</div>` : ""}${luck.length ? `<h3 class="nh r">Random-drop unlocks (${luck.length})</h3><div class="next-list">${luck.map(card).join("")}</div>` : ""}` : `<p>Nothing new is reachable from your unlocked moons.</p>`;''' + s[j:]
rep('<div class="panel next"><h2>Next up: moons you can unlock now</h2><div class="next-list">${nextHtml}</div></div>', '<div class="panel next"><h2>Next up: moons you can unlock now</h2>${nextHtml}</div>')

# 5. moon page guide/hazards + grouped reach
rep('  const tips = TIPS[t] ? `<div class="callout"><h2>Crew quick guide</h2><ul>${TIPS[t].map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>` : "";',
    '  const tips = guideHazards(t, isMoon ? m : null, false);')
i = s.index('    const srcRows = (m.sources || []).map(src => {'); j = s.index('    }).join("");', s.index('    const outRows', i)) + len('    }).join("");')
s = s[:i] + '''    const srcRows = grouped(incoming(t), x => `<div class="row"><span data-srcchip="${esc(x.src)}"></span><div>${esc(x.how || "See the source moon's page.")}</div></div>`)
      || (m.unlockedByHtml ? `<div class="wiki" style="padding:0;border:0;background:none">${m.unlockedByHtml}</div>` : `<p>${m.default ? "Unlocked by default." : "See below."}</p>`);
    const outRows = grouped(outgoing(t), x => `<div class="row"><label><input type="checkbox" data-found="${esc(t + ">" + x.to)}"><a class="mn" href="${esc(moonLink(x.to))}">${esc(x.to)}</a></label><div>${esc(x.how)}</div></div>`);''' + s[j:]

# 6. item links in wiki content
rep('  $$("img", root).forEach(im => im.addEventListener("click"', '  linkItems(root);\n  $$("img", root).forEach(im => im.addEventListener("click"')

# 7. items route, nav, popover element, data
rep('<a href="#guides" data-tab="guides">Guides &amp; items</a>', '<a href="#item-uses" data-tab="item-uses">What items do</a>\n      <a href="#guides" data-tab="guides">Guides</a>')
rep('  <section class="view" id="v-page"></section>', '  <section class="view" id="v-page"></section>\n  <section class="view" id="v-items"></section>')
rep('<div class="lb" id="lb"', '<div class="pop" id="pop" role="dialog" aria-label="Item details" hidden></div>\n<div class="lb" id="lb"')
rep('  else if (h === "field-notes"){', '  else if (h === "item-uses"){ $("#v-items").classList.add("on"); renderItems(); }\n  else if (h === "field-notes"){')
rep('window.INTICONS = mj.intIcons || {};', 'window.INTICONS = mj.intIcons || {}; window.ITEMS = mj.items || {};')

# 8. CSS: new bits + tighter spacing
CSS = '''
.wsec{margin:2px 0 8px}
.wsh{font:600 11px var(--font-mono);text-transform:uppercase;letter-spacing:.08em;padding:3px 0;margin-bottom:2px;border-bottom:2px solid}
.wsh span{opacity:.7}
.wsh.g{color:var(--ok);border-color:var(--ok)}
.wsh.r{color:var(--warn);border-color:var(--warn)}
h3.nh{font:600 13px var(--font-mono);text-transform:uppercase;letter-spacing:.06em;margin:10px 0 6px}
h3.nh.g{color:var(--ok)} h3.nh.r{color:var(--warn)}
.gh{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:10px}
.gh.compact{grid-template-columns:1fr;gap:8px;margin-top:8px}
.gh .callout,.gh .hazbox{margin:0}
.hazbox{border:1px solid var(--bad);border-left:4px solid var(--bad);background:color-mix(in srgb,var(--bad) 8%,var(--panel));border-radius:var(--radius);padding:10px 12px}
.hazbox h2,.hazbox h3,.gh .callout h2,.gh .callout h3{font-size:16px;margin:0 0 4px}
.hazbox h2,.hazbox h3{color:var(--bad)}
.gh.compact h3{font:600 12px var(--font-mono)!important;text-transform:uppercase;letter-spacing:.08em}
.hazbox ul,.gh .callout ul{margin:0;padding-left:18px}
.hazbox li,.gh .callout li{margin:2px 0;font-size:14px}
.gh.compact li{font-size:13px}
.itemlink{font:inherit;color:var(--accent);background:none;border:0;padding:0;cursor:pointer;text-align:left;text-decoration:underline dotted;text-underline-offset:3px}
.itemlink.info{font:700 11px var(--font-mono);text-decoration:none;border:1px solid var(--accent);border-radius:50%;width:17px;height:17px;display:inline-grid;place-items:center;vertical-align:middle}
.pop{position:fixed;z-index:60;background:var(--panel);border:1px solid var(--accent);border-radius:var(--radius);box-shadow:0 10px 30px rgba(0,0,0,.35);padding:10px 12px;font-size:14px}
.pop[hidden]{display:none}
.pop b{font:700 17px var(--font-display);display:block;margin:2px 0 4px;padding-right:20px}
.pop p{margin:0 0 6px}
.pop .pclose{position:absolute;top:4px;right:6px;border:0;background:none;color:var(--muted);font-size:20px;cursor:pointer}
.pop .plinks{display:flex;gap:12px;font-size:13px;margin-top:6px}
table.items td{vertical-align:top;font-size:13.5px}
table.items tr.grp th{background:var(--bg);color:var(--accent);cursor:default;position:static}
/* tighter spacing */
body{line-height:1.45}
main{padding:12px 14px}
.top-in{padding:7px 14px;gap:8px 14px}
.panel{padding:12px}
.grid{gap:10px}
.hero{gap:10px!important;margin-bottom:10px!important}
.next-list{gap:6px}
.next-item{padding:7px 10px}
.next-item p{margin:2px 0}
.dossier{gap:12px}
.rail{gap:10px;top:62px}
.content{gap:10px}
.callout{padding:10px 12px}
.wiki{padding:12px 14px}
.wiki section + section{margin-top:14px}
.wiki h2.sec{font-size:19px;margin:0 0 6px;padding-bottom:4px}
.wiki h3.sec{margin:12px 0 4px}
.wiki h4.sec{margin:10px 0 4px}
.wiki p{margin:4px 0}
.wiki details{margin:6px 0}
.mapbox{padding:10px}
.filters{margin:0 0 8px}
.cards,.bcards{gap:10px}
.tree{margin:-12px -14px 10px!important}
.foot{margin:6px auto 16px}
.reach .how{gap:4px}
.reach .row{padding-top:5px}
.tree-side{padding:12px}
.tree-side h3{margin:10px 0 4px}
'''
rep('@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}', CSS + '\n@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
