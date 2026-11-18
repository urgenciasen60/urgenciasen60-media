"""Mano derecha enguantada (modelo CC0 MakeHuman) con los dedos en pinza. build_hand(mat) -> (obj, punta_pulgar, punta_indice, muñeca)"""
import bpy, json, math, numpy as np
from mathutils import Vector, Quaternion, Matrix
import humano
def build_hand(mat):
    V,F=humano.load_obj(); sk=json.load(open(humano.D+"rigs/default.mhskel")); J={k:Vector(V[v].mean(0)) for k,v in sk["joints"].items()}
    jb=lambda b,e: J[sk["bones"][b][e]]
    wr=jb("wrist.R","head"); mid=jb("finger3-1.R","tail")-jb("finger3-1.R","head")
    across=jb("finger2-1.R","head")-jb("finger5-1.R","head")
    n=across.cross(mid).normalized()          # normal de la palma (comprobada por el signo de la flexión)
    pose={}
    def flex(f,angs,sign):
        for k,a in zip((1,2,3),angs):
            b=f"finger{f}-{k}.R"; d=(jb(b,"tail")-jb(b,"head")).normalized()
            pose[b]=(tuple(d.cross(n)*sign),a)
    import os; S=float(os.environ.get("FLEXSIGN","1"))
    flex(2,(30,45,25),S)                      # índice
    for f in (3,4,5): flex(f,(55,75,45),S)    # medio, anular y meñique recogidos
    pose["finger1-1.R"]=(tuple((across.cross(n)).normalized()),0)
    flex(1,(25,30,20),S*-1 if os.environ.get("THUMBNEG") else S)
    ob,Jp=humano.build(pose,name="mano_tmp")
    g=ob.vertex_groups["finger2-3.R"]; me=ob.data
    pts=[ob.matrix_world@v.co for v in me.vertices if any(ge.group==g.index and ge.weight>0.5 for ge in v.groups)]
    tip=max(pts,key=lambda p:(p-wr).length)
    g1=ob.vertex_groups["finger1-2.R"]
    t2=[ob.matrix_world@v.co for v in me.vertices if any(ge.group==g1.index and ge.weight>0.5 for ge in v.groups)]
    tb=sum(t2,Vector())/len(t2)
    bpy.data.objects.remove(ob)
    tgt=tip+(n*0.004)
    pose["finger1-1.R"]=("dir",tuple(((tb+tgt)/2-jb("finger1-1.R","head")).normalized()))
    pose["finger1-2.R"]=("dir",tuple((tgt-tb).normalized()))
    pose["finger1-3.R"]=("dir",tuple((tgt-tb).normalized()))
    ob,Jp=humano.build(pose,name="mano")
    globals()["TIP_INDEX"]=tip
    # quitar todo salvo mano y antebrazo distal (en reposo: x < muñeca + 0.13)
    import bmesh
    used=sorted({i for f in F for i in f}); REST=np.array(V)[used]
    bm=bmesh.new(); bm.from_mesh(ob.data)
    kill=[f for f in bm.faces if REST[[v.index for v in f.verts]].mean(0)[0] > wr.x+0.13]
    bmesh.ops.delete(bm,geom=kill,context='FACES')
    bmesh.ops.holes_fill(bm,edges=bm.edges,sides=0)
    bm.to_mesh(ob.data); bm.free()
    ob.data.materials.clear(); ob.data.materials.append(mat)
    # puntas de los dedos en la pose: vértice más alejado de la muñeca dentro de cada dedo
    return ob
