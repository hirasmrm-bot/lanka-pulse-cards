import re,subprocess,sys,json
from PIL import Image
S='/tmp/claude-0/-home-claude/738bfcb9-4b9a-51c8-92f0-b5f79f9acda1/scratchpad/'
t=open(S+'sq/gold.html').read()
i=t.find('<div style="display: flex; justify-content: space-between; align-items: center">')
j=t.find('</span>',t.find('NOV 2026',i))+len('</span>\n</div>')
header=t[i:j]
header=re.sub(r'\d\d NOV 2026','{{DATE}}',header)
header=header.replace('fill="#1C1C1C"','fill="#0B2347"')
def card(d,out):
    h=header.replace('{{DATE}}',d['date'])
    def fmt(v): return f"Rs {v/1e9:.2f} Bn" if v>=1e9 else f"Rs {v/1e6:,.1f} Mn"
    net=d['buy']-d['sell']
    up=net>=0
    netc='#22C55E' if up else '#F87171'
    netl=('NET FOREIGN BUYING' if up else 'NET FOREIGN SELLING')
    rows=''
    if d.get('topbuy') and d.get('topsell'):
        def li(xs,c,lab):
            r=''.join(f'<div style="padding:10px 0;border-top:1px solid rgba(160,190,240,.18)"><div style="font-size:24px;font-weight:700;color:#E6EEFB;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{k+1}. {n}</div><div style="font-family:Archivo;font-weight:900;font-size:34px;color:{c};margin-top:2px">{fmt(v)}</div></div>' for k,(n,v) in enumerate(xs))
            return f'<div style="flex:1;background:rgba(255,255,255,0.06);border:1px solid rgba(120,170,255,0.28);border-radius:26px;padding:20px 30px 12px"><div style="font-size:20px;font-weight:800;letter-spacing:.14em;color:#7FB2FF;padding-bottom:6px">{lab}</div>{r}</div>'
        rows=f'<div style="display:flex;gap:20px">{li(d["topbuy"],"#22C55E","TOP 2 FOREIGN BUYS")}{li(d["topsell"],"#F87171","TOP 2 FOREIGN SALES")}</div>'
    box='background:rgba(255,255,255,0.06);border:1px solid rgba(120,170,255,0.28);border-radius:26px;box-shadow:inset 0 1px 0 rgba(255,255,255,0.08)'
    chart=''
    if d.get('days') and not rows:
        mx=max(max(b,s) for _,b,s in d['days']) or 1
        cols=''
        for n,b,s in d['days']:
            hb=max(4,int(100*b/mx)); hs=max(4,int(100*s/mx))
            cols+=f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:10px"><div style="height:100px;display:flex;align-items:flex-end;gap:10px"><div style="width:34px;height:{hb}px;background:#22C55E;border-radius:6px 6px 0 0"></div><div style="width:34px;height:{hs}px;background:#F87171;border-radius:6px 6px 0 0"></div></div><div style="font-size:22px;font-weight:700;color:#C9D6EE">{n}</div></div>'
        chart=f'<div style="{box};padding:22px 32px"><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:20px;font-weight:800;letter-spacing:.14em;color:#7FB2FF">DAY BY DAY</span><span style="font-size:20px;color:#C9D6EE"><b style="color:#22C55E">■</b> Buying &nbsp; <b style="color:#F87171">■</b> Selling</span></div><div style="display:flex;margin-top:14px">{cols}</div></div>'
    html=f'''<!doctype html><html><head><meta charset="utf-8"><style>@font-face{{font-family:Archivo;src:url(archivo-latin-800-normal.woff2);font-weight:800}}@font-face{{font-family:Archivo;src:url(archivo-latin-900-normal.woff2);font-weight:900}}body{{margin:0}}</style></head><body>
<div style="width:1080px;height:1080px;box-sizing:border-box;padding:56px 64px 52px;background:radial-gradient(circle at 85% 8%,#1E4FA0 0%,rgba(30,79,160,0) 45%),linear-gradient(160deg,#0A2A5E 0%,#061A3D 55%,#030E24 100%);font-family:Inter,system-ui,sans-serif;color:#fff;display:flex;flex-direction:column;gap:20px;position:relative;overflow:hidden">
<svg style="position:absolute;right:-40px;top:120px;opacity:.07" width="520" height="300" viewBox="0 0 520 300"><polyline points="0,250 80,210 150,230 230,150 300,175 380,90 450,110 520,30" fill="none" stroke="#9CC3FF" stroke-width="6"/></svg>
{h}
<div><span style="display:inline-block;background:linear-gradient(90deg,#3B82F6,#60A5FA);color:#04122B;font-size:24px;font-weight:800;letter-spacing:.16em;padding:12px 22px;border-radius:8px">WEEKLY · FOREIGN INVESTORS</span></div>
<div style="font-family:Archivo,sans-serif;font-weight:900;font-size:80px;line-height:.95;letter-spacing:-.01em">CSE <span style="color:#7FB2FF">FOREIGN</span><br><span style="color:#7FB2FF">MONEY FLOW</span></div>
<div style="font-size:28px;color:#C9D6EE">{d['sub']}</div>
<div style="display:flex;gap:24px">
<div style="flex:1;{box};padding:22px 32px"><div style="font-size:22px;font-weight:800;letter-spacing:.14em;color:#7FB2FF">FOREIGN BUYING</div><div style="font-family:Archivo;font-weight:900;font-size:56px;margin-top:8px">{fmt(d['buy'])}</div></div>
<div style="flex:1;{box};padding:22px 32px"><div style="font-size:22px;font-weight:800;letter-spacing:.14em;color:#7FB2FF">FOREIGN SELLING</div><div style="font-family:Archivo;font-weight:900;font-size:56px;margin-top:8px">{fmt(d['sell'])}</div></div>
</div>
<div style="{box};padding:22px 32px;display:flex;justify-content:space-between;align-items:center;border-color:{netc}66"><div style="font-size:24px;font-weight:800;letter-spacing:.14em;color:#7FB2FF">{netl}</div><div style="font-family:Archivo;font-weight:900;font-size:60px;color:{netc}">{'▲' if up else '▼'} {fmt(abs(net))}</div></div>
{rows}
<div style="margin-top:auto;border-top:1px solid rgba(160,190,240,.25);padding-top:22px;display:flex;justify-content:space-between;font-size:21px;color:#B9C7E2"><span>Source: <b style="color:#fff">{d.get("src","Colombo Stock Exchange")}</b></span><span>Educational purposes only · Not investment advice</span></div>
</div></body></html>'''
    html=html.replace('–',' to ').replace('—',', ')
    open('_r.html','w').write(html)
    subprocess.run(['google-chrome','--headless','--no-sandbox','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=1.8963','--window-size=1080,1080','--screenshot=_r.png','file://'+S+'fw/_r.html'],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
    Image.open('_r.png').convert('RGB').save(out,quality=100,subsampling=0)
if __name__=='__main__':
    card(json.loads(open(sys.argv[1]).read()),sys.argv[2])
