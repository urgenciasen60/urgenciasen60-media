import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
ROOT=os.path.dirname(HERE); BL="#0B4F9E"
sp=lambda h: f'<div style="height:{h}px"></div>'
ficha="file://"+os.path.join(ROOT,"borradores","guia-01-sepsis","urgenciasen60-guia-sepsis-2026-11.jpg")
S=[
 (BL,[kicker("GUÍA 01")+sp(10)+big("SEPSIS<br>2026",300),big("PASO A PASO<br>EN TU GUARDIA",140,Y)],[2]),
 (W,[kicker("1 · DETECTA",G)+sp(20)+big("CÓDIGO<br>SEPSIS",230,BL),txt("Infección + qSOFA ≥ 2, SIRS ≥ 2 o NEWS-2 ≥ 5",62)+sp(16)+txt("El qSOFA solo no basta",58,G)],[1,2]),
 (BL,[kicker("LAS ESCALAS")+sp(20)+big("QSOFA",200,Y),txt("FR ≥ 22 · PAS ≤ 100 · consciencia alterada",58)+sp(16)+big("SIRS",200,Y)+txt("T &gt; 38 o &lt; 36 · FC &gt; 90 · FR &gt; 20 · leucocitos &gt; 12.000 o &lt; 4.000",50)],[2,4]),
 (K,[kicker("2 · LACTATO")+sp(20)+big("≥ 2 MMOL/L",190,Y),txt("En el triaje. Repítelo",64)+sp(16)+txt("Hemocultivos antes del antibiótico",60)],[1,2]),
 (W,[kicker("3 · ANTIBIÓTICO",G)+sp(20)+f'<div style="{A};font-size:220px;white-space:nowrap;color:{BL}">EN 1 HORA</div>',txt("Shock o sepsis probable. Hasta 3 h si es solo posible",60)+sp(16)+txt("Sin foco: ceftriaxona",60,BL)],[1,2]),
 (BL,[kicker("4 · FLUIDOS")+sp(20)+big("30 ML/KG",250,Y),txt("Cristaloide balanceado en 3 h",66)+sp(16)+txt("Reevalúa. Sin almidones",58,"#DCE6F5")],[1,2]),
 (W,[kicker("5 · NORADRENALINA",G)+sp(20)+big("0,05–0,15",220,BL),txt("µg/kg/min, por vía periférica",64)+sp(16)+txt("Objetivo PAM ≥ 65 mmHg",64)],[1,2]),
 (K,[kicker("6 · SI PERSISTE")+sp(20)+big("AVISA<br>A UCI",230,Y),txt("Hidrocortisona 50 mg/6 h IV",64)],[1,2]),
 (BL,[kicker("Y SIEMPRE")+sp(20)+big("CONTROLA<br>EL FOCO",220,Y),txt("En las primeras 6 horas",66)],[1,2]),
 (K,[big("GUÍA 01",130,Y),f'<img src="{ficha}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Guárdala.",50)],[3]),
]
import wave
VOZ=os.environ.get("VOZ","/tmp/loc")
def dur(i):
    with wave.open(os.path.join(VOZ,f"e{i}.wav")) as w: return w.getnframes()/w.getframerate()
PAD=0.9; XF=0.5
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
