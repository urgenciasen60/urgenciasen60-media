"""Técnica 03 · Toracocentesis (25/11/2026): escenas externas con el paciente de alta calidad (paciente.py).
Paciente sin camiseta, sentado e inclinado hacia delante con los brazos sobre una mesa; costillas posteriores derechas
proyectadas desde su propia anatomía; marca justo por encima de una costilla (posterolateral, lejos de la columna);
sonda convexa de ecografía, jeringa con aguja que aspira líquido seroso y catéter con llave de tres pasos.
Uso: python3 toracocentesis_v1.py -- stills RES SAMPLES [planos]
     python3 toracocentesis_v1.py -- anim RES SAMPLES intro|eco|puncion|cateter F0 F1   (NFR = fotogramas totales)"""
import bpy, sys, os, math, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
A = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
OUT = os.environ.get("TOROUT", "/home/claude/v3d/tora"); os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
import paciente, humano, mano
from humano import X
from paciente import mat
LEAN = {"spine05": (X, 16), "spine04": (X, 8), "spine03": (X, 6), "spine02": (X, 4), "spine01": (X, 3), "neck01": (X, 8), "neck02": (X, 5), "head": (X, 6),
        "upperleg01.L": ("dir", (0.02, -0.98, 0.12)), "upperleg01.R": ("dir", (-0.02, -0.98, 0.12)),
        "lowerleg01.L": ("dir", (0.0, 0.08, -1)), "lowerleg01.R": ("dir", (0.0, 0.08, -1)),
        "upperarm01.L": ("dir", (0.28, -0.88, -0.38)), "upperarm01.R": ("dir", (-0.28, -0.88, -0.38)),
        "lowerarm01.L": ("dir", (-0.88, -0.45, 0.02)), "lowerarm01.R": ("dir", (0.88, -0.45, 0.06))}
# ---------- reposo: costillas posteriores derechas y punto de punción
humano.TARGETS = paciente.TARGETS
V0, F0 = humano.load_obj(); used = sorted({i for f in F0 for i in f}); REST = V0[used]
remap = {o: k for k, o in enumerate(used)}
BVr = BVHTree.FromPolygons([tuple(p) for p in REST], [[remap[i] for i in f] for f in F0])
def back_hit(x, z):
    loc, nrm, i, d = BVr.ray_cast(Vector((x, 0.6, z)), Vector((0, -1, 0)))
    return (np.array(loc), np.array(nrm)) if loc else (None, None)
XS = -0.118; ZS = 0.392                       # punto: hemitórax derecho, posterolateral, unos 12 cm de la línea media
SLOPE = 0.045; SP = 0.028; RR = 0.0048        # caída de la costilla en 15 cm, distancia entre costillas, semialtura
def rib_z(k, x): return ZS-0.010+k*SP-SLOPE*((-x-0.02)/0.15)+SLOPE*((-XS-0.02)/0.15)
RIBS_REST = []
for k in range(-3, 4):
    pts = []
    for x in np.linspace(-0.018, -0.185, 28):
        p, n = back_hit(x, rib_z(k, x))
        if p is None: continue
        depth = 0.016+0.022*max(0.0, 1-(-x-0.035)/0.07)          # más profunda junto a la columna (musculatura)
        pts.append(p-n*depth)
    RIBS_REST.append(pts)
MP, MN = back_hit(XS, rib_z(0, XS)+RR+0.0035)
SPINE_REST = []
for z in np.arange(0.24, 0.60, 0.028):
    p, n = back_hit(0.0, z)
    if p is not None: SPINE_REST.append(p-n*0.022)                  # justo por encima del borde superior de la costilla 0
# ---------- paciente posado
P = paciente.crear(LEAN, ropa=True, camiseta=False); ob = P["ob"]
zmin = min(v.co.z for v in ob.data.vertices)
OBJS = [ob, P["eyes"], P["bot"]]
for o in OBJS: o.matrix_world = Matrix.Translation((0, 0, -zmin))@o.matrix_world
bpy.context.view_layer.update()
VW = np.array([tuple(ob.matrix_world@v.co) for v in ob.data.vertices]); DISP = VW-REST
kd = KDTree(len(REST))
for i, p in enumerate(REST): kd.insert(p, i)
kd.balance()
def warp(p, k=8):
    near = kd.find_n(Vector(p), k); w = np.array([1/(d*d+1e-6) for _, _, d in near]); idx = [i for _, i, _ in near]
    return np.array(p)+(DISP[idx]*w[:, None]).sum(0)/w.sum()
dg = bpy.context.evaluated_depsgraph_get(); me_e = ob.evaluated_get(dg).to_mesh()
BV = BVHTree.FromPolygons([ob.matrix_world@v.co for v in me_e.vertices], [tuple(p.vertices) for p in me_e.polygons])
def onskin(p, n):
    loc, nrm, i, d = BV.ray_cast(Vector(p)+Vector(n)*0.05, -Vector(n))
    return (loc, nrm.normalized()) if loc else (Vector(p), Vector(n))
iM = kd.find(Vector(MP))[1]
SITE, NRM = onskin(warp(MP), ob.matrix_world.to_3x3()@ob.data.vertices[iM].normal)
UPB = Vector(warp(MP+np.array([0, 0, 0.05])))-Vector(warp(MP)); UPB = (UPB-NRM*UPB.dot(NRM)).normalized()   # hacia craneal sobre la piel
LAT = NRM.cross(UPB).normalized()
# costillas (transparencia) y marca
BONE = mat("costilla", (0.90, 0.84, 0.70), 0.55, **{"Emission Color": (0.90, 0.84, 0.70, 1), "Emission Strength": 0.25})
RIBS = []
for pts in RIBS_REST:
    cu = bpy.data.curves.new("costilla", "CURVE"); cu.dimensions = '3D'; sp = cu.splines.new('NURBS'); W_ = [warp(p) for p in pts]
    sp.points.add(len(W_)-1)
    for q, w_ in zip(sp.points, W_): q.co = (*w_, 1)
    sp.use_endpoint_u = True; sp.order_u = 4; cu.bevel_depth = RR; cu.bevel_resolution = 4
    o = bpy.data.objects.new("costilla", cu); bpy.context.collection.objects.link(o); cu.materials.append(BONE); o.scale = (1, 1, 1); RIBS.append(o)
SPN = []
for p in SPINE_REST:
    bpy.ops.mesh.primitive_cube_add(size=1, location=tuple(warp(p))); o = bpy.context.object; o.scale = (0.010, 0.012, 0.016)
    bv = o.modifiers.new("b", "BEVEL"); bv.width = 0.004; bv.segments = 3; o.data.materials.append(BONE); SPN.append(o)
RIBS += SPN
RED = mat("rojo", (0.50, 0.0, 0.006), 0.4, **{"Emission Color": (0.5, 0, 0.006, 1), "Emission Strength": 0.1})
bpy.ops.mesh.primitive_cylinder_add(radius=0.0040, depth=0.0010, location=SITE+NRM*0.0007, vertices=32); MARK = bpy.context.object
MARK.rotation_mode = 'QUATERNION'; MARK.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(NRM); MARK.data.materials.append(RED)
# ---------- mesa negra bajo los antebrazos
fore = [VW[i] for i, d in enumerate(P["dom"]) if d.startswith("lowerarm")]
tz = min(p[2] for p in fore)-0.004; tc = np.mean(fore, 0)
TABLE = mat("mesa", (0.006, 0.006, 0.007), 0.5)
bpy.ops.mesh.primitive_cube_add(location=(tc[0], tc[1]-0.05, tz-0.018)); tb = bpy.context.object; tb.scale = (0.45, 0.25, 0.018)
b_ = tb.modifiers.new("b", "BEVEL"); b_.width = 0.008; b_.segments = 3; tb.data.materials.append(TABLE)
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=tz-0.04, location=(tc[0], tc[1]-0.05, (tz-0.04)/2)); bpy.context.object.data.materials.append(TABLE)
STOOL = mat("taburete", (0.008, 0.008, 0.009), 0.5)
seat_z = min(VW[i][2] for i in range(len(VW)) if P["dom"][i] in ("pelvis.L", "pelvis.R") and abs(VW[i][0]) < 0.15)
bpy.ops.mesh.primitive_cylinder_add(radius=0.23, depth=0.08, location=(0, 0.07, seat_z-0.045), vertices=64); st = bpy.context.object
b_ = st.modifiers.new("b", "BEVEL"); b_.width = 0.012; b_.segments = 4; st.data.materials.append(STOOL); bpy.ops.object.shade_smooth()
# ---------- luz cálida de estudio
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
def area(loc, tgt, e, col, sx, sy=None):
    d = bpy.data.lights.new("a", "AREA"); d.energy = e; d.color = col; d.shape = 'RECTANGLE'; d.size = sx; d.size_y = sy or sx
    o = bpy.data.objects.new("a", d); o.location = loc; bpy.context.collection.objects.link(o)
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = (Vector(tgt)-Vector(loc)).to_track_quat('-Z', 'Y'); return o
area(SITE+Vector((-1.0, 0.9, 0.9)), SITE, 42, (1.0, 0.76, 0.54), 1.2, 0.9)        # principal (derecha y detrás)
area(SITE+Vector((1.0, 0.8, 0.6)), SITE, 35, (1.0, 0.85, 0.68), 1.0, 0.5)         # contraluz
area(SITE+Vector((-0.3, 1.5, -0.1)), SITE, 7, (0.95, 0.92, 0.9), 1.4)            # relleno
# ---------- mano enguantada, sonda, jeringa, catéter
GLOVE = mat("guante", (0.50, 0.51, 0.52), 0.68, **{"Subsurface Weight": 0.04, "Specular IOR Level": 0.25})
SLEEVE = mat("manga", (0.02, 0.09, 0.17), 0.85)
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
AWAY = Vector((0, 0, -9))
def group(name):
    e = bpy.data.objects.new(name, None); bpy.context.collection.objects.link(e); e.rotation_mode = 'QUATERNION'; return e
def part(op, m, parent, smooth=True, **kw):
    op(**kw); o = bpy.context.object; o.data.materials.append(m); o.parent = parent
    if smooth: bpy.ops.object.shade_smooth()
    return o
# sonda convexa (local: cara de contacto en el origen, el cuerpo hacia +Z, la huella a lo largo de Y)
PLAS = mat("sonda", (0.035, 0.037, 0.04), 0.35); GEL = mat("gel", (0.85, 0.9, 0.95), 0.05, **{"Transmission Weight": 0.9})
PROBE = group("sonda")
pb = part(bpy.ops.mesh.primitive_cube_add, PLAS, PROBE, size=1, location=(0, 0, 0.016)); pb.scale = (0.020, 0.056, 0.032)
bv = pb.modifiers.new("b", "BEVEL"); bv.width = 0.008; bv.segments = 6
ph = part(bpy.ops.mesh.primitive_cube_add, PLAS, PROBE, size=1, location=(0, 0, 0.068)); ph.scale = (0.019, 0.032, 0.080)
bv = ph.modifiers.new("b", "BEVEL"); bv.width = 0.008; bv.segments = 6
part(bpy.ops.mesh.primitive_cylinder_add, PLAS, PROBE, radius=0.0035, depth=0.20, location=(0, 0, 0.205))
part(bpy.ops.mesh.primitive_cube_add, GEL, PROBE, size=1, location=(0, 0, 0.0015)).scale = (0.018, 0.055, 0.003)
PROBE.location = AWAY
# jeringa de 20 ml con aguja (local: punta de la aguja en el origen, jeringa hacia +Z)
CLEAR = mat("plastico", (0.95, 0.96, 0.97), 0.06, **{"Transmission Weight": 1.0, "IOR": 1.45})
STEEL = mat("acero", (0.92, 0.92, 0.95), 0.15, Metallic=1.0)
FLUID = mat("liquido_pleural", (0.98, 0.80, 0.30), 0.03, **{"Transmission Weight": 0.85, "IOR": 1.34})
RUBBER = mat("embolo", (0.08, 0.08, 0.09), 0.5); WHITE = mat("blanco", (0.92, 0.92, 0.90), 0.4)
SYR = group("jeringa")
part(bpy.ops.mesh.primitive_cylinder_add, STEEL, SYR, radius=0.0004, depth=0.040, location=(0, 0, 0.020), vertices=12)
part(bpy.ops.mesh.primitive_cone_add, mat("cono_verde", (0.10, 0.55, 0.20), 0.4), SYR, radius1=0.0028, radius2=0.0016, depth=0.012, location=(0, 0, 0.044))
part(bpy.ops.mesh.primitive_cylinder_add, CLEAR, SYR, radius=0.0100, depth=0.080, location=(0, 0, 0.092), end_fill_type='NOTHING')
LIQ = part(bpy.ops.mesh.primitive_cylinder_add, FLUID, SYR, radius=0.0094, depth=1.0, location=(0, 0, 0.053))
PLUN = group("embolo_g"); PLUN.parent = SYR
part(bpy.ops.mesh.primitive_cylinder_add, RUBBER, PLUN, radius=0.0094, depth=0.006, location=(0, 0, 0.0))
part(bpy.ops.mesh.primitive_cube_add, WHITE, PLUN, smooth=False, size=1, location=(0, 0, 0.045)).scale = (0.010, 0.0015, 0.085)
part(bpy.ops.mesh.primitive_cylinder_add, WHITE, PLUN, radius=0.012, depth=0.002, location=(0, 0, 0.088))
SYR.location = AWAY
def syringe(depth, fill):
    """depth: profundidad de la punta (m); fill: ml de líquido aspirado (0-20)"""
    q = Vector((0, 0, 1)).rotation_difference(NRM); SYR.rotation_quaternion = q; SYR.location = SITE-NRM*depth
    h = 0.002+0.0032*fill; PLUN.location = (0, 0, 0.056+h); LIQ.scale = (1, 1, max(1e-4, h)); LIQ.location = (0, 0, 0.053+h/2)
    LIQ.hide_render = fill < 0.05
# catéter con llave de tres pasos y alargadera
BLUE = mat("llave", (0.10, 0.35, 0.80), 0.35)
CAT = group("cateter")
part(bpy.ops.mesh.primitive_cylinder_add, WHITE, CAT, radius=0.0012, depth=0.045, location=(0, 0, 0.0225), vertices=16)
part(bpy.ops.mesh.primitive_cylinder_add, CLEAR, CAT, radius=0.0035, depth=0.018, location=(0, 0, 0.054))
part(bpy.ops.mesh.primitive_cylinder_add, BLUE, CAT, radius=0.0042, depth=0.016, location=(0, 0, 0.071))
part(bpy.ops.mesh.primitive_cylinder_add, BLUE, CAT, radius=0.0030, depth=0.030, location=(0, 0, 0.071), rotation=(0, math.pi/2, 0))
part(bpy.ops.mesh.primitive_cube_add, WHITE, CAT, smooth=False, size=1, location=(0, 0, 0.081)).scale = (0.003, 0.014, 0.004)
TUBE = bpy.data.curves.new("alargadera", "CURVE"); TUBE.dimensions = '3D'; TUBE.bevel_depth = 0.0024; TUBE.bevel_resolution = 4
TUBO = bpy.data.objects.new("alargadera", TUBE); bpy.context.collection.objects.link(TUBO); TUBE.materials.append(FLUID); TUBO.location = AWAY
CAT.location = AWAY
def catheter():
    CAT.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(NRM); CAT.location = SITE-NRM*0.020; bpy.context.view_layer.update()
    side = CAT.matrix_world@Vector((0.015, 0, 0.071)); TUBE.splines.clear(); sp = TUBE.splines.new('BEZIER'); sp.bezier_points.add(2)
    pts = [side, side+LAT*0.06-UPB*0.05+NRM*0.02, side+LAT*0.10-Vector((0, 0, 0.45))]
    for b_, p in zip(sp.bezier_points, pts): b_.co = p; b_.handle_left_type = b_.handle_right_type = 'AUTO'
    TUBO.location = (0, 0, 0)
def hide_tools():
    for o in (PROBE, SYR, CAT, TUBO): o.location = AWAY
    HAND.matrix_world = Matrix.Translation(AWAY)
# ---------- cámara y render
cam = bpy.data.cameras.new("c"); co = bpy.data.objects.new("c", cam); bpy.context.collection.objects.link(co); sc.camera = co
def aim(pos, tgt, lens, up=Vector((0, 0, 1)), focus=None):
    pos = Vector(pos); tgt = Vector(tgt); f = (tgt-pos).normalized(); r = f.cross(up).normalized(); u = r.cross(f)
    co.matrix_world = Matrix.Translation(pos)@Matrix((r, u, -f)).transposed().to_4x4(); cam.lens = lens
    cam.dof.use_dof = focus is not None
    if focus is not None: cam.dof.focus_distance = (Vector(focus)-pos).length; cam.dof.aperture_fstop = 4.0
r = sc.render; r.resolution_x = int(A[1]) if len(A) > 1 else 360; r.resolution_y = r.resolution_x*16//9
r.engine = 'CYCLES'; sc.cycles.samples = int(A[2]) if len(A) > 2 else 16; sc.cycles.use_denoising = True
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.03
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; r.image_settings.file_format = 'JPEG'; r.image_settings.quality = 93
BACKC = Vector(tuple(np.mean([VW[i] for i, d in enumerate(P["dom"]) if d in ("spine02", "spine01")], 0)))
SH = {"general": (SITE+NRM*0.95+Vector((-0.45, 0, 0.30)), BACKC+Vector((0, 0, 0.05)), 30, Vector((0, 0, 1)), None),
      "intro0": (SITE+NRM*1.35+Vector((-0.85, 0, 0.45)), BACKC+Vector((0, 0, 0.05)), 28, Vector((0, 0, 1)), None),
      "rayos": (SITE+NRM*0.46+LAT*0.06+UPB*0.04, SITE+LAT*0.06+UPB*0.04, 40, UPB, None),
      "marca": (SITE+NRM*0.24+UPB*0.03-LAT*0.02, SITE, 55, UPB, SITE),
      "eco": (SITE+NRM*0.34+LAT*0.10+UPB*0.20, SITE+NRM*0.05, 40, Vector((0, 0, 1)), SITE+NRM*0.04),
      "puncion": (SITE+NRM*0.26+LAT*0.20+UPB*0.06, SITE+NRM*0.05, 45, Vector((0, 0, 1)), SITE+NRM*0.04),
      "cateter": (SITE+NRM*0.26+LAT*0.17+UPB*0.07, SITE+NRM*0.04-Vector((0, 0, 0.03)), 42, Vector((0, 0, 1)), SITE+NRM*0.04)}
SKIN = ob.data.materials[0]
def setshot(n):
    xr = n == "rayos"
    SKIN.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = 0.18 if xr else 1.0
    for o in RIBS: o.hide_render = not xr
    MARK.hide_render = n in ("general", "intro0")
    p, t, l, u, f = SH[n]; aim(p, t, l, u, f)
def save(path): r.filepath = path; bpy.ops.render.render(write_still=True)
ease = lambda x: x*x*(3-2*x)
def probe_at(slide):
    PROBE.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(NRM)
    yax = PROBE.rotation_quaternion@Vector((0, 1, 0)); PROBE.rotation_quaternion = (yax.rotation_difference(UPB))@PROBE.rotation_quaternion
    PROBE.location = SITE+UPB*(0.005+slide)+NRM*0.002; bpy.context.view_layer.update()
    place(HAND, HP, HS, PROBE.matrix_world@Vector((0, 0, 0.075)), -NRM*0.5+LAT*0.6-UPB*0.2, UPB)
def frame(kind, u):
    hide_tools()
    if kind == "intro":
        (p0, t0, l0, u0, _), (p1, t1, l1, u1, _) = SH["intro0"], SH["general"]; k = ease(u); setshot("general"); aim(p0.lerp(p1, k), t0.lerp(t1, k), l0+(l1-l0)*k)
    elif kind == "eco":
        setshot("eco"); MARK.hide_render = u < 0.8; probe_at(0.02*math.sin(u*math.pi*1.5))
        if u > 0.8: hide_tools()
    elif kind == "puncion":                 # entra perpendicular por encima de la costilla, aspirando; aparece líquido
        setshot("puncion"); k = ease(min(1, u/0.55)); depth = -0.03+0.068*k
        fill = 0 if depth < 0.030 else 12*ease(min(1, (u-0.55)/0.40))
        syringe(depth, fill); bpy.context.view_layer.update(); place(HAND, HP, HS, SYR.matrix_world@Vector((0, 0, 0.085)), -NRM*0.3+LAT*0.7, UPB)
    elif kind == "cateter":
        setshot("cateter"); catheter()
if A and A[0] == "stills":
    for n in (A[3:] or SH):
        hide_tools(); setshot(n)
        if n == "eco": probe_at(0.0)
        if n == "puncion": frame("puncion", 1.0)
        if n == "cateter": frame("cateter", 1.0)
        t = time.time(); save(f"{OUT}/s_{n}.jpg"); print(n, round(time.time()-t, 1), flush=True)
if A and A[0] == "anim":
    kind, a0, a1 = A[3], int(A[4]), int(A[5]); N = int(os.environ.get("NFR", "30")); od = f"{OUT}/f_{kind}"; os.makedirs(od, exist_ok=True)
    for fr in range(a0, a1):
        frame(kind, fr/(N-1)); save(f"{od}/{fr:03d}.jpg"); print(kind, fr, flush=True)
