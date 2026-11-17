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
BED=mat("camilla",(0.10,0.105,0.115),0.6)
SHEET=mat("sabana",(0.20,0.22,0.25),0.85)
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
bpy.ops.mesh.primitive_cube_add(location=(0,0.33,0.40)); o=bpy.context.object; o.scale=(1.10,0.50,0.05); link(o,BED)
bpy.ops.mesh.primitive_cube_add(location=(0,0.33,0.46)); o=bpy.context.object; o.scale=(1.08,0.49,0.012); link(o,SHEET)
bpy.ops.mesh.primitive_cylinder_add(radius=0.11,depth=0.30,location=(-0.80,0.15,0.54),rotation=(0,math.pi/2,0)); link(bpy.context.object,SHEET); sm()
Z=0.66
import bmesh
PARTS=[]
def spl(P,n=10):
    P=[Vector(p) for p in P]; out=[]
    for i in range(len(P)-1):
        p0=P[max(i-1,0)];p1=P[i];p2=P[i+1];p3=P[min(i+2,len(P)-1)]
        for k in range(n):
            t=k/n; out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3))
    out.append(P[-1]); return out
def interp(prof,u):
    for (u0,a0,b0),(u1,a1,b1) in zip(prof,prof[1:]):
        if u0<=u<=u1:
            f=(u-u0)/(u1-u0); f=f*f*(3-2*f); return a0+(a1-a0)*f, b0+(b1-b0)*f
    return prof[-1][1],prof[-1][2]
def loft(ctrl,prof,name,n=12,seg=40,yoff=None):
    """tubo continuo: ctrl = puntos del eje; prof = [(u, semieje profundidad, semieje ancho)] con u de 0 a 1"""
    pts=spl(ctrl,n); L=[0]
    for p,q in zip(pts,pts[1:]): L.append(L[-1]+(q-p).length)
    me=bpy.data.meshes.new(name); bm=bmesh.new(); rings=[]
    for i,p in enumerate(pts):
        t=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized()
        wz=Vector((0,0,1)); dep=wz.cross(t).normalized()
        if dep.y>0: dep=-dep          # "profundidad" apunta hacia la espalda (-Y)
        a,b=interp(prof,L[i]/L[-1])
        off=yoff(L[i]/L[-1]) if yoff else 0.0
        ring=[]
        for k in range(seg):
            ang=2*math.pi*k/seg; c,s_=math.cos(ang),math.sin(ang)
            # sección algo aplanada por detrás (espalda) y redonda por delante
            ra=a*(0.92 if c>0 else 1.0)
            ring.append(bm.verts.new(p+dep*(ra*c+off)+wz*(b*s_)))
        rings.append(ring)
    for r0,r1 in zip(rings,rings[1:]):
        for k in range(seg): bm.faces.new((r0[k],r0[(k+1)%seg],r1[(k+1)%seg],r1[k]))
    for r,rev in ((rings[0],True),(rings[-1],False)):
        c=bm.verts.new(sum((v.co for v in r),Vector())/len(r))
        for k in range(seg):
            f=(r[k],r[(k+1)%seg],c) if not rev else (r[(k+1)%seg],r[k],c); bm.faces.new(f)
    bm.to_mesh(me); bm.free(); o=bpy.data.objects.new(name,me); bpy.context.collection.objects.link(o); PARTS.append(o); return o
def E(c,sem,rot=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1,location=c,segments=40,ring_count=20); o=bpy.context.object; o.scale=sem
    if rot is not None: o.rotation_mode='QUATERNION'; o.rotation_quaternion=rot
    PARTS.append(o); return o
along=lambda p1,p2: Vector((1,0,0)).rotation_difference(Vector(p2)-Vector(p1))
# tronco: del sacro a la base del cuello, en C (flexión)
loft([(0.40,0.175,Z),(0.30,0.160,Z),(0.15,0.135,Z),(0.00,0.130,Z),(-0.16,0.145,Z),(-0.30,0.180,Z),(-0.38,0.205,Z)],
     [(0.00,0.050,0.070),(0.06,0.105,0.150),(0.16,0.118,0.172),(0.30,0.106,0.158),(0.45,0.096,0.138),(0.60,0.108,0.150),(0.76,0.118,0.165),(0.88,0.110,0.190),(0.96,0.085,0.150),(1.00,0.055,0.060)],"tronco")
loft([(-0.36,0.205,Z),(-0.41,0.232,Z),(-0.46,0.262,Z)],[(0,0.072,0.074),(1,0.062,0.066)],"cuello",n=6)
for dz in (0.068,-0.068): E((0.335,0.135,Z+dz),(0.085,0.080,0.082))
E((-0.535,0.300,Z),(0.118,0.100,0.092),along((-0.47,0.26,Z),(-0.62,0.35,Z)))    # cabeza lisa, sin cara
for dz in (0.088,-0.088):                  # piernas en flexión
    loft([(0.24,0.17,Z+dz*0.7),(0.22,0.33,Z+dz),(0.10,0.50,Z+dz),(0.00,0.62,Z+dz),(0.10,0.70,Z+dz),(0.24,0.745,Z+dz*0.92),(0.33,0.77,Z+dz*0.9)],
         [(0,0.115,0.100),(0.12,0.098,0.096),(0.35,0.078,0.076),(0.47,0.050,0.050),(0.55,0.052,0.050),(0.66,0.056,0.052),(0.85,0.036,0.034),(1,0.030,0.030)],"pierna",n=8,seg=32)
    E((0.375,0.83,Z+dz*0.9),(0.072,0.028,0.036),along((0.33,0.77,Z),(0.41,0.89,Z)))   # pie
for dz in (0.125,-0.105):                  # brazos que abrazan las rodillas
    loft([(-0.31,0.205,Z+dz*1.05),(-0.29,0.33,Z+dz),(-0.20,0.47,Z+dz*0.7),(-0.11,0.53,Z+dz*0.55),(0.00,0.60,Z+dz*0.42),(0.07,0.625,Z+dz*0.35)],
         [(0,0.058,0.060),(0.15,0.048,0.050),(0.42,0.040,0.042),(0.55,0.040,0.040),(0.75,0.034,0.036),(1,0.026,0.030)],"brazo",n=8,seg=28)
    E((0.11,0.640,Z+dz*0.3),(0.056,0.022,0.040),along((0.07,0.625,Z),(0.15,0.65,Z)))  # mano
bpy.context.view_layer.update()
for o in bpy.context.selected_objects: o.select_set(False)
for o in PARTS: o.select_set(True)
bpy.context.view_layer.objects.active=PARTS[0]; bpy.ops.object.join(); BODY=bpy.context.object; BODY.name="cuerpo"
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
rm=BODY.modifiers.new("fusion","REMESH"); rm.mode='VOXEL'; rm.voxel_size=0.004; bpy.ops.object.modifier_apply(modifier="fusion")
lp=BODY.modifiers.new("lap","LAPLACIANSMOOTH"); lp.iterations=8; lp.lambda_factor=1.5; lp.use_volume_preserve=True; bpy.ops.object.modifier_apply(modifier="lap")
cs=BODY.modifiers.new("cs","CORRECTIVE_SMOOTH"); cs.iterations=10; cs.factor=0.6; bpy.ops.object.modifier_apply(modifier="cs")
bpy.ops.object.shade_smooth(); BODY.data.materials.clear(); BODY.data.materials.append(SKIN)
T=BODY
bpy.context.view_layer.update()
dg=bpy.context.evaluated_depsgraph_get()
def skin_at(x,z=Z):
    hit,loc,nor,*_=sc.ray_cast(dg,Vector((x,-2,z)),Vector((0,1,0)))
    return loc,nor
# apófisis espinosas L1-L5 + sacro: pequeños relieves sobre la línea media
L={}
for i,x in enumerate([-0.15,-0.075,0.0,0.075,0.15]):  # L1..L5; L4 = 0.075
    loc,nor=skin_at(x); L[i+1]=(x,loc)
# ----- anatomía de superficie: crestas ilíacas, escápulas y línea de Tuffier
import numpy as np
SKX=[-0.38,-0.30,-0.16,0.0,0.15,0.30,0.40]; SKY=[0.205,0.18,0.145,0.13,0.135,0.16,0.175]
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
import numpy as np
feat=[]   # (punto, amplitud, sigma) relieves puntuales
lines=[]  # (polilínea, amplitud, sigma) relieves lineales
CR=[(22,0.215),(42,0.15),(62,0.10),(80,X4),(100,0.085),(120,0.125),(132,0.165)]
for sgn in (1,-1):
    pl=[]
    for k in range(60):
        u=k/59*(len(CR)-1); i=min(int(u),len(CR)-2); f=u-i
        th=CR[i][0]+(CR[i+1][0]-CR[i][0])*f; x=CR[i][1]+(CR[i+1][1]-CR[i][1])*f
        loc,nor=surf(x,sgn*th)
        if loc: pl.append(np.array(loc))
    lines.append((np.array(pl),0.0065,0.011))                       # cresta ilíaca: reborde continuo
    for x in (-0.27,):
        loc,nor=surf(x,sgn*40)
        if loc: feat.append((loc,0.0030,0.045))                    # escápula: relieve amplio y suave
for x in [-0.15,-0.075,0.0,0.075,0.15]:
    loc,nor=surf(x,0)
    if loc: feat.append((loc,0.0035,0.007))                        # apófisis espinosas
def segdist(V,pl):
    A=pl[:-1]; B=pl[1:]; AB=B-A; L2=(AB**2).sum(1)+1e-12
    t=np.clip(((V[:,None,:]-A[None])*AB[None]).sum(2)/L2[None],0,1)
    C=A[None]+t[...,None]*AB[None]; return np.sqrt(((V[:,None,:]-C)**2).sum(2)).min(1)
bm=bmesh.new(); bm.from_mesh(BODY.data); bm.normal_update()
V=np.array([v.co[:] for v in bm.verts]); N=np.array([v.normal[:] for v in bm.verts]); W=np.zeros(len(V))
for p,A_,S_ in feat: W=np.maximum(W,A_*np.exp(-((V-np.array(p))**2).sum(1)/S_**2))
for pl,A_,S_ in lines:
    near=np.where(((V[:,0]>pl[:,0].min()-0.05)&(V[:,0]<pl[:,0].max()+0.05)))[0]
    d=segdist(V[near],pl); W[near]=np.maximum(W[near],A_*np.exp(-(d/S_)**2))
for i,v in enumerate(bm.verts):
    w=W[i]; t=math.atan2(v.co.z-Z, -(v.co.y-yc(v.co.x)))
    if -0.36<v.co.x<0.22 and abs(t)<0.35 and v.co.y<yc(v.co.x): w-=0.0035*math.exp(-(t/0.12)**2)   # surco paravertebral
    if w!=0: v.co+=v.normal*w
bm.to_mesh(BODY.data); bm.free(); BODY.data.update()
bpy.context.view_layer.update(); dg=bpy.context.evaluated_depsgraph_get()
# línea amarilla discontinua de cresta a cresta, sobre la piel, cruzando L4
for th in range(-78,79,13):
    loc,nor=surf(X4,th)
    if not loc: continue
    bpy.ops.mesh.primitive_cylinder_add(radius=0.0032,depth=0.016,location=loc+nor*0.003,vertices=12); o=bpy.context.object
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
GLOVE=mat("guante",(0.30,0.55,0.85),0.45)
def gpart(obj): obj.parent=nd; link(obj,GLOVE); bpy.ops.object.shade_smooth(); return obj
def gcaps(p1,p2,r):
    p1=Vector(p1);p2=Vector(p2);d=p2-p1
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=d.length,location=(p1+p2)/2,vertices=24); c=bpy.context.object
    c.rotation_mode='QUATERNION'; c.rotation_quaternion=Vector((0,0,1)).rotation_difference(d); gpart(c)
    for p in (p1,p2): bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=p,segments=24,ring_count=12); gpart(bpy.context.object)
# mano enguantada en pinza sobre el cono de la aguja (coordenadas locales de la aguja: +Z hacia fuera)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1,location=(0.050,0.0,0.170),segments=32,ring_count=16); o=bpy.context.object; o.scale=(0.026,0.011,0.034); gpart(o)
gcaps((0.040,0.008,0.150),(0.012,0.008,0.112),0.0085)      # índice
gcaps((0.040,-0.010,0.150),(0.012,-0.010,0.112),0.0085)    # pulgar
gcaps((0.055,0.0,0.140),(0.050,0.0,0.118),0.008)           # medio, flexionado
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
 "gotas":((xm+0.10,-0.30,Z+0.10),tuple(P+dirv*0.10),45,-0.03),
 "aguja_lejos":((xm+0.10,-0.40,Z+0.30),tuple(P+dirv*0.11),30,0.16),
 "aguja_piel":((xm+0.09,-0.32,Z+0.22),tuple(P+dirv*0.06),36,0.004),
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

if A and A[0]=="orbit":
    a0,a1,N=int(A[3]),int(A[4]),58
    ease=lambda u: u*u*(3-2*u)
    c=Vector((-0.05,0.30,Z))
    for f in range(a0,a1):
        u=ease(f/(N-1)); el=math.radians(25+53*u); R=1.80-0.15*u
        pos=c+Vector((0.15*(1-u),-R*math.cos(el),R*math.sin(el)))
        aim(pos,c,26,up=Vector((0,0,1)) if u<0.5 else Vector((-1,0,0)).lerp(Vector((0,0,1)),0.0)); nd.location=Vector((0,0,-5))
        r.filepath=f"/home/claude/v3d/fo/o_{f:03d}.jpg"; bpy.ops.render.render(write_still=True)
    print("ok",a0,a1,flush=True)
if A and A[0]=="gotas":
    a0,a1,N=int(A[3]),int(A[4]),36
    setshot("gotas")
    hubtip=P+dirv*(-0.03+0.112)
    drops=[]
    for i in range(3):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0022,location=(0,0,-5),segments=16,ring_count=8); d=bpy.context.object; d.scale=(1,1,1.35)
        link(d,mat("lcr",(0.75,0.88,1.0),0.05,emit=0.4)); bpy.ops.object.shade_smooth(); drops.append(d)
    for f in range(a0,a1):
        for i,d in enumerate(drops):
            t=(f-i*12)/30.0
            d.location=hubtip+Vector((0,0,-(0.5*9.8*0.06*t*t))) if t>=0 else Vector((0,0,-5))
            if t>0.9: d.location=Vector((0,0,-5))
        r.filepath=f"/home/claude/v3d/fg/g_{f:03d}.jpg"; bpy.ops.render.render(write_still=True)
    print("ok",a0,a1,flush=True)
