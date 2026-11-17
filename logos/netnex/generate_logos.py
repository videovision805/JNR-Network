import os, json, sys
sys.path.insert(0,'/tmp/nn')
from fontpath import text_path
OUT=os.environ.get('NNOUT',os.path.dirname(os.path.abspath(__file__)))
FONT=os.environ.get('NNFONT','poppins')
WT=os.environ.get('NNWT','600')
FF=f'/tmp/nn/fonts/node_modules/@fontsource/{FONT}/files/{FONT}-latin-{WT}-normal.woff'
PURPLE='#1B1035'; GREEN='#3DFF9A'; LAV='#F7F5FC'; WHITE='#FFFFFF'; BLACK='#000000'
TRACK=int(os.environ.get('NNTRACK','10'))
from fontTools.ttLib import TTFont as _T
_f=_T(FF); CAP=_f['OS/2'].sCapHeight/_f['head'].unitsPerEm
# ---- symbol: round badge, N drawn as a line with 4 nodes (cut out = true transparency)
SYM_W=SYM_H=176
NPATH='M70 138V62L130 138V62'
NODES=[(70,138),(70,62),(130,138),(130,62)]
def symbol(color,holes=True,uid='h',ncolor=None):
    if ncolor:  # two-tone: solid badge + coloured N on top (light version)
        return (f'<circle cx="100" cy="100" r="88" fill="{color}"/>'
                f'<path d="{NPATH}" fill="none" stroke="{ncolor}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
                +''.join(f'<circle cx="{x}" cy="{y}" r="14" fill="{ncolor}"/>' for x,y in NODES))
    if holes:
        cut=(f'<path d="{NPATH}" fill="none" stroke="#000" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
             +''.join(f'<circle cx="{x}" cy="{y}" r="14" fill="#000"/>' for x,y in NODES))
    else:  # simplified for 16-32 px: bold N, no nodes
        cut=f'<path d="{NPATH}" fill="none" stroke="#000" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>'
    return (f'<defs><mask id="{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="200" height="200"><rect width="200" height="200" fill="#fff"/>{cut}</mask></defs>'
            f'<circle cx="100" cy="100" r="88" fill="{color}" mask="url(#{uid})"/>')
def place_symbol(color,cx,cy,height,holes=True,uid='h',ncolor=None):
    k=height/SYM_H
    return f'<g transform="translate({cx-100*k:g} {cy-100*k:g}) scale({k:g})">{symbol(color,holes,uid,ncolor)}</g>'
def wordmark(text,color,cap_px,x,cy):
    size=cap_px/CAP
    d,w,c,xh=text_path(FF,text,TRACK,size)
    return f'<path d="{d}" fill="{color}" transform="translate({x:g} {cy+cap_px/2:g})"/>', w
def svg(w,h,body,bg=None,title='NetNex'):
    b=f'<rect width="{w:g}" height="{h:g}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}"><title>{title}</title>{b}{body}</svg>\n'
THEMES={'dark':(GREEN,WHITE,PURPLE),'light':(PURPLE,PURPLE,LAV),'white':(WHITE,WHITE,None),'black':(BLACK,BLACK,None)}
NCOL={'light':GREEN}
C=150  # cap height px
def horizontal(text,theme):
    sc,tc,bg=THEMES[theme]; P=1.25*C; hs=1.8*C; ws_=hs*SYM_W/SYM_H
    gap=0.8*C
    _,tw=wordmark(text,tc,C,0,0)
    W=P+ws_+gap+tw+P; H=hs+2*P; cy=H/2
    s=place_symbol(sc,P+ws_/2,cy,hs,ncolor=NCOL.get(theme))
    t,_=wordmark(text,tc,C,P+ws_+gap,cy)
    return svg(W,H,s+t,bg,text)
def stacked(text,theme):
    sc,tc,bg=THEMES[theme]; P=1.5*C; hs=2.6*C; ws_=hs*SYM_W/SYM_H; gap=0.95*C
    _,tw=wordmark(text,tc,C,0,0)
    W=max(tw,ws_)+2*P; H=hs+gap+C+2*P
    s=place_symbol(sc,W/2,P+hs/2,hs,ncolor=NCOL.get(theme))
    t,_=wordmark(text,tc,C,W/2-tw/2,P+hs+gap+C/2)
    return svg(W,H,s+t,bg,text)
files={}
for th in THEMES:
    files[f'netnex-horizontal-{th}']=horizontal('NetNex',th)
    files[f'netnex-stacked-{th}']=stacked('NetNex',th)
for p in ['BillNex','OLTNex','ISPNex']:
    files[f'{p.lower()}-horizontal-dark']=horizontal(p,'dark')
    files[f'{p.lower()}-horizontal-light']=horizontal(p,'light')
S=512
for name,col in [('green',GREEN),('white',WHITE),('black',BLACK),('purple',PURPLE)]:
    files[f'netnex-symbol-{col and name}']=svg(S,S,place_symbol(col,S/2,S/2,380),None)
files['netnex-app-icon-purple']=svg(S,S,f'<rect width="{S}" height="{S}" rx="116" fill="{PURPLE}"/>'+place_symbol(GREEN,S/2,S/2,330),None)
files['netnex-app-icon-green']=svg(S,S,f'<rect width="{S}" height="{S}" rx="116" fill="{GREEN}"/>'+place_symbol(PURPLE,S/2,S/2,330),None)
files['netnex-favicon-simple']=svg(S,S,place_symbol(GREEN,S/2,S/2,500,holes=False),None)
for k,v in files.items():
    os.makedirs(OUT+'/svg',exist_ok=True); open(f'{OUT}/svg/{k}.svg','w').write(v)
json.dump(list(files),open('/tmp/nn/names.json','w'))
print(len(files),FONT)
