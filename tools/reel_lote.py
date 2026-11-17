"""Reels del lote de noviembre: python3 tools/reel_lote.py <clave> <dir_salida> [frames]"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
ROOT=os.path.dirname(HERE)
sp=lambda h: f'<div style="height:{h}px"></div>'
def fin(carpeta,slug,sello):
    f="file://"+os.path.join(ROOT,"borradores",carpeta,f"urgenciasen60-{slug}-7.jpg")
    return (K,[big(sello,130,Y),f'<img src="{f}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Completa en el perfil. Guárdala.",50)],[(3,6.0)])
L={
"sepsis":("SEPSIS","urgenciasen60-sepsis-reel.mp4",[
 (Y,[big("SEPSIS",330),big("LA PRIMERA<br>HORA MANDA",170,R)],[(2,3.4)]),
 (R,[kicker("1 · ANTIBIÓTICO")+sp(30)+f'<div style="{A};font-size:230px;white-space:nowrap">EN 1 HORA</div>',txt("Si shock posible o sepsis probable",68,Y)+sp(24)+txt("Hasta 3 h si sepsis posible sin shock",60)],[(1,2.0),(2,3.0)]),
 (W,[kicker("2 · FLUIDOS",G)+sp(30)+big("30 ML/KG",250,R),txt("Cristaloide balanceado en 3 h si hay hipoperfusión",66)+sp(24)+txt("Reevalúa e individualiza",60,G)],[(1,1.8),(2,3.0)]),
 (K,[kicker("3 · VASOPRESOR")+sp(30)+big("NORADRE&shy;NALINA",200,Y),txt("Por vía periférica, sin esperar a la central",66)+sp(24)+txt("PAM 65 mmHg",72)],[(1,1.8),(2,3.0)]),
 (Y,[kicker("Y SIEMPRE")+sp(30)+big("CONTROLA EL FOCO",210,R),txt("Hemocultivos antes del antibiótico, sin retrasarlo",62)],[(1,1.6),(2,2.6)]),
 fin("sepsis","sepsis","FICHA 04")]),
"epistaxis":("EPISTAXIS","urgenciasen60-tecnica-epistaxis-reel.mp4",[
 (K,[kicker("TÉCNICA 01")+sp(20)+big("EPISTAXIS",250,Y),big("CINCO PASOS,<br>EN ORDEN",170)],[(2,3.2)]),
 (Y,[f'<div style="{A};font-size:420px;line-height:.9;color:{R}">1</div>'+big("COMPRIME",230),txt("Tercio inferior de la nariz, firme, 5 minutos o más",66)+sp(20)+txt("Sentado y con la cabeza hacia delante",58)],[(1,1.6),(2,3.0)]),
 (W,[f'<div style="{A};font-size:420px;line-height:.9;color:{R}">2</div>'+big("VASOCONS&shy;TRICTOR",190),txt("Algodón con anestésico local y vasoconstrictor, 5–10 min",64)],[(1,1.6),(2,2.6)]),
 (K,[f'<div style="{A};font-size:420px;line-height:.9;color:{Y}">3</div>'+big("BUSCA EL PUNTO",210),txt("Rinoscopia anterior con buena luz, sin coágulos",64)],[(1,1.6),(2,2.4)]),
 (R,[f'<div style="{A};font-size:420px;line-height:.9;color:{Y}">4</div>'+big("CAUTERIZA",230),txt("Nitrato de plata solo en el punto. Nunca los dos lados del tabique",62)],[(1,1.6),(2,2.8)]),
 (Y,[f'<div style="{A};font-size:420px;line-height:.9;color:{R}">5</div>'+big("TAPONA",260),txt("Si persiste o no ves el punto. Reabsorbible si toma antitrombóticos",62)],[(1,1.6),(2,2.8)]),
 fin("tecnica-epistaxis","tecnica-epistaxis","TÉCNICA 01")]),
"pl":("PUNCIÓN LUMBAR","urgenciasen60-tecnica-puncion-lumbar-reel.mp4",[
 (K,[kicker("TÉCNICA 02")+sp(20)+big("PUNCIÓN LUMBAR",215,Y),big("ANTES DE<br>PINCHAR",170)],[(2,3.2)]),
 (R,[big("¿TC PRIMERO?",230),txt("Bajo nivel de consciencia, focalidad o papiledema",62,Y)+sp(22)+txt("Crisis reciente, inmunodepresión, 60 años o más",58)],[(1,1.8),(2,3.2)]),
 (W,[kicker("REFERENCIA",G)+sp(30)+big("L3–L4<br>O L4–L5",250,R),txt("La línea entre las crestas ilíacas cruza la apófisis de L4",62)],[(1,1.8),(2,3.0)]),
 (Y,[kicker("POSICIÓN")+sp(30)+big("FLEXIÓN MÁXIMA",220,R),txt("Decúbito lateral, rodillas al pecho, sin rotar hombros ni caderas",62)],[(1,1.6),(2,3.0)]),
 (K,[kicker("AGUJA")+sp(30)+big("LÍNEA MEDIA, AL OMBLIGO",190,Y),txt("Avanza despacio. Fiador puesto al avanzar y al retirar",62)],[(1,1.6),(2,3.0)]),
 fin("tecnica-puncion-lumbar","tecnica-puncion-lumbar","TÉCNICA 02")]),
}
k=sys.argv[1]; tema,name,S=L[k]
print(build(S,tema,os.path.abspath(sys.argv[2]),name,frames_only=(len(sys.argv)>3)))
