import bpy, sys, math, time
sys.path.insert(0,"/home/claude/v3d/mh")
import numpy as np
from humano import build, FETAL, load_obj
import huesos
from mathutils import Vector, Matrix, Quaternion
A=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
V,F=load_obj(); used=sorted({i for f in F for i in f}); B=V[used]; MID=B[np.abs(B[:,0])<0.03]
def back_y(z): s=MID[np.abs(MID[:,2]-z)<0.01]; return float(s[:,1].max())
def skin_rest(x,z):
    s=B[(np.abs(B[:,0]-x)<0.008)&(np.abs(B[:,2]-z)<0.008)&(B[:,1]>-0.05)]
    i=np.argmax(s[:,1]+0*s[:,0]) if abs(x)<0.08 else np.argmax(np.abs(s[:,0])*0+s[:,1])
    return Vector(s[i])
def M(n,c,r=0.5,a=1.0,e=0.0,metal=0.0,sss=0.0):
    m=bpy.data.materials.new(n); m.use_nodes=True; b=m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value=(*c,1); b.inputs["Roughness"].default_value=r; b.inputs["Alpha"].default_value=a; b.inputs["Metallic"].default_value=metal
    if e: b.inputs["Emission Color"].default_value=(*c,1); b.inputs["Emission Strength"].default_value=e
    if sss: b.inputs["Subsurface Weight"].default_value=sss; b.inputs["Subsurface Radius"].default_value=(0.010,0.004,0.002)
    return m
SKIN=M("piel",(0.78,0.56,0.45),0.45,sss=0.12); CLOTH=M("ropa",(0.10,0.16,0.28),0.85)
BONE=M("hueso",(0.93,0.88,0.76),0.5,e=0.35); YEL=M("amarillo",(1.0,0.78,0.02),0.4,e=0.8); RED=M("rojo",(0.85,0.03,0.04),0.4,e=0.8)
BED=M("camilla",(0.12,0.125,0.135),0.6); SHEET=M("sabana",(0.55,0.62,0.70),0.85)
# marcas sobre la piel (en reposo) que siguen al esqueleto
EX=[]
def disc(name,p,nrm,r,mat,bone,depth=0.0015):
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=depth,location=p,vertices=24); o=bpy.context.object
    o.rotation_mode='QUATERNION'; o.rotation_quaternion=Vector((0,0,1)).rotation_difference(nrm)
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True); o.name=name; o.data.materials.append(mat); EX.append((o,bone)); return o
BONES=huesos.build(BONE,back_y)
ob,J=build(FETAL,extras=BONES)
ob.data.materials.append(SKIN); ob.data.materials.append(CLOTH)
# ropa interior: caras de la pelvis por debajo de L5 (en reposo) — se calcula con la posición de reposo guardada
for p,f in zip(ob.data.polygons,F):
    c=B[[{o:n for n,o in enumerate(used)}[i] for i in f]].mean(0) if False else None
REST=np.array([B[i] for i in range(len(B))])
for p in ob.data.polygons:
    c=REST[list(p.vertices)].mean(0)
    if -0.14<c[2]<(0.075 if c[1]>0 else 0.095) and abs(c[0])<0.22: p.material_index=1
# tumbar: decúbito lateral izquierdo (cabeza hacia +X, espalda hacia +Y, lado izquierdo abajo)
ALL=[ob]+[b for b,_ in BONES]
Rl=Matrix.Rotation(math.radians(90),4,'Y')
for o in ALL: o.matrix_world=Rl@o.matrix_world
bpy.context.view_layer.update()
zmin=min((o.matrix_world@v.co).z for v in ob.data.vertices)
T=Matrix.Translation((0,0,0.47-zmin+0.002))
for o in ALL: o.matrix_world=T@o.matrix_world
bpy.context.view_layer.update()
from mathutils.bvhtree import BVHTree
dg=bpy.context.evaluated_depsgraph_get(); oe=ob.evaluated_get(dg); me_e=oe.to_mesh()
BV=BVHTree.FromPolygons([ob.matrix_world@v.co for v in me_e.vertices],[tuple(p.vertices) for p in me_e.polygons])
def ctr(name): o=bpy.data.objects[name]; return o.matrix_world@(sum((v.co for v in o.data.vertices),Vector())/len(o.data.vertices))
def tipof(name):
    o=bpy.data.objects[name]; vs=[o.matrix_world@v.co for v in o.data.vertices]; return max(vs,key=lambda v:v.y)
BACK=Vector((0,1,0))
def onskin(p,d=BACK):
    loc,nrm,i,dist=BV.ray_cast(p+d*0.25,-d)
    return (loc,nrm.normalized()) if loc else (None,None)
def mark_disc(p,n,r,mat,name):
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=0.0015,location=p+n*0.0012,vertices=28); o=bpy.context.object; o.name=name
    o.rotation_mode='QUATERNION'; o.rotation_quaternion=Vector((0,0,1)).rotation_difference(n); o.data.materials.append(mat); return o
T={k:tipof("espinosa_"+k) for k in ("L3","L4","L5")}
P45,N45=onskin((T["L4"]+T["L5"])/2); P34,N34=onskin((T["L3"]+T["L4"])/2)
mark_disc(P45,N45,0.0075,RED,"punto_L4L5"); mark_disc(P34,N34,0.0075,RED,"punto_L3L4")
PL4,NL4=onskin(T["L4"])
# línea de Tuffier: plano perpendicular a la columna en L4; se recorre la piel alrededor del eje
axis=(T["L3"]-T["L5"]).normalized(); cb=ctr("cuerpo_L4"); c0=cb+axis*((T["L4"]-cb).dot(axis))
u=(BACK-axis*BACK.dot(axis)).normalized(); v=axis.cross(u).normalized()
line=[]
for th in np.linspace(-80,80,47):
    t=math.radians(th); d=(u*math.cos(t)+v*math.sin(t)).normalized()
    loc,nrm,i,dist=BV.ray_cast(c0+d*0.5,-d)
    if loc: line.append((loc,nrm.normalized()))
for i in range(0,len(line)-1,2):
    (a,na),(b_,nb)=line[i],line[i+1]; d=b_-a
    bpy.ops.mesh.primitive_cylinder_add(radius=0.0022,depth=d.length*0.85,location=(a+b_)/2+((na+nb)/2).normalized()*0.0015,vertices=10); o=bpy.context.object
    o.rotation_mode='QUATERNION'; o.rotation_quaternion=Vector((0,0,1)).rotation_difference(d); o.data.materials.append(YEL)
ymax=max((ob.matrix_world@v.co).y for v in ob.data.vertices)
# camilla bajo el paciente, con la espalda en el borde
bpy.ops.mesh.primitive_cube_add(location=(0.05,ymax-0.45,0.41)); o=bpy.context.object; o.scale=(1.0,0.42,0.05); o.data.materials.append(BED)
bpy.ops.mesh.primitive_cube_add(location=(0.05,ymax-0.45,0.465)); o=bpy.context.object; o.scale=(0.98,0.41,0.008); o.data.materials.append(SHEET)
bpy.ops.mesh.primitive_cylinder_add(radius=0.10,depth=0.30,location=(0.78,ymax-0.32,0.54),rotation=(math.pi/2,0,0)); bpy.context.object.data.materials.append(SHEET)
bpy.ops.mesh.primitive_plane_add(size=14,location=(0,0,0)); bpy.context.object.data.materials.append(M("suelo",(0.02,0.02,0.022),0.35))
# luz suave y natural + contraluz de marca
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0.006,0.006,0.007,1)
def area(loc,tgt,e,col,size):
    d=bpy.data.lights.new("a","AREA"); d.energy=e; d.color=col; d.size=size; o=bpy.data.objects.new("a",d); o.location=loc; bpy.context.collection.objects.link(o)
    o.rotation_mode='QUATERNION'; o.rotation_quaternion=(Vector(tgt)-Vector(loc)).to_track_quat('-Z','Y')
CEN=Vector((0.0,ymax-0.2,0.62))
area((0.3,ymax+1.2,1.9),CEN,70,(1.0,0.96,0.90),1.8)
area((-0.8,ymax-1.2,1.5),CEN,45,(1.0,0.80,0.25),1.2)
area((1.3,ymax+0.4,0.8),CEN,12,(0.85,0.90,1.0),1.0)
# ---- aguja espinal y mano enguantada
import mano
STEEL=M("acero",(0.92,0.92,0.95),0.15,metal=1.0); HUBM=M("cono",(1.0,0.82,0.10),0.25); GLOVE=M("guante",(0.93,0.93,0.91),0.33,sss=0.05)
HEAD=Vector((1,0,0))
inward=(-N45+HEAD*0.22).normalized(); dirv=-inward
nd=bpy.data.objects.new("aguja",None); bpy.context.collection.objects.link(nd)
def part(op,mat,**kw):
    op(**kw); o=bpy.context.object; o.data.materials.append(mat); o.parent=nd; bpy.ops.object.shade_smooth(); return o
part(bpy.ops.mesh.primitive_cylinder_add,STEEL,radius=0.00075,depth=0.090,location=(0,0,0.045),vertices=16)
part(bpy.ops.mesh.primitive_cone_add,STEEL,radius1=0.00075,radius2=0.0,depth=0.004,location=(0,0,-0.002),rotation=(math.pi,0,0),vertices=16)
part(bpy.ops.mesh.primitive_cylinder_add,HUBM,radius=0.0045,depth=0.018,location=(0,0,0.099),vertices=24)
part(bpy.ops.mesh.primitive_cylinder_add,HUBM,radius=0.0062,depth=0.006,location=(0,0,0.111),vertices=24)
nd.rotation_mode='QUATERNION'; nd.rotation_quaternion=Vector((0,0,1)).rotation_difference(dirv)
HUBLOCAL=0.100
hand=mano.build_hand(GLOVE)
me=hand.data
def grp_pts(name):
    g=hand.vertex_groups[name]; return [hand.matrix_world@v.co for v in me.vertices if any(ge.group==g.index and ge.weight>0.5 for ge in v.groups)]
wr0=sum(grp_pts("wrist.R"),Vector())/max(1,len(grp_pts("wrist.R")))
ti=max(grp_pts("finger2-3.R"),key=lambda p:(p-wr0).length); tt=max(grp_pts("finger1-3.R"),key=lambda p:(p-wr0).length)
pinch=(ti+tt)/2; fh=(pinch-wr0).normalized(); ah=(ti-tt); ah=(ah-fh*ah.dot(fh)).normalized()
src=Matrix((fh,ah,fh.cross(ah))).transposed()
side=Vector((0,0,1)); side=(side-dirv*side.dot(dirv)).normalized()
ft=(inward*0.55+(-side)*0.0+side*-0.0).normalized()
ft=(inward*0.80-side*0.60).normalized()      # la mano del médico llega desde detrás del paciente y algo por arriba
at=dirv.cross(ft).normalized(); ft=(at.cross(dirv)*0+ft); at=(at-ft*at.dot(ft)).normalized()
dst=Matrix((ft,at,ft.cross(at))).transposed()
R=(dst@src.inverted()).to_4x4()
def place_hand(d):
    hub=P45+dirv*(d+HUBLOCAL)
    hand.matrix_world=Matrix.Translation(hub)@R@Matrix.Translation(-pinch)
cam=bpy.data.cameras.new("c"); co=bpy.data.objects.new("c",cam); bpy.context.collection.objects.link(co); sc.camera=co
def aim(pos,tgt,lens,up=Vector((0,0,1))):
    pos=Vector(pos);tgt=Vector(tgt); f=(tgt-pos).normalized(); r=f.cross(up).normalized(); u=r.cross(f)
    co.matrix_world=Matrix.Translation(pos)@Matrix((r,u,-f)).transposed().to_4x4(); cam.lens=lens
r=sc.render; r.resolution_x=int(A[1]) if len(A)>1 else 540; r.resolution_y=r.resolution_x*16//9
r.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=int(A[2]) if len(A)>2 else 16; sc.cycles.use_denoising=True; sc.cycles.max_bounces=4
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'; r.image_settings.file_format='JPEG'; r.image_settings.quality=92
HEADUP=Vector((1,0,0))
SH={"general":((0.25,ymax+1.25,1.30),(0.0,ymax-0.25,0.62),26,Vector((0,0,1))),
    "crestas":((P45.x+0.03,ymax+0.50,P45.z+0.14),(P45.x+0.01,P45.y,P45.z+0.03),32,HEADUP),
    "rayos":((P45.x+0.03,ymax+0.50,P45.z+0.14),(P45.x+0.01,P45.y,P45.z+0.03),32,HEADUP),
    "marca":((P45.x+0.01,ymax+0.30,P45.z+0.08),(P45.x+0.01,P45.y,P45.z),45,HEADUP),
    "arriba":((0.05,ymax-0.25,2.6),(0.05,ymax-0.25,0.6),30,Vector((1,0,0))),
    "frente":((0.05,ymax-1.8,0.75),(0.05,ymax-0.25,0.65),30,Vector((0,0,1))),
    "aguja_lejos":(None,None,30,HEADUP),
    "aguja_piel":(None,None,34,HEADUP),
    "cabecera":((1.6,ymax-0.2,1.2),(0.0,ymax-0.25,0.62),30,Vector((0,0,1)))}
def setshot(n):
    xr=(n=="rayos")
    SKIN.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value=0.18 if xr else 1.0
    CLOTH.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value=0.25 if xr else 1.0
    for b,_ in BONES: b.hide_render=not xr
    p,t,l,u=SH[n]
    dd={"aguja_lejos":0.12,"aguja_piel":0.003}.get(n,None)
    if dd is None: nd.location=Vector((0,0,-5)); hand.location=Vector((0,0,-5)); hand.matrix_world=Matrix.Translation((0,0,-5))
    else:
        nd.location=P45+dirv*dd; place_hand(dd)
        foc=P45+dirv*(0.17 if dd>0.05 else 0.10)
        p=foc+Vector((-0.03,0.0,0.40 if dd>0.05 else 0.30)); t=foc; u=dirv
    aim(p,t,l,u)
if A and A[0]=="stills":
    for n in (A[3:] or SH):
        setshot(n); r.filepath=f"/home/claude/v3d/mh/s_{n}.jpg"; t=time.time(); bpy.ops.render.render(write_still=True); print(n,round(time.time()-t,1),flush=True)
ease=lambda u: u*u*(3-2*u)
def save(path): r.filepath=path; bpy.ops.render.render(write_still=True)
if A and A[0]=="anim":
    kind,a0,a1=A[3],int(A[4]),int(A[5]); os=__import__("os"); os.makedirs(f"/home/claude/v3d/mh/f_{kind}",exist_ok=True)
    if kind=="orbit":
        setshot("general"); (p0,t0,l0,u0),(p1,t1,l1,u1)=SH["general"],SH["arriba"]
        for f in range(a0,a1):
            u=ease(f/57); p=Vector(p0).lerp(Vector(p1),u); t=Vector(t0).lerp(Vector(t1),u)
            up=Vector(u0).lerp(Vector(u1),u).normalized(); aim(p,t,l0+(l1-l0)*u,up); save(f"/home/claude/v3d/mh/f_orbit/o_{f:03d}.jpg")
    if kind=="aguja":
        setshot("aguja_piel")
        for f in range(a0,a1):
            u=f/59
            d=0.16+(0.003-0.16)*ease(min(1,u/0.6)) if u<0.6 else (0.003 if u<0.72 else 0.003+(-0.035-0.003)*ease((u-0.72)/0.28))
            nd.location=P45+dirv*d; place_hand(d)
            cu=ease(u); foc=P45+dirv*(0.17+(0.10-0.17)*cu); p=foc+Vector((-0.03,0.0,0.40+(0.30-0.40)*cu)); aim(p,foc,30+4*cu,dirv)
            save(f"/home/claude/v3d/mh/f_aguja/a_{f:03d}.jpg")
    if kind=="gotas":
        setshot("aguja_piel"); d=-0.035; nd.location=P45+dirv*d; hand.matrix_world=Matrix.Translation((0,0,-5))
        hubend=P45+dirv*(d+0.114); foc=hubend-dirv*0.02; aim(foc+Vector((-0.02,0.0,0.16)),foc,45,dirv)
        LCR=M("lcr",(0.85,0.93,1.0),0.05,e=0.3); drops=[]
        for i in range(3):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0022,location=(0,0,-5),segments=16,ring_count=8); o=bpy.context.object; o.scale=(1,1,1.35); o.data.materials.append(LCR); bpy.ops.object.shade_smooth(); drops.append(o)
        for f in range(a0,a1):
            for i,o in enumerate(drops):
                t=(f-i*12)/30.0
                o.location=hubend+dirv*0.002+Vector((0,0,-0.5*9.8*0.05*t*t)) if 0<=t<=0.9 else Vector((0,0,-5))
            save(f"/home/claude/v3d/mh/f_gotas/g_{f:03d}.jpg")
    print("ok",kind,a0,a1,flush=True)
