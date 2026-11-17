import os, sys, json, math
sys.path.insert(0,'/tmp/nn')
from fontpath import text_path
OUT='/home/user/JNR-Network/logos/netnex/concepts'
FF='/tmp/nn/fonts/node_modules/@fontsource/poppins/files/poppins-latin-600-normal.woff'
from fontTools.ttLib import TTFont
CAP=TTFont(FF)['OS/2'].sCapHeight/TTFont(FF)['head'].unitsPerEm
PURPLE='#1B1035'; GREEN='#3DFF9A'; WHITE='#FFFFFF'
def hexpts(cx,cy,R):
    return [(cx+R*math.cos(math.radians(a)),cy+R*math.sin(math.radians(a))) for a in range(-90,270,60)]
def concepts():
    c={}
    # 1 CLOUD N
    shape='<g fill="G"><circle cx="112" cy="90" r="46"/><circle cx="66" cy="108" r="30"/><circle cx="154" cy="116" r="26"/><rect x="36" y="100" width="144" height="46" rx="23"/></g>'
    cut='<path d="M90 128V80L128 128V80" fill="none" stroke="#000" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/><circle cx="90" cy="128" r="11" fill="#000"/><circle cx="128" cy="80" r="11" fill="#000"/>'
    c['cloud']=(shape,cut,(36,44,144,102))
    # 2 BADGE with live dot
    shape='<g fill="G"><circle cx="100" cy="100" r="88"/><circle cx="170" cy="36" r="15"/></g>'
    cut='<circle cx="170" cy="36" r="27" fill="#000"/><path d="M70 138V62L130 138V62" fill="none" stroke="#000" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>'
    # dot must stay: draw dot after mask instead
    c['badge']=('<g fill="G"><circle cx="100" cy="100" r="88"/></g>',
      '<circle cx="170" cy="36" r="28" fill="#000"/><path d="M70 138V62L130 138V62" fill="none" stroke="#000" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>',
      (12,12,178,178),'<circle cx="170" cy="36" r="15" fill="G"/>')
    return c
CON=concepts()
def sym(name,color,cx,cy,height,uid):
    t=CON[name]; shape,cut,(x0,y0,w,h)=t[0],t[1],t[2]; extra=t[3] if len(t)>3 else ''
    k=height/h
    m=f'<mask id="{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="200" height="200"><rect width="200" height="200" fill="#fff"/>{cut}</mask>'
    body=f'<g mask="url(#{uid})">{shape.replace("G",color)}</g>{extra.replace("G",color)}'
    return f'<defs>{m}</defs><g transform="translate({cx-(x0+w/2)*k:g} {cy-(y0+h/2)*k:g}) scale({k:g})">{body}</g>', w/h
def wm(text,color,cap,x,cy):
    size=cap/CAP; d,w,c,xh=text_path(FF,text,10,size)
    return f'<path d="{d}" fill="{color}" transform="translate({x:g} {cy+cap/2:g})"/>', w
def svg(w,h,body,bg=None):
    b=f'<rect width="{w:g}" height="{h:g}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}"><title>NetNex</title>{b}{body}</svg>\n'
files={}
C=150
for n in CON:
    s,r=sym(n,GREEN,256,256,330,'m'); files[f'concept-{n}-symbol']=svg(512,512,s)
    s,r=sym(n,GREEN,256,256,290,'m'); files[f'concept-{n}-app-icon']=svg(512,512,f'<rect width="512" height="512" rx="116" fill="{PURPLE}"/>'+s)
    P=1.25*C; hs=1.8*C; ws=hs*r; gap=.8*C
    _,tw=wm('NetNex',WHITE,C,0,0)
    W=P+ws+gap+tw+P; H=hs+2*P
    s,_=sym(n,GREEN,P+ws/2,H/2,hs,'m'); t,_=wm('NetNex',WHITE,C,P+ws+gap,H/2)
    files[f'concept-{n}-horizontal-dark']=svg(W,H,s+t,PURPLE)
for k,v in files.items(): open(f'{OUT}/{k}.svg','w').write(v)
json.dump(list(files),open('/tmp/nn/names3.json','w')); print(len(files))
