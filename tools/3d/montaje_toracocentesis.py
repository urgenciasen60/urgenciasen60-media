"""Montaje del vídeo de técnica de la toracocentesis (Técnica 03, ~60 s, sin voz: subtítulos y música del canal).
Misma maqueta de rótulos que la punción lumbar v4 (etiqueta arriba, marca abajo, subtítulos, palabra clave en Anton)."""
import subprocess, textwrap, os
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920; Y = (255, 214, 10); K = (17, 17, 17)
REPO = "/home/claude/urgenciasen60-media"
AN = lambda s: ImageFont.truetype(f"{REPO}/tools/fonts/anton-latin-400-normal.woff2", s)
IN = lambda s, w="Bold": ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{w}.otf", s)
E = "/home/claude/v3d/tora"; WD = "/home/claude/v3d/mont_tora"; OV = f"{WD}/ov"; os.makedirs(OV, exist_ok=True); os.chdir(WD)
END = 60.0
def png(name, draw): im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw(ImageDraw.Draw(im)); im.save(f"{OV}/{name}.png"); return f"{OV}/{name}.png"
def base(d):
    tag = "TÉCNICA 03 · TORACOCENTESIS"; tw = d.textlength(tag, font=IN(30, "Black"))
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
SUBS = [(0.3, 4.4, "Toracocentesis: con eco y encima de la costilla."),
        (4.5, 8.0, "Sentado, inclinado hacia delante, con los brazos apoyados."),
        (8.0, 11.0, "Marca el punto con ecografía, en la misma posición en la que vas a pinchar."),
        (11.0, 14.0, "Lateral o posterolateral, nunca pegado a la columna."),
        (14.0, 17.0, "Justo por encima del borde superior de la costilla de abajo."),
        (17.0, 20.5, "La arteria, la vena y el nervio van por debajo de cada costilla."),
        (20.5, 24.0, "Aspira mientras avanzas: si sale líquido, estás en la pleura."),
        (24.0, 28.0, "Asepsia y lidocaína al 1 %: piel, borde de la costilla y pleura."),
        (28.0, 32.0, "Aguja fina, perpendicular a la piel, aspirando."),
        (32.0, 36.0, "Muestras: bioquímica, pH, citología, cultivos y ADA."),
        (36.0, 40.0, "Para evacuar, catéter con llave de tres pasos."),
        (40.0, 44.0, "Despacio, con jeringa o por gravedad. Nunca con vacío."),
        (44.0, 48.0, "Para si aparece tos persistente, opresión, dolor o más disnea."),
        (48.0, 52.0, "El edema de reexpansión es raro, pero grave."),
        (52.0, 55.0, "Radiografía de control solo si hay síntomas, complicaciones o varios intentos."),
        (55.2, 59.6, "Los cinco pasos, en el carrusel.")]
OVL = [(png("base", base), 0, END)]+[(png(f"s{i:02d}", sub(t)), a, b) for i, (a, b, t) in enumerate(SUBS)]
OVL += [(png("k_tit", key("TORACOCENTESIS")), 0, 4.5),
        (png("k_1", key("1 · ECOGRAFÍA")), 4.5, 11.0), (png("p_1", pill("Obligatoria salvo emergencia")), 4.5, 11.0),
        (png("k_2", key("2 · DÓNDE")), 11.0, 17.0), (png("p_2", pill("Encima de la costilla de abajo")), 11.0, 17.0),
        (png("k_por", key("¿POR QUÉ?")), 17.0, 24.0), (png("p_por", pill("El paquete va bajo la costilla")), 17.0, 24.0),
        (png("k_3", key("3 · ANESTESIA")), 24.0, 28.0),
        (png("k_4", key("4 · PUNCIÓN")), 28.0, 36.0), (png("p_4", pill("Diagnóstica: aguja 21 G, ~50 ml")), 28.0, 36.0),
        (png("k_ev", key("EVACUADORA")), 36.0, 44.0), (png("p_ev", pill("Catéter si más de 60 ml")), 36.0, 44.0),
        (png("k_5", key("5 · SABER PARAR")), 44.0, 52.0), (png("p_5", pill("Máximo 1,5 l por sesión")), 44.0, 52.0),
        (png("k_rx", key("CONTROL")), 52.0, 55.0)]
FICHA = f"{REPO}/borradores/tecnica-toracocentesis/urgenciasen60-tecnica-toracocentesis-7.jpg"
SEG = [("anim", f"{E}/f_intro/%03d.jpg", 0, 4.5, 30), ("anim", f"{E}/f_eco/%03d.jpg", 4.5, 11.0, 30),
       ("still", f"{E}/s_rayos.jpg", 11.0, 17.0, 0), ("anim", f"{E}/f_corte/%03d.jpg", 17.0, 24.0, 40),
       ("still", f"{E}/s_marca.jpg", 24.0, 28.0, 0), ("anim", f"{E}/f_puncion/%03d.jpg", 28.0, 36.0, 30),
       ("still", f"{E}/s_cateter.jpg", 36.0, 44.0, 0), ("still", f"{E}/s_general.jpg", 44.0, 52.0, 0),
       ("still", f"{E}/s_cateter.jpg", 52.0, 55.0, 0), ("ficha", FICHA, 55.0, END, 0)]
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
        ins += ["-i", p]; tag = f"[v{j}]"; fcx.append(f"{last}[{j+1}:v]overlay=enable='between(t,{a:.3f},{b-0.034:.3f})'{tag}"); last = tag
    out = f"ovl_{k}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", cur]+ins+["-filter_complex", ";".join(fcx), "-map", last, "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", out], check=True); cur = out
subprocess.run(["python3", f"{REPO}/tools/musica.py", "musica.wav", str(END)], check=True, capture_output=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", cur, "-i", "musica.wav", "-filter_complex",
  f"[1:a]loudnorm=I=-16:TP=-1.5,afade=t=in:st=0:d=0.8,afade=t=out:st={END-2.5:.2f}:d=2.5[a]",
  "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(END), "urgenciasen60-tecnica-toracocentesis-video60.mp4"], check=True)
print("hecho", END)
