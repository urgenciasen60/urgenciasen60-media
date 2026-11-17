import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
T="ANAFILAXIA"; ROOT=os.path.dirname(HERE)
ficha="file://"+os.path.join(ROOT,"anafilaxia","urgenciasen60-anafilaxia-7.jpg")
S=[]
def scene(bg,blocks,durs):
    for i,d in enumerate(durs): S.append((html(bg,blocks,i+1,T),d))
scene(Y,[big("ANAFILAXIA",200),big("¿QUÉ VA<br>PRIMERO?",170)],[0.8,1.9])
scene(W,[kicker("LO PRIMERO"),big("ADRENALINA",200,R)+big("INTRAMUSCULAR",150,R),txt("Antes que cualquier otro fármaco")],[0.7,1.4,1.9])
scene(W,[kicker("DOSIS EN EL ADULTO"),f'<div style="{A};font-size:215px;color:{R};white-space:nowrap">0,3–0,5 mg</div>',txt("Ampolla de 1 mg/ml"),txt("Cara anterolateral del muslo")],[0.6,1.5,1.3,1.9])
scene(W,[big("¿NO MEJORA?",200),big("REPITE",260,R),txt("a los 5–15 minutos",84)],[0.9,1.0,1.8])
scene(W,[big("CORTICOIDES Y ANTIHISTA&shy;MÍNICOS",130),big("DESPUÉS",250,R),txt("Son segunda línea: nunca retrasan la adrenalina")],[1.3,1.1,2.2])
scene(Y,[big("FICHA 01",110),f'<img src="{ficha}" style="width:580px;display:block;box-shadow:0 20px 60px rgba(0,0,0,.35)">',txt("Completa en el perfil. Guárdala.",56)],[0.6,2.6,2.4])
out=sys.argv[1] if len(sys.argv)>1 else "out_reel"
print(build(S,out,"urgenciasen60-anafilaxia-reel.mp4",frames_only=(len(sys.argv)>2)), sum(d for _,d in S))
