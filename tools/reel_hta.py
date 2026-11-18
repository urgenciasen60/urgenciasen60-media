import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
T="HTA EN URGENCIAS"; ROOT=os.path.dirname(HERE)
ficha="file://"+os.path.join(ROOT,"borradores","hta","urgenciasen60-hta-9.jpg")
sp=lambda h: f'<div style="height:{h}px"></div>'
S=[
 (Y,[big("¿220 DE<br>SISTÓLICA?",190),big("¿LO MANDAS A CASA?",120,R)],[(1,1.8),(2,2.4)]),
 (W,[kicker("PRIMERO",G)+sp(30)+big("¿HAY DAÑO?",210,R),txt("Cerebro · corazón · aorta",62)+sp(18)+txt("Riñón · ojo · embarazo",62,G)],[(1,1.6),(2,3.0)]),
 (R,[kicker("SI NO LO HAY")+sp(30)+big("NO CORRAS",230),txt("Bajarla rápido puede hacer daño",62,Y)+sp(18)+txt("Ajusta el oral y control en una semana",56)],[(1,1.6),(2,3.4)]),
 (K,[big("&lt; 1 %",300,Y),txt("de eventos a los 6 meses en asintomáticos",60)+sp(18)+txt("Mandarlos al hospital no lo mejora",56,Y)],[(1,1.6),(2,3.4)]),
 (Y,[kicker("¿CEFALEA?")+sp(30)+big("ANALGESIA<br>PRIMERO",190,R),txt("Casi siempre el dolor sube la PA, no al revés",58)],[(1,1.8),(2,3.0)]),
 (K,[big("FICHA 11",130,Y),f'<img src="{ficha}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Objetivos en cada emergencia. Guárdala.",50)],[(3,6.0)]),
]
out=sys.argv[1] if len(sys.argv)>1 else "out_reel"
print(build(S,T,out,"urgenciasen60-hta-reel-sinmusica.mp4",frames_only=(len(sys.argv)>2)))
