import sys
S = sys.argv[1]
p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]
    s = s.replace(a, b, 1)

CSS = '''
.wx{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:12px}
.wxc{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--wc,var(--line));border-radius:var(--radius);padding:10px 12px;display:flex;flex-direction:column;gap:6px}
.wxc header{display:flex;gap:10px;align-items:flex-start}
.wxc header img{width:110px;height:70px;object-fit:cover;border-radius:4px;flex:none;cursor:zoom-in}
.wxc h2{margin:0;font-size:18px;color:var(--wc,var(--ink))}
.wxc .wtag{font:600 11px var(--font-mono);text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.wxc .wrisk{display:inline-block;font:600 11px var(--font-mono);padding:1px 6px;border-radius:3px;margin-left:6px;vertical-align:2px;border:1px solid currentColor}
.wxc p{margin:0;font-size:14px}
.wxc h3{font:600 12px var(--font-mono);text-transform:uppercase;letter-spacing:.06em;margin:4px 0 0;color:var(--ok)}
.wxc ul{margin:0;padding-left:18px;font-size:14px}
.wxc details summary{cursor:pointer;font-size:13px;color:var(--muted)}
.wxc details .chips{margin-top:6px}
@media (max-width:520px){.wx{grid-template-columns:1fr}}
'''
rep('@media (prefers-reduced-motion: reduce)', CSS + '\n@media (prefers-reduced-motion: reduce)')
rep('      <a href="#guides" data-tab="guides">Guides</a>',
    '      <a href="#weather" data-tab="weather">Weather</a>\n      <a href="#guides" data-tab="guides">Guides</a>')
rep('  <section class="view" id="v-items"></section>',
    '  <section class="view" id="v-items"></section>\n  <section class="view" id="v-weather"></section>')
rep('''  else if (h === "item-uses"){ $("#v-items").classList.add("on"); renderItems(); }''',
    '''  else if (h === "item-uses"){ $("#v-items").classList.add("on"); renderItems(); }
  else if (h === "weather"){ $("#v-weather").classList.add("on"); renderWeather(); }''')

JS = r'''
/* ---------- weather ---------- */
const WEATHER = [
 {n:"Clear", k:["None",""], src:"Vanilla", risk:0, c:"var(--ok)",
  d:"No weather. Normal enemy spawns and no extra outdoor hazards.",
  h:["Best days for learning a moon, doing puzzles and trials, or making a long scrap run.", "Night still brings outdoor enemies, so plan to be back at the ship before late evening."]},
 {n:"Foggy", src:"Vanilla", risk:1, c:"#9aa3ad",
  d:"Thick fog covers the outside. Enemies are near-sighted too: they can't spot you beyond about 30 units.",
  h:["Mostly a navigation problem. Leave someone on the ship terminal to guide people back, or follow the ship's lights and walls/paths.", "Walk the route out and back once before carrying heavy loot.", "Fog helps you sneak past outdoor enemies: keep your distance and they lose you."]},
 {n:"Rainy", src:"Vanilla", risk:1, c:"#5b8fd6",
  d:"Leaves patches of quicksand outside. Sinking all the way kills you, leaves no body and deletes everything you carry.",
  h:["Quicksand looks like a big round puddle of brown dirt. Watch the ground, especially at night and with a flashlight.", "If you start sinking, back out immediately. Don't sprint blindly across the outside.", "Otherwise a fine day: scrap and enemies are normal."]},
 {n:"Stormy", src:"Vanilla", risk:2, c:"#d6c25b",
  d:"Lightning. Metal (conductive) items outside get charged and then struck: 50 damage up to instant death depending on distance. Random strikes also hit around the map.",
  h:["When an item starts sparking and crackling, drop it and step well away. Wait a second or two before picking it back up; it can be struck more than once.", "Scroll through your slots to find which item is sparking: it sparks even when not in hand.", "A sparking item under a solid roof (or inside the ship) is safe; the bolt hits the roof.", "Carry metal scrap in short dashes between cover. Equipment bought that day isn't conductive until the ship leaves orbit.", "If lightning hits the ship, turn the lights back on with the switch and the monitor with its side power button."]},
 {n:"Flooded", src:"Vanilla", risk:2, c:"#3aa0b8",
  d:"Water rises outside through the day (roughly maximum by 5 PM). Water slows you, stops sprinting, drains stamina, and you drown if you stay under.",
  h:["Grab the outside scrap first and get the main entrance route done early.", "Be back on the ship before the water gets high, around mid-afternoon. Don't plan a late run.", "If the path floods, go around through higher ground rather than swimming with heavy loot."]},
 {n:"Eclipsed", src:"Vanilla", risk:3, c:"#d65b5b",
  d:"Night-time outdoor enemies spawn immediately and enemy spawns are much higher inside and out. No bonus loot.",
  h:["Usually skip it, or route somewhere else that day.", "If you must land: go straight in with the ship close to the main door, grab nearby scrap and leave early.", "Bring weapons and stun grenades, and never walk around outside alone."]},
 {n:"Earthquakes", src:"Wesley's Weathers", risk:2, c:"#B8860B", img:"img/EarthquakesWeather-644edc.webp", k:["Earthquakes","Earthquake"],
  d:"An earthquake roughly every 220 s (about 1 PM, 6 PM and 11 PM). Outside it's only shaking. Inside, the roof collapses and falling rubble crushes anyone under it; some rubble blocks paths for about 45 s. 1.1× scrap amount.",
  h:["Watch the clock: be outside or in a big open room around 1 PM and 6 PM, or listen for the rumble and stop moving.", "Rubble lands at random, so don't stand in narrow corridors when the shaking starts; keep moving out from under falling debris.", "If a path gets blocked, wait about 45 s instead of taking a dangerous detour.", "Slightly more scrap, so it's worth landing on."]},
 {n:"Forsaken", src:"Wesley's Weathers", risk:3, c:"#e05050", img:"img/ForsakenWeather-c8d4d6.webp", ent:[["The Wail","p-the-wail"],["Emma","p-emma"]],
  d:"Blood rain and Emma hauntings (scares only). The Wail, a 10 HP Bracken variant, spawns inside on landing, and the real entity Emma (a Ghost Girl variant) spawns inside at exactly 2 PM. 1.2× scrap amount and value.",
  h:["Treat The Wail like a Bracken: look at it briefly to make it back off, don't stare, and never walk into dead ends alone. With 10 HP it can be killed by a group with weapons.", "Get your big haul out before 2 PM, when Emma spawns. After that, leave or stay together and be ready to run.", "The flying scream encounters are only scares: keep calm and keep moving.", "Good money (1.2× amount and value) if your crew is confident."]},
 {n:"Hallowed", src:"Wesley's Weathers", risk:3, c:"#a35bd6", img:"img/HallowedWeather-3b42a9.webp", ent:[["Arachnohead","p-arachnohead"],["Corpse Crawler","p-corpse-crawler"],["Creaker","p-creaker"]],
  d:"Halloween decor outside, plus 'scrap head' traps: a pale head on a pole that wakes when you approach, locks a red eye light on you for 6–7 s and bites for 99 damage if you walk into the light. Inside spawns get Arachnoheads, Corpse Crawlers and Creakers.",
  h:["Scrap heads: when one wakes, step out of its red light and wait for it to go dormant (about 28 s cooldown before it can wake again). Never walk through the beam.", "Arachnohead (2 HP spider) explodes when it dies: kill it from a distance or back off after hitting it.", "Corpse Crawler spits Gore Spikes that pulse every ~8 s for 20 damage. Go around them.", "Creaker is a Nutcracker variant: freeze when it scans, or avoid its hallways.", "Avoid while learning; it's one of the more dangerous weathers."]},
 {n:"Hurricane", src:"Wesley's Weathers", risk:2, c:"#0096C7", img:"img/HurricaneWeather-cafd21.webp",
  d:"Strong wind and rain, and trees fall from the sky outside all day, sometimes many in a row. A tree knocks you back and does 50 damage near its impact, then stays as an obstacle. Spawns 8–9 extra scrap outside on landing (bells, steel ingots, kettles, sometimes a cash register).",
  h:["Grab the free outside scrap near the ship early, then go inside.", "Outside, keep moving and look up; don't stand still in open areas.", "Expect your path back to be blocked by fallen trees: plan another route or leave a little earlier.", "Steel ingots from the extra scrap are crafting material on Gratar/Galetry."]},
 {n:"Minefield", src:"Wesley's Weathers", risk:2, c:"#3ca050", img:"img/MinefieldWeather-8e6bc1.webp",
  d:"Several mines spawn outside on landing. They beep occasionally and faster when you're close; stand too close too long and they explode (30 damage, or instant death up close). Stepping on one is safe on its own.",
  h:["Listen for beeping and keep walking; never stop or wait near a mine.", "Walk single file on a route someone has already used, and spread the crew out so one blast doesn't hit everyone.", "Explosions also kill most entities and set Giants on fire, so you can lure enemies over them."]},
 {n:"Meteor shower", src:"Vanilla event", risk:2, c:"#e08a3c", k:[],
  d:"A random event, not a forecast weather: can start any time with an emergency alert on screen and lasts about 12 in-game hours. Meteors fall in waves and kill anything right where they land; nearby players are just knocked back.",
  h:["When the alert pops up, watch the sky outside. Meteors are slow: look for fireballs and move away from where they will land.", "Stay inside the building or the ship where you can, and cross the outside in quick dashes between waves."]}
];
function renderWeather(){
  const MS = Object.entries(M).filter(([n, m]) => !m.vanilla && m.weather !== undefined);
  const RISK = ["Low", "Low", "Medium", "High"], RC = ["var(--ok)", "var(--ok)", "var(--warn)", "var(--bad)"];
  const cards = WEATHER.map(w => {
    const keys = w.k || [w.n];
    const moons = keys.length ? MS.filter(([n, m]) => (m.weather || "").split(/,\s*/).some(x => keys.includes(x))).map(([n]) => n).sort() : [];
    const ents = (w.ent || []).map(([l, sl]) => P[sl] ? `<a href="#${sl}">${esc(l)}</a>` : esc(l)).join(", ");
    return `<article class="wxc" style="--wc:${w.c}" id="wx-${esc(w.n.toLowerCase().replace(/\s+/g, "-"))}"><header>${w.img ? `<img src="${esc(w.img)}" alt="${esc(w.n)} weather" data-lb="${esc(w.img)}">` : ""}<div>
      <h2>${esc(w.n)}<span class="wrisk" style="color:${RC[w.risk]}">${RISK[w.risk]} risk</span></h2><div class="wtag">${esc(w.src)}</div></div></header>
      <p>${esc(w.d)}</p>${ents ? `<p><b>Entities:</b> ${ents}</p>` : ""}
      <h3>How to handle it</h3><ul>${w.h.map(x => `<li>${esc(x)}</li>`).join("")}</ul>
      ${keys.length && w.n !== "Clear" ? `<details><summary>Can happen on ${moons.length} Wesley's moons</summary><div class="chips">${moons.map(moonChip).join(" ")}</div></details>` : ""}
    </article>`;
  }).join("");
  $("#v-weather").innerHTML = `<h1 style="font-size:22px;margin:0 0 4px">Weather</h1>
    <p style="margin:0 0 10px;font-size:13px;color:var(--muted)">Check the forecast in brackets next to each moon in the terminal's <code>moons</code> list. Vanilla weathers apply everywhere; Wesley's Weathers adds Earthquakes, Forsaken, Hallowed, Hurricane and Minefield. Vanilla weather doesn't change loot; Earthquakes, Forsaken and Hurricane do add scrap. ${P["p-weathers"] ? `Full details: <a href="#p-weathers">Weathers wiki page</a>.` : ""}</p>
    <div class="wx">${cards}</div>`;
  $$("#v-weather img[data-lb]").forEach(i => i.onclick = () => openLb(i.currentSrc || i.src, i.alt));
}
'''
rep('/* ---------- progression tree', JS + '\n/* ---------- progression tree')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
