"""Imágenes de elaboración propia para Cuenta atrás MIR · Ep. 02 (no son de pacientes reales).
python3 tools/mir_ep02_imagenes.py <dir_salida>
- rx_neumoperitoneo.png: radiografía de tórax PA en bipedestación con aire libre bajo ambos hemidiafragmas.
- tc_gas_portal.png: TC axial con contraste (fase portal), ventana abdominal, con gas portal periférico,
  defecto de repleción en la AMS y neumatosis de un asa de yeyuno."""
import os, sys
import numpy as np
from scipy import ndimage as ndi
from PIL import Image, ImageDraw, ImageFont

FB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
FS = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"

def norm01(a):
    a = a - a.min(); return a / (a.max() + 1e-9)

def blob(shape, cx, cy, rx, ry, rot=0.0, irr=0.06, seed=0, k=6):
    """Máscara de forma orgánica: elipse con radio modulado por armónicos aleatorios."""
    r_ = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]].astype(float)
    X = (xx - cx) * np.cos(rot) + (yy - cy) * np.sin(rot)
    Y = -(xx - cx) * np.sin(rot) + (yy - cy) * np.cos(rot)
    th = np.arctan2(Y / ry, X / rx)
    mod = 1 + sum(r_.normal(0, irr / (n ** 0.7)) * np.cos(n * th + r_.uniform(0, 6.28)) for n in range(2, k + 2))
    return np.sqrt((X / rx) ** 2 + (Y / ry) ** 2) < mod

def poly(shape, pts, smooth=6):
    im = Image.new("L", (shape[1], shape[0]), 0)
    ImageDraw.Draw(im).polygon([tuple(p) for p in pts], fill=255)
    return ndi.gaussian_filter(np.asarray(im, float) / 255, smooth) > 0.5

def lowfreq(shape, s, seed):
    return norm01(ndi.gaussian_filter(np.random.default_rng(seed).normal(size=shape), s)) - 0.5

def caption(img, left, right):
    d = ImageDraw.Draw(img); f = ImageFont.truetype(FS, 21)
    d.text((18, img.height - 32), left, fill=(225, 225, 225), font=f)
    w = d.textlength(right, font=f); d.text((img.width - w - 18, img.height - 32), right, fill=(225, 225, 225), font=f)
    d.text((22, 16), "D", fill=(235, 235, 235), font=ImageFont.truetype(FB, 32))
    return img

def paint(arr, pts, H, W):
    for a, b in pts:
        if 0 <= int(b) < H and 0 <= int(a) < W: arr[int(b), int(a)] = 1

# ======================================================================= RADIOGRAFÍA
def rx(path):
    rng = np.random.default_rng(11)
    H, W = 1200, 1100
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    cx = W / 2
    xr = np.arange(W, dtype=float)
    def dome(x, x0, x1, top, depth, skew):
        t = np.clip((x - x0) / (x1 - x0), 0, 1) ** skew
        return top + depth * (1 - np.sin(np.pi * t)) ** 1.6
    dia = np.where(xr < 550, dome(xr, 140, 545, 780, 230, 0.85), dome(xr, 555, 975, 810, 230, 1.15))
    below = yy > dia[None, :]
    trunk = blob((H, W), cx, 720, 520, 900, irr=0.01, seed=1)
    img = np.where(trunk, 0.52, 0.03)
    img += 0.10 * np.clip(np.abs(xx - cx) / 520, 0, 1) ** 3 * trunk
    lungR = poly((H, W), [(205, 260), (300, 150), (420, 130), (480, 220), (490, 420), (470, 560), (440, 700), (330, 800), (180, 960), (150, 760), (160, 450)], 14)
    lungL = poly((H, W), [(640, 140), (760, 130), (860, 210), (930, 450), (950, 760), (930, 990), (800, 860), (690, 820), (640, 640), (650, 470), (620, 260)], 14)
    lungs = ndi.gaussian_filter(((lungR | lungL) & ~below).astype(float), 7)
    img = img - 0.33 * lungs * (1 - 0.25 * np.clip((yy - 150) / 900, 0, 1))
    vasc = np.zeros((H, W))
    def vessel(x, y, ang, L, w, depth):
        for _ in range(int(L / 3)):
            ang += rng.normal(0, 0.045); x += 3 * np.cos(ang); y += 3 * np.sin(ang)
            if 0 <= int(y) < H and 0 <= int(x) < W: vasc[int(y), int(x)] += w
        if depth > 0:
            for da in (-0.42, 0.38): vessel(x, y, ang + da + rng.normal(0, 0.12), L * 0.7, w * 0.72, depth - 1)
    for hx, hy, base, sg in [(470, 470, np.pi, -1), (650, 480, 0.0, 1)]:
        for a in np.linspace(-1.2, 1.2, 8): vessel(hx, hy, base + sg * a, rng.uniform(70, 120), 1.0, 2)
    vasc = ndi.gaussian_filter(ndi.grey_dilation(vasc, size=(3, 3)), 3.0)
    img += 0.08 * np.clip(vasc / np.percentile(vasc[vasc > 0], 97), 0, 1) * lungs
    for hx, hy, sx, sy in [(468, 470, 32, 75), (655, 485, 30, 70)]:
        img += 0.12 * np.exp(-(((xx - hx) / sx) ** 2 + ((yy - hy) / sy) ** 2)) * lungs
    med = poly((H, W), [(495, 120), (610, 120), (640, 300), (690, 330), (690, 400), (650, 450), (760, 540), (840, 700), (820, 800), (700, 830), (520, 820), (430, 790), (430, 640), (470, 520), (480, 330)], 10)
    img += (0.17 + 0.07 * np.clip((yy - 300) / 300, 0, 1)) * ndi.gaussian_filter((med & ~below).astype(float), 12)
    img += (0.03 + 0.02 * np.cos(2 * np.pi * yy / 62) ** 8) * np.exp(-(((xx - 555) / 32) ** 6)) * (yy > 120)
    img -= 0.06 * ndi.gaussian_filter(((np.abs(xx - 552) < 15) & (yy > 100) & (yy < 380)).astype(float), 4)
    ribs = np.zeros((H, W))
    for side in (-1, 1):
        for k in range(9):
            y0 = 190 + k * 66 + (8 if side > 0 else 0); lenx = 380 + 12 * min(k, 4); width = 22 + k
            t = np.linspace(0, 1, 600)
            for a, b in zip(cx + side * (75 + lenx * t), y0 - 30 * np.sin(np.pi * t * 0.6) + 170 * t ** 2.4):
                ia, ib = int(a), int(b)
                if 0 <= ib < H and 0 <= ia < W: ribs[max(0, ib - width // 2): ib + width // 2, ia] = 1
    ribs = ndi.gaussian_filter(ribs, 3.2)
    edges = ndi.gaussian_filter(np.abs(ndi.sobel(ribs, axis=0)), 1.2)
    img += (0.045 * ribs + 0.035 * norm01(edges)) * np.clip((np.abs(xx - cx) - 80) / 90, 0, 1) * trunk * (~below | (yy < dia[None, :] + 40))
    ant = np.zeros((H, W))
    for side in (-1, 1):
        for k in range(6):
            t = np.linspace(0, 1, 400)
            for a, b in zip(cx + side * (420 - 300 * t), 300 + k * 85 + 150 * t):
                if 0 <= int(b) < H and 0 <= int(a) < W: ant[int(b) - 6:int(b) + 6, int(a)] = 1
    img += 0.035 * ndi.gaussian_filter(ant, 3) * trunk
    for side in (-1, 1):
        cl = np.zeros((H, W)); t = np.linspace(0, 1, 400)
        for a, b in zip(cx + side * (60 + 330 * t), 175 - 40 * t + 30 * t ** 2): cl[int(b) - 12:int(b) + 12, int(a)] = 1
        img += 0.13 * ndi.gaussian_filter(cl, 3)
    img = np.where(below & trunk, 0.57 + 0.05 * lowfreq((H, W), 40, 3) - 0.06 * np.clip(np.abs(xx - cx) / 520, 0, 1) ** 2, img)
    dist = yy - dia[None, :]
    def crescent(x0, x1, peak, seed):
        t = np.clip((xx - x0) / (x1 - x0), 0, 1)
        th = peak * np.sin(np.pi * t) ** 1.3 * (1 + 0.25 * lowfreq((H, W), 25, seed))
        return (dist > 11) & (dist < 11 + th) & (xx > x0) & (xx < x1)
    air = crescent(200, 515, 27, 5) | crescent(610, 895, 19, 6)
    img = np.where(air, 0.21, img)
    img = np.where((dist > 0) & (dist <= 11) & trunk, 0.55, img)
    gb = blob((H, W), 760, dia[760] + 105, 62, 34, irr=0.08, seed=9) & (yy < dia[760] + 108)
    img = np.where(gb, 0.22, img)
    img = np.where(gb & (yy > dia[760] + 100), 0.60, img)
    img += 0.05 * lowfreq((H, W), 60, 21) * trunk
    img = ndi.gaussian_filter(img, 2.2)
    img += 0.012 * ndi.gaussian_filter(rng.normal(size=(H, W)), 1.0) + 0.012 * rng.normal(size=(H, W))
    img = np.clip(img * (1 - 0.55 * (((xx - cx) / W) ** 2 + ((yy - H * 0.45) / H) ** 2)), 0, 1)
    img = norm01(1 / (1 + np.exp(-(norm01(img) - 0.5) * 5.2)))
    out = Image.fromarray((img * 255).astype(np.uint8)).convert("RGB")
    out = out.crop((70, 540, 1030, 1060)).resize((920, 498))
    caption(out, "Rx tórax PA en bipedestación", "Imagen elaborada para docencia")
    out.save(path)

# ================================================================================ TC
def tc(path):
    rng = np.random.default_rng(3)
    N = 1000; S = (N, N)
    yy, xx = np.mgrid[0:N, 0:N].astype(float)
    cx, cy = 500, 500
    HU = np.full(S, -1000.0)
    body = blob(S, cx, cy, 440, 330, irr=0.025, seed=1); HU[body] = -105
    wall = blob(S, cx, cy + 5, 412, 300, irr=0.025, seed=2)
    cav = blob(S, cx, cy + 10, 392, 280, irr=0.03, seed=3)
    HU[wall & ~cav] = 55; HU[cav] = -95
    for side in (-1, 1):
        HU[blob(S, cx + side * 70, cy - 268, 62, 16, irr=0.05, seed=4 + side) & body] = 55
        HU[blob(S, cx + side * 150, cy + 250, 85, 40, rot=side * 0.35, irr=0.05, seed=6 + side) & body] = 55
    for side in (-1, 1):
        for i, ang in enumerate(np.linspace(0.25, 1.45, 5)):
            px = cx + side * 405 * np.cos(ang); py = cy - 295 * np.sin(ang) * 0.9 + 20
            HU[blob(S, px, py, 15, 10, rot=side * ang, irr=0.05, seed=30 + i)] = 600
            HU[blob(S, px, py, 10, 6, rot=side * ang, irr=0.05, seed=30 + i)] = 180
        for i, ang in enumerate(np.linspace(-0.55, -0.1, 3)):
            px = cx + side * 395 * np.cos(ang); py = cy - 290 * np.sin(ang)
            HU[blob(S, px, py, 13, 11, irr=0.05, seed=40 + i)] = 650
            HU[blob(S, px, py, 8, 6, irr=0.05, seed=40 + i)] = 200
    liver = (blob(S, 300, 470, 205, 245, rot=-0.15, irr=0.05, seed=12) | blob(S, 445, 330, 130, 85, rot=-0.35, irr=0.06, seed=13)) & cav
    liver &= ~blob(S, 470, 520, 90, 110, irr=0.04, seed=14)
    HU[liver] = (112 + 6 * lowfreq(S, 30, 15))[liver]
    HU[blob(S, 395, 420, 30, 22, rot=0.6, irr=0.04, seed=16)] = 8
    spleen = blob(S, 815, 560, 62, 110, rot=0.45, irr=0.06, seed=17) & cav; HU[spleen] = 118
    st_o = blob(S, 650, 355, 115, 78, rot=0.25, irr=0.07, seed=18) & cav & ~liver
    st_i = blob(S, 650, 357, 99, 63, rot=0.25, irr=0.07, seed=18)
    HU[st_o] = 95; HU[st_o & st_i] = 18; HU[st_o & st_i & (yy < 318)] = -980
    panc = blob(S, 615, 555, 135, 26, rot=-0.12, irr=0.1, seed=19) & cav
    HU[panc] = (96 + 10 * lowfreq(S, 6, 20))[panc]
    for side, seed in ((-1, 21), (1, 22)):
        k_o = blob(S, cx + side * 200, 650, 62, 78, rot=side * -0.5, irr=0.04, seed=seed)
        k_i = blob(S, cx + side * 200, 650, 38, 52, rot=side * -0.5, irr=0.08, seed=seed + 5)
        HU[k_o & cav] = 165; HU[k_i & cav] = 120
    vb_o = blob(S, cx, 690, 72, 62, irr=0.02, seed=23); vb_i = blob(S, cx, 690, 62, 52, irr=0.02, seed=23)
    HU[vb_o] = 750; HU[vb_i] = (230 + 40 * lowfreq(S, 3, 24))[vb_i]
    canal = blob(S, cx, 785, 26, 24, irr=0.02, seed=26)
    HU[blob(S, cx, 790, 82, 52, irr=0.03, seed=25) & ~canal & (yy > 745)] = 620; HU[canal] = 30
    HU[blob(S, cx, 860, 16, 32, irr=0.04, seed=27)] = 620
    for side in (-1, 1):
        HU[blob(S, cx + side * 95, 775, 34, 14, rot=side * 0.3, irr=0.05, seed=28)] = 600
        HU[blob(S, cx + side * 72, 630, 20, 60, rot=side * 0.25, irr=0.05, seed=50 + side) & cav] = 60
    HU[blob(S, cx + 25, 610, 30, 30, irr=0.01, seed=31)] = 175
    HU[blob(S, 440, 585, 32, 22, rot=0.3, irr=0.03, seed=32)] = 150
    ams = blob(S, cx + 22, 540, 13, 13, irr=0.01, seed=33)
    sv = np.zeros(S, bool); t = np.linspace(0, 1, 400)
    for a, b in zip(cx + 10 + 250 * t, 585 - 15 * np.sin(np.pi * t)): sv[int(b), int(a)] = True
    sv = ndi.binary_dilation(sv, iterations=7) & cav & ~ams; HU[sv] = 150
    HU[ams] = 170; HU[blob(S, cx + 24, 541, 8, 8, irr=0.01, seed=33)] = 45
    HU[blob(S, cx - 22, 540, 17, 15, irr=0.02, seed=34)] = 150
    vess = np.zeros(S)
    def branch(arr, x, y, ang, L, w, depth, jitter=0.05):
        for _ in range(int(L / 2)):
            x += 2 * np.cos(ang); y += 2 * np.sin(ang); ang += rng.normal(0, jitter)
            if 0 <= int(y) < N and 0 <= int(x) < N: arr[int(y), int(x)] = max(arr[int(y), int(x)], w)
        if depth > 0:
            for da in (-0.55, 0.45): branch(arr, x, y, ang + da + rng.normal(0, 0.1), L * 0.68, w * 0.78, depth - 1, jitter)
    branch(vess, 430, 500, -2.6, 70, 1.0, 4); branch(vess, 430, 500, -1.95, 75, 0.95, 4); branch(vess, 430, 500, 2.75, 60, 0.9, 3)
    vmask = ndi.gaussian_filter(ndi.grey_dilation(vess, size=(6, 6)), 2.0)
    HU = np.where(liver, HU + 45 * np.clip(vmask * 1.4, 0, 1), HU)
    gas = np.zeros(S)
    capd = ndi.distance_transform_edt(liver)
    for j in range(16):
        a0 = rng.uniform(-3.0, -0.9) if j < 11 else rng.uniform(2.3, 3.1)
        rr = rng.uniform(0.55, 0.75)
        x0 = 330 + 190 * rr * np.cos(a0) * 1.1; y0 = 470 + 240 * rr * np.sin(a0) * 0.95
        branch(gas, x0, y0, a0 + rng.normal(0, 0.25), rng.uniform(16, 30), 1.0, 2, 0.15)
    gas = ndi.gaussian_filter(ndi.grey_dilation(gas, size=(2, 2)), 0.8) * (capd > 5) * (capd < 110) * liver
    HU = np.where(gas > 0.2, HU - 1000 * np.clip(gas * 1.6, 0, 1), HU)
    loops = [(625, 478, 56, 38, 0.15, True), (745, 470, 34, 28, -0.3, False), (760, 650, 40, 30, 0.2, False), (650, 690, 38, 30, -0.5, False)]
    for i, (lx, ly, a, b, rot, isq) in enumerate(loops):
        o = blob(S, lx, ly, a, b, rot=rot, irr=0.05, seed=60 + i) & cav & ~st_o & ~spleen & ~panc
        inn = blob(S, lx, ly, a - (5 if isq else 8), b - (5 if isq else 8), rot=rot, irr=0.05, seed=60 + i)
        HU[o] = 30 if isq else 150
        HU[o & inn] = 14 if isq else 22
        if isq:
            th = np.arctan2(yy - ly, xx - lx)
            bub = (o & ~inn) & ((th < 0.4) | (th > 2.0)) & (rng.random(S) < 0.08)
            bub = ndi.binary_dilation(bub, iterations=2) & o & ~blob(S, lx, ly, a - 9, b - 9, rot=rot, irr=0.05, seed=60 + i)
            HU[bub] = -850
    HU = np.where(cav & (HU > -500) & (HU < 300), HU + 14 * lowfreq(S, 2, 71) * 2, HU)
    fat = (HU < -80) & (HU > -110) & cav
    HU = np.where(fat, HU + 25 * np.clip(lowfreq(S, 3, 70) * 2, 0, 1), HU)
    HU = ndi.gaussian_filter(HU, 1.4) + rng.normal(0, 16, S)
    HU = ndi.gaussian_filter(HU, 0.7)
    lo, hi = 50 - 210, 50 + 210
    img = np.clip((HU - lo) / (hi - lo), 0, 1)
    out = Image.fromarray((img * 255).astype(np.uint8)).convert("RGB")
    out = out.crop((60, 170, 940, 700)).resize((920, 554))
    caption(out, "TC abdominal con contraste IV · corte axial", "Imagen elaborada para docencia")
    out.save(path)

if __name__ == "__main__":
    o = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "."); os.makedirs(o, exist_ok=True)
    which = sys.argv[2] if len(sys.argv) > 2 else "both"
    if which in ("both", "rx"): rx(os.path.join(o, "rx_neumoperitoneo.png"))
    if which in ("both", "tc"): tc(os.path.join(o, "tc_gas_portal.png"))
    print("ok")
