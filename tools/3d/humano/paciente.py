"""Paciente de alta calidad para los vídeos de técnica (epistaxis v2, 25/11/2026).
Malla CC0 de MakeHuman (varón de unos 50 años), UV de la malla base con máscaras de piel de MPFB2 (labios, párpados,
orejas, uñas), ojos high-poly con iris texturizado, cejas y pelo corto como hebras de Blender, barba incipiente en el
sombreador y ropa (camiseta y pantalón) como funda de tela ajustada sobre el cuerpo.
Uso (dentro de bpy): import paciente; P = paciente.crear(pose)  -> dict con objetos y puntos de referencia."""
import bpy, json, math, os
import numpy as np
from mathutils import Vector, Matrix
import humano
D = humano.D
MPFB = "/home/claude/mpfb2/src/mpfb/data/textures/"
# varón de unos 50 años (edad de MakeHuman: 25 = young, 90 = old; 50 años ≈ 0,38 de «old»), complexión media
EDAD = 0.38
TARGETS = [("caucasian-male-young.target", 1-EDAD), ("caucasian-male-old.target", EDAD),
           ("universal-male-young-averagemuscle-averageweight.target", (1-EDAD)*0.7),
           ("universal-male-young-averagemuscle-maxweight.target", (1-EDAD)*0.3),
           ("universal-male-old-averagemuscle-averageweight.target", EDAD*0.7),
           ("universal-male-old-averagemuscle-maxweight.target", EDAD*0.3)]

def _bsdf(m): return m.node_tree.nodes["Principled BSDF"]
def mat(n, c, r=0.5, **kw):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = _bsdf(m)
    b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = r
    for k, v in kw.items(): b.inputs[k].default_value = v
    return m
def _uv_body():
    """vt de la malla base y, por cada cara del grupo body (mismo orden que humano.load_obj), sus índices de UV"""
    VT = []; FT = []; grp = None
    for l in open(D+"3dobjs/base.obj"):
        if l.startswith("vt "): VT.append(tuple(map(float, l.split()[1:3])))
        elif l.startswith("g "): grp = l.split()[1]
        elif l.startswith("f ") and grp == "body": FT.append([int(t.split("/")[1])-1 for t in l.split()[1:]])
    return VT, FT
def _img(nt, path, cs="Non-Color"):
    n = nt.nodes.new("ShaderNodeTexImage"); n.image = bpy.data.images.load(path); n.image.colorspace_settings.name = cs; return n
def skin_material():
    m = mat("piel_hq", (0.66, 0.44, 0.33), 0.45); nt = m.node_tree; N = nt.nodes; L = nt.links; b = _bsdf(m)
    uv = N.new("ShaderNodeUVMap"); tc = N.new("ShaderNodeTexCoord")
    def noise(scale, detail=3.0, coord="Object"):
        t = N.new("ShaderNodeTexNoise"); t.inputs["Scale"].default_value = scale; t.inputs["Detail"].default_value = detail
        L.new(tc.outputs[coord], t.inputs["Vector"]); return t
    def mix(a, bcol, fac, mode='MIX'):
        x = N.new("ShaderNodeMix"); x.data_type = 'RGBA'; x.blend_type = mode
        if isinstance(fac, float): x.inputs["Factor"].default_value = fac
        else: L.new(fac, x.inputs["Factor"])
        if isinstance(a, tuple): x.inputs["A"].default_value = (*a, 1)
        else: L.new(a, x.inputs["A"])
        if isinstance(bcol, tuple): x.inputs["B"].default_value = (*bcol, 1)
        else: L.new(bcol, x.inputs["B"])
        return x.outputs["Result"]
    def mask(name, k=1.0):
        im = _img(nt, MPFB+f"mpfb_{name}.jpg"); L.new(uv.outputs["UV"], im.inputs["Vector"])
        if k == 1.0: return im.outputs["Color"]
        mm = N.new("ShaderNodeMath"); mm.operation = 'MULTIPLY'; mm.inputs[1].default_value = k; L.new(im.outputs["Color"], mm.inputs[0]); return mm.outputs["Value"]
    # tono base con manchas suaves
    n1 = noise(16, 5); r1 = N.new("ShaderNodeValToRGB"); e = r1.color_ramp.elements
    e[0].position, e[0].color = 0.32, (0.48, 0.29, 0.20, 1); e[1].position, e[1].color = 0.70, (0.63, 0.41, 0.29, 1)
    L.new(n1.outputs["Fac"], r1.inputs["Fac"]); col = r1.outputs["Color"]
    col = mix(col, (0.70, 0.36, 0.28), mask("face", 0.20))          # rubor de cara (nariz, mejillas)
    col = mix(col, (0.62, 0.30, 0.28), mask("ears", 0.45))          # orejas más rojizas
    col = mix(col, (0.46, 0.28, 0.23), mask("eyelids", 0.55))       # párpados algo más oscuros
    col = mix(col, (0.58, 0.27, 0.24), mask("lips", 0.85))          # labios
    col = mix(col, (0.86, 0.70, 0.64), mask("fingernails", 1.0))    # uñas
    col = mix(col, (0.86, 0.70, 0.64), mask("toenails", 1.0))
    # barba incipiente: atributo «barba» (0-1) por los puntitos del vello
    at = N.new("ShaderNodeAttribute"); at.attribute_name = "barba"
    dots = N.new("ShaderNodeTexVoronoi"); dots.inputs["Scale"].default_value = 2600; L.new(tc.outputs["Object"], dots.inputs["Vector"])
    dr = N.new("ShaderNodeMapRange"); dr.inputs["From Min"].default_value = 0.0; dr.inputs["From Max"].default_value = 0.35
    dr.inputs["To Min"].default_value = 1.0; dr.inputs["To Max"].default_value = 0.0; L.new(dots.outputs["Distance"], dr.inputs["Value"])
    bm = N.new("ShaderNodeMath"); bm.operation = 'MULTIPLY'; L.new(at.outputs["Fac"], bm.inputs[0]); L.new(dr.outputs["Result"], bm.inputs[1])
    bm2 = N.new("ShaderNodeMath"); bm2.operation = 'MULTIPLY'; bm2.inputs[1].default_value = 0.75; L.new(bm.outputs["Value"], bm2.inputs[0])
    sh = N.new("ShaderNodeMath"); sh.operation = 'MULTIPLY'; sh.inputs[1].default_value = 0.22; L.new(at.outputs["Fac"], sh.inputs[0])
    col = mix(col, (0.42, 0.30, 0.25), sh.outputs["Value"])            # sombra azulada-grisácea de la barba rasurada
    col = mix(col, (0.10, 0.08, 0.07), bm2.outputs["Value"])          # puntos de vello
    for an, c_, k_ in (("cuero", (0.075, 0.055, 0.045), 0.80), ("ceja", (0.045, 0.034, 0.027), 0.85)):   # piel bajo el pelo corto y las cejas
        a2 = N.new("ShaderNodeAttribute"); a2.attribute_name = an; m2 = N.new("ShaderNodeMath"); m2.operation = 'MULTIPLY'; m2.inputs[1].default_value = k_
        L.new(a2.outputs["Fac"], m2.inputs[0]); col = mix(col, c_, m2.outputs["Value"])
    L.new(col, b.inputs["Base Color"])
    b.inputs["Subsurface Weight"].default_value = 0.32; b.inputs["Subsurface Radius"].default_value = (1.0, 0.36, 0.17)
    b.inputs["Subsurface Scale"].default_value = 0.005; b.inputs["Specular IOR Level"].default_value = 0.45
    b.inputs["Sheen Weight"].default_value = 0.10; b.inputs["Sheen Roughness"].default_value = 0.45
    # rugosidad: labios y zona T más brillantes
    n3 = noise(30, 2); mr = N.new("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = 0.40; mr.inputs["To Max"].default_value = 0.56
    L.new(n3.outputs["Fac"], mr.inputs["Value"])
    lipr = N.new("ShaderNodeMix"); lipr.data_type = 'FLOAT'; L.new(mask("lips"), lipr.inputs["Factor"]); L.new(mr.outputs["Result"], lipr.inputs["A"]); lipr.inputs["B"].default_value = 0.28
    L.new(lipr.outputs["Result"], b.inputs["Roughness"])
    # poros y microrrelieve
    vo = N.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 1100; L.new(tc.outputs["Object"], vo.inputs["Vector"])
    n4 = noise(1800, 1); ad = N.new("ShaderNodeMath"); ad.operation = 'ADD'; L.new(vo.outputs["Distance"], ad.inputs[0]); L.new(n4.outputs["Fac"], ad.inputs[1])
    bp = N.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.12; bp.inputs["Distance"].default_value = 0.0003
    L.new(ad.outputs["Value"], bp.inputs["Height"]); L.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m
def _set(n, k, v):
    if k in n.inputs: n.inputs[k].default_value = v
def hair_material(name, melanin=0.85, grey=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; N = nt.nodes
    out = N["Material Output"]; N.remove(N["Principled BSDF"])
    h = N.new("ShaderNodeBsdfHairPrincipled"); h.parametrization = 'COLOR'
    # color directo: castaño oscuro (la luz del estudio es cálida y aclara mucho la melanina)
    dark = 0.010+0.030*(1-melanin)/0.2; _set(h, "Color", (dark*1.35, dark*0.95, dark*0.70, 1))
    pass
    _set(h, "Roughness", 0.35); _set(h, "Random Color", 0.15)
    if "Random Roughness" in h.inputs: _set(h, "Random Roughness", 0.2)
    if grey:
        tint = h.inputs.get("Tint")
        if tint: tint.default_value = (1, 1, 1, 1)
        g = grey*0.10; c = h.inputs["Color"].default_value; _set(h, "Color", (c[0]+g, c[1]+g, c[2]+g, 1))
        if "Random Color" in h.inputs: _set(h, "Random Color", 0.35)
    nt.links.new(h.outputs[0], out.inputs["Surface"]); return m
def _fit_proxy(mhclo, V_raw):
    """Ajusta un proxy .mhclo de MakeHuman a la malla base (coordenadas crudas de la obj) y devuelve verts y caras"""
    lines = open(mhclo).read().splitlines(); sc = {}; refs = []; objf = None; inv = False
    for l in lines:
        p = l.split()
        if not p or p[0].startswith("#"): continue
        if p[0] in ("x_scale", "y_scale", "z_scale"): sc[p[0][0]] = (int(p[1]), int(p[2]), float(p[3]))
        elif p[0] == "obj_file": objf = p[1]
        elif p[0] == "verts": inv = True; continue
        elif inv:
            if len(p) == 9: refs.append(([int(x) for x in p[:3]], [float(x) for x in p[3:6]], [float(x) for x in p[6:9]]))
            elif len(p) == 1: refs.append(([int(p[0])]*3, [1.0, 0, 0], [0, 0, 0]))
            else: inv = False
    s = {k: abs(V_raw[a][i]-V_raw[b][i])/d for i, k in enumerate("xyz") for (a, b, d) in [sc[k]]}
    P = np.array([sum(w*V_raw[v] for v, w in zip(vs, ws))+np.array([o[0]*s["x"], o[1]*s["y"], o[2]*s["z"]]) for vs, ws, o in refs])
    VTp = []; Fp = []; FTp = []
    for l in open(os.path.join(os.path.dirname(mhclo), objf)):
        if l.startswith("vt "): VTp.append(tuple(map(float, l.split()[1:3])))
        elif l.startswith("f "):
            t = [x.split("/") for x in l.split()[1:]]; Fp.append([int(x[0])-1 for x in t]); FTp.append([int(x[1])-1 for x in t])
    P = np.stack([P[:, 0], -P[:, 2], P[:, 1]], 1)*0.1
    return P, Fp, VTp, FTp
def _raw_from(V): return np.stack([V[:, 0], V[:, 2], -V[:, 1]], 1)/0.1
def crear(pose, name="paciente", ropa=True, pelo=True):
    humano.TARGETS = TARGETS; humano.BREAST = 0.0
    V, F = humano.load_obj(); used = sorted({i for f in F for i in f}); REST = V[used]
    # ojos high-poly ajustados a la malla y unidos al hueso de la cabeza
    P, Fp, VTp, FTp = _fit_proxy(D+"eyes/high-poly/high-poly.mhclo", _raw_from(V))
    me = bpy.data.meshes.new("ojos"); me.from_pydata([tuple(p) for p in P], [], Fp); me.update()
    uvl = me.uv_layers.new(name="UV")
    for poly, ft in zip(me.polygons, FTp):
        for li, ti in zip(poly.loop_indices, ft): uvl.data[li].uv = VTp[ti]
    eyes = bpy.data.objects.new("ojos", me); bpy.context.collection.objects.link(eyes)
    em = mat("ojo", (1, 1, 1), 0.08, **{"Coat Weight": 1.0, "Coat Roughness": 0.02}); nt = em.node_tree
    it = _img(nt, D+"eyes/materials/brown_eye.png", "sRGB"); uvn = nt.nodes.new("ShaderNodeUVMap")
    nt.links.new(uvn.outputs["UV"], it.inputs["Vector"]); nt.links.new(it.outputs["Color"], _bsdf(em).inputs["Base Color"])
    me.materials.append(em)
    for p in me.polygons: p.use_smooth = True
    ob, J = humano.build(pose, name=name, extras=[(eyes, "head")])
    me = ob.data
    # UV de la malla base
    VT, FT = _uv_body(); uvl = me.uv_layers.new(name="UV")
    for poly, ft in zip(me.polygons, FT):
        for li, ti in zip(poly.loop_indices, ft): uvl.data[li].uv = VT[ti]
    ob.data.materials.append(skin_material())
    # referencias en reposo
    sk = json.load(open(D+"rigs/default.mhskel")); JR = {k: V[v].mean(0) for k, v in sk["joints"].items()}
    def jr(n): return JR[sk["bones"][n]["head"]]
    eyeL, eyeR = jr("eye.L"), jr("eye.R"); eyec = (eyeL+eyeR)/2; headc = (jr("head")+jr("special03") if "special03" in sk["bones"] else jr("head"))
    # hueso dominante de cada vértice
    names = [g.name for g in ob.vertex_groups]; dom = []
    for v in me.vertices:
        best = max(v.groups, key=lambda g: g.weight, default=None); dom.append(names[best.group] if best else "")
    # barba incipiente: mitad inferior de la cara por delante, sin labios
    barba = me.attributes.new("barba", 'FLOAT', 'POINT')
    for i, p in enumerate(REST):
        dz = p[2]-eyec[2]; front = p[1] < eyec[1]+0.035
        f = 0.0
        if front and -0.125 < dz < -0.040 and abs(p[0]) < 0.075:
            f = min(1, (-0.040-dz)/0.015)*min(1, (dz+0.125)/0.02)
            if abs(p[0]) > 0.055 and dz > -0.07: f *= max(0, 1-(abs(p[0])-0.055)/0.02)   # mejillas: se desvanece
        if dom[i] in ("neck01", "neck02", "neck03") and p[1] < eyec[1]-0.01 and dz > -0.17: f = max(f, 0.6)
        barba.data[i].value = f
    out = {"ob": ob, "eyes": eyes, "J": J, "REST": REST, "dom": dom, "eyec": Vector(eyec)}
    if pelo: out.update(_pelo(ob, REST, eyeL, eyeR, dom))
    if ropa: out.update(_ropa(ob, dom, REST, jr("neck01")))
    return out
def _vgroup(ob, name, weights):
    g = ob.vertex_groups.new(name=name)
    for i, w in enumerate(weights):
        if w > 0.001: g.add([i], float(w), 'REPLACE')
    return g
def _hair_system(ob, name, group, count, length, children, mat_, align=(0, 0, 0), normal=1.0, rnd=0.1, radius=0.00006, clump=0.0, rough=0.0):
    md = ob.modifiers.new(name, 'PARTICLE_SYSTEM'); ps = md.particle_system; s = ps.settings; s.name = name
    s.type = 'HAIR'; s.use_advanced_hair = True; s.count = count; s.hair_length = length; s.emit_from = 'FACE'
    # en bpy sin interfaz la longitud del pelo la fija la velocidad de emisión (×4), no hair_length
    k = length/4.0; s.normal_factor = normal*k; s.object_align_factor = tuple(x*k/max(1e-9, length) for x in align) if any(align) else (0, 0, 0); s.factor_random = rnd*k
    s.child_type = 'INTERPOLATED' if children else 'NONE'; s.rendered_child_count = children; s.child_percent = max(1, children//4)
    s.clump_factor = clump; s.roughness_1 = rough; s.roughness_1_size = 0.2
    s.root_radius = 1.0; s.tip_radius = 0.0; s.radius_scale = radius; s.use_close_tip = True
    s.hair_step = 4; s.display_step = 3; s.render_step = 4
    ob.data.materials.append(mat_); s.material = len(ob.data.materials); s.material_slot = mat_.name
    ps.vertex_group_density = group.name; return md
def _pelo(ob, REST, eyeL, eyeR, dom):
    n = len(REST); eyec = (eyeL+eyeR)/2; hw = abs(eyeL[0]-eyeR[0])
    head = np.array([d in ("head",) or d.startswith(("temporalis", "special")) for d in dom])
    hc = REST[head].mean(0) if head.any() else eyec
    # cuero cabelludo: línea de implantación según el ángulo alrededor del eje vertical de la cabeza (pelo corto, algo de entradas)
    wscalp = np.zeros(n)
    for i, p in enumerate(REST):
        if not head[i] and dom[i] not in ("neck03",): continue
        th = math.degrees(math.atan2(p[0]-hc[0], -(p[1]-hc[1])))          # 0 = delante
        a = abs(th); dz = p[2]-eyec[2]
        line = np.interp(a, [0, 25, 45, 75, 100, 130, 180], [0.072, 0.068, 0.078, 0.032, 0.010, -0.050, -0.085])
        ear = abs(p[0]-hc[0]) > hw*1.05 and -0.035 < dz < 0.035 and 60 < a < 120
        if dz > line and not ear: wscalp[i] = min(1, (dz-line)/0.010)
    # cejas: arco sobre cada ojo, algo más alto en el centro
    wbrow = np.zeros(n)
    for e, sgn in ((eyeL, 1), (eyeR, -1)):
        for i, p in enumerate(REST):
            if p[1] > eyec[1]-0.01: continue
            u = (p[0]-e[0])*sgn                                            # >0 hacia fuera
            if not (-0.020 < u < 0.030): continue
            zc = e[2]+0.017+0.004*math.cos(math.pi*(u-0.004)/0.05)-0.006*max(0, u-0.018)/0.012
            th = 0.0055 if u < 0.018 else 0.0055*(1-(u-0.018)/0.014)
            d = abs(p[2]-zc)
            if d < th: wbrow[i] = max(wbrow[i], (1-d/th)*(0.5 if u < -0.015 else 1.0))
    gs = _vgroup(ob, "pelo_cuero", wscalp); gb = _vgroup(ob, "pelo_cejas", wbrow)
    for an, w in (("cuero", wscalp), ("ceja", wbrow)):
        at = ob.data.attributes.new(an, 'FLOAT', 'POINT')
        for i, x in enumerate(w): at.data[i].value = float(x)
    HM = hair_material("pelo", 0.93, grey=0.18); BM = hair_material("cejas", 0.95)
    scalp = _hair_system(ob, "pelo", gs, 12000, 0.010, 12, HM, normal=1.0, rnd=0.25, radius=0.00006, clump=0.1, rough=0.002)
    # cejas: dos sistemas para orientar el vello hacia fuera en cada lado
    brows = []
    for side, sx in (("L", 1), ("R", -1)):
        w = np.array([wbrow[i] if (REST[i][0]-eyec[0])*sx > 0 else 0 for i in range(n)])
        g = _vgroup(ob, "ceja_"+side, w)
        brows.append(_hair_system(ob, "ceja_"+side, g, 520, 0.0075, 5, BM, align=(0.0085*sx, 0, 0.0035), normal=0.30, rnd=0.15, radius=0.000032, clump=0.3))
    return {"hair_scalp": scalp, "hair_brows": brows}
def _ropa(ob, dom, REST_, NB):
    me = ob.data; ob.data.update()
    TOP = ("spine01", "spine02", "spine03", "spine04", "spine05", "clavicle.L", "clavicle.R", "shoulder01.L", "shoulder01.R",
           "breast.L", "breast.R", "upperarm01.L", "upperarm01.R")
    BOT = ("pelvis.L", "pelvis.R", "root", "upperleg01.L", "upperleg01.R", "upperleg02.L", "upperleg02.R", "lowerleg01.L", "lowerleg01.R", "lowerleg02.L", "lowerleg02.R")
    def shell(name, bones, off, col, extra=None, keep=None):
        sel = any if name == "camiseta" else all      # la camiseta se queda con las caras frontera (sin huecos en la cintura)
        faces = [p for p in me.polygons if (sel(dom[i] in bones for i in p.vertices) or (extra and extra(p))) and (keep is None or all(keep(i) for i in p.vertices))]
        vids = sorted({i for p in faces for i in p.vertices}); rm = {o: k for k, o in enumerate(vids)}
        nrm = {i: me.vertices[i].normal.copy() for i in vids}
        verts = [tuple(me.vertices[i].co+nrm[i]*off) for i in vids]
        m2 = bpy.data.meshes.new(name); m2.from_pydata(verts, [], [[rm[i] for i in p.vertices] for p in faces]); m2.update()
        o = bpy.data.objects.new(name, m2); bpy.context.collection.objects.link(o); o.matrix_world = ob.matrix_world.copy()
        for p in m2.polygons: p.use_smooth = True
        tx = bpy.data.textures.new(name+"_arrugas", 'CLOUDS'); tx.noise_scale = 0.06
        dsp = o.modifiers.new("arrugas", 'DISPLACE'); dsp.texture = tx; dsp.strength = 0.004; dsp.mid_level = 0.5
        sm = o.modifiers.new("suave", 'SMOOTH'); sm.factor = 0.5; sm.iterations = 4
        sd = o.modifiers.new("grosor", 'SOLIDIFY'); sd.thickness = 0.0018; sd.offset = 1.0
        ss = o.modifiers.new("sub", 'SUBSURF'); ss.levels = 1; ss.render_levels = 2
        m = mat(name, col, 0.82, **{"Sheen Weight": 0.4, "Sheen Roughness": 0.5}); nt = m.node_tree
        w = nt.nodes.new("ShaderNodeTexWave"); w.inputs["Scale"].default_value = 1400; tc = nt.nodes.new("ShaderNodeTexCoord")
        nt.links.new(tc.outputs["Object"], w.inputs["Vector"]); bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.15; bp.inputs["Distance"].default_value = 0.0002
        nt.links.new(w.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], _bsdf(m).inputs["Normal"])
        m2.materials.append(m); return o
    nb = NB
    def neck_ok(i):
        x, y, z = REST_[i]; front = max(0.0, -(y-nb[1])/0.07); lat = max(0.0, 1-(x/0.085)**2)
        return z < nb[2]-0.004-0.040*min(1, front)*lat
    top = shell("camiseta", TOP+("neck01",), 0.006, (0.05, 0.08, 0.13), keep=neck_ok)
    bot = shell("pantalon", BOT, 0.007, (0.035, 0.035, 0.04))
    # calzado: piel oscura sobre los pies
    shoe = mat("calzado", (0.02, 0.018, 0.016), 0.35); ob.data.materials.append(shoe); k = len(ob.data.materials)-1
    for p in me.polygons:
        if all(dom[i].startswith(("foot", "toe")) for i in p.vertices): p.material_index = k
    return {"top": top, "bot": bot}
