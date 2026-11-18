import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
T="CRISIS DE ASMA"; ROOT=os.path.dirname(HERE)
ficha="file://"+os.path.join(ROOT,"asma","urgenciasen60-asma-7.jpg")
sp=lambda h: f'<div style="height:{h}px"></div>'
S=[
 (Y,[big("CRISIS DE ASMA",190),big("DECIDE EN<br>3 HORAS",170,R)],[(2,3.4)]),
 (W,[kicker("¿GRAVE? SIN PEF",G)+sp(30)+big("MIRA CÓMO HABLA",190,R),txt("Habla con palabras · FR &gt; 25 · FC &gt; 120 · SatO2 &lt; 90 %",62)],[(1,1.8),(2,3.0)]),
 (R,[kicker("1 · NEBULIZA")+sp(30)+f'<div style="{A};font-size:200px;white-space:nowrap">SALBUTAMOL</div>',txt("+ ipratropio + budesonida",72,Y)+sp(24)+txt("2,5–5 mg · 0,5 mg · 0,5 mg<br>cada 20 min, 1.ª hora",64)],[(1,2.0),(2,3.2)]),
 (K,[kicker("2 · CORTICOIDE")+sp(30)+big("PRONTO",230,Y),txt("Prednisona 50 mg oral o metilprednisolona IV",64)],[(1,1.8),(2,2.8)]),
 (Y,[kicker("3 · SI NO CEDE")+sp(30)+big("MAGNESIO IV",210,R),txt("2 g en 20 minutos, dosis única",66)+sp(24)+txt("Fracaso: VMNI sin retrasar la intubación",58)],[(1,1.6),(2,3.0)]),
 (K,[big("FICHA 03",130,Y),f'<img src="{ficha}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Completa en el perfil. Guárdala.",50)],[(3,6.0)]),
]
out=sys.argv[1] if len(sys.argv)>1 else "out_reel"
print(build(S,T,out,"urgenciasen60-asma-reel-sinmusica.mp4",frames_only=(len(sys.argv)>2)))
