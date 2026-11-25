"""Cuenta atrás MIR · Ep. 03 (politrauma): python3 tools/mir_ep03.py <dir_salida>. Sin imagen (caso 6 de datos)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mir_ep02 import page, opts, sol, render, LOGO, A, MG, Y, K, R, G, W
EP="EP. 03"; DIAS="55 DÍAS"
P=[]
P.append(page(f'''<div style="display:flex;gap:26px;align-items:center"><img src="{LOGO}" style="width:150px;height:150px">
<div style="border:5px solid {Y};padding:12px 24px"><div style="color:{Y};font-size:26px;font-weight:800;letter-spacing:4px">FALTAN</div><div style="{A};font-size:64px">{DIAS}</div></div></div>
<div style="{A};font-size:200px;line-height:.98">2 CASOS<br>MIR</div>
<div style="{A};font-size:66px">POLITRAUMA: <span style="color:{Y}">¿QUÉ VA PRIMERO?</span></div>
<div style="font-size:34px;font-weight:500;margin-top:-6px">Evaluación primaria y shock hemorrágico · ¿Cuántos aciertas?</div>''', "EP. 03 · CASOS 05-06", "Responde y desliza →", green=True))
P.append(page(f'''<div style="font-size:31px;line-height:1.4">Varón de 32 años, accidente de moto. Llega <b>hablando con frases cortas</b>, GCS 14, FR 28, SatO2 93 % con oxígeno, <b>TA 88/50, FC 128</b>. Tiene una herida en la cara interna del muslo derecho con <b>sangrado pulsátil</b> que empapa los apósitos.</div>
<div style="{A};font-size:44px">¿QUÉ HACES PRIMERO?</div>
{opts([("A", "Intubación orotraqueal por el riesgo de que se deteriore la vía aérea"), ("B", "Controlar la hemorragia: compresión directa y torniquete proximal a la herida"), ("C", "Collarín cervical rígido y TC de cuerpo entero antes de cualquier maniobra"), ("D", "Dos litros de cristaloide para recuperar una PAS de 120 mmHg")], 29)}''', "CASO 5 · 2/7", "Comenta A, B, C o D y desliza →"))
P.append(page(f'''<img src="{LOGO}" style="width:110px;height:110px">
<div style="{A};font-size:190px;line-height:.98">¿A, B, C<br>O D?</div>
<div style="{A};font-size:58px">ESCRÍBELO EN COMENTARIOS <span style="color:{Y}">ANTES DE DESLIZAR</span></div>
<div style="font-size:32px;font-weight:500">Sin trampas: la solución está en la siguiente.</div>''', EP, "3/7 · Desliza →", green=True))
P.append(page(sol("B", "LA X VA ANTES QUE LA A",
 "Una <b>hemorragia externa exanguinante</b> mata antes que la vía aérea. Por eso la evaluación primaria empieza por controlarla: <b>xABCDE</b> en la nueva edición del ATLS, &lt;C&gt;ABCDE en la guía europea. Compresión directa y, si no basta en una extremidad, <b>torniquete</b>. Después, A, B, C, D y E.",
 [("A", "Habla: la vía aérea está permeable. Intubarlo ahora no corrige el shock y lo puede empeorar."),
  ("C", "La inmovilización nunca debe retrasar una maniobra que salva la vida, y la TC es para el paciente estable."),
  ("D", "En el shock hemorrágico se restringen los cristaloides y se tolera una PAS de 80-90 mmHg si no hay TCE grave.")],
 "x = exanguinación: compresión, torniquete y hemostáticos, antes de la A."), "SOLUCIÓN 5 · 4/7", "Desliza →"))
P.append(page(f'''<div style="font-size:31px;line-height:1.4">Mujer de 45 años, colisión frontal con cinturón, hace 1 hora. <b>TA 78/40, FC 135</b>, relleno capilar lento, GCS 15, sin TCE. <b>eFAST: líquido libre en el espacio de Morison.</b> Tras 500 ml de cristaloide sigue con TA 80/45.</div>
<div style="{A};font-size:44px">¿QUÉ AFIRMACIÓN ES CORRECTA?</div>
{opts([("A", "Antes de operar, TC toracoabdominal con contraste para localizar la lesión"), ("B", "Ácido tranexámico, transfusión precoz, hipotensión permisiva y quirófano para control de daños"), ("C", "Más cristaloide hasta una PAS de 120 mmHg y después decidir"), ("D", "Un FAST negativo habría descartado la lesión abdominal")], 29)}''', "CASO 6 · 5/7", "Comenta A, B, C o D y desliza →"))
P.append(page(sol("B", "INESTABLE + FAST POSITIVO:<br>QUIRÓFANO",
 "Shock hemorrágico que no responde y <b>sangrado abdominal</b> en la eFAST: control quirúrgico inmediato (cirugía de <b>control de daños</b>), sin pasar por la TC. Mientras, <b>ácido tranexámico</b> 1 g en 10 min (dentro de las 3 primeras horas) y 1 g en 8 h, hemoderivados pronto (plasma y hematíes, fibrinógeno si &lt; 1,5 g/l) y <b>PAS objetivo de 80-90 mmHg</b>.",
 [("A", "La TC es para el paciente estable o estabilizable. En shock que no responde, retrasa el control del sangrado."),
  ("C", "Más cristaloide diluye la coagulación y aumenta el sangrado: se restringe."),
  ("D", "La eFAST es poco sensible (en torno al 74 %): si es negativa y la sospecha persiste, hay que seguir buscando.")],
 "con TCE grave cambia el objetivo: PAM de al menos 80 mmHg."), "SOLUCIÓN 6 · 6/7", "Desliza →"))
card = lambda t, x: f'<div style="background:{W};color:{K};padding:24px 26px;flex:1"><div style="{A};font-size:38px;margin-bottom:12px">{t}</div><div style="font-size:28px;line-height:1.38">{x}</div></div>'
P.append(page(f'''<div style="{A};font-size:92px;line-height:1">PRIMERO,<br><span style="color:{Y}">LA HEMORRAGIA</span></div>
<div style="font-size:32px;font-weight:500;line-height:1.4">En el politrauma, lo que mata antes se trata antes.</div>
<div style="display:flex;gap:24px">{card("xABCDE", "Hemorragia externa exanguinante: <b>compresión y torniquete</b>, antes de la vía aérea.")}{card("SHOCK HEMORRÁGICO", "<b>Tranexámico en &lt; 3 h</b>, sangre pronto, poco cristaloide y PAS de 80-90.")}</div>
<div style="background:{Y};color:{K};padding:22px 26px;font-size:29px;line-height:1.4"><b>FAST + e inestable: quirófano. FAST + y estable: TC.</b> Un FAST negativo no descarta la lesión.</div>
<div style="font-size:19px;line-height:1.4;color:#CFE3D9">Fuentes: guía europea de hemorragia y coagulopatía en el trauma, 6.ª ed. (Rossaint et al., Crit Care 2023); ATLS, 11.ª ed. Casos de elaboración propia. Contenido formativo; no sustituye a los protocolos de tu centro.</div>''', "CLAVE MIR · 7/7", "Guárdalo para el repaso", green=True))
if __name__ == "__main__":
    print(render(P, os.path.abspath(sys.argv[1]), "urgenciasen60-mir-ep03"))
