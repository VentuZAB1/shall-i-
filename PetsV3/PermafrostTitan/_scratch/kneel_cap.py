# blender -b --factory-startup --python PermafrostTitan/_scratch/kneel_cap.py -- <tag> [f=40]
# r10: what is the BEST vert share any camera could see? For Leg_L / Shin_L / Foot_L at frame f:
#   buried   : share of the part's verts that sit INSIDE another part's closed block (nearest face of the other
#              parts, outward normal test) - those are hidden from every camera
#   game     : the arm_search.py vert share, but from the REAL game camera (camera_for loc, not the stale
#              matrix_world at the origin that arm_search.py read)
#   sweep    : the same share from 24 cameras around the kneeling knee (every 15 deg azimuth) at the game
#              camera's elevation and distance; best / its azimuth (0 = the game camera's azimuth)
import sys, runpy, json, math, os
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
tag = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
F = int(opts.get("f", "40"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
pk = R3["pk"]
R3["full"]("PermafrostTitan", save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
k.set_action("act_kneelrise")
sc.frame_set(0)
loc, tgt = pk.camera_for(k, "game")
loc, tgt = Vector(loc), Vector(tgt)
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]
sc.frame_set(F)
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
full = BVHTree.FromPolygons(W, polys)
PARTS = ("Leg_L", "Shin_L", "Foot_L")
others = {b: BVHTree.FromPolygons(W, [pl for pl, o in zip(polys, pown) if o != b]) for b in PARTS}
ids = {b: [i for i in range(len(W)) if own[i] == b] for b in PARTS}


OCC = {}


def vis(cam, b, occ=None):
    n = 0
    for i in ids[b]:
        d = W[i] - cam
        h = full.ray_cast(cam, d.normalized(), d.length + 0.01)
        if h[0] is None or h[3] >= d.length - 0.004 or pown[h[2]] == b:
            n += 1
        elif occ is not None:
            occ[pown[h[2]]] = occ.get(pown[h[2]], 0) + 1
    return round(n / max(1, len(ids[b])), 3)


out = {"tag": tag, "f": F, "buried": {}, "game": {}, "sweep": {}}
for b in PARTS:
    bur = 0
    for i in ids[b]:
        h = others[b].find_nearest(W[i])
        if h[0] is not None and h[3] < 0.06 and (W[i] - h[0]).dot(h[1]) < -1e-4:
            bur += 1
    out["buried"][b] = round(bur / max(1, len(ids[b])), 3)
    OCC[b] = {}
    out["game"][b] = vis(loc, b, OCC[b])
    out.setdefault("occ", {})[b] = dict(sorted(OCC[b].items(), key=lambda x: -x[1])[:4])
    out.setdefault("nverts", {})[b] = len(ids[b])
knee = k.arm.matrix_world @ k.arm.pose.bones["Knee_L"].head
kn_ids = [i for i in ids["Shin_L"] if (W[i] - knee).length < 0.14]
out["knee_z"] = round(min(W[i].z for i in kn_ids), 4) if kn_ids else None
_kn2 = [i for i in range(len(W)) if own[i] in ("Leg_L", "Shin_L", "Knee_L") and (W[i] - knee).length < 0.20]
_ki = min(_kn2, key=lambda i: W[i].z)
out["knee_any"] = [round(W[_ki].z, 4), own[_ki], round((W[_ki] - knee).length, 3)]
out["knee_joint_z"] = round(knee.z, 4)
_gi = min(range(len(W)), key=lambda i: W[i].z)
out["ground"] = [round(W[_gi].z, 4), own[_gi]]
out["armleg"] = len(BVHTree.FromPolygons(W, [pl for pl, o in zip(polys, pown) if o in ("Leg_L", "Shin_L")]).overlap(
    BVHTree.FromPolygons(W, [pl for pl, o in zip(polys, pown) if o in ("Arm_L", "Fore_L", "Hand_L", "Fist_L")])))
d = loc - tgt
r_xy = Vector((d.x, d.y)).length
az0 = math.atan2(d.y, d.x)
for b in PARTS:
    best = (0, 0)
    row = []
    for s in range(24):
        a = az0 + math.radians(15 * s)
        cam = knee + Vector((r_xy * math.cos(a), r_xy * math.sin(a), d.z))
        v = vis(cam, b)
        row.append(v)
        if v > best[0]:
            best = (v, 15 * s)
    out["sweep"][b] = {"best": best[0], "best_az": best[1], "all": row}
print("KNEELCAP " + json.dumps({kk: vv for kk, vv in out.items() if kk not in ("sweep",)}) + " SWEEP " +
      json.dumps({b: (out["sweep"][b]["best"], out["sweep"][b]["best_az"]) for b in PARTS}))
open(os.path.join(k.dir, "_scratch", "kneel_cap_%s.json" % tag), "w").write(json.dumps(out, indent=1))
