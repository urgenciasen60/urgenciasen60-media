"""Carrusel de Cuenta atrás MIR · Ep. 02 (abdomen agudo): python3 tools/mir_ep02.py <dir_salida>
Mismo diseño que el ep. 01: portada verde quirófano, interiores blancos, amarillo para la respuesta, JPG 1080x1350.
Imágenes reales con licencia CC BY 4.0 (en mir-ep02/assets/): Rx de Baker J, Patane J, Chandwani C. JETEM 2016 (recortada y con ajuste de contraste);
TC de Florim S, Almeida A, Rocha D, Portugal P. Insights Imaging 2018;9:673-82, fig. 5 (sin cambios salvo el tamaño)."""
import os, sys, subprocess
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FONT = os.path.join(HERE, "fonts", "anton-latin-400-normal.woff2")
MG = "#0E4A37"; Y = "#FFD60A"; K = "#111111"; R = "#D7141A"; G = "#4A4A4A"; W = "#FFFFFF"
A = "font-family:Anton,sans-serif;line-height:1.04"
AS = os.path.join(ROOT, "mir-ep02", "assets")
LOGO = "file://" + os.path.join(AS, "logo.png")
RX = "file://" + os.path.join(AS, "rx_real.jpg")
TC = "file://" + os.path.join(AS, "tc_real.jpg")

def page(body, right, foot, green=False):
    bg = MG if green else W; fg = W if green else K
    tagbg, tagfg = (Y, K) if green else (MG, W)
    strip = "" if green else f'<div style="height:22px;background:{MG}"></div>'
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>@font-face{{font-family:Anton;src:url("file://{FONT}") format("woff2")}}body{{margin:0}}b{{font-weight:800}}</style></head><body>
<div style="width:1080px;height:1350px;box-sizing:border-box;display:flex;flex-direction:column;background:{bg};color:{fg};font-family:Inter,sans-serif">
{strip}<div style="display:flex;justify-content:space-between;align-items:center;padding:{'64' if green else '42'}px 80px 0 80px">
<div style="background:{tagbg};color:{tagfg};padding:12px 22px;border-radius:4px;font-size:25px;font-weight:800;letter-spacing:2px">URGENCIAS EN 60 · MIR</div>
<div style="{A};font-size:34px">{right}</div></div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:26px;padding:0 80px">{body}</div>
<div style="height:96px;background:{K};display:flex;justify-content:space-between;align-items:center;padding:0 80px;font-size:28px;font-weight:800"><div style="color:{Y};font-size:32px">@urgenciasen60</div><div style="color:{W}">{foot}</div></div>
</div></body></html>'''

def opts(items, fs=30):
    return "".join(f'<div style="border:3px solid {K};display:flex;align-items:center;gap:26px;padding:14px 22px;margin-top:-10px"><div style="{A};font-size:40px;width:24px">{l}</div><div style="font-size:{fs}px;font-weight:500;line-height:1.25">{t}</div></div>' for l, t in items)

def img(src, h, credit):
    return f'<div><div style="background:#000;display:flex;justify-content:center"><img src="{src}" style="height:{h}px;display:block"></div><div style="font-size:17px;color:{G};margin-top:6px">{credit}</div></div>'

def sol(letter, title, text, why, perla):
    w = "".join(f'<div style="display:flex;gap:22px;align-items:baseline"><div style="{A};font-size:32px;color:{R};width:22px">{l}</div><div style="font-size:28px;line-height:1.35">{t}</div></div>' for l, t in why)
    return f'''<div style="display:flex;gap:26px;align-items:center"><div style="background:{Y};{A};font-size:96px;padding:6px 18px">{letter}</div><div style="{A};font-size:46px">{title}</div></div>
<div style="font-size:30px;line-height:1.42">{text}</div>
<div style="{A};font-size:40px;color:{MG}">POR QUÉ NO LAS DEMÁS</div><div style="display:flex;flex-direction:column;gap:16px;margin-top:-12px">{w}</div>
<div style="background:{Y};padding:20px 26px;font-size:28px;line-height:1.38"><b>Perla:</b> {perla}</div>'''

P = []
# 1 · Portada
P.append(page(f'''<div style="display:flex;gap:26px;align-items:center"><img src="{LOGO}" style="width:150px;height:150px">
<div style="border:5px solid {Y};padding:12px 24px"><div style="color:{Y};font-size:26px;font-weight:800;letter-spacing:4px">FALTAN</div><div style="{A};font-size:64px">59 DÍAS</div></div></div>
<div style="{A};font-size:200px;line-height:.98">2 CASOS<br>MIR</div>
<div style="{A};font-size:66px">ABDOMEN AGUDO: <span style="color:{Y}">¿LO VES EN 60 S?</span></div>
<div style="font-size:34px;font-weight:500;margin-top:-6px">Perforación e isquemia mesentérica · ¿Cuántos aciertas?</div>''',
 "EP. 02 · CASOS 03-04", "Responde y desliza →", green=True))
# 2 · Caso 3
P.append(page(f'''<div style="font-size:28px;line-height:1.36">Varón de 58 años, fumador, que toma <b>ibuprofeno</b> desde hace 3 semanas por una lumbalgia. <b>Dolor epigástrico brusco, «en puñalada»</b>, de 4 h, ya difuso. <b>TA 105/65, FC 112, T 37,8 °C. Abdomen en tabla</b>, sin ruidos. Rx de tórax portátil, sentado:</div>
{img(RX, 360, "Imagen real: Baker J, Patane J, Chandwani C. JETEM 2016 · CC BY 4.0 · recortada")}
<div style="{A};font-size:40px">¿ACTITUD MÁS ADECUADA?</div>
{opts([("A", "SNG, IBP IV, tratamiento conservador y TC de control a las 24 h"), ("B", "Dieta absoluta, fluidos, IBP IV, antibiótico de amplio espectro y cirugía urgente"), ("C", "Gastroscopia urgente para localizar y cerrar la perforación"), ("D", "Repetir la Rx en decúbito lateral antes de avisar a Cirugía")], 26)}''',
 "CASO 3 · 2/7", "Comenta A, B, C o D y desliza →"))
# 3 · Pausa
P.append(page(f'''<img src="{LOGO}" style="width:110px;height:110px">
<div style="{A};font-size:190px;line-height:.98">¿A, B, C<br>O D?</div>
<div style="{A};font-size:58px">ESCRÍBELO EN COMENTARIOS <span style="color:{Y}">ANTES DE DESLIZAR</span></div>
<div style="font-size:32px;font-weight:500">Sin trampas: la solución está en la siguiente.</div>''', "EP. 02", "3/7 · Desliza →", green=True))
# 4 · Solución 3
P.append(page(sol("B", "PERITONITIS + AIRE LIBRE:<br>CIRUGÍA URGENTE",
 "Dolor brusco, abdomen en tabla y <b>neumoperitoneo</b>: perforación de víscera hueca, probablemente <b>úlcera péptica por AINE</b>. Con esa clínica, el aire libre basta para operar (sutura con <b>parche de epiplón</b>, por laparoscopia si está estable). Desde Urgencias: dieta absoluta, fluidos, IBP IV y antibiótico. Después, retirar el AINE y erradicar <i>H. pylori</i> si lo hay.",
 [("A", "El manejo conservador no es de rutina: solo en casos muy seleccionados, estables, sin peritonitis y con la perforación sellada en el estudio con contraste."),
  ("C", "Se desaconseja el cierre endoscópico de la úlcera perforada: el tejido es fibrótico y los clips no funcionan."),
  ("D", "El diagnóstico ya está hecho; repetir pruebas solo retrasa la cirugía.")],
 "la Rx solo muestra el aire libre en el 50-75 % de los casos. Si es normal y la sospecha persiste, pide una TC."),
 "SOLUCIÓN 3 · 4/7", "Desliza →"))
# 5 · Caso 4
P.append(page(f'''<div style="font-size:28px;line-height:1.36">Mujer de 81 años con <b>FA permanente</b>; dejó el anticoagulante hace 10 días por una extracción dental. <b>Dolor periumbilical muy intenso</b> de 6 h que no cede con metamizol y una deposición diarreica. <b>Abdomen blando, apenas doloroso.</b> Lactato 4,8 mmol/l. TC con contraste:</div>
{img(TC, 304, "Imagen real: Florim S, et al. Insights Imaging 2018;9:673-82, fig. 5 · CC BY 4.0")}
<div style="{A};font-size:40px">¿QUÉ AFIRMACIÓN ES CORRECTA?</div>
{opts([("A", "El gas portal suele ser benigno: anticoagular y observar"), ("B", "Isquemia mesentérica embólica con necrosis: heparina IV, revascularización y laparotomía urgente"), ("C", "Con un lactato normal se habría descartado la isquemia"), ("D", "Es una colitis isquémica: dieta, fluidos y colonoscopia a las 48 h")], 26)}''',
 "CASO 4 · 5/7", "Comenta A, B, C o D y desliza →"))
# 6 · Solución 4
P.append(page(sol("B", "DOLOR DESPROPORCIONADO + FA:<br>ISQUEMIA MESENTÉRICA",
 "FA sin anticoagular, dolor brusco que no cuadra con la exploración y vaciamiento intestinal: <b>embolia de la AMS</b>. La TC muestra <b>gas portal</b> hasta la periferia del hígado (a) y asas dilatadas de <b>pared fina</b>, con neumatosis y gas en venas mesentéricas (b): infarto transmural. <b>Heparina IV</b> en cuanto se diagnostica, revascularización (embolectomía o endovascular) y laparotomía para resecar el intestino no viable, con segunda revisión si la viabilidad es dudosa.",
 [("A", "La neumatosis aislada puede ser benigna, pero el gas portal sugiere con fuerza infarto intestinal, y más con la AMS ocluida."),
  ("C", "Ningún análisis descarta la isquemia: un lactato normal no la excluye. La angio-TC se hace aunque haya fracaso renal."),
  ("D", "La colitis isquémica afecta al colon, suele dar dolor leve con rectorragia y no ocluye la AMS.")],
 "el gas portal llega a la <b>periferia</b> del hígado; la aerobilia se queda en el <b>centro</b>, junto al hilio."),
 "SOLUCIÓN 4 · 6/7", "Desliza →"))
# 7 · Clave MIR
card = lambda t, x: f'<div style="background:{W};color:{K};padding:24px 26px;flex:1"><div style="{A};font-size:38px;margin-bottom:12px">{t}</div><div style="font-size:28px;line-height:1.38">{x}</div></div>'
P.append(page(f'''<div style="{A};font-size:92px;line-height:1">PRIMERO:<br><span style="color:{Y}">¿TABLA O BLANDO?</span></div>
<div style="font-size:32px;font-weight:500;line-height:1.4">La exploración orienta antes que cualquier prueba: abdomen en tabla con aire libre, o dolor brutal con un abdomen blando.</div>
<div style="display:flex;gap:24px">{card("ABDOMEN EN TABLA", "Perforación: <b>cirugía urgente</b>. Si la Rx es normal y la sospecha persiste, <b>TC</b>.")}{card("BLANDO, PERO DUELE MUCHO", "Isquemia mesentérica: <b>angio-TC ya</b>, sin esperar al lactato ni a la creatinina.")}</div>
<div style="background:{Y};color:{K};padding:22px 26px;font-size:29px;line-height:1.4"><b>Neumatosis + gas portal en una isquemia = necrosis.</b> Gas portal en la periferia del hígado; aerobilia en el centro.</div>
<div style="font-size:19px;line-height:1.4;color:#CFE3D9">Fuentes: guías WSES de úlcera péptica perforada y sangrante (Tarasconi et al., 2020) y de isquemia mesentérica aguda (Bala et al., 2022). Imágenes reales: Baker et al., JETEM 2016, y Florim et al., Insights Imaging 2018 (CC BY 4.0). Contenido formativo; no sustituye a los protocolos de tu centro.</div>''',
 "CLAVE MIR · 7/7", "Guárdalo para el repaso", green=True))

def render(pages, outdir, slug):
    os.makedirs(outdir, exist_ok=True); out = []
    for i, h in enumerate(pages, 1):
        hp = os.path.join(outdir, f"{i}.html"); open(hp, "w").write(h)
        png = os.path.join(outdir, f"{slug}-{i}.png")
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--window-size=1080,1350",
                        f"--screenshot={png}", "--virtual-time-budget=3000", "file://" + hp], capture_output=True)
        jpg = png[:-4] + ".jpg"; Image.open(png).convert("RGB").save(jpg, quality=95, subsampling=0); os.remove(png); os.remove(hp); out.append(jpg)
    sh = Image.new("RGB", (4 * 550 + 10, 2 * 685 + 10), "#888888")
    for i, f in enumerate(out): sh.paste(Image.open(f).resize((540, 675)), (10 + (i % 4) * 550, 10 + (i // 4) * 685))
    sh.save(os.path.join(outdir, "_sheet.jpg"), quality=85); return out

if __name__ == "__main__":
    o = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "out_mir_ep02")
    print(render(P, o, "urgenciasen60-mir-ep02"))
