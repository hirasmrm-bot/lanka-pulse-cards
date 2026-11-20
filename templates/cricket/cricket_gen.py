#!/usr/bin/env python3
"""LankaXpress cricket card, "Flag split" style (chosen by Hiras, 20 Nov 2026).
Usage: cd templates/cricket && python3 cricket_gen.py match.json out.jpg
JSON: {"left":"pk","right":"lk","tag":"RESULT · 2ND TEST","headline":"Pakistan beat Sri Lanka by 8 wickets",
"hl":"8 wickets","sub":"Series won 1 to 0 · Rathnayake 66 for Sri Lanka","source":"ICC","date":"20 NOV 2026","hashtag":"#PAKvSL"}
Flag codes = file names in flags/ (lk pk in au gb-eng nz za bd af zw ie nl ae np om us). Put the WINNER on the left.
West Indies has no national flag: use "wi" and a maroon panel is drawn instead."""
import json,sys,os,subprocess
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
d=json.load(open(sys.argv[1])); out=os.path.abspath(sys.argv[2])
l1=open(D+'/logo1.svg').read().replace('width="50" height="50"','width="54" height="54"')
l2=open(D+'/logo2.svg').read().replace('width="205" height="31"','width="220" height="33"')
def fl(code,side):
    clip='polygon(0 0,100% 0,62% 100%,0 100%)' if side=='l' else 'polygon(38% 0,100% 0,100% 100%,0 100%)'
    pos='left:-60px;width:720px' if side=='l' else 'right:-60px;width:740px'
    if code=='wi': return f'<div class=abs style="{pos};top:0;height:560px;background:#7B1E32;clip-path:{clip};display:flex;align-items:center;justify-content:center;font-family:Archivo;font-weight:900;font-size:110px;color:#F5C518">WI</div>'
    return f'<img src="flags/{code}.svg" class=abs style="{pos};top:0;height:560px;object-fit:cover;clip-path:{clip}">'
hl=d['headline'].replace(d.get('hl',''),f'<span style="color:#F5C518">{d.get("hl","")}</span>',1) if d.get('hl') else d['headline']
size=76 if len(d['headline'])<=40 else 64
h=f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:Archivo;src:url(archivo-latin-900-normal.woff2);font-weight:900}}@font-face{{font-family:Archivo;src:url(archivo-latin-800-normal.woff2);font-weight:800}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1080px;overflow:hidden;position:relative;color:#fff;font-family:Inter,sans-serif;background:#111}}.A{{font-family:Archivo;font-weight:900}}.abs{{position:absolute}}
</style></head><body>
<div class=abs style="left:0;top:0;width:1080px;height:560px;overflow:hidden">{fl(d['left'],'l')}{fl(d['right'],'r')}</div>
<div class=abs style="left:0;right:0;top:330px;height:240px;background:linear-gradient(transparent,#111)"></div>
<div class=abs style="left:56px;top:44px;background:rgba(0,0,0,.6);padding:10px 16px;border-radius:14px"><div style="display:flex;align-items:center;gap:12px">{l1}{l2}</div></div>
<div class="abs A" style="left:50%;top:205px;transform:translateX(-50%);width:150px;height:150px;border-radius:50%;background:#111;border:5px solid #F5C518;display:flex;align-items:center;justify-content:center;font-size:52px;color:#F5C518">VS</div>
<div class="abs A" style="left:64px;top:590px;background:#22C55E;color:#06210f;padding:8px 16px;border-radius:6px;font-size:22px;letter-spacing:3px">{d.get('tag','RESULT')}</div>
<div class="abs A" style="left:64px;right:64px;top:650px;font-size:{size}px;line-height:1.02">{hl}</div>
<div class=abs style="left:64px;right:64px;top:870px;font-size:28px;color:#ccc">{d.get('sub','')}</div>
<div class=abs style="left:64px;right:64px;bottom:40px;display:flex;justify-content:space-between;font-size:18px;color:#bbb"><span>Source: {d.get('source','ICC')}</span><span>{d.get('date','')} · {d.get('hashtag','#Cricket')}</span></div>
</body></html>"""
p=D+'/_tmp.html';open(p,'w').write(h)
subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=1.8963','--window-size=1080,1080','--screenshot='+D+'/_tmp.png','file://'+p],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
Image.open(D+'/_tmp.png').convert('RGB').save(out,quality=100,subsampling=0)
os.remove(p);os.remove(D+'/_tmp.png');print(out)
