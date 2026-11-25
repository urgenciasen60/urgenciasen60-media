"""Montaje del vídeo de técnica de la punción lumbar v4 (~60 s): escenas 3D, corte sagital, rótulos, locución y música baja.
Rótulos con la misma maqueta que v3 (aprobada): etiqueta arriba, marca abajo, subtítulos y palabra clave en Anton."""
import subprocess, textwrap, os
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920; Y = (255, 214, 10); K = (17, 17, 17); R = (215, 20, 26)
REPO = "/home/claude/urgenciasen60-media"
AN = lambda s: ImageFont.truetype(f"{REPO}/tools/fonts/anton-latin-400-normal.woff2", s)
IN = lambda s, w="Bold": ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{w}.otf", s)
V4 = "/home/claude/v3d/v4"; WD = "/home/claude/v3d/mont"; OV = f"{WD}/ov"; os.makedirs(OV, exist_ok=True); os.chdir(WD)
T = [(float(a), b) for a, b in (l.split("\t") for l in open("/home/claude/v3d/pl_voz.wav.tiempos.txt").read().splitlines())]
t = lambda i: T[i][0]
END = round(T[-1][0]+3.2+1.7, 2)    # fin de la última frase + cola con la ficha
def png(name, draw): im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw(ImageDraw.Draw(im)); im.save(f"{OV}/{name}.png"); return f"{OV}/{name}.png"
def base(d):
    tag = "TÉCNICA 01 · PUNCIÓN LUMBAR"; tw = d.textlength(tag, font=IN(30, "Black"))
    d.rounded_rectangle([60, 236, 60+tw+40, 294], 8, fill=Y); d.text((80, 247), tag, font=IN(30, "Black"), fill=K)
    h = "@urgenciasen60"; d.rounded_rectangle([60, H-410, 60+d.textlength(h, font=IN(34, "Bold"))+36, H-354], 8, fill=K); d.text((78, H-402), h, font=IN(34, "Bold"), fill=Y)
def sub(text):
    def f(d):
        lines = textwrap.wrap(text, 30); y = H-440-len(lines)*70
        for l in lines:
            w = d.textlength(l, font=IN(52, "Black")); d.rectangle([60-16, y-8, 60+w+16, y+62], fill=(17, 17, 17, 225)); d.text((60, y), l, font=IN(52, "Black"), fill=(255, 255, 255)); y += 70
    return f
def key(text, col=Y): return lambda d: d.text((60, 330), text, font=AN(118), fill=col, stroke_width=6, stroke_fill=(17, 17, 17))
def pill(text):
    def f(d):
        w = d.textlength(text, font=IN(44, "Black")); d.rounded_rectangle([60, 505, 60+w+44, 573], 10, fill=Y); d.text((82, 513), text, font=IN(44, "Black"), fill=K)
    return f
OVL = [(png("base", base), 0, END)]
for i, (a, txt) in enumerate(T):
    b = T[i+1][0] if i+1 < len(T) else END-0.4
    txt = txt.replace("ele cuatro, ele cinco", "L4–L5").replace("ele cuatro", "L4").replace("sesenta segundos", "60 segundos")
    OVL.append((png(f"s{i:02d}", sub(txt)), a, b))
OVL += [(png("k_titulo", key("PUNCIÓN LUMBAR")), 0, t(2)), (png("k_pos", key("POSICIÓN")), t(2), t(4)),
        (png("k_ref", key("REFERENCIA")), t(4), t(7)), (png("k_l4", pill("Línea de las crestas = L4")), t(5), t(7)),
        (png("k_ase", key("ASEPSIA")), t(7), t(9)), (png("k_esp", pill("Pinchar en L4–L5 o en L3–L4")), t(7), t(9)),
        (png("k_agu", key("AGUJA")), t(9), t(14)), (png("k_atr", pill("Atraumática · bisel paralelo")), t(9), t(11)),
        (png("k_lcr", key("LCR")), t(14), t(16)), (png("k_fia", key("FIADOR DENTRO")), t(16), t(17))]
# capas del corte: fotogramas de la animación (escala de 71) -> segundos
c0, c1 = t(12), t(14); NC = 71
fc = lambda f: c0+f/NC*(c1-c0)
for a, b, txt in [(0, 15, "Piel y tejido subcutáneo"), (15, 27, "Ligamentos supra e interespinoso"), (27, 38, "Ligamento amarillo"),
                  (38, 48, "Espacio epidural"), (48, 53, "Duramadre"), (53, 71, "Espacio subaracnoideo: LCR")]:
    OVL.append((png(f"capa{a}", pill(txt)), fc(a), fc(b)))
# fiador de vuelta: los fotogramas de la retirada, al revés
os.makedirs("rev", exist_ok=True)
ph1 = [f for f in range(56) if f/55 < 0.31]
for j, f in enumerate(reversed(ph1)): os.system(f"cp {V4}/f_lcr/{f:03d}.jpg rev/{j:03d}.jpg")
FICHA = f"{REPO}/borradores/tecnica-puncion-lumbar/urgenciasen60-tecnica-puncion-lumbar-7.jpg"
SEG = [("anim", f"{V4}/f_intro/%03d.jpg", 0, t(2), 28), ("anim", f"{V4}/f_orbit/%03d.jpg", t(2), t(4), 48),
       ("still", f"{V4}/s_crestas.jpg", t(4), t(5), 0), ("still", f"{V4}/s_rayos.jpg", t(5), t(7), 0), ("still", f"{V4}/s_marca.jpg", t(7), t(9), 0),
       ("anim", f"{V4}/f_aguja/%03d.jpg", t(9), t(12), 56), ("anim", f"{V4}/f_corte/%03d.jpg", t(12), t(14), 56),
       ("anim", f"{V4}/f_lcr/%03d.jpg", t(14), t(16), 56), ("anim", f"{WD}/rev/%03d.jpg", t(16), t(17), len(ph1)),
       ("ficha", FICHA, t(17), END, 0)]
os.makedirs("seg", exist_ok=True); files = []
for i, (kind, src, a, b, x) in enumerate(SEG):
    d = b-a; out = f"seg/{i:02d}.mp4"; n = round(d*30)
    if kind == "still":
        vf = f"scale=2160:3840,zoompan=z='1+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", src, "-vf", vf+",format=yuv420p", "-frames:v", str(n)]
    elif kind == "anim":
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", f"{x/d:.4f}", "-i", src, "-vf", "scale=1080:1920:flags=lanczos,minterpolate=fps=30:mi_mode=blend,tpad=stop_mode=clone:stop_duration=2,format=yuv420p", "-frames:v", str(n)]
    else:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", src, "-vf", "scale=800:-1,pad=1080:1920:(ow-iw)/2:315:color=0x111111,format=yuv420p", "-frames:v", str(n)]
    subprocess.run(cmd+["-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", out], check=True); files.append(out)
open("seg/lista.txt", "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in files))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "seg/lista.txt", "-c", "copy", "base.mp4"], check=True)
cur = "base.mp4"
for k in range(0, len(OVL), 12):
    batch = OVL[k:k+12]; ins = []; fcx = []; last = "[0:v]"
    for j, (p, a, b) in enumerate(batch):
        ins += ["-i", p]; tag = f"[v{j}]"; fcx.append(f"{last}[{j+1}:v]overlay=enable='between(t,{a:.2f},{b:.2f})'{tag}"); last = tag
    out = f"ovl_{k}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", cur]+ins+["-filter_complex", ";".join(fcx), "-map", last, "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", out], check=True); cur = out
subprocess.run(["python3", f"{REPO}/tools/musica.py", "musica.wav", str(END)], check=True, capture_output=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", cur, "-i", "/home/claude/v3d/pl_voz.wav", "-i", "musica.wav", "-filter_complex",
  f"[1:a]loudnorm=I=-16:TP=-1.5,apad[v];[2:a]volume=0.08,afade=t=out:st={END-2.5:.2f}:d=2.5[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
  "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(END), "urgenciasen60-tecnica-puncion-lumbar-video60.mp4"], check=True)
print("hecho", END)
