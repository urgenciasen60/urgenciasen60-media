import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
ROOT=os.path.dirname(HERE); BL="#0B4F9E"
sp=lambda h: f'<div style="height:{h}px"></div>'
portada="file://"+os.path.join(ROOT,"borradores","guia-01-sepsis","urgenciasen60-guia-sepsis-2026-1.jpg")
S=[
 (BL,[kicker("GUÍA 01")+sp(10)+big("SEPSIS<br>2026",270),big("LA GUÍA<br>DE URGENCIAS",125,Y)],[2]),
 (W,[kicker("LA FUENTE",G)+sp(20)+big("GT-<br>LATINFURG",230,BL),txt("INFURG-SEMES · Emergencias 2026",60)],[1,2]),
 (BL,[kicker("1 · DETECTA")+sp(20)+big("DESDE EL<br>TRIAJE",230,Y),txt("Escalas sencillas que activan el código sepsis",62)],[1,2]),
 (K,[kicker("2 · EL TIEMPO MANDA")+sp(20)+big("PRIMERA<br>HORA",230,Y),txt("Lactato, cultivos y antibiótico",62)+sp(16)+txt("Elige el antibiótico según el foco",60,Y)],[1,2]),
 (BL,[kicker("3 · REANIMA")+sp(20)+big("FLUIDOS Y<br>NORADRE&shy;NALINA",200,Y),txt("Sin esperar a la vía central, con un objetivo claro",62)],[1,2]),
 (W,[kicker("4 · SI NO RESPONDE",G)+sp(20)+big("AVISA A UCI<br>Y CONTROLA<br>EL FOCO",190,BL)],[1,2]),
 (BL,[kicker("EVITA")+sp(20)+big("CINCO<br>ERRORES",250,Y),txt("Los que más se repiten en la guardia",62)],[1,2]),
 (K,[big("GUÍA 01",130,Y),f'<img src="{portada}" style="width:500px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Guárdalo.",50)],[3]),
]
import wave
VOZ=os.environ.get("VOZ","/tmp/loc")
def dur(i):
    with wave.open(os.path.join(VOZ,f"e{i}.wav")) as w: return w.getnframes()/w.getframerate()
PAD=0.6; XF=0.5
S2=[]; starts=[]; t=0.0
for i,(bg,bl,pasos) in enumerate(S):
    D=dur(i)+PAD+(0.6 if i==len(S)-1 else 0); f=min(2.5,D*0.3)
    st=[(pasos[0],f)] if len(pasos)==1 and False else None
    if len(pasos)==1: steps=[(pasos[0],D)]
    else: steps=[(n,f) for n in pasos[:-1]]+[(pasos[-1],D-f*(len(pasos)-1))]
    S2.append((bg,bl,steps)); starts.append(t); t+=D-XF
S=S2
out=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else "out_reel")
print(build(S,"GUÍA 01 · SEPSIS",out,"urgenciasen60-guia-sepsis-reel-sinmusica.mp4",frames_only=(len(sys.argv)>2),xf=XF))
open(os.path.join(out,"inicios.txt"),"w").write("\n".join(f"{a+0.45:.2f}" for a in starts))
