import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
T="HIPOGLUCEMIA"; ROOT=os.path.dirname(HERE)
ficha="file://"+os.path.join(ROOT,"hipoglucemia","urgenciasen60-hipoglucemia-7.jpg")
sp=lambda h: f'<div style="height:{h}px"></div>'
S=[
 (Y,[big("HIPOGLUCEMIA",160),big("TRATARLA ES FÁCIL",150,R)],[(2,3.4)]),
 (W,[kicker("1 · SI TRAGA",G)+sp(30)+big("15 / 15",260,R),txt("15–20 g de glucosa oral",66)+sp(22)+txt("Nueva glucemia a los 15 min",62,G)],[(1,1.8),(2,3.0)]),
 (R,[kicker("2 · SI NO TRAGA")+sp(30)+f'<div style="{A};font-size:210px;white-space:nowrap">GLUCOSA IV</div>',txt("10–25 g",80,Y)+sp(22)+txt("100–250 ml al 10 % · 30–75 ml al 33 %<br>20–50 ml al 50 %",56)],[(1,2.0),(2,3.4)]),
 (K,[kicker("3 · SIN VÍA")+sp(30)+big("GLUCAGÓN",220,Y),txt("1 mg IM o subcutáneo",66)],[(1,1.6),(2,2.6)]),
 (Y,[kicker("¿SULFONILUREAS?")+sp(30)+big("NO TE FÍES",210,R),txt("Perfusión de glucosado al 10 %",62)+sp(22)+txt("Vigilancia de 48–72 h",62)],[(1,1.8),(2,3.2)]),
 (K,[big("FICHA 05",130,Y),f'<img src="{ficha}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Completa en el perfil. Guárdala.",50)],[(3,6.0)]),
]
out=sys.argv[1] if len(sys.argv)>1 else "out_reel"
print(build(S,T,out,"urgenciasen60-hipoglucemia-reel-sinmusica.mp4",frames_only=(len(sys.argv)>2)))
