"""Interiors: Wesley's / Vanilla / All filter with guide cards for Facility, Mansion (Manor) and Mineshaft."""
import sys
S = sys.argv[1]
p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]
    s = s.replace(a, b, 1)

CSS = '''
.vint{display:grid;grid-template-columns:minmax(260px,380px) 1fr;gap:0;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;margin-bottom:12px;scroll-margin-top:calc(var(--top) + 10px)}
.vint>img{width:100%;height:100%;min-height:220px;object-fit:cover;display:block;cursor:zoom-in}
.vint .vbody{padding:10px 14px}
.vint h2{margin:0;font-size:20px}
.vint .aka{font:600 11px var(--font-mono);text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.vint p{margin:6px 0;font-size:14px}
.vint .gh{margin-top:8px}
.vint .gh h3{font:600 12px var(--font-mono);text-transform:uppercase;letter-spacing:.08em;margin:0 0 4px}
.vint .moonsline{font-size:13px;color:var(--muted)}
.vint.flash{outline:2px solid var(--accent)}
@media (max-width:760px){.vint{grid-template-columns:1fr}.vint>img{min-height:0;aspect-ratio:16/9}}
'''
rep('@media (prefers-reduced-motion: reduce)', CSS + '\n@media (prefers-reduced-motion: reduce)')

JS = r'''
/* ---------- vanilla interiors ---------- */
const VINT = [
 {id:"facility", n:"Facility", aka:"Factory · vanilla", names:["Facility","Factory"], link:"https://lethal.miraheze.org/wiki/Factory",
  d:"The most common vanilla interior: maze-like concrete hallways, storage and server rooms, and catwalks over deep pits across two floors. The apparatus sits in a room with a big power machine.",
  g:["Use the ship terminal: type a security door's code (shown on the radar map) to open it, or a turret's/mine's code to switch it off for a few seconds. Keep one person on the terminal if you can.",
     "Turning off the breaker box cuts the lights but opens every security door for good.",
     "Fire exits only open onto catwalks or the small loot rooms. Note where they are; they're often a quicker way out.",
     "Catwalks: walk, don't sprint, near the broken gap; jump the bent beam carefully with heavy scrap.",
     "The apparatus is worth ~80 (and needed for Repress repairs). Pulling it kills the power, so grab the rest of your loot first and expect enemies to get busier."],
  h:["Turrets in hallways: disable them from the terminal or stay out of their sweep.", "Landmines: step off and away quickly, or disable from the terminal.", "Long pits under catwalks: falling is instant death.", "Thumpers and Coil-Heads love the long hallways; keep corners between you and them."]},
 {id:"mansion", n:"Mansion", aka:"Manor · vanilla", names:["Mansion","Manor"], link:"https://lethal.miraheze.org/wiki/Mansion",
  d:"Carpeted hallways and household rooms on two floors: a big foyer with a balcony, library, kitchen, bedrooms, bathroom, garage, party room and a pool. Mostly on Rend and Dine in vanilla; on Wesley's moons it shows up on about a dozen moons.",
  g:["Scrap hides in closets under stairs, cupboards, bathroom drawers, alcoves and sometimes in the pool. Check them all.",
     "No security doors here; locked doors need a key or lockpicker.",
     "Fire exits always open into a bookshelf room, sometimes hidden behind a shelf (look for the red glow).",
     "To escape enemies, jump onto the foyer bookshelves, big tables or kitchen counters, then hop between them.",
     "Rooms are big and look alike: drop a marker or stick to one wing at a time and keep the foyer as your reference point."],
  h:["Butlers are common: they only attack when you're alone, so stay in pairs. A kitchen knife kills one in a hit; killing it releases Mask Hornets.", "Brackens and Ghost Girls use the many rooms and stairs to sneak up; check behind you.", "The pool's deep end can drown you: don't jump in with heavy loot.", "Wide open foyers mean ranged enemies (Nutcrackers) see you from far away."]},
 {id:"mineshaft", n:"Mineshaft", aka:"vanilla", names:["Mineshaft"], link:"https://lethal.miraheze.org/wiki/Mineshaft",
  d:"An elevator from the entrance takes you down to facility tunnels and a deep cave system. The caves, behind doorways with a blue light above them, hold most of the scrap.",
  g:["Head straight for the blue-lit doorways: that's where most scrap is.", "Caves are dark and branchy. Bring flashlights and mark your way back.",
     "The elevator is slow and the only way back from the main area except fire exits. Fire exits open straight into the hallways and skip the elevator, so find one early.",
     "Ride the elevator in groups and check it's empty before calling it."],
  h:["Getting stuck on the elevator with an enemy is a common death: don't call it if something is chasing you.", "Cave drops and narrow ledges: walk, don't sprint.", "Enemies come from the dark side passages; keep your back to a wall when looting."]}
];
let intFilter = localStorage.getItem("wm-ints") || "wes";
function vintIdFor(n){ const v = VINT.find(x => x.names.includes(n)); return v ? v.id : null; }
function vintCards(){
  const VI = window.VINTIMGS || {};
  return VINT.map(v => {
    const moons = Object.entries(M).filter(([n, m]) => !m.vanilla).filter(([n, m]) => { let L = m.interiors; if (typeof L === "string"){ try { L = JSON.parse(L.replace(/'/g, '"')); } catch(e){ L = []; } } return (L || []).some(([x]) => v.names.includes(x)); }).map(([n]) => n).sort();
    return `<article class="vint" id="vint-${v.id}">${VI[v.id] ? `<img src="${esc(VI[v.id])}" alt="${esc(v.n)} entrance" data-lb>` : "<div></div>"}<div class="vbody">
      <h2>${esc(v.n)}</h2><div class="aka">${esc(v.aka)}</div><p>${esc(v.d)}</p>
      ${moons.length ? `<p class="moonsline">Can be the interior on: ${moons.map(moonChip).join(" ")}</p>` : ""}
      <div class="gh"><div class="callout"><h3>Guide</h3><ul>${v.g.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div><div class="hazbox"><h3>Hazards</h3><ul>${v.h.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div></div>
      <p><a href="${esc(v.link)}" target="_blank" rel="noopener">Lethal Company wiki ↗</a></p></div></article>`;
  }).join("");
}
'''
rep('let entFilter =', JS + '\nlet entFilter =')

rep('''  if (k === "entity"){''', '''  if (k === "interior"){
    const seg = (v, l) => `<button aria-pressed="${intFilter === v}" data-if="${v}">${l}</button>`;
    const wes = `<div class="bcards">${cards}</div>`, van = vintCards();
    $("#v-list").innerHTML = `<div class="filters"><h1 style="font-size:24px;margin-right:8px">Interiors</h1><div class="seg" role="group" aria-label="Which interiors">${seg("wes", `Wesley's (${NAV[k].length})`)}${seg("van", `Vanilla (${VINT.length})`)}${seg("all", "All")}</div></div>
      <p style="color:var(--muted);margin:4px 0 12px">${intFilter === "van" ? "The base game's buildings. Many Wesley's moons can still roll them." : intFilter === "wes" ? "Building layouts added by the mod, with their hazards, puzzles and rewards." : "Wesley's interiors first, then the base game's."}</p>
      ${intFilter === "wes" ? wes : intFilter === "van" ? van : `${wes}<h2 style="font-size:18px;margin:16px 0 8px">Vanilla Lethal Company</h2>${van}`}`;
    $$("#v-list [data-if]").forEach(b => b.onclick = () => { intFilter = b.dataset.if; localStorage.setItem("wm-ints", intFilter); renderList(kind); });
    $$("#v-list .vint img[data-lb]").forEach(i => i.onclick = () => openLb(i.currentSrc || i.src, i.alt));
    return;
  }
  if (k === "entity"){''')

# moon pages: vanilla interior tiles link to their card
rep('''return sl ? `<a class="int" href="#${sl}" title="Open the ${esc(n)} guide">${inner}</a>` : `<span class="int">${inner}</span>`;''',
    '''const vi = !sl && vintIdFor(n); return sl ? `<a class="int" href="#${sl}" title="Open the ${esc(n)} guide">${inner}</a>` : vi ? `<a class="int" href="#vint-${vi}" title="Open the ${esc(n)} guide">${inner}</a>` : `<span class="int">${inner}</span>`;''')
rep('''const ic = window.INTICONS && INTICONS[n]; const inner''', '''const ic = (window.INTICONS && INTICONS[n]) || (vintIdFor(n) && (window.VINTIMGS || {})[vintIdFor(n)]); const inner''')

# routing: #vint-<id>
rep('''  else if (h === "interiors" || h === "entities" || h === "guides"){ $("#v-list").classList.add("on"); renderList(h); }''',
    '''  else if (h === "interiors" || h === "entities" || h === "guides"){ $("#v-list").classList.add("on"); renderList(h); }
  else if (h.startsWith("vint-")){ $("#v-list").classList.add("on"); if (intFilter === "wes") intFilter = "van"; renderList("interiors"); tab = "interiors";
    requestAnimationFrame(() => { const el = document.getElementById(h); if (el){ el.scrollIntoView({block:"start"}); el.classList.add("flash"); setTimeout(() => el.classList.remove("flash"), 1500); } }); return finishRoute(tab); }''')
rep('''  const a = $(`nav.tabs a[data-tab="${tab}"]`); if (a) a.setAttribute("aria-current","page");
  window.scrollTo(0,0);
}''', '''  finishRoute(tab); window.scrollTo(0,0);
}
function finishRoute(tab){ const a = $(`nav.tabs a[data-tab="${tab}"]`); if (a) a.setAttribute("aria-current","page"); }''')
rep('window.VENTS = mj.vents || [];', 'window.VENTS = mj.vents || []; window.VINTIMGS = mj.vintImgs || {};')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
