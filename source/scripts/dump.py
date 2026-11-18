import sys, json, urllib.request, urllib.parse, time
api, out = sys.argv[1], sys.argv[2]
def get(params):
    params['format']='json'
    req=urllib.request.Request(api+'?'+urllib.parse.urlencode(params),headers={'User-Agent':'wiki-reader/1.0'})
    for i in range(5):
        try: return json.load(urllib.request.urlopen(req,timeout=60))
        except Exception as e: time.sleep(2+i*3)
    raise
titles=[]; cont={}
while True:
    r=get({'action':'query','list':'allpages','apnamespace':0,'apfilterredir':'nonredirects','aplimit':500,**cont})
    titles+= [p['title'] for p in r['query']['allpages']]
    if 'continue' in r: cont=r['continue']
    else: break
with open(out,'w',encoding='utf-8') as f:
    for i in range(0,len(titles),50):
        r=get({'action':'query','prop':'revisions','rvprop':'content','rvslots':'main','titles':'|'.join(titles[i:i+50])})
        for p in r['query']['pages'].values():
            t=p.get('revisions',[{}])[0].get('slots',{}).get('main',{}).get('*','')
            f.write(f"\n\n######## {p['title']}\n{t}")
        time.sleep(0.5)
print(len(titles),'pages')
