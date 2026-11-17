"""Generador de carruseles Urgencias en 60 -> HTML estático + PNG 1080x1350."""
import os, subprocess, sys
Y="#FFD60A"; K="#111111"; R="#D7141A"; G="#4A4A4A"
FONT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"fonts","anton-latin-400-normal.woff2")
A="font-family: Anton, sans-serif; line-height: 1.02"
def page(n,total,tema,body,cover=False,ficha=None):
    bg = Y if cover else "#FFFFFF"; fb = K if cover else Y; ff = Y if cover else K
    right = f"FICHA {ficha}" if ficha else f"{n} / {total}"
    last = "Guárdalo" if ficha else "Desliza →"
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>@font-face{{font-family:Anton;src:url("file://{FONT}") format("woff2")}}body{{margin:0}}</style></head><body>
<div style="width:1080px;height:1350px;box-sizing:border-box;display:flex;flex-direction:column;background:{bg};color:{K};font-family:Inter,sans-serif">
<div style="height:28px;background:{R}"></div>
<div style="display:flex;justify-content:space-between;align-items:center;padding:48px 80px 0 80px">
<div style="background:{K};color:#FFF;padding:12px 24px;border-radius:8px;font-size:26px;font-weight:800;letter-spacing:3px">URGENCIAS EN 60 · {tema}</div>
<div style="font-size:30px;font-weight:800">{right}</div></div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px;padding:0 80px">{body}</div>
<div style="height:108px;background:{fb};color:{ff};display:flex;justify-content:space-between;align-items:center;padding:0 80px;font-size:32px;font-weight:800"><div>@urgenciasen60</div><div>{last}</div></div>
</div></body></html>'''
def row(k,v): return f'<div style="border-top:4px solid {K};padding-top:22px;display:flex;justify-content:space-between;gap:32px;font-size:40px"><div style="color:{G};font-weight:600">{k}</div><div style="font-weight:800;text-align:right">{v}</div></div>'
def num(i,t): return f'<div style="display:flex;gap:32px;align-items:baseline"><div style="{A};font-size:80px;color:{R};width:64px">{i}</div><div style="font-size:50px;font-weight:800;line-height:1.2">{t}</div></div>'
def line(t,bold=False): return f'<div style="border-top:4px solid {K};padding-top:22px;font-size:42px;font-weight:{800 if bold else 600};line-height:1.3">{t}</div>'
def kicker(t): return f'<div style="font-size:40px;font-weight:800;letter-spacing:6px;color:{G}">{t}</div>'
def big(t,size,color=K,nowrap=False): return f'<div style="{A};font-size:{size}px;color:{color};{"white-space:nowrap" if nowrap else ""}">{t}</div>'
def frow(k,v,red=False,fs=36): return f'<div style="border-top:4px solid {K};padding-top:16px;display:flex;gap:28px;align-items:baseline"><div style="width:250px;flex-shrink:0;font-size:28px;font-weight:800;letter-spacing:2px;color:{G}">{k}</div><div style="font-size:{fs}px;font-weight:800;line-height:1.25;color:{R if red else K}">{v}</div></div>'
def ficha_body(titulo,ambito,rows,fuentes,size=136,fs=36):
    """fs: tamaño del texto de las filas (36 por defecto; bajar a 32-33 si la ficha lleva mucho texto)."""
    r="".join(frow(*x,fs=fs) if len(x)==2 else frow(x[0],x[1],x[2],fs) for x in rows)
    return f'<div style="display:flex;align-items:baseline;justify-content:space-between"><div style="{A};font-size:{size}px;white-space:nowrap">{titulo}</div><div style="font-size:34px;font-weight:800;color:{G}">{ambito}</div></div><div style="display:flex;flex-direction:column;gap:16px">{r}</div><div style="font-size:21px;line-height:1.4;color:{G}">Fuentes: {fuentes}. Contenido formativo para profesionales sanitarios; no sustituye a los protocolos de tu centro.</div>'
def render(pages,outdir,slug):
    os.makedirs(outdir,exist_ok=True); out=[]
    for i,h in enumerate(pages,1):
        hp=os.path.join(outdir,f"{i}.html"); open(hp,"w").write(h)
        png=os.path.join(outdir,f"urgenciasen60-{slug}-{i}.png")
        subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--window-size=1080,1350",f"--screenshot={png}","--virtual-time-budget=3000","file://"+hp],capture_output=True)
        from PIL import Image
        jpg=png[:-4]+".jpg"   # TikTok no admite PNG: se entrega siempre JPG
        Image.open(png).convert("RGB").save(jpg,quality=95,subsampling=0); os.remove(png)
        out.append(jpg)
    from PIL import Image
    cols=4; rows_=(len(out)+cols-1)//cols
    sheet=Image.new("RGB",(cols*550+10,rows_*685+10),"#888888")
    for i,f in enumerate(out): sheet.paste(Image.open(f).resize((540,675)),(10+(i%cols)*550,10+(i//cols)*685))
    sheet.save(os.path.join(outdir,"_sheet.png")); return out
