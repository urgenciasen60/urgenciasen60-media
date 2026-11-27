"""Reels del lote del 27/11/2026 (regla del 22/11: gancho, sin dosis ni cifras sueltas; sin voz desde el 25/11).
python3 tools/reel_lote_2711.py <clave> <dir_salida> [frames]
Música: python3 tools/musica.py base.wav <segundos> y mezcla con ffmpeg (ver tools/README.md)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
ROOT=os.path.dirname(HERE)
sp=lambda h: f'<div style="height:{h}px"></div>'
def fin(carpeta,slug,sello,n=7):
    f=os.path.join(ROOT,"borradores",carpeta,f"urgenciasen60-{slug}-{n}.jpg")
    if not os.path.exists(f): f=os.path.join(ROOT,carpeta,f"urgenciasen60-{slug}-{n}.jpg")
    return (K,[big(sello,130,Y),f'<img src="file://{f}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Completa en el perfil. Guárdala.",50)],[(3,6.0)])
L={
"pna":("PIELONEFRITIS","urgenciasen60-pielonefritis-reel.mp4",[
 (Y,[big("PIELONEFRITIS",165),big("YA NO ES COMPLICADA O NO: ES SISTÉMICA",112,R)],[(2,3.6)]),
 (W,[kicker("1 · CLASIFICA",G)+sp(30)+big("¿TIENE FIEBRE?",200,R),txt("Fiebre, escalofríos o delirium: es sistémica y cambia el antibiótico",60)],[(1,1.8),(2,3.2)]),
 (K,[kicker("2 · ANTES DEL ANTIBIÓTICO")+sp(30)+big("UROCULTIVO",210,Y),txt("Y busca obstrucción: obstruida e infectada se drena",60)],[(1,1.8),(2,3.2)]),
 (R,[kicker("3 · ¿A CASA?")+sp(30)+big("MIRA TU ANTIBIOGRAMA",160),txt("La quinolona solo vale si la resistencia local es baja",60,Y)],[(1,1.8),(2,3.2)]),
 (Y,[kicker("4 · ¿CUÁNTOS DÍAS?")+sp(30)+big("MENOS DE LO QUE CREES",160,R),txt("Salvo en el varón con posible prostatitis",62)],[(1,1.8),(2,3.0)]),
 fin("pielonefritis","pielonefritis","FICHA 17")]),
}
k=sys.argv[1]; tema,name,S=L[k]
print(build(S,tema,os.path.abspath(sys.argv[2]),name,frames_only=(len(sys.argv)>3)))
