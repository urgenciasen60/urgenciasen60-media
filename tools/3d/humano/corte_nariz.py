"""Corte sagital medio de la cabeza (epistaxis v2, 25/11/2026). La mitad derecha del paciente real (paciente.py),
cortada en la línea media y vista desde la izquierda: piel, partes blandas, hueso propio de la nariz, cartílago septal,
lámina perpendicular, vómer, paladar duro y blando, incisivo, lengua, rinofaringe, y la mucosa del tabique con el plexo
de Kiesselbach. Los instrumentos entran por el espacio de la fosa izquierda, delante del tabique.
Uso: python3 corte_nariz.py -- stills RES SAMPLES [planos]
     python3 corte_nariz.py -- anim RES SAMPLES intro|rayos|rinos|nitrato|tapon F0 F1   (NFR)"""
import bpy, bmesh, sys, os, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
A = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
OUT = os.environ.get("EPIOUT", "/home/claude/v3d/epi"); os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
import paciente
from paciente import mat
P = paciente.crear({}, ropa=False, pelo=False); ob = P["ob"]; REST = P["REST"]; eyec = P["eyec"]
# cabeza sola, malla suavizada y cortada por la línea media (se queda la mitad derecha, x < 0)
ob.modifiers["s"].levels = 2
dg = bpy.context.evaluated_depsgraph_get(); me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
bm = bmesh.new(); bm.from_mesh(me)
bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.calc_center_median().z < eyec.z-0.17], context='FACES')
BV = BVHTree.FromBMesh(bm)          # cabeza entera: el perfil se toma antes de cortar
bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_outer=True)
bm.to_mesh(me); bm.free(); half = bpy.data.objects.new("media_cabeza", me); bpy.context.collection.objects.link(half)
for p in me.polygons: p.use_smooth = True
bpy.data.objects.remove(ob); bpy.data.objects.remove(P["eyes"])
# perfil sagital por rayos desde el centro de la cabeza (en el plano x = 0)
C = Vector((0, eyec.y+0.05, eyec.z-0.04)); prof = []
for a in np.linspace(0, 2*math.pi, 1440, endpoint=False):
    d = Vector((0, math.cos(a), math.sin(a))); hit = BV.ray_cast(C+d*0.5, -d)      # desde fuera hacia dentro: superficie exterior
    if hit[0] is not None: prof.append(Vector((0, hit[0].y, hit[0].z)))
yz = np.array([(p.y, p.z) for p in prof])
print('perfil', len(prof), 'ojos', round(eyec.y,3), round(eyec.z,3), 'y', yz[:,0].min().round(3), yz[:,0].max().round(3), 'z', yz[:,1].min().round(3), yz[:,1].max().round(3), flush=True)
# referencias del perfil: punta nasal, subnasal y nasion
band = [(y, z) for y, z in yz if eyec.z-0.07 < z < eyec.z+0.02]
TIP = min(band, key=lambda q: q[0])
SUB = max([(y, z) for y, z in yz if TIP[1]-0.030 < z < TIP[1]-0.008 and y < TIP[0]+0.03], key=lambda q: q[0])
NAS = max([(y, z) for y, z in yz if eyec.z-0.01 < z < eyec.z+0.025 and y < TIP[0]+0.04], key=lambda q: q[0])
ys, zs = SUB; FLOOR = zs+0.004
def W(u, v): return (ys+u, zs+v)              # u: hacia atrás desde el subnasal; v: hacia arriba
tipu, tipv = TIP[0]-ys, TIP[1]-zs; nasu, nasv = NAS[0]-ys, NAS[1]-zs
# ---------- materiales
def T(m, kind, scale, **kw):
    nt = m.node_tree; tc = nt.nodes.get("tc") or nt.nodes.new("ShaderNodeTexCoord"); tc.name = "tc"
    t = nt.nodes.new(kind); t.inputs["Scale"].default_value = scale
    for k, v in kw.items():
        if k in t.inputs: t.inputs[k].default_value = v
        else: setattr(t, k, v)
    nt.links.new(tc.outputs["Object"], t.inputs["Vector"]); return t
def RAMP(m, src, stops, to="Base Color"):
    nt = m.node_tree; r = nt.nodes.new("ShaderNodeValToRGB"); el = r.color_ramp.elements
    while len(el) < len(stops): el.new(0.5)
    for e_, (p, c) in zip(el, stops): e_.position = p; e_.color = (*c, 1)
    nt.links.new(src, r.inputs["Fac"]); nt.links.new(r.outputs["Color"], nt.nodes["Principled BSDF"].inputs[to]); return r
def BUMP(m, src, s, d):
    nt = m.node_tree; bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = s; bp.inputs["Distance"].default_value = d
    nt.links.new(src, bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], nt.nodes["Principled BSDF"].inputs["Normal"])
SOFTT = mat("partes_blandas", (0.62, 0.30, 0.26), 0.5, **{"Subsurface Weight": 0.2})
n_ = T(SOFTT, "ShaderNodeTexWave", 220, wave_type="BANDS", bands_direction="DIAGONAL", Distortion=6.0, Detail=4.0)
RAMP(SOFTT, n_.outputs["Fac"], [(0.2, (0.55, 0.22, 0.20)), (0.8, (0.70, 0.36, 0.30))]); BUMP(SOFTT, n_.outputs["Fac"], 0.15, 0.0003)
FATM = mat("grasa", (0.92, 0.76, 0.36), 0.35, **{"Coat Weight": 0.3})
vf = T(FATM, "ShaderNodeTexVoronoi", 420, feature="DISTANCE_TO_EDGE"); RAMP(FATM, vf.outputs["Distance"], [(0.0, (0.90, 0.78, 0.66)), (0.05, (0.95, 0.78, 0.32)), (1.0, (0.86, 0.64, 0.18))])
CORT = mat("cortical", (0.92, 0.88, 0.78), 0.4)
CANC = mat("esponjoso", (0.80, 0.55, 0.45), 0.6)
vc = T(CANC, "ShaderNodeTexVoronoi", 900, feature="DISTANCE_TO_EDGE"); RAMP(CANC, vc.outputs["Distance"], [(0.0, (0.92, 0.85, 0.72)), (0.10, (0.92, 0.85, 0.72)), (0.18, (0.72, 0.40, 0.32)), (1.0, (0.60, 0.26, 0.22))])
CART = mat("cartilago", (0.80, 0.86, 0.92), 0.25, **{"Subsurface Weight": 0.4, "Coat Weight": 0.5})
nc = T(CART, "ShaderNodeTexNoise", 300); RAMP(CART, nc.outputs["Fac"], [(0.3, (0.74, 0.82, 0.90)), (0.7, (0.86, 0.90, 0.95))])
MUC = mat("mucosa", (0.78, 0.32, 0.32), 0.30, **{"Coat Weight": 0.8, "Coat Roughness": 0.15, "Subsurface Weight": 0.25, "Alpha": 0.55})
# red vascular: bordes de Voronoi distorsionados, más densos en el área de Kiesselbach (atributo «kiess» por vértice)
nt = MUC.node_tree; tcm = nt.nodes.new("ShaderNodeTexCoord"); ns = nt.nodes.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value = 180
nt.links.new(tcm.outputs["Object"], ns.inputs["Vector"]); mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = 'VECTOR'; mx.inputs["Factor"].default_value = 0.25
nt.links.new(tcm.outputs["Object"], mx.inputs["A"]); nt.links.new(ns.outputs["Color"], mx.inputs["B"])
vv = nt.nodes.new("ShaderNodeTexVoronoi"); vv.feature = 'DISTANCE_TO_EDGE'; vv.inputs["Scale"].default_value = 260; nt.links.new(mx.outputs["Result"], vv.inputs["Vector"])
vr = nt.nodes.new("ShaderNodeMapRange"); vr.inputs["From Min"].default_value = 0.0; vr.inputs["From Max"].default_value = 0.05
vr.inputs["To Min"].default_value = 1.6; vr.inputs["To Max"].default_value = 0.0; nt.links.new(vv.outputs["Distance"], vr.inputs["Value"])
ka = nt.nodes.new("ShaderNodeAttribute"); ka.attribute_name = "kiess"; km = nt.nodes.new("ShaderNodeMath"); km.operation = 'MULTIPLY'
nt.links.new(vr.outputs["Result"], km.inputs[0]); nt.links.new(ka.outputs["Fac"], km.inputs[1])
mc = nt.nodes.new("ShaderNodeMix"); mc.data_type = 'RGBA'; mc.inputs["A"].default_value = (0.80, 0.40, 0.38, 1); mc.inputs["B"].default_value = (0.42, 0.02, 0.03, 1)
nt.links.new(km.outputs["Value"], mc.inputs["Factor"]); nt.links.new(mc.outputs["Result"], nt.nodes["Principled BSDF"].inputs["Base Color"])
TOOTH = mat("diente", (0.93, 0.90, 0.82), 0.25, **{"Coat Weight": 0.6})
TONGUE = mat("lengua", (0.70, 0.30, 0.30), 0.45, **{"Subsurface Weight": 0.3})
AIR = mat("aire", (0.015, 0.008, 0.008), 0.9)
BRAIN = mat("encefalo", (0.80, 0.70, 0.66), 0.55)
BLOOD = mat("sangre", (0.22, 0.003, 0.008), 0.08, **{"Coat Weight": 1.0, "Subsurface Weight": 0.3})
SKINCUT = mat("piel_corte", (0.70, 0.45, 0.36), 0.5)
for p in half.data.polygons: p.material_index = 0
# ---------- formas 2D en el plano del corte
def spline(Pts, n=6):
    Pts = [Vector(p) for p in Pts]; out = []; L_ = len(Pts)
    for i in range(L_):
        p0, p1, p2, p3 = Pts[(i-1) % L_], Pts[i], Pts[(i+1) % L_], Pts[(i+2) % L_]
        for k in range(n):
            t = k/n; out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3))
    return out
def shape(name, pts_uv, m, x=0.0006, smooth=True, absolute=False):
    pts = [Vector(W(*p)) if not absolute else Vector(p) for p in pts_uv]
    if smooth: pts = spline(pts)
    bm = bmesh.new(); vs = [bm.verts.new((x, p.x, p.y)) for p in pts]; f = bm.faces.new(vs)
    if f.normal.x < 0: f.normal_flip()
    bmesh.ops.triangulate(bm, faces=[f])
    me2 = bpy.data.meshes.new(name); bm.to_mesh(me2); bm.free(); o = bpy.data.objects.new(name, me2); bpy.context.collection.objects.link(o); me2.materials.append(m); return o
# tapa del corte: todo el perfil
shape("tapa", [tuple(q) for q in yz[::2]], SOFTT, x=0.0001, smooth=False, absolute=True)
# piel (banda de 2,5 mm por dentro del perfil) y tejido subcutáneo de la nariz
inner = []
for i in range(0, len(prof), 2):
    p = prof[i]; q = prof[(i+2) % len(prof)]; t = (q-p).normalized(); nrm = Vector((0, -t.z, t.y))
    if (C-p).dot(nrm) < 0: nrm = -nrm
    inner.append(p+nrm*0.0025)
o = shape("piel", [(p.y, p.z) for p in prof[::2]], SKINCUT, x=0.00025, smooth=False, absolute=True)
shape("dermis_int", [(p.y, p.z) for p in inner], SOFTT, x=0.0003, smooth=False, absolute=True)
# encéfalo y hueso frontal (arriba), seno frontal
shape("frontal", [(nasu+0.004, nasv+0.002), (nasu+0.003, nasv+0.030), (nasu+0.020, nasv+0.070), (nasu+0.060, nasv+0.080), (nasu+0.060, nasv+0.018), (nasu+0.028, nasv+0.004)], CANC, x=0.0005)
shape("seno_frontal", [(nasu+0.010, nasv+0.010), (nasu+0.010, nasv+0.032), (nasu+0.020, nasv+0.040), (nasu+0.024, nasv+0.016)], AIR, x=0.0007)
shape("encefalo", [(nasu+0.030, nasv+0.040), (nasu+0.040, nasv+0.078), (nasu+0.090, nasv+0.090), (nasu+0.095, nasv+0.030), (nasu+0.060, nasv+0.022)], BRAIN, x=0.0007)
# rinofaringe (aire) por detrás del tabique, sobre el paladar blando
shape("rinofaringe", [(0.058, 0.006), (0.060, 0.050), (0.085, 0.060), (0.095, 0.010), (0.085, -0.012), (0.070, -0.006)], AIR, x=0.0005)
# paladar duro, paladar blando, incisivo y lengua
shape("paladar", [(0.010, -0.002), (0.016, 0.002), (0.060, 0.000), (0.062, -0.006), (0.024, -0.010), (0.020, -0.018), (0.012, -0.012)], CANC, x=0.0007)
shape("paladar_cort", [(0.014, 0.002), (0.060, 0.000), (0.061, -0.0015), (0.015, 0.0005)], CORT, x=0.0008, smooth=False)
shape("paladar_blando", [(0.060, 0.000), (0.075, -0.006), (0.088, -0.022), (0.082, -0.026), (0.070, -0.014), (0.060, -0.007)], SOFTT, x=0.0008)
shape("incisivo", [(0.017, 0.000), (0.021, -0.002), (0.023, -0.012), (0.021, -0.022), (0.017, -0.023), (0.015, -0.012)], TOOTH, x=0.0009)
shape("lengua", [(0.022, -0.030), (0.028, -0.016), (0.050, -0.013), (0.075, -0.030), (0.080, -0.060), (0.034, -0.062), (0.022, -0.046)], TONGUE, x=0.0006)
# tabique: hueso propio, cartílago cuadrangular, lámina perpendicular del etmoides y vómer
db = Vector(TIP)-Vector(NAS); dbn = db.normalized()
nb_end = Vector(NAS)+db*0.45; nbu, nbv = nb_end.x-ys, nb_end.y-zs
shape("hueso_propio", [(nasu+0.002, nasv-0.001), (nbu+0.0025, nbv), (nbu+0.0055, nbv-0.002), (nasu+0.008, nasv-0.004)], CORT, x=0.0009)
SEPT = [(nbu+0.004, nbv-0.001), (tipu+0.010, tipv+0.004), (0.008, 0.012), (0.012, 0.005), (0.032, 0.006), (0.036, 0.030), (nbu+0.020, nbv+0.004)]
shape("cartilago", SEPT, CART, x=0.0008)
shape("lamina_perp", [(nbu+0.006, nbv+0.003), (nasu+0.012, nasv+0.002), (nasu+0.030, nasv+0.016), (0.056, 0.040), (0.036, 0.030), (nbu+0.020, nbv+0.004)], CANC, x=0.0008)
shape("vomer", [(0.032, 0.006), (0.058, 0.004), (0.060, 0.018), (0.056, 0.040), (0.036, 0.030)], CANC, x=0.0008)
# mucosa del tabique (semitransparente) con el área de Kiesselbach en el tercio anteroinferior
mu = shape("mucosa_tabique", [(0.010, 0.006), (tipu+0.012, tipv+0.003), (nbu+0.006, nbv-0.003), (nasu+0.014, nasv+0.002), (nasu+0.030, nasv+0.014), (0.056, 0.038), (0.058, 0.005)], MUC, x=0.0013)
bm = bmesh.new(); bm.from_mesh(mu.data); bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=6, use_grid_fill=True); bm.to_mesh(mu.data); bm.free()
KIESS = Vector((0, *W(0.016, 0.014)))
ka_ = mu.data.attributes.new("kiess", 'FLOAT', 'POINT')
for v in mu.data.vertices:
    d = (Vector((0, v.co.y, v.co.z))-KIESS).length; ka_.data[v.index].value = 0.35+0.65*math.exp(-(d/0.012)**2)
# punto sangrante y gota que baja hacia el suelo
BLEED = Vector((0.0018, *W(0.015, 0.013)))
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0024, location=BLEED, segments=24, ring_count=12); spot = bpy.context.object; spot.scale = (0.35, 1.0, 0.8); spot.data.materials.append(BLOOD); bpy.ops.object.shade_smooth()
cu = bpy.data.curves.new("hilo", "CURVE"); cu.dimensions = '3D'; sp = cu.splines.new('NURBS')
pts = [BLEED+Vector((-0.0006, 0.0003*k+0.0004*math.sin(k*1.7), -0.0016*k)) for k in range(6)]; sp.points.add(len(pts)-1)
for p_, q in zip(sp.points, pts): p_.co = (*q, 1)
sp.use_endpoint_u = True; cu.bevel_depth = 0.0011; trickle = bpy.data.objects.new("hilo", cu); bpy.context.collection.objects.link(trickle); cu.materials.append(BLOOD)
ASH = mat("escara", (0.55, 0.55, 0.53), 0.7)
# ---------- instrumentos (en la fosa izquierda, delante del tabique)
STEEL = mat("acero", (0.92, 0.92, 0.95), 0.15, Metallic=1.0)
GLOVE = mat("guante", (0.50, 0.51, 0.52), 0.68)
FLOOR_DIR = Vector((0, 1, 0.04)).normalized()                       # paralelo al suelo de la fosa (hacia atrás)
NOS = Vector((0.004, *W(0.009, 0.009)))                              # entrada de la narina
def stick(name, length, r, m):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=length, vertices=16); o = bpy.context.object; o.data.materials.append(m); bpy.ops.object.shade_smooth()
    o.data.transform(Matrix.Translation((0, 0, length/2))); o.rotation_mode = 'QUATERNION'; return o
# aplicador de nitrato de plata: varilla blanca con la punta gris
APP = stick("aplicador", 0.15, 0.0011, mat("varilla", (0.90, 0.88, 0.82), 0.5))
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0019, segments=16, ring_count=8); tipb = bpy.context.object; tipb.parent = APP; tipb.data.materials.append(mat("nitrato", (0.20, 0.20, 0.21), 0.35)); tipb.scale = (1, 1, 1.4)
# esponja nasal (tapón anterior): bloque alargado de espuma con cordón
SP = mat("esponja", (0.90, 0.86, 0.80), 0.85, **{"Subsurface Weight": 0.2})
vs_ = T(SP, "ShaderNodeTexVoronoi", 900); BUMP(SP, vs_.outputs["Distance"], 0.5, 0.0004)
bpy.ops.mesh.primitive_cube_add(size=1); spg = bpy.context.object; spg.data.materials.append(SP)
spg.data.transform(Matrix.Translation((0, 0.5, 0))); bv = spg.modifiers.new("b", "BEVEL"); bv.width = 0.15; bv.segments = 4; bv.affect = 'EDGES'
spg.scale = (0.004, 0.080, 0.009)
cord = stick("cordon", 0.05, 0.0005, mat("cordon", (0.92, 0.92, 0.9), 0.6))
# espéculo nasal (dos valvas) y haz de luz
VAL = []
for sgn in (1, -1):
    bpy.ops.mesh.primitive_cube_add(size=1); v_ = bpy.context.object; v_.scale = (0.0005, 0.014, 0.0035); v_.data.materials.append(mat("valva", (0.80, 0.80, 0.82), 0.30, Metallic=1.0))
    bv = v_.modifiers.new("b", "BEVEL"); bv.width = 0.0003; VAL.append((v_, sgn))
LIGHT = bpy.data.lights.new("frontal", "SPOT"); LIGHT.energy = 0; LIGHT.spot_size = math.radians(16); LIGHT.spot_blend = 0.6; LIGHT.color = (1.0, 0.97, 0.92); LIGHT.shadow_soft_size = 0.002
LO = bpy.data.objects.new("frontal", LIGHT); bpy.context.collection.objects.link(LO)
AWAY = Vector((0, 0, -9))
def hide_all():
    for o in (APP, spg, cord) + tuple(v for v, _ in VAL): o.location = AWAY
    LIGHT.energy = 0
def place_along(o, base, d):
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d); o.location = base
# ---------- luz y cámara
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
FOC = Vector((0.0, *W(0.024, 0.018)))
def area(loc, tgt, e, col, s):
    d = bpy.data.lights.new("a", "AREA"); d.energy = e; d.color = col; d.size = s; o = bpy.data.objects.new("a", d); o.location = loc; bpy.context.collection.objects.link(o)
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = (Vector(tgt)-Vector(loc)).to_track_quat('-Z', 'Y'); return o
area(FOC+Vector((0.40, -0.25, 0.35)), FOC, 3.2, (1.0, 0.80, 0.62), 0.5)
area(FOC+Vector((0.35, 0.30, -0.10)), FOC, 0.9, (0.88, 0.92, 1.0), 0.4)
area(FOC+Vector((-0.30, -0.10, 0.25)), FOC+Vector((0, -0.04, 0)), 6, (1.0, 0.85, 0.70), 0.5)   # contraluz de la silueta
cam = bpy.data.cameras.new("c"); co = bpy.data.objects.new("c", cam); bpy.context.collection.objects.link(co); sc.camera = co
def aim(pos, tgt, lens, focus=None):
    pos = Vector(pos); tgt = Vector(tgt); f = (tgt-pos).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); u = r.cross(f)
    co.matrix_world = Matrix.Translation(pos)@Matrix((r, u, -f)).transposed().to_4x4(); cam.lens = lens
    cam.dof.use_dof = focus is not None
    if focus is not None: cam.dof.focus_distance = (Vector(focus)-pos).length; cam.dof.aperture_fstop = 5.6
r = sc.render; r.resolution_x = int(A[1]) if len(A) > 1 else 360; r.resolution_y = r.resolution_x*16//9
r.engine = 'CYCLES'; sc.cycles.samples = int(A[2]) if len(A) > 2 else 24; sc.cycles.use_denoising = True; sc.cycles.use_adaptive_sampling = True
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; r.image_settings.file_format = 'JPEG'; r.image_settings.quality = 93
SIDEV = (FOC+Vector((0.34, 0.0, 0.0)), FOC, 50)                     # vista lateral del corte
CLOSE = (Vector((0.20, *W(0.018, 0.012))), Vector((0, *W(0.018, 0.012))), 55)
OBLQ = (FOC+Vector((0.30, -0.22, 0.10)), FOC, 45)                   # tres cuartos: se ve que es media cabeza
SH = {"lateral": SIDEV, "cerca": CLOSE, "oblicua": OBLQ}
ease = lambda x: x*x*(3-2*x)
def save(path): r.filepath = path; bpy.ops.render.render(write_still=True)
def frame(kind, u):
    hide_all(); spot.hide_render = kind in ("intro", "tapon"); trickle.hide_render = spot.hide_render
    spot.data.materials[0] = BLOOD
    if kind == "intro":                    # de tres cuartos a la vista lateral del corte
        k = ease(u); (p0, t0, l0), (p1, t1, l1) = OBLQ, SIDEV; aim(p0.lerp(p1, k), t0.lerp(t1, k), l0+(l1-l0)*k)
    elif kind == "rayos":                  # acercamiento al tabique anterior
        k = ease(u); (p0, t0, l0), (p1, t1, l1) = SIDEV, CLOSE; aim(p0.lerp(p1, k), t0.lerp(t1, k), l0+(l1-l0)*k)
    elif kind == "rinos":                  # espéculo en el vestíbulo y luz frontal sobre el tabique anterior
        k = ease(min(1, u/0.4))
        for v_, sgn in VAL:
            v_.rotation_euler = (math.radians(14*sgn*k), 0, 0); v_.location = NOS+Vector((0.0016, 0.008, 0.0045*sgn*k))
        LO.location = NOS+Vector((0.03, -0.20, 0.02)); LO.rotation_mode = 'QUATERNION'; LO.rotation_quaternion = (BLEED-LO.location).to_track_quat('-Z', 'Y')
        LIGHT.energy = 6*ease(min(1, u/0.5)); aim(*CLOSE)
    elif kind == "nitrato":                # el aplicador toca solo el punto; la mucosa queda gris
        k = ease(min(1, u/0.55)); d = (BLEED+Vector((0.0005, 0, 0))-(NOS+Vector((0.002, -0.03, -0.004)))).normalized()
        place_along(APP, BLEED+Vector((0.0016, 0, 0))-d*(0.15+0.06*(1-k)), d); tipb.location = (0, 0, 0.15+0.001)
        if u > 0.6: spot.data.materials[0] = ASH; trickle.hide_render = True
        aim(*CLOSE)
    elif kind == "tapon":                  # tapón paralelo al suelo de la fosa; después se expande
        k = ease(min(1, u/0.6)); e = 1+0.45*ease(max(0, (u-0.7)/0.3))
        spg.rotation_mode = 'QUATERNION'; spg.rotation_quaternion = Vector((0, 1, 0)).rotation_difference(FLOOR_DIR)
        spg.location = Vector((0.0045, *W(0.006-0.065*(1-k), 0.0080))); spg.scale = (0.0035*e, 0.055, 0.0060*e)
        place_along(cord, spg.location+Vector((0, 0.002, -0.001)), Vector((0, -1, -0.9)).normalized()); cord.scale = (1, 1, 0.45)
        aim(*SIDEV)
if A and A[0] == "stills":
    for n in (A[3:] or SH):
        hide_all(); aim(*SH[n]); save(f"{OUT}/c_{n}.jpg"); print(n, flush=True)
if A and A[0] == "test":
    for kind, u in [("rinos", 1.0), ("nitrato", 0.5), ("tapon", 0.65), ("tapon", 1.0)]:
        frame(kind, u); save(f"{OUT}/ct_{kind}_{u}.jpg"); print(kind, u, flush=True)
if A and A[0] == "anim":
    kind, a0, a1 = A[3], int(A[4]), int(A[5]); N = int(os.environ.get("NFR", "36")); od = f"{OUT}/f_c{kind}"; os.makedirs(od, exist_ok=True)
    for fr in range(a0, a1):
        frame(kind, fr/(N-1)); save(f"{od}/{fr:03d}.jpg"); print(kind, fr, flush=True)
