"""Construye el modelo humano CC0 de MakeHuman, lo rigea con su esqueleto y lo posa.
Uso (dentro de bpy): from humano import build; obj = build(pose_dict)"""
import bpy, json, math
import numpy as np
from mathutils import Vector, Matrix, Quaternion
D="/home/claude/mh/makehuman/data/"
def load_obj():
    V=[];F=[];grp=None
    for l in open(D+"3dobjs/base.obj"):
        if l.startswith("v "): x,y,z=map(float,l.split()[1:4]); V.append((x,-z,y))
        elif l.startswith("g "): grp=l.split()[1]
        elif l.startswith("f ") and grp=="body": F.append([int(t.split("/")[0])-1 for t in l.split()[1:]])
    return np.array(V)*0.1, F
def build(pose, name="humano", extras=()):
    V,F=load_obj()
    used=sorted({i for f in F for i in f}); remap={o:n for n,o in enumerate(used)}
    me=bpy.data.meshes.new(name); me.from_pydata([tuple(V[i]) for i in used],[],[[remap[i] for i in f] for f in F]); me.update()
    ob=bpy.data.objects.new(name,me); bpy.context.collection.objects.link(ob)
    sk=json.load(open(D+"rigs/default.mhskel")); J={k:V[v].mean(0) for k,v in sk["joints"].items()}
    arm=bpy.data.armatures.new("rig"); ao=bpy.data.objects.new("rig",arm); bpy.context.collection.objects.link(ao)
    bpy.context.view_layer.objects.active=ao; bpy.ops.object.mode_set(mode='EDIT')
    for n,b in sk["bones"].items():
        eb=arm.edit_bones.new(n); eb.head=Vector(J[b["head"]]); eb.tail=Vector(J[b["tail"]])
        if (eb.tail-eb.head).length<1e-5: eb.tail=eb.head+Vector((0,0,0.01))
    for n,b in sk["bones"].items():
        if b["parent"]: arm.edit_bones[n].parent=arm.edit_bones[b["parent"]]
    bpy.ops.object.mode_set(mode='OBJECT')
    W=json.load(open(D+"rigs/default_weights.mhw"))["weights"]
    for bn,lst in W.items():
        vg=ob.vertex_groups.new(name=bn)
        for vi,w in lst:
            if vi in remap: vg.add([remap[vi]],w,'REPLACE')
    md=ob.modifiers.new("arm","ARMATURE"); md.object=ao; ob.parent=ao
    for eo,bn in extras:
        vg=eo.vertex_groups.new(name=bn); vg.add(list(range(len(eo.data.vertices))),1.0,'REPLACE')
        m2=eo.modifiers.new("arm","ARMATURE"); m2.object=ao
    # pose: (eje, grados) = rotación relativa al padre en ejes globales de reposo; ("dir", vector) = dirección final del hueso en el mundo
    bpy.context.view_layer.objects.active=ao; bpy.ops.object.mode_set(mode='POSE')
    acc={}
    def order(n,out):
        out.append(n)
        for c in ao.data.bones[n].children: order(c.name,out)
        return out
    for bn in order("root",[]):
        pb=ao.pose.bones[bn]; bone=pb.bone; Mr=bone.matrix_local.to_quaternion()
        par=acc.get(bone.parent.name,Quaternion()) if bone.parent else Quaternion()
        spec=pose.get(bn)
        if spec is None: delta=Quaternion()
        elif spec[0]=="dir":
            rest=(bone.tail_local-bone.head_local).normalized(); cur=par@rest
            delta=par.inverted()@cur.rotation_difference(Vector(spec[1]).normalized())@par
        else: delta=Quaternion(Vector(spec[0]).normalized(),math.radians(spec[1]))
        acc[bn]=par@delta
        pb.rotation_mode='QUATERNION'; pb.rotation_quaternion=Mr.inverted()@delta@Mr
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.update()
    import os
    if os.environ.get('DBG'):
        for n in ['upperleg01.L','upperleg02.L','lowerleg01.L','foot.L','upperleg01.R','upperleg02.R','lowerleg01.R','foot.R','upperarm01.R','lowerarm01.R']:
            pb=ao.pose.bones[n]; print('DBG',n,[round(x,2) for x in pb.head],[round(x,2) for x in pb.tail])
    # aplicar la pose y quitar el esqueleto
    bpy.context.view_layer.objects.active=ob
    for o in bpy.context.selected_objects: o.select_set(False)
    ob.select_set(True); bpy.ops.object.modifier_apply(modifier="arm")
    for eo,bn in extras:
        for o in bpy.context.selected_objects: o.select_set(False)
        bpy.context.view_layer.objects.active=eo; eo.select_set(True); bpy.ops.object.modifier_apply(modifier="arm")
    bpy.context.view_layer.objects.active=ob
    ob.parent=None; ob.matrix_world=Matrix(); bpy.data.objects.remove(ao)
    for side in (".L",".R"):
        g=ob.vertex_groups.get("breast"+side)
        if g:
            for v in me.vertices:
                for ge in v.groups:
                    if ge.group==g.index and ge.weight>0.05: v.co.y+=0.022*ge.weight
    sub=ob.modifiers.new("s","SUBSURF"); sub.levels=1; sub.render_levels=2
    for p in me.polygons: p.use_smooth=True
    return ob, {k:Vector(v) for k,v in J.items()}
X=(1,0,0); Y=(0,1,0); Z=(0,0,1)
FETAL={
 "spine05":(X,5),"spine04":(X,9),"spine03":(X,9),"spine02":(X,6),"spine01":(X,4),
 "neck01":(X,10),"neck02":(X,8),"neck03":(X,6),"head":(X,12),
 "upperleg01.L":("dir",(-0.06,-0.92,0.38)),"upperleg01.R":("dir",(0.26,-0.88,0.38)),
 "lowerleg01.L":("dir",(-0.03,0.50,-0.87)),"lowerleg01.R":("dir",(-0.02,0.50,-0.87)),
 "upperarm01.L":("dir",(0.25,-0.35,-0.90)),"upperarm01.R":("dir",(-0.25,-0.35,-0.90)),
 "lowerarm01.L":("dir",(-0.60,-0.70,-0.38)),"lowerarm01.R":("dir",(0.60,-0.70,-0.38)),
}
