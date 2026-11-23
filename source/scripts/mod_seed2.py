"""New default progress (SEED) from the user's progress code; move share / load / reset box from Field notes to Progress."""
import sys, re, json
S = sys.argv[1]
p = S + '/build/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]; s = s.replace(a, b, 1)

seed = {"moons": {"Asteroid-13": {"u": 1, "v": 1}, "Junic": {"u": 1, "v": 1}, "Infernis": {"u": 1, "v": 1}, "Motra": {"u": 1, "v": 1},
        "Fission-C": {"u": 1}, "Oldred": {"u": 1}, "Galetry": {"u": 1, "v": 1}, "MorvDonalds": {"u": 1}, "Repress": {"u": 1},
        "Crowd": {"u": 1}, "Atlantica": {"u": 1}, "Narcotic": {"u": 1}, "Dreck": {"u": 1}, "Chasm": {"u": 1}, "Etern": {"u": 1},
        "Gratar": {"u": 1}, "Roart": {"u": 1}, "Thalasso": {"u": 1}, "Lecaro": {"u": 1}, "Acidir": {"u": 1}, "Trite": {"u": 1},
        "Duckstroid-14": {"u": 1}},
        "found": {"Asteroid-13>Junic": 1, "Motra>Fission-C": 1, "Motra>Oldred": 1}, "goals": {}, "t": 0}
s, n = re.subn(r'const SEED = \{.*?\};\n', 'const SEED = ' + json.dumps(seed, separators=(',', ':')) + ';\n', s, count=1)
assert n == 1

# cut the share block + its handlers out of renderNotes
a = s.index('  <h2>Share or back up this tracker</h2>')
b = s.index('  </div>\n  </div>`;', a) + len('  </div>\n')
block = s[a:b]
s = s[:a] + '  <p style="margin-top:14px"><a class="btn" href="#progress" style="text-decoration:none">Share, back up or reset your progress →</a></p>\n' + s[b:]
h1 = s.index('  $("#copycode").onclick')
h2 = s.index('\n}', h1)
handlers = s[h1:h2]
s = s[:h1].rstrip('\n') + s[h2:]

JS = ('function shareHtml(){\n  return `<div class="panel" style="margin-top:12px">' + block.replace('<h2>', '<h2 style="font-size:18px">') + '</div>`;\n}\n'
      'function wireShare(){\n' + handlers + '\n}\n')
JS = JS.replace('<p style="margin:4px 0 8px;font-size:14px">If crew sync is on, everyone with access sees the same ticks. You can also copy a code and paste it on another device.</p>',
                '<p style="margin:4px 0 8px;font-size:14px">Copy a code to back up your progress or move it to another device. New visitors start from the guide author\'s progress; press Reset tracker (twice) to start from zero.</p>')
rep('function renderProgress(){', JS + 'function renderProgress(){')
rep('''  <div class="panel next"><h2>Next up: moons you can unlock now</h2>${nextHtml}</div>`;
  $$("#v-progress [data-u]")''', '''  <div class="panel next"><h2>Next up: moons you can unlock now</h2>${nextHtml}</div>${shareHtml()}`;
  wireShare();
  $$("#v-progress [data-u]")''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
