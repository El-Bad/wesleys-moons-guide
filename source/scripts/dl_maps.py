import json,sys,os,re,io,urllib.request,urllib.parse,hashlib
from PIL import Image
S=sys.argv[1]; OUT=os.path.join(S,'build','img')
imgmap=json.load(open(os.path.join(S,'build','imgmap.json')))
d=json.load(open(os.path.join(S,'build','maps_raw.json'),encoding='utf-8'))
need={}
maps={}
for p in d['query']['pages'].values():
    m=json.loads(p['revisions'][0]['slots']['main']['*']); t=p['title'][4:]
    bgs=m.get('backgrounds') or [{'name':'Terrain','image':m['background']}]
    for b in bgs: need[b['image']]=1600
    for g in m['groups'].values():
        if 'icon' in g: need[g['icon']]=96
    maps[t]=m
def safe(n):
    b=re.sub(r'[^A-Za-z0-9._-]','_',n.rsplit('.',1)[0])[:60]
    return b+'-'+hashlib.md5(n.encode()).hexdigest()[:6]
for n,want in need.items():
    n=n.replace(' ','_')
    if n in imgmap and want<1000: continue
    q=urllib.parse.quote(n); ext=n.rsplit('.',1)[-1].lower()
    for host in ('https://wesleysmoons.wiki.gg','https://commons.wiki.gg'):
        try: data=urllib.request.urlopen(urllib.request.Request(f'{host}/images/{q}',headers={'User-Agent':'wiki-reader/1.0'}),timeout=60).read(); break
        except Exception as e: data=None
    if not data: print('FAIL',n); continue
    if ext=='svg': outn=safe(n)+'.svg'; open(os.path.join(OUT,outn),'wb').write(data)
    else:
        im=Image.open(io.BytesIO(data)); im=im.convert('RGBA') if im.mode in('P','LA','RGBA') else im.convert('RGB')
        print(n, im.size)
        if im.width>want: im=im.resize((want,round(im.height*want/im.width)),Image.Resampling.LANCZOS)
        outn=safe(n)+('-map' if want>1000 else '')+'.webp'; im.save(os.path.join(OUT,outn),'WEBP',quality=78,method=5)
    imgmap[n]=outn if want<1000 else imgmap.get(n,outn)
    if want>1000: imgmap['MAP:'+n]=outn
json.dump(imgmap,open(os.path.join(S,'build','imgmap.json'),'w'),indent=0)
json.dump(maps,open(os.path.join(S,'build','maps.json'),'w',encoding='utf-8'))
