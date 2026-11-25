import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ficha import *
note=lambda t: f'<div style="font-size:33px;line-height:1.4;color:{G}">{t}</div>'
rows=lambda *x: '<div style="display:flex;flex-direction:column;gap:18px">'+"".join(x)+'</div>'
red=lambda t: f'<div style="border-top:4px solid {K};padding-top:20px;font-size:40px;font-weight:800;line-height:1.3;color:{R}">{t}</div>'
def tabla(H,D,cols,fs=34):
    th="".join(f'<div style="font-weight:800;font-size:{fs}px;color:{G}">{h}</div>' for h in H)
    tr="".join("".join(f'<div style="font-size:{fs}px;font-weight:{800 if j==0 else 600};border-top:3px solid {K};padding-top:12px;line-height:1.25">{c}</div>' for j,c in enumerate(r)) for r in D)
    return f'<div style="display:grid;grid-template-columns:{cols};gap:12px 18px">{th}{tr}</div>'
