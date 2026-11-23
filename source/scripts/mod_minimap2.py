"""Mini map: move into the top rail panel (under the status), compact; shorter map legend."""
import sys
S = sys.argv[1]
p = S + '/build/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]; s = s.replace(a, b, 1)
rep('''        ${isMoon ? miniMap(t) : ""}
''', '')
rep('''          ${isMoon ? `<div class="status-row" id="statusbox"></div>` : ""}''',
    '''          ${isMoon ? `<div class="status-row" id="statusbox"></div>` : ""}
          ${isMoon ? miniMap(t) : ""}''')
rep('''  return `<div class="panel"><div class="mmcap"><span class="eyebrow">On the map</span><small>click to open</small></div>''',
    '''  return `<div class="mmwrap"><div class="mmcap"><span class="eyebrow">On the map</span><small>click to open</small></div>''')
rep('.mmcap{display:flex;', '.mmwrap{margin:8px 0 10px}\n.mmcap{display:flex;')
rep('<span>Click: details · Right-click or double-click: open guide · Middle-click: guide in new tab · Drag / scroll: pan &amp; zoom</span>',
    '<span>Click: details · Right/double-click: guide · Middle-click: new tab · Drag/scroll: pan &amp; zoom</span>')
open(p, 'w', encoding='utf-8').write(s); print('ok')
