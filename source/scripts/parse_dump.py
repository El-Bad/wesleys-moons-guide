import sys, json, urllib.request, urllib.parse, time, os, re
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
    titles+=[p['title'] for p in r['query']['allpages']]
    if 'continue' in r: cont=r['continue']
    else: break
for t in titles:
    fn=os.path.join(out,re.sub(r'[^\w.-]','_',t)+'.json')
    if os.path.exists(fn): continue
    r=get({'action':'parse','page':t,'prop':'text|images|categories','disablelimitreport':1,'disableeditsection':1})
    json.dump({'title':t,'html':r['parse']['text']['*'],'images':r['parse']['images'],'cats':[c['*'] for c in r['parse'].get('categories',[])]},open(fn,'w',encoding='utf-8'))
    time.sleep(0.3)
print(len(titles))
