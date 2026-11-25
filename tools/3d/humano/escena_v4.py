"""Punción lumbar v4 (decisiones de Eduardo del 18/11/2026).
Varón joven musculado (MakeHuman CC0), piel realista con dispersión subsuperficial y textura, luz cálida de estudio,
fondo y camilla negros, paño quirúrgico sobre pelvis y glúteos (simulación de tela), línea de crestas en L4 y puntos L4-L5 y L3-L4,
mano con guante blanco, aguja espinal con fiador extraíble y gotas de LCR.
Uso: python3 escena_v4.py -- stills RES SAMPLES [planos...]
     python3 escena_v4.py -- anim RES SAMPLES intro|orbit|aguja|lcr F0 F1"""
import bpy, sys, math, time, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import humano
humano.TARGETS = humano.MACHO; humano.BREAST = 0.0
from humano import build, FETAL, load_obj
import huesos
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
A = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
OUT = os.environ.get("V4OUT", "/home/claude/v3d/v4"); os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene

# ---------- malla: varón musculado y malla neutra de referencia (para colocar el esqueleto)
V, F = load_obj(); V0, _ = load_obj([])
used = sorted({i for f in F for i in f}); B0 = V0[used]
MID0 = B0[np.abs(B0[:, 0]) < 0.03]
def back_y0(z): s = MID0[np.abs(MID0[:, 2]-z) < 0.01]; return float(s[:, 1].max())

# ---------- materiales
def nodes(m): return m.node_tree.nodes, m.node_tree.links
def bsdf(m): return m.node_tree.nodes["Principled BSDF"]
def M(n, c, r=0.5, a=1.0, e=0.0, metal=0.0, sss=0.0):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = bsdf(m)
    b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = r
    b.inputs["Alpha"].default_value = a; b.inputs["Metallic"].default_value = metal
    if e: b.inputs["Emission Color"].default_value = (*c, 1); b.inputs["Emission Strength"].default_value = e
    if sss: b.inputs["Subsurface Weight"].default_value = sss; b.inputs["Subsurface Radius"].default_value = (1.0, 0.37, 0.18); b.inputs["Subsurface Scale"].default_value = 0.004
    return m
def tex(m, kind, scale, detail=2.0, coord="Object"):
    nd, ln = nodes(m); tc = nd.get("tc") or nd.new("ShaderNodeTexCoord"); tc.name = "tc"
    t = nd.new(kind); t.inputs["Scale"].default_value = scale
    if "Detail" in t.inputs: t.inputs["Detail"].default_value = detail
    ln.new(tc.outputs[coord], t.inputs["Vector"]); return t
def ramp(m, src, c0, c1, p0=0.3, p1=0.7):
    nd, ln = nodes(m); r = nd.new("ShaderNodeValToRGB"); e = r.color_ramp.elements
    e[0].position, e[0].color = p0, (*c0, 1); e[1].position, e[1].color = p1, (*c1, 1)
    ln.new(src, r.inputs["Fac"]); return r
def bump(m, height, strength, dist):
    nd, ln = nodes(m); bp = nd.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = strength; bp.inputs["Distance"].default_value = dist
    ln.new(height, bp.inputs["Height"]); ln.new(bp.outputs["Normal"], bsdf(m).inputs["Normal"]); return bp
def skin_mat(name="piel"):
    m = M(name, (0.70, 0.45, 0.32), 0.45); b = bsdf(m); nd, ln = nodes(m)
    # color con manchas suaves y variación por zonas
    n1 = tex(m, "ShaderNodeTexNoise", 18, 5); r1 = ramp(m, n1.outputs["Fac"], (0.55, 0.32, 0.21), (0.76, 0.50, 0.36), 0.30, 0.72)
    n2 = tex(m, "ShaderNodeTexNoise", 220, 3); mix = nd.new("ShaderNodeMix"); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
    mix.inputs["Factor"].default_value = 0.10; ln.new(r1.outputs["Color"], mix.inputs["A"]); ln.new(n2.outputs["Color"], mix.inputs["B"])
    ln.new(mix.outputs["Result"], b.inputs["Base Color"])
    b.inputs["Subsurface Weight"].default_value = 0.30; b.inputs["Subsurface Radius"].default_value = (1.0, 0.36, 0.17)
    b.inputs["Subsurface Scale"].default_value = 0.006; b.inputs["Specular IOR Level"].default_value = 0.42
    b.inputs["Sheen Weight"].default_value = 0.12; b.inputs["Sheen Roughness"].default_value = 0.45
    # rugosidad variable (zonas más brillantes y más mates)
    n3 = tex(m, "ShaderNodeTexNoise", 40, 2); mr = nd.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = 0.36; mr.inputs["To Max"].default_value = 0.56
    ln.new(n3.outputs["Fac"], mr.inputs["Value"]); ln.new(mr.outputs["Result"], b.inputs["Roughness"])
    # poros y microrrelieve
    vo = tex(m, "ShaderNodeTexVoronoi", 900); n4 = tex(m, "ShaderNodeTexNoise", 1600, 1)
    add = nd.new("ShaderNodeMath"); add.operation = 'ADD'; ln.new(vo.outputs["Distance"], add.inputs[0]); ln.new(n4.outputs["Fac"], add.inputs[1])
    bump(m, add.outputs["Value"], 0.10, 0.0004)
    return m
SKIN = skin_mat()
BRIEF = M("ropa_interior", (0.025, 0.025, 0.03), 0.7)
BONE = M("hueso", (0.90, 0.84, 0.70), 0.55, e=0.25)
YEL = M("amarillo", (1.0, 0.72, 0.0), 0.45, e=0.35); RED = M("rojo", (0.50, 0.0, 0.006), 0.40, e=0.10)
BED = M("camilla", (0.003, 0.003, 0.0035), 0.62); bn = tex(BED, "ShaderNodeTexNoise", 260, 3); bump(BED, bn.outputs["Fac"], 0.06, 0.0006)
DRAPE = M("pano", (0.025, 0.12, 0.22), 0.85); DRAPE.node_tree.nodes["Principled BSDF"].inputs["Sheen Weight"].default_value = 0.35
wv = tex(DRAPE, "ShaderNodeTexWave", 900); bump(DRAPE, wv.outputs["Fac"], 0.08, 0.0003)
GLOVE = M("guante", (0.50, 0.51, 0.52), 0.68, sss=0.04); bsdf(GLOVE).inputs["Specular IOR Level"].default_value = 0.25   # guante mate (25/11)
gn = tex(GLOVE, "ShaderNodeTexNoise", 700, 2); bump(GLOVE, gn.outputs["Fac"], 0.08, 0.0002)
STEEL = M("acero", (0.92, 0.92, 0.95), 0.12, metal=1.0); HUBM = M("cono", (1.0, 0.80, 0.08), 0.22); HUBM2 = M("cono_fiador", (1.0, 0.86, 0.25), 0.3)
SCLERA = M("esclera", (0.85, 0.82, 0.78), 0.15); IRIS = M("iris", (0.16, 0.09, 0.05), 0.2); PUPIL = M("pupila", (0.0, 0.0, 0.0), 0.05)
LCR = bpy.data.materials.new("lcr"); LCR.use_nodes = True; lb = bsdf(LCR)
lb.inputs["Base Color"].default_value = (0.95, 0.97, 1.0, 1); lb.inputs["Transmission Weight"].default_value = 1.0
lb.inputs["Roughness"].default_value = 0.02; lb.inputs["IOR"].default_value = 1.335
PLAST = bpy.data.materials.new("tubo"); PLAST.use_nodes = True; pb = bsdf(PLAST)
pb.inputs["Base Color"].default_value = (0.90, 0.92, 0.95, 1); pb.inputs["Transmission Weight"].default_value = 0.85; pb.inputs["Roughness"].default_value = 0.20; pb.inputs["IOR"].default_value = 1.49
LABEL = M("etiqueta", (0.88, 0.88, 0.86), 0.7); CAPM = M("tapon_rojo", (0.55, 0.02, 0.03), 0.4)

# ---------- esqueleto lumbar y pelvis: se modela sobre la malla neutra y se deforma con los cambios de las articulaciones
sk = json.load(open(humano.D+"rigs/default.mhskel"))
J0 = np.array([V0[v].mean(0) for v in sk["joints"].values()]); J1 = np.array([V[v].mean(0) for v in sk["joints"].values()]); DJ = J1-J0
def warp(p):
    d = np.linalg.norm(J0-p, axis=1); i = np.argsort(d)[:6]; w = 1/(d[i]**2+1e-6); return p+(DJ[i]*w[:, None]).sum(0)/w.sum()
BONES = huesos.build(BONE, back_y0)
# pelvis masculina: más estrecha que la del modelo neutro
PC = Vector((0, back_y0(0.15)-0.06, huesos.ZC))
for o, _ in BONES:
    if o.name.split("_")[0] in ("pala1", "pala-1", "cresta1", "cresta-1", "rama", "isquion1", "isquion-1", "cabeza", "sacro") or o.name.startswith(("pala", "cresta", "rama_sup", "isquion", "cabeza_femur", "sacro")):
        for v in o.data.vertices: v.co = PC+Vector(((v.co-PC).x*0.82, (v.co-PC).y*0.92, (v.co-PC).z*0.92))
for o, _ in BONES:
    for v in o.data.vertices: v.co = Vector(warp(np.array(v.co)))
# ojos (para que la cara, si se ve, tenga mirada)
def group_center(g):
    idx = set(); cur = None
    for l in open(humano.D+"3dobjs/base.obj"):
        if l.startswith("g "): cur = l.split()[1]
        elif l.startswith("f ") and cur == g: idx |= {int(t.split("/")[0])-1 for t in l.split()[1:]}
    return V[sorted(idx)].mean(0)
EYES = []
for side in ("l", "r"):
    c = Vector(group_center(f"joint-{side}-eye")); rr = 0.0118
    bpy.ops.mesh.primitive_uv_sphere_add(radius=rr, location=c, segments=32, ring_count=16); e = bpy.context.object; e.data.materials.append(SCLERA); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_cylinder_add(radius=0.0056, depth=0.0006, location=c+Vector((0, -rr*0.93, 0)), rotation=(math.pi/2, 0, 0), vertices=32); i = bpy.context.object; i.data.materials.append(IRIS)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.0024, depth=0.0008, location=c+Vector((0, -rr*0.95, 0)), rotation=(math.pi/2, 0, 0), vertices=24); p = bpy.context.object; p.data.materials.append(PUPIL)
    EYES += [(e, "head"), (i, "head"), (p, "head")]

ob, J = build(FETAL, extras=BONES+EYES)
ob.data.materials.append(SKIN); ob.data.materials.append(BRIEF)
REST = np.array(V[used])
for p in ob.data.polygons:
    c = REST[list(p.vertices)].mean(0)
    zp = J1[list(sk["joints"].keys()).index("spine05____head")][2] if "spine05____head" in sk["joints"] else 0.12
    if -0.10+(zp-0.073) < c[2] < (0.075 if c[1] > 0 else 0.095)+(zp-0.073) and abs(c[0]) < 0.22: p.material_index = 1
# tumbar en decúbito lateral izquierdo (cabeza hacia +X, espalda hacia +Y)
ALL = [ob]+[b for b, _ in BONES]+[e for e, _ in EYES]
Rl = Matrix.Rotation(math.radians(90), 4, 'Y')
for o in ALL: o.matrix_world = Rl@o.matrix_world
bpy.context.view_layer.update()
zmin = min((o.matrix_world@v.co).z for v in ob.data.vertices)
T = Matrix.Translation((0, 0, 0.47-zmin+0.002))
for o in ALL: o.matrix_world = T@o.matrix_world
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get(); oe = ob.evaluated_get(dg); me_e = oe.to_mesh()
BV = BVHTree.FromPolygons([ob.matrix_world@v.co for v in me_e.vertices], [tuple(p.vertices) for p in me_e.polygons])
def ctr(name): o = bpy.data.objects[name]; return o.matrix_world@(sum((v.co for v in o.data.vertices), Vector())/len(o.data.vertices))
def tipof(name): o = bpy.data.objects[name]; vs = [o.matrix_world@v.co for v in o.data.vertices]; return max(vs, key=lambda v: v.y)
BACK = Vector((0, 1, 0))
def onskin(p, d=BACK):
    loc, nrm, i, dist = BV.ray_cast(p+d*0.25, -d)
    return (loc, nrm.normalized()) if loc else (None, None)
def mark_disc(p, n, r, mat, name):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=0.0012, location=p+n*0.0009, vertices=32); o = bpy.context.object; o.name = name
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(n); o.data.materials.append(mat); return o
TP = {k: tipof("espinosa_"+k) for k in ("L3", "L4", "L5")}
P45, N45 = onskin((TP["L4"]+TP["L5"])/2); P34, N34 = onskin((TP["L3"]+TP["L4"])/2)
MARKS = [mark_disc(P45, N45, 0.0065, RED, "punto_L4L5"), mark_disc(P34, N34, 0.0065, RED, "punto_L3L4")]
# línea de Tuffier (cresta a cresta) a la altura de la apófisis espinosa de L4
axis = (TP["L3"]-TP["L5"]).normalized(); cb = ctr("cuerpo_L4"); c0 = cb+axis*((TP["L4"]-cb).dot(axis))
u = (BACK-axis*BACK.dot(axis)).normalized(); v = axis.cross(u).normalized(); line = []
for th in np.linspace(-82, 82, 61):
    t = math.radians(th); d = (u*math.cos(t)+v*math.sin(t)).normalized()
    loc, nrm, i, dist = BV.ray_cast(c0+d*0.5, -d)
    if loc: line.append((loc, nrm.normalized()))
for i in range(0, len(line)-1):
    (a, na), (b_, nb) = line[i], line[i+1]; d = b_-a
    bpy.ops.mesh.primitive_cylinder_add(radius=0.0017, depth=d.length*1.02, location=(a+b_)/2+((na+nb)/2).normalized()*0.0012, vertices=10); o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d); o.data.materials.append(YEL); MARKS.append(o)
ymax = max((ob.matrix_world@v.co).y for v in ob.data.vertices)

# ---------- camilla negra (espalda en el borde), almohada y suelo
def rbox(loc, scl, mat, bev=0.02):
    bpy.ops.mesh.primitive_cube_add(location=loc); o = bpy.context.object; o.scale = scl
    bpy.ops.object.transform_apply(scale=True); b = o.modifiers.new("b", "BEVEL"); b.width = bev; b.segments = 5
    o.data.materials.append(mat); bpy.ops.object.shade_smooth(); return o
BEDO = rbox((0.05, ymax-0.44, 0.415), (1.05, 0.44, 0.055), BED, 0.03)
PILLOW = rbox((0.80, ymax-0.32, 0.52), (0.14, 0.17, 0.05), BED, 0.04)

# ---------- paño quirúrgico (tela simulada sobre pelvis y glúteos, por debajo de la línea de crestas)
DR_CACHE = os.path.join(OUT, "pano_cache.npz")
edge_x = P45.x-0.055
if os.path.exists(DR_CACHE):
    z = np.load(DR_CACHE); me = bpy.data.meshes.new("pano"); me.from_pydata(z["v"].tolist(), [], z["f"].tolist()); me.update()
    DRO = bpy.data.objects.new("pano", me); bpy.context.collection.objects.link(DRO)
else:
    x0, x1 = edge_x-0.62, edge_x; y0, y1 = ymax-0.62, ymax+0.48
    ztop = max((ob.matrix_world@vv.co).z for vv in ob.data.vertices if x0 < (ob.matrix_world@vv.co).x < x1)
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=80, y_subdivisions=80, size=1, location=((x0+x1)/2, (y0+y1)/2, ztop+0.012))
    DRO = bpy.context.object; DRO.name = "pano"; DRO.scale = (x1-x0, y1-y0, 1); bpy.ops.object.transform_apply(scale=True)
    # se fija la franja que queda justo sobre la cadera para que la tela no resbale hacia los pies
    pin = DRO.vertex_groups.new(name="pin")
    for vv in DRO.data.vertices:
        loc, nrm, i_, dist = BV.ray_cast(vv.co, Vector((0, 0, -1)))
        if loc is not None and dist < 0.03: pin.add([vv.index], 1.0, "REPLACE")
    cl = DRO.modifiers.new("cloth", "CLOTH"); s = cl.settings; s.vertex_group_mass = "pin"; s.pin_stiffness = 1.0; s.quality = 8; s.mass = 0.12; s.tension_stiffness = 6; s.compression_stiffness = 6
    s.shear_stiffness = 4; s.bending_stiffness = 0.25; s.air_damping = 1.5
    cl.collision_settings.distance_min = 0.003; cl.collision_settings.use_self_collision = False
    cl.point_cache.frame_start = 1; cl.point_cache.frame_end = 70
    for o in (ob, BEDO, PILLOW):
        cm = o.modifiers.new("col", "COLLISION"); o.collision.thickness_outer = 0.004; o.collision.cloth_friction = 40
    sc.frame_start, sc.frame_end = 1, 70
    t0 = time.time()
    for f in range(1, 71): sc.frame_set(f)
    print("tela", round(time.time()-t0, 1), "s", flush=True)
    bpy.context.view_layer.objects.active = DRO
    for x in bpy.context.selected_objects: x.select_set(False)
    DRO.select_set(True); bpy.ops.object.modifier_apply(modifier="cloth")
    for o in (ob, BEDO, PILLOW): o.modifiers.remove(o.modifiers["col"])
    sc.frame_set(1)
    np.savez(DR_CACHE, v=np.array([tuple(vv.co) for vv in DRO.data.vertices]), f=np.array([tuple(p.vertices) for p in DRO.data.polygons]))
DRO.data.materials.append(DRAPE)
sd = DRO.modifiers.new("g", "SOLIDIFY"); sd.thickness = 0.0015; ss = DRO.modifiers.new("s", "SUBSURF"); ss.levels = 1; ss.render_levels = 2
for p in DRO.data.polygons: p.use_smooth = True

# ---------- luz cálida de estudio sobre fondo negro
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
def area(loc, tgt, e, col, sx, sy=None):
    d = bpy.data.lights.new("a", "AREA"); d.energy = e; d.color = col; d.shape = 'RECTANGLE'; d.size = sx; d.size_y = sy or sx
    o = bpy.data.objects.new("a", d); o.location = loc; bpy.context.collection.objects.link(o)
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = (Vector(tgt)-Vector(loc)).to_track_quat('-Z', 'Y'); return o
CEN = Vector((0.05, ymax-0.18, 0.66))
KEY = area((1.05, ymax+0.55, 1.65), CEN, 170, (1.0, 0.72, 0.48), 1.4, 0.9)        # principal, cálida, cenital-posterior
RIM = area((-0.55, ymax-0.95, 1.45), CEN, 120, (1.0, 0.84, 0.66), 1.2, 0.5)       # contraluz que recorta la silueta
FILL = area((-0.20, ymax+1.50, 0.70), CEN, 10, (0.95, 0.90, 0.85), 1.4, 0.8)       # relleno bajo y suave

# ---------- aguja espinal con fiador y mano enguantada
import mano
inward = (-N45+Vector((1, 0, 0))*0.22).normalized(); dirv = -inward
nd = bpy.data.objects.new("aguja", None); bpy.context.collection.objects.link(nd)
def part(op, mat, parent, **kw):
    op(**kw); o = bpy.context.object; o.data.materials.append(mat); o.parent = parent; bpy.ops.object.shade_smooth(); return o
part(bpy.ops.mesh.primitive_cylinder_add, STEEL, nd, radius=0.0006, depth=0.090, location=(0, 0, 0.045), vertices=16)
part(bpy.ops.mesh.primitive_cone_add, STEEL, nd, radius1=0.0006, radius2=0.0, depth=0.0035, location=(0, 0, -0.00175), rotation=(math.pi, 0, 0), vertices=16)
part(bpy.ops.mesh.primitive_cylinder_add, HUBM, nd, radius=0.0042, depth=0.016, location=(0, 0, 0.098), vertices=32)
part(bpy.ops.mesh.primitive_cylinder_add, HUBM, nd, radius=0.0058, depth=0.004, location=(0, 0, 0.1075), vertices=32)
# fiador: varilla fina dentro de la aguja + cabeza que asoma del cono
sty = bpy.data.objects.new("fiador", None); bpy.context.collection.objects.link(sty); sty.parent = nd
part(bpy.ops.mesh.primitive_cylinder_add, STEEL, sty, radius=0.00035, depth=0.092, location=(0, 0, 0.064), vertices=12)
part(bpy.ops.mesh.primitive_cylinder_add, HUBM2, sty, radius=0.0050, depth=0.006, location=(0, 0, 0.1125), vertices=32)
part(bpy.ops.mesh.primitive_cylinder_add, HUBM2, sty, radius=0.0022, depth=0.006, location=(0, 0, 0.1175), vertices=24)
nd.rotation_mode = 'QUATERNION'; nd.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(dirv)
HUBLOCAL = 0.100; CAPLOCAL = 0.115
hand = mano.build_hand(GLOVE); hme = hand.data
SLEEVE = M("manga", (0.02, 0.09, 0.17), 0.85); hme.materials.append(SLEEVE)
g_w = hand.vertex_groups["wrist.R"]
_wr = [vv.co for vv in hme.vertices if any(ge.group == g_w.index and ge.weight > 0.5 for ge in vv.groups)]
_wc = sum(_wr, Vector())/len(_wr)
_g2 = hand.vertex_groups["finger3-3.R"]
_tp = [vv.co for vv in hme.vertices if any(ge.group == _g2.index and ge.weight > 0.5 for ge in vv.groups)]
_fd = (_wc-sum(_tp, Vector())/len(_tp)).normalized()   # de los dedos hacia el antebrazo
for p in hme.polygons:
    c = sum((hme.vertices[i].co for i in p.vertices), Vector())/len(p.vertices)
    if (c-_wc).dot(_fd) > 0.035: p.material_index = 1
def grp_pts(name):
    g = hand.vertex_groups[name]; return [hand.matrix_world@vv.co for vv in hme.vertices if any(ge.group == g.index and ge.weight > 0.5 for ge in vv.groups)]
wr0 = sum(grp_pts("wrist.R"), Vector())/max(1, len(grp_pts("wrist.R")))
ti = max(grp_pts("finger2-3.R"), key=lambda p: (p-wr0).length); tt = max(grp_pts("finger1-3.R"), key=lambda p: (p-wr0).length)
pinch = (ti+tt)/2; fh = (pinch-wr0).normalized(); ah = (ti-tt); ah = (ah-fh*ah.dot(fh)).normalized()
src = Matrix((fh, ah, fh.cross(ah))).transposed()
side = Vector((0, 0, 1)); side = (side-dirv*side.dot(dirv)).normalized()
ft = (inward*0.80-side*0.60).normalized()
at = dirv.cross(ft).normalized(); at = (at-ft*at.dot(ft)).normalized()
dst = Matrix((ft, at, ft.cross(at))).transposed(); RH = (dst@src.inverted()).to_4x4()
AWAY = Vector((0, 0, -5))
def place_hand(pt): hand.matrix_world = Matrix.Translation(pt)@RH@Matrix.Translation(-pinch)
def needle(d, s=0.0):
    """d: posición de la punta respecto a la piel (positivo = fuera); s: cuánto se ha retirado el fiador"""
    nd.location = P45+dirv*d; sty.location = Vector((0, 0, s))
def hide_needle(): nd.location = AWAY; hand.matrix_world = Matrix.Translation(AWAY)

# ---------- cámara y render
cam = bpy.data.cameras.new("c"); co = bpy.data.objects.new("c", cam); bpy.context.collection.objects.link(co); sc.camera = co
cam.dof.use_dof = False
HEADUP = Vector((1, 0, 0))
def aim(pos, tgt, lens, up=Vector((0, 0, 1)), focus=None):
    pos = Vector(pos); tgt = Vector(tgt); f = (tgt-pos).normalized(); r = f.cross(up).normalized(); u = r.cross(f)
    co.matrix_world = Matrix.Translation(pos)@Matrix((r, u, -f)).transposed().to_4x4(); cam.lens = lens
    if focus is not None: cam.dof.use_dof = True; cam.dof.focus_distance = (Vector(focus)-pos).length; cam.dof.aperture_fstop = 2.8
    else: cam.dof.use_dof = False
r = sc.render; r.resolution_x = int(A[1]) if len(A) > 1 else 540; r.resolution_y = r.resolution_x*16//9
r.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = int(A[2]) if len(A) > 2 else 16
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.03; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6; sc.cycles.transmission_bounces = 8; sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
r.image_settings.file_format = 'JPEG'; r.image_settings.quality = 93
DIAG = Vector((1, 0, 0.55)).normalized()
SH = {"general": ((P45.x+0.10, ymax+0.80, P45.z+0.20), (P45.x+0.15, P45.y-0.05, P45.z+0.03), 26, HEADUP),
      "intro0": ((P45.x+0.08, ymax+1.15, P45.z+0.32), (P45.x+0.15, P45.y-0.05, P45.z+0.03), 26, HEADUP),
      "arriba": ((0.05, ymax-0.22, 2.55), (0.05, ymax-0.22, 0.62), 30, Vector((1, 0, 0))),
      "crestas": ((P45.x+0.03, ymax+0.50, P45.z+0.15), (P45.x+0.01, P45.y, P45.z+0.03), 32, HEADUP),
      "rayos": ((P45.x+0.03, ymax+0.50, P45.z+0.15), (P45.x+0.01, P45.y, P45.z+0.03), 32, HEADUP),
      "marca": ((P45.x+0.01, ymax+0.30, P45.z+0.09), (P45.x+0.01, P45.y, P45.z), 45, HEADUP),
      "cara": ((1.25, ymax-0.55, 0.95), (0.75, ymax-0.25, 0.62), 50, Vector((0, 0, 1)))}
def setshot(n):
    xr = (n == "rayos")
    bsdf(SKIN).inputs["Alpha"].default_value = 0.16 if xr else 1.0
    bsdf(BRIEF).inputs["Alpha"].default_value = 0.2 if xr else 1.0
    bsdf(DRAPE).inputs["Alpha"].default_value = 0.35 if xr else 1.0
    for b, _ in BONES: b.hide_render = (not xr) or b.name.startswith(("isquion", "rama_sup", "cabeza_femur"))
    for e, _ in EYES: e.hide_render = xr
    for mk in MARKS: mk.hide_render = n in ("general", "intro0", "arriba", "cara") or (n == "crestas" and mk.name.startswith("punto"))
    hide_needle(); p, t, l, u = SH[n]; aim(p, t, l, u)
def save(path): r.filepath = path; bpy.ops.render.render(write_still=True)
ease = lambda x: x*x*(3-2*x)
if A and A[0] == "stills":
    for n in (A[3:] or SH):
        setshot(n); t = time.time(); save(f"{OUT}/s_{n}.jpg"); print(n, round(time.time()-t, 1), flush=True)
def needle_cam(d, k=0.0):
    foc = P45+dirv*(0.17+(0.10-0.17)*k); p = foc+Vector((-0.03, 0.0, 0.40+(0.30-0.40)*k)); aim(p, foc, 30+4*k, dirv)
if A and A[0] == "anim":
    kind, a0, a1 = A[3], int(A[4]), int(A[5]); od = f"{OUT}/f_{kind}"; os.makedirs(od, exist_ok=True)
    N = int(os.environ.get("NFR", "60")); DUR = float(os.environ.get("DUR", "6"))
    for f in range(a0, a1):
        u = f/(N-1)
        if kind == "intro":          # acercamiento lento al paciente
            setshot("general"); (p0, t0, l0, u0), (p1, t1, l1, u1) = SH["intro0"], SH["general"]; k = ease(u)
            aim(Vector(p0).lerp(Vector(p1), k), Vector(t0).lerp(Vector(t1), k), l0+(l1-l0)*k, u0)
        elif kind == "orbit":        # de la vista general a la cenital
            setshot("general"); (p0, t0, l0, u0), (p1, t1, l1, u1) = SH["general"], SH["arriba"]; k = ease(u)
            aim(Vector(p0).lerp(Vector(p1), k), Vector(t0).lerp(Vector(t1), k), l0+(l1-l0)*k, Vector(u0).lerp(Vector(u1), k).normalized())
        elif kind == "aguja":        # la mano acerca la aguja, entra por la línea media y avanza
            setshot("marca"); d = 0.16+(0.003-0.16)*ease(min(1, u/0.55)) if u < 0.55 else (0.003 if u < 0.68 else 0.003+(-0.035-0.003)*ease((u-0.68)/0.32))
            needle(d); place_hand(P45+dirv*(d+HUBLOCAL)); needle_cam(d, ease(u))
        elif kind == "lcr":          # la mano retira el fiador; después caen las gotas
            setshot("marca"); d = -0.035; s = 0.12*ease(min(1, u/0.30)); needle(d, s)
            if u < 0.34: place_hand(P45+dirv*(d+CAPLOCAL+s))
            else: hand.matrix_world = Matrix.Translation(AWAY)
            if u > 0.31: sty.location = Vector((0, 0, 0.6))       # el fiador ya ha salido de cuadro
            hubend = P45+dirv*(d+0.110); k = ease(min(1, u/0.5))
            p0 = hubend+Vector((0.36, 0.10, 0.14)); t0 = hubend-dirv*0.005
            p1 = hubend+Vector((0.17, 0.035, 0.02)); t1 = hubend+Vector((0, 0.006, -0.035))
            if "catch" not in globals():
                globals()["catch"] = area(hubend+Vector((0.12, 0.08, 0.06)), hubend, 1.2, (1.0, 0.95, 0.9), 0.04)
            catch.data.energy = 0.0 if u < 0.34 else 1.2
            if u < 0.34:                 # 1.º plano: aguja en vertical, la mano tira del fiador hacia arriba
                mid = P45+dirv*0.135; aim(mid+Vector((0.36, 0.0, 0.03)), mid, 50, dirv, focus=mid)
            else:                        # 2.º plano: el cono de cerca y las gotas cayendo
                k = ease(min(1, (u-0.34)/0.2)); aim(p0.lerp(p1, 0.6+0.4*k), t0.lerp(t1, 0.6+0.4*k), 50+6*k, Vector((0, 0, 1)), focus=hubend-Vector((0, 0, 0.025)))
            if "drops" not in globals():
                globals()["drops"] = []
                for i in range(6):
                    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0027, location=AWAY, segments=24, ring_count=12); o = bpy.context.object
                    o.data.materials.append(LCR); bpy.ops.object.shade_smooth(); drops.append(o)
            # tubo de muestras estéril bajo el cono (25/11): recoge las gotas y el nivel sube
            drip = hubend+dirv*0.0015; MOUTH = drip+Vector((0, 0, -0.018)); TL = 0.085; TR = 0.0065
            if "tube" not in globals():
                bpy.ops.mesh.primitive_cylinder_add(radius=TR, depth=TL, location=MOUTH-Vector((0, 0, TL/2)), vertices=48, end_fill_type='NOTHING'); tb = bpy.context.object
                bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.object.mode_set(mode='OBJECT')
                for vv in tb.data.vertices: vv.select = vv.co.z < 0
                bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.fill_grid(); bpy.ops.object.mode_set(mode='OBJECT')
                sd2 = tb.modifiers.new("g", "SOLIDIFY"); sd2.thickness = 0.0008
                tb.data.materials.append(PLAST); bpy.ops.object.shade_smooth()
                bpy.ops.mesh.primitive_cylinder_add(radius=TR+0.0002, depth=0.032, location=MOUTH-Vector((0, 0, 0.072)), vertices=48, end_fill_type='NOTHING'); lbl = bpy.context.object
                lbl.data.materials.append(LABEL); bpy.ops.object.shade_smooth()
                bpy.ops.mesh.primitive_cylinder_add(radius=TR-0.0009, depth=1.0, location=AWAY, vertices=48); lq = bpy.context.object
                lq.data.materials.append(LCR); bpy.ops.object.shade_smooth()
                bpy.ops.mesh.primitive_torus_add(major_radius=TR-0.0002, minor_radius=0.0006, location=AWAY, major_segments=48, minor_segments=12); rm = bpy.context.object
                rm.data.materials.append(M("borde_tubo", (0.92, 0.93, 0.94), 0.3)); bpy.ops.object.shade_smooth()
                globals().update(tube=tb, label=lbl, liq=lq, rim=rm)
            show = u >= 0.34
            tube.location = MOUTH-Vector((0, 0, TL/2)) if show else AWAY; label.location = MOUTH-Vector((0, 0, 0.072)) if show else AWAY
            rim.location = MOUTH-Vector((0, 0, 0.0004)) if show else AWAY
            landed = 0; surf = lambda n: MOUTH.z-TL+0.040+0.0012*n
            for i, o in enumerate(drops):
                t = (u-0.36)*DUR-i*1.0          # segundos desde que empieza a gotear (una gota por segundo)
                if t < 0: o.location = AWAY; continue
                grow = min(1, t/0.75); fall = max(0, t-0.75)
                z = drip.z-0.0022*grow-0.5*9.8*fall*fall
                if z < surf(landed): o.location = AWAY; landed += 1; continue
                o.scale = (grow, grow, grow*(1.0+0.6*min(1, fall*4)))
                o.location = Vector((drip.x, drip.y, z))
            h = surf(landed)-(MOUTH.z-TL+0.0008)
            liq.scale = (1, 1, h); liq.location = Vector((MOUTH.x, MOUTH.y, MOUTH.z-TL+0.0008+h/2)) if show else AWAY
        save(f"{od}/{f:03d}.jpg"); print(kind, f, flush=True)
    print("ok", kind, a0, a1, flush=True)
