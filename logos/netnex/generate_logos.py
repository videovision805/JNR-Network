import os, json, sys
sys.path.insert(0,'/tmp/nn')
from fontpath import text_path
OUT=os.environ.get('NNOUT',os.path.dirname(os.path.abspath(__file__)))
FONT=os.environ.get('NNFONT','sora')
FF=f'/tmp/nn/fonts/node_modules/@fontsource/{FONT}/files/{FONT}-latin-700-normal.woff'
PURPLE='#1B1035'; GREEN='#3DFF9A'; LAV='#F7F5FC'; WHITE='#FFFFFF'; BLACK='#000000'
TRACK={'sora':14,'outfit':20}[FONT]
CAP={'sora':0.730,'outfit':0.706}[FONT]
# ---- symbol: bold N, round caps, node holes (true transparency via mask)
SW_=26; WID=96
SYM_W=WID+SW_; SYM_H=100+SW_   # bbox 122 x 126
HOLES=[(0,0),(WID,0),(0,100),(WID,100),(WID/2,50)]
def symbol(color,holes=True,uid='h'):
    m=''
    if holes:
        m=(f'<mask id="{uid}" maskUnits="userSpaceOnUse" x="-30" y="-30" width="{WID+60}" height="160"><rect x="-30" y="-30" width="{WID+60}" height="160" fill="#fff"/><g fill="#000">'
           +''.join(f'<circle cx="{x:g}" cy="{y:g}" r="7.5"/>' for x,y in HOLES)+'</g></mask>')
    g=f'<g{" mask=\"url(#%s)\""%uid if holes else ""} fill="none" stroke="{color}" stroke-width="{SW_}" stroke-linecap="round" stroke-linejoin="round"><path d="M0 100V0M{WID} 0V100M0 0L{WID} 100"/></g>'
    return (f'<defs>{m}</defs>' if m else '')+g
def place_symbol(color,cx,cy,height,holes=True,uid='h'):
    k=height/SYM_H
    return f'<g transform="translate({cx-(WID/2)*k:g} {cy-50*k:g}) scale({k:g})">{symbol(color,holes,uid)}</g>'
def wordmark(text,color,cap_px,x,cy):
    size=cap_px/CAP
    d,w,c,xh=text_path(FF,text,TRACK,size)
    return f'<path d="{d}" fill="{color}" transform="translate({x:g} {cy+cap_px/2:g})"/>', w
def svg(w,h,body,bg=None,title='NetNex'):
    b=f'<rect width="{w:g}" height="{h:g}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}"><title>{title}</title>{b}{body}</svg>\n'
THEMES={'dark':(GREEN,WHITE,PURPLE),'light':(GREEN,PURPLE,LAV),'white':(WHITE,WHITE,None),'black':(BLACK,BLACK,None)}
C=150  # cap height px
def horizontal(text,theme):
    sc,tc,bg=THEMES[theme]; P=1.25*C; hs=1.75*C; ws_=hs*SYM_W/SYM_H
    gap=0.8*C
    _,tw=wordmark(text,tc,C,0,0)
    W=P+ws_+gap+tw+P; H=hs+2*P; cy=H/2
    s=place_symbol(sc,P+ws_/2,cy,hs)
    t,_=wordmark(text,tc,C,P+ws_+gap,cy)
    return svg(W,H,s+t,bg,text)
def stacked(text,theme):
    sc,tc,bg=THEMES[theme]; P=1.5*C; hs=3.0*C; ws_=hs*SYM_W/SYM_H; gap=0.95*C
    _,tw=wordmark(text,tc,C,0,0)
    W=max(tw,ws_)+2*P; H=hs+gap+C+2*P
    s=place_symbol(sc,W/2,P+hs/2,hs)
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
    files[f'netnex-symbol-{col and name}']=svg(S,S,place_symbol(col,S/2,S/2,330),None)
files['netnex-app-icon-purple']=svg(S,S,f'<rect width="{S}" height="{S}" rx="116" fill="{PURPLE}"/>'+place_symbol(GREEN,S/2,S/2,290),None)
files['netnex-app-icon-green']=svg(S,S,f'<rect width="{S}" height="{S}" rx="116" fill="{GREEN}"/>'+place_symbol(PURPLE,S/2,S/2,290),None)
files['netnex-favicon-simple']=svg(S,S,f'<rect width="{S}" height="{S}" rx="116" fill="{PURPLE}"/>'+place_symbol(GREEN,S/2,S/2,300,holes=False),None)
for k,v in files.items():
    os.makedirs(OUT+'/svg',exist_ok=True); open(f'{OUT}/svg/{k}.svg','w').write(v)
json.dump(list(files),open('/tmp/nn/names.json','w'))
print(len(files),FONT)
