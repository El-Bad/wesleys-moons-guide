import sys, json
S = sys.argv[1]
p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()
css = open(S + '/scripts/tree_css.txt', encoding='utf-8').read()
js = open(S + '/scripts/tree_js.txt', encoding='utf-8').read()
if '.tree-stage' not in s:
    a = '@media (prefers-reduced-motion: reduce){*{transition:none!important}}'
    assert a in s
    s = s.replace(a, css + '\n@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}')
    b = '/* ---------- home / tracker ---------- */'
    assert b in s
    s = s.replace(b, js + '\n' + b)
    old = '  $("#v-home").innerHTML = `\n  <div class="hero">'
    assert old in s
    new = '''  $("#v-home").innerHTML = `
  <div class="tree" id="tree">
    <div class="tree-stage">
      <div class="tree-tools"><button id="tzin" aria-label="Zoom in">+ Zoom</button><button id="tzout" aria-label="Zoom out">−</button><button id="tzreset">Fit</button><label><input type="checkbox" id="tall" ${tAll ? "checked" : ""}> Show all alternate routes</label></div>
      <div class="tree-legend"><span><i style="border-color:#f0a23a"></i>Visited</span><span><i style="border-color:#5cc28a"></i>Unlocked</span><span><i style="border-color:#f0a23a;border-style:dashed"></i>Reachable now</span><span><i style="border-color:#3a3f4a"></i>Locked</span><span>Click: details · Double-click: open guide · Drag / scroll: pan &amp; zoom</span></div>
      <div class="tree-credit">Layout after the community progression map by WhiteA12 (inspired by Nagatonis)</div>
    </div>
    <aside class="tree-side" aria-live="polite"></aside>
  </div>
  <div class="hero">'''
    s = s.replace(old, new)
    c = '  $$("#v-home [data-u]").forEach(b => b.onclick = () => { setU(b.dataset.u, true); });'
    assert c in s
    s = s.replace(c, c + '\n  renderTree();')
    d = 'P = pj.pages; PLAIN = pj.plain; NAV = pj.nav; M = mj.moons; MAPS = mj.maps;'
    assert d in s
    s = s.replace(d, d + ' window.ICONS = mj.icons || {};')
open(p, 'w', encoding='utf-8').write(s)
mj = json.load(open(S + '/build/data/moons.json', encoding='utf-8'))
mj['icons'] = json.load(open(S + '/build/data/icons.json'))
json.dump(mj, open(S + '/build/data/moons.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('ok')
