import bpy, sys, math
sys.path.insert(0,"/home/claude/v3d/mh")
import numpy as np
from humano import build, X
import mano
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
A=sys.argv[sys.argv.index("--")+1:]
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
def M(n,c,r=0.5,e=0.0,sss=0.0,metal=0.0):
    m=bpy.data.materials.new(n); m.use_nodes=True; b=m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value=(*c,1); b.inputs["Roughness"].default_value=r; b.inputs["Metallic"].default_value=metal
    if e: b.inputs["Emission Color"].default_value=(*c,1); b.inputs["Emission Strength"].default_value=e
    if sss: b.inputs["Subsurface Weight"].default_value=sss; b.inputs["Subsurface Radius"].default_value=(0.010,0.004,0.002)
    return m
SKIN=M("piel",(0.78,0.56,0.45),0.45,sss=0.12); CLOTH=M("bata",(0.42,0.58,0.70),0.85); GLOVE=M("guante",(0.93,0.93,0.91),0.33,sss=0.05)
SEAT={"spine05":(X,14),"spine04":(X,5),"spine03":(X,4),"spine02":(X,3),"spine01":(X,2),"neck01":(X,-4),"neck02":(X,-3),"head":(X,4),
 "upperleg01.L":("dir",(0.02,-0.98,0.12)),"upperleg01.R":("dir",(-0.02,-0.98,0.12)),
 "lowerleg01.L":("dir",(0.0,0.08,-1)),"lowerleg01.R":("dir",(0.0,0.08,-1)),
 "upperarm01.L":("dir",(0.15,-0.25,-0.95)),"upperarm01.R":("dir",(-0.15,-0.25,-0.95)),
 "lowerarm01.L":("dir",(-0.10,-0.95,-0.25)),"lowerarm01.R":("dir",(0.10,-0.95,-0.25))}
ob,J=build(SEAT); ob.data.materials.append(SKIN); ob.data.materials.append(CLOTH)
import humano
V,F=humano.load_obj(); used=sorted({i for f in F for i in f}); REST=np.array(V)[used]
for p in ob.data.polygons:
    c=REST[list(p.vertices)].mean(0)
    if -0.30<c[2]<0.55 and abs(c[0])<0.24: p.material_index=1      # bata/ropa en tronco y muslos
bpy.context.view_layer.update()
zmin=min((ob.matrix_world@v.co).z for v in ob.data.vertices)
ob.matrix_world=Matrix.Translation((0,0,-zmin))@ob.matrix_world
bpy.context.view_layer.update()
dg=bpy.context.evaluated_depsgraph_get(); me=ob.evaluated_get(dg).to_mesh()
BV=BVHTree.FromPolygons([ob.matrix_world@v.co for v in me.vertices],[tuple(p.vertices) for p in me.polygons])
vs=[ob.matrix_world@v.co for v in me.vertices]
cand=[i for i,p in enumerate(REST) if p[2]>0.60 and abs(p[0])<0.012]
inose=min(cand,key=lambda i:REST[i][1])
NOSE=ob.matrix_world@ob.data.vertices[inose].co
FACEDIR=(NOSE-(ob.matrix_world@ob.data.vertices[max(cand,key=lambda i:REST[i][1])].co)).normalized()
SOFT=NOSE-FACEDIR*0.010+Vector((0,0,0.004))
# taburete
st=M("taburete",(0.12,0.125,0.135),0.5)
seat_z=min(v.z for v in vs if abs(v.y-0.05)<0.08 and abs(v.x)<0.15)
bpy.ops.mesh.primitive_cylinder_add(radius=0.22,depth=0.04,location=(0,0.04,seat_z-0.02),vertices=48); bpy.context.object.data.materials.append(st)
bpy.ops.mesh.primitive_plane_add(size=14,location=(0,0,0)); bpy.context.object.data.materials.append(M("suelo",(0.02,0.02,0.022),0.35))
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0.006,0.006,0.007,1)
def area(loc,tgt,e,col,size):
    d=bpy.data.lights.new("a","AREA"); d.energy=e; d.color=col; d.size=size; o=bpy.data.objects.new("a",d); o.location=loc; bpy.context.collection.objects.link(o)
    o.rotation_mode='QUATERNION'; o.rotation_quaternion=(Vector(tgt)-Vector(loc)).to_track_quat('-Z','Y')
area((-1.2,-1.4,2.0),NOSE,70,(1,0.96,0.9),1.8); area((1.3,0.8,1.8),NOSE,45,(1,0.8,0.25),1.2); area((-1.5,0.3,1.0),NOSE,12,(0.85,0.9,1),1.0)
# mano enguantada en pinza sobre la parte blanda de la nariz
hand=mano.build_hand(GLOVE); hm=hand.data
def gp(n):
    g=hand.vertex_groups[n]; return [hand.matrix_world@v.co for v in hm.vertices if any(ge.group==g.index and ge.weight>0.5 for ge in v.groups)]
wr0=sum(gp("wrist.R"),Vector())/len(gp("wrist.R"))
ti=max(gp("finger2-3.R"),key=lambda p:(p-wr0).length); tt=max(gp("finger1-3.R"),key=lambda p:(p-wr0).length)
pinch=(ti+tt)/2; fh=(pinch-wr0).normalized(); ah=(ti-tt); ah=(ah-fh*ah.dot(fh)).normalized()
src=Matrix((fh,ah,fh.cross(ah))).transposed()
ft=(-FACEDIR*0.9+Vector((0.25,0,0.3))).normalized()          # la mano llega desde delante y abajo hacia la nariz
at=Vector((1,0,0)); at=(at-ft*at.dot(ft)).normalized()   # pulgar e índice a ambos lados de la nariz
dst=Matrix((ft,at,ft.cross(at))).transposed()
hand.matrix_world=Matrix.Translation(SOFT)@(dst@src.inverted()).to_4x4()@Matrix.Translation(-pinch)
cam=bpy.data.cameras.new("c"); co=bpy.data.objects.new("c",cam); bpy.context.collection.objects.link(co); sc.camera=co
def aim(pos,tgt,lens):
    pos=Vector(pos);tgt=Vector(tgt); f=(tgt-pos).normalized(); up=Vector((0,0,1)); rr=f.cross(up).normalized(); u=rr.cross(f)
    co.matrix_world=Matrix.Translation(pos)@Matrix((rr,u,-f)).transposed().to_4x4(); cam.lens=lens
r=sc.render; r.resolution_x=540; r.resolution_y=960; r.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=16; sc.cycles.use_denoising=True
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'; r.image_settings.file_format='JPEG'; r.image_settings.quality=92
C=(sum(vs,Vector())/len(vs))
SH={"general":((1.9,-1.6,1.2),(0,-0.05,0.75),32,False),"perfil":((NOSE.x+0.55,NOSE.y+0.02,NOSE.z+0.06),(NOSE.x,NOSE.y+0.07,NOSE.z-0.02),50,False),
    "pinza":((NOSE.x+0.48,NOSE.y-0.12,NOSE.z+0.06),(NOSE.x,NOSE.y+0.05,NOSE.z-0.02),45,True)}
for n in (A or SH):
    p,t,l,h=SH[n]; hand.hide_render=not h; aim(p,t,l); r.filepath=f"/home/claude/v3d/mh/e2_{n}.jpg"; bpy.ops.render.render(write_still=True); print(n,flush=True)
