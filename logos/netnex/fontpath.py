from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
def text_path(fontfile, text, track=0, size=1000):
    f=TTFont(fontfile); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    sc=size/upm; x=0; pen=SVGPathPen(gs, ntos=lambda v:f"{v:.1f}")
    adv=[]
    for i,ch in enumerate(text):
        gn=cmap[ord(ch)]
        tp=TransformPen(pen,(sc,0,0,-sc,x,0))
        gs[gn].draw(tp)
        x+=gs[gn].width*sc+track*size/1000
    cap=f['OS/2'].sCapHeight*sc; xh=f['OS/2'].sxHeight*sc
    return pen.getCommands(), x-track*size/1000, cap, xh
if __name__=='__main__':
    import sys
    for fn in ['sora','outfit']:
        ff=f'/tmp/nn/fonts/node_modules/@fontsource/{fn}/files/{fn}-latin-700-normal.woff'
        d,w,c,x=text_path(ff,'NetNex')
        print(fn,w,c,x,len(d))
