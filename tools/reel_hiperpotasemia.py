import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
T="HIPERPOTASEMIA"; ROOT=os.path.dirname(HERE)
ficha="file://"+os.path.join(ROOT,"hiperpotasemia","urgenciasen60-hiperpotasemia-7.jpg")
sp=lambda h: f'<div style="height:{h}px"></div>'
S=[
 (Y,[big("HIPERPOTA&shy;SEMIA",200),big("TRES PASOS,<br>EN ORDEN",170,R)],[(2,3.4)]),
 (R,[kicker("1 · PROTEGE")+sp(30)+f'<div style="{A};font-size:225px;white-space:nowrap">CALCIO IV</div>',txt("Gluconato cálcico al 10 %",72,Y)+sp(24)+txt("1 ampolla (10 ml)<br>en 2–3 minutos",72)],[(1,2.0),(2,3.0)]),
 (K,[big(f'EL CALCIO <span style="color:{Y}">NO</span> BAJA EL POTASIO',200),txt("Repite la dosis si persiste el ECG alterado",68)],[(1,2.2),(2,2.2)]),
 (W,[kicker("2 · DESPLAZA",G)+sp(30)+big("INSULINA",215,R)+big("+ GLUCOSA",185,R),txt("10 UI + 25–50 g de glucosa",72)+sp(30)+txt("Suma salbutamol nebulizado, 10–20 mg",64,G)],[(1,1.8),(2,3.4)]),
 (Y,[kicker("3 · ELIMINA")+sp(30)+big("SACA EL POTASIO",215,R),txt("Diurético de asa, captores digestivos o hemodiálisis",68)],[(1,1.6),(2,3.0)]),
 (K,[big("FICHA 02",130,Y),f'<img src="{ficha}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Completa en el perfil. Guárdala.",50)],[(3,6.0)]),
]
out=sys.argv[1] if len(sys.argv)>1 else "out_reel"
print(build(S,T,out,"urgenciasen60-hiperpotasemia-reel.mp4",frames_only=(len(sys.argv)>2)))
