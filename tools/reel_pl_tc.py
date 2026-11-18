import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
T="PUNCIÓN LUMBAR"; ROOT=os.path.dirname(HERE)
ficha="file://"+os.path.join(ROOT,"puncion-lumbar-indicaciones","urgenciasen60-pl-tc-antes-7.jpg")
sp=lambda h: f'<div style="height:{h}px"></div>'
S=[
 (Y,[big("PUNCIÓN LUMBAR",200),big("¿SÍ O NO?",190,R)],[(2,3.4)]),
 (W,[kicker("1 · ¿TC ANTES?",G)+sp(30)+big("SOLO SI…",210,R),txt("GCS &lt; 15 · focalidad · papiledema",62)+sp(22)+txt("Crisis &lt; 1 semana · inmunodepresión · lesión previa del SNC",58)],[(1,1.8),(2,3.4)]),
 (R,[kicker("2 · SI SE RETRASA")+sp(30)+f'<div style="{A};font-size:180px;line-height:1">EL ANTIBIÓTICO NO ESPERA</div>',txt("Hemocultivos y antibiótico antes de la TC",64)],[(1,2.2),(2,2.8)]),
 (K,[kicker("3 · CONTRAINDICACIONES")+sp(30)+big("NO PINCHES",200,Y),txt("Infección local · efecto masa",62)+sp(22)+txt("Plaquetas &lt; 50.000/µl · INR ≥ 1,5",62)],[(1,1.8),(2,3.2)]),
 (Y,[kicker("4 · ¿MENINGITIS?")+sp(30)+big("ES URGENTE",210,R),txt("Antiagregado: pincha sin esperar",62)+sp(22)+txt("Anticoagulado: antibiótico ya y Hematología",58)],[(1,1.8),(2,3.2)]),
 (K,[big("FICHA 04",130,Y),f'<img src="{ficha}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Completa en el perfil. Guárdala.",50)],[(3,6.0)]),
]
out=sys.argv[1] if len(sys.argv)>1 else "out_reel"
print(build(S,T,out,"urgenciasen60-pl-indicaciones-reel-sinmusica.mp4",frames_only=(len(sys.argv)>2)))
