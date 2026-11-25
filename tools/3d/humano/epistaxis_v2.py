"""Epistaxis v2 (25/11/2026): escenas externas con el paciente de alta calidad (paciente.py).
Paciente sentado e inclinado hacia delante; mano con guante mate que pinza el tercio inferior de la nariz; pinza de bayoneta
con algodón empapado entrando en la fosa. Fondo negro y luz cálida de estudio, como la punción lumbar v4.
Uso: python3 epistaxis_v2.py -- stills RES SAMPLES [planos...]
     python3 epistaxis_v2.py -- anim RES SAMPLES intro|pinza|algodon F0 F1   (NFR = fotogramas totales)"""
import bpy, sys, os, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from mathutils import Vector, Matrix
A = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
OUT = os.environ.get("EPIOUT", "/home/claude/v3d/epi"); os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
import paciente, humano, mano
from humano import X
from paciente import mat
SEAT = {"spine05": (X, 20), "spine04": (X, 8), "spine03": (X, 6), "spine02": (X, 4), "spine01": (X, 2), "neck01": (X, -6), "neck02": (X, -4), "head": (X, 4),
        "upperleg01.L": ("dir", (0.02, -0.98, 0.12)), "upperleg01.R": ("dir", (-0.02, -0.98, 0.12)),
        "lowerleg01.L": ("dir", (0.0, 0.08, -1)), "lowerleg01.R": ("dir", (0.0, 0.08, -1)),
        "upperarm01.L": ("dir", (0.15, -0.25, -0.95)), "upperarm01.R": ("dir", (-0.15, -0.25, -0.95)),
        "lowerarm01.L": ("dir", (-0.25, -0.90, -0.35)), "lowerarm01.R": ("dir", (0.25, -0.90, -0.35))}
P = paciente.crear(SEAT); ob = P["ob"]; REST = P["REST"]; eyec = P["eyec"]
OBJS = [ob, P["eyes"], P["top"], P["bot"]]
zmin = min(v.co.z for v in ob.data.vertices)
for o in OBJS: o.matrix_world = Matrix.Translation((0, 0, -zmin))@o.matrix_world
bpy.context.view_layer.update()
VW = [ob.matrix_world@v.co for v in ob.data.vertices]
# referencias de la nariz
mid = [i for i, p in enumerate(REST) if abs(p[0]) < 0.004 and eyec.z-0.075 < p[2] < eyec.z-0.01]
itip = min(mid, key=lambda i: REST[i][1]); NOSE = VW[itip]
iback = [i for i, p in enumerate(REST) if abs(p[0]) < 0.006 and abs(p[2]-REST[itip][2]) < 0.006]
FACEDIR = (NOSE-VW[max(iback, key=lambda i: REST[i][1])]).normalized()          # hacia delante en el marco de la cabeza
UP = (VW[min(mid, key=lambda i: -REST[i][2])]-NOSE); UP = (UP-FACEDIR*UP.dot(FACEDIR)).normalized()   # hacia la frente
SIDE = FACEDIR.cross(UP).normalized()
SOFT = NOSE-FACEDIR*0.011-UP*0.002                                            # parte blanda (tercio inferior)
# narina izquierda: vértice más profundo de la base de la nariz a ese lado
rt = REST[itip]
cand = [i for i, p in enumerate(REST) if 0.004 < p[0] < 0.014 and rt[2]-0.020 < p[2] < rt[2]-0.006 and p[1] < rt[1]+0.025]
NOSTRIL = VW[max(cand, key=lambda i: REST[i][1])] if cand else NOSE-UP*0.012
# taburete negro y suelo invisible
STOOL = mat("taburete", (0.008, 0.008, 0.009), 0.5)
seat_z = min(VW[i].z for i in range(len(VW)) if P["dom"][i] in ("pelvis.L", "pelvis.R") and abs(VW[i].x) < 0.15)
bpy.ops.mesh.primitive_cylinder_add(radius=0.23, depth=0.08, location=(0, 0.05, seat_z-0.045), vertices=64); st = bpy.context.object
b = st.modifiers.new("b", "BEVEL"); b.width = 0.012; b.segments = 4; st.data.materials.append(STOOL); bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=seat_z-0.09, location=(0, 0.05, (seat_z-0.09)/2), vertices=24); bpy.context.object.data.materials.append(STOOL)
# luz cálida de estudio
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
def area(loc, tgt, e, col, sx, sy=None):
    d = bpy.data.lights.new("a", "AREA"); d.energy = e; d.color = col; d.shape = 'RECTANGLE'; d.size = sx; d.size_y = sy or sx
    o = bpy.data.objects.new("a", d); o.location = loc; bpy.context.collection.objects.link(o)
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = (Vector(tgt)-Vector(loc)).to_track_quat('-Z', 'Y'); return o
area(NOSE+Vector((1.0, -1.0, 0.8)), NOSE, 60, (1.0, 0.76, 0.54), 1.2, 0.9)        # principal
area(NOSE+Vector((-1.0, 0.6, 0.7)), NOSE, 50, (1.0, 0.85, 0.68), 1.0, 0.5)        # contraluz
area(NOSE+Vector((-0.6, -1.4, 0.0)), NOSE, 7, (0.95, 0.92, 0.9), 1.4)            # relleno
# guante mate y manga azul (como la PL v4)
GLOVE = mat("guante", (0.50, 0.51, 0.52), 0.68, **{"Subsurface Weight": 0.04, "Specular IOR Level": 0.25})
SLEEVE = mat("manga", (0.02, 0.09, 0.17), 0.85)
STEEL = mat("acero", (0.92, 0.92, 0.95), 0.15, Metallic=1.0)
COTTON = mat("algodon", (0.93, 0.92, 0.88), 0.55, **{"Subsurface Weight": 0.25, "Sheen Weight": 0.5})
def glove_hand():
    h = mano.build_hand(GLOVE); hm = h.data; hm.materials.append(SLEEVE)
    gw = h.vertex_groups["wrist.R"]; wr = [v.co for v in hm.vertices if any(g.group == gw.index and g.weight > 0.5 for g in v.groups)]
    wc = sum(wr, Vector())/len(wr); g3 = h.vertex_groups["finger3-3.R"]
    tp = [v.co for v in hm.vertices if any(g.group == g3.index and g.weight > 0.5 for g in v.groups)]; fd = (wc-sum(tp, Vector())/len(tp)).normalized()
    for p in hm.polygons:
        c = sum((hm.vertices[i].co for i in p.vertices), Vector())/len(p.vertices)
        if (c-wc).dot(fd) > 0.035: p.material_index = 1
    def gp(n):
        g = h.vertex_groups[n]; return [h.matrix_world@v.co for v in hm.vertices if any(ge.group == g.index and ge.weight > 0.5 for ge in v.groups)]
    w0 = sum(gp("wrist.R"), Vector())/len(gp("wrist.R")); ti = max(gp("finger2-3.R"), key=lambda p: (p-w0).length); tt = max(gp("finger1-3.R"), key=lambda p: (p-w0).length)
    pinch = (ti+tt)/2; fh = (pinch-w0).normalized(); ah = ti-tt; ah = (ah-fh*ah.dot(fh)).normalized()
    return h, pinch, Matrix((fh, ah, fh.cross(ah))).transposed()
def place(h, pinch, src, at, fingers_dir, across):
    ft = fingers_dir.normalized(); a2 = (across-ft*across.dot(ft)).normalized()
    dst = Matrix((ft, a2, ft.cross(a2))).transposed(); h.matrix_world = Matrix.Translation(at)@(dst@src.inverted()).to_4x4()@Matrix.Translation(-pinch)
HAND, HP, HS = glove_hand()
# mano del propio paciente (piel) para la compresión
OWN = paciente.mat("piel_mano", (0.62, 0.40, 0.29), 0.45, **{"Subsurface Weight": 0.3, "Subsurface Radius": (1.0, 0.36, 0.17), "Subsurface Scale": 0.005})
_g = GLOVE; GLOVE = OWN; PH, PP, PS = glove_hand(); GLOVE = _g
PH.data.materials[1] = paciente.mat("manga_pac", (0.05, 0.08, 0.13), 0.82)   # manga corta de la camiseta: se ve solo el antebrazo
for p in PH.data.polygons: p.material_index = 0
AWAY = Vector((0, 0, -6))
# pinza de bayoneta (local: punta en el origen, el mango hacia +Z) con un algodón en la punta
fc = bpy.data.objects.new("pinza", None); bpy.context.collection.objects.link(fc)
def blade(dy):
    cu = bpy.data.curves.new("hoja", "CURVE"); cu.dimensions = '3D'; sp = cu.splines.new('POLY')
    pts = [(0, dy, 0), (0, dy*1.3, 0.050), (0.004, dy*1.5, 0.058), (0.013, dy*1.8, 0.066), (0.014, dy*2.6, 0.120), (0.014, dy*0.2, 0.175)]
    sp.points.add(len(pts)-1)
    for p, q in zip(sp.points, pts): p.co = (*q, 1)
    cu.bevel_depth = 0.0010; cu.bevel_resolution = 2
    o = bpy.data.objects.new("hoja", cu); bpy.context.collection.objects.link(o); cu.materials.append(STEEL); o.parent = fc; return o
blade(0.0009); blade(-0.0009)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, -0.006), segments=32, ring_count=16); cot = bpy.context.object
cot.scale = (0.0045, 0.0042, 0.013); cot.parent = fc; cot.data.materials.append(COTTON); bpy.ops.object.shade_smooth()
tx = bpy.data.textures.new("fibra", 'CLOUDS'); tx.noise_scale = 0.08; dp = cot.modifiers.new("fibra", 'DISPLACE'); dp.texture = tx; dp.strength = 0.25
fc.location = AWAY
def forceps(depth):
    """depth: cuánto ha entrado la punta en la fosa (m) siguiendo el suelo nasal"""
    axis = FACEDIR.copy()                                      # el mango sale hacia delante
    fc.rotation_mode = 'QUATERNION'; q = Vector((0, 0, 1)).rotation_difference(axis)
    xr = q@Vector((1, 0, 0)); q = (xr.rotation_difference(-UP))@q        # el acodamiento de la bayoneta queda hacia abajo
    fc.rotation_quaternion = q; fc.location = NOSTRIL-FACEDIR*depth
# cámara y render
cam = bpy.data.cameras.new("c"); co = bpy.data.objects.new("c", cam); bpy.context.collection.objects.link(co); sc.camera = co
def aim(pos, tgt, lens, focus=None):
    pos = Vector(pos); tgt = Vector(tgt); f = (tgt-pos).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); u = r.cross(f)
    co.matrix_world = Matrix.Translation(pos)@Matrix((r, u, -f)).transposed().to_4x4(); cam.lens = lens
    cam.dof.use_dof = focus is not None
    if focus is not None: cam.dof.focus_distance = (Vector(focus)-pos).length; cam.dof.aperture_fstop = 4.0
r = sc.render; r.resolution_x = int(A[1]) if len(A) > 1 else 360; r.resolution_y = r.resolution_x*16//9
r.engine = 'CYCLES'; sc.cycles.samples = int(A[2]) if len(A) > 2 else 16; sc.cycles.use_denoising = True
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.03
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; r.image_settings.file_format = 'JPEG'; r.image_settings.quality = 93
CH = NOSE+Vector((0, 0.18, -0.30))                                  # pecho, para encuadres amplios
SH = {"general": (NOSE+Vector((0.55, -0.80, 0.02)), NOSE+Vector((0, 0.10, -0.22)), 32, None),
      "intro0": (NOSE+Vector((0.85, -1.20, 0.20)), NOSE+Vector((0, 0.10, -0.24)), 30, None),
      "perfil": (NOSE+Vector((0.95, 0.10, -0.10)), NOSE+Vector((0, 0.16, -0.22)), 32, None),
      "retrato": (NOSE+Vector((0.30, -0.45, 0.05)), NOSE+Vector((0, 0.06, 0.0)), 70, NOSE),
      "pinza": (NOSE+Vector((0.30, -0.36, -0.06)), SOFT+Vector((0, 0.03, -0.03)), 60, SOFT),
      "algodon": (NOSTRIL+FACEDIR*0.20+SIDE*0.17-UP*0.05, NOSTRIL+FACEDIR*0.06-UP*0.02, 45, NOSTRIL)}
def shot(n):
    p, t, l, f = SH[n]; aim(p, t, l, f)
def save(path): r.filepath = path; bpy.ops.render.render(write_still=True)
ease = lambda x: x*x*(3-2*x)
def hand_on_nose(k):
    tgt = SOFT; fdir = (UP*0.55-FACEDIR*0.55+SIDE*0.15)
    place(PH, PP, PS, tgt+(-fdir.normalized())*0.12*(1-k), fdir, SIDE)
def hand_on_forceps():
    hp = fc.matrix_world@Vector((0.014, 0, 0.125)); fdir = (UP*0.6+SIDE*0.4-FACEDIR*0.3)
    place(HAND, HP, HS, hp, fdir, fc.matrix_world.to_quaternion()@Vector((0, 0, 1)))
if A and A[0] == "stills":
    for n in (A[3:] or SH):
        fc.location = AWAY; HAND.matrix_world = Matrix.Translation(AWAY); PH.matrix_world = Matrix.Translation(AWAY)
        if n == "pinza": hand_on_nose(1.0)
        if n == "algodon": forceps(0.012); hand_on_forceps()
        shot(n); t = time.time(); save(f"{OUT}/s_{n}.jpg"); print(n, round(time.time()-t, 1), flush=True)
if A and A[0] == "anim":
    kind, a0, a1 = A[3], int(A[4]), int(A[5]); N = int(os.environ.get("NFR", "36")); od = f"{OUT}/f_{kind}"; os.makedirs(od, exist_ok=True)
    for fr in range(a0, a1):
        u = fr/(N-1); fc.location = AWAY; HAND.matrix_world = Matrix.Translation(AWAY); PH.matrix_world = Matrix.Translation(AWAY)
        if kind == "intro":
            (p0, t0, l0, _), (p1, t1, l1, _) = SH["intro0"], SH["general"]; k = ease(u); aim(p0.lerp(p1, k), t0.lerp(t1, k), l0+(l1-l0)*k)
        elif kind == "pinza":
            hand_on_nose(ease(min(1, u/0.55))); shot("pinza")
        elif kind == "algodon":
            forceps(-0.05+0.075*ease(min(1, u/0.8))); hand_on_forceps(); shot("algodon")
        save(f"{od}/{fr:03d}.jpg"); print(kind, fr, flush=True)
