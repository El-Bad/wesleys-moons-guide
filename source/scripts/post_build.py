import json, sys
B = sys.argv[1]
mj = json.load(open(B + '/data/moons.json', encoding='utf-8'))
mj['icons'] = json.load(open(B + '/data/icons.json'))
mj['intIcons'] = json.load(open(B + '/data/inticons.json'))
mj['items'] = json.load(open(B + '/data/items.json', encoding='utf-8'))
json.dump(mj, open(B + '/data/moons.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('merged', len(mj['items']), mj['moons']['Junic'].get('traps'))
