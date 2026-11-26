"""Epistaxis v3 (26/11/2026): bodegón del material sobre paño azul y planos de producto animados.
Sin paciente: material modelado (esponja expansible con cordón, gelatina reabsorbible, celulosa oxidada, balón con
manguito piloto, jeringa de 10 ml, varillas de nitrato de plata, pinza de bayoneta, espéculo nasal y algodones).
Uso: python3 material_epistaxis.py -- still RES SAMPLES plano...      (planos: mesa0 mesa1 esponja reabs balon nitrato)
     python3 material_epistaxis.py -- anim RES SAMPLES mesa|esponja|balon F0 F1   (NFR = fotogramas totales, 30 por defecto)"""
import bpy, sys, os, math
from mathutils import Vector, Matrix, Euler
A = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
OUT = os.environ.get("MATOUT", "/home/claude/v3d/epi3/mat"); os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
C = bpy.context.collection
def mat(n, c, r=0.5, **kw):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = r
    for k, v in kw.items(): b.inputs[k].default_value = v
    return m
def bump(m, scale, strength, detail=6.0, kind="noise", dist=0.4):
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    if kind == "noise":
        t = nt.nodes.new("ShaderNodeTexNoise"); t.inputs["Scale"].default_value = scale; t.inputs["Detail"].default_value = detail
    elif kind == "voronoi":
        t = nt.nodes.new("ShaderNodeTexVoronoi"); t.inputs["Scale"].default_value = scale
    else:
        t = nt.nodes.new("ShaderNodeTexWave"); t.inputs["Scale"].default_value = scale; t.inputs["Distortion"].default_value = 2
    tc = nt.nodes.new("ShaderNodeTexCoord"); nt.links.new(tc.outputs["Object"], t.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = strength; bp.inputs["Distance"].default_value = dist
    nt.links.new(t.outputs[0] if kind != "voronoi" else t.outputs["Distance"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m
STEEL = mat("acero", (0.78, 0.78, 0.80), 0.30, Metallic=1.0); bump(STEEL, 3000, 0.03, dist=0.0002)
DRAPE = bump(mat("pano", (0.010, 0.045, 0.085), 0.95, **{"Sheen Weight": 0.5}), 700, 0.35, kind="wave", dist=0.0006)
SPONGE = bump(mat("esponja", (0.90, 0.86, 0.76), 0.95), 2400, 0.7, kind="voronoi", dist=0.0004)
WET = bump(mat("esponja_humeda", (0.84, 0.77, 0.66), 0.5, **{"Subsurface Weight": 0.2}), 1500, 0.8, kind="voronoi", dist=0.0007)
GELA = bump(mat("gelatina", (0.93, 0.90, 0.80), 0.97, **{"Subsurface Weight": 0.15}), 1600, 0.9, kind="voronoi", dist=0.0006)
CELL = bump(mat("celulosa", (0.94, 0.91, 0.78), 0.85, **{"Sheen Weight": 0.8, "Subsurface Weight": 0.2}), 900, 0.6, kind="wave", dist=0.0004)
CORD = mat("cordon", (0.05, 0.20, 0.65), 0.6)
SLEEVE = bump(mat("funda_balon", (0.10, 0.30, 0.55), 0.8, **{"Sheen Weight": 0.5}), 1800, 0.4, kind="wave", dist=0.0003)
PILOT = mat("piloto", (0.9, 0.9, 0.92), 0.25, **{"Transmission Weight": 0.6})
CLEAR = mat("plastico", (0.95, 0.97, 1.0), 0.05, **{"Transmission Weight": 1.0, "IOR": 1.49})
PLUNG = mat("embolo", (0.95, 0.95, 0.95), 0.4)
RUB = mat("goma", (0.05, 0.05, 0.05), 0.6)
WOOD = bump(mat("madera", (0.78, 0.62, 0.42), 0.7), 900, 0.2, kind="wave", dist=0.0002)
AGNO = mat("nitrato", (0.20, 0.20, 0.21), 0.5)
COT = bump(mat("algodon", (0.96, 0.95, 0.92), 0.9, **{"Subsurface Weight": 0.3, "Sheen Weight": 0.8}), 900, 0.6, dist=0.0005)
WATER = mat("suero", (0.9, 0.95, 1.0), 0.02, **{"Transmission Weight": 1.0, "IOR": 1.33})
LAB = mat("rotulo", (0.98, 0.98, 0.98), 0.5)
def obj_from(fn, *a, m=None, smooth=True, **k):
    fn(*a, **k); o = bpy.context.object
    if m: o.data.materials.append(m)
    if smooth: bpy.ops.object.shade_smooth()
    return o
def fix(o):
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); return o
def bevel(o, w, seg=3):
    b = o.modifiers.new("b", "BEVEL"); b.width = w; b.segments = seg; b.limit_method = 'NONE'; return o
def tube(pts, r, m, res=3):
    cu = bpy.data.curves.new("t", "CURVE"); cu.dimensions = '3D'; sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts)-1)
    for bp, p in zip(sp.bezier_points, pts): bp.co = p; bp.handle_left_type = bp.handle_right_type = 'AUTO'
    cu.bevel_depth = r; cu.bevel_resolution = res; o = bpy.data.objects.new("t", cu); C.objects.link(o); cu.materials.append(m); return o
# --- paño y bandeja
drape = obj_from(bpy.ops.mesh.primitive_plane_add, size=1.2, m=DRAPE, smooth=False)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.subdivide(number_cuts=60); bpy.ops.object.mode_set(mode='OBJECT')
tx = bpy.data.textures.new("arruga", 'CLOUDS'); tx.noise_scale = 0.25; d = drape.modifiers.new("d", 'DISPLACE'); d.texture = tx; d.strength = 0.012; bpy.ops.object.shade_smooth()
tray = obj_from(bpy.ops.mesh.primitive_cube_add, size=1, m=STEEL, smooth=False); tray.scale = (0.30, 0.20, 0.006); tray.location = (0, 0, 0.003)
bevel(tray, 0.004, 4)
# --- esponja expansible (local: eje largo X, grosor Z) con cordón
def esponja(loc, rot=0.0):
    o = obj_from(bpy.ops.mesh.primitive_cube_add, size=1, m=SPONGE, smooth=False); o.scale = (0.080, 0.015, 0.0025); fix(o); o.location = loc; o.rotation_euler.z = rot
    bevel(o, 0.0012, 3)
    tip = Vector(loc)+Matrix.Rotation(rot, 3, 'Z')@Vector((-0.040, 0, 0))
    cord = tube([tip, tip+Matrix.Rotation(rot, 3, 'Z')@Vector((-0.03, 0.012, 0)), tip+Matrix.Rotation(rot, 3, 'Z')@Vector((-0.07, -0.01, 0))], 0.0007, CORD)
    return o, cord
# --- gelatina reabsorbible: bloque y tira cortada
def gelatina(loc, rot=0.0):
    o = obj_from(bpy.ops.mesh.primitive_cube_add, size=1, m=GELA, smooth=False); o.scale = (0.070, 0.050, 0.010); fix(o); o.location = loc; o.rotation_euler.z = rot; bevel(o, 0.0015, 2)
    t = obj_from(bpy.ops.mesh.primitive_cube_add, size=1, m=GELA, smooth=False); t.scale = (0.060, 0.012, 0.008); fix(t)
    t.location = Vector(loc)+Matrix.Rotation(rot, 3, 'Z')@Vector((0.0, -0.045, -0.001)); t.rotation_euler.z = rot+0.12; bevel(t, 0.0012, 2)
    return o, t
# --- celulosa oxidada: lámina de malla ondulada
def celulosa(loc, rot=0.0):
    o = obj_from(bpy.ops.mesh.primitive_plane_add, size=1, m=CELL, smooth=False); o.scale = (0.075, 0.050, 1); fix(o); o.location = loc; o.rotation_euler.z = rot
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.subdivide(number_cuts=30); bpy.ops.object.mode_set(mode='OBJECT')
    w = o.modifiers.new("w", 'WAVE'); w.height = 0.0012; w.width = 0.03; w.narrowness = 1.2; w.use_normal = False
    s = o.modifiers.new("s", 'SOLIDIFY'); s.thickness = 0.0008; bpy.ops.object.shade_smooth(); return o
# --- balón anterior: cuerpo fusiforme con funda, manguito piloto y válvula
def balon(loc, rot=0.0, infl=0.0):
    g = bpy.data.objects.new("balon", None); C.objects.link(g); g.location = loc; g.rotation_euler.z = rot
    body = obj_from(bpy.ops.mesh.primitive_uv_sphere_add, radius=1, segments=48, ring_count=24, m=SLEEVE)
    body.scale = (0.030, 0.0055, 0.0050); fix(body); body.parent = g; body.location = (0, 0, 0.0055)
    stem = tube([Vector((-0.028, 0, 0.006)), Vector((-0.06, 0.004, 0.004)), Vector((-0.10, 0.018, 0.003)), Vector((-0.14, 0.030, 0.003))], 0.0014, PILOT); stem.parent = g
    cuff = obj_from(bpy.ops.mesh.primitive_uv_sphere_add, radius=1, segments=32, ring_count=16, m=PILOT); cuff.scale = (0.008, 0.0035, 0.0035); fix(cuff)
    cuff.parent = g; cuff.location = (-0.15, 0.033, 0.004+0.003*infl)
    valve = obj_from(bpy.ops.mesh.primitive_cylinder_add, radius=0.0035, depth=0.012, vertices=24, m=CORD); valve.parent = g; valve.location = (-0.164, 0.036, 0.004); valve.rotation_euler = (0, math.pi/2, 0.2)
    return g, body, cuff
# --- jeringa de 10 ml (eje X, punta hacia -X); emb: recorrido del émbolo (0 = vacía, 1 = cargada)
def jeringa(loc, rot=(0, 0, 0), emb=1.0, liquid=True):
    g = bpy.data.objects.new("jeringa", None); C.objects.link(g); g.location = loc; g.rotation_euler = rot
    barrel = obj_from(bpy.ops.mesh.primitive_cylinder_add, radius=0.0078, depth=0.075, vertices=48, m=CLEAR); barrel.rotation_euler = (0, math.pi/2, 0); barrel.parent = g
    s = barrel.modifiers.new("s", 'SOLIDIFY'); s.thickness = 0.0008
    nose = obj_from(bpy.ops.mesh.primitive_cone_add, radius1=0.0030, radius2=0.0016, depth=0.010, vertices=24, m=CLEAR); nose.rotation_euler = (0, -math.pi/2, 0); nose.location = (-0.0425, 0, 0); nose.parent = g
    fl = obj_from(bpy.ops.mesh.primitive_cube_add, size=1, m=CLEAR, smooth=False); fl.scale = (0.002, 0.030, 0.012); fl.location = (0.0375, 0, 0); fl.parent = g; bevel(fl, 0.0008)
    px = -0.030+0.060*emb
    stop = obj_from(bpy.ops.mesh.primitive_cylinder_add, radius=0.0072, depth=0.005, vertices=40, m=RUB); stop.rotation_euler = (0, math.pi/2, 0); stop.location = (px, 0, 0); stop.parent = g
    rod = obj_from(bpy.ops.mesh.primitive_cube_add, size=1, m=PLUNG, smooth=False); rod.scale = (0.075, 0.0012, 0.010); rod.location = (px+0.040, 0, 0); rod.parent = g
    rod2 = rod.copy(); rod2.data = rod.data; C.objects.link(rod2); rod2.rotation_euler = (math.pi/2, 0, 0); rod2.parent = g; rod2.location = rod.location
    thumb = obj_from(bpy.ops.mesh.primitive_cylinder_add, radius=0.010, depth=0.002, vertices=40, m=PLUNG); thumb.rotation_euler = (0, math.pi/2, 0); thumb.location = (px+0.078, 0, 0); thumb.parent = g
    if liquid and emb > 0.02:
        lq = obj_from(bpy.ops.mesh.primitive_cylinder_add, radius=0.0069, depth=0.060*emb, vertices=40, m=WATER); lq.rotation_euler = (0, math.pi/2, 0)
        lq.location = (-0.0335+0.030*emb, 0, 0); lq.parent = g
    for i in range(11):                                              # marcas de graduación
        mk = obj_from(bpy.ops.mesh.primitive_cube_add, size=1, m=RUB, smooth=False); mk.scale = (0.0003, 0.0001, 0.003 if i % 5 else 0.005)
        mk.location = (-0.033+0.006*i, -0.0079, 0.002); mk.parent = g
    PARTS[g.name] = (stop, rod, rod2, thumb)
    return g
PARTS = {}
def embolo(g, emb):
    stop, rod, rod2, thumb = PARTS[g.name]; px = -0.030+0.060*emb
    stop.location.x = px; rod.location.x = rod2.location.x = px+0.040; thumb.location.x = px+0.078
def nitrato(loc, rot):
    o = tube([Vector((0, 0, 0)), Vector((0.075, 0, 0)), Vector((0.15, 0, 0))], 0.0011, WOOD); o.location = loc; o.rotation_euler.z = rot
    t = obj_from(bpy.ops.mesh.primitive_uv_sphere_add, radius=1, segments=24, ring_count=12, m=AGNO); t.scale = (0.0045, 0.0019, 0.0019); t.parent = o; t.location = (-0.002, 0, 0)
    return o
def bayoneta(loc, rot):
    g = bpy.data.objects.new("bayoneta", None); C.objects.link(g); g.location = loc; g.rotation_euler.z = rot
    for dy in (0.0018, -0.0018):
        o = tube([Vector((0, dy, 0.0012)), Vector((0.05, dy*1.4, 0.0012)), Vector((0.058, dy*1.6, 0.0012)), Vector((0.066, dy*2.2+0.008, 0.0012)), Vector((0.12, dy*3.5+0.008, 0.0012)), Vector((0.175, dy*0.4+0.008, 0.0012))], 0.0011, STEEL)
        o.parent = g
    return g
def especulo(loc, rot):
    g = bpy.data.objects.new("especulo", None); C.objects.link(g); g.location = loc; g.rotation_euler.z = rot
    for s in (1, -1):
        bl = obj_from(bpy.ops.mesh.primitive_uv_sphere_add, radius=1, segments=32, ring_count=16, m=STEEL); bl.scale = (0.018, 0.0035, 0.0012)
        bl.parent = g; bl.location = (-0.012, s*0.0045, 0.0013); bl.rotation_euler.z = s*0.08
        h = tube([Vector((0.004, s*0.004, 0.0015)), Vector((0.03, s*0.010, 0.0015)), Vector((0.07, s*0.016, 0.0015)), Vector((0.085, s*0.004, 0.0015))], 0.0016, STEEL); h.parent = g
    return g
def algodon(loc, k=1.0):
    o = obj_from(bpy.ops.mesh.primitive_ico_sphere_add, radius=0.011*k, subdivisions=4, m=COT); o.location = loc; o.scale = (1.2, 1.0, 0.75)
    tx = bpy.data.textures.new("fib", 'CLOUDS'); tx.noise_scale = 0.004; d = o.modifiers.new("d", 'DISPLACE'); d.texture = tx; d.strength = 0.004; return o
# --- disposición en la bandeja (z = 0.024 sobre el fondo de la bandeja)
Z = 0.006
SP, SPC = esponja((-0.07, 0.07, Z+0.00125), 0.15)
G1, G2 = gelatina((0.075, 0.055, Z+0.005), -0.25)
CE = celulosa((0.10, -0.035, Z+0.0012), 0.3)
BG, BB, BC = balon((-0.03, -0.055, Z), -0.35)
SY = jeringa((0.06, -0.085, Z+0.008), (0, 0, 0.12), emb=0.0, liquid=False)
NI = [nitrato((-0.13+0.006*i, 0.006*i-0.01, Z+0.0012), -0.05+0.03*i) for i in range(3)]
BY = bayoneta((-0.05, 0.025, Z), 0.05)
ES = especulo((0.02, 0.11, Z), 2.9)
for p in ((0.13, 0.035, Z+0.007), (0.15, 0.02, Z+0.007), (0.145, 0.045, Z+0.007)): algodon(p)
# --- luz y mundo
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0.004, 0.005, 0.007, 1)
def area(loc, tgt, e, col, sx, sy=None):
    d = bpy.data.lights.new("a", "AREA"); d.energy = e; d.color = col; d.shape = 'RECTANGLE'; d.size = sx; d.size_y = sy or sx
    o = bpy.data.objects.new("a", d); o.location = loc; C.objects.link(o)
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = (Vector(tgt)-Vector(loc)).to_track_quat('-Z', 'Y'); return o
area((0.5, -0.45, 0.7), (0, 0, 0), 14, (1.0, 0.90, 0.78), 0.5, 0.35)
area((-0.6, 0.5, 0.35), (0, 0, 0), 9, (0.80, 0.90, 1.0), 0.4, 0.2)
area((0.0, 0.0, 1.0), (0, 0, 0), 2.5, (1, 1, 1), 0.8)
# --- cámara
cam = bpy.data.cameras.new("c"); co = bpy.data.objects.new("c", cam); C.objects.link(co); sc.camera = co
def aim(pos, tgt, lens, focus=None, f=2.8):
    pos = Vector(pos); tgt = Vector(tgt); fw = (tgt-pos).normalized(); r = fw.cross(Vector((0, 0, 1))).normalized(); u = r.cross(fw)
    co.matrix_world = Matrix.Translation(pos)@Matrix((r, u, -fw)).transposed().to_4x4(); cam.lens = lens
    cam.dof.use_dof = focus is not None
    if focus is not None: cam.dof.focus_distance = (Vector(focus)-pos).length; cam.dof.aperture_fstop = f
r = sc.render; r.resolution_x = int(A[1]) if len(A) > 1 else 360; r.resolution_y = r.resolution_x*16//9
r.engine = 'CYCLES'; sc.cycles.samples = int(A[2]) if len(A) > 2 else 16; sc.cycles.use_denoising = True
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.03; sc.cycles.max_bounces = 8; sc.cycles.transmission_bounces = 8
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; r.image_settings.file_format = 'JPEG'; r.image_settings.quality = 93
def save(p): r.filepath = p; bpy.ops.render.render(write_still=True)
ease = lambda x: x*x*(3-2*x)
SPC_ = SP.location.copy(); BGC = BG.location.copy()
def orb(t, d, el, az, lens, fs=5.6, foc=None):
    t = Vector(t); el, az = math.radians(el), math.radians(az)
    p = t+Vector((math.cos(el)*math.sin(az), -math.cos(el)*math.cos(az), math.sin(el)))*d
    return (p, t, lens, foc if foc is not None else t, fs)
GC = (G1.location+CE.location)/2
SHOTS = {"mesa0": orb((0.0, 0.02, 0.0), 0.55, 52, -10, 40, 8.0),
         "mesa1": orb((-0.01, 0.01, 0.0), 0.36, 40, 12, 42, 6.3),
         "esponja": orb(SPC_+Vector((0.005, 0, 0.004)), 0.21, 38, 8, 50, 6.3),
         "reabs": orb(GC, 0.40, 50, -15, 50, 7.0),
         "balon": orb(BGC+Matrix.Rotation(-0.35, 3, "Z")@Vector((-0.085, 0.02, 0.004)), 0.40, 48, -8, 35, 8.0),
         "nitrato": orb((-0.128, -0.006, Z), 0.15, 38, -20, 50, 4.5)}
def shot(n): p, t, l, f, fs = SHOTS[n]; aim(p, t, l, f, fs)
def set_sponge(k):
    """k: 0 = comprimida, 1 = expandida e hidratada"""
    SP.scale = (1+0.075*k, 1+0.4*k, 1+4.2*k); SP.location.z = Z+0.00125+0.00525*k
    SP.data.materials[0] = WET if k > 0.35 else SPONGE
DROPS = []
def drops(u, src):
    for o in DROPS: bpy.data.objects.remove(o)
    DROPS.clear()
    for i in range(6):
        ph = (u*3.0-i*0.17)
        if 0 < ph < 1:
            o = obj_from(bpy.ops.mesh.primitive_uv_sphere_add, radius=0.0018, segments=16, ring_count=8, m=WATER); o.scale = (1, 1, 1.4)
            o.location = Vector(src)+Vector((0.006*math.sin(i), 0, -0.045*ph*ph)); DROPS.append(o)
if A and A[0] == "still":
    for n in A[3:]:
        if n == "esponja": set_sponge(0)
        shot(n); save(f"{OUT}/s_{n}.jpg"); print(n, flush=True)
if A and A[0] == "anim":
    kind, a0, a1 = A[3], int(A[4]), int(A[5]); N = int(os.environ.get("NFR", "30")); od = f"{OUT}/f_{kind}"; os.makedirs(od, exist_ok=True)
    if kind == "esponja":
        syr = jeringa(SPC_+Vector((0.030, 0.0, 0.075)), (0, 0.55, math.pi), emb=1.0)
    if kind == "balon":
        bpy.data.objects.remove(SY, do_unlink=True)
        BG.location = (0.10, -0.30, 0.010); BG.rotation_euler.z = 1.75
        T_ = Vector((0.10, -0.30, 0.010))+Matrix.Rotation(1.75, 3, "Z")@Vector((-0.13, 0.02, 0.0)); SHOTS["balon"] = orb(T_, 0.36, 58, -10, 35, 8.0)
    for fr in range(a0, a1):
        u = fr/(N-1)
        if kind == "mesa":
            (p0, t0, l0, f0, s0), (p1, t1, l1, f1, s1) = SHOTS["mesa0"], SHOTS["mesa1"]; k = ease(u)
            aim(Vector(p0).lerp(Vector(p1), k), Vector(t0).lerp(Vector(t1), k), l0+(l1-l0)*k, Vector(f0).lerp(Vector(f1), k), 5.6)
        elif kind == "esponja":
            k = ease(max(0, min(1, (u-0.25)/0.6))); set_sponge(k); drops(u, SPC_+Vector((0.000, 0.0, 0.050))); shot("esponja")
        elif kind == "balon":
            k = ease(max(0, min(1, (u-0.2)/0.65)))
            BB.scale = (1+0.13*k, 1+1.2*k, 1+1.3*k); BB.location.z = 0.0055+0.0065*k
            BC.scale = (1, 1+0.9*k, 1+0.9*k)
            if fr == a0:
                bpy.context.view_layer.update(); vp = BG.matrix_world@Vector((-0.17, 0.037, 0.004)); rz = BG.rotation_euler.z; globals()["SYB"] = jeringa(vp+Matrix.Rotation(rz, 3, "Z")@Vector((-0.050, 0.0, 0.0)), (0, 0, rz+math.pi), emb=1.0, liquid=False)
            embolo(globals()["SYB"], 1-k)
            shot("balon")
        save(f"{od}/{fr:03d}.jpg"); print(kind, fr, flush=True)
