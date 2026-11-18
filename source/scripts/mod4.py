import sys
S = sys.argv[1]
p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]
    s = s.replace(a, b, 1)

i = s.index('function renderHome(){'); j = s.index('/* ---------- moon list ---------- */')
NEW = r'''function progressNumbers(){
  const wes = Object.values(M).filter(m => !m.vanilla && m.name !== "End");
  const avail = Object.keys(M).filter(available).sort((a,b) => hzRank(M[a].hazard) - hzRank(M[b].hazard) || (M[a].price||0) - (M[b].price||0));
  return {wes, uN: wes.filter(m => isU(m.name)).length, vN: wes.filter(m => isV(m.name)).length, avail};
}
function renderHome(){
  const {wes, uN, vN, avail} = progressNumbers();
  $("#v-home").innerHTML = `
  <div class="tree" id="tree">
    <div class="tree-stage">
      <div class="tree-tools"><button id="tzin" aria-label="Zoom in">+ Zoom</button><button id="tzout" aria-label="Zoom out">−</button><button id="tzreset">Fit</button><button id="tfull">⛶ Full screen</button><label><input type="checkbox" id="tall" ${tAll ? "checked" : ""}> Show all alternate routes</label><a class="tsum" href="#progress" title="Open the progress page">${uN}/${wes.length} unlocked · ${vN} visited · ${avail.length} reachable →</a></div>
      <div class="tree-legend"><span><i style="border-color:#f0a23a"></i>Visited</span><span><i style="border-color:#5cc28a"></i>Unlocked</span><span><i style="border-color:#f0a23a;border-style:dashed"></i>Reachable now</span><span><i style="border-color:#3a3f4a"></i>Locked</span><span>Click: details · Right-click or double-click: open guide · Drag / scroll: pan &amp; zoom</span></div>
      <div class="tree-credit">Layout after the community progression map by WhiteA12 (inspired by Nagatonis)</div>
    </div>
    <aside class="tree-side" aria-live="polite"></aside>
  </div>`;
  renderTree();
}
function renderProgress(){
  const {wes, uN, vN, avail} = progressNumbers();
  const card = n => {
    const m = M[n];
    const ways = incoming(n).filter(x => isU(x.src));
    const body = grouped(ways, x => `<p><span class="from">From ${esc(x.src)}</span><br>${esc(x.how || "See the moon's page.")}</p>`);
    return `<div class="next-item"><header>${hzPill(m.hazard)}<a href="${esc(moonLink(n))}">${esc(n)}</a><span class="chip mono">${m.price ? "▮" + m.price : "Free"}</span>${m.est ? `<span class="chip mono" title="Estimated loot per day">~${m.est} loot</span>` : ""}<button class="toggle tu" aria-pressed="false" data-u="${esc(n)}" style="margin-left:auto">Mark unlocked</button></header>${body}</div>`;
  };
  const sure = avail.filter(n => incoming(n).some(x => isU(x.src) && !x.random));
  const luck = avail.filter(n => !sure.includes(n));
  const nextHtml = avail.length ? `${sure.length ? `<h3 class="nh g">Guaranteed unlocks (${sure.length})</h3><div class="next-list">${sure.map(card).join("")}</div>` : ""}${luck.length ? `<h3 class="nh r">Random-drop unlocks (${luck.length})</h3><div class="next-list">${luck.map(card).join("")}</div>` : ""}` : `<p>Nothing new is reachable from your unlocked moons.</p>`;
  const goalsHtml = GOALS.map(([title, items]) => `<h3>${esc(title)}</h3><ul>${items.map(([k, t, d]) => `<li><label><input type="checkbox" data-goal="${k}" ${state.goals?.[k] ? "checked" : ""}><span>${esc(t)}${d ? `<small>${esc(d)}</small>` : ""}</span></label></li>`).join("")}</ul>`).join("");
  $("#v-progress").innerHTML = `
  <div class="hero">
    <div class="panel">
      <div class="eyebrow">Crew progress</div>
      <h1 style="font-size:26px;margin-top:2px">Where we are</h1>
      <div class="stats">
        <div class="stat"><b>${uN}<span style="font-size:16px;color:var(--muted)"> / ${wes.length}</span></b><span>Wesley moons unlocked</span></div>
        <div class="stat"><b>${vN}</b><span>Moons visited</span></div>
        <div class="stat"><b>${avail.length}</b><span>Unlocks within reach</span></div>
      </div>
      <div class="bar" aria-hidden="true"><i style="width:${Math.round(uN / wes.length * 100)}%"></i></div>
      <p style="margin:10px 0 0;font-size:14px;color:var(--muted)">Tick moons on the map, the moon list or each moon's page. "Next up" lists every moon you can reach from what you have, easiest first, with the exact step from each moon.</p>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px"><a class="btn primary" href="#home" style="text-decoration:none">Back to the map</a><a class="btn" href="#moons" style="text-decoration:none">Moon list</a><a class="btn" href="#field-notes" style="text-decoration:none">Field notes</a></div>
    </div>
    <div class="panel goals"><h2>Goals checklist</h2>${goalsHtml}</div>
  </div>
  <div class="panel next"><h2>Next up: moons you can unlock now</h2>${nextHtml}</div>`;
  $$("#v-progress [data-u]").forEach(b => b.onclick = () => setU(b.dataset.u, true));
  $$("#v-progress [data-goal]").forEach(c => c.onchange = () => { state.goals = state.goals || {}; state.goals[c.dataset.goal] = c.checked ? 1 : 0; commit(); });
}

'''
s = s[:i] + NEW + s[j:]

rep('<a href="#home" data-tab="home">Tracker</a>', '<a href="#home" data-tab="home">Map</a>\n      <a href="#progress" data-tab="progress">Progress</a>')
rep('  <section class="view" id="v-moons"></section>', '  <section class="view" id="v-progress"></section>\n  <section class="view" id="v-moons"></section>')
rep('  else if (h === "moons"){', '  else if (h === "progress"){ $("#v-progress").classList.add("on"); renderProgress(); }\n  else if (h === "moons"){')
rep('  if (h === "home") renderHome(); else if (h === "moons") renderMoons();', '  if (h === "home") renderHome(); else if (h === "progress") renderProgress(); else if (h === "moons") renderMoons();')
CSS = '''
/* home = map only, exactly one screen */
body.home{overflow:hidden}
body.home main{padding:0}
body.home .foot{display:none}
body.home .tree{margin:0!important;height:calc(100vh - var(--top,52px));border-bottom:0}
.tsum{font:600 12px var(--font-display);background:rgba(240,162,58,.18);color:#f3c27a;border:1px solid #6b4a1c;border-radius:5px;padding:5px 9px;text-decoration:none}
.tsum:hover{background:rgba(240,162,58,.3)}
@media (max-width:1000px){body.home{overflow:auto}body.home .tree{height:auto}}
'''
rep('@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}', CSS + '\n@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
