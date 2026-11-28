"""Reels del lote del 25/11/2026 (regla del 22/11: gancho, sin dosis ni cifras sueltas).
python3 tools/reel_lote_2511.py <clave> <dir_salida> [frames]"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import *
ROOT=os.path.dirname(HERE)
sp=lambda h: f'<div style="height:{h}px"></div>'
def fin(carpeta,slug,sello,n=7,seg=6.0):
    f=os.path.join(ROOT,"borradores",carpeta,f"urgenciasen60-{slug}-{n}.jpg")
    if not os.path.exists(f): f=os.path.join(ROOT,carpeta,f"urgenciasen60-{slug}-{n}.jpg")
    return (K,[big(sello,130,Y),f'<img src="file://{f}" style="width:560px;display:block;box-shadow:0 24px 70px rgba(0,0,0,.6)">',txt("Completa en el perfil. Guárdala.",50)],[(3,seg)])
L={
"sva":("SVA ADULTO","urgenciasen60-algoritmo-sva-reel.mp4",[
 (Y,[kicker("ALGORITMO 01 · ERC 2025")+sp(20)+big("SOPORTE VITAL AVANZADO",160),big("LA FV FINA TAMBIÉN SE DESCARGA",120,R)],[(2,3.6)]),
 (W,[kicker("1 · LO QUE MÁS PESA",G)+sp(30)+big("COMPRIME BIEN",210,R),txt("Pausas mínimas: carga el desfibrilador mientras comprimes",60)],[(1,1.8),(2,3.0)]),
 (R,[kicker("2 · ¿DESFIBRILABLE?")+sp(30)+big("DESCARGA Y COMPRIME",180),txt("Sin mirar el pulso. El ritmo, a los dos minutos",60,Y)],[(1,1.8),(2,3.0)]),
 (K,[kicker("3 · ¿NO DESFIBRILABLE?")+sp(30)+big("ADRENALINA YA",200,Y),txt("Lo antes posible, sin esperar",64)],[(1,1.8),(2,2.8)]),
 (Y,[kicker("4 · MIENTRAS TANTO")+sp(30)+big("4H Y 4T",260,R),txt("Busca la causa: es lo que cambia el pronóstico",62)],[(1,1.8),(2,3.0)]),
 fin("algoritmo-sva","algoritmo-sva","ALGORITMO 01")]),
"vih":("PPE VIH","urgenciasen60-vih-ppe-reel.mp4",[
 (Y,[big("¿PINCHAZO O SEXO DE RIESGO?",150),big("¿PPE SÍ O NO?",150,R)],[(2,3.0)]),
 (W,[kicker("1 · CUÁNDO",G)+sp(30)+big("CUANTO ANTES",200,R),txt("Las primeras horas cuentan. No esperes a la fuente",62)],[(1,1.8),(2,3.0)]),
 (R,[kicker("2 · A QUIÉN")+sp(30)+big("DEPENDE DE LA FUENTE",170),txt("Con carga viral indetectable, no hace falta",62,Y)],[(1,1.8),(2,3.0)]),
 (K,[kicker("3 · QUÉ")+sp(30)+big("UN MES",260,Y),txt("Una pauta de tres fármacos, a veces en un solo comprimido",60)],[(1,1.8),(2,3.0)]),
 (Y,[kicker("4 · Y ADEMÁS")+sp(30)+big("HEPATITIS B E ITS",170,R),txt("Y aprovecha para pedir la serología del VIH a quien la necesita",58)],[(1,1.8),(2,3.2)]),
 fin("vih-ppe","vih-ppe","FICHA 07",seg=4.0)]),
"vertigo":("VÉRTIGO AGUDO","urgenciasen60-vertigo-reel.mp4",[
 (Y,[big("VÉRTIGO AGUDO",180),big("UN TAC NORMAL NO DESCARTA UN ICTUS",120,R)],[(2,3.6)]),
 (W,[kicker("1 · EL TIEMPO",G)+sp(30)+big("¿CUÁNTO DURA?",200,R),txt("Continuo, al moverse o espontáneo: cada uno se estudia distinto",60)],[(1,1.8),(2,3.2)]),
 (K,[kicker("2 · LEVÁNTALO")+sp(30)+big("MIRA LA MARCHA",190,Y),txt("Si no camina sin apoyo, piensa en el cerebelo",62)],[(1,1.8),(2,3.0)]),
 (R,[kicker("3 · CON NISTAGMO")+sp(30)+big("HINTS PLUS",230),txt("Cuatro signos. Periférico solo si los cuatro son benignos",60,Y)],[(1,1.8),(2,3.2)]),
 (Y,[kicker("4 · SI ES POSICIONAL")+sp(30)+big("EPLEY",280,R),txt("La maniobra cura en el box. Los sedantes, no",62)],[(1,1.8),(2,3.0)]),
 fin("vertigo","vertigo","FICHA 13")]),
"scacest":("SCACEST","urgenciasen60-scacest-reel.mp4",[
 (Y,[big("SCACEST",280),big("EL RELOJ EMPIEZA EN EL ECG",130,R)],[(2,3.4)]),
 (W,[kicker("1 · ECG",G)+sp(30)+big("LEE EL ST",240,R),txt("Los criterios cambian según la derivación, la edad y el sexo",60)],[(1,1.8),(2,3.2)]),
 (K,[kicker("2 · NO TODOS ELEVAN")+sp(30)+big("EQUIVA&shy;LENTES",200,Y),txt("Bloqueos, marcapasos, infarto posterior y aVR",62)],[(1,1.8),(2,3.0)]),
 (R,[kicker("3 · REPERFUSIÓN")+sp(30)+big("¿ICP O FIBRINÓLISIS?",170),txt("Depende de cuánto tardes en llegar a la sala",62,Y)],[(1,1.8),(2,3.0)]),
 (Y,[kicker("4 · DE ENTRADA")+sp(30)+f'<div style="{A};font-size:170px;line-height:1.15;color:{R}">ANTITROM&shy;BÓTICOS</div>',txt("Antiagregación y anticoagulación, según tu código infarto",60)],[(1,1.8),(2,3.0)]),
 fin("scacest","scacest","FICHA 14")]),
"cad":("CETOACIDOSIS DIABÉTICA","urgenciasen60-cetoacidosis-reel.mp4",[
 (Y,[big("CETOACIDOSIS",160),big("EL POTASIO VA ANTES QUE LA INSULINA",120,R)],[(2,3.6)]),
 (W,[kicker("1 · DIAGNÓSTICO",G)+sp(30)+big("D + K + A",260,R),txt("Y ojo: con gliflozinas, la glucemia puede ser normal",60)],[(1,1.8),(2,3.2)]),
 (K,[kicker("2 · LO PRIMERO")+sp(30)+big("SUERO",280,Y),txt("Y glucosado cuando baje la glucemia",62)],[(1,1.8),(2,2.8)]),
 (R,[kicker("3 · ANTES DE LA INSULINA")+sp(30)+big("MIRA EL POTASIO",190),txt("Si está bajo, la insulina espera",64,Y)],[(1,1.8),(2,2.8)]),
 (Y,[kicker("4 · ¿RESUELTA?")+sp(30)+big("MIRA LAS CETONAS",180,R),txt("No la glucemia. Y solapa la insulina subcutánea",62)],[(1,1.8),(2,3.0)]),
 fin("cetoacidosis","cetoacidosis","FICHA 15")]),
"ee":("ESTADO EPILÉPTICO","urgenciasen60-estado-epileptico-reel.mp4",[
 (Y,[big("ESTADO EPILÉPTICO",170),big("A LOS 5 MINUTOS YA NO ES UNA CRISIS",120,R)],[(2,3.6)]),
 (W,[kicker("1 · LO PRIMERO",G)+sp(30)+big("GLUCEMIA",215,R),txt("Vía aérea, oxígeno y monitor",64)],[(1,1.8),(2,2.8)]),
 (K,[kicker("2 · BENZODIACEPINA")+sp(30)+big("YA Y COMPLETA",200,Y),txt("Sin vía también se puede. Quedarse corto es lo habitual",60)],[(1,1.8),(2,3.2)]),
 (R,[kicker("3 · SI SIGUE")+sp(30)+big("SEGUNDA LÍNEA",200),txt("Tres fármacos que funcionan igual. Elige según el paciente",60,Y)],[(1,1.8),(2,3.2)]),
 (Y,[kicker("4 · SI SE RECUPERA")+sp(30)+big("PRIMERA CRISIS",190,R),txt("Busca la causa y decide el destino",64)],[(1,1.8),(2,2.8)]),
 fin("estado-epileptico","estado-epileptico","FICHA 16")]),
}
k=sys.argv[1]; tema,name,S=L[k]
print(build(S,tema,os.path.abspath(sys.argv[2]),name,frames_only=(len(sys.argv)>3)))
