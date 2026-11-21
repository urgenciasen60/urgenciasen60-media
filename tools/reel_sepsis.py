import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
ROOT=os.path.dirname(HERE); T="SEPSIS"
ficha="file://"+os.path.join(ROOT,"sepsis","urgenciasen60-sepsis-7.jpg")
sp=lambda h: f'<div style="height:{h}px"></div>'
S=[
 (Y,[big("SEPSIS",300),big("LA PRIMERA<br>HORA MANDA",160,R)],[(2,3.2)]),
 (R,[kicker("1 · ANTIBIÓTICO")+sp(30)+f'<div style="{A};font-size:220px;white-space:nowrap">EN 1 HORA</div>',txt("Sin foco: ceftriaxona",64,Y)+sp(20)+txt("Shock: meropenem + vancomicina",60)],[(1,1.8),(2,3.4)]),
 (W,[kicker("2 · FLUIDOS",G)+sp(30)+big("30 ML/KG",240,R),txt("Ringer lactato en 3 h si hay hipoperfusión",64)+sp(20)+txt("Reevalúa e individualiza",58,G)],[(1,1.8),(2,3.0)]),
 (K,[kicker("3 · NORADRENALINA")+sp(30)+big("0,05–0,15",220,Y),txt("µg/kg/min, también por vía periférica",62)+sp(20)+txt("Objetivo: PAM 65 mmHg",64,Y)],[(1,1.8),(2,3.2)]),
 (Y,[kicker("Y SIEMPRE")+sp(30)+big("CONTROLA EL FOCO",200,R),txt("Hemocultivos antes del antibiótico, sin retrasarlo",60)+sp(20)+txt("Si no responde: avisa a UCI",60)],[(1,1.6),(2,3.0)]),
 (K,[big("FICHA 06",130,Y),f'<img src="{ficha}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Con dosis. Guárdala.",50)],[(3,6.0)]),
]
out=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else "out_reel")
print(build(S,T,out,"urgenciasen60-sepsis-reel-sinmusica.mp4",frames_only=(len(sys.argv)>2)))
