import os, sys, subprocess; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
# Reels de las Guías 01 y 02 (28/11): sin voz, título de la guía como apertura (excepción de Eduardo), planos de 4 s como máximo.
# Uso: python3 tools/reel_guias.py <carpeta de trabajo>
ROOT=os.path.dirname(HERE); BL="#0B4F9E"
sp=lambda h: f'<div style="height:{h}px"></div>'
def fin(n,path):
    img="file://"+os.path.join(ROOT,path)
    return (K,[big(f"GUÍA {n}",120,Y),f'<img src="{img}" style="width:520px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("La ficha, en el carrusel. Guárdala y envíala.",50)],[(3,3.8)])
def esc(bg,k,t,size,color,sub=None,d=3.6,kc=None,sc=62):
    head=kicker(k,kc)+sp(20)+big(t,size,color)
    if not sub: return (bg,[head],[(1,2.8)])
    return (bg,[head,txt(sub,sc)],[(1,1.2),(2,d-1.2)])
G1=[
 (BL,[kicker("GUÍA 01")+sp(10)+big("SEPSIS<br>2026",270),big("LA GUÍA<br>DE URGENCIAS",125,Y)],[(2,2.8)]),
 esc(W,"LA FUENTE","GT-<br>LATINFURG",230,BL,"INFURG-SEMES · Emergencias 2026",3.4,G,60),
 esc(BL,"1 · DETECTA","DESDE EL<br>TRIAJE",230,Y,"Escalas sencillas que activan el código sepsis",4.0),
 esc(K,"2 · EL TIEMPO MANDA","PRIMERA<br>HORA",230,Y,"Lactato, cultivos y antibiótico"),
 esc(BL,"3 · REANIMA","FLUIDOS Y<br>NORADRE&shy;NALINA",200,Y,"Sin esperar a la vía central",3.6),
 esc(W,"4 · SI NO RESPONDE","AVISA<br>A UCI",230,BL,None,kc=G),
 esc(K,"5 · NO LO OLVIDES","CONTROLA<br>EL FOCO",200,Y,"En las primeras 6 horas",3.2),
 esc(BL,"CINCO PUNTOS","QUÉ<br>EVITAR",250,Y,"Están en el carrusel",3.2),
 fin("01","borradores/guia-01-sepsis/urgenciasen60-guia-sepsis-2026-11.jpg")]
G2=[
 (BL,[kicker("GUÍA 02 · ERC 2025")+sp(10)+big("SOPORTE<br>VITAL<br>AVANZADO",200),big("EL ALGORITMO<br>DE 2025",120,Y)],[(2,2.8)]),
 esc(W,"1 · LO QUE MÁS PESA","COMPRIME<br>BIEN",210,BL,"Pausas mínimas: carga el desfibrilador comprimiendo",4.0,G,60),
 esc(BL,"2 · ¿DESFIBRILABLE?","DESCARGA",215,Y,"También la FV fina. Y vuelve a comprimir",4.0),
 esc(K,"3 · ¿NO DESFIBRILABLE?","ADRENALINA<br>YA",185,Y,"Lo antes posible, sin esperar",3.4,sc=64),
 esc(BL,"4 · MIENTRAS TANTO","4H Y 4T",260,Y,"Busca la causa",3.0),
 esc(W,"5 · VÍA AÉREA","CAPNO&shy;GRAFÍA",200,BL,"Confirma el tubo",3.0,G),
 esc(K,"6 · ACCESO","VÍA IV<br>PRIMERO",230,Y,"Antes que la intraósea",3.2),
 esc(BL,"2025 FRENTE A 2021","¿QUÉ<br>CAMBIA?",230,Y,"Poco en el algoritmo, bastante en los detalles",4.0),
 fin("02","guia-02-sva/urgenciasen60-guia-sva-erc2025-1.jpg".replace("-1.jpg","-11.jpg"))]
W_=sys.argv[1]
for S,tema,dest in ((G1,"GUÍA 01 · SEPSIS","borradores/guia-01-sepsis/urgenciasen60-guia-sepsis-reel.mp4"),(G2,"GUÍA 02 · SVA","guia-02-sva/urgenciasen60-guia-sva-reel.mp4")):
    out=os.path.join(W_,tema[:7].replace(" ",""))
    v,T=build(S,tema,out,"sinmusica.mp4",xf=0.4)
    wav=os.path.join(out,"m.wav"); subprocess.run([sys.executable,os.path.join(HERE,"musica.py"),wav,str(T)],check=True)
    subprocess.run(["ffmpeg","-y","-v","error","-i",v,"-i",wav,"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","160k","-af","loudnorm=I=-16:TP=-1.5","-ar","44100","-shortest",os.path.join(ROOT,dest)],check=True)
    print(dest,T)
