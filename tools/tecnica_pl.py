import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ficha import *
T="PUNCIÓN LUMBAR"; N=7; KW=dict(strip=K)
note=lambda t: f'<div style="font-size:36px;line-height:1.4;color:{G}">{t}</div>'
rows=lambda *x: '<div style="display:flex;flex-direction:column;gap:22px">'+"".join(x)+'</div>'
def esquema():
    v="".join(f'<rect x="150" y="{40+i*112}" width="150" height="76" rx="22" fill="{K}"/><text x="225" y="{92+i*112}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="40" fill="#FFF">L{i+1}</text>' for i in range(5))
    return f'''<svg style="width:920px;height:610px;flex-shrink:0" width="920" height="610" viewBox="0 0 920 610" xmlns="http://www.w3.org/2000/svg">{v}
<line x1="20" y1="414" x2="430" y2="414" stroke="{G}" stroke-width="6" stroke-dasharray="16 12"/>
<circle cx="34" cy="414" r="20" fill="{G}"/><circle cx="416" cy="414" r="20" fill="{G}"/>
<text x="470" y="405" font-family="Inter" font-weight="800" font-size="34" fill="{G}">Línea entre crestas</text><text x="470" y="447" font-family="Inter" font-weight="800" font-size="34" fill="{G}">ilíacas: apófisis de L4</text>
<path d="M440 358 L320 358" stroke="{R}" stroke-width="12"/><path d="M320 358 l34 -22 v44 z" fill="{R}"/>
<path d="M440 470 L320 470" stroke="{R}" stroke-width="12"/><path d="M320 470 l34 -22 v44 z" fill="{R}"/>
<text x="470" y="330" font-family="Inter" font-weight="800" font-size="38" fill="{R}">L3–L4</text>
<text x="470" y="520" font-family="Inter" font-weight="800" font-size="38" fill="{R}">L4–L5</text>
<text x="470" y="70" font-family="Inter" font-weight="600" font-size="30" fill="{G}">Esquema propio,</text><text x="470" y="108" font-family="Inter" font-weight="600" font-size="30" fill="{G}">vista posterior</text></svg>'''
paso=lambda t: kicker(f"TÉCNICA 01 · {t}")
P=[page(1,N,T,f'<div style="font-size:40px;font-weight:800;letter-spacing:6px;color:{Y}">TÉCNICA 01</div>'+big("PUNCIÓN LUMBAR",140,"#FFFFFF",True)+big(f'LA MITAD DEL ÉXITO ES LA <span style="color:{Y}">POSICIÓN</span>',118,"#FFFFFF")+'<div style="font-size:40px;font-weight:600;line-height:1.3;max-width:820px">Solo la técnica: posición, referencias, aguja y pasos. Con ficha final.</div>',cover=True,dark=True,**KW),
page(2,N,T,paso("REFERENCIAS")+big("L3–L4 O L4–L5",150,R,True)+esquema(),**KW),
page(3,N,T,paso("POSICIÓN")+big("FLEXIÓN MÁXIMA",140,nowrap=True)+rows(line("Decúbito lateral, rodillas al pecho y mentón al esternón: abre los espacios",True),line("Hombros y caderas perpendiculares a la cama, sin rotar"),line("Sentado e inclinado hacia delante si es obeso o la anatomía es difícil"))+note("Solo en decúbito lateral se puede medir la presión de apertura."),**KW),
page(4,N,T,paso("LA AGUJA")+big("ATRAUMÁTICA",150,R,True)+rows(line("Punta de lápiz: menos cefalea pospunción (11 % frente a 4,2 %)",True),line("22 G si vas a medir la presión de apertura"),line("Si es biselada: bisel paralelo al eje de la columna"))+note("Nath S, et al. Lancet 2018: 110 ensayos, más de 31.000 pacientes."),**KW),
page(5,N,T,paso("PASOS")+f'<div style="display:flex;flex-direction:column;gap:20px">{num(1,"Asepsia, campo estéril y anestesia local")}{num(2,"Aguja en línea media, apuntando al ombligo")}{num(3,"Avanza despacio; retira el fiador para comprobar")}{num(4,"Sale líquido: mide presión y recoge los tubos")}{num(5,"Recoloca el fiador antes de retirar la aguja")}</div>'+note("Si tocas hueso, retira hasta el subcutáneo y redirige."),**KW),
page(6,N,T,paso("AL TERMINAR")+big("FIADOR DENTRO",150,nowrap=True)+rows(line("Vuelve a colocar el fiador antes de retirar la aguja",True),line("Apósito estéril en el punto de punción"),line("Vigila cefalea pospunción, dolor lumbar, sangrado o infección"))+note("La presión de apertura solo es válida en decúbito lateral."),**KW),
page(7,N,T,ficha_body("PUNCIÓN LUMBAR","Adulto · técnica",[("POSICIÓN","Decúbito lateral en flexión máxima, espalda en el borde. Sentado si es difícil"),("REFERENCIA","Línea entre crestas ilíacas = L4. Espacio L4–L5 o L3–L4",True),("ASEPSIA","Campo estéril y anestesia local de piel y trayecto"),("AGUJA","Atraumática (22 G si mides presión). Biselada: bisel paralelo a la columna",True),("AVANCE","Línea media, hacia el ombligo. Resalte en ligamento amarillo y duramadre"),("PRESIÓN","Presión de apertura en decúbito lateral; recoge las muestras"),("RETIRADA","Fiador dentro antes de sacar la aguja")],"Ellenby MS, et al. N Engl J Med 2006;355:e12; Nath S, et al. Lancet 2018;391:1197-204",size=100,fs=28),ficha="01",fam="TÉCNICA",**KW),
]
render(P,sys.argv[1] if len(sys.argv)>1 else "out","tecnica-puncion-lumbar")
