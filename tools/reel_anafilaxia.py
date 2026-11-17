import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
T="ANAFILAXIA"; ROOT=os.path.dirname(HERE)
ficha="file://"+os.path.join(ROOT,"anafilaxia","urgenciasen60-anafilaxia-7.jpg")
S=[
 (Y,[big("ANAFILAXIA",210),big("¿QUÉ VA<br>PRIMERO?",190,R)],[(2,2.4)]),
 (R,[kicker("LO PRIMERO")+'<div style="height:30px"></div>'+big("ADRENALINA",195)+big("INTRA&shy;MUSCULAR",195,Y),txt("Antes que cualquier otro fármaco",72)],[(1,1.9),(2,1.9)]),
 (W,[kicker("DOSIS EN EL ADULTO",G)+'<div style="height:30px"></div>'+f'<div style="{A};font-size:200px;color:{R};white-space:nowrap">0,3–0,5 mg</div>',txt("Ampolla de 1 mg/ml",76)+'<div style="height:36px"></div>'+txt("Cara anterolateral del muslo",76)],[(1,1.5),(2,2.6)]),
 (Y,[big("¿NO MEJORA?",205),big("REPITE",330,R)+'<div style="height:20px"></div>'+txt("a los 5–15 minutos",92)],[(1,1.0),(2,2.4)]),
 (K,[big("CORTICOIDES Y ANTIHISTA&shy;MÍNICOS",150),big("DESPUÉS",265,Y)+'<div style="height:20px"></div>'+txt("Son segunda línea: nunca retrasan la adrenalina",68)],[(1,1.3),(2,2.9)]),
 (Y,[big("FICHA 01",130),f'<img src="{ficha}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.4)">',txt("Completa en el perfil. Guárdala.",50)],[(3,4.6)]),
]
out=sys.argv[1] if len(sys.argv)>1 else "out_reel"
print(build(S,T,out,"urgenciasen60-anafilaxia-reel.mp4",frames_only=(len(sys.argv)>2)))
