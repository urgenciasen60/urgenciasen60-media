"""Generador de reels Urgencias en 60 (v2): 1080x1920, 30 fps.
- Título arriba; marca y @ abajo, dentro de la zona segura.
- Cada escena tiene su color de fondo y 1-2 pasos (varios elementos entran a la vez).
- Efectos: golpe de zoom al entrar cada paso, transición deslizante entre escenas y barra de progreso roja.
Un solo render con ffmpeg."""
import os, subprocess
HERE=os.path.dirname(os.path.abspath(__file__))
FONT=os.path.join(HERE,"fonts","anton-latin-400-normal.woff2")
Y="#FFD60A"; K="#111111"; R="#D7141A"; G="#4A4A4A"; W="#FFFFFF"
A="font-family:Anton,sans-serif;line-height:1.02"
THEME={  # fondo: (texto, acento, secundario, fondo etiqueta, texto etiqueta)
 Y:(K,R,K,K,W), W:(K,R,G,K,W), R:(W,Y,W,K,W), K:(W,Y,"#CFCFCF",Y,K)}
def big(t,size,color=None): return f'<div style="{A};font-size:{size}px;{"color:"+color if color else ""}">{t}</div>'
def txt(t,size=64,color=None,weight=800): return f'<div style="max-width:800px;font-size:{size}px;font-weight:{weight};line-height:1.2;{"color:"+color if color else ""}">{t}</div>'
def kicker(t,color=None): return f'<div style="font-size:46px;font-weight:800;letter-spacing:7px;{"color:"+color if color else ""}">{t}</div>'
def html(bg,blocks,shown,tema):
    fg,acc,sec,tb,tf=THEME[bg]
    body="".join(f'<div style="visibility:{"visible" if i<shown else "hidden"}">{b}</div>' for i,b in enumerate(blocks))
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>@font-face{{font-family:Anton;src:url("file://{FONT}") format("woff2")}}body{{margin:0}}</style></head><body>
<div style="width:1080px;height:1920px;box-sizing:border-box;background:{bg};color:{fg};font-family:Inter,sans-serif;position:relative;overflow:hidden">
<div style="position:absolute;top:230px;bottom:640px;left:90px;right:90px;display:flex;flex-direction:column;justify-content:flex-start;gap:44px">{body}</div>
<div style="position:absolute;bottom:420px;left:90px;display:flex;flex-direction:column;gap:22px;align-items:flex-start">
<div style="background:{tb};color:{tf};padding:12px 24px;border-radius:10px;font-size:28px;font-weight:800;letter-spacing:4px">URGENCIAS EN 60 · {tema}</div>
<div style="font-size:38px;font-weight:800">@urgenciasen60</div></div>
</div></body></html>'''
def shot(h,png):
    hp=png[:-4]+".html"; open(hp,"w").write(h)
    subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--window-size=1080,1920",f"--screenshot={png}","--virtual-time-budget=3000","file://"+hp],capture_output=True)
    os.remove(hp)
def build(scenes,tema,outdir,name,frames_only=False,xf=0.3):
    """scenes: lista de (fondo, bloques, [(n_bloques_visibles, segundos), ...])."""
    os.makedirs(outdir,exist_ok=True); pngs=[]; meta=[]
    for si,(bg,blocks,steps) in enumerate(scenes):
        for ti,(shown,d) in enumerate(steps):
            png=os.path.join(outdir,f"s{si}_{ti}.png"); shot(html(bg,blocks,shown,tema),png)
            pngs.append(png); meta.append((si,ti,d))
    if frames_only: return pngs
    cmd=["ffmpeg","-y","-loglevel","error"]
    for p in pngs: cmd+=["-i",p]
    fc=[]; scene_lab=[]; scene_dur=[]
    for si in range(len(scenes)):
        labs=[]; tot=0
        for idx,(s,ti,d) in enumerate(meta):
            if s!=si: continue
            n=int(round(d*30)); amp=0.14 if ti==0 else 0.05
            fc.append(f"[{idx}:v]zoompan=z='if(lt(on,7),1+{amp}*(1-on/7),1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps=30,format=yuv420p,setsar=1[v{idx}]")
            labs.append(f"[v{idx}]"); tot+=n/30
        fc.append("".join(labs)+f"concat=n={len(labs)}:v=1:a=0,fps=30,settb=1/30[s{si}]"); scene_lab.append(f"[s{si}]"); scene_dur.append(tot)
    trans=["slideup","slideleft","slideup","slideright","slideup"]
    cur=scene_lab[0]; acc=scene_dur[0]
    for i in range(1,len(scene_lab)):
        off=acc-xf; out=f"[x{i}]"
        fc.append(f"{cur}{scene_lab[i]}xfade=transition={trans[(i-1)%len(trans)]}:duration={xf}:offset={off:.3f}{out}")
        cur=out; acc=acc+scene_dur[i]-xf
    T=acc
    fc.append(f"color=c=0x111111:s=1080x30:r=30:d={T:.3f},drawbox=x=0:y=20:w=1080:h=10:color=0xFFD60A:t=fill[bar];{cur}[bar]overlay=x='-W+W*t/{T:.3f}':y=0:shortest=1[v]")
    final=os.path.join(outdir,name); tmp=final[:-4]+".tmp.mp4"
    cmd+=["-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=44100","-filter_complex",";".join(fc),"-map","[v]","-map",f"{len(pngs)}:a","-t",f"{T:.3f}","-c:v","libx264","-crf","18","-preset","veryfast","-pix_fmt","yuv420p","-r","30","-c:a","aac",tmp]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode!=0: raise SystemExit(r.stderr[-1500:])
    os.replace(tmp,final); return final,round(T,1)
