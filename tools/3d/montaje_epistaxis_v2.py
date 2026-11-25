"""Montaje del vídeo de técnica de la epistaxis v2 (~60 s, sin voz: subtítulos y música del canal).
Misma maqueta de rótulos que la punción lumbar v4 (etiqueta arriba, marca abajo, subtítulos, palabra clave en Anton)."""
import subprocess, textwrap, os
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920; Y = (255, 214, 10); K = (17, 17, 17)
REPO = "/home/claude/urgenciasen60-media"
AN = lambda s: ImageFont.truetype(f"{REPO}/tools/fonts/anton-latin-400-normal.woff2", s)
IN = lambda s, w="Bold": ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{w}.otf", s)
E = "/home/claude/v3d/epi"; WD = "/home/claude/v3d/mont_epi"; OV = f"{WD}/ov"; os.makedirs(OV, exist_ok=True); os.chdir(WD)
END = 60.0
def png(name, draw): im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw(ImageDraw.Draw(im)); im.save(f"{OV}/{name}.png"); return f"{OV}/{name}.png"
def base(d):
    tag = "TÉCNICA 02 · EPISTAXIS"; tw = d.textlength(tag, font=IN(30, "Black"))
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
# guion (subtítulos sin locución): (inicio, fin, texto)
SUBS = [(0.3, 4.4, "Epistaxis: cinco pasos, en orden."),
        (4.5, 8.0, "Sentado e inclinado hacia delante. Nunca con la cabeza hacia atrás."),
        (8.0, 11.0, "Antes, que se suene para expulsar los coágulos."),
        (11.0, 15.2, "Pinza firme de la parte blanda de la nariz, sin soltar."),
        (15.2, 19.0, "Al menos cinco minutos, de forma continua."),
        (19.0, 22.2, "Casi siempre sangra la parte anterior del tabique."),
        (22.2, 25.0, "Comprimir sobre el hueso no sirve."),
        (25.0, 31.0, "Si no cede: algodón con anestésico local y vasoconstrictor dentro de la fosa, y vuelve a comprimir."),
        (31.0, 37.0, "Retira los coágulos y busca el punto con rinoscopia anterior y buena luz."),
        (37.0, 40.2, "Si lo ves, nitrato de plata solo en ese punto."),
        (40.2, 43.5, "Nunca en los dos lados del tabique a la vez."),
        (43.5, 48.0, "Si sigue sangrando o no lo ves: taponamiento anterior, paralelo al suelo de la fosa."),
        (48.0, 51.5, "Si toma anticoagulantes o antiagregantes, mejor material reabsorbible."),
        (51.5, 55.0, "Si sangra pese al taponamiento, avisa a Otorrinolaringología."),
        (55.2, 59.6, "Los cinco pasos, en el carrusel.")]
OVL = [(png("base", base), 0, END)]+[(png(f"s{i:02d}", sub(t)), a, b) for i, (a, b, t) in enumerate(SUBS)]
OVL += [(png("k_tit", key("EPISTAXIS")), 0, 4.5), (png("k_pos", key("POSICIÓN")), 4.5, 11.0),
        (png("k_1", key("1 · COMPRIME")), 11.0, 19.0), (png("p_1", pill("Tercio inferior · 5 min o más")), 11.0, 19.0),
        (png("k_kie", key("¿POR QUÉ AHÍ?")), 19.0, 25.0), (png("p_kie", pill("Área de Kiesselbach")), 19.0, 25.0),
        (png("k_2", key("2 · VASOCONSTRICTOR")), 25.0, 31.0),
        (png("k_3", key("3 · BUSCA EL PUNTO")), 31.0, 37.0),
        (png("k_4", key("4 · CAUTERIZA")), 37.0, 43.5), (png("p_4", pill("Solo el punto · un solo lado")), 37.0, 43.5),
        (png("k_5", key("5 · TAPONA")), 43.5, 51.5), (png("p_5", pill("Paralelo al suelo de la fosa")), 43.5, 51.5),
        (png("k_orl", key("AVISA A ORL")), 51.5, 55.0)]
FICHA = f"{REPO}/borradores/tecnica-epistaxis/urgenciasen60-tecnica-epistaxis-7.jpg"
SEG = [("anim", f"{E}/f_intro/%03d.jpg", 0, 4.5, 30), ("still", f"{E}/s_perfil.jpg", 4.5, 11.0, 0),
       ("anim", f"{E}/f_pinza/%03d.jpg", 11.0, 19.0, 30), ("anim", f"{E}/f_crayos/%03d.jpg", 19.0, 25.0, 30),
       ("anim", f"{E}/f_algodon/%03d.jpg", 25.0, 31.0, 30), ("anim", f"{E}/f_crinos/%03d.jpg", 31.0, 37.0, 30),
       ("anim", f"{E}/f_cnitrato/%03d.jpg", 37.0, 43.5, 30), ("anim", f"{E}/f_ctapon/%03d.jpg", 43.5, 51.5, 40),
       ("still", f"{E}/s_retrato.jpg", 51.5, 55.0, 0), ("ficha", FICHA, 55.0, END, 0)]
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
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", cur, "-i", "musica.wav", "-filter_complex",
  f"[1:a]loudnorm=I=-16:TP=-1.5,afade=t=in:st=0:d=0.8,afade=t=out:st={END-2.5:.2f}:d=2.5[a]",
  "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(END), "urgenciasen60-tecnica-epistaxis-video60.mp4"], check=True)
print("hecho", END)
