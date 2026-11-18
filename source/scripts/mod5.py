import sys
S = sys.argv[1]
p = S + '/build/index.html'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:90]
    s = s.replace(a, b, 1)

CSS = '''
/* home: map runs to the top, nav floats top-left, map tools sit under it */
@media (min-width:1001px){
  body.home .top{position:fixed;top:10px;left:10px;right:auto;max-width:min(980px,calc(100vw - 400px));background:rgba(18,20,26,.92);border:1px solid #3a3f4c;border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.45);backdrop-filter:blur(6px)}
  body.home .top-in{padding:6px 10px;gap:6px 12px;max-width:none}
  body.home .top .brand b{color:#e9e4d8}
  body.home .top nav.tabs a{color:#b9b4a8}
  body.home .top nav.tabs a[aria-current="page"]{background:#3a2a12;color:#f3c27a}
  body.home .top .search{flex:1 1 180px;max-width:260px;margin-left:0}
  body.home .top .search input{background:#0d0f14;color:#e9e4d8;border-color:#3a3f4c;padding:6px 8px}
  body.home .top .sync{color:#9a9ea6}
  body.home .tree{height:100vh}
  body.home .tree-tools{top:calc(var(--navh,52px) + 20px)}
}
'''
rep('@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}', CSS + '\n@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}')
# keep --navh in sync with the floating nav's height (it may wrap to two rows)
rep('  document.documentElement.style.setProperty("--top", ($(".top").offsetHeight || 62) + "px");',
    '  document.documentElement.style.setProperty("--top", ($(".top").offsetHeight || 62) + "px");\n  requestAnimationFrame(() => document.documentElement.style.setProperty("--navh", ($(".top").offsetHeight || 52) + "px"));')
rep('window.addEventListener("resize", () => document.documentElement.style.setProperty("--top", ($(".top").offsetHeight || 62) + "px"));',
    'window.addEventListener("resize", () => { document.documentElement.style.setProperty("--top", ($(".top").offsetHeight || 62) + "px"); document.documentElement.style.setProperty("--navh", ($(".top").offsetHeight || 52) + "px"); });')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
