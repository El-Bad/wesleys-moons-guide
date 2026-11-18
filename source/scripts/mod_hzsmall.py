"""Smaller hazard badge on the map; price & hazard on by default (new storage key resets old 'off')."""
import sys
S = sys.argv[1]; p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]; s = s.replace(a, b)
rep('const h = 22, h2 = 17;', 'const h = 18, h2 = 17;')
rep('const w1 = Math.max(hz.length * 9.4 + 10, 26)', 'const w1 = Math.max(hz.length * 8 + 8, 22)')
rep('const hx = x - R - w1 + 6,', 'const hx = x - R - w1 + 5,')
rep('<text x="${hx + w1 / 2}" y="${hy + 16}" text-anchor="middle" fill="#fff">', '<text class="hzt" x="${hx + w1 / 2}" y="${hy + 13.5}" text-anchor="middle" fill="#fff">')
rep('svg .tinfo text.prt{font-size:12.5px}', 'svg .tinfo text.prt{font-size:12.5px}\nsvg .tinfo text.hzt{font-size:13.5px}')
rep('localStorage.getItem("wm-tinfo") !== "0"', 'localStorage.getItem("wm-tinfo2") !== "0"')
rep('localStorage.setItem("wm-tinfo", tInfo ? "1" : "0")', 'localStorage.setItem("wm-tinfo2", tInfo ? "1" : "0")')
open(p, 'w', encoding='utf-8').write(s); print('ok')
