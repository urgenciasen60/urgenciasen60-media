"""Reel de la serie Cuenta atrás MIR, episodio 02 (abdomen agudo): python3 tools/reel_mir_ep02.py <dir_salida>
Formato: caso → «piensa» 3 s → respuesta. Verde de la serie MIR; logo y amarillo del canal."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
MG = "#0E4A37"
THEME[MG] = (W, Y, "#DDEEE6", Y, K)   # verde de la serie MIR
ROOT = os.path.dirname(HERE)
sp = lambda h: f'<div style="height:{h}px"></div>'
portada = "file://" + os.path.join(ROOT, "mir-ep02", "urgenciasen60-mir-ep02-1.jpg")
rx = "file://" + os.path.join(ROOT, "mir-ep02", "assets", "rx_real.jpg")
tc = "file://" + os.path.join(ROOT, "mir-ep02", "assets", "tc_real.jpg")
im = lambda s, h: f'<img src="{s}" style="width:900px;height:{h}px;object-fit:cover;display:block"><div style="font-size:22px;color:#4A4A4A;margin-top:6px">Imagen real · CC BY 4.0</div>'
S = [
 (MG, [kicker("CUENTA ATRÁS MIR · EP. 02", Y) + sp(24) + big("2 CASOS DE<br>ABDOMEN<br>AGUDO", 200), txt("Pausa el vídeo si necesitas pensar", 64, Y)], [(2, 3.0)]),
 (W, [kicker("CASO 3", G) + sp(20) + big("ABDOMEN EN TABLA", 110, R), txt("58 años · ibuprofeno · dolor epigástrico «en puñalada»", 54) + sp(20) + im(rx, 230), txt("¿Conservador o quirófano?", 58)], [(2, 2.0), (4, 3.0)]),
 (K, [big("PIENSA", 300, Y), txt("3 segundos", 80)], [(2, 3.0)]),
 (Y, [kicker("RESPUESTA") + sp(24) + big("CIRUGÍA<br>URGENTE", 220, R), txt("Peritonitis + aire libre = perforación. Fluidos, IBP IV y antibiótico, y al quirófano", 60)], [(1, 1.4), (2, 3.0)]),
 (W, [kicker("CASO 4", G) + sp(20) + big("DUELE MUCHO,<br>ABDOMEN BLANDO", 118, R), txt("81 años · FA sin anticoagular · gas portal en la TC", 54) + sp(20) + im(tc, 297), txt("¿Benigno o necrosis?", 64)], [(2, 2.0), (4, 3.0)]),
 (K, [big("PIENSA", 300, Y), txt("3 segundos", 80)], [(2, 3.0)]),
 (Y, [kicker("RESPUESTA") + sp(24) + big("ISQUEMIA<br>MESEN&shy;TÉRICA", 168, R).replace("line-height:1.02","line-height:1.12"), txt("Embolia de la AMS con necrosis: heparina IV, revascularización y laparotomía", 60)], [(1, 1.4), (2, 2.8)]),
 (MG, [big("¿CUÁNTAS ACERTASTE?", 130, Y), f'<img src="{portada}" style="width:440px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.5)">', txt("Solución justificada en el carrusel del perfil", 50)], [(3, 4.5)]),
]
out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "out_reel")
print(build(S, "MIR", out, "urgenciasen60-mir-ep02-reel-sinmusica.mp4", frames_only=(len(sys.argv) > 2)))
