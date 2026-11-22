import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
ROOT=os.path.dirname(HERE)
sp=lambda h: f'<div style="height:{h}px"></div>'
ficha="file://"+os.path.join(ROOT,"borradores","guia-01-sepsis","urgenciasen60-guia-sepsis-2026-10.jpg")
S=[
 (Y,[kicker("GUÍA 01")+sp(10)+big("SEPSIS<br>2026",300),big("PASO A PASO<br>EN TU GUARDIA",140,R)],[(2,5.0)]),
 (W,[kicker("1 · DETECTA",G)+sp(20)+big("CÓDIGO<br>SEPSIS",230,R),txt("Infección + qSOFA ≥ 2, SIRS ≥ 2 o NEWS-2 ≥ 5",62)+sp(16)+txt("El qSOFA solo no basta",58,G)],[(1,2.5),(2,6.0)]),
 (R,[kicker("2 · LACTATO")+sp(20)+big("≥ 2 MMOL/L",190,Y),txt("En el triaje. Repítelo",64)+sp(16)+txt("Hemocultivos antes del antibiótico",60)],[(1,2.5),(2,6.0)]),
 (K,[kicker("3 · ANTIBIÓTICO")+sp(20)+f'<div style="{A};font-size:220px;white-space:nowrap;color:{Y}">EN 1 HORA</div>',txt("Shock o sepsis probable. Hasta 3 h si es solo posible",60)+sp(16)+txt("Sin foco: ceftriaxona",60,Y)],[(1,2.5),(2,6.5)]),
 (Y,[kicker("4 · FLUIDOS")+sp(20)+big("30 ML/KG",250,R),txt("Cristaloide balanceado en 3 h",66)+sp(16)+txt("Reevalúa. Sin almidones",58,G)],[(1,2.5),(2,5.5)]),
 (W,[kicker("5 · NORADRENALINA",G)+sp(20)+big("0,05–0,15",220,R),txt("µg/kg/min, por vía periférica",64)+sp(16)+txt("Objetivo PAM ≥ 65 mmHg",64)],[(1,2.5),(2,6.0)]),
 (R,[kicker("6 · SI PERSISTE")+sp(20)+big("AVISA<br>A UCI",230,Y),txt("Hidrocortisona 50 mg/6 h IV",64)],[(1,2.5),(2,5.0)]),
 (Y,[kicker("Y SIEMPRE")+sp(20)+big("CONTROLA<br>EL FOCO",220,R),txt("En las primeras 6 horas",66)],[(1,2.5),(2,4.0)]),
 (K,[big("GUÍA 01",130,Y),f'<img src="{ficha}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Guárdala.",50)],[(3,6.0)]),
]
out=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else "out_reel")
print(build(S,"GUÍA 01 · SEPSIS",out,"urgenciasen60-guia-sepsis-reel-sinmusica.mp4",frames_only=(len(sys.argv)>2)))
