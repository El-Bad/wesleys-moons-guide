import json,sys,re,glob,os,io,urllib.request,urllib.parse,time,hashlib
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from PIL import Image
S=sys.argv[1]; OUT=os.path.join(S,'build','img')
names={}
def add(n,want,fw):
    o=names.get(n); 
    if not o or want>o[0]: names[n]=(want,fw)
for f in glob.glob(S+'/parsed/*.json'):
    d=json.load(open(f,encoding='utf-8')); s=BeautifulSoup(d['html'],'lxml')
    for im in s.find_all('img'):
        src=im.get('src',''); m=re.search(r'/images/(?:thumb/)?([^/?]+)',src)
        if not m: continue
        n=urllib.parse.unquote(m.group(1)); fw=int(im.get('data-file-width') or 0); w=int(im.get('width') or 0)
        if 'item-preview' in (im.get('class') or []) or w<=64: want=96
        elif im.find_parent(class_='gallerybox'): want=720
        else: want=min(900,max(2*w,480))
        add(n,want,fw)
    for m in re.finditer(r'"image":"/images/([^"?]+)',d['html']): add(urllib.parse.unquote(m.group(1)),1600,99999)
    for m in re.finditer(r'"markerIcon":"(?:https://commons\.wiki\.gg)?/images/(?:thumb/)?([^"?/]+)',d['html']): add(urllib.parse.unquote(m.group(1)),96,0)
def safe(n): 
    b=re.sub(r'[^A-Za-z0-9._-]','_',n.rsplit('.',1)[0])[:60]
    return b+'-'+hashlib.md5(n.encode()).hexdigest()[:6]
manifest={}
def job(item):
    n,(want,fw)=item
    ext=n.rsplit('.',1)[-1].lower(); q=urllib.parse.quote(n)
    host='https://commons.wiki.gg' if n=='Warning-red.svg' else 'https://wesleysmoons.wiki.gg'
    if ext=='svg': url=f'{host}/images/{q}'; outn=safe(n)+'.svg'
    elif fw and want<fw: url=f'{host}/images/thumb/{q}/{want}px-{q}'; outn=safe(n)+'.webp'
    else: url=f'{host}/images/{q}'; outn=safe(n)+'.webp'
    p=os.path.join(OUT,outn)
    if os.path.exists(p): return n,outn
    for i in range(4):
        try:
            data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'wiki-reader/1.0'}),timeout=60).read(); break
        except Exception as e:
            if i==3: print('FAIL',n,url,e); return n,None
            time.sleep(2+i*2)
    if ext=='svg': open(p,'wb').write(data); return n,outn
    try:
        im=Image.open(io.BytesIO(data)); im.seek(0); im=im.convert('RGBA') if im.mode in('P','LA','RGBA') else im.convert('RGB')
        if im.width>want: im=im.resize((want,round(im.height*want/im.width)),Image.LANCZOS)
        im.save(p,'WEBP',quality=72,method=5)
    except Exception as e: print('BAD',n,e); return n,None
    return n,outn
with ThreadPoolExecutor(8) as ex:
    for n,o in ex.map(job,names.items()):
        if o: manifest[n]=o
json.dump(manifest,open(os.path.join(S,'build','imgmap.json'),'w'),indent=0)
print(len(names),len(manifest))
