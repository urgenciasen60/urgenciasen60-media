"""Cuenta atrás MIR · Ep. 04 (shock): python3 tools/mir_ep04.py <dir_salida>. Sin imagen (caso 8 de datos). Remite a la Guía 01."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mir_ep02 import page, opts, sol, render, LOGO, A, MG, Y, K, R, G, W
EP="EP. 04"; DIAS="52 DÍAS"
P=[]
P.append(page(f'''<div style="display:flex;gap:26px;align-items:center"><img src="{LOGO}" style="width:150px;height:150px">
<div style="border:5px solid {Y};padding:12px 24px"><div style="color:{Y};font-size:26px;font-weight:800;letter-spacing:4px">FALTAN</div><div style="{A};font-size:64px">{DIAS}</div></div></div>
<div style="{A};font-size:128px;line-height:1.05">TA 78/42 DESPUÉS DE LOS FLUIDOS</div>
<div style="{A};font-size:92px;color:{Y}">¿ESPERAS A LA VÍA CENTRAL?</div>
<div style="font-size:34px;font-weight:500">2 casos MIR de shock</div>''', "EP. 04 · CASOS 07-08", "Responde y desliza →", green=True))
P.append(page(f'''<div style="font-size:31px;line-height:1.4">Mujer de 74 años con fiebre, disuria y confusión. Tras <b>30 ml/kg de cristaloide balanceado</b> sigue con <b>TA 78/42</b>, FC 118 y <b>lactato 5 mmol/l</b>. Todavía no tiene vía central.</div>
<div style="{A};font-size:44px">¿QUÉ ES LO MÁS ADECUADO?</div>
{opts([("A", "Dopamina por vía periférica hasta que se coloque la vía central"), ("B", "Noradrenalina ya, por vía periférica, con objetivo de PAM 65 mmHg, y antibiótico en la primera hora tras los hemocultivos"), ("C", "Más bolos de cristaloide hasta normalizar el lactato antes de empezar el vasopresor"), ("D", "Esperar a la vía central para empezar la noradrenalina por el riesgo de extravasación")], 29)}''', "CASO 7 · 2/7", "Comenta A, B, C o D y desliza →"))
P.append(page(f'''<img src="{LOGO}" style="width:110px;height:110px">
<div style="{A};font-size:190px;line-height:.98">¿A, B, C<br>O D?</div>
<div style="{A};font-size:58px">ESCRÍBELO EN COMENTARIOS <span style="color:{Y}">ANTES DE DESLIZAR</span></div>
<div style="font-size:32px;font-weight:500">Sin trampas: la solución está en la siguiente.</div>''', EP, "3/7 · Desliza →", green=True))
P.append(page(sol("B", "SHOCK SÉPTICO:<br>NORADRENALINA SIN ESPERAR",
 "Hipotensión que persiste tras la carga de volumen y lactato alto: <b>shock séptico</b> de foco urinario. El vasopresor de primera línea es la <b>noradrenalina</b>, y se puede iniciar por una <b>vía periférica de buen calibre</b> mientras se canaliza la central. Objetivo inicial: <b>PAM de 65 mmHg</b>. Hemocultivos y antibiótico en la primera hora.",
 [("A", "La dopamina no se recomienda como primera línea: la noradrenalina es superior."),
  ("C", "No se siguen dando fluidos solo para normalizar el lactato: aumenta el riesgo de sobrecarga."),
  ("D", "Esperar a la vía central retrasa el vasopresor; la vía periférica es aceptable al principio.")],
 "el lactato sirve para seguir la evolución: repítelo y mira la tendencia."), "SOLUCIÓN 7 · 4/7", "Desliza →"))
tab = lambda rows: '<div style="display:grid;grid-template-columns:1.4fr 1fr;gap:10px 20px;font-size:32px">'+"".join(f'<div style="border-top:3px solid {K};padding-top:10px;color:{G}">{a}</div><div style="border-top:3px solid {K};padding-top:10px;font-weight:800">{b}</div>' for a,b in rows)+'</div>'
P.append(page(f'''<div style="font-size:31px;line-height:1.4">Varón de 66 años operado de una prótesis de cadera hace 8 días. <b>Disnea brusca e hipotensión.</b> Datos hemodinámicos:</div>
{tab([("TA · FC","80/50 mmHg · 125 lpm"),("PVC","18 mmHg (alta)"),("POAP (presión de enclavamiento)","8 mmHg (normal)"),("Gasto cardiaco","Bajo"),("Resistencias vasculares sistémicas","Altas")])}
<div style="{A};font-size:44px">¿QUÉ TIPO DE SHOCK ES MÁS PROBABLE?</div>
{opts([("A", "Hipovolémico"), ("B", "Cardiogénico por fallo del ventrículo izquierdo"), ("C", "Obstructivo por tromboembolismo pulmonar masivo"), ("D", "Distributivo (séptico)")], 30)}''', "CASO 8 · 5/7", "Comenta A, B, C o D y desliza →"))
P.append(page(sol("C", "PVC ALTA CON POAP NORMAL:<br>OBSTRUCTIVO",
 "Gasto bajo con resistencias altas. La clave está en las presiones: la <b>PVC está alta</b> pero la <b>POAP es normal</b>, así que el problema está <b>antes del ventrículo izquierdo</b>. En un operado reciente con disnea brusca, lo primero es el <b>TEP masivo</b>.",
 [("A", "En el hipovolémico, la PVC y la POAP están bajas."),
  ("B", "En el fallo del ventrículo izquierdo, la POAP está alta."),
  ("D", "En el distributivo, las resistencias están bajas y el gasto suele ser normal o alto.")],
 "la ecografía ayuda a diferenciarlo: ventrículo derecho dilatado en el TEP, derrame en el taponamiento."), "SOLUCIÓN 8 · 6/7", "Desliza →"))
th = lambda c: f'<div style="{A};font-size:34px;color:{Y}">{c}</div>'
td = lambda c, b=False: f'<div style="background:{W};color:{K};padding:10px 12px;font-size:28px;font-weight:{800 if b else 600}">{c}</div>'
grid = '<div style="display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1fr;gap:8px">'+"".join(th(c) for c in ["SHOCK","PVC","POAP","GC","RVS"])+"".join("".join(td(c,i==0) for i,c in enumerate(r)) for r in [("Hipovolémico","↓","↓","↓","↑"),("Cardiogénico","= / ↑","↑","↓","↑"),("Obstructivo (TEP)","↑","= / ↓","↓","↑"),("Distributivo","= / ↓","= / ↓","= / ↑","↓")])+'</div>'
P.append(page(f'''<div style="{A};font-size:84px;line-height:1">EL SHOCK,<br><span style="color:{Y}">EN UNA TABLA</span></div>
{grid}
<div style="background:{Y};color:{K};padding:22px 26px;font-size:29px;line-height:1.4"><b>Shock séptico:</b> noradrenalina por vía periférica si hace falta, PAM 65 y antibiótico en la primera hora. Todo el manejo, en la <b>Guía 01</b> del perfil.</div>
<div style="font-size:19px;line-height:1.4;color:#CFE3D9">Fuentes: Surviving Sepsis Campaign 2021 y 2026; GT-LATINFURG (Emergencias 2026;38:27-63); Oliveira MDC, et al. einstein 2024 (perfiles hemodinámicos). Casos de elaboración propia. Contenido formativo; no sustituye a los protocolos de tu centro.</div>''', "CLAVE MIR · 7/7", "Guárdalo para el repaso", green=True))
if __name__ == "__main__":
    print(render(P, os.path.abspath(sys.argv[1]), "urgenciasen60-mir-ep04"))
