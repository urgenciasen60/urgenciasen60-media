"""Corte sagital medio de la columna lumbar (L3-L5) con la aguja entrando en L4-L5 — v4, aspecto realista.
Capas (de fuera adentro): piel, tejido subcutáneo, ligamento supraespinoso, apófisis espinosas y ligamento interespinoso,
ligamento amarillo, grasa epidural, duramadre-aracnoides, espacio subaracnoideo con LCR y raíces de la cola de caballo,
duramadre anterior, ligamento longitudinal posterior, cuerpos vertebrales y discos.
x = profundidad desde la piel (m), z = craneal (+). Uso: python3 corte_v4.py -- RES SAMPLES F0 F1 [NFR]"""
import bpy, bmesh, math, sys, os
from mathutils import Vector
A = sys.argv[sys.argv.index("--")+1:]
OUT = os.environ.get("V4OUT", "/home/claude/v3d/v4")+"/f_corte"; os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
DEPTH = 0.05
def mat(n, c, r=0.5, coat=0.0, sss=0.0, e=0.0):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = r; b.inputs["Coat Weight"].default_value = coat
    if sss: b.inputs["Subsurface Weight"].default_value = sss; b.inputs["Subsurface Radius"].default_value = (1, 0.4, 0.25); b.inputs["Subsurface Scale"].default_value = 0.002
    if e: b.inputs["Emission Color"].default_value = (*c, 1); b.inputs["Emission Strength"].default_value = e
    return m
def T(m, kind, scale, **kw):
    nt = m.node_tree; tc = nt.nodes.get("tc") or nt.nodes.new("ShaderNodeTexCoord"); tc.name = "tc"
    t = nt.nodes.new(kind); t.inputs["Scale"].default_value = scale
    for k, v in kw.items():
        if k in t.inputs: t.inputs[k].default_value = v
        else: setattr(t, k, v)
    src = tc.outputs["Object"]
    if "rot" in kw: pass
    nt.links.new(src, t.inputs["Vector"]); return t
def RAMP(m, src, stops):
    nt = m.node_tree; r = nt.nodes.new("ShaderNodeValToRGB"); el = r.color_ramp.elements
    while len(el) < len(stops): el.new(0.5)
    for e_, (p, c) in zip(el, stops): e_.position = p; e_.color = (*c, 1)
    nt.links.new(src, r.inputs["Fac"]); nt.links.new(r.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"]); return r
def BUMP(m, src, s, d):
    nt = m.node_tree; bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = s; bp.inputs["Distance"].default_value = d
    nt.links.new(src, bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], nt.nodes["Principled BSDF"].inputs["Normal"])
# --- materiales con textura procedimental
EPI = mat("epidermis", (0.55, 0.33, 0.24), 0.45, sss=0.2)
DER = mat("dermis", (0.80, 0.50, 0.45), 0.55, sss=0.3); t = T(DER, "ShaderNodeTexNoise", 900); RAMP(DER, t.outputs["Fac"], [(0.35, (0.78, 0.45, 0.40)), (0.65, (0.88, 0.60, 0.52))])
FAT = mat("grasa", (0.95, 0.78, 0.35), 0.35, coat=0.3, sss=0.3)
v = T(FAT, "ShaderNodeTexVoronoi", 200, feature="DISTANCE_TO_EDGE", Randomness=1.0); RAMP(FAT, v.outputs["Distance"], [(0.0, (0.92, 0.80, 0.70)), (0.035, (0.92, 0.80, 0.70)), (0.06, (0.97, 0.80, 0.30)), (1.0, (0.90, 0.68, 0.18))]); BUMP(FAT, v.outputs["Distance"], 0.35, 0.0006)
LIG = mat("ligamento", (0.90, 0.86, 0.82), 0.30, coat=0.2, sss=0.15)
w = T(LIG, "ShaderNodeTexWave", 140, wave_type="BANDS", bands_direction="Z", Distortion=3.0, Detail=3.0); RAMP(LIG, w.outputs["Fac"], [(0.2, (0.80, 0.72, 0.70)), (0.8, (0.95, 0.92, 0.88))]); BUMP(LIG, w.outputs["Fac"], 0.2, 0.0003)
ISP = mat("interespinoso", (0.86, 0.76, 0.72), 0.32, coat=0.2, sss=0.15)
w2 = T(ISP, "ShaderNodeTexWave", 160, wave_type="BANDS", bands_direction="DIAGONAL", Distortion=4.0, Detail=3.0); RAMP(ISP, w2.outputs["Fac"], [(0.2, (0.74, 0.58, 0.56)), (0.8, (0.93, 0.86, 0.82))]); BUMP(ISP, w2.outputs["Fac"], 0.2, 0.0003)
FLAV = mat("amarillo", (1.0, 0.80, 0.22), 0.30, coat=0.3, sss=0.2)
w3 = T(FLAV, "ShaderNodeTexWave", 220, wave_type="BANDS", bands_direction="Z", Distortion=2.0, Detail=2.0); RAMP(FLAV, w3.outputs["Fac"], [(0.2, (0.95, 0.70, 0.12)), (0.8, (1.0, 0.86, 0.38))])
EPF = mat("grasa_epidural", (0.98, 0.88, 0.55), 0.35, coat=0.3)
v2 = T(EPF, "ShaderNodeTexVoronoi", 500); RAMP(EPF, v2.outputs["Distance"], [(0.0, (0.55, 0.08, 0.10)), (0.08, (0.55, 0.08, 0.10)), (0.12, (0.99, 0.88, 0.55)), (1.0, (0.95, 0.80, 0.42))])
DURA = mat("duramadre", (0.78, 0.84, 0.95), 0.18, coat=0.6, sss=0.1)
CSF = mat("lcr", (0.18, 0.36, 0.58), 0.05, coat=1.0, e=0.04)
n = T(CSF, "ShaderNodeTexNoise", 60); RAMP(CSF, n.outputs["Fac"], [(0.3, (0.14, 0.30, 0.52)), (0.7, (0.26, 0.46, 0.68))])
ROOT = mat("raiz", (0.95, 0.90, 0.78), 0.35, coat=0.3, sss=0.2)
CORT = mat("cortical", (0.94, 0.90, 0.80), 0.40)
CANC = mat("esponjoso", (0.85, 0.55, 0.45), 0.6)
v3 = T(CANC, "ShaderNodeTexVoronoi", 1500, feature="DISTANCE_TO_EDGE", Randomness=1.0); RAMP(CANC, v3.outputs["Distance"], [(0.0, (0.93, 0.86, 0.74)), (0.08, (0.93, 0.86, 0.74)), (0.16, (0.72, 0.40, 0.32)), (1.0, (0.58, 0.26, 0.22))]); BUMP(CANC, v3.outputs["Distance"], 0.5, 0.0004)
ANN = mat("anillo_fibroso", (0.88, 0.90, 0.92), 0.3, coat=0.3)
w4 = T(ANN, "ShaderNodeTexWave", 180, wave_type="BANDS", bands_direction="Z", Distortion=1.0); RAMP(ANN, w4.outputs["Fac"], [(0.3, (0.78, 0.82, 0.88)), (0.7, (0.95, 0.96, 0.97))])
NUC = mat("nucleo", (0.70, 0.78, 0.92), 0.15, coat=0.8, sss=0.3)
STEEL = mat("acero", (0.92, 0.92, 0.95), 0.12); STEEL.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0
# --- geometría: perfiles 2D (x, z) extruidos en profundidad (y)
def spline(P, n=6, closed=True):
    P = [Vector(p) for p in P]; out = []; L = len(P)
    for i in range(L if closed else L-1):
        p0 = P[(i-1) % L] if closed else P[max(i-1, 0)]; p1 = P[i]; p2 = P[(i+1) % L]; p3 = P[(i+2) % L] if closed else P[min(i+2, L-1)]
        for k in range(n):
            t = k/n; out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3))
    return out
def slab(name, pts, m, y0=0.0, depth=DEPTH, smooth=True):
    pts = spline(pts) if smooth else [Vector(p) for p in pts]
    bm = bmesh.new(); vs = [bm.verts.new((p.x, y0, p.y)) for p in pts]; f = bm.faces.new(vs)
    if f.normal.y > 0: f.normal_flip()
    ex = bmesh.ops.extrude_face_region(bm, geom=[f]); nv = [e for e in ex["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, depth, 0), verts=nv)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); me.materials.append(m)
    return o
def rect(name, x0, x1, z0, z1, m, y0=0.0): return slab(name, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)], m, y0, smooth=False)
Z0, Z1 = -0.17, 0.17
rect("epidermis", 0.0, 0.0008, Z0, Z1, EPI); rect("dermis", 0.0008, 0.0030, Z0, Z1, DER)
rect("grasa", 0.0030, 0.0200, Z0, Z1, FAT)
rect("supraespinoso", 0.0200, 0.0240, Z0, Z1, LIG)
rect("interespinoso", 0.0240, 0.0520, Z0, Z1, ISP, 0.0003)          # queda detrás de las apófisis
rect("amarillo", 0.0500, 0.0620, Z0, Z1, FLAV, 0.0006)
rect("epidural", 0.0620, 0.0660, Z0, Z1, EPF)
rect("dura_post", 0.0660, 0.0668, Z0, Z1, DURA)
rect("lcr", 0.0668, 0.0800, Z0, Z1, CSF, 0.0012)
rect("dura_ant", 0.0800, 0.0808, Z0, Z1, DURA)
rect("fondo_cuerpos", 0.0832, 0.13, Z0, Z1, CANC, 0.003)
rect("lig_long_post", 0.0808, 0.0832, Z0, Z1, LIG)
LEV = {"L2": 0.080, "L3": 0.040, "L4": 0.0, "L5": -0.040, "S1": -0.080}
for nme, zc in LEV.items():
    # apófisis espinosa + lámina (en la línea media), algo inclinada en sentido caudal
    sp = [(0.0245, zc+0.006), (0.0245, zc-0.013), (0.032, zc-0.014), (0.050, zc-0.009), (0.0585, zc-0.011), (0.0605, zc-0.004), (0.0600, zc+0.011), (0.0580, zc+0.014), (0.050, zc+0.010), (0.032, zc+0.009)]
    slab("espinosa_"+nme, sp, CORT, -0.0001)
    c = Vector((0.043, zc-0.0005)); inner = [(c+(Vector(p)-c)*0.80) for p in sp]
    slab("esponjosa_"+nme, [tuple(p) for p in inner], CANC, -0.0003, depth=0.0002)
    # cuerpo vertebral (algo craneal a su apófisis espinosa) y disco por debajo
    zb = zc+0.014; body = [(0.0832, zb-0.0145), (0.13, zb-0.0145), (0.13, zb+0.0145), (0.0832, zb+0.0145)]
    slab("cuerpo_"+nme, body, CORT, 0.0, smooth=False)
    slab("cuerpo_esp_"+nme, [(0.0848, zb-0.013), (0.13, zb-0.013), (0.13, zb+0.013), (0.0848, zb+0.013)], CANC, -0.0002, depth=0.0002, smooth=False)
    zd = zb-0.0145-0.0055
    slab("disco_"+nme, [(0.0832, zd-0.0055), (0.13, zd-0.0055), (0.13, zd+0.0055), (0.0832, zd+0.0055)], ANN, 0.0, smooth=False)
    slab("nucleo_"+nme, [(0.096, zd-0.0035), (0.12, zd-0.0035), (0.12, zd+0.0035), (0.096, zd+0.0035)], NUC, -0.0002, depth=0.0002)
# raíces de la cola de caballo: fibras longitudinales algo onduladas dentro del saco dural
import random; random.seed(4)
for i in range(9):
    x = 0.0705+0.0011*i+random.uniform(-0.0003, 0.0003); y = random.uniform(-0.0004, 0.006)
    cu = bpy.data.curves.new("r", "CURVE"); cu.dimensions = '3D'; spn = cu.splines.new('NURBS'); pts = [(x+0.0004*math.sin(z*60+i), y, z) for z in [Z0+k*0.022 for k in range(17)]]
    spn.points.add(len(pts)-1)
    for p, q in zip(spn.points, pts): p.co = (*q, 1)
    spn.use_endpoint_u = True; spn.order_u = 4; cu.bevel_depth = 0.00042+0.00012*random.random(); cu.bevel_resolution = 3
    o = bpy.data.objects.new("raiz", cu); bpy.context.collection.objects.link(o); cu.materials.append(ROOT)
# --- aguja: entra en L4-L5, 12° en sentido craneal
ANG = math.radians(12); ZE = -0.026; DIR = Vector((math.cos(ANG), 0, math.sin(ANG)))
nd = bpy.data.objects.new("aguja", None); bpy.context.collection.objects.link(nd)
bpy.ops.mesh.primitive_cylinder_add(radius=0.0007, depth=0.25, location=(-0.125, 0, 0), rotation=(0, math.pi/2, 0), vertices=20); o = bpy.context.object; o.data.materials.append(STEEL); o.parent = nd
bpy.ops.mesh.primitive_cone_add(radius1=0.0007, radius2=0.0, depth=0.0035, location=(0.0014, 0, 0), rotation=(0, math.pi/2, 0), vertices=20); o = bpy.context.object; o.data.materials.append(STEEL); o.parent = nd
nd.rotation_euler = (0, -ANG, 0)
def place(xt):                       # xt: profundidad de la punta
    p = Vector((0, -0.0010, ZE))+DIR*(xt/math.cos(ANG)); nd.location = p
# --- luz y cámara
wo = bpy.data.worlds.new("w"); sc.world = wo; wo.use_nodes = True; wo.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
def area(loc, tgt, e, col, size):
    d = bpy.data.lights.new("a", "AREA"); d.energy = e; d.color = col; d.size = size; o = bpy.data.objects.new("a", d); o.location = loc; bpy.context.collection.objects.link(o)
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = (Vector(tgt)-Vector(loc)).to_track_quat('-Z', 'Y')
area((-0.05, -0.25, 0.18), (0.045, 0, 0), 1.1, (1.0, 0.80, 0.60), 0.30)
area((0.20, -0.20, -0.10), (0.045, 0, 0), 0.35, (0.85, 0.90, 1.0), 0.25)
cam = bpy.data.cameras.new("c"); co = bpy.data.objects.new("c", cam); bpy.context.collection.objects.link(co); sc.camera = co
cam.dof.use_dof = True; cam.dof.aperture_fstop = 5.6
def aim(pos, tgt, lens):
    pos = Vector(pos); tgt = Vector(tgt); f = (tgt-pos).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); u = r.cross(f)
    from mathutils import Matrix
    co.matrix_world = Matrix.Translation(pos)@Matrix((r, u, -f)).transposed().to_4x4(); cam.lens = lens; cam.dof.focus_distance = (tgt-pos).length
r = sc.render; r.resolution_x = int(A[0]); r.resolution_y = r.resolution_x*16//9
r.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = int(A[1]); sc.cycles.use_denoising = True; sc.cycles.use_adaptive_sampling = True
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; r.image_settings.file_format = 'JPEG'; r.image_settings.quality = 93
# avance: rápido por partes blandas, frena en el amarillo y en la duramadre («resalte») y entra en el LCR
NFR = int(A[4]) if len(A) > 4 else 72
KEY = [(0, -0.030), (8, 0.000), (16, 0.022), (26, 0.048), (34, 0.0535), (38, 0.0618), (44, 0.0640), (50, 0.0660), (54, 0.0676), (62, 0.0706), (71, 0.0712)]
KEY = [(f*(NFR-1)/71, x) for f, x in KEY]
def tip(f):
    for (f0, x0), (f1, x1) in zip(KEY, KEY[1:]):
        if f0 <= f <= f1: u = (f-f0)/(f1-f0); u = u*u*(3-2*u); return x0+(x1-x0)*u
    return KEY[-1][1]
for f in range(int(A[2]), int(A[3])):
    xt = tip(f); place(xt); k = f/(NFR-1); k = k*k*(3-2*k)
    tgt = Vector((0.040+0.012*k, 0, -0.012+0.004*k)); pos = tgt+Vector((0.010, -0.30+0.10*k, 0.030-0.010*k))
    aim(pos, tgt, 50)
    r.filepath = f"{OUT}/{f:03d}.jpg"; bpy.ops.render.render(write_still=True); print("corte", f, flush=True)
