import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
ROOT=os.path.dirname(HERE); T="CÓLICO NEFRÍTICO"
ficha="file://"+os.path.join(ROOT,"colico-nefritico","urgenciasen60-colico-nefritico-7.jpg")
sp=lambda h: f'<div style="height:{h}px"></div>'
S=[
 (Y,[big("CÓLICO<br>NEFRÍTICO",200),big("CON FIEBRE YA NO ES SIMPLE",110,R)],[(2,3.2)]),
 (W,[kicker("1 · ANALGESIA",G)+sp(30)+big("AINE PRIMERO",200,R),txt("Dexketoprofeno o diclofenaco, IV o IM",62)+sp(20)+txt("Si no cede: metamizol y, después, tramadol",58,G)],[(1,1.8),(2,3.4)]),
 (K,[kicker("2 · IMAGEN")+sp(30)+big("ECOGRAFÍA",220,Y),txt("¿Fiebre? Mira si el riñón está dilatado",62)+sp(20)+txt("TC solo si va mal o hay dudas",60,Y)],[(1,1.8),(2,3.2)]),
 (R,[kicker("3 · LA URGENCIA REAL")+sp(30)+big("OBSTRUIDO E INFECTADO",150),txt("Descompresión urgente: avisa a Urología",62,Y)],[(1,1.8),(2,2.8)]),
 (Y,[kicker("AL ALTA")+sp(30)+big("AINE PAUTADO",200,R),txt("Tamsulosina si litiasis distal de 5–10 mm",60)+sp(20)+txt("Sin sobrehidratar",60)],[(1,1.6),(2,2.8)]),
 (K,[big("FICHA 06",130,Y),f'<img src="{ficha}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Completa en el perfil. Guárdala.",50)],[(3,6.0)]),
]
out=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else "out_reel")
print(build(S,T,out,"urgenciasen60-colico-nefritico-reel-sinmusica.mp4",frames_only=(len(sys.argv)>2)))
