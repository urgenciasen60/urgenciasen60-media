"""Generador de reels Urgencias en 60: 1080x1920, 30 fps, texto que se construye por pasos.
Cada escena es una lista de bloques; cada paso muestra un bloque más (el diseño no se mueve)."""
import os, subprocess, shutil
HERE=os.path.dirname(os.path.abspath(__file__))
FONT=os.path.join(HERE,"fonts","anton-latin-400-normal.woff2")
Y="#FFD60A"; K="#111111"; R="#D7141A"; G="#4A4A4A"; W="#FFFFFF"
A="font-family:Anton,sans-serif;line-height:1.02"
def big(t,size,color=K): return f'<div style="{A};font-size:{size}px;color:{color}">{t}</div>'
def txt(t,size=64,color=K,weight=800): return f'<div style="font-size:{size}px;font-weight:{weight};line-height:1.2;color:{color}">{t}</div>'
def kicker(t,color=G): return f'<div style="font-size:46px;font-weight:800;letter-spacing:7px;color:{color}">{t}</div>'
def html(bg,blocks,shown,tema,fg=K):
    body="".join(f'<div style="visibility:{"visible" if i<shown else "hidden"}">{b}</div>' for i,b in enumerate(blocks))
    tagbg,tagfg=(K,W)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>@font-face{{font-family:Anton;src:url("file://{FONT}") format("woff2")}}body{{margin:0}}</style></head><body>
<div style="width:1080px;height:1920px;box-sizing:border-box;background:{bg};color:{fg};font-family:Inter,sans-serif;position:relative;overflow:hidden">
<div style="position:absolute;top:0;left:0;right:0;height:36px;background:{R}"></div>
<div style="position:absolute;top:250px;left:90px;background:{tagbg};color:{tagfg};padding:14px 28px;border-radius:10px;font-size:32px;font-weight:800;letter-spacing:4px">URGENCIAS EN 60 · {tema}</div>
<div style="position:absolute;top:380px;bottom:520px;left:90px;right:90px;display:flex;flex-direction:column;justify-content:center;gap:48px">{body}</div>
<div style="position:absolute;bottom:400px;left:90px;font-size:40px;font-weight:800">@urgenciasen60</div>
</div></body></html>'''
def shot(h,png):
    hp=png[:-4]+".html"; open(hp,"w").write(h)
    subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--window-size=1080,1920",f"--screenshot={png}","--virtual-time-budget=3000","file://"+hp],capture_output=True)
    os.remove(hp)
def still(png,dur,mp4):
    tmp=mp4[:-4]+".tmp.mp4"
    r=subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","30","-i",png,"-vf",f"format=yuv420p,loop=-1:1,trim=duration={dur}","-c:v","libx264","-crf","18","-preset","veryfast","-pix_fmt","yuv420p","-r","30",tmp])
    if r.returncode==0: os.replace(tmp,mp4)
    else: raise SystemExit("ffmpeg falló en "+png)
def build(steps,outdir,name,frames_only=False):
    """steps: lista de (html, duración en segundos)."""
    os.makedirs(outdir,exist_ok=True); parts=[]
    for i,(h,d) in enumerate(steps):
        png=os.path.join(outdir,f"f{i:02d}.png"); shot(h,png)
        if frames_only: continue
        mp4=os.path.join(outdir,f"p{i:02d}.mp4"); still(png,d,mp4); parts.append(mp4)
    if frames_only: return
    lst=os.path.join(outdir,"lista.txt"); open(lst,"w").write("".join(f"file '{p}'\n" for p in parts))
    mudo=os.path.join(outdir,"mudo.mp4")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-c","copy",mudo],check=True)
    final=os.path.join(outdir,name)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",mudo,"-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=44100","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-shortest",final],check=True)
    return final
