# blender -b --factory-startup --python PermafrostTitan/_scratch/kneel_vis.py -- [tag]
# r10 (side-on kneel): on the FIXED game camera (pk.camera_for(k, "game") at f0, as arm_search.py) measure for
# act_kneelrise:
#   vis_<bone> at f30 / f40 / f50 : share of the bone's verts the camera sees (ray cast; same test as arm_search.py)
#   knee_band                     : lowest point of the kneeling knee (Shin_L verts within 0.12 of the Knee_L joint)
#                                   over f18-52 (min, max), and the frame the knee first reaches z <= 0 (landing)
#   foot_r                        : the standing ankle (Foot_R head) xy drift while planted (f18-52) and its min z
#   arm_leg                       : face overlaps Fore_L / Hand_L / Fist_L / Arm_L vs Leg_L / Shin_L, and the right
#                                   arm vs Leg_R / Shin_R, over f8-64 (count of frames with overlap)
#   ground                        : lowest mesh point over the act
#   ang                           : max matrix_basis angle of Chest (chest vs spine) and Head (head vs chest)
import sys, runpy, json, math, os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
tag = argv[0] if argv else os.environ.get("TITAN_YAW", "30")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
pk = R3["pk"]
R3["full"]("PermafrostTitan", save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
arm = k.arm
k.set_action("act_kneelrise")
sc.frame_set(0)
loc, tgt = pk.camera_for(k, "game")
cam = Vector(loc)
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]


def mesh():
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    W = [mw @ v.co for v in me.vertices]
    polys = [list(p.vertices) for p in me.polygons]
    ev.to_mesh_clear()
    pown = []
    for pl in polys:
        c = {}
        for i in pl:
            c[own[i]] = c.get(own[i], 0) + 1
        pown.append(max(c, key=c.get))
    return W, polys, pown


out = {"tag": tag, "vis": {}, "occ": {}}
for f in (30, 40, 50):
    sc.frame_set(f)
    W, polys, pown = mesh()
    full = BVHTree.FromPolygons(W, polys)
    out["vis"][f] = {}
    for grp in ("Leg_L", "Shin_L", "Foot_L"):
        ids = [i for i in range(len(W)) if own[i] == grp]
        vis, occ = 0, {}
        for i in ids:
            d = W[i] - cam
            h = full.ray_cast(cam, d.normalized(), d.length + 0.01)
            if h[0] is None or h[3] >= d.length - 0.004 or pown[h[2]] == grp:
                vis += 1
            else:
                occ[pown[h[2]]] = occ.get(pown[h[2]], 0) + 1
        out["vis"][f][grp] = round(vis / max(1, len(ids)), 3)
        out["occ"]["%d_%s" % (f, grp)] = dict(sorted(occ.items(), key=lambda x: -x[1])[:4])
# knee band, standing foot, collisions, ground, angles over the act
kneeJ = k.J["Knee_L"]
knee_ids = None
band, land = [], None
fr0 = None
drift = 0.0
footz = 9.0
coll = {"L": [], "R": []}
gmin = (9.0, -1)
ang = {"Chest": (0.0, 0), "Head": (0.0, 0)}
n = k.clips["act_kneelrise"][0]
for f in range(0, n + 1):
    sc.frame_set(f)
    W, polys, pown = mesh()
    z = min(p.z for p in W)
    if z < gmin[0]:
        gmin = (round(z, 4), f)
    for b in ang:
        a = math.degrees(arm.pose.bones[b].matrix_basis.to_quaternion().angle)
        if a > ang[b][0]:
            ang[b] = (round(a, 2), f)
    kj = arm.matrix_world @ arm.pose.bones["Knee_L"].head
    if knee_ids is None:
        knee_ids = [i for i in range(len(W)) if own[i] == "Shin_L" and (W[i] - kj).length < 0.14]
    kz = min(W[i].z for i in knee_ids)
    if 18 <= f <= 52:
        band.append(kz)
    if land is None and f >= 8 and kz <= 0.0:
        land = f
    fa = arm.matrix_world @ arm.pose.bones["Foot_R"].head
    if 18 <= f <= 52:
        if fr0 is None:
            fr0 = fa.copy()
        drift = max(drift, (Vector((fa.x - fr0.x, fa.y - fr0.y, 0))).length)
        footz = min(footz, min(W[i].z for i in range(len(W)) if own[i] == "Foot_R"))
    if 8 <= f <= 64:
        for s, armset, legset in (("L", ("Fore_L", "Hand_L", "Fist_L", "Arm_L"), ("Leg_L", "Shin_L")),
                                  ("R", ("Fore_R", "Hand_R", "Fist_R", "Arm_R"), ("Leg_R", "Shin_R"))):
            lp = [pl for pl, o in zip(polys, pown) if o in legset]
            ap = [pl for pl, o in zip(polys, pown) if o in armset]
            if lp and ap and BVHTree.FromPolygons(W, lp).overlap(BVHTree.FromPolygons(W, ap)):
                coll[s].append(f)
out["knee_band_f18_52"] = [round(min(band), 4), round(max(band), 4)]
out["knee_lands_f"] = land
out["foot_r_drift_f18_52"] = round(drift, 4)
out["foot_r_minz_f18_52"] = round(footz, 4)
out["arm_leg_overlap_frames"] = coll
out["ground_min"] = gmin
out["ang"] = ang
print("KNEELVIS " + json.dumps(out))
open(os.path.join(k.dir, "_scratch", "kneel_vis_%s.json" % tag), "w").write(json.dumps(out, indent=1))
