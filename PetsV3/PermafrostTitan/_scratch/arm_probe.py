# blender -b --factory-startup --python PermafrostTitan/_scratch/arm_probe.py -- <Name> [clips=idle,walk] [step=2]
# r5 MC2' / MC3' check per clip:
#   travel_f0_f30 : fist centre (Hand_X + Fist_X verts) displacement f0 -> f30 (BU), per side
#   range         : the largest distance between any two sampled fist centres in the clip (BU), per side
#   min_gap       : the smallest SURFACE gap (BVH) from that side's fist + hand verts to the faces of Leg_L / Leg_R /
#                   Shin_L / Shin_R, over all sampled frames, with the frame it happens at
import sys, runpy, json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
clips = opts.get("clips", "idle,walk").split(",")
step = int(opts.get("step", "2"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]
LEGS = ("Leg_L", "Leg_R", "Shin_L", "Shin_R")
out = {}
for clip in clips:
    k.set_action(clip)
    n, loop = k.clips[clip]
    cen = {"L": {}, "R": {}}
    gap = {"L": (9.0, -1, ""), "R": (9.0, -1, "")}
    for f in range(0, n + 1, step):
        bpy.context.scene.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        ev = k.main.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        W = [mw @ v.co for v in me.vertices]
        for leg in LEGS:
            ids = set(i for i in range(len(W)) if own[i] == leg)
            polys = [list(pl.vertices) for pl in me.polygons if all(v in ids for v in pl.vertices)]
            bvh = BVHTree.FromPolygons(W, polys)
            for side in ("L", "R"):
                fist = [W[i] for i in range(len(W)) if own[i] in ("Hand_" + side, "Fist_" + side)]
                d = min(bvh.find_nearest(p)[3] for p in fist)
                if d < gap[side][0]:
                    gap[side] = (round(d, 3), f, leg)
        for side in ("L", "R"):
            fist = [W[i] for i in range(len(W)) if own[i] in ("Hand_" + side, "Fist_" + side)]
            cen[side][f] = sum(fist, Vector()) / len(fist)
        ev.to_mesh_clear()
    res = {}
    for side in ("L", "R"):
        c = cen[side]
        fs = sorted(c)
        rng = max((c[a] - c[b]).length for a in fs for b in fs)
        res[side] = {"travel_f0_f30": round((c[30] - c[0]).length, 3) if 30 in c else None, "range": round(rng, 3),
                     "min_gap": gap[side]}
    out[clip] = res
print("ARMPROBE " + json.dumps(out))
