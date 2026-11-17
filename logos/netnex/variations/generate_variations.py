import os, sys, json, math
sys.path.insert(0,'/tmp/nn')
from fontpath import text_path
OUT='/home/user/JNR-Network/logos/netnex/variations'
FF='/tmp/nn/fonts/node_modules/@fontsource/poppins/files/poppins-latin-600-normal.woff'
from fontTools.ttLib import TTFont
CAP=TTFont(FF)['OS/2'].sCapHeight/TTFont(FF)['head'].unitsPerEm
PURPLE='#1B1035'; GREEN='#3DFF9A'; WHITE='#FFFFFF'
def concepts():
    c={}
    CL=lambda d: (f'<circle cx="112" cy="90" r="{46-d}"/><circle cx="66" cy="108" r="{30-d}"/><circle cx="154" cy="116" r="{26-d}"/><rect x="{36+d}" y="{100+d}" width="{144-2*d}" height="{46-2*d}" rx="{23-d}"/>')
    Ncut=lambda col,sw=13,r=11: f'<path d="M90 128V80L128 128V80" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/><circle cx="90" cy="128" r="{r}" fill="{col}"/><circle cx="128" cy="80" r="{r}" fill="{col}"/>'
    # cloud + live dot
    c['cloud-dot']=(f'<g fill="G">{CL(0)}</g>',Ncut('#000'),(36,44,152,102),'<circle cx="176" cy="68" r="13" fill="G"/>')
    # cloud outline, solid N
    c['cloud-outline']=(f'<g fill="G">{CL(0)}</g>',f'<g fill="#000">{CL(13)}</g>',(36,44,144,102),Ncut('G',13,11))
    # cloud, nodes-only N (thin line, 4 node holes)
    c['cloud-nodes']=(f'<g fill="G">{CL(0)}</g>','<path d="M90 128V80L128 128V80" fill="none" stroke="#000" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><g fill="#000"><circle cx="90" cy="128" r="11"/><circle cx="90" cy="80" r="11"/><circle cx="128" cy="128" r="11"/><circle cx="128" cy="80" r="11"/></g>',(36,44,144,102))
    # badge ring
    c['badge-ring']=('<circle cx="100" cy="100" r="88" fill="G"/>','<circle cx="100" cy="100" r="72" fill="#000"/>',(12,12,176,176),'<path d="M72 134V66L128 134V66" fill="none" stroke="G" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>')
    # badge squircle + dot
    c['badge-squircle']=('<rect x="14" y="14" width="172" height="172" rx="56" fill="G"/>','<circle cx="172" cy="34" r="28" fill="#000"/><path d="M70 138V62L130 138V62" fill="none" stroke="#000" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>',(14,10,180,176),'<circle cx="172" cy="34" r="15" fill="G"/>')
    # badge nodes
    c['badge-nodes']=('<circle cx="100" cy="100" r="88" fill="G"/>','<path d="M70 138V62L130 138V62" fill="none" stroke="#000" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><g fill="#000"><circle cx="70" cy="138" r="13"/><circle cx="70" cy="62" r="13"/><circle cx="130" cy="138" r="13"/><circle cx="130" cy="62" r="13"/></g>',(12,12,176,176))
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
json.dump(list(files),open('/tmp/nn/names4.json','w')); print(len(files))
