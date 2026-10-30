# blender -b --factory-startup --python PermafrostTitan/_scratch/arm_search.py -- <Name> [frames=40] [grid=full|cur]
# r9 MUST 1: search the LEFT arm hold of act_kneelrise (out, fwd, bend; Arm_L rot = (-fwd, 0, -out), Fore_L rot =
# (-bend, 0, 0), Hand_L rest) for a pose that uncovers the kneeling shin + foot (claws) on the fixed game camera.
# Per candidate and frame:
#   vis_shin / vis_foot : share of Shin_L / Foot_L verts the camera sees (ray cast, nothing else in front)
#   coll                : any face overlap Fore_L / Fist_L / Hand_L vs Leg_L (BVH overlap)
#   gap                 : min surface distance fist + hand verts -> Leg_L faces
#   fist_z, chest_z     : fist centre height vs the Chest head (the "braced" read: low, on the thigh / knee)
# The Arm_L / Fore_L / Hand_L fcurves are muted and their pose set by hand, so every other bone keeps its keyed pose.
import sys, runpy, json, itertools
from mathutils import Vector, Quaternion
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
frames = [int(v) for v in opts.get("frames", "40").split(",")]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from bpy_extras.object_utils import world_to_camera_view
pk = R3["pk"]
R3["full"](name, save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = 700
arm = k.arm
k.set_action("act_kneelrise")
sc.frame_set(0)
loc, tgt = pk.camera_for(k, "game")
pk.aim(sc.camera, loc, tgt)
cam = sc.camera.matrix_world.to_translation()
ad = arm.animation_data
for fc in ad.action.fcurves if hasattr(ad.action, "fcurves") else k.fcurves():
    pass
fcs = k.fcurves()
MUTE = ('pose.bones["Arm_L"]', 'pose.bones["Fore_L"]', 'pose.bones["Hand_L"]')
for fc in fcs:
    if fc.data_path.startswith(MUTE):
        fc.mute = True
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]
ARMSET = ("Fore_L", "Fist_L", "Hand_L")


def setrot(bone, rot):
    pb = arm.pose.bones[bone]
    R0 = arm.data.bones[bone].matrix_local.to_quaternion()
    pb.rotation_quaternion = R0.inverted() @ pk.Rq(*rot) @ R0


def measure(f, out, fwd, bend):
    sc.frame_set(f)
    setrot("Arm_L", (-fwd, 0, -out))
    setrot("Fore_L", (-bend, 0, 0))
    setrot("Hand_L", (0, 0, 0))
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    W = [mw @ v.co for v in me.vertices]
    polys = [list(p.vertices) for p in me.polygons]
    pown = []
    for pl in polys:
        c = {}
        for i in pl:
            c[own[i]] = c.get(own[i], 0) + 1
        pown.append(max(c, key=c.get))
    full = BVHTree.FromPolygons(W, polys)
    res = {}
    for grp in ("Shin_L", "Foot_L"):
        ids = [i for i in range(len(W)) if own[i] == grp]
        vis = 0
        for i in ids:
            d = W[i] - cam
            h = full.ray_cast(cam, d.normalized(), d.length + 0.01)
            if h[0] is None or h[3] >= d.length - 0.004 or pown[h[2]] == grp:
                vis += 1
        res["vis_" + grp] = round(vis / max(1, len(ids)), 3)
        occ = {}
        for i in ids:
            d = W[i] - cam
            h = full.ray_cast(cam, d.normalized(), d.length + 0.01)
            if not (h[0] is None or h[3] >= d.length - 0.004 or pown[h[2]] == grp):
                occ[pown[h[2]]] = occ.get(pown[h[2]], 0) + 1
        res["occ_" + grp] = occ
    legp = [pl for pl, o in zip(polys, pown) if o == "Leg_L"]
    armp = [pl for pl, o in zip(polys, pown) if o in ARMSET]
    bl = BVHTree.FromPolygons(W, legp)
    ba = BVHTree.FromPolygons(W, armp)
    res["coll"] = len(bl.overlap(ba))
    fist = [W[i] for i in range(len(W)) if own[i] in ("Hand_L", "Fist_L")]
    res["gap"] = round(min(bl.find_nearest(p)[3] for p in fist), 3)
    c = sum(fist, Vector()) / len(fist)
    res["fist_z"] = round(c.z, 3)
    res["chest_z"] = round((arm.matrix_world @ arm.pose.bones["Chest"].head).z, 3)
    res["fist_to_knee"] = round((c - (arm.matrix_world @ arm.pose.bones["Shin_L"].head)).length, 3)
    ev.to_mesh_clear()
    return res


grid = opts.get("grid", "full")
if grid == "cur":
    cands = [(-6, 14, 14)]
else:
    cands = list(itertools.product((-11, -6, -1, 4), (-6, 4, 14), (0, 15, 30)))
out = []
for o, fw, b in cands:
    row = {"out": o, "fwd": fw, "bend": b}
    for f in frames:
        row[f] = measure(f, o, fw, b)
    out.append(row)
    print("ARMROW " + json.dumps(row), flush=True)
print("ARMSEARCH done %d" % len(out))
