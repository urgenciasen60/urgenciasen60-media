"""Epistaxis v3: ilustraciones vectoriales animadas (SVG -> JPG con rsvg-convert), 1080x1920.
Escenas: postura, pinza, algodon, rinos, nitrato, tapona, posterior. Cada escena recibe u en [0, 1].
Uso: python3 svg_epistaxis.py OUTDIR escena NFR   (genera OUTDIR/f_<escena>/000.jpg ...)"""
import math, os, subprocess, sys, random
W, H = 1080, 1920
BG = "#0B1118"; SKIN = "#D9A47F"; SKIN2 = "#B9805C"; MUC = "#E7A3A0"; MUC2 = "#C9706F"; CAV = "#5A1F24"; BONE = "#EFE6D2"
Y = "#FFD60A"; R = "#E0262C"; BLOOD = "#B3121A"; STEEL = "#C9CDD3"; COT = "#F4F1EA"; GREEN = "#2BB673"; INK = "#111111"
ease = lambda x: x*x*(3-2*x)
clamp = lambda x, a=0.0, b=1.0: max(a, min(b, x))
seg = lambda u, a, b: clamp((u-a)/(b-a))
def svg(body, bg=BG):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs><radialGradient id="vig" cx="50%" cy="45%" r="70%"><stop offset="60%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity="0.6"/></radialGradient>'
            f'<radialGradient id="luz" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FFF4E0" stop-opacity="0.55"/><stop offset="70%" stop-color="#FFF4E0" stop-opacity="0.08"/><stop offset="100%" stop-color="#000" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="acero" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2F4F7"/><stop offset="0.5" stop-color="#9AA1AA"/><stop offset="1" stop-color="#E3E6EA"/></linearGradient>'
            f'<filter id="sombra" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#000" flood-opacity="0.5"/></filter>'
            f'<filter id="blur4"><feGaussianBlur stdDeviation="4"/></filter></defs>'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}<rect width="{W}" height="{H}" fill="url(#vig)"/></svg>')
def mark(x, y, ok, s=1.0, op=1.0):
    if op <= 0: return ""
    if ok:
        return (f'<g opacity="{op:.3f}" transform="translate({x},{y}) scale({s})"><circle r="46" fill="{GREEN}"/>'
                f'<path d="M-22 2 L-6 18 L24 -16" stroke="#fff" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
    return (f'<g opacity="{op:.3f}" transform="translate({x},{y}) scale({s})"><circle r="46" fill="{R}"/>'
            f'<path d="M-18 -18 L18 18 M18 -18 L-18 18" stroke="#fff" stroke-width="11" stroke-linecap="round"/></g>')
# ------------------------------------------------------------------ perfil de cabeza y tronco (mira a la derecha)
HEAD = ("M 300 120 C 380 40 560 30 650 90 C 700 125 720 180 722 240 C 724 265 735 280 742 300 "
        "C 760 345 800 395 812 418 C 818 430 810 440 796 444 C 780 448 768 450 762 458 C 770 470 772 486 768 498 "
        "C 778 506 780 520 772 530 C 770 548 760 566 742 580 C 715 600 670 606 640 600 L 610 640 C 600 700 560 720 520 720 "
        "L 470 720 C 410 700 350 660 320 600 C 270 520 250 400 262 300 C 270 220 280 160 300 120 Z")
EAR = "M 410 330 C 380 300 350 320 352 360 C 354 400 380 420 405 410 C 420 400 425 360 410 330 Z"
def cabeza(x, y, ang, sangre_atras=0.0, sangre_fuera=0.0, mano=0.0, s=1.0):
    """cabeza de perfil con pivote en el cuello (520, 700) en coords locales; ang en grados (+ = flexión hacia delante)"""
    neck = (f'<path d="M 450 640 L 600 640 L 640 860 L 410 860 Z" fill="{SKIN2}"/>')
    torso = (f'<path d="M 250 840 C 330 800 520 790 720 830 C 820 850 880 960 900 1100 L 140 1100 C 150 960 180 870 250 840 Z" fill="#2E4A66"/>'
             f'<path d="M 470 812 C 520 845 600 845 640 812" stroke="#24405A" stroke-width="10" fill="none"/>')
    eye = f'<path d="M 650 262 C 664 254 680 256 690 266" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>'
    brow = f'<path d="M 640 225 C 660 214 690 214 706 224" stroke="#5B3B2A" stroke-width="9" fill="none" stroke-linecap="round"/>'
    hair = (f'<path d="M 300 120 C 380 40 560 30 650 90 C 690 115 705 150 700 170 C 640 140 560 150 500 170 C 430 190 380 240 360 300 '
            f'C 330 270 300 260 270 280 C 272 210 282 160 300 120 Z" fill="#3A2A20"/>')
    mouth = f'<path d="M 742 566 C 730 570 716 570 706 566" stroke="#8C4B3B" stroke-width="6" fill="none" stroke-linecap="round"/>'
    nostril = f'<ellipse cx="770" cy="452" rx="16" ry="7" fill="#6B3426" transform="rotate(-12 770 452)"/>'
    blood = ""
    if sangre_fuera > 0:   # gotas que salen por la narina hacia el suelo (en coords de pantalla, se añaden fuera)
        pass
    if sangre_atras > 0:   # mancha que baja por la faringe (vista en transparencia)
        blood = (f'<path d="M 740 455 C 690 455 640 462 610 490 C 585 515 572 560 568 620 C 566 680 568 720 572 760" stroke="{BLOOD}" stroke-width="16" '
                 f'fill="none" stroke-linecap="round" opacity="0.75" stroke-dasharray="{560*sangre_atras:.0f} 900"/>')
    hand = ""
    if mano > 0:
        k = ease(mano); dx, dy = 220*(1-k), 260*(1-k)
        line = lambda x0, y0, x1, y1, w: (f'<path d="M {x0} {y0} L {x1} {y1}" stroke="{SKIN2}" stroke-width="{w+8}" stroke-linecap="round"/>'
                                          f'<path d="M {x0} {y0} L {x1} {y1}" stroke="{SKIN}" stroke-width="{w}" stroke-linecap="round"/>')
        hand = (f'<g transform="translate({dx:.1f},{dy:.1f}) translate(780 446) scale(1.35) translate(-780 -446)" opacity="{min(1, mano*3):.3f}">'
                + line(930, 520, 1180, 700, 100) +
                f'<ellipse cx="900" cy="478" rx="66" ry="54" fill="{SKIN}" stroke="{SKIN2}" stroke-width="5" transform="rotate(20 900 478)"/>'
                f'<path d="M 856 500 C 870 520 900 526 924 518 M 862 470 C 880 490 905 494 930 486" stroke="{SKIN2}" stroke-width="5" fill="none"/>'
                + line(776, 446, 868, 446, 30) + line(800, 470, 870, 486, 28) +
                f'<path d="M 772 440 C 776 436 784 436 788 440" stroke="#F1D2BE" stroke-width="5" fill="none"/></g>')
    head = (f'<g transform="rotate({ang:.2f} 520 700)"><path d="{HEAD}" fill="{SKIN}"/>{hair}<path d="{EAR}" fill="{SKIN2}"/>'
            f'{brow}{eye}{nostril}{mouth}{blood}{hand}</g>')
    return f'<g transform="translate({x},{y}) scale({s})">{torso}{neck}{head}</g>'
def nose_point(x, y, ang, s=1.0):
    """posición en pantalla de la narina (770, 455) tras la rotación"""
    a = math.radians(ang); px, py = 770-520, 455-700
    rx = px*math.cos(a)-py*math.sin(a); ry = px*math.sin(a)+py*math.cos(a)
    return x+(520+rx)*s, y+(700+ry)*s
# ------------------------------------------------------------------ corte sagital de la fosa nasal (pared lateral), nariz a la derecha
# coords locales 0..1000 x 0..900
SAG_SKIN = ("M 120 40 C 300 0 560 10 700 60 C 760 90 780 150 790 210 C 800 260 840 320 900 400 C 930 440 935 470 915 490 "
            "C 890 505 860 505 840 500 C 850 520 850 540 838 552 C 820 600 760 640 700 660 L 640 900 L 80 900 L 60 300 C 60 160 80 70 120 40 Z")
CAVITY = ("M 300 300 C 360 250 480 215 600 215 C 690 215 740 240 770 290 C 800 340 840 400 868 448 C 875 462 868 476 852 478 "
          "L 820 480 C 810 500 790 510 760 512 L 330 512 C 300 512 280 500 270 480 L 262 420 C 262 370 275 330 300 300 Z")
PHARYNX = "M 262 420 C 230 440 215 520 218 600 C 220 700 232 800 240 900 L 330 900 C 322 800 316 700 318 620 C 320 560 320 530 330 512 Z"
PALATE = "M 320 512 L 800 512 C 812 512 818 520 812 530 L 790 560 L 330 560 C 314 560 306 548 312 536 Z"
TURB = [("M 380 498 C 430 448 600 440 700 452 C 740 458 748 478 730 492 C 700 512 520 514 420 512 C 395 511 380 506 380 498 Z", "inferior"),
        ("M 400 410 C 450 366 590 360 650 374 C 680 382 684 398 668 410 C 630 432 500 436 430 432 C 410 430 400 422 400 410 Z", "medio"),
        ("M 430 322 C 470 296 560 292 590 302 C 606 308 604 320 590 326 C 560 338 490 340 450 338 C 436 336 428 330 430 322 Z", "superior")]
def sagital(x, y, s=1.0, extra="", posterior=0.0, labels=0.0):
    t = [f'<path d="{SAG_SKIN}" fill="{SKIN}"/>',
         f'<path d="M 120 40 C 300 0 560 10 700 60 C 720 70 735 82 746 98 L 640 160 C 520 120 300 110 160 150 Z" fill="{BONE}" opacity="0.9"/>',
         f'<path d="{CAVITY}" fill="{CAV}"/>', f'<path d="{PHARYNX}" fill="{CAV}"/>',
         f'<path d="{PALATE}" fill="{BONE}"/>',
         f'<path d="M 300 300 C 360 250 480 215 600 215 C 690 215 740 240 770 290" stroke="{BONE}" stroke-width="10" fill="none"/>']
    for d, n in TURB:
        t.append(f'<path d="{d}" fill="{MUC}" stroke="{MUC2}" stroke-width="5"/>')
    t.append(f'<path d="M 330 512 L 810 512" stroke="{MUC2}" stroke-width="6"/>')
    if posterior > 0:
        k = ease(posterior)
        t.append(f'<path d="M 300 470 C 270 500 250 560 248 {560+260*k:.0f}" stroke="{BLOOD}" stroke-width="30" fill="none" stroke-linecap="round"/>'
                 f'<circle cx="305" cy="465" r="{16+6*math.sin(posterior*20):.1f}" fill="{BLOOD}"/>')
    if labels > 0:
        op = ease(labels)
        t.append(f'<g opacity="{op:.3f}" font-family="Inter" font-weight="800" font-size="34" fill="#fff">'
                 f'<text x="540" y="590">SUELO DE LA FOSA</text><text x="140" y="250">NASOFARINGE</text></g>')
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(t)}{extra}</g>'
def pinza_bayoneta(tip_x, tip_y, ang, carga=None):
    """pinza de bayoneta: punta en (tip_x, tip_y), el mango sale hacia la derecha-arriba; ang: inclinación del tramo distal (grados)"""
    body = (f'<path d="M 0 -4 L 230 -4 L 260 -46 L 600 -60 L 600 -40 L 268 -28 L 238 6 L 0 6 Z" fill="url(#acero)" stroke="#6B727C" stroke-width="2"/>'
            f'<path d="M 0 2 L 232 2 L 262 -34" stroke="#6B727C" stroke-width="2" fill="none"/>')
    c = ""
    if carga == "algodon":
        c = f'<ellipse cx="-8" cy="0" rx="40" ry="17" fill="{COT}" stroke="#D8D2C4" stroke-width="3"/><ellipse cx="-14" cy="-4" rx="20" ry="7" fill="#fff" opacity="0.7"/>'
    return f'<g transform="translate({tip_x},{tip_y}) rotate({ang})">{c}{body}</g>'
def esponja(x, y, ang, L=330, k=0.0, cord=True):
    """esponja expansible: k 0 = plana; 1 = expandida"""
    th = 16+38*k
    col = "#EFE7D6" if k < 0.3 else "#E2CDB8"
    pores = "".join(f'<circle cx="{-L+12+i*22}" cy="{(-th/2+6+((i*7) % 5)*th/6):.1f}" r="2.4" fill="#C9BBA2"/>' for i in range(int(L/22)))
    s = (f'<g transform="translate({x},{y}) rotate({ang})"><rect x="{-L}" y="{-th/2:.1f}" width="{L}" height="{th:.1f}" rx="{6+8*k:.1f}" fill="{col}" stroke="#BFAE92" stroke-width="3"/>{pores}')
    if cord: s += f'<path d="M 0 0 C 60 10 110 -20 190 6" stroke="#1E4FB8" stroke-width="5" fill="none"/>'
    return s+"</g>"
def timer(x, y, frac, txt):
    a = 2*math.pi*frac; ex = x+70*math.sin(a); ey = y-70*math.cos(a); large = 1 if frac > 0.5 else 0
    arc = f'<path d="M {x} {y-70} A 70 70 0 {large} 1 {ex:.1f} {ey:.1f}" stroke="{Y}" stroke-width="14" fill="none" stroke-linecap="round"/>' if frac > 0.001 else ""
    return (f'<circle cx="{x}" cy="{y}" r="70" stroke="#2A3440" stroke-width="14" fill="#0B1118"/>{arc}'
            f'<text x="{x}" y="{y+16}" text-anchor="middle" font-family="Inter" font-weight="900" font-size="44" fill="#fff">{txt}</text>')
# ------------------------------------------------------------------ vista de rinoscopia anterior (a través del espéculo, con luz frontal)
random.seed(7)
def _vessels(cx, cy, n, r):
    out = []
    for i in range(n):
        x, y = cx+random.uniform(-r, r), cy+random.uniform(-r, r); pts = [(x, y)]
        a = random.uniform(0, 2*math.pi)
        for j in range(7):
            a += random.uniform(-0.7, 0.7); x += 22*math.cos(a); y += 22*math.sin(a); pts.append((x, y))
        d = "M "+" L ".join(f"{p[0]:.1f} {p[1]:.1f}" for p in pts)
        out.append((d, random.uniform(2.5, 6)))
    return out
VES = _vessels(430, 960, 26, 120)
def rinos(u_cau=0.0, stick=0.0, point=1.0, side_note=0.0, clot=0.0):
    cx, cy, R0 = 540, 960, 420
    clip = f'<clipPath id="ojo"><circle cx="{cx}" cy="{cy}" r="{R0}"/></clipPath>'
    s = [f'<defs>{clip}</defs><g clip-path="url(#ojo)">',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="#3A0E12"/>',
         # tabique a la izquierda (vertical), cornete inferior a la derecha, suelo abajo
         f'<path d="M 120 520 C 260 540 400 600 470 700 C 520 780 520 1150 470 1300 C 430 1400 260 1420 120 1420 Z" fill="{MUC}"/>',
         f'<path d="M 960 760 C 820 760 700 840 660 960 C 630 1060 680 1200 800 1260 C 880 1300 960 1300 980 1290 Z" fill="#D88C88"/>',
         f'<path d="M 120 1290 C 360 1240 700 1260 980 1320 L 980 1420 L 120 1420 Z" fill="#C97A78"/>',
         f'<ellipse cx="600" cy="1060" rx="70" ry="160" fill="#2A0709" opacity="0.85"/>']
    for d, w in VES:
        s.append(f'<path d="{d}" stroke="#B2343C" stroke-width="{w:.1f}" fill="none" stroke-linecap="round" opacity="0.75"/>')
    px, py = 430, 960
    if point > 0:
        if u_cau < 1:
            s.append(f'<circle cx="{px}" cy="{py}" r="{18*(1-u_cau)+4:.1f}" fill="{BLOOD}"/>'
                     f'<path d="M {px} {py} C {px+10} {py+80} {px-6} {py+160} {px+4} {py+260*point*(1-u_cau):.0f}" stroke="{BLOOD}" stroke-width="{16*(1-u_cau)+1:.1f}" fill="none" stroke-linecap="round"/>')
        if u_cau > 0:
            s.append(f'<circle cx="{px}" cy="{py}" r="{34*ease(u_cau):.1f}" fill="#8E8F92" opacity="0.92"/><circle cx="{px-8}" cy="{py-8}" r="{12*ease(u_cau):.1f}" fill="#D7D8DA" opacity="0.8"/>')
    if clot > 0:
        s.append(f'<path d="M 380 1100 C 420 1080 470 1120 460 1180 C 450 1240 380 1250 360 1200 C 340 1160 350 1120 380 1100 Z" fill="#4A0508" opacity="{clot:.2f}"/>')
    if stick > 0:
        k = ease(stick); sx, sy = px+20+500*(1-k), py+30+700*(1-k)
        s.append(f'<g transform="translate({sx:.1f},{sy:.1f}) rotate(-58)"><rect x="0" y="-9" width="900" height="18" rx="9" fill="#C8A37A"/>'
                 f'<ellipse cx="-6" cy="0" rx="26" ry="14" fill="#3C3D40"/></g>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R0}" fill="url(#luz)"/></g>')
    # palas del espéculo (arriba y abajo) y aro
    s.append(f'<path d="M {cx-R0} {cy-R0+40} C {cx-200} {cy-330} {cx+200} {cy-330} {cx+R0} {cy-R0+40} L {cx+R0} {cy-R0-60} L {cx-R0} {cy-R0-60} Z" fill="url(#acero)" opacity="0.95"/>')
    s.append(f'<path d="M {cx-R0} {cy+R0-40} C {cx-200} {cy+330} {cx+200} {cy+330} {cx+R0} {cy+R0-40} L {cx+R0} {cy+R0+60} L {cx-R0} {cy+R0+60} Z" fill="url(#acero)" opacity="0.95"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R0}" stroke="#05080B" stroke-width="40" fill="none"/>')
    if side_note > 0:
        op = ease(side_note)
        s.append(f'<g opacity="{op:.3f}" font-family="Inter" font-weight="800" font-size="34" fill="#fff"><text x="190" y="560">TABIQUE</text><text x="760" y="740">CORNETE</text></g>')
    return "".join(s)
# ------------------------------------------------------------------ escenas
def scene(name, u):
    b = []
    if name == "postura":        # 0-0.45 cabeza atrás (mal); 0.45-1 hacia delante (bien)
        k = ease(seg(u, 0.42, 0.62)); ang = -24+46*k
        b.append(cabeza(40, 520, ang))
        b.append(mark(880, 600, False, 1.3, seg(u, 0.12, 0.2)*(1-seg(u, 0.4, 0.46))))
        if u > 0.55:
            nx, ny = nose_point(40, 520, ang)
            for i in range(3):
                ph = (u*2.2-i*0.33) % 1
                b.append(f'<ellipse cx="{nx:.0f}" cy="{ny+30+340*ph*ph:.0f}" rx="9" ry="13" fill="{BLOOD}" opacity="{1-ph*0.6:.2f}"/>')
            b.append(mark(880, 600, True, 1.3, seg(u, 0.68, 0.76)))
    elif name == "pinza":        # mano propia pinzando el ala; temporizador
        ang = 22
        b.append(cabeza(-40, 520, ang, mano=seg(u, 0.0, 0.35)))
        b.append(timer(900, 460, seg(u, 0.35, 1.0), "5 min"))
        if u > 0.5:
            nx, ny = nose_point(-40, 520, ang)
            b.append(f'<g opacity="{ease(seg(u, 0.5, 0.62)):.3f}"><path d="M {nx+15:.0f} {ny-25:.0f} L {nx+110:.0f} {ny-300:.0f}" stroke="{Y}" stroke-width="7"/>'
                     f'<text x="1040" y="{ny-320:.0f}" text-anchor="end" font-family="Inter" font-weight="900" font-size="40" fill="{Y}">PARTE BLANDA</text></g>')
    elif name == "algodon":      # pinza de bayoneta deja el algodón a lo largo del suelo
        k = ease(seg(u, 0.05, 0.6)); tip_x = 1020-360*k; tip_y = 1020+60*(1-k)
        extra = ""
        b.append(sagital(40, 520, 1.0, labels=seg(u, 0.55, 0.7)))
        b.append(pinza_bayoneta(40+tip_x*1.0-40, 520+(470)*1.0+2, -2, "algodon") if False else "")
        b.append(f'<g transform="translate(40,520)">{pinza_bayoneta(tip_x-40+(-0), 485, -3, "algodon")}</g>')
        b.append(timer(870, 470, seg(u, 0.65, 1.0), "10 min"))
    elif name == "rinos":
        b.append(rinos(point=1.0, side_note=seg(u, 0.35, 0.5), clot=1-seg(u, 0.0, 0.3)))
    elif name == "nitrato":
        b.append(rinos(stick=seg(u, 0.0, 0.35)*(1-seg(u, 0.85, 1.0)), u_cau=seg(u, 0.35, 0.75)))
        b.append(mark(880, 560, True, 1.2, seg(u, 0.75, 0.85)))
    elif name == "tapona":       # 0-0.45 paralela al suelo (bien); 0.5-0.75 hacia el dorso (mal, tachada); 0.8-1 se expande
        k = ease(seg(u, 0.05, 0.45)); NX, NY = 40+905, 520+497
        b.append(sagital(40, 520, 1.0, labels=seg(u, 0.1, 0.25)))
        b.append(esponja(NX+300*(1-k), NY, 0, 330, k=ease(seg(u, 0.8, 1.0))))
        wrong = min(1, seg(u, 0.5, 0.58)*1.0)*(1-seg(u, 0.74, 0.8))
        if wrong > 0:
            kw = ease(seg(u, 0.5, 0.66))
            b.append(f'<g opacity="{wrong:.3f}">{esponja(NX+40+260*(1-kw)*0.82, NY-30-260*(1-kw)*0.57, 35, 300, cord=False)}</g>')
            b.append(mark(700, 760, False, 1.2, wrong*seg(u, 0.62, 0.66)))
        b.append(mark(880, 440, True, 1.2, seg(u, 0.3, 0.4)*(1-seg(u, 0.48, 0.52))+seg(u, 0.85, 0.92)))
    elif name == "posterior":
        b.append(sagital(40, 520, 1.0, posterior=seg(u, 0.05, 0.6)))
        b.append(f'<g opacity="{ease(seg(u, 0.55, 0.7)):.3f}"><rect x="660" y="400" width="340" height="110" rx="16" fill="{R}"/>'
                 f'<text x="830" y="477" text-anchor="middle" font-family="Anton" font-size="72" fill="#fff">ORL</text></g>')
    return svg("".join(b))
if __name__ == "__main__":
    out, name, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
    d = f"{out}/f_{name}"; os.makedirs(d, exist_ok=True)
    only = [int(sys.argv[4])] if len(sys.argv) > 4 else range(n)
    for i in only:
        u = i/(n-1) if n > 1 else 0.0; p = f"{d}/{i:03d}"
        open(p+".svg", "w").write(scene(name, u))
        subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", p+".png", p+".svg"], check=True)
        from PIL import Image
        Image.open(p+".png").convert("RGB").save(p+".jpg", quality=93); os.remove(p+".png"); os.remove(p+".svg")
