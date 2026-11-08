"""LankaXpress news card generator: 6 formats (A scene, B number, C newspaper, D lanka, E alert, G minimal), changing colours.
Usage: python3 news_gen.py story.json out.jpg   (run in a folder with header.html + archivo woff2 files)
story.json: {"tag":"ECONOMY","headline":"ADB backs Sri Lanka's water reforms with $100 million","hl":"$100 million",
 "number":"$100M","numlabel":"ADB SUPPORT","summary":"one short line (format C)","topic":"water","source":"Daily FT, Newswire",
 "date":"07 NOV 2026","format":"auto|A|B|C|D|E|G","state":"path/to/news_state.json"}
"""
import json,sys,os,random,re,subprocess
from PIL import Image
W=os.path.dirname(os.path.abspath(__file__))
ICONS={
'water':'<path d="M50 6 C50 6 16 48 16 66 a34 30 0 0 0 68 0 C84 48 50 6 50 6Z" fill="{c1}"/><path d="M32 66 a18 16 0 0 0 18 18" stroke="{c2}" stroke-width="6" fill="none" stroke-linecap="round"/>',
'parliament':'<rect x="10" y="78" width="80" height="10" fill="{c1}"/><rect x="18" y="44" width="64" height="8" fill="{c1}"/><g fill="{c1}"><rect x="22" y="54" width="7" height="22"/><rect x="36" y="54" width="7" height="22"/><rect x="50" y="54" width="7" height="22"/><rect x="64" y="54" width="7" height="22"/></g><path d="M14 44 L50 16 L86 44Z" fill="{c2}"/>',
'port':'<path d="M10 62 h80 l-12 22 h-56Z" fill="{c1}"/><rect x="26" y="40" width="16" height="20" fill="{c2}"/><rect x="44" y="34" width="16" height="26" fill="{c1}" opacity=".8"/><rect x="62" y="44" width="14" height="16" fill="{c2}"/><path d="M8 92 q10-6 20 0 t20 0 t20 0 t20 0" stroke="{c2}" stroke-width="4" fill="none"/>',
'tea':'<path d="M50 90 C20 70 18 36 50 10 C82 36 80 70 50 90Z" fill="{c1}"/><path d="M50 88 V24" stroke="{c2}" stroke-width="5"/><path d="M50 50 L34 38 M50 66 L66 52" stroke="{c2}" stroke-width="4"/>',
'construction':'<rect x="44" y="14" width="8" height="74" fill="{c1}"/><rect x="18" y="14" width="70" height="8" fill="{c1}"/><path d="M80 22 v18" stroke="{c2}" stroke-width="3"/><rect x="72" y="40" width="16" height="12" fill="{c2}"/><rect x="30" y="84" width="40" height="6" fill="{c2}"/>',
'road':'<path d="M40 8 L14 92 H86 L60 8Z" fill="{c1}"/><g fill="{c2}"><rect x="47" y="20" width="6" height="12"/><rect x="47" y="44" width="6" height="14"/><rect x="47" y="70" width="6" height="16"/></g>',
'power':'<path d="M56 6 L22 56 H46 L40 94 L78 40 H54Z" fill="{c1}"/>',
'money':'<circle cx="50" cy="50" r="40" fill="{c1}"/><circle cx="50" cy="50" r="30" fill="none" stroke="{c2}" stroke-width="4"/><text x="50" y="62" text-anchor="middle" font-family="Archivo" font-weight="900" font-size="34" fill="{c2}">Rs</text>',
'dollar':'<circle cx="50" cy="50" r="40" fill="{c1}"/><circle cx="50" cy="50" r="30" fill="none" stroke="{c2}" stroke-width="4"/><text x="50" y="64" text-anchor="middle" font-family="Archivo" font-weight="900" font-size="40" fill="{c2}">$</text>',
'chart':'<g fill="{c1}"><rect x="14" y="60" width="14" height="28"/><rect x="34" y="46" width="14" height="42"/><rect x="54" y="34" width="14" height="54"/><rect x="74" y="18" width="14" height="70"/></g><path d="M12 50 L40 32 L60 38 L90 10" stroke="{c2}" stroke-width="5" fill="none"/>',
'plane':'<path d="M50 6 c5 0 7 6 7 12 v22 l32 18 v9 l-32-9 v18 l10 8 v7 l-17-5 -17 5 v-7 l10-8 v-18 l-32 9 v-9 l32-18 v-22 c0-6 2-12 7-12Z" fill="{c1}"/>',
'train':'<rect x="22" y="10" width="56" height="66" rx="12" fill="{c1}"/><rect x="30" y="20" width="40" height="22" rx="4" fill="{c2}"/><circle cx="36" cy="60" r="5" fill="{c2}"/><circle cx="64" cy="60" r="5" fill="{c2}"/><path d="M30 78 L20 92 M70 78 L80 92" stroke="{c1}" stroke-width="5"/>',
'cricket':'<rect x="44" y="8" width="14" height="60" rx="5" fill="{c1}" transform="rotate(30 50 50)"/><circle cx="30" cy="76" r="12" fill="{c2}"/>',
'weather':'<path d="M28 60 a16 16 0 0 1 4-31 a22 22 0 0 1 42 6 a14 14 0 0 1 0 28Z" fill="{c1}"/><g stroke="{c2}" stroke-width="5" stroke-linecap="round"><path d="M34 72 l-5 12"/><path d="M52 72 l-5 12"/><path d="M70 72 l-5 12"/></g>',
'health':'<rect x="38" y="12" width="24" height="76" rx="4" fill="{c1}"/><rect x="12" y="38" width="76" height="24" rx="4" fill="{c1}"/>',
'education':'<path d="M50 16 L94 36 L50 56 L6 36Z" fill="{c1}"/><path d="M24 46 v20 c14 12 38 12 52 0 v-20 L50 58Z" fill="{c2}"/>',
'farming':'<path d="M50 92 V40" stroke="{c1}" stroke-width="5"/><g fill="{c1}"><ellipse cx="38" cy="34" rx="8" ry="14" transform="rotate(-25 38 34)"/><ellipse cx="62" cy="34" rx="8" ry="14" transform="rotate(25 62 34)"/><ellipse cx="38" cy="58" rx="8" ry="14" transform="rotate(-25 38 58)"/><ellipse cx="62" cy="58" rx="8" ry="14" transform="rotate(25 62 58)"/><ellipse cx="50" cy="16" rx="7" ry="13"/></g>',
'tourism':'<circle cx="68" cy="28" r="14" fill="{c2}"/><path d="M50 92 C50 60 44 40 30 30" stroke="{c1}" stroke-width="5" fill="none"/><path d="M30 30 c-10-8 -24-6 -26 2 c10-2 18 0 26-2 c-4-10 -16-16 -24-12 c10 2 18 6 24 12 c2-12 12-18 22-16 c-8 4 -16 10 -22 16Z" fill="{c1}"/>',
'globe':'<circle cx="50" cy="50" r="40" fill="{c1}"/><path d="M10 50 h80 M50 10 c-20 22 -20 58 0 80 c20-22 20-58 0-80" stroke="{c2}" stroke-width="4" fill="none"/>',
}
ICONS['default']=ICONS['chart']
# palettes: (bg_dark, bg_mid, accent, icon_light)
PAL={
'A':[('#081B26','#0E6E8C','#F5C518','#5FC3D6'),('#1A0F2E','#6B3FA0','#FFB547','#C9A7F5'),('#0F1F14','#2E7D4F','#F5C518','#8EE3B0'),('#2A0E12','#B23A48','#FFD166','#F7A8B0'),('#0B1A33','#2F5DA8','#FF8A3D','#9CC3FF'),('#1C1206','#B86B16','#FFE08A','#F3C27A')],
'B':[('#06222C','#13788F','#F5C518','#7FE0F5'),('#1B0B2E','#5B2A86','#FFD23F','#C9A7F5'),('#0D1F12','#1E7A46','#F5C518','#8EE3B0'),('#2B0A0A','#A8321E','#FFD166','#FFB199'),('#0A1530','#1F4FBF','#7CF5C8','#9CC3FF'),('#111111','#3A3A3A','#F5C518','#DDDDDD')],
'C':[('#F3EDE0','#0E4F66','#F5C518','#7FE0F5'),('#F4EFE6','#7A1F2B','#F2C14E','#F7C9CF'),('#EEF1EA','#24553A','#F5C518','#A8E0BF'),('#F2EEF7','#3D2A7A','#FFC94A','#CFC2F7'),('#F6F0E8','#8A4B12','#F5C518','#F3C995')],
'D':[('#8D153A','#F7B718','#00534E','#EB7400'),('#00534E','#F7B718','#8D153A','#EB7400'),('#5A0E26','#F7B718','#00534E','#EB7400')],
'E':[('#1B1446','#2BB3D1','#E85A86','#7FE0F5'),('#0B1E1A','#22C55E','#F5C518','#86EFAC'),('#24081E','#E85A86','#F5C518','#FBA4C4'),('#0A1328','#3B82F6','#F97316','#93C5FD'),('#1A1205','#F59E0B','#EF4444','#FCD34D')],
'G':[('#F6F4EF','#1593C2','#121212','#1593C2'),('#F7F3EE','#C2410C','#121212','#C2410C'),('#F2F5F2','#15803D','#121212','#15803D'),('#F5F3F8','#6D28D9','#121212','#6D28D9'),('#F7F4EE','#B45309','#121212','#B45309'),('#F3F6F8','#0F766E','#121212','#0F766E')],
}
FONT='<style>@font-face{font-family:Archivo;src:url(archivo-latin-800-normal.woff2);font-weight:800}@font-face{font-family:Archivo;src:url(archivo-latin-900-normal.woff2);font-weight:900}body{margin:0}</style>'
def icon(topic,c1,c2,size,extra=''):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" {extra}>'+ICONS.get(topic,ICONS['default']).format(c1=c1,c2=c2)+'</svg>'
def hlh(h,hl,col):
    return h.replace(hl,f'<span style="color:{col}">{hl}</span>') if hl and hl in h else h
def hsize(h,base):  # shrink long headlines
    n=len(h); return base if n<=48 else int(base*48/n**0.97*1.0+base*0.15) if n<90 else int(base*0.62)
def foot(src,col,b='#fff',right='Full story in caption'):
    return f'<div style="position:absolute;left:64px;right:64px;bottom:48px;border-top:1px solid {col}40;padding-top:18px;display:flex;justify-content:space-between;font-size:21px;color:{col}"><span>Source: <b style="color:{b}">{src}</b></span><span>{right}</span></div>'
def build(s,fmt,p,H,Hd):
    tag,h,hl,src,date,topic=s['tag'],s['headline'],s.get('hl',''),s['source'],s['date'],s.get('topic','default')
    H=re.sub(r'\d\d [A-Z]{3} \d{4}',date,H); Hd=re.sub(r'\d\d [A-Z]{3} \d{4}',date,Hd)
    d,m,a,l=p
    if fmt=='A':
        fs=hsize(h,80)
        return f'''<div style="width:1080px;height:1080px;position:relative;overflow:hidden;font-family:Inter,sans-serif;background:{d}">
<svg width="1080" height="700" viewBox="0 0 1080 700" style="position:absolute;left:0;top:0"><defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{d}"/><stop offset=".6" stop-color="{m}"/><stop offset="1" stop-color="{l}"/></linearGradient><radialGradient id="gl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{a}" stop-opacity=".55"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient></defs>
<rect width="1080" height="700" fill="url(#sk)"/><circle cx="820" cy="260" r="240" fill="url(#gl)"/><circle cx="820" cy="260" r="70" fill="{a}" opacity=".85"/>
<path d="M0 430 Q180 320 360 390 T720 370 T1080 340 L1080 700 L0 700Z" fill="{d}" opacity=".55"/><path d="M0 480 Q240 390 480 460 T1080 430 L1080 700 L0 700Z" fill="{d}" opacity=".8"/></svg>
<div style="position:absolute;left:120px;top:150px;filter:drop-shadow(0 20px 30px #0006)">{icon(topic,'#FFFFFF',a,360)}</div>
<div style="position:absolute;left:0;top:0;width:1080px;height:200px;background:linear-gradient({d}cc,{d}00)"></div>
<div style="position:absolute;left:0;top:380px;width:1080px;height:700px;background:linear-gradient({d}00 0%,{d} 45%)"></div>
<div style="position:absolute;left:56px;right:56px;top:48px">{H}</div>
<div style="position:absolute;left:64px;right:64px;bottom:130px;color:#fff"><span style="display:inline-block;background:{a};color:#111;font-weight:800;letter-spacing:.16em;font-size:22px;padding:10px 20px;border-radius:8px">{tag}</span>
<div style="font-family:Archivo;font-weight:900;font-size:{fs}px;line-height:.98;margin-top:22px;text-transform:uppercase">{hlh(h,hl,a)}</div></div>{foot(src,'#C9D6DE')}</div>'''
    if fmt=='B':
        num=s.get('number') or ''
        fs=hsize(h,64) if num else hsize(h,96)
        big=f'<div style="font-family:Archivo;font-weight:900;font-size:{220 if len(num)<=6 else int(1320/len(num))}px;line-height:.9;color:{a};margin-top:30px;letter-spacing:-.02em">{num}</div>' if num else ''
        hh=h if num else hlh(h,hl,a)
        return f'''<div style="width:1080px;height:1080px;position:relative;overflow:hidden;font-family:Inter,sans-serif;background:radial-gradient(circle at 80% 20%,{m} 0%,{d} 70%);color:#fff;box-sizing:border-box;padding:48px 56px">
<div style="position:absolute;right:-90px;bottom:60px;opacity:.16">{icon(topic,l,l,620)}</div>{H}
<div style="margin-top:{160 if num else 220}px"><span style="display:inline-block;background:{a};color:#111;font-weight:800;letter-spacing:.16em;font-size:22px;padding:10px 20px;border-radius:8px">{tag}</span></div>{big}
<div style="font-family:Archivo;font-weight:900;font-size:{fs}px;line-height:1.02;margin-top:22px;text-transform:uppercase;max-width:900px">{hh}</div>{foot(src,'#C9D6DE')}</div>'''
    if fmt=='C':
        fs=hsize(h,96)
        hh=h.replace(hl,f'<span style="background:{a};padding:0 10px">{hl}</span>') if hl and hl in h else h
        return f'''<div style="width:1080px;height:1080px;box-sizing:border-box;padding:44px 56px;background:{d};color:#141414;font-family:Inter,sans-serif;position:relative">
<div style="border-bottom:6px double #141414;padding-bottom:14px">{Hd}</div>
<div style="display:flex;justify-content:space-between;font-size:18px;letter-spacing:.2em;font-weight:700;padding:10px 0;border-bottom:2px solid #141414"><span>{tag}</span><span>COLOMBO EDITION</span><span>SRI LANKA NEWS</span></div>
<div style="font-family:'Liberation Serif',serif;font-weight:700;font-size:{fs}px;line-height:.98;margin-top:30px">{hh}</div>
<div style="position:absolute;left:56px;right:56px;bottom:110px;display:flex;gap:36px;height:300px">
<div style="flex:1.2;border-top:2px solid #141414;padding-top:16px;font-family:'Liberation Serif',serif;font-size:32px;line-height:1.35;color:#333">{s.get('summary','')}<div style="font-family:Inter;font-size:20px;font-weight:700;margin-top:18px;color:#141414">Full story in caption →</div></div>
<div style="flex:1;background:{m};border-radius:6px;display:flex;align-items:center;justify-content:center">{icon(topic,l,'#FFFFFF',220)}</div></div>
<div style="position:absolute;left:56px;right:56px;bottom:40px;border-top:2px solid #141414;padding-top:14px;display:flex;justify-content:space-between;font-size:20px"><span>Source: <b>{src}</b></span><span style="font-weight:700">{date}</span></div></div>'''
    if fmt=='D':
        bottom,top,s1,s2=d,m,a,l
        num=s.get('number')
        fs=hsize(h,92)
        right=f'<div style="position:absolute;right:56px;top:190px;text-align:right;color:{bottom}"><div style="font-family:Archivo;font-weight:900;font-size:{108 if len(num)<=6 else int(650/len(num))}px;line-height:.9">{num}</div><div style="font-weight:800;font-size:24px;letter-spacing:.14em">{s.get("numlabel","")}</div></div>' if num else ''
        cx=290 if num else 400
        return f'''<div style="width:1080px;height:1080px;position:relative;overflow:hidden;font-family:Inter,sans-serif;background:{bottom};color:#fff">
<div style="position:absolute;left:0;top:0;width:1080px;height:470px;background:{top}"></div>
<div style="position:absolute;left:0;top:0;width:150px;height:470px;background:{s1}"></div><div style="position:absolute;left:150px;top:0;width:110px;height:470px;background:{s2}"></div>
<div style="position:absolute;left:{cx}px;top:160px;width:270px;height:270px;border-radius:50%;background:#fff;box-shadow:0 18px 40px #0004;display:flex;align-items:center;justify-content:center">{icon(topic,bottom,top,170)}</div>{right}
<div style="position:absolute;left:300px;right:56px;top:44px"><div style="background:{bottom};border-radius:14px;padding:12px 18px">{H}</div></div>
<div style="position:absolute;left:64px;right:64px;top:530px"><span style="display:inline-block;background:{top};color:{bottom};font-weight:800;letter-spacing:.16em;font-size:22px;padding:10px 20px;border-radius:8px">{tag}</span>
<div style="font-family:Archivo;font-weight:900;font-size:{fs}px;line-height:.98;margin-top:26px;text-transform:uppercase">{hlh(h,hl,top)}</div></div>{foot(src,'#F3E3E8')}</div>'''
    if fmt=='E':
        fs=hsize(h,76)
        return f'''<div style="width:1080px;height:1080px;position:relative;overflow:hidden;font-family:Inter,sans-serif;background:linear-gradient(150deg,{d},#0B0B1E 60%,#03131F);color:#fff;box-sizing:border-box;padding:48px 56px">
<div style="position:absolute;width:600px;height:600px;border-radius:50%;background:{m};filter:blur(140px);opacity:.45;right:-150px;top:-120px"></div>
<div style="position:absolute;width:500px;height:500px;border-radius:50%;background:{a};filter:blur(150px);opacity:.35;left:-160px;bottom:-140px"></div>
<div style="position:relative">{H}</div>
<div style="position:relative;margin-top:120px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:40px;padding:40px 44px;box-shadow:0 30px 60px #0006">
<div style="display:flex;align-items:center;gap:18px"><div style="width:64px;height:64px;border-radius:16px;background:{m};display:flex;align-items:center;justify-content:center">{icon(topic,'#FFFFFF','#FFFFFF',40)}</div>
<div style="flex:1"><div style="font-weight:800;font-size:24px">LankaXpress · {tag.title()}</div><div style="font-size:20px;color:#B8C2D9">now</div></div><span style="background:{a};color:#111;font-weight:800;font-size:18px;letter-spacing:.14em;padding:8px 14px;border-radius:999px">NEW</span></div>
<div style="font-family:Archivo;font-weight:900;font-size:{fs}px;line-height:1;margin-top:30px">{hlh(h,hl,l)}</div>
<div style="font-size:26px;color:#C9D2E6;margin-top:22px">Tap the caption for the full story.</div></div>
<div style="position:absolute;left:56px;right:56px;bottom:44px;display:flex;justify-content:space-between;font-size:21px;color:#B8C2D9"><span>Source: <b style="color:#fff">{src}</b></span><span>#LankaXpress</span></div></div>'''
    if fmt=='G':
        num=s.get('number'); logo=H[H.find('<svg'):H.find('</svg>')+6].replace('width="60" height="60"','width="44" height="44"')
        top=f'<div style="position:absolute;left:80px;top:300px;width:6px;height:120px;background:{m}"></div><div style="position:absolute;left:110px;top:290px;font-family:Archivo;font-weight:900;font-size:{200 if len(num)<=6 else int(1150/len(num))}px;line-height:1;letter-spacing:-.04em;color:{m}">{num}</div>' if num else ''
        fs=hsize(h,58) if num else hsize(h,96)
        return f'''<div style="width:1080px;height:1080px;position:relative;overflow:hidden;font-family:Inter,sans-serif;background:{d};color:#121212;box-sizing:border-box;padding:72px 80px">
<div style="display:flex;justify-content:space-between;align-items:center"><div style="display:flex;align-items:center;gap:14px">{logo}<span style="font-weight:700;font-size:22px">LankaXpress</span></div><span style="font-size:18px;letter-spacing:.2em;color:#777">{tag} · {date}</span></div>
{top}<div style="position:absolute;left:80px;right:80px;top:{540 if num else 400}px;font-size:{fs}px;font-weight:600;line-height:1.12;letter-spacing:-.02em">{h if num else hlh(h,hl,m)}</div>
<div style="position:absolute;{'right:80px;top:300px' if num else 'left:80px;top:200px'}">{icon(topic,m,d,120 if num else 150)}</div>
<div style="position:absolute;left:80px;right:80px;bottom:72px;display:flex;justify-content:space-between;font-size:18px;color:#777;border-top:1px solid #12121220;padding-top:22px"><span>Source: {src}</span><span>Full story in caption</span></div></div>'''
def choose(s,last):
    tag=s['tag'].upper(); cands=[]
    if 'BREAKING' in tag or 'WEATHER' in tag or 'ALERT' in tag: cands=['E','A','B']
    elif s.get('number'): cands=['B','D','G','A']
    elif 'POLITIC' in tag or 'POLICY' in tag or 'GOVERN' in tag: cands=['C','G','E']
    elif s.get('topic') in ('tourism','tea','port','road','construction','water','power','train','plane','farming'): cands=['A','D','C']
    else: cands=['G','C','A','D']
    if s.get('summary') is None and 'C' in cands: cands.remove('C')
    for f in cands:
        if f!=last.get('format'): return f
    return [f for f in 'ABDEG' if f!=last.get('format')][0]
def main():
    s=json.load(open(sys.argv[1])); out=sys.argv[2]
    st=s.get('state') or os.path.join(W,'news_state.json')
    try: last=json.load(open(st))
    except Exception: last={}
    fmt=s.get('format','auto'); fmt=choose(s,last) if fmt=='auto' else fmt
    pals=PAL[fmt]; ids=[i for i in range(len(pals)) if not (last.get('format')==fmt and last.get('pal')==i) and i!=last.get('pal_'+fmt)]
    pi=s.get('palette', random.choice(ids or list(range(len(pals))))); p=pals[pi]
    H=open(os.path.join(W,'header.html')).read()
    Hd=re.sub(r'color: ?#[0-9A-Fa-f]{3,6}','color:#141414',H.replace('fill="#FFFFFF"','fill="#111111"'))
    html=build(s,fmt,p,H,Hd).replace('–',' to ').replace('—',', ')
    tmp=os.path.join(W,'_n.html'); open(tmp,'w').write('<!doctype html><html><head><meta charset="utf-8">'+FONT+'</head><body>'+html+'</body></html>')
    subprocess.run(['google-chrome','--headless','--no-sandbox','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=1.8963','--window-size=1080,1080','--screenshot='+tmp[:-5]+'.png','file://'+tmp],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
    Image.open(tmp[:-5]+'.png').convert('RGB').save(out,quality=100,subsampling=0)
    last.update({'format':fmt,'pal':pi,'pal_'+fmt:pi}); json.dump(last,open(st,'w'))
    print(fmt,pi)
if __name__=='__main__': main()
