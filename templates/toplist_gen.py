import re,subprocess
base=open('top5.html').read()
hdr_end=base.find('<div style="display:flex;flex-direction:column;gap:12px">')
foot=base.find('<div style="margin-top: auto;')
head=base[:hdr_end]; tail=base[foot:]
rows=[('1','MAS Holdings','Apparel','1987','Clothing maker for Nike and other global brands; factories in 15+ countries','👕'),
('2','Dilmah','Ceylon Tea','1988','Took genuine Ceylon tea to tea drinkers around the world','🍵'),
('3','Hayleys','Conglomerate','1878','Started in Galle; now 17+ sectors selling to 80 markets','🏭'),
('4','Brandix','Apparel','1969','Makes clothes for global fashion brands; also in India','🧵'),
('5','LOLC','Finance','1980','Financial services in 25+ countries across Asia and Africa','🏦')]
def card(bg1,bg2,panel,line,acc,tag,h1a,h1b,sub,name):
    R=''.join(f'''<div style="display:flex;align-items:center;gap:18px;background:{panel};border:1px solid rgba(255,255,255,.10);border-left:8px solid {line};border-radius:14px;padding:17px 24px">
<span style="font-family:Archivo,sans-serif;font-weight:900;font-size:40px;color:{acc};width:28px">{n}</span>
<div style="width:62px;height:62px;flex:0 0 62px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-family:'Noto Color Emoji';font-size:34px;box-shadow:0 0 0 3px {acc}">{ic}</div>
<div style="flex:1;display:flex;flex-direction:column;gap:3px"><div style="display:flex;align-items:baseline;gap:12px"><span style="font-family:Archivo,sans-serif;font-weight:900;font-size:30px">{nm}</span><span style="font-size:16px;font-weight:700;letter-spacing:.12em;color:{acc};text-transform:uppercase">{sec}</span></div><span style="font-size:19px;color:rgba(255,255,255,.78)">{fact}</span></div>
<div style="display:flex;flex-direction:column;align-items:flex-end"><span style="font-size:13px;letter-spacing:.14em;color:rgba(255,255,255,.6)">SINCE</span><span style="font-family:Archivo,sans-serif;font-weight:800;font-size:29px">{yr}</span></div></div>''' for n,nm,sec,yr,fact,ic in rows)
    mid=f'''<div style="display:flex;flex-direction:column;gap:10px">
<span style="align-self:flex-start;background:{acc};color:#111;font-weight:800;font-size:20px;letter-spacing:.16em;padding:9px 18px;border-radius:6px">{tag}</span>
<h1 style="margin:0;font-family:Archivo,sans-serif;font-weight:900;font-size:60px;line-height:1.02;text-transform:uppercase">{h1a} <span style="color:{acc}">{h1b}</span></h1>
<p style="margin:0;font-size:22px;color:rgba(255,255,255,.8)">{sub}</p></div>
<div style="display:flex;flex-direction:column;gap:14px">{R}</div>
'''
    s=head+mid+tail
    s=s.replace('background: #111111;',f'background: linear-gradient(160deg,{bg1},{bg2});',1).replace('border-top: 1px solid #2E2E2E','border-top: 1px solid rgba(255,255,255,.18)')
    s=s.replace('color: #CFCFCF','color: rgba(255,255,255,.75)')
    open(name+'.html','w').write(s)
    subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=1.8963','--window-size=1080,1080','--screenshot='+name+'.png','file://'+__import__('os').getcwd()+'/'+name+'.html'],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
card('#005A54','#00302C','rgba(255,255,255,.08)','#F5C518','#F5C518','TOP 5 · SRI LANKA PRIDE','From Sri Lanka','to the world','5 companies born here that became global names','final')
