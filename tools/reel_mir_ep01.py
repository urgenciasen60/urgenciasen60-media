"""Reel de la serie Cuenta atrás MIR, episodio 01 (ECG): python3 tools/reel_mir_ep01.py <dir_salida>
Formato: caso → «piensa» 3 s → respuesta. Verde de la serie MIR; logo y amarillo del canal."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
MG = "#0E4A37"
THEME[MG] = (W, Y, "#DDEEE6", Y, K)   # verde de la serie MIR
ROOT = os.path.dirname(HERE)
sp = lambda h: f'<div style="height:{h}px"></div>'
portada = "file://" + os.path.join(ROOT, "mir-ep01", "urgenciasen60-mir-ep01-1.jpg")
S = [
 (MG, [kicker("CUENTA ATRÁS MIR · EP. 01", Y) + sp(24) + big("2 CASOS<br>DE ECG", 230), txt("Pausa el vídeo si necesitas pensar", 64, Y)], [(2, 3.0)]),
 (W, [kicker("CASO 1", G) + sp(24) + big("SÍNCOPE<br>FC 34", 220, R), txt("78 años · TA 90/55 · P a 80 y QRS anchos a 34, sin relación", 62) + sp(24) + txt("¿Alta con Holter o marcapasos?", 66)], [(1, 1.6), (2, 3.0)]),
 (K, [big("PIENSA", 300, Y), txt("3 segundos", 80)], [(2, 3.0)]),
 (Y, [kicker("RESPUESTA") + sp(24) + big("MARCA&shy;PASOS", 230, R), txt("BAV completo inestable: atropina como puente, marcapasos transcutáneo y definitivo", 62)], [(1, 1.4), (2, 3.0)]),
 (W, [kicker("CASO 2", G) + sp(24) + big("QRS ESTRECHO<br>A 180", 200, R), txt("28 años · palpitaciones bruscas · estable", 62) + sp(24) + txt("¿Cardioversión o vagales?", 66)], [(1, 1.6), (2, 2.8)]),
 (K, [big("PIENSA", 300, Y), txt("3 segundos", 80)], [(2, 3.0)]),
 (Y, [kicker("RESPUESTA") + sp(24) + big("VAGALES", 270, R), txt("Valsalva modificada. Si no cede, adenosina", 64)], [(1, 1.4), (2, 2.6)]),
 (MG, [big("¿CUÁNTAS ACERTASTE?", 130, Y), f'<img src="{portada}" style="width:440px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.5)">', txt("Solución justificada en el carrusel del perfil", 50)], [(3, 4.5)]),
]
out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "out_reel")
print(build(S, "MIR", out, "urgenciasen60-mir-ep01-reel-sinmusica.mp4", frames_only=(len(sys.argv) > 2)))
