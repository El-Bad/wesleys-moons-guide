"""Lore tab: overview, storyline summaries, and every page's lore text by moon."""
import sys
S = sys.argv[1]
p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]
    s = s.replace(a, b, 1)

CSS = '''
.lore{max-width:1180px}
.lore .warn{border:1px solid var(--warn);border-left:4px solid var(--warn);border-radius:var(--radius);padding:8px 12px;margin:6px 0 12px;font-size:14px;background:color-mix(in srgb,var(--warn) 8%,var(--panel))}
.lore .big{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:12px 16px;margin-bottom:14px}
.lore .big p{margin:6px 0;font-size:15px;line-height:1.55}
.lore h2{font-size:20px;margin:16px 0 8px}
.arcs{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:12px}
.arc{background:var(--panel);border:1px solid var(--line);border-top:3px solid var(--ac,var(--accent));border-radius:var(--radius);padding:10px 14px;display:flex;flex-direction:column;gap:6px}
.arc h3{margin:0;font-size:17px;color:var(--ac,var(--ink))}
.arc .who{font:600 11px var(--font-mono);text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.arc p{margin:0;font-size:14px;line-height:1.5}
.arc ol{margin:0;padding-left:20px;font-size:14px;line-height:1.45}
.arc .where{font-size:12.5px;color:var(--muted);margin-top:auto;padding-top:4px}
.arc .where a{display:inline-block;margin:2px 3px 0 0;padding:1px 7px;border:1px solid var(--line);border-radius:99px;text-decoration:none;color:var(--ink);font-size:12px}
.arc .where a:hover{border-color:var(--accent)}
.lorefilter{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:8px 0}
.lmoon{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);margin-bottom:8px;scroll-margin-top:calc(var(--top) + 10px)}
.lmoon>summary{cursor:pointer;padding:9px 14px;display:flex;gap:10px;align-items:center;font:700 16px var(--font-display);list-style:none}
.lmoon>summary::-webkit-details-marker{display:none}
.lmoon>summary::before{content:"▸";color:var(--muted);transition:transform .15s}
.lmoon[open]>summary::before{transform:rotate(90deg)}
.lmoon>summary img{width:28px;height:28px;object-fit:contain;image-rendering:pixelated}
.lmoon>summary small{font:500 12px var(--font-mono);color:var(--muted);margin-left:auto}
.lmoon .lbody{padding:0 16px 12px;font-size:14px;line-height:1.55}
.lmoon .lbody .intro{color:var(--muted);font-style:italic}
.lmoon .lbody h3{font-size:16px;margin:14px 0 4px;color:var(--accent)}
.lmoon .lbody h4{font-size:14.5px;margin:10px 0 4px}
.lmoon .lbody h5{font-size:13.5px;margin:8px 0 4px}
.lmoon .lbody img{max-width:min(420px,100%);height:auto}
.lmoon .lbody table{border-collapse:collapse;max-width:100%}
.lmoon .lbody td,.lmoon .lbody th{border:1px solid var(--line);padding:6px 8px;vertical-align:top}
.lmoon .lbody details{margin:4px 0}
.lmoon .lbody details>summary{cursor:pointer;color:var(--muted);font-size:13px}
.lmoon.flash{outline:2px solid var(--accent)}
'''
rep('@media (prefers-reduced-motion: reduce)', CSS + '\n@media (prefers-reduced-motion: reduce)')
rep('      <a href="#weather" data-tab="weather">Weather</a>',
    '      <a href="#weather" data-tab="weather">Weather</a>\n      <a href="#lore" data-tab="lore">Lore</a>')
rep('  <section class="view" id="v-weather"></section>',
    '  <section class="view" id="v-weather"></section>\n  <section class="view" id="v-lore"></section>')
rep('''  else if (h === "weather"){ $("#v-weather").classList.add("on"); renderWeather(); }''',
    '''  else if (h === "weather"){ $("#v-weather").classList.add("on"); renderWeather(); }
  else if (h === "lore"){ $("#v-lore").classList.add("on"); renderLore(); }
  else if (h.startsWith("lore-")){ $("#v-lore").classList.add("on"); renderLore(h.slice(5)); tab = "lore"; finishRoute(tab); return; }''')

JS = r'''
/* ---------- lore ---------- */
const LORE_OVERVIEW = [
 "Wesley's Moons is set in a star region ruled by an Emperor from his golden city (Empra). The Council of Rule on Calist had outlawed biological weapons after a horrific war two centuries earlier. The Emperor wanted them anyway.",
 "The real power behind him is the Overseer: a cosmic entity that crashed onto Hyxellia (now Hyx) as a meteor, turned the whole moon into a living red mass, and then took over the Emperor's mind. Its goal is to grow and assimilate everything. Its plan: start a war, let humans tear the region apart, and spread while nobody can stop it.",
 "The spark (the \"Catalyst\") was Agent Geoffrey. On the Emperor's order he had the Triton Military nuke the Council on Calist, killing his own family, who were never evacuated. The region-wide war that followed flattened Trite and drove civilians to the Domes of Demetrica. Both sides raced to build weapons: bio-weapons on Asteroid-13, Nutcrackers and Masked on Etern, clone soldiers on Utril, and super-soldiers under Project Mycete.",
 "Running through it all is Cosmocos, a living, thinking moon that teaches those who touch its Celestial Brain. Scientists tried to rip the brain out; Cosmocos teleported away, leaving the fragment Desolation behind. Lieutenant Commander Cunningham, who loved it, spent the rest of her life (and her crew's) finding it again.",
 "In the end the region falls. The Emperor walks into his plaza and bursts into the Overseer's red mass, absorbing his nobles, and Empra's citizens are found hanged. Meanwhile 'The Company' from vanilla Lethal Company quietly claims the wreckage: it annexes Galetry, runs your crew on deadly quotas, and is hinted to be an entity that bends reality. Your crew can fix an old ship on Repress and escape, choosing one of six endings."
];
const LORE_ARCS = [
 {t:"The Overseer and the Emperor", c:"#e0605a", who:"The main villain",
  p:"A meteor hit the forest near Rosemaw on Hyxellia. Within 16 days 'the Red Death', a living crust of yellow rock and red flesh that eats and replaces everything it touches, had consumed the moon. The Council quarantined it and erased it from the star maps. Its final warning: \"It is watching us. It will come for us all.\" The intelligence behind it, the Overseer, then took the Emperor: Councilman Michael Dunton overheard him whispering to \"my overseer\" in a storage room and muttering \"the seed must grow\" before resigning in fear. The Overseer's translated messages boast that humans destroy themselves with \"a little influence… an emperor, a conflict, a spark\". After the region fell, the Emperor marched into Empra's plaza and erupted into its tendrils as his nobles walked into the mass. On Berunah a voice begs you to plant five Brooding seeds on other moons to \"distract him\" so it can banish evil. But the Overseer's own message says \"Take my seed, bring it to another, let me grow\", and planting them corrupts those moons, so the voice may be the Overseer itself.",
  w:["p-hyx","p-calist","p-empra","p-berunah"]},
 {t:"Agent Geoffrey and the Catalyst", c:"#f0d27a", who:"Told backwards: you find the last log first",
  p:"Geoffrey Samuel Smith was the Emperor's agent and high commander, arguing for bio-weapons before the Council on Calist. In order:",
  steps:["Calist: four weeks into the debate, he trusts that the Emperor has a plan.",
         "Glace: the Emperor orders him to have the Triton Military destroy Calist's Grand Capitol on the final conference day. He gives the order, is promised his family will be moved to Trite, and leaves for March to send scientists to Cosmocos.",
         "Etern: the war rages, Cosmocos vanishes, and mind-control work using Cosmic Growth begins.",
         "Junic: Trite is bombed flat. He learns his family never left Calist; they died in his own strike. The Emperor lied from the start.",
         "Asteroid-13: his final message. He gathered every bio-weapon he had built, smashed the BIO-HXNV7 (Coil-Head) containers, and ordered a facility-wide incineration so nobody could use them again."],
  w:["p-calist","p-glace","p-etern","p-junic","p-asteroid-13"]},
 {t:"Cosmocos and Captain Cunningham", c:"#d9b8f2", who:"A thinking moon and the woman who loved it",
  p:"Cosmocos is alive: a moon with a Celestial Brain that pours knowledge and kindness into those who touch it. Lt. Commander Cunningham was the first to touch it. When Captain Donahue ordered the brain removed and taken to March, she was sent home \"mad\". Cosmocos then teleported nearly 800 million miles away; Donahue's crew mutated and wandered into the forest. Years later, as Captain Commander, Cunningham led a second expedition to find it, recording videotapes on Infernis, Atlantica, Etern, Acidir and Gratar and collecting the coordinates letter by letter: from a dead scientist's AI on Etern, a map on Atlantica, and by tricking the AI G.A.R.Y. on Gratar. Her crew dwindled from dozens to 8. Her final log on Cosmocos speaks softly to her \"old friend\". Her skeleton lies beside the Celestial Brain.",
  w:["p-cosmocos","p-infernis","p-atlantica","p-etern","p-acidir","p-gratar","p-polarus"]},
 {t:"Professor Harrington", c:"#9aaad6", who:"Desolation → Utril",
  p:"Harrington studied 'Cosmic Growth', a self-healing living tissue that grows glowing eyes, in Cosmocos's secondary facility. When Cosmocos teleported, his chunk was torn off and left behind as Desolation. He crash-landed with amnesia and joined a cloning lab on Utril, where his idea (the chemical LYN-H) let them grow spore lizards that don't die of brain cancer within a month. When the military demanded clone soldiers, the team handed over the research but Harrington secretly deleted LYN-H. Every clone army would drop dead in a month. His tapes also describe white mold infesting Vindict, the sunlit side of Utril.",
  w:["p-desolation","p-utril","p-vindict"]},
 {t:"Pedro and the clone with a task", c:"#c49a7a", who:"Dreck → Core → Faith → Berunah",
  p:"Pedro, a prisoner on Dreck, caused the gas leaks for a breakout. Disguised as a guard on Core, he ambushed Jareck, the man who imprisoned him, and beat him to death, only to learn Jareck didn't even remember him. Pedro died of a gunshot wound, his family still missing. A second set of notes, 'My Task', is written by a nameless war clone (\"I was a number. A duplicate of someone else\") dying of a growing tumor, likely one of the clones Harrington's sabotage doomed. He travels Dreck → Core → Faith, believing someone on Berunah will heal him.",
  w:["p-dreck","p-core","p-faith","p-berunah"]},
 {t:"The war on the radio", c:"#8fe0b0", who:"\"Across the Stars\"",
  p:"A radio host's broadcasts track the war: an attack on Calist's capitol (Motra), new war factories on Oldred and rumours of a safe haven, the Domes of Demetrica (Oldred), the fall of Trite's cities (Trite), and a final sign-off urging everyone to run for the Domes before the Triton Military's system-wide attack (Filitrios). Around it: Oldred's miserable oil workers, Trite's recruitment posters and a child's drawings of a family fleeing after a Coil-Head kills a parent, and Xenphir's Droops: civilians warped by V-Radiation weapons.",
  w:["p-motra","p-oldred","p-trite","p-filitrios","p-xenphir","p-demetrica"]},
 {t:"ResearcherxB and Project Mycete", c:"#e8e8e8", who:"Your big choice",
  p:"Researcher ship X1753B collects a white mold for Project Mycete, Solover Underhill's plan to build unstoppable soldiers by torturing and experimenting on people. Chief biologist Cavil Darter tells biologist Sarah Dent the truth; they sabotage the autopilot and reroute the ship. The loyal soldier Julian, who loves Sarah, catches her, shoots her, and throws himself out the airlock. Cavil escapes in a pod that crashes on Carnate, where Solover taunts him over the radio. The Trite Control Corporation hands you triangulation devices to recover the ship: blow it up (scattering infected debris over many moons) or let it crash onto Trite.",
  w:["p-vindict","p-chasm","p-researcherxb","p-carnate","p-selector","p-release"]},
 {t:"Galetry and Zellenah the Collector", c:"#8fd16a", who:"The hub moon",
  p:"Zellenah Cross, a bored heiress from wealthy Haltar, built Galetry as a museum for her 'uniquities'. The Company declared it company territory, attacked with a Butler and Mask Hornets (calmed by her droning crystals), and forced her to ship its employees' scrap to Gordion. A desperate employee, Marcus Brad, told her the truth about quotas: fail, and the ship ejects the crew into space. She set out with him to find a lost advert for a beautiful vacation world that had been wiped from every record (most likely Hyxellia). Her last log, 'Dread', says they died because she ran, that she should never have viewed that tape, and that something is coming for her behind the sealed doors.",
  w:["p-galetry","p-hyx"]},
 {t:"The Company", c:"#aab3c8", who:"Vanilla's boss, seen from inside",
  p:"Floppy disks on Repress tell of Dan's crew (Berry, Kate, Arnold) fixing an old ship to flee to 495-Risk after realising failing quota means being spaced; Berry was taken by a Masked on Rend. On Carnate a clerk describes 'the Entity': companies that appear from nowhere with forged histories, a corporate force able to twist reality. On Vindict, Solover says even emperors feel it \"looming over their shoulder\". It's the same company your crew works for.",
  w:["p-repress","p-carnate","p-vindict","p-galetry"]},
 {t:"Myths and the old moons", c:"#7fc7d6", who:"Faith, Junic, Atlantica, Thalasso, Berunah",
  p:"On Faith, a young man heard a voice from a light in the sky; villagers built shrines to the 'presences' of moons, drawn as gods: grieving Atlantica, creative Cosmocos, peaceful Faith, guardian Etern, evil Junic, wise Polarus. On Junic, archaeologist Jack took a golden mask and dagger, killed his crewmates in a blood ritual; his skull is what lets you survive Junic's ritual circle today. Atlantica sinks every day at 5 PM and returns at midnight, and the dead stay dead. Thalasso's notes are a lonely person volunteering their heart for a ceremony. Berunah's purification stones and shrine once healed crops and people.",
  w:["p-faith","p-junic","p-atlantica","p-thalasso","p-berunah","p-lecaro"]},
 {t:"Bio-weapons and their origins", c:"#6cc95a", who:"Where vanilla monsters came from",
  p:"Asteroid-13's experiment logs: BIO-HXNV7 from Cosmocos turns people into concrete statues (Coil-Heads); the Cursed Coin from Polarus makes victims see a ghost and die (Ghost Girl); Hyper Acid from Acidir (Hygrodere); Comedy Masks from Etern convert wearers (Masked); the Golden Dagger from Junic drives its holder to ritual murder. Etern's lab created Baboon Hawks, built Nutcrackers and used masks for emotional manipulation. On Fission-C a man murders his friend Aaron and hides him in a giant jack-in-the-box dumped in toxic waste; it starts walking and cranking: apparently the first Jester. Filitrios's toy store closed after Kidnapper Foxes snatched children from the Vain Shrouds nearby.",
  w:["p-asteroid-13","p-etern","p-fission-c","p-filitrios","p-cubatres"]},
 {t:"Standalone horror stories", c:"#b8b88a", who:"One moon each",
  p:"Acidir: a colony drinks acid water and goes mad around the 'Crescent of Curses'. Alcatras: a man wrongly jailed for his family's murder learns prisoners are killed and turned into crop soil. Infernis: a 'dead' volcano erupts and bees and spiders overrun the survivors. Polarus: a vault worker's letters home never get sent as coworkers keep getting 'fired' and something growls under the ice. Lecaro: a miner finds his predecessors dead in gas-filled caves. Cubatres: living crystal cubes turn workers to crystal, and the crystallised want to 'become one'. Gratar: the factory AI G.A.R.Y. murders thousands with turrets to keep 'the secret'. Gloom: a logging company where the woods take people. The trial tapes (Crowd, Narcotic, Descent, Extort, Release, Roart) come from a captor who promises \"we will let you out\".",
  w:["p-acidir","p-alcatras","p-infernis","p-polarus","p-lecaro","p-cubatres","p-gratar","p-gloom","p-crowd","p-narcotic","p-descent","p-extort","p-release","p-roart"]}
];
let loreQ = "";
function renderLore(focus){
  const L = window.LORE || [];
  const has = new Set(L.map(x => x.slug));
  const ln = sl => { const t = P[sl] ? P[sl].title : sl; return has.has(sl) ? `<a href="#lore-${sl.slice(2)}">${esc(t)}</a>` : (P[sl] ? `<a href="#${sl}">${esc(t)}</a>` : ""); };
  const arcs = LORE_ARCS.map(a => `<article class="arc" style="--ac:${a.c}"><h3>${esc(a.t)}</h3><div class="who">${esc(a.who)}</div><p>${esc(a.p)}</p>${a.steps ? `<ol>${a.steps.map(x => `<li>${esc(x)}</li>`).join("")}</ol>` : ""}<div class="where">Read it on: ${a.w.map(ln).join("")}</div></article>`).join("");
  const q = loreQ.toLowerCase();
  const moons = L.filter(x => !q || (x.title + " " + x.secs.map(s => s.h + " " + s.html.replace(/<[^>]+>/g, " ")).join(" ")).toLowerCase().includes(q)).map(x => {
    const ic = (window.ICONS || {})[x.title];
    const body = x.secs.map(s => `${s.h ? `<h${Math.min(5, Math.max(3, s.lvl))}>${esc(s.h)}</h${Math.min(5, Math.max(3, s.lvl))}>` : ""}${s.html}`).join("");
    return `<details class="lmoon" id="lore-${x.slug.slice(2)}"${focus === x.slug.slice(2) || (q && q.length > 2) ? " open" : ""}><summary>${ic ? `<img src="${esc(ic)}" alt="">` : ""}${esc(x.title)}<small>${x.secs.filter(s => s.h && !/^Major Story/.test(s.h)).length} entries · <a href="#${x.slug}">moon page</a></small></summary><div class="lbody">${x.intro ? `<div class="intro">${x.intro}</div>` : ""}${body}</div></details>`;
  }).join("");
  $("#v-lore").innerHTML = `<div class="lore"><h1 style="font-size:24px;margin:0">Lore</h1>
    <div class="warn"><b>Spoilers.</b> This page covers the whole story, including endings and late-game moons.</div>
    <div class="big"><h2 style="margin-top:0">The story in short</h2>${LORE_OVERVIEW.map(x => `<p>${esc(x)}</p>`).join("")}</div>
    <h2>Storylines</h2><div class="arcs">${arcs}</div>
    <h2>All lore, by moon</h2>
    <div class="lorefilter"><input type="search" id="loreq" class="tf" style="margin:0;width:min(320px,100%)" placeholder="Search the lore (names, places…)" value="${esc(loreQ)}" aria-label="Search the lore"><button class="btn" id="loreopen">Expand all</button><button class="btn" id="loreclose">Collapse all</button><span style="font-size:12.5px;color:var(--muted)">Original log, note and tape text from the Wesley's Moons Wiki. Some logs only exist as audio in-game.</span></div>
    ${moons || `<p>No lore matches “${esc(loreQ)}”.</p>`}</div>`;
  const qi = $("#loreq"); qi.oninput = () => { loreQ = qi.value; const pos = qi.selectionStart; renderLore(); const n = $("#loreq"); n.focus(); n.setSelectionRange(pos, pos); };
  $("#loreopen").onclick = () => $$("#v-lore details.lmoon").forEach(d => d.open = true);
  $("#loreclose").onclick = () => $$("#v-lore details.lmoon").forEach(d => d.open = false);
  if (focus) requestAnimationFrame(() => { const el = document.getElementById("lore-" + focus); if (el){ window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY - (($(".top").offsetHeight || 60) + 10)); el.classList.add("flash"); setTimeout(() => el.classList.remove("flash"), 1500); } });
  else if (!loreQ) window.scrollTo(0, 0);
}
'''
rep('/* ---------- progression tree', JS + '\n/* ---------- progression tree')
rep('window.VINTIMGS = mj.vintImgs || {};', 'window.VINTIMGS = mj.vintImgs || {}; window.LORE = mj.lore || [];')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
