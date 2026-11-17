import os, json
OUT=os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT+'/svg',exist_ok=True)
PURPLE='#1B1035'; GREEN='#3DFF9A'; LAV='#F7F5FC'; WHITE='#FFFFFF'; BLACK='#000000'
SW=15; GAP=18
# glyph: (advance, path d, extra svg)
G={
'N':(52,'M0 64V0L52 64V0'),
'e':(52,'M0 39H52A26 26 0 1 0 44.4 57.4'),
't':(32,'M16 4V52Q16 64 29 64M2 24H32'),
'x':(52,'M0 14L52 64M52 14L0 64'),
'i':(5,'M0 14V64M0 -6V-6.01'),
'l':(5,'M0 0V64'),
'I':(5,'M0 0V64'),
'L':(38,'M0 0V64H38'),
'T':(52,'M0 0H52M26 0V64'),
'B':(46,'M0 0V64M0 0H22A15 15 0 0 1 22 30H0M0 30H28A17 17 0 0 1 28 64H0'),
'P':(44,'M0 0V64M0 0H26A18.5 18.5 0 0 1 26 37H0'),
'O':(64,'M32 0A32 32 0 1 1 32 64A32 32 0 1 1 32 0Z'),
'S':(44,'M40 14Q36 0 22 0Q4 0 4 16Q4 30 22 32Q42 35 42 49Q42 64 22 64Q9 64 3 51'),
}
def wordmark(text,color):
    x=0; ds=[]
    for ch in text:
        adv,d=G[ch]
        ds.append(f'<path d="{d}" transform="translate({x:g} 0)"/>')
        x+=adv+GAP
    w=x-GAP
    pad=SW/2+(8 if 'i' in text else 0)
    grp=f'<g transform="translate({SW/2} {pad})" fill="none" stroke="{color}" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round">'+''.join(ds)+'</g>'
    return grp, w+SW, 64+2*pad   # unscaled bbox
def symbol(color,full=True):
    mid=(f'<circle cx="50" cy="50" r="17" fill="{color}"/>' if full else '')
    return (f'<g transform="TRANSFORM"><g mask="url(#h)">'
            f'<path d="M0 100V0L100 100V0" fill="none" stroke="{color}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<g fill="{color}"><circle cx="0" cy="0" r="24"/><circle cx="0" cy="100" r="24"/><circle cx="100" cy="0" r="24"/><circle cx="100" cy="100" r="24"/>{mid}</g></g></g>')
MASK='<defs><mask id="h" maskUnits="userSpaceOnUse" x="-40" y="-40" width="180" height="180"><rect x="-40" y="-40" width="180" height="180" fill="#fff"/><g fill="#000"><circle cx="0" cy="0" r="9"/><circle cx="0" cy="100" r="9"/><circle cx="100" cy="0" r="9"/><circle cx="100" cy="100" r="9"/>MIDCUT</g></mask></defs>'
def svg(w,h,body,bg=None,title='NetNex',full=True):
    b=f'<rect width="{w:g}" height="{h:g}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}"><title>{title}</title>{MASK.replace('MIDCUT','<circle cx="50" cy="50" r="6"/>' if full else '')}{b}{body}</svg>\n'
THEMES={'dark':(GREEN,WHITE,PURPLE),'light':(GREEN,PURPLE,LAV),'white':(WHITE,WHITE,None),'black':(BLACK,BLACK,None)}
files={}
def horizontal(text,theme):
    sc,tc,bg=THEMES[theme]; P=170; ss=1.2; ws=1.9; gap=80
    wm,ww,wh=wordmark(text,tc)
    symw=(100+48)*ss; symh=symw
    H=max(symh,wh*ws)+2*P; cy=H/2
    sx=P+24*ss; tx=P+symw+gap
    W=tx+ww*ws+P
    s=symbol(sc).replace('TRANSFORM',f'translate({sx:g} {cy-50*ss:g}) scale({ss})')
    body=s+f'<g transform="translate({tx:g} {cy-wh*ws/2:g}) scale({ws})">{wm}</g>'
    return svg(W,H,body,bg,text)
def stacked(text,theme):
    sc,tc,bg=THEMES[theme]; P=230; ss=1.7; ws=2.1; gap=100
    wm,ww,wh=wordmark(text,tc)
    symw=(100+48)*ss
    W=max(ww*ws,symw)+2*P; H=symw+gap+wh*ws+2*P
    sx=W/2-50*ss; sy=P+24*ss
    s=symbol(sc).replace('TRANSFORM',f'translate({sx:g} {sy:g}) scale({ss})')
    body=s+f'<g transform="translate({W/2-ww*ws/2:g} {P+symw+gap:g}) scale({ws})">{wm}</g>'
    return svg(W,H,body,bg,text)
for th in THEMES:
    files[f'netnex-horizontal-{th}']=horizontal('NetNex',th)
    files[f'netnex-stacked-{th}']=stacked('NetNex',th)
for p in ['BillNex','OLTNex','ISPNex']:
    files[f'{p.lower()}-horizontal-dark']=horizontal(p,'dark')
    files[f'{p.lower()}-horizontal-light']=horizontal(p,'light')
# symbol only
S=512; ss=2.4
sx=S/2-50*ss; sy=S/2-50*ss
for name,col,bg in [('netnex-symbol-green',GREEN,None),('netnex-symbol-white',WHITE,None),('netnex-symbol-black',BLACK,None),('netnex-symbol-purple',PURPLE,None)]:
    files[name]=svg(S,S,symbol(col).replace('TRANSFORM',f'translate({sx:g} {sy:g}) scale({ss})'),bg)
# app icon: rounded purple square
ss=2.0
files['netnex-app-icon']=svg(S,S,f'<rect width="{S}" height="{S}" rx="112" fill="{PURPLE}"/>'+symbol(GREEN).replace('TRANSFORM',f'translate({S/2-50*ss:g} {S/2-50*ss:g}) scale({ss})'))
files['netnex-favicon-simple']=svg(S,S,f'<rect width="{S}" height="{S}" rx="112" fill="{PURPLE}"/>'+symbol(GREEN,False).replace('TRANSFORM',f'translate({S/2-50*2.0:g} {S/2-50*2.0:g}) scale(2.0)'),None,'NetNex',False)
# SVGs with bg need hole color: mask gives transparency, so bg shows through (correct)
for k,v in files.items(): open(f'{OUT}/svg/{k}.svg','w').write(v)
json.dump(list(files),open('/tmp/nn/names.json','w'))
print(len(files))
