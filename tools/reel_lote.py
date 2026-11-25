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
 (K,[kicker("TÉCNICA 02")+sp(20)+big("EPISTAXIS",250,Y),big("CINCO PASOS,<br>EN ORDEN",170)],[(2,3.2)]),
 (Y,[f'<div style="{A};font-size:420px;line-height:.9;color:{R}">1</div>'+big("COMPRIME",230),txt("Tercio inferior de la nariz, firme, 5 minutos o más",66)+sp(20)+txt("Sentado y con la cabeza hacia delante",58)],[(1,1.6),(2,3.0)]),
 (W,[f'<div style="{A};font-size:420px;line-height:.9;color:{R}">2</div>'+big("VASOCONS&shy;TRICTOR",190),txt("Algodón con anestésico local y vasoconstrictor, 5–10 min",64)],[(1,1.6),(2,2.6)]),
 (K,[f'<div style="{A};font-size:420px;line-height:.9;color:{Y}">3</div>'+big("BUSCA EL PUNTO",210),txt("Rinoscopia anterior con buena luz, sin coágulos",64)],[(1,1.6),(2,2.4)]),
 (R,[f'<div style="{A};font-size:420px;line-height:.9;color:{Y}">4</div>'+big("CAUTERIZA",230),txt("Nitrato de plata solo en el punto. Nunca los dos lados del tabique",62)],[(1,1.6),(2,2.8)]),
 (Y,[f'<div style="{A};font-size:420px;line-height:.9;color:{R}">5</div>'+big("TAPONA",260),txt("Si persiste o no ves el punto. Reabsorbible si toma antitrombóticos",62)],[(1,1.6),(2,2.8)]),
 fin("tecnica-epistaxis","tecnica-epistaxis","TÉCNICA 02")]),
"pl":("PUNCIÓN LUMBAR","urgenciasen60-tecnica-puncion-lumbar-reel.mp4",[   # rehecho 25/11: solo técnica, gancho al vídeo y al carrusel
 (K,[kicker("TÉCNICA 01")+sp(20)+big("PUNCIÓN LUMBAR",215,Y),big("PASO A<br>PASO",190)],[(2,3.2)]),
 (Y,[kicker("POSICIÓN")+sp(30)+big("TODO EMPIEZA AQUÍ",200,R),txt("Decúbito lateral, en flexión, con la espalda en el borde",62)],[(1,1.6),(2,3.0)]),
 (W,[kicker("REFERENCIA",G)+sp(30)+big("BUSCA LAS CRESTAS",210,R),txt("La línea que las une te dice dónde pinchar",62)],[(1,1.8),(2,3.0)]),
 (R,[kicker("AGUJA")+sp(30)+big("LÍNEA MEDIA",230),txt("Despacio, hasta notar el resalte",62,Y)],[(1,1.6),(2,3.0)]),
 (K,[kicker("Y AL FINAL")+sp(30)+big("¿SALE LCR?",230,Y),txt("Qué hacer antes de retirar la aguja, en el vídeo",62)],[(1,1.6),(2,3.0)]),
 (K,[big("TÉCNICA 01",130,Y),f'<img src="file://{os.path.join(ROOT,"tecnica-puncion-lumbar","urgenciasen60-tecnica-puncion-lumbar-7.jpg")}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Vídeo y carrusel en el perfil",50)],[(3,6.0)])]),
"tora":("TORACOCENTESIS","urgenciasen60-tecnica-toracocentesis-reel.mp4",[   # 25/11: gancho al vídeo y al carrusel (regla del 22/11)
 (K,[kicker("TÉCNICA 03")+sp(20)+big("TORACOCENTESIS",140,Y),big("PASO A<br>PASO",190)],[(2,3.2)]),
 (Y,[kicker("ANTES DE PINCHAR")+sp(30)+big("ECO PRIMERO",215,R),txt("Marca el punto en la misma posición en la que vas a pinchar",62)],[(1,1.6),(2,3.0)]),
 (W,[kicker("DÓNDE",G)+sp(30)+big("ENCIMA DE LA COSTILLA",180,R),txt("Por debajo de cada costilla va el paquete vasculonervioso",62)],[(1,1.8),(2,3.0)]),
 (R,[kicker("Y SOBRE TODO")+sp(30)+big("SABER PARAR",220),txt("Cuándo y cuánto, en el carrusel",62,Y)],[(1,1.6),(2,3.0)]),
 (K,[big("TÉCNICA 03",130,Y),f'<img src="file://{os.path.join(ROOT,"borradores","tecnica-toracocentesis","urgenciasen60-tecnica-toracocentesis-7.jpg")}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Vídeo y carrusel en el perfil",50)],[(3,6.0)])]),
}
k=sys.argv[1]; tema,name,S=L[k]
print(build(S,tema,os.path.abspath(sys.argv[2]),name,frames_only=(len(sys.argv)>3)))
