import bpy, math, sys, time
from mathutils import Vector, Matrix
A=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
def mat(name,col,rough=0.55,metal=0.0,emit=0.0):
    m=bpy.data.materials.new(name); m.use_nodes=True; b=m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value=(*col,1); b.inputs["Roughness"].default_value=rough; b.inputs["Metallic"].default_value=metal
    if emit: b.inputs["Emission Color"].default_value=(*col,1); b.inputs["Emission Strength"].default_value=emit
    return m
SKIN=mat("maniqui",(0.16,0.165,0.18),0.42)          # silueta grafito
BED=mat("camilla",(0.30,0.31,0.33),0.6)
SHEET=mat("sabana",(0.62,0.66,0.70),0.85)
YEL=mat("amarillo",(1.0,0.78,0.02),0.4,emit=0.8)
RED=mat("rojo",(0.90,0.03,0.04),0.4,emit=0.9)
STEEL=mat("acero",(0.92,0.92,0.95),0.12,1.0)
HUB=mat("cono",(1.0,0.80,0.05),0.3,emit=0.3)
def link(o,m): o.data.materials.clear(); o.data.materials.append(m); return o
def sm(): bpy.ops.object.shade_smooth()
def caps(p1,p2,r1,m,r2=None):
    r2=r2 or r1; p1=Vector(p1);p2=Vector(p2);d=p2-p1
    bpy.ops.mesh.primitive_cone_add(radius1=r1,radius2=r2,depth=d.length,location=(p1+p2)/2,vertices=40); c=bpy.context.object
    c.rotation_mode='QUATERNION'; c.rotation_quaternion=Vector((0,0,1)).rotation_difference(d); sm(); link(c,m)
    for p,r in ((p1,r1),(p2,r2)): bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=p,segments=40,ring_count=20); sm(); link(bpy.context.object,m)
def ell(p,r,m,s=(1,1,1),rot=(0,0,0)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=p,segments=48,ring_count=24,rotation=rot); o=bpy.context.object; o.scale=s; sm(); return link(o,m)
# ----- camilla: eje X longitudinal (cabeza en -X). Paciente en decúbito lateral izquierdo, espalda hacia -Y
bpy.ops.mesh.primitive_cube_add(location=(0,0.15,0.40)); o=bpy.context.object; o.scale=(1.10,0.45,0.05); link(o,BED)
bpy.ops.mesh.primitive_cube_add(location=(0,0.15,0.46)); o=bpy.context.object; o.scale=(1.08,0.44,0.012); link(o,SHEET)
bpy.ops.mesh.primitive_cylinder_add(radius=0.11,depth=0.30,location=(-0.80,0.15,0.54),rotation=(0,math.pi/2,0)); link(bpy.context.object,SHEET); sm()
Z=0.66
import bmesh
def skin_obj(name,chains,sz=1.0):
    me=bpy.data.meshes.new(name); ob=bpy.data.objects.new(name,me); bpy.context.collection.objects.link(ob)
    bm=bmesh.new(); rad=[]
    for ch in chains:
        vs=[]
        for (p,r) in ch:
            v=bm.verts.new(p); vs.append(v); rad.append(r)
        for v1,v2 in zip(vs,vs[1:]): bm.edges.new((v1,v2))
    bm.to_mesh(me); bm.free()
    mod=ob.modifiers.new("skin","SKIN"); mod.use_smooth_shade=True
    for sv,r in zip(me.skin_vertices[0].data,rad): sv.radius=(r,r)
    me.skin_vertices[0].data[0].use_root=True
    ss=ob.modifiers.new("sub","SUBSURF"); ss.levels=2; ss.render_levels=3
    me.materials.append(SKIN); return ob
# tronco (se escala en Z: de lado, hombro a hombro es más ancho que de delante a atrás)
T=skin_obj("tronco",[[((0.34,0.20,Z),0.105),((0.24,0.155,Z),0.115),((0.12,0.125,Z),0.10),((0.0,0.115,Z),0.10),((-0.14,0.13,Z),0.115),((-0.28,0.17,Z),0.12),((-0.38,0.215,Z),0.10)]])
T.scale=(1,1,1.32); T.location.z=Z*(1-1.32)
# hombros, caderas, cuello, extremidades
for dz in (0.16,-0.16):
    skin_obj("brazo",[[((-0.33,0.215,Z+dz*0.65),0.055),((-0.33,0.215,Z+dz),0.05),((-0.19,0.48,Z+dz*0.55),0.042),((0.00,0.62,Z+dz*0.25),0.034)]])
for dz in (0.095,-0.095):
    skin_obj("pierna",[[((0.27,0.20,Z+dz*0.4),0.10),((0.30,0.24,Z+dz),0.095),((-0.02,0.58,Z+dz),0.065),((0.29,0.75,Z+dz*0.9),0.042),((0.36,0.84,Z+dz*0.9),0.03)]])
skin_obj("cuello",[[((-0.38,0.22,Z),0.055),((-0.50,0.29,Z),0.05)]])
ell((-0.60,0.35,Z),1.0,SKIN,(0.105,0.095,0.09))   # cabeza lisa, sin cara
bpy.context.view_layer.update()
for o in list(bpy.data.objects):
    if any(m.type=="SKIN" for m in o.modifiers):
        bpy.context.view_layer.objects.active=o
        for o2 in bpy.context.selected_objects: o2.select_set(False)
        o.select_set(True)
        for m in list(o.modifiers): bpy.ops.object.modifier_apply(modifier=m.name)
bpy.context.view_layer.update()
dg=bpy.context.evaluated_depsgraph_get()
def skin_at(x,z=Z):
    hit,loc,nor,*_=sc.ray_cast(dg,Vector((x,-2,z)),Vector((0,1,0)))
    return loc,nor
# apófisis espinosas L1-L5 + sacro: pequeños relieves sobre la línea media
L={}
for i,x in enumerate([-0.15,-0.075,0.0,0.075,0.15]):  # L1..L5; L4 = 0.075
    loc,nor=skin_at(x); L[i+1]=(x,loc); ell(loc-nor*0.003,1.0,SKIN,(0.014,0.008,0.008))
# ----- anatomía de superficie: crestas ilíacas, escápulas y línea de Tuffier
import numpy as np
SKX=[-0.38,-0.28,-0.14,0.0,0.12,0.24,0.34]; SKY=[0.215,0.17,0.13,0.115,0.125,0.155,0.20]
yc=lambda x: float(np.interp(x,SKX,SKY))
from mathutils.bvhtree import BVHTree
_te=T.evaluated_get(dg); _me=_te.to_mesh()
BVH=BVHTree.FromPolygons([T.matrix_world@v.co for v in _me.vertices],[tuple(p.vertices) for p in _me.polygons])
def surf(x,th):
    """punto de la piel a la altura x, ángulo th (0 = línea media de la espalda, +90 = flanco de arriba, -90 = flanco de abajo)"""
    t=math.radians(th); d=Vector((0,-math.cos(t),math.sin(t)))
    c=Vector((x,yc(x),Z)); loc,nor,idx,dist=BVH.ray_cast(c+d*1.0,-d)
    return (loc,nor.normalized()) if loc else (None,None)
def ridge(pts,r,m):
    cu=bpy.data.curves.new("cresta","CURVE"); cu.dimensions='3D'; sp=cu.splines.new('NURBS'); sp.points.add(len(pts)-1)
    for p,q in zip(sp.points,pts): p.co=(*q,1)
    sp.use_endpoint_u=True; sp.order_u=4; cu.bevel_depth=r; cu.bevel_resolution=6; cu.use_fill_caps=True
    o=bpy.data.objects.new("cresta",cu); bpy.context.collection.objects.link(o); cu.materials.append(m); return o
X4=0.075
for sgn in (1,-1):
    pts=[]
    for th,x in [(22,0.215),(40,0.15),(60,0.10),(80,X4),(100,0.085),(118,0.12),(132,0.17)]:
        loc,nor=surf(x,sgn*th)
        if loc: pts.append(tuple(loc-nor*0.008))
    ridge(pts,0.0135,SKIN)
    for th in (30,45):        # relieve de la escápula
        loc,nor=surf(-0.27,sgn*th)
        if loc: ell(loc-nor*0.012,1.0,SKIN,(0.075,0.02,0.045))
bpy.context.view_layer.update(); dg=bpy.context.evaluated_depsgraph_get()
# línea amarilla discontinua de cresta a cresta, sobre la piel, cruzando L4
for th in range(-78,79,13):
    loc,nor=surf(X4,th)
    if not loc: continue
    bpy.ops.mesh.primitive_cylinder_add(radius=0.0045,depth=0.022,location=loc+nor*0.004,vertices=12); o=bpy.context.object
    tang=Vector((0,math.sin(math.radians(th)),math.cos(math.radians(th))))
    o.rotation_mode='QUATERNION'; o.rotation_quaternion=Vector((0,0,1)).rotation_difference(tang); link(o,YEL)
TOP,_=surf(X4,80)
print("crest-top",TOP,flush=True)
# ----- esqueleto simplificado (solo visible en el plano de rayos X)
BONE=mat("hueso",(0.95,0.90,0.78),0.5,emit=0.25)
BONES=[]
def keep(): BONES.append(bpy.context.object); return bpy.context.object
for i,x in enumerate([-0.15,-0.075,0.0,0.075,0.15]):
    by=yc(x)-0.025
    bpy.ops.mesh.primitive_cylinder_add(radius=0.024,depth=0.046,location=(x,by,Z),rotation=(0,math.pi/2,0),vertices=32); link(keep(),BONE); sm()
    bpy.ops.mesh.primitive_cube_add(location=(x+0.006,by-0.045,Z)); o=keep(); o.scale=(0.010,0.032,0.006); link(o,BONE)   # apófisis espinosa
    bpy.ops.mesh.primitive_cube_add(location=(x,by-0.02,Z)); o=keep(); o.scale=(0.012,0.008,0.040); link(o,BONE)        # apófisis transversas
import bmesh
def spline(P,n=24):
    P=[Vector(p) for p in P]; out=[]
    for i in range(len(P)-1):
        p0=P[max(i-1,0)];p1=P[i];p2=P[i+1];p3=P[min(i+2,len(P)-1)]
        for k in range(n):
            t=k/n; out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3))
    out.append(P[-1]); return out
for sgn in (1,-1):   # palas ilíacas en abanico: el borde superior es la cresta y su punto más alto queda a la altura de L4
    w=lambda x,dz,dy=0.0: (x,yc(x)-0.035+dy,Z+sgn*dz)
    arc=spline([w(0.235,0.025,-0.02),w(0.15,0.055,-0.01),w(0.075,0.105),w(0.095,0.15,0.03),w(0.16,0.165,0.06),w(0.20,0.16,0.08)])
    piv=Vector(w(0.27,0.085,0.03))
    me=bpy.data.meshes.new("pala"); bm=bmesh.new(); vp=bm.verts.new(piv)
    va=[bm.verts.new(p) for p in arc]
    rings=[]
    for f in (0.35,0.7):
        rings.append([bm.verts.new(piv.lerp(p,f)+Vector((0,0.012*math.sin(math.pi*f),0))) for p in arc])
    allr=[ [vp]*len(arc) ]+rings+[va]
    for r0,r1 in zip(allr,allr[1:]):
        for i in range(len(arc)-1):
            vs=[r0[i],r0[i+1],r1[i+1],r1[i]]
            vs=list(dict.fromkeys(vs))
            if len(vs)>=3: bm.faces.new(vs)
    bm.to_mesh(me); bm.free(); o=bpy.data.objects.new("pala",me); bpy.context.collection.objects.link(o); BONES.append(o); me.materials.append(BONE)
    sd=o.modifiers.new("g","SOLIDIFY"); sd.thickness=0.010; ss=o.modifiers.new("s","SUBSURF"); ss.levels=1; ss.render_levels=2
    for p in o.data.polygons: p.use_smooth=True
    cu=bpy.data.curves.new("rebordecresta","CURVE"); cu.dimensions='3D'; spn=cu.splines.new('POLY'); spn.points.add(len(arc)-1)
    for p,q in zip(spn.points,arc): p.co=(*q,1)
    cu.bevel_depth=0.007; cu.bevel_resolution=4; cu.use_fill_caps=True; c=bpy.data.objects.new("rebordecresta",cu); bpy.context.collection.objects.link(c); cu.materials.append(BONE); BONES.append(c)
bpy.ops.mesh.primitive_cone_add(radius1=0.045,radius2=0.015,depth=0.12,location=(0.27,yc(0.27)-0.02,Z),rotation=(0,math.pi/2,0),vertices=32); o=keep(); o.scale=(1,0.45,1); link(o,BONE); sm()  # sacro
for o in BONES: o.hide_render=True
# punto de punción L4-L5
xm=(L[4][0]+L[5][0])/2; P,Nn=skin_at(xm)
bpy.ops.mesh.primitive_cylinder_add(radius=0.013,depth=0.003,location=P+Nn*0.003,vertices=32); o=bpy.context.object; o.rotation_mode='QUATERNION'; o.rotation_quaternion=Vector((0,0,1)).rotation_difference(Nn); link(o,RED)
# aguja espinal: entra por línea media, ligeramente cefálica
nd=bpy.data.objects.new("aguja",None); bpy.context.collection.objects.link(nd)
for prim,kw,m in [("cyl",dict(radius=0.0016,depth=0.09,location=(0,0,0.045)),STEEL),("cone",dict(radius1=0.0016,radius2=0,depth=0.006,location=(0,0,-0.003),rotation=(math.pi,0,0)),STEEL),("cyl",dict(radius=0.0065,depth=0.024,location=(0,0,0.102)),HUB)]:
    (bpy.ops.mesh.primitive_cylinder_add if prim=="cyl" else bpy.ops.mesh.primitive_cone_add)(vertices=16,**kw); o=bpy.context.object; link(o,m); o.parent=nd
ang=math.radians(12); dirv=Vector((math.sin(ang),-math.cos(ang),0)).normalized()   # eje de la aguja hacia fuera
nd.rotation_mode='QUATERNION'; nd.rotation_quaternion=Vector((0,0,1)).rotation_difference(dirv)
# ----- luz: estudio oscuro, principal fría suave, contraluz amarillo que recorta la silueta
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0.004,0.004,0.005,1)
def area(loc,tgt,energy,col,size):
    d=bpy.data.lights.new("a","AREA"); d.energy=energy; d.color=col; d.size=size; o=bpy.data.objects.new("a",d); o.location=loc; bpy.context.collection.objects.link(o)
    o.rotation_mode='QUATERNION'; o.rotation_quaternion=(Vector(tgt)-Vector(loc)).to_track_quat('-Z','Y')
area((-0.4,-1.3,1.9),(0,0.1,Z),22,(0.95,0.97,1.0),1.4)
area((0.6,1.2,1.6),(0,0.1,Z),45,(1.0,0.78,0.12),1.0)
area((0.9,-0.6,0.9),(0,0.1,Z),8,(1.0,0.9,0.7),0.5)
bpy.ops.mesh.primitive_plane_add(size=14,location=(0,0,0)); link(bpy.context.object,mat("suelo",(0.015,0.015,0.017),0.3))
# ----- cámara con giro: columna en vertical en el encuadre 9:16 (cabeza arriba)
cam=bpy.data.cameras.new("cam"); co=bpy.data.objects.new("cam",cam); bpy.context.collection.objects.link(co); sc.camera=co
def aim(pos,tgt,lens,up=None):
    up=up or (Vector((0,0,1)) if lens<30 else Vector((-1,0,0)))
    pos=Vector(pos);tgt=Vector(tgt); f=(tgt-pos).normalized(); r=f.cross(up).normalized(); u=r.cross(f)
    M=Matrix((r,u,-f)).transposed(); co.matrix_world=Matrix.Translation(pos)@M.to_4x4(); cam.lens=lens
r=sc.render; r.resolution_x=int(A[1]) if len(A)>1 else 540; r.resolution_y=r.resolution_x*16//9
r.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=int(A[2]) if len(A)>2 else 12; sc.cycles.use_denoising=True
sc.cycles.max_bounces=3; sc.cycles.diffuse_bounces=2; sc.cycles.glossy_bounces=2; sc.cycles.transmission_bounces=0; sc.cycles.use_adaptive_sampling=True
sc.view_settings.view_transform='Standard'; sc.view_settings.look='None'
r.image_settings.file_format='JPEG'; r.image_settings.quality=92; sc.render.film_transparent=False
SHOTS={
 "general":((0.10,-1.35,1.45),(-0.05,0.30,Z),26,0.6),
 "crestas":((X4+0.03,-0.45,Z+0.62),(X4,yc(X4)-0.02,Z+0.09),30,0.6),
 "rayos":((X4+0.02,-0.62,Z+0.22),(X4+0.03,yc(X4)-0.03,Z),34,0.6),
 "marca":((xm,-0.40,0.95),(xm,P.y,Z),42,0.6),
 "aguja_lejos":((xm+0.04,-0.30,Z+0.36),(xm,P.y-0.05,Z),40,0.16),
 "aguja_piel":((xm+0.05,-0.24,Z+0.26),(xm,P.y-0.03,Z),50,0.004),
}
def setshot(name):
    xr=(name=='rayos')
    for o in BONES: o.hide_render=not xr
    b=SKIN.node_tree.nodes['Principled BSDF']; b.inputs['Alpha'].default_value=0.16 if xr else 1.0
    pos,tgt,lens,d=SHOTS[name]; aim(pos,tgt,lens); nd.location=P+dirv*d if d<0.5 else Vector((0,0,-5))
if A and A[0]=="stills":
    for n in (A[3:] or SHOTS):
        setshot(n); r.filepath=f"/home/claude/v3d/s2_{n}.jpg"; t=time.time(); bpy.ops.render.render(write_still=True); print(n,round(time.time()-t,1),flush=True)

if A and A[0]=="anim":
    a0,a1,N=int(A[3]),int(A[4]),60
    p0,t0,l0,_=SHOTS["aguja_lejos"]; p1,t1,l1,_=SHOTS["aguja_piel"]
    ease=lambda u: u*u*(3-2*u)
    for f in range(a0,a1):
        u=f/(N-1)
        cu=ease(min(1,u/0.75)); pos=Vector(p0).lerp(Vector(p1),cu); tg=Vector(t0).lerp(Vector(t1),cu); aim(pos,tg,l0+(l1-l0)*cu)
        d=0.18+(0.004-0.18)*ease(min(1,u/0.6)) if u<0.6 else (0.004 if u<0.72 else 0.004+(-0.03-0.004)*ease((u-0.72)/0.28))
        nd.location=P+dirv*d
        r.filepath=f"/home/claude/v3d/fr/n_{f:03d}.jpg"; bpy.ops.render.render(write_still=True)
    print("ok",a0,a1,flush=True)
