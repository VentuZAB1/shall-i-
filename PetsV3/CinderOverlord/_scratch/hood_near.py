# blender -b ... hood_near.py -- CinderOverlord clip:frame [B=Head]  -> the closest HOOD vertex / B surface point
import sys, runpy, json
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
clip, fr = argv[1].split(":")
opts = dict(a.split("=", 1) for a in argv[2:] if "=" in a)
BG = opts.get("B", "Head")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]
rest = [k.main.matrix_world @ v.co for v in k.main.data.vertices]
hood = [i for i, g in enumerate(own) if (g == "Neck2" and abs(rest[i].x) > 0.25) or (g == "Neck3" and abs(rest[i].x) > 0.215)]
k.set_action(clip)
sc.frame_set(int(fr))
dg = bpy.context.evaluated_depsgraph_get()
ev = k.main.evaluated_get(dg)
me = ev.to_mesh()
me.calc_loop_triangles()
co = [ev.matrix_world @ v.co for v in me.vertices]
tb = [list(t.vertices) for t in me.loop_triangles if own[t.vertices[0]] == BG]
T = BVHTree.FromPolygons(co, tb, all_triangles=True)
best = None
for i in hood:
    q, n, _, d = T.find_nearest(co[i])
    if best is None or d < best[0]:
        best = (d, i, co[i], q)
res = []
for d, i, p, q in [best]:
    res.append({"d": round(d, 4), "hood_rest": [round(c, 3) for c in rest[i]], "hood_now": [round(c, 3) for c in p],
                "B_pt": [round(c, 3) for c in q]})
# also how many hood verts within 0.02
near = sum(1 for i in hood if T.find_nearest(co[i])[3] < 0.02)
print("HOODNEAR " + json.dumps({"best": res, "n_within_0.02": near}))
