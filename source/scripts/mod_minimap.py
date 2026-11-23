"""Map: middle-click a moon opens its page in a new tab. Moon pages: small map in the left rail highlighting the moon;
clicking it opens the main map with that moon selected (#map-<Moon>)."""
import sys
S = sys.argv[1]
p = S + '/build/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]; s = s.replace(a, b, 1)

CSS = '''
.minimap{display:block;border:1px solid var(--line);border-radius:6px;background:#07080c;overflow:hidden;line-height:0}
.minimap svg{width:100%;height:auto;display:block}
.minimap:hover,.minimap:focus-visible{border-color:var(--accent)}
.minimap .mmhalo{animation:mmpulse 1.6s ease-in-out infinite}
@keyframes mmpulse{0%,100%{opacity:.35}50%{opacity:.9}}
.mmcap{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px}
.mmcap small{color:var(--muted);font-size:11.5px}
'''
rep('@media (prefers-reduced-motion: reduce)', CSS + '\n@media (prefers-reduced-motion: reduce)')

JS = r'''
/* ---------- mini map on moon pages ---------- */
function miniMap(n){
  if (!TPOS[n]) return "";
  const col = x => isV(x) ? "#f0a23a" : isU(x) ? "#5cc28a" : available(x) ? "#c9a24a" : "#3d4250";
  const edges = TEDGES.map(([a, b]) => { const [x1, y1] = TPOS[a], [x2, y2] = TPOS[b]; const on = a === n || b === n;
    return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${on ? "#f0a23a" : "#2a2e38"}" stroke-width="${on ? 9 : 5}"/>`; }).join("");
  const dots = Object.entries(TPOS).filter(([x]) => M[x] && x !== n).map(([x, [cx, cy]]) => `<circle cx="${cx}" cy="${cy}" r="22" fill="${col(x)}"/>`).join("");
  const [x, y] = TPOS[n], lx = Math.max(140, Math.min(1860, x));
  const label = n === "End" ? "Repress" : n;
  return `<div class="panel"><div class="mmcap"><span class="eyebrow">On the map</span><small>click to open</small></div>
    <a class="minimap" href="#map-${encodeURIComponent(n)}" title="Show ${esc(label)} on the moon map" aria-label="Show ${esc(label)} on the moon map">
    <svg viewBox="-60 -40 2120 1220" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">${edges}${dots}
      <circle class="mmhalo" cx="${x}" cy="${y}" r="95" fill="#f0a23a"/><circle cx="${x}" cy="${y}" r="46" fill="#f3c27a" stroke="#07080c" stroke-width="10"/>
      <text x="${lx}" y="${y < 160 ? y + 140 : y - 80}" text-anchor="middle" fill="#fff" stroke="#07080c" stroke-width="16" paint-order="stroke" style="font:700 92px var(--font-display, sans-serif)">${esc(label)}</text>
    </svg></a></div>`;
}
'''
rep('function renderPage(slug){', JS + '\nfunction renderPage(slug){')
rep('''        ${toc ? `<div class="panel"><div class="eyebrow" style="margin-bottom:6px">On this page</div>''',
    '''        ${isMoon ? miniMap(t) : ""}
        ${toc ? `<div class="panel"><div class="eyebrow" style="margin-bottom:6px">On this page</div>''')

# route: #map-<Moon> opens the main map with the moon selected
rep('document.body.classList.toggle("home", h === "home");', 'document.body.classList.toggle("home", h === "home" || h.startsWith("map-"));')
rep('''  if (h === "home"){ $("#v-home").classList.add("on"); renderHome(); }''',
    '''  if (h === "home"){ $("#v-home").classList.add("on"); renderHome(); }
  else if (h.startsWith("map-")){ const n = decodeURIComponent(h.slice(4)); tsel = M[n] ? n : null; tv = null; history.replaceState(null, "", "#home");
    $("#v-home").classList.add("on"); renderHome(); tab = "home"; }''')

# middle-click a moon on the map: open its page in a new tab
rep('''    g.addEventListener("dblclick", open);''',
    '''    g.addEventListener("dblclick", open);
    g.addEventListener("mousedown", e => { if (e.button === 1) e.preventDefault(); });
    g.addEventListener("auxclick", e => { if (e.button !== 1) return; e.preventDefault(); const l = moonLink(g.dataset.n); if (!l || l === "#moons") return;
      window.open(l.startsWith("#") ? location.href.split("#")[0] + l : l, "_blank", "noopener"); });''')
rep('<span>Click: details · Right-click or double-click: open guide · Drag / scroll: pan &amp; zoom</span>',
    '<span>Click: details · Right-click or double-click: open guide · Middle-click: guide in new tab · Drag / scroll: pan &amp; zoom</span>')
open(p, 'w', encoding='utf-8').write(s); print('ok')
