"""Spread out the right side of the map, names on top; weather sorted by risk."""
import sys, re
S = sys.argv[1]; p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]; s = s.replace(a, b, 1)
NEW = {"MorvDonalds":[1090,60], "Repress":[1230,60],
 "Motra":[1250,195], "Fission-C":[1400,195], "Selector":[1550,235], "Dormant":[1700,275], "Xenphir":[1850,315],
 "Oldred":[1250,325], "Duckstroid-14":[1420,340], "Trite":[1250,455], "Heap":[1400,470],
 "Vindict":[1080,585], "Filitrios":[1250,585], "Centrus":[1400,610], "Demetrica":[1250,715],
 "Desolation":[1700,490], "Facto":[1090,725], "Gratar":[1170,930],
 "Alcatras":[1570,760], "Gloom":[1770,760], "Hyve":[1670,945]}
for n, (x, y) in NEW.items():
    pat = re.compile(r'"%s":\[\d+,\d+\]' % re.escape(n))
    assert pat.search(s), n
    s = pat.sub('"%s":[%d,%d]' % (n, x, y), s, count=1)
for n in ["Selector","Dormant","Xenphir","Heap","Centrus","Duckstroid-14","Fission-C"]:
    s = s.replace('"%s":"r",' % n, '').replace(',"%s":"r"' % n, '')
rep('<rect x="1370" y="405" width="340" height="265" rx="8"/><rect x="1010" y="740" width="360" height="390" rx="8"/><rect x="1385" y="690" width="335" height="440" rx="8"/>',
    '<rect x="1520" y="395" width="380" height="160" rx="8"/><rect x="1010" y="810" width="330" height="200" rx="8"/><rect x="1480" y="650" width="420" height="380" rx="8"/>')
rep('<text x="1385" y="426">Alt. unlock: eclipse meteor or crash log</text><text x="1022" y="760">Gratar: tape always on Repress · fabricator</text><text x="1398" y="710">Random-drop moons: files, tapes, hives</text>',
    '<text x="1535" y="416">Alt. unlock: eclipse meteor or crash log</text><text x="1022" y="830">Gratar: tape always on Repress · fabricator</text><text x="1495" y="671">Random-drop moons: files, tapes, hives</text>')
rep('<text x="1560" y="132">Repress is unlocked from the start, like Galetry.</text><text x="1560" y="154">Bring a destiny item to Repress for an ending (6 endings).</text><text x="1560" y="180" fill="#8d8a82" font-size="13">',
    '<text x="1620" y="40">Repress is unlocked from the start, like Galetry.</text><text x="1620" y="62">Bring a destiny item to Repress for an ending (6 endings).</text><text x="1620" y="86" fill="#8d8a82" font-size="13">')
rep('const cards = WEATHER.map(w => {', 'const cards = [...WEATHER].sort((a, b) => a.risk - b.risk).map(w => {')
open(p, 'w', encoding='utf-8').write(s); print('ok')
