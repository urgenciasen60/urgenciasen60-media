import subprocess, textwrap, os
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920; Y=(255,214,10); K=(17,17,17); R=(215,20,26)
AN=lambda s: ImageFont.truetype("/home/claude/v3d/Anton.ttf",s); IN=lambda s,w="Bold": ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{w}.otf",s)
V="/home/claude/v3d"; OV="/home/claude/night/ov"
T=[(float(a),b) for a,b in (l.split("\t") for l in open("pl_voz.wav.tiempos.txt").read().splitlines())]
END=63.5
def png(name,draw): im=Image.new("RGBA",(W,H),(0,0,0,0)); draw(ImageDraw.Draw(im)); im.save(f"{OV}/{name}.png"); return f"{OV}/{name}.png"
def base(d):
    tag="TÉCNICA 02 · PUNCIÓN LUMBAR"; tw=d.textlength(tag,font=IN(30,"Black"))
    d.rounded_rectangle([60,236,60+tw+40,294],8,fill=Y); d.text((80,247),tag,font=IN(30,"Black"),fill=K)
    h="@urgenciasen60"; d.rounded_rectangle([60,H-410,60+d.textlength(h,font=IN(34,"Bold"))+36,H-354],8,fill=K); d.text((78,H-402),h,font=IN(34,"Bold"),fill=Y)
def sub(text):
    def f(d):
        lines=textwrap.wrap(text,30); y=H-440-len(lines)*70
        for l in lines:
            w=d.textlength(l,font=IN(52,"Black")); d.rectangle([60-16,y-8,60+w+16,y+62],fill=(17,17,17,225)); d.text((60,y),l,font=IN(52,"Black"),fill=(255,255,255)); y+=70
    return f
def key(text,col=Y):
    return lambda d: d.text((60,330),text,font=AN(118),fill=col,stroke_width=6,stroke_fill=(17,17,17))
def pill(text):
    def f(d):
        w=d.textlength(text,font=IN(44,"Black")); d.rounded_rectangle([60,505,60+w+44,573],10,fill=Y); d.text((82,513),text,font=IN(44,"Black"),fill=K)
    return f
def tclist(d):
    d.text((60,330),"¿TC ANTES?",font=AN(130),fill=Y,stroke_width=6,stroke_fill=(17,17,17))
    items=["Bajo nivel de consciencia","Focalidad neurológica","Papiledema","Crisis reciente","Inmunodepresión","60 años o más"]
    y=520
    for it in items: d.rectangle([60,y+14,84,y+38],fill=R); d.text((104,y),it,font=IN(50,"Black"),fill=(255,255,255),stroke_width=4,stroke_fill=(17,17,17)); y+=82
OVL=[(png("base",base),0,END)]
for i,(t,txt) in enumerate(T):
    t1=T[i+1][0] if i+1<len(T) else END-0.5
    txt=txt.replace("te ce","TC").replace("ele cuatro, ele cinco","L4–L5").replace("Hoy, solo la técnica.","Hoy, solo la técnica.").replace("ele cuatro","L4").replace("sesenta segundos","60 segundos").replace("sesenta años","60 años")
    OVL.append((png(f"s{i:02d}",sub(txt)),t,t1))
OVL+=[(png("k_titulo",key("PUNCIÓN LUMBAR")),0,4.72),(png("k_pos",key("POSICIÓN")),4.72,13.67),
      (png("k_ref",key("REFERENCIA")),13.67,23.57),(png("k_l4",pill("Línea de las crestas = L4")),15.85,23.57),
      (png("k_ase",key("ASEPSIA")),23.57,29.77),(png("k_esp",pill("Pinchar en L4–L5 o en L3–L4")),23.57,29.77),
      (png("k_agu",key("AGUJA")),29.77,49.91),(png("k_atr",pill("Atraumática · bisel paralelo")),29.77,36.6),(png("k_lcr",key("LCR")),49.91,55.06)]
cut0,cutd=40.23,9.68; ft=lambda f: cut0+f/60*cutd
for a,b,txt in [(0,12,"Piel y tejido subcutáneo"),(12,32,"Ligamentos supra e interespinoso"),(32,38,"Ligamento amarillo"),(38,43,"Espacio epidural"),(43,49,"Duramadre"),(49,60,"Espacio subaracnoideo: LCR")]:
    OVL.append((png(f"capa{a}",pill(txt)),ft(a),ft(b)))
# segmentos de vídeo
SEG=[("still","/home/claude/v3d/mh/s_general.jpg",0,4.72,0),("anim","/home/claude/v3d/mh/f_orbit/o_%03d.jpg",4.72,13.67,58),
     ("still","/home/claude/v3d/mh/s_crestas.jpg",13.67,15.85,0),("still","/home/claude/v3d/mh/s_rayos.jpg",15.85,23.57,0),("still","/home/claude/v3d/mh/s_marca.jpg",23.57,29.77,0),
     ("anim","/home/claude/v3d/mh/f_aguja/a_%03d.jpg",29.77,40.23,60),("anim",f"{V}/fc/c_%03d.jpg",40.23,49.91,60),("anim","/home/claude/v3d/mh/f_gotas/g_%03d.jpg",49.91,55.06,36),
     ("ficha","/home/claude/urgenciasen60-media/borradores/tecnica-puncion-lumbar/urgenciasen60-tecnica-puncion-lumbar-7.jpg",55.06,END,0)]
os.makedirs("seg",exist_ok=True); files=[]
for i,(kind,src,a,b,x) in enumerate(SEG):
    d=b-a; out=f"seg/{i:02d}.mp4"; n=round(d*30)
    if kind=="still":
        vf=f"scale=2160:3840,zoompan=z='1+0.05*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"+(",eq=brightness=-0.22:saturation=0.6" if x else "")
        cmd=["ffmpeg","-y","-loglevel","error","-loop","1","-i",src,"-vf",vf+",format=yuv420p","-frames:v",str(n)]
    elif kind=="anim":
        cmd=["ffmpeg","-y","-loglevel","error","-framerate",f"{x/d:.4f}","-i",src,"-vf","scale=1080:1920:flags=lanczos,minterpolate=fps=30:mi_mode=blend,format=yuv420p","-frames:v",str(n)]
    else:
        cmd=["ffmpeg","-y","-loglevel","error","-loop","1","-i",src,"-vf","scale=800:-1,pad=1080:1920:(ow-iw)/2:315:color=0x111111,format=yuv420p","-frames:v",str(n)]
    subprocess.run(cmd+["-r","30","-c:v","libx264","-crf","18","-preset","veryfast",out],check=True); files.append(out)
open("seg/lista.txt","w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in files))
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i","seg/lista.txt","-c","copy","base.mp4"],check=True)
# rótulos: en tandas para no saturar el filtro
cur="base.mp4"
for k in range(0,len(OVL),12):
    batch=OVL[k:k+12]; ins=[]; fc=[]; last="[0:v]"
    for j,(p,a,b) in enumerate(batch):
        ins+=["-i",p]; tag=f"[v{j}]"; fc.append(f"{last}[{j+1}:v]overlay=enable='between(t,{a:.2f},{b:.2f})'{tag}"); last=tag
    out=f"ovl_{k}.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",cur]+ins+["-filter_complex",";".join(fc),"-map",last,"-c:v","libx264","-crf","18","-preset","veryfast",out],check=True); cur=out
subprocess.run(["python3","/home/claude/urgenciasen60-media/tools/musica.py","musica.wav",str(END)],check=True,capture_output=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",cur,"-i","pl_voz.wav","-i","musica.wav","-filter_complex",
  "[1:a]loudnorm=I=-16:TP=-1.5,apad[v];[2:a]volume=0.10,afade=t=out:st=61:d=2.5[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
  "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-t",str(END),"urgenciasen60-tecnica-puncion-lumbar-video60-v3.mp4"],check=True)
print("hecho")
