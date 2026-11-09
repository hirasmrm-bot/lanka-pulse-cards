import re,subprocess
from PIL import Image
H=re.sub(r'\d\d [A-Z]{3} \d{4}','09 NOV 2026',open('header.html').read())
G=[('CRL','Softlogic Finance','5.00','+25.00%'),('SHL','Softlogic Holdings','10.60','+24.71%'),('AMSL','Asiri Surgical','13.80','+21.05%'),('UBF','UB Finance','2.60','+18.18%'),('KHC','Kandy Hotels','13.50','+17.39%')]
L=[('INME','Insureme Insurance','1,754.00','−6.18%'),('ATLL','Amana Takaful Life','19.30','−4.46%'),('TANG','Tangerine Beach Hotels','95.60','−4.40%'),('ASHO','Lanka Ashok Leyland','2,772.50','−4.39%'),('CARS','Carson Cumberbatch','712.00','−4.24%')]
def col(title,rows,c,arrow):
    r=''.join(f'''<div style="display:flex;justify-content:space-between;align-items:center;padding:15px 0;border-top:1px solid #ffffff1a">
<div style="min-width:0"><div style="font-family:Archivo;font-weight:900;font-size:30px">{t}</div><div style="font-size:18px;color:#A9B3C7;white-space:nowrap">{n}</div></div>
<div style="text-align:right"><div style="font-family:Archivo;font-weight:900;font-size:30px;color:{c};white-space:nowrap">{arrow} {pc.lstrip('+−')}</div><div style="font-size:17px;color:#A9B3C7">Rs {p}</div></div></div>''' for t,n,p,pc in rows)
    return f'<div style="flex:1;background:rgba(255,255,255,.05);border:1px solid {c}55;border-radius:24px;padding:20px 26px 8px"><div style="font-weight:800;font-size:21px;letter-spacing:.16em;color:{c};padding-bottom:10px">{title}</div>{r}</div>'
html=f'''<!doctype html><html><head><meta charset="utf-8"><style>@font-face{{font-family:Archivo;src:url(archivo-latin-800-normal.woff2);font-weight:800}}@font-face{{font-family:Archivo;src:url(archivo-latin-900-normal.woff2);font-weight:900}}body{{margin:0}}</style></head><body>
<div style="width:1080px;height:1080px;box-sizing:border-box;padding:48px 56px;background:radial-gradient(circle at 85% 0%,#1d2a4a 0%,#0B0F1A 55%);color:#fff;font-family:Inter,sans-serif;position:relative">
{H}
<div style="margin-top:34px"><span style="display:inline-block;background:#F5C518;color:#111;font-weight:800;letter-spacing:.16em;font-size:21px;padding:9px 18px;border-radius:8px">CSE · MARKET MOVERS</span></div>
<div style="font-family:Archivo;font-weight:900;font-size:72px;line-height:.95;margin-top:18px">TODAY'S <span style="color:#22C55E">GAINERS</span> &amp; <span style="color:#EF4444">LOSERS</span></div>
<div style="font-size:24px;color:#C9D2E6;margin-top:12px">Top 5 by % change · Monday 9 November 2026</div>
<div style="display:flex;gap:22px;margin-top:28px">{col('TOP GAINERS',G,'#22C55E','▲')}{col('TOP LOSERS',L,'#EF4444','▼')}</div>
<div style="position:absolute;left:56px;right:56px;bottom:40px;border-top:1px solid #ffffff26;padding-top:16px;display:flex;justify-content:space-between;font-size:19px;color:#A9B3C7"><span>Source: <b style="color:#fff">Colombo Stock Exchange, via Capital Trust</b></span><span>Educational only · Not investment advice</span></div>
</div></body></html>'''
open('mv.html','w').write(html)
subprocess.run(['google-chrome','--headless','--no-sandbox','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=1.8963','--window-size=1080,1080','--screenshot=mv.png','file://'+__import__('os').path.abspath('mv.html')],stderr=subprocess.DEVNULL)
Image.open('mv.png').convert('RGB').save('/home/claude/lanka-pulse-cards/queue/2026-11-09-gainers-losers.jpg',quality=100,subsampling=0)
