import bpy, math, sys
from mathutils import Vector
A=sys.argv[sys.argv.index("--")+1:]
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
def mat(n,c,r=0.5,emit=0.0,alpha=1.0,metal=0.0):
    m=bpy.data.materials.new(n); m.use_nodes=True; b=m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value=(*c,1); b.inputs["Roughness"].default_value=r; b.inputs["Metallic"].default_value=metal
    if emit: b.inputs["Emission Color"].default_value=(*c,1); b.inputs["Emission Strength"].default_value=emit
    b.inputs["Alpha"].default_value=alpha; return m
def box(x0,x1,z0,z1,m,y=0.03,bev=0.0):
    bpy.ops.mesh.primitive_cube_add(location=((x0+x1)/2,0,(z0+z1)/2)); o=bpy.context.object; o.scale=((x1-x0)/2,y,(z1-z0)/2)
    if bev: bv=o.modifiers.new("b","BEVEL"); bv.width=bev; bv.segments=6
    o.data.materials.append(m); return o
SKIN=mat("piel",(0.16,0.165,0.18),0.45); FAT=mat("grasa",(0.85,0.72,0.35),0.6); BONE=mat("hueso",(0.95,0.90,0.78),0.5,emit=0.15)
LIG=mat("lig",(0.80,0.80,0.84),0.5); FLAV=mat("amarillo",(1.0,0.80,0.05),0.4,emit=0.4); DURA=mat("dura",(0.25,0.45,0.85),0.4,emit=0.3)
CSF=mat("lcr",(0.55,0.80,1.0),0.1,emit=0.35); NERV=mat("nervio",(0.95,0.95,0.85),0.5); STEEL=mat("acero",(0.92,0.92,0.95),0.15,metal=1.0); HUB=mat("cono",(1.0,0.8,0.05),0.3)
H=0.10
box(-0.004,0.0,-H,H,SKIN); box(0.0,0.015,-H,H,FAT)
box(0.015,0.019,-H,H,LIG)                                 # supraespinoso
for zc in (0.048,-0.048): box(0.019,0.050,zc-0.034,zc+0.034,BONE)   # apófisis espinosas L4 (arriba) y L5 (abajo)
box(0.019,0.046,-0.014,0.014,LIG)                         # interespinoso
box(0.046,0.051,-H,H,FLAV)                                # ligamento amarillo
box(0.051,0.055,-H,H,FAT)                                 # espacio epidural
box(0.055,0.0565,-H,H,DURA)                               # duramadre
box(0.0565,0.080,-H,H,CSF)                                # espacio subaracnoideo con LCR
for x in (0.062,0.066,0.070,0.074):                       # raíces de la cola de caballo
    bpy.ops.mesh.primitive_cylinder_add(radius=0.0011,depth=2*H,location=(x,-0.032,0)); bpy.context.object.data.materials.append(NERV)
box(0.080,0.11,-H,H,BONE)                                 # muro posterior del cuerpo vertebral
nd=bpy.data.objects.new("aguja",None); bpy.context.collection.objects.link(nd)
bpy.ops.mesh.primitive_cylinder_add(radius=0.0009,depth=0.20,location=(-0.10,-0.035,0),rotation=(0,math.pi/2,0),vertices=16); o=bpy.context.object; o.data.materials.append(STEEL); o.parent=nd
bpy.ops.mesh.primitive_cone_add(radius1=0.0009,radius2=0,depth=0.003,location=(0.0015,-0.035,0),rotation=(0,math.pi/2,0),vertices=16); o=bpy.context.object; o.data.materials.append(STEEL); o.parent=nd
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0.01,0.01,0.012,1)
d=bpy.data.lights.new("a","AREA"); d.energy=0.35; d.size=0.4; o=bpy.data.objects.new("a",d); o.location=(0.03,-0.30,0.15); o.rotation_euler=(math.radians(70),0,0); bpy.context.collection.objects.link(o)
cam=bpy.data.cameras.new("c"); cam.type='ORTHO'; cam.ortho_scale=0.19; co=bpy.data.objects.new("c",cam); bpy.context.collection.objects.link(co); sc.camera=co
co.location=(0.045,-0.4,0); co.rotation_euler=(math.radians(90),0,0)
r=sc.render; r.resolution_x=540; r.resolution_y=960; r.engine='CYCLES'; sc.cycles.samples=16; sc.cycles.use_denoising=True; sc.cycles.device='CPU'
sc.view_settings.view_transform='Standard'; r.image_settings.file_format='JPEG'; r.image_settings.quality=92
# avance de la punta: rápido por tejidos blandos, frena en el amarillo y en la duramadre ("resalte"), entra en LCR
KEY=[(0,-0.035),(14,0.012),(26,0.040),(32,0.0455),(36,0.0505),(42,0.053),(47,0.0558),(52,0.0605),(59,0.0615)]
def tip(f):
    for (f0,x0),(f1,x1) in zip(KEY,KEY[1:]):
        if f0<=f<=f1: u=(f-f0)/(f1-f0); u=u*u*(3-2*u); return x0+(x1-x0)*u
    return KEY[-1][1]
a0,a1=int(A[0]),int(A[1])
for f in range(a0,a1):
    nd.location=(tip(f),0,0)
    r.filepath=f"/home/claude/v3d/fc/c_{f:03d}.jpg"; bpy.ops.render.render(write_still=True)
print("ok",a0,a1,flush=True)
