# blender -b --factory-startup --python IceMammoth/_scratch/sweep.py
# Scoop-pose search: for candidate (head, neck, trunk1..4) pitches, the world z of Trunk_Tip (bone head), the lowest
# trunk vertex, and the lowest head vertex (tusks) - no keys, the pose is set directly.
import sys, runpy, json, itertools, math
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"]("IceMammoth", save=False)
k = R3["STATE"]["k"]
pk = R3["pk"]
import bpy
from mathutils import Vector
arm, body = k.arm, k.main
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
k.set_action("act_dustover")
arm.animation_data.action = None


def setp(b, rot, loc=None):
    pb = arm.pose.bones[b]
    R0 = arm.data.bones[b].matrix_local.to_quaternion()
    pb.rotation_quaternion = R0.inverted() @ pk.Rq(*rot) @ R0
    if loc is not None:
        pb.location = R0.inverted() @ Vector(loc)


def measure(hd, nk, tp):
    for p in arm.pose.bones:
        p.rotation_quaternion = (1, 0, 0, 0)
        p.location = (0, 0, 0)
    setp("Neck", (nk, 0, 0))
    setp("Head", (hd, 0, 0))
    for b, v in zip(("Trunk1", "Trunk2", "Trunk3", "Trunk4"), tp):
        setp(b, (v, 0, 0))
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = ev.to_mesh()
    lo = {}
    for i, v in enumerate(me.vertices):
        o = owner[i]
        if o in ("Trunk3", "Trunk4", "Head", "Jaw"):
            z = (ev.matrix_world @ v.co).z
            lo[o] = min(lo.get(o, 9), z)
    ev.to_mesh_clear()
    tip = (arm.matrix_world @ arm.pose.bones["Trunk_Tip"].head)
    return round(tip.z, 3), round(tip.y, 3), {o: round(z, 3) for o, z in lo.items()}


cands = []
for hd in (10, 13, 16):
    for nk in (3,):
        for tp in ((0, 0, 0, 30), (0, 0, 4, 45), (-2, 0, 6, 60), (0, -4, 4, 60), (-4, -4, 8, 70), (2, 0, 0, 50),
                   (-6, -2, 6, 75), (-4, 0, 10, 80)):
            cands.append((hd, nk, tp))
res = []
for hd, nk, tp in cands:
    tz, ty, lo = measure(hd, nk, tp)
    res.append({"head": hd, "neck": nk, "trunk": tp, "tip_z": tz, "tip_y": ty, "low": lo})
print("SWEEP " + json.dumps(res))
