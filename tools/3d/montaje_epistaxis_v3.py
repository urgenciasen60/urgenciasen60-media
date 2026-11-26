"""Montaje del vídeo de técnica de la epistaxis v3 (60 s, sin voz: subtítulos y música del canal).
Ilustraciones vectoriales animadas (tools/svg_epistaxis.py) para postura, compresión, anatomía y rinoscopia,
y planos 3D del material real (tools/3d/material_epistaxis.py). Menos texto en pantalla: etiqueta, paso y subtítulo."""
import subprocess, textwrap, os
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920; Y = (255, 214, 10); K = (17, 17, 17)
REPO = "/home/claude/urgenciasen60-media"
IN = lambda s, w="Bold": ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{w}.otf", s)
E = "/home/claude/v3d/epi3"; S = f"{E}/svg"; M = f"{E}/mat"
WD = f"{E}/mont"; OV = f"{WD}/ov"; os.makedirs(OV, exist_ok=True); os.chdir(WD)
END = 60.0
def png(name, draw): im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw(ImageDraw.Draw(im)); im.save(f"{OV}/{name}.png"); return f"{OV}/{name}.png"
def base(d):
    tag = "TÉCNICA 02 · EPISTAXIS"; tw = d.textlength(tag, font=IN(30, "Black"))
    d.rounded_rectangle([60, 236, 60+tw+40, 294], 8, fill=Y); d.text((80, 247), tag, font=IN(30, "Black"), fill=K)
    h = "@urgenciasen60"; d.rounded_rectangle([60, H-330, 60+d.textlength(h, font=IN(30, "Bold"))+32, H-282], 8, fill=K); d.text((76, H-323), h, font=IN(30, "Bold"), fill=Y)
def sub(text):
    def f(d):
        lines = textwrap.wrap(text, 28); y = H-380-len(lines)*70
        for l in lines:
            w = d.textlength(l, font=IN(54, "Black")); d.rounded_rectangle([60-18, y-10, 60+w+18, y+64], 10, fill=(17, 17, 17, 230)); d.text((60, y), l, font=IN(54, "Black"), fill=(255, 255, 255)); y += 74
    return f
def paso(text):
    def f(d):
        w = d.textlength(text, font=IN(32, "Black")); d.rounded_rectangle([60, 310, 60+w+36, 364], 8, fill=(255, 255, 255)); d.text((78, 318), text, font=IN(32, "Black"), fill=K)
    return f
def marca(text, y=1180):
    def f(d):
        w = d.textlength(text, font=IN(34, "SemiBold")); d.rounded_rectangle([W-60-w-36, y, W-60, y+56], 28, fill=(17, 17, 17, 210)); d.text((W-60-w-18, y+8), text, font=IN(34, "SemiBold"), fill=Y)
    return f
# guion (subtítulos sin locución): (inicio, fin, texto)
SUBS = [(0.2, 2.6, "¿Cabeza hacia atrás? No."),
        (2.6, 5.0, "Sentado e inclinado hacia delante."),
        (5.0, 10.0, "Pinza la parte blanda, 5 minutos sin soltar."),
        (10.0, 14.5, "Prepara todo el material antes de empezar."),
        (14.5, 19.5, "Algodón con anestésico y vasoconstrictor, 10 minutos."),
        (19.5, 24.5, "Retira los coágulos y busca el punto con buena luz."),
        (24.5, 27.5, "¿Ves el punto? Nitrato de plata solo ahí."),
        (27.5, 30.5, "Nunca los dos lados del tabique."),
        (30.5, 33.5, "¿No lo ves o sigue sangrando? Tapona."),
        (33.5, 36.5, "Paralelo al suelo, nunca hacia arriba."),
        (36.5, 41.0, "Esponja expansible: se hidrata y se expande."),
        (41.0, 45.5, "¿Anticoagulado o antiagregado? Mejor reabsorbible."),
        (45.5, 50.0, "Balón: mójalo antes y se hincha con aire."),
        (50.0, 55.0, "¿Cae sangre a la faringe o sangra con el taponamiento? Avisa a ORL."),
        (55.2, 59.6, "Guárdate la ficha.")]
OVL = [(png("base", base), 0, 55.0)]+[(png(f"s{i:02d}", sub(t)), a, b) for i, (a, b, t) in enumerate(SUBS)]
OVL += [(png("p1", paso("1 · POSICIÓN Y COMPRESIÓN")), 0.2, 10.0), (png("p2", paso("2 · VASOCONSTRICTOR")), 14.5, 19.5),
        (png("p3", paso("3 · BUSCA EL PUNTO")), 19.5, 24.5), (png("p4", paso("4 · CAUTERIZA")), 24.5, 30.5),
        (png("p5", paso("5 · TAPONA")), 30.5, 50.0), (png("pm", paso("MATERIAL")), 10.0, 14.5),
        (png("m1", marca("tipo Merocel®")), 36.5, 41.0), (png("m2", marca("tipo Spongostan® · Surgicel®")), 41.0, 45.5),
        (png("m3", marca("tipo Rapid Rhino®")), 45.5, 50.0), (png("m4", marca("varillas tipo Argenpal®")), 24.5, 26.2)]
FICHA = f"{REPO}/borradores/tecnica-epistaxis/urgenciasen60-tecnica-epistaxis-7.jpg"
# (tipo, fuente, inicio, fin, nº de fotogramas de la fuente)
SEG = [("seq", f"{S}/f_postura/%03d.jpg", 0.0, 5.0, 150), ("seq", f"{S}/f_pinza/%03d.jpg", 5.0, 10.0, 150),
       ("anim", f"{M}/f_mesa/%03d.jpg", 10.0, 14.5, 18), ("seq", f"{S}/f_algodon/%03d.jpg", 14.5, 19.5, 150),
       ("seq", f"{S}/f_rinos/%03d.jpg", 19.5, 24.5, 150), ("still", f"{M}/s_nitrato.jpg", 24.5, 26.2, 0),
       ("seq", f"{S}/f_nitrato/%03d.jpg", 26.2, 30.5, 135), ("seq", f"{S}/f_tapona/%03d.jpg", 30.5, 36.5, 180),
       ("anim", f"{M}/f_esponja/%03d.jpg", 36.5, 41.0, 18), ("still", f"{M}/s_reabs.jpg", 41.0, 45.5, 0),
       ("anim", f"{M}/f_balon/%03d.jpg", 45.5, 50.0, 18), ("seq", f"{S}/f_posterior/%03d.jpg", 50.0, 55.0, 150),
       ("ficha", FICHA, 55.0, END, 0)]
os.makedirs("seg", exist_ok=True); files = []
for i, (kind, src, a, b, x) in enumerate(SEG):
    d = b-a; out = f"seg/{i:02d}.mp4"; n = round(d*30)
    if kind == "still":
        vf = f"scale=2160:3840,zoompan=z='1+0.08*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", src, "-vf", vf+",format=yuv420p", "-frames:v", str(n)]
    elif kind == "anim":
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", f"{x/d:.4f}", "-i", src, "-vf", "scale=1080:1920:flags=lanczos,minterpolate=fps=30:mi_mode=blend,tpad=stop_mode=clone:stop_duration=2,format=yuv420p", "-frames:v", str(n)]
    elif kind == "seq":
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", f"{x/d:.4f}", "-i", src, "-vf", "fps=30,tpad=stop_mode=clone:stop_duration=2,format=yuv420p", "-frames:v", str(n)]
    else:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", src, "-vf", "scale=820:-1,pad=1080:1920:(ow-iw)/2:330:color=0x111111,format=yuv420p", "-frames:v", str(n)]
    subprocess.run(cmd+["-r", "30", "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", out], check=True); files.append(out)
open("seg/lista.txt", "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in files))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "seg/lista.txt", "-c", "copy", "base.mp4"], check=True)
cur = "base.mp4"
for k in range(0, len(OVL), 12):
    batch = OVL[k:k+12]; ins = []; fcx = []; last = "[0:v]"
    for j, (p, a, b) in enumerate(batch):
        ins += ["-i", p]; tag = f"[v{j}]"; fcx.append(f"{last}[{j+1}:v]overlay=enable='between(t,{a:.3f},{b-0.034:.3f})'{tag}"); last = tag
    out = f"ovl_{k}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", cur]+ins+["-filter_complex", ";".join(fcx), "-map", last, "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", out], check=True); cur = out
subprocess.run(["python3", f"{REPO}/tools/musica.py", "musica.wav", str(END)], check=True, capture_output=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", cur, "-i", "musica.wav", "-filter_complex",
  f"[1:a]loudnorm=I=-16:TP=-1.5,afade=t=in:st=0:d=0.8,afade=t=out:st={END-2.5:.2f}:d=2.5[a]",
  "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(END), "urgenciasen60-tecnica-epistaxis-video60.mp4"], check=True)
print("hecho", END)
