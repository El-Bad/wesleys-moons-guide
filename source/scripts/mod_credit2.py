"""Use the in-game credit symbol shape (from the Lethal Company wiki's Scrap_Currency_Symbol.svg)."""
import sys
S = sys.argv[1]; p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]; s = s.replace(a, b, 1)
PTS = '0 0 3 0 3 2 7 2 7 4 11 4 11 6 13 6 13 19 0 19 0 0'
rep('''const CR = '<span class="cr" aria-label="credits">▮</span>';''',
    '''const CRPTS = "%s";
const CR = `<svg class="cr" viewBox="0 0 13 19" role="img" aria-label="credits"><polygon points="${CRPTS}" fill="currentColor"/></svg>`;''' % PTS)
rep('.cr{display:inline-block;font-size:.62em;transform:scaleX(.8);margin-right:1px;vertical-align:.12em;opacity:.9}',
    '.cr{display:inline-block;height:.72em;width:auto;aspect-ratio:13/19;margin-right:.18em;vertical-align:-.02em}')
# map price tag: icon + number, left aligned inside the pill
rep('w2 = pr.length * 7.4 + (m.price ? 5 : 0) + 9;', 'w2 = pr.length * 7.4 + (m.price ? 8 : 0) + 9;')
rep('''<text class="prt" x="${x}" y="${py + 12.5}" text-anchor="middle" fill="${m.price ? "#f3c27a" : "#5cc28a"}">${m.price ? `<tspan font-size="8.5" dy="-1">▮</tspan><tspan dy="1">${esc(pr)}</tspan>` : esc(pr)}</text></g>`;''',
    '''${m.price ? `<polygon points="${CRPTS.split(" ").map((v, i) => i % 2 ? (py + 4 + v * 0.5).toFixed(1) : (px + 5 + v * 0.5).toFixed(1)).join(" ")}" fill="#f3c27a"/><text class="prt" x="${px + 13}" y="${py + 12.5}" fill="#f3c27a">${esc(pr)}</text>` : `<text class="prt" x="${x}" y="${py + 12.5}" text-anchor="middle" fill="#5cc28a">${esc(pr)}</text>`}</g>`;''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
