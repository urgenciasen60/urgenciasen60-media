"""Reels del lote del 20/11/2026: python3 tools/reel_lote_2011.py <clave> <dir_salida> [frames]"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
ROOT=os.path.dirname(HERE)
sp=lambda h: f'<div style="height:{h}px"></div>'
def fin(carpeta,slug,sello,n=7):
    f="file://"+os.path.join(ROOT,"borradores",carpeta,f"urgenciasen60-{slug}-{n}.jpg")
    if not os.path.exists(f[7:]): f="file://"+os.path.join(ROOT,carpeta,f"urgenciasen60-{slug}-{n}.jpg")
    return (K,[big(sello,130,Y),f'<img src="{f}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Completa en el perfil. Guárdala.",50)],[(3,6.0)])
L={
"ictus":("CÓDIGO ICTUS","urgenciasen60-codigo-ictus-reel.mp4",[
 (Y,[big("CÓDIGO ICTUS",190),big("¿SE DESPERTÓ<br>ASÍ?",170,R)],[(2,3.4)]),
 (W,[kicker("1 · ACTIVA",G)+sp(30)+big("&lt; 24 H",260,R),txt("Déficit agudo o de inicio desconocido",66)+sp(22)+txt("Cuenta la última vez que se le vio bien",58,G)],[(1,1.8),(2,3.2)]),
 (R,[kicker("2 · ANTES DEL TAC")+sp(30)+big("GLUCEMIA",220),txt("Imagen en menos de 15 minutos",66,Y)],[(1,1.8),(2,2.8)]),
 (K,[kicker("3 · &lt; 4,5 H")+sp(30)+big("TROMBÓLISIS",180,Y),txt("Tenecteplasa 0,25 mg/kg en bolo o alteplasa 0,9 mg/kg",60)+sp(22)+txt("PA por debajo de 185/110",66)],[(1,1.8),(2,3.4)]),
 (Y,[kicker("4 · GRAN VASO")+sp(30)+f'<div style="{A};font-size:170px;line-height:1.15;color:{R}">TROMBEC&shy;TOMÍA</div>',txt("Hasta 24 h con selección por imagen",64)+sp(22)+txt("Sin esperar a la trombólisis",64)],[(1,1.8),(2,3.2)]),
 fin("codigo-ictus","codigo-ictus","FICHA 11")]),
"eap":("IC AGUDA Y EAP","urgenciasen60-ica-eap-reel.mp4",[
 (Y,[big("EDEMA AGUDO<br>DE PULMÓN",180),big("¿FUNCIONA LA<br>FUROSEMIDA?",150,R)],[(2,3.4)]),
 (W,[kicker("1 · FUROSEMIDA IV",G)+sp(30)+big("40 MG",260,R),txt("Si ya la tomaba: 1–2 veces su dosis oral",64)],[(1,1.8),(2,3.0)]),
 (R,[kicker("2 · A LAS 2 HORAS")+sp(30)+big("MIDE LA ORINA",210),txt("Sodio &gt; 70 mEq/l a las 2 h o diuresis ≥ 100–150 ml/h",60,Y)+sp(22)+txt("Si no responde: dobla la dosis",60)],[(1,1.8),(2,3.4)]),
 (K,[kicker("3 · RESPIRA")+sp(30)+big("VMNI PRONTO",220,Y),txt("FR &gt; 25 y SatO2 &lt; 90 %",68)],[(1,1.6),(2,2.8)]),
 (Y,[kicker("4 · LA PRESIÓN DECIDE")+sp(30)+big("PAS &gt; 110",240,R),txt("Nitroglicerina IV desde 10–20 µg/min",64)+sp(22)+txt("Morfina: no de rutina",62)],[(1,1.8),(2,3.0)]),
 fin("ica-eap","ica-eap","FICHA 06",8)]),
"epoc":("AGUDIZACIÓN DE EPOC","urgenciasen60-epoc-reel.mp4",[
 (Y,[big("EPOC<br>AGUDIZADA",210),big("MÁS OXÍGENO<br>NO ES MEJOR",160,R)],[(2,3.4)]),
 (W,[kicker("1 · OBJETIVO",G)+sp(30)+big("88–92 %",220,R),txt("Venturi 24–28 % o gafas 2–4 l/min",64)],[(1,1.8),(2,3.0)]),
 (R,[kicker("2 · BRONCODILATA")+sp(30)+big("SALBUTAMOL + IPRATROPIO",170),txt("Si retiene CO2, nebuliza con aire",64,Y)],[(1,1.8),(2,3.0)]),
 (K,[kicker("3 · pH &lt; 7,35 Y PaCO2 &gt; 45")+sp(30)+big("VMNI",300,Y),txt("Pese al tratamiento",64)],[(1,1.8),(2,2.8)]),
 (Y,[kicker("4 · CINCO DÍAS")+sp(30)+big("PREDNISONA",180,R),txt("40 mg/día o 0,5 mg/kg/día",66)+sp(22)+txt("Antibiótico si esputo purulento o PCR ≥ 20",58)],[(1,1.8),(2,3.2)]),
 fin("epoc","epoc","FICHA 13")]),
}
k=sys.argv[1]; tema,name,S=L[k]
print(build(S,tema,os.path.abspath(sys.argv[2]),name,frames_only=(len(sys.argv)>3)))
