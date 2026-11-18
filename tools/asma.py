import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ficha import *
T="CRISIS DE ASMA"; N=7
note=lambda t: f'<div style="font-size:34px;line-height:1.4;color:{G}">{t}</div>'
rows=lambda *x: '<div style="display:flex;flex-direction:column;gap:20px">'+"".join(x)+'</div>'
redrow=lambda k,v: f'<div style="border-top:4px solid {K};padding-top:20px;display:flex;justify-content:space-between;gap:32px;font-size:40px;color:{R}"><div style="font-weight:800">{k}</div><div style="font-weight:800;text-align:right">{v}</div></div>'
def tabla():
    H=["","Leve","Moderada","Grave"]
    D=[("SatO2","&gt; 95 %","&lt; 95 %","&lt; 90 %"),("FR","Normal o ↑","&gt; 20","&gt; 25"),("FC","&lt; 100","&gt; 100","&gt; 120"),("PaCO2","Normal","&lt; 40","&lt; 40")]
    th="".join(f'<div style="font-weight:800;font-size:38px;color:{(R if i==3 else K) if i else G}">{h}</div>' for i,h in enumerate(H))
    tr="".join("".join(f'<div style="font-size:38px;font-weight:{800 if j==0 else 600};border-top:3px solid {K};padding-top:14px;{"color:"+R if j==3 else ""}">{c}</div>' for j,c in enumerate(r)) for r in D)
    return f'<div style="display:grid;grid-template-columns:1fr 1fr 1.1fr 1fr;gap:14px 20px">{th}{tr}</div>'
P=[
page(1,N,T,big("CRISIS DE ASMA",140,nowrap=True)+big(f'DECIDE EN LAS <span style="color:{R}">3 PRIMERAS HORAS</span>',112)+'<div style="font-size:40px;font-weight:600;line-height:1.3;max-width:820px">Gravedad, dosis de la primera hora y alta o ingreso, sin necesidad de PEF. Con ficha final.</div>',cover=True),
page(2,N,T,kicker("¿CUÁNTO ES GRAVE?")+big("LO QUE PUEDES MEDIR",118,nowrap=True)+tabla()+f'<div style="border-top:4px solid {K};padding-top:22px;font-size:38px;font-weight:800;line-height:1.3;color:{R}">Riesgo vital: PaCO2 &gt; 45, bradicardia, bradipnea, silencio auscultatorio o bajo nivel de consciencia → UCI</div>'+note("Leve: salbutamol. Moderada o grave: nebulización triple, corticoide y oxígeno.")),
page(3,N,T,kicker("PRIMERA HORA · NEBULIZA")+big("SALBUTAMOL",150,R,True)+rows(row("Nebulizado","2,5–5 mg cada 20 min"),row("Con cámara","2–8 puls. cada 10–15 min"))+big("+ IPRATROPIO + BUDESONIDA",92)+rows(row("Ipratropio","0,5 mg nebulizado cada 20 min"),row("Budesonida","0,5 mg nebulizada cada 20 min"))+note("En la misma nebulización, desde el inicio en la crisis moderada o grave. El corticoide inhalado precoz reduce ingresos.")),
page(4,N,T,kicker("PRIMERA HORA · OXÍGENO Y CORTICOIDE")+rows(row("Oxígeno","SatO2 &gt; 90 % (&gt; 95 % embarazo o cardiopatía)"))+big("CORTICOIDE PRONTO",116,R,True)+rows(row("Prednisona oral","50 mg"),row("Metilprednisolona IV","20–40 mg cada 8–12 h · o 80 mg en bolo"),row("Hidrocortisona IV","100–200 mg cada 6 h"))+note("Pauta de metilprednisolona: individualiza. Si hay riesgo de hipercapnia, oxígeno controlado y SatO2 en torno a 93–95 %.")),
page(5,N,T,kicker("SI NO RESPONDE")+big("ESCALA",170,R,True)+rows(row("Sulfato de magnesio IV","2 g en 20 min, dosis única"),line("Fracaso del tratamiento: VMNI sin retrasar la intubación si hay riesgo vital",True))+note("Adrenalina solo si hay anafilaxia. No uses teofilinas.")),
page(6,N,T,kicker("ALTA O INGRESO")+big("A LAS 3 HORAS, DECIDE",112)+rows(row("Alta","Síntomas mínimos y poco rescate"),row("Al alta","Prednisona 50 mg/día, 5–7 días, sin pauta descendente"),row("Ingreso","Necesita O2 para SatO2 &gt; 92 %"),row("Control","Médico de familia en &lt; 5 días"),redrow("UCI","SatO2 &lt; 90 % con O2, PaCO2 &gt; 45, bajo nivel de consciencia"))+note("Antes del alta: técnica inhalatoria y plan de acción por escrito.")),
page(7,N,T,ficha_body("CRISIS DE ASMA","Adulto",[("GRAVE","SatO2 &lt; 90 %, FR &gt; 25, FC &gt; 120. Riesgo vital: PaCO2 &gt; 45"),("NEBULIZA","Salbutamol 2,5–5 mg + ipratropio 0,5 mg + budesonida 0,5 mg cada 20 min (1.ª hora)",True),("CORTICOIDE","Prednisona 50 mg oral · metilprednisolona 20–40 mg/8–12 h o 80 mg en bolo IV: individualiza"),("SI NO CEDE","Sulfato de magnesio 2 g IV en 20 min · VMNI"),("OXÍGENO","SatO2 &gt; 90 % (&gt; 95 % embarazo o cardiopatía)"),("ALTA","Síntomas mínimos. Prednisona 50 mg 5–7 días, sin descenso",True)],"GEMA 5.5. Guía Española para el Manejo del Asma, 2025 (cap. 4); protocolo de Urgencias HUPM",size=130,fs=29),ficha="03"),
]
render(P,sys.argv[1] if len(sys.argv)>1 else "out","asma")
