import bpy, math, sys, bmesh
from mathutils import Vector, Matrix
A=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
def mat(n,c,r=0.5,emit=0.0,metal=0.0,alpha=1.0):
    m=bpy.data.materials.new(n); m.use_nodes=True; b=m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value=(*c,1); b.inputs["Roughness"].default_value=r; b.inputs["Metallic"].default_value=metal; b.inputs["Alpha"].default_value=alpha
    if emit: b.inputs["Emission Color"].default_value=(*c,1); b.inputs["Emission Strength"].default_value=emit
    return m
SKIN=mat("maniqui",(0.16,0.165,0.18),0.42); DARK=mat("orificio",(0.02,0.02,0.02),0.8); SEPT=mat("tabique",(0.85,0.55,0.55),0.5,emit=0.15)
KIES=mat("kiesselbach",(0.95,0.05,0.06),0.4,emit=2.5); BONE=mat("hueso",(0.95,0.90,0.78),0.5,emit=0.2); PACK=mat("tapon",(0.95,0.95,0.92),0.8,emit=0.15)
STOOL=mat("taburete",(0.10,0.105,0.115),0.5); YEL=mat("luz",(1.0,0.85,0.2),0.3,emit=3.0)
PARTS=[]
def E(c,sem,rot=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1,location=c,segments=40,ring_count=20); o=bpy.context.object; o.scale=sem
    if rot: o.rotation_euler=rot
    PARTS.append(o); return o
def C(p1,p2,r1,r2):
    p1=Vector(p1);p2=Vector(p2);d=p2-p1
    bpy.ops.mesh.primitive_cone_add(radius1=r1,radius2=r2,depth=d.length,location=(p1+p2)/2,vertices=40); o=bpy.context.object
    o.rotation_mode='QUATERNION'; o.rotation_quaternion=Vector((0,0,1)).rotation_difference(d); PARTS.append(o)
    for p,r in ((p1,r1),(p2,r2)): bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=p,segments=32,ring_count=16); PARTS.append(bpy.context.object)
# ---- figura sentada (cara hacia +X): superficies continuas
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
def loft(ctrl,prof,name,n=10,seg=36,wax=Vector((0,1,0)),shift=None):
    pts=spl(ctrl,n); L=[0]
    for p,q in zip(pts,pts[1:]): L.append(L[-1]+(q-p).length)
    me=bpy.data.meshes.new(name); bm=bmesh.new(); rings=[]
    for i,p in enumerate(pts):
        t=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized(); dep=wax.cross(t).normalized()
        a,b=interp(prof,L[i]/L[-1]); off=shift(L[i]/L[-1]) if shift else 0
        rings.append([bm.verts.new(p+dep*(a*math.cos(2*math.pi*k/seg)+off)+wax*(b*math.sin(2*math.pi*k/seg))) for k in range(seg)])
    for r0,r1 in zip(rings,rings[1:]):
        for k in range(seg): bm.faces.new((r0[k],r0[(k+1)%seg],r1[(k+1)%seg],r1[k]))
    for r,rev in ((rings[0],True),(rings[-1],False)):
        c=bm.verts.new(sum((v.co for v in r),Vector())/len(r))
        for k in range(seg): bm.faces.new((r[(k+1)%seg],r[k],c) if rev else (r[k],r[(k+1)%seg],c))
    bm.to_mesh(me); bm.free(); o=bpy.data.objects.new(name,me); bpy.context.collection.objects.link(o); PARTS.append(o); return o
# tronco vertical: de la pelvis a la base del cuello (secciones: profundidad X, anchura Y)
loft([(0,0,0.56),(0,0,0.70),(0.005,0,0.88),(0.0,0,1.05),(0.0,0,1.15)],
     [(0,0.10,0.15),(0.12,0.115,0.17),(0.35,0.095,0.14),(0.62,0.11,0.16),(0.85,0.10,0.19),(1,0.06,0.07)],"tronco",wax=Vector((0,1,0)))
loft([(0,0,1.14),(0.008,0,1.20),(0.018,0,1.25)],[(0,0.060,0.062),(1,0.055,0.056)],"cuello",n=5,wax=Vector((0,1,0)))
# cabeza: cráneo, cara y mentón como una sola sección variable
loft([(0.0,0,1.23),(0.012,0,1.28),(0.016,0,1.35),(0.008,0,1.42),(0.0,0,1.47)],
     [(0,0.050,0.050),(0.15,0.085,0.065),(0.40,0.098,0.074),(0.70,0.100,0.078),(0.92,0.088,0.068),(1,0.045,0.04)],"cabeza",n=10,wax=Vector((0,1,0)),
     shift=lambda u: -0.012*math.sin(math.pi*min(1,u*1.3)))
E((0.070,0,1.275),(0.040,0.040,0.022))      # mentón
# nariz: dorso desde la raíz hasta la punta, y alas
loft([(0.090,0,1.385),(0.105,0,1.355),(0.121,0,1.328)],[(0,0.007,0.008),(0.6,0.010,0.011),(1,0.012,0.013)],"nariz",n=8,seg=24,wax=Vector((0,1,0)))
E((0.118,0,1.322),(0.015,0.014,0.013))
for s in (1,-1): E((0.104,0.015*s,1.318),(0.013,0.008,0.010))
for s in (1,-1):                             # muslos y piernas (sentado)
    loft([(0.02,0.09*s,0.58),(0.20,0.095*s,0.585),(0.40,0.10*s,0.575)],[(0,0.085,0.085),(1,0.058,0.058)],"muslo",n=6,seg=28,wax=Vector((0,0,1)))
    loft([(0.40,0.10*s,0.575),(0.41,0.105*s,0.35),(0.42,0.11*s,0.10)],[(0,0.056,0.056),(0.3,0.058,0.055),(1,0.035,0.035)],"pierna",n=6,seg=28,wax=Vector((0,1,0)))
    loft([(0.0,0.20*s,1.10),(0.02,0.215*s,0.92),(0.12,0.19*s,0.80),(0.28,0.16*s,0.70)],[(0,0.050,0.050),(0.45,0.040,0.040),(1,0.030,0.030)],"brazo",n=6,seg=24,wax=Vector((0,1,0)))
bpy.context.view_layer.update()
for o in bpy.context.selected_objects: o.select_set(False)
for o in PARTS: o.select_set(True)
bpy.context.view_layer.objects.active=PARTS[0]; bpy.ops.object.join(); BODY=bpy.context.object
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
rm=BODY.modifiers.new("f","REMESH"); rm.mode='VOXEL'; rm.voxel_size=0.0028; bpy.ops.object.modifier_apply(modifier="f")
lp=BODY.modifiers.new("l","LAPLACIANSMOOTH"); lp.iterations=6; lp.lambda_factor=1.0; bpy.ops.object.modifier_apply(modifier="l")
bpy.ops.object.shade_smooth(); BODY.data.materials.clear(); BODY.data.materials.append(SKIN)
# orificios nasales
NOS=[]
for s in (1,-1):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.0055,depth=0.004,location=(0.112,0.0075*s,1.311),rotation=(0,math.radians(30),0),vertices=24); o=bpy.context.object; o.scale=(1.4,1,1); o.data.materials.append(DARK); NOS.append(o)
# anatomía interna (solo en rayos X): tabique, zona de Kiesselbach, suelo de la fosa, cornetes
INT=[]
bpy.ops.mesh.primitive_cube_add(location=(0.060,0,1.345)); o=bpy.context.object; o.scale=(0.050,0.0015,0.040); o.data.materials.append(SEPT); INT.append(o)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.011,location=(0.098,-0.002,1.327),segments=24,ring_count=12); o=bpy.context.object; o.scale=(1.3,0.25,1.0); o.data.materials.append(KIES); INT.append(o)
bpy.ops.mesh.primitive_cube_add(location=(0.050,0,1.303)); o=bpy.context.object; o.scale=(0.060,0.020,0.0025); o.data.materials.append(BONE); INT.append(o)   # suelo de la fosa (paladar duro)
for z in (1.322,1.345):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1,location=(0.040,-0.012,z),segments=24,ring_count=12); o=bpy.context.object; o.scale=(0.035,0.004,0.006); o.data.materials.append(BONE); INT.append(o)   # cornetes
for o in INT: o.hide_render=True
# taponamiento (esponja alargada) y algodón
bpy.ops.mesh.primitive_cylinder_add(radius=0.006,depth=0.075,location=(0,0,0),rotation=(0,math.pi/2,0),vertices=24); TAP=bpy.context.object; TAP.data.materials.append(PACK)
bv=TAP.modifiers.new("b","BEVEL"); bv.width=0.004; bv.segments=4; TAP.location=(0.30,0,-5)
# taburete
bpy.ops.mesh.primitive_cylinder_add(radius=0.20,depth=0.04,location=(0.02,0,0.50),vertices=48); bpy.context.object.data.materials.append(STOOL)
bpy.ops.mesh.primitive_cylinder_add(radius=0.03,depth=0.48,location=(0.02,0,0.24),vertices=24); bpy.context.object.data.materials.append(STOOL)
# inclinación hacia delante del tronco y la cabeza (pivote en la pelvis): todo lo que está por encima de la pelvis
piv=Vector((0,0,0.62)); Rm=Matrix.Rotation(math.radians(22),4,'Y')   # cabeza hacia +X y abajo
def tilt(o):
    o.matrix_world=Matrix.Translation(piv)@Rm@Matrix.Translation(-piv)@o.matrix_world
bm=bmesh.new(); bm.from_mesh(BODY.data)
for v in bm.verts:
    if v.co.z>0.66 and abs(v.co.y)<0.16 or (v.co.z>0.66 and v.co.x<0.12):
        w=min(1,(v.co.z-0.66)/0.12); p=Vector(v.co); q=piv+(Rm.to_3x3()@(p-piv)); v.co=p.lerp(q,w)
bm.to_mesh(BODY.data); bm.free()
for o in NOS+INT: tilt(o)
for o in NOS: o.hide_render=True
NOSE_TIP=piv+(Rm.to_3x3()@(Vector((0.112,0,1.311))-piv))
FLOOR_DIR=(Rm.to_3x3()@Vector((-1,0,0))).normalized()     # hacia atrás, paralelo al suelo de la fosa
# luz y cámara
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0.004,0.004,0.005,1)
def area(loc,tgt,e,col,size):
    d=bpy.data.lights.new("a","AREA"); d.energy=e; d.color=col; d.size=size; o=bpy.data.objects.new("a",d); o.location=loc; bpy.context.collection.objects.link(o)
    o.rotation_mode='QUATERNION'; o.rotation_quaternion=(Vector(tgt)-Vector(loc)).to_track_quat('-Z','Y')
area((0.8,-1.6,2.0),(0.2,0,1.1),40,(0.95,0.97,1.0),1.4); area((-1.0,0.8,1.8),(0.2,0,1.1),55,(1.0,0.78,0.12),1.0); area((1.2,0.2,0.9),(0.2,0,1.1),10,(1,0.9,0.7),0.6)
bpy.ops.mesh.primitive_plane_add(size=14,location=(0,0,0)); bpy.context.object.data.materials.append(mat("suelo",(0.015,0.015,0.017),0.3))
cam=bpy.data.cameras.new("c"); co=bpy.data.objects.new("c",cam); bpy.context.collection.objects.link(co); sc.camera=co
def aim(pos,tgt,lens):
    pos=Vector(pos);tgt=Vector(tgt); f=(tgt-pos).normalized(); up=Vector((0,0,1)); r=f.cross(up).normalized(); u=r.cross(f)
    co.matrix_world=Matrix.Translation(pos)@Matrix((r,u,-f)).transposed().to_4x4(); cam.lens=lens
r=sc.render; r.resolution_x=540; r.resolution_y=960; r.engine='CYCLES'; sc.cycles.samples=12; sc.cycles.use_denoising=True; sc.cycles.device='CPU'
sc.cycles.max_bounces=3; sc.view_settings.view_transform='Standard'; r.image_settings.file_format='JPEG'; r.image_settings.quality=92
N=NOSE_TIP
SH={"general":((0.75,-1.55,1.05),(0.20,0,0.85),28),
    "perfil":((N.x+0.16,-0.48,N.z+0.06),(N.x-0.06,0,N.z+0.01),45),
    "pinza":((N.x+0.16,-0.48,N.z+0.06),(N.x-0.04,0,N.z+0.0),45),
    "rayos":((N.x-0.02,-0.34,N.z+0.03),(N.x-0.05,0,N.z+0.02),52),
    "tapon":((N.x-0.02,-0.34,N.z+0.03),(N.x-0.05,0,N.z+0.02),52)}
GL=mat("guante",(0.30,0.55,0.85),0.45); HAND=[]
def hc(p1,p2,r):
    p1=Vector(p1);p2=Vector(p2);d=p2-p1
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=d.length,location=(p1+p2)/2,vertices=24); c=bpy.context.object
    c.rotation_mode='QUATERNION'; c.rotation_quaternion=Vector((0,0,1)).rotation_difference(d); c.data.materials.append(GL); bpy.ops.object.shade_smooth(); HAND.append(c)
    for p in (p1,p2): bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=p,segments=24,ring_count=12); bpy.context.object.data.materials.append(GL); bpy.ops.object.shade_smooth(); HAND.append(bpy.context.object)
for s_ in (1,-1): hc(N+Vector((0.080,0.034*s_,-0.020)),N+Vector((-0.004,0.0175*s_,0.013)),0.0080)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1,location=N+Vector((0.105,0,-0.05)),segments=32,ring_count=16); o=bpy.context.object; o.scale=(0.04,0.035,0.028); o.data.materials.append(GL); bpy.ops.object.shade_smooth(); HAND.append(o)
def setshot(n):
    for o in HAND: o.hide_render=(n!="pinza")
    xr=n in ("rayos","tapon")
    SKIN.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value=0.22 if xr else 1.0
    for o in INT: o.hide_render=not xr
    TAP.location=(0,0,-5)
    if n=="tapon":
        TAP.rotation_mode='QUATERNION'; TAP.rotation_quaternion=Vector((0,0,1)).rotation_difference(FLOOR_DIR)
        TAP.location=N+FLOOR_DIR*0.022+Vector((0,-0.006,0.004))
    p,t,l=SH[n]; aim(p,t,l)
if A and A[0]=="stills":
    for n in (A[1:] or SH):
        setshot(n); r.filepath=f"/home/claude/v3d/epi/e_{n}.jpg"; bpy.ops.render.render(write_still=True); print(n,flush=True)
