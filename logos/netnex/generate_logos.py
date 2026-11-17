import os, json
OUT=os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT+'/svg',exist_ok=True)
PURPLE='#1B1035'; GREEN='#3DFF9A'; LAV='#F7F5FC'; WHITE='#FFFFFF'; BLACK='#000000'
SW=9; GAP=16
# glyph: (advance, path d, extra svg)
G={
'N':(40,'M0 60V0L40 60V0'),
'e':(44,'M0 38H44A22 22 0 1 0 38 53.6'),
't':(28,'M14 4V48Q14 60 26 60M2 20H28'),
'x':(44,'M0 16L44 60M44 16L0 60'),
'i':(0,'M0 16V60M0 2V2.01'),
'l':(0,'M0 0V60'),
'I':(0,'M0 0V60'),
'L':(34,'M0 0V60H34'),
'T':(44,'M0 0H44M22 0V60'),
'B':(40,'M0 0V60M0 0H20A14 14 0 0 1 20 28H0M0 28H24A16 16 0 0 1 24 60H0'),
'P':(38,'M0 0V60M0 0H22A16.5 16.5 0 0 1 22 33H0'),
'O':(60,'M30 0A30 30 0 1 1 30 60A30 30 0 1 1 30 0Z'),
'S':(42,'M37 13Q33 0 20 0Q4 0 4 15Q4 28 20 30Q38 33 38 46Q38 60 20 60Q8 60 3 47'),
}
def wordmark(text,color):
    x=0; ds=[]
    for ch in text:
        adv,d=G[ch]
        ds.append(f'<path d="{d}" transform="translate({x:g} 0)"/>')
        x+=adv+GAP
    w=x-GAP
    grp=f'<g transform="translate({SW/2} {SW/2})" fill="none" stroke="{color}" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round">'+''.join(ds)+'</g>'
    return grp, w+SW, 60+SW   # unscaled bbox
def symbol(color):
    # N from line + 4 nodes, node holes cut out with a mask (true transparency)
    return (f'<g transform="TRANSFORM"><g mask="url(#h)">'
            f'<path d="M0 100V0L100 100V0" fill="none" stroke="{color}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<g fill="{color}"><circle cx="0" cy="0" r="14"/><circle cx="0" cy="100" r="14"/><circle cx="100" cy="0" r="14"/><circle cx="100" cy="100" r="14"/></g></g></g>')
MASK='<defs><mask id="h" maskUnits="userSpaceOnUse" x="-30" y="-30" width="160" height="160"><rect x="-30" y="-30" width="160" height="160" fill="#fff"/><g fill="#000"><circle cx="0" cy="0" r="5"/><circle cx="0" cy="100" r="5"/><circle cx="100" cy="0" r="5"/><circle cx="100" cy="100" r="5"/></g></mask></defs>'
def svg(w,h,body,bg=None,title='NetNex'):
    b=f'<rect width="{w:g}" height="{h:g}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}"><title>{title}</title>{MASK}{b}{body}</svg>\n'
THEMES={'dark':(GREEN,WHITE,PURPLE),'light':(GREEN,PURPLE,LAV),'white':(WHITE,WHITE,None),'black':(BLACK,BLACK,None)}
files={}
def horizontal(text,theme):
    sc,tc,bg=THEMES[theme]; P=170; ss=1.2; ws=2.0; gap=70
    wm,ww,wh=wordmark(text,tc)
    symw=(100+28)*ss; symh=symw
    H=max(symh,wh*ws)+2*P; cy=H/2
    sx=P+14*ss; tx=P+symw+gap
    W=tx+ww*ws+P
    s=symbol(sc).replace('TRANSFORM',f'translate({sx:g} {cy-50*ss:g}) scale({ss})')
    body=s+f'<g transform="translate({tx:g} {cy-wh*ws/2:g}) scale({ws})">{wm}</g>'
    return svg(W,H,body,bg,text)
def stacked(text,theme):
    sc,tc,bg=THEMES[theme]; P=230; ss=1.5; ws=2.2; gap=90
    wm,ww,wh=wordmark(text,tc)
    symw=(100+28)*ss
    W=max(ww*ws,symw)+2*P; H=symw+gap+wh*ws+2*P
    sx=W/2-50*ss; sy=P+14*ss
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
S=512; ss=2.6
sx=S/2-50*ss; sy=S/2-50*ss
for name,col,bg in [('netnex-symbol-green',GREEN,None),('netnex-symbol-white',WHITE,None),('netnex-symbol-black',BLACK,None),('netnex-symbol-purple',PURPLE,None)]:
    files[name]=svg(S,S,symbol(col).replace('TRANSFORM',f'translate({sx:g} {sy:g}) scale({ss})'),bg)
# app icon: rounded purple square
ss=2.0
files['netnex-app-icon']=svg(S,S,f'<rect width="{S}" height="{S}" rx="112" fill="{PURPLE}"/>'+symbol(GREEN).replace('TRANSFORM',f'translate({S/2-50*ss:g} {S/2-50*ss:g}) scale({ss})'))
# SVGs with bg need hole color: mask gives transparency, so bg shows through (correct)
for k,v in files.items(): open(f'{OUT}/svg/{k}.svg','w').write(v)
json.dump(list(files),open('/tmp/nn/names.json','w'))
print(len(files))
