"""Smaller in-game style credit sign before prices."""
import sys
S = sys.argv[1]; p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()
n = s.count('"▮" +')
s = s.replace('const pr = m.price ? "▮" + m.price : "Free";', 'const pr = m.price ? String(m.price) : "Free";')
s = s.replace('"▮" + ', 'CR + ')
s = s.replace('/* ---------- hazard ranking ---------- */', '/* ---------- hazard ranking ---------- */\nconst CR = \'<span class="cr" aria-label="credits">▮</span>\';', 1)
s = s.replace('@media (prefers-reduced-motion: reduce)', '.cr{display:inline-block;font-size:.62em;transform:scaleX(.8);margin-right:1px;vertical-align:.12em;opacity:.9}\n@media (prefers-reduced-motion: reduce)', 1)
# map tag: small tspan for the sign
old = '''text-anchor="middle" fill="${m.price ? "#f3c27a" : "#5cc28a"}">${esc(pr)}</text></g>`;'''
assert old in s
s = s.replace(old, '''text-anchor="middle" fill="${m.price ? "#f3c27a" : "#5cc28a"}">${m.price ? `<tspan font-size="8.5" dy="-1">▮</tspan><tspan dy="1">${esc(pr)}</tspan>` : esc(pr)}</text></g>`;''')
s = s.replace('w2 = pr.length * 7.4 + 9;', 'w2 = pr.length * 7.4 + (m.price ? 5 : 0) + 9;')
open(p, 'w', encoding='utf-8').write(s); print('replaced', n)
