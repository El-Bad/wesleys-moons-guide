"""Moons tab Wesley's/Vanilla/All filter; map price & hazard on by default with a smaller, closer price tag."""
import sys
S = sys.argv[1]
p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]
    s = s.replace(a, b, 1)

rep('let mf = {show:"all", vanilla:false, sort:"route", dir:1};', 'let mf = {show:"all", src:localStorage.getItem("wm-msrc") || "wes", sort:"route", dir:1};')
rep('let list = Object.values(M).filter(m => mf.vanilla || !m.vanilla);', 'let list = Object.values(M).filter(m => mf.src === "all" ? true : mf.src === "van" ? m.vanilla : !m.vanilla);')
rep('''      <label><input type="checkbox" id="vanilla" ${mf.vanilla ? "checked" : ""}> Include vanilla moons</label>''',
    '''      <div class="seg" role="group" aria-label="Which moons">${[["wes","Wesley's"],["van","Vanilla"],["all","All"]].map(([k, l]) => `<button aria-pressed="${mf.src === k}" data-src="${k}">${l}</button>`).join("")}</div>''')
rep('''  $("#vanilla").onchange = e => { mf.vanilla = e.target.checked; renderMoons(); };''',
    '''  $$("#v-moons [data-src]").forEach(b => b.onclick = () => { mf.src = b.dataset.src; localStorage.setItem("wm-msrc", mf.src); renderMoons(); });''')
rep('tInfo = localStorage.getItem("wm-tinfo") === "1";', 'tInfo = localStorage.getItem("wm-tinfo") !== "0";')
i = s.find('function tInfoBadge'); j = s.find('function treeSvg(){')
s = s[:i] + '''function tInfoBadge(n, x, y, R, lab){
  const m = M[n]; if (!m || n === "End") return "";
  const hz = ({"B.. for Bees":"B", "I see you":"??", "Quack":"Qk"})[m.hazard] || m.hazard || "?";
  const pr = m.price ? "▮" + m.price : "Free";
  const h = 22, h2 = 17;
  const w1 = Math.max(hz.length * 9.4 + 10, 26), w2 = pr.length * 7.4 + 9;
  const hx = x - R - w1 + 6, hy = y - h / 2, px = x - w2 / 2, py = y + R - 4;
  return `<g class="tinfo" aria-hidden="true"><rect x="${hx}" y="${hy}" width="${w1}" height="${h}" rx="5" fill="${HZFILL[hzClass(m.hazard)]}" stroke="#07080c" stroke-width="2"/><text x="${hx + w1 / 2}" y="${hy + 16}" text-anchor="middle" fill="#fff">${esc(hz)}</text>
    <rect class="pr" x="${px}" y="${py}" width="${w2}" height="${h2}" rx="4"/><text class="prt" x="${x}" y="${py + 12.5}" text-anchor="middle" fill="${m.price ? "#f3c27a" : "#5cc28a"}">${esc(pr)}</text></g>`;
}
''' + s[j:]
rep('svg .tinfo .pr{', 'svg .tinfo text.prt{font-size:12.5px}\nsvg .tinfo .pr{')
rep('el.scrollIntoView({block:"start"});', 'window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY - (($(".top").offsetHeight || 60) + 10));')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
