"""Pelvis y columna lumbar esquemáticas pero con forma anatómica, en el sistema de reposo del modelo MakeHuman
(frente -Y, espalda +Y, arriba +Z, izquierda del modelo +X). Devuelve [(objeto, hueso_del_esqueleto)]."""
import bpy, bmesh, math
from mathutils import Vector
ZV={"L5":0.117,"L4":0.155,"L3":0.193,"L2":0.231,"L1":0.269}   # centros vertebrales; línea de Tuffier en L4 (z=0.155)
ZC=0.155; Z45=0.136; Z34=0.174
def _obj(name,bm,mat):
    me=bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o=bpy.data.objects.new(name,me); bpy.context.collection.objects.link(o); me.materials.append(mat)
    for p in me.polygons: p.use_smooth=True
    return o
def _ell(name,c,sem,mat,rot=None):
    bm=bmesh.new(); bmesh.ops.create_uvsphere(bm,u_segments=24,v_segments=12,radius=1.0)
    for v in bm.verts:
        v.co=Vector((v.co.x*sem[0],v.co.y*sem[1],v.co.z*sem[2]))
        if rot: v.co=rot@v.co
        v.co+=Vector(c)
    return _obj(name,bm,mat)
def _tube(name,pts,r,mat,seg=12):
    cu=bpy.data.curves.new(name,"CURVE"); cu.dimensions='3D'; sp=cu.splines.new('NURBS'); sp.points.add(len(pts)-1)
    for p,q in zip(sp.points,pts): p.co=(*q,1)
    sp.use_endpoint_u=True; sp.order_u=min(4,len(pts)); cu.bevel_depth=r; cu.bevel_resolution=4; cu.use_fill_caps=True
    o=bpy.data.objects.new(name,cu); bpy.context.collection.objects.link(o); cu.materials.append(mat)
    bpy.context.view_layer.objects.active=o
    for x in bpy.context.selected_objects: x.select_set(False)
    o.select_set(True); bpy.ops.object.convert(target='MESH'); return bpy.context.object
def _fan(name,piv,arc,mat,thick=0.006):
    bm=bmesh.new(); pv=bm.verts.new(piv); rings=[[pv]*len(arc)]
    for f in (0.33,0.66): rings.append([bm.verts.new(Vector(piv).lerp(Vector(p),f)) for p in arc])
    rings.append([bm.verts.new(p) for p in arc])
    for r0,r1 in zip(rings,rings[1:]):
        for i in range(len(arc)-1):
            vs=list(dict.fromkeys([r0[i],r0[i+1],r1[i+1],r1[i]]))
            if len(vs)>=3: bm.faces.new(vs)
    o=_obj(name,bm,mat); sd=o.modifiers.new("g","SOLIDIFY"); sd.thickness=thick; ss=o.modifiers.new("s","SUBSURF"); ss.levels=2
    bpy.context.view_layer.objects.active=o
    for x in bpy.context.selected_objects: x.select_set(False)
    o.select_set(True)
    for m in list(o.modifiers): bpy.ops.object.modifier_apply(modifier=m.name)
    return o
def spline(P,n=10):
    P=[Vector(p) for p in P]; out=[]
    for i in range(len(P)-1):
        p0=P[max(i-1,0)];p1=P[i];p2=P[i+1];p3=P[min(i+2,len(P)-1)]
        for k in range(n):
            t=k/n; out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3))
    out.append(P[-1]); return out
def build(mat, back_y):
    """back_y(z): coordenada y de la piel de la espalda en la línea media"""
    out=[]
    for name,z in ZV.items():
        bone={"L5":"spine05","L4":"spine04","L3":"spine04","L2":"spine03","L1":"spine03"}[name]
        by=back_y(z); cy=by-0.072
        out.append((_ell(f"cuerpo_{name}",(0,cy,z),(0.024,0.018,0.0145),mat),bone))
        out.append((_ell(f"espinosa_{name}",(0,(cy+by-0.012)/2+0.006,z-0.004),(0.0045,0.022,0.0085),mat),bone))
        for s in (1,-1):
            out.append((_ell(f"transversa_{name}{s}",(0.030*s,cy+0.022,z),(0.022,0.006,0.0055),mat),bone))
            out.append((_tube(f"lamina_{name}{s}",[(0.012*s,cy+0.016,z),(0.010*s,cy+0.032,z),(0.0035*s,cy+0.046,z)],0.0045,mat),bone))
    # sacro
    bys=back_y(0.07)
    out.append((_ell("sacro",(0,bys-0.035,0.065),(0.045,0.018,0.050),mat),"root"))
    for s in (1,-1):
        crest=[(0.042*s,back_y(0.10)-0.020,0.100),(0.090*s,back_y(0.15)-0.030,ZC-0.006),(0.130*s,0.000,ZC+0.008),(0.142*s,-0.050,ZC-0.004),(0.122*s,-0.095,0.105)]
        arc=spline(crest,8)
        out.append((_fan(f"pala{s}",(0.098*s,-0.012,0.045),arc,mat),"root"))
        out.append((_tube(f"cresta{s}",[tuple(p) for p in arc[::3]]+[tuple(arc[-1])],0.0055,mat),"root"))
        ac=(0.098*s,-0.012,0.045)
        out.append((_tube(f"rama_sup{s}",[ac,(0.06*s,-0.075,0.020),(0.012*s,-0.105,0.005)],0.009,mat),"root"))
        out.append((_tube(f"isquion{s}",[ac,(0.085*s,0.015,-0.005),(0.07*s,0.020,-0.030),(0.035*s,-0.050,-0.025),(0.012*s,-0.100,-0.010)],0.010,mat),"root"))
        out.append((_ell(f"cabeza_femur{s}",ac,(0.023,0.023,0.023),mat),"upperleg01."+("L" if s>0 else "R")))
    return out
