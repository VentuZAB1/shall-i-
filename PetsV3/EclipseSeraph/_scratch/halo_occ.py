# blender -b --factory-startup --python EclipseSeraph/_scratch/halo_occ.py -- <Name> <clip> <f0> <f1> [view=game]
# (builder D scratch) share of the Halo bone's camera-facing vertices hidden by ANOTHER part (ray from the camera to
# each halo vertex; self-hidden halo verts are skipped) per frame, plus the bone that hides the most
import sys, runpy, json
from collections import Counter
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, f0, f1 = argv[0], argv[1], int(argv[2]), int(argv[3])
view = argv[4] if len(argv) > 4 else "game"
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from mathutils.bvhtree import BVHTree
R3["full"](name, save=False)
k = R3["STATE"]["k"]
pk = R3["pk"]
body = k.main
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
halo_idx = [i for i, o in enumerate(owner) if o == "Halo"]
k.set_action(clip)
out = {}
for f in range(f0, f1 + 1):
    bpy.context.scene.frame_set(f)
    cam, _ = pk.camera_for(k, view)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    em = ev.to_mesh()
    em.calc_loop_triangles()
    co = [ev.matrix_world @ v.co for v in em.vertices]
    tris = [tuple(t.vertices) for t in em.loop_triangles]
    T = BVHTree.FromPolygons(co, [list(t) for t in tris], all_triangles=True)
    vis = hid = 0
    by = Counter()
    nr = [ev.matrix_world.to_3x3() @ v.normal for v in em.vertices]
    for i in halo_idx:
        p = co[i]
        d = p - cam
        if nr[i].dot(d) >= 0:                 # faces away from the camera
            continue
        L = d.length
        loc, nrm, fi, dist = T.ray_cast(cam, d.normalized(), L + 0.01)
        if loc is None:
            continue
        o = owner[tris[fi][0]]
        if dist >= L - 0.012:
            vis += 1
        elif o == "Halo":
            continue
        else:
            hid += 1
            by[o] += 1
    ev.to_mesh_clear()
    out[f] = [round(100.0 * hid / max(1, vis + hid), 1), by.most_common(2)]
print("HALO_OCC " + json.dumps(out))
