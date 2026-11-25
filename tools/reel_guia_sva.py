import os, sys, wave; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
# Reel de la Guía 02 (SVA, ERC 2025), sin voz (decisión de Eduardo 25/11): música y textos; los tiempos siguen la locución de tools/voz/guia-sva para dar tiempo de lectura. VOZ=<carpeta con e0..e7.wav> python3 tools/reel_guia_sva.py <salida>
ROOT=os.path.dirname(HERE); BL="#0B4F9E"
sp=lambda h: f'<div style="height:{h}px"></div>'
portada="file://"+os.path.join(ROOT,"guia-02-sva","urgenciasen60-guia-sva-erc2025-1.jpg")
S=[
 (BL,[kicker("GUÍA 02 · ERC 2025")+sp(10)+big("SOPORTE<br>VITAL<br>AVANZADO",210),big("EL ALGORITMO<br>DE 2025",120,Y)],[2]),
 (W,[kicker("1 · LO QUE MÁS PESA",G)+sp(20)+big("COMPRIME<br>BIEN",250,BL),txt("Pausas mínimas: carga el desfibrilador comprimiendo",60)],[1,2]),
 (BL,[kicker("2 · ¿DESFIBRILABLE?")+sp(20)+big("DESCARGA",250,Y),txt("También la FV fina. Y vuelve a comprimir",62)],[1,2]),
 (K,[kicker("3 · ¿NO DESFIBRILABLE?")+sp(20)+big("ADRENALINA<br>YA",220,Y),txt("Lo antes posible, sin esperar",64)],[1,2]),
 (BL,[kicker("4 · MIENTRAS TANTO")+sp(20)+big("4H Y 4T",280,Y),txt("Busca la causa",64)],[1,2]),
 (W,[kicker("5 · VÍA AÉREA Y ACCESO",G)+sp(20)+big("CAPNO&shy;GRAFÍA",210,BL),txt("Y la vía venosa, antes que la intraósea",62)],[1,2]),
 (BL,[kicker("2025 FRENTE A 2021")+sp(20)+big("¿QUÉ<br>CAMBIA?",250,Y),txt("Poco en el algoritmo, bastante en los detalles",62)],[1,2]),
 (K,[big("GUÍA 02",130,Y),f'<img src="{portada}" style="width:500px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Guárdala.",50)],[3]),
]
VOZ=os.environ.get("VOZ","/tmp/loc")
def dur(i):
    with wave.open(os.path.join(VOZ,f"e{i}.wav")) as w: return w.getnframes()/w.getframerate()
PAD=0.6; XF=0.5; S2=[]; starts=[]; t=0.0
for i,(bg,bl,pasos) in enumerate(S):
    D=dur(i)+PAD+(0.8 if i==len(S)-1 else 0); f=min(2.5,D*0.3)
    steps=[(pasos[0],D)] if len(pasos)==1 else [(n,f) for n in pasos[:-1]]+[(pasos[-1],D-f*(len(pasos)-1))]
    S2.append((bg,bl,steps)); starts.append(t); t+=D-XF
out=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else "out_reel")
print(build(S2,"GUÍA 02 · SVA",out,"urgenciasen60-guia-sva-reel-sinmusica.mp4",frames_only=(len(sys.argv)>2),xf=XF))
open(os.path.join(out,"inicios.txt"),"w").write("\n".join(f"{a+0.45:.2f}" for a in starts))
