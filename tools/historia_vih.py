"""Historia de Instagram (1080x1920) del 1/12/2026: aviso de la Ficha 07 (PPE VIH).
python3 tools/historia_vih.py <salida.jpg>"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
from PIL import Image
sp=lambda h: f'<div style="height:{h}px"></div>'
blocks=[kicker("1 DE DICIEMBRE")+sp(20)+big("DÍA MUNDIAL<br>DEL VIH",135),
 txt("¿Pinchazo o sexo de riesgo? ¿PPE sí o no? Cómo decidirlo, en la Ficha 07.",50,weight=700),
 big("HOY, 21:00",150,R)]
out=os.path.abspath(sys.argv[1]); png=out[:-4]+".png"
shot(html(Y,blocks,3,"FICHA 07"),png)
Image.open(png).convert("RGB").save(out,quality=95,subsampling=0); os.remove(png); print(out)
