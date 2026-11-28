"""Reels de Cuenta atrás MIR, episodios 03 y 04: python3 tools/reel_mir_ep03_04.py <03|04> <dir_salida>
Formato: caso → «piensa» 3 s → respuesta. Sin voz: música y textos."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
MG = "#0E4A37"; THEME[MG] = (W, Y, "#DDEEE6", Y, K)
ROOT = os.path.dirname(HERE); sp = lambda h: f'<div style="height:{h}px"></div>'
def port(ep):
    p=os.path.join(ROOT,"borradores",f"mir-ep{ep}",f"urgenciasen60-mir-ep{ep}-1.jpg")
    if not os.path.exists(p): p=os.path.join(ROOT,f"mir-ep{ep}",f"urgenciasen60-mir-ep{ep}-1.jpg")
    return "file://"+p
PIENSA=(K, [big("PIENSA", 300, Y), txt("3 segundos", 80)], [(2, 3.0)])
def fin(ep): return (MG, [big("¿CUÁNTAS ACERTASTE?", 130, Y), f'<img src="{port(ep)}" style="width:440px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.5)">', txt("Solución justificada en el carrusel del perfil", 50)], [(3, 4.0)])
E={
"03":[
 (W, [kicker("CASO 5", G) + sp(20) + big("SANGRA A CHORRO", 120, R), txt("Moto · habla · TA 88/50 · herida pulsátil en el muslo", 56), txt("¿Intubas, torniquete o TC?", 60)], [(2, 2.8), (3, 3.0)]),
 PIENSA,
 (Y, [kicker("RESPUESTA") + sp(24) + big("TORNIQUETE", 190, R), txt("La x va antes que la A: primero se para la hemorragia exanguinante", 60)], [(1, 1.4), (2, 3.0)]),
 (W, [kicker("CASO 6", G) + sp(20) + big("FAST POSITIVO E INESTABLE", 110, R), txt("Colisión · TA 78/40 · líquido en Morison · no responde a fluidos", 56), txt("¿TC o quirófano?", 64)], [(2, 2.8), (3, 3.0)]),
 PIENSA,
 (Y, [kicker("RESPUESTA") + sp(24) + big("QUIRÓFANO", 210, R), txt("Control de daños, tranexámico, sangre pronto y poco cristaloide", 60)], [(1, 1.4), (2, 3.0)]),
 fin("03")],
"04":[
 (W, [kicker("CASO 7", G) + sp(20) + big("SIGUE HIPOTENSA", 130, R), txt("Sepsis urinaria · ya ha recibido fluidos · sin vía central", 56), txt("¿Esperas a la central?", 64)], [(2, 2.8), (3, 3.0)]),
 PIENSA,
 (Y, [kicker("RESPUESTA") + sp(24) + big("NORADRE&shy;NALINA YA", 170, R).replace("line-height:1.02","line-height:1.12"), txt("Por vía periférica, con antibiótico en la primera hora", 60)], [(1, 1.4), (2, 3.0)]),
 (W, [kicker("CASO 8", G) + sp(20) + big("PVC ALTA, POAP NORMAL", 116, R), txt("Operado de cadera · disnea brusca · gasto bajo", 56), txt("¿Qué tipo de shock es?", 64)], [(2, 2.8), (3, 3.0)]),
 PIENSA,
 (Y, [kicker("RESPUESTA") + sp(24) + big("OBSTRUCTIVO", 175, R), txt("TEP masivo: el problema está antes del ventrículo izquierdo", 60)], [(1, 1.4), (2, 3.0)]),
 fin("04")],
}
ep=sys.argv[1]; out=os.path.abspath(sys.argv[2])
print(build(E[ep], "MIR", out, f"urgenciasen60-mir-ep{ep}-reel-sinmusica.mp4", frames_only=(len(sys.argv) > 3)))
