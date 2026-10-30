# blender -b --factory-startup --python EclipseSeraph/_scratch/rod_metric.py -- <clip:f,...> [view=game]
# (builder D scratch) "rod or fan" for the upper wings from the view camera, on the REAL clip frames: the camera-facing
# vertices of Wing_A_<s> + WingTip_A_<s> that are visible (ray test), projected to the image plane; PCA of that 2D
# cloud -> major / minor std (minor = the visible width of the blade; a rod has a small minor) + visible count.
import sys, runpy, json, math
argv = sys.argv[sys.argv.index("--") + 1:]
picks = [(t.rsplit(":", 1)[0], int(t.rsplit(":", 1)[1])) for t in argv[0].split(",")]
view = argv[1] if len(argv) > 1 else "game"
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"]("EclipseSeraph", save=False)
k = R3["STATE"]["k"]
pk = R3["pk"]
import bpy
from mathutils.bvhtree import BVHTree
pk.stage(k)
body = k.main
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
sets = {s: [i for i, o in enumerate(owner) if o in ("Wing_A_" + s, "WingTip_A_" + s)] for s in ("L", "R")}
mane = [i for i, o in enumerate(owner) if o == "Mane"]
out = {}
for clip, f in picks:
    k.set_action(clip)
    bpy.context.scene.frame_set(f)
    cam, tgt = pk.camera_for(k, view)
    fwd = (tgt - cam).normalized(); right = fwd.cross((0, 0, 1)).normalized(); up = right.cross(fwd)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    em = ev.to_mesh(); em.calc_loop_triangles()
    co = [ev.matrix_world @ v.co for v in em.vertices]
    nr = [ev.matrix_world.to_3x3() @ v.normal for v in em.vertices]
    tris = [tuple(t.vertices) for t in em.loop_triangles]
    T = BVHTree.FromPolygons(co, [list(t) for t in tris], all_triangles=True)
    row = {}
    for s, idx in sets.items():
        bones = ("Wing_A_" + s, "WingTip_A_" + s)
        pts = []
        for i in idx:
            d = co[i] - cam
            if nr[i].dot(d) >= 0:
                continue
            L = d.length
            loc, n_, fi, dist = T.ray_cast(cam, d.normalized(), L + 0.01)
            if loc is not None and (dist >= L - 0.012 or owner[tris[fi][0]] in bones):
                z = d.dot(fwd)
                pts.append((d.dot(right) / z, d.dot(up) / z))
        if len(pts) < 3:
            row[s] = {"vis": len(pts)}
            continue
        mx = sum(p[0] for p in pts) / len(pts); my = sum(p[1] for p in pts) / len(pts)
        sxx = sum((p[0] - mx) ** 2 for p in pts) / len(pts); syy = sum((p[1] - my) ** 2 for p in pts) / len(pts)
        sxy = sum((p[0] - mx) * (p[1] - my) for p in pts) / len(pts)
        tr, det = sxx + syy, sxx * syy - sxy * sxy
        l1 = tr / 2 + math.sqrt(max(0.0, tr * tr / 4 - det)); l2 = tr / 2 - math.sqrt(max(0.0, tr * tr / 4 - det))
        row[s] = {"vis": len(pts), "major": round(1000 * math.sqrt(l1), 1), "minor": round(1000 * math.sqrt(max(l2, 0)), 1)}
    em = None
    ev.to_mesh_clear()
    mf = mv = 0
    for i in mane:                                  # the share of the camera-facing Mane verts that are visible
        d = co[i] - cam
        if nr[i].dot(d) >= 0:
            continue
        mf += 1
        L = d.length
        loc, n_, fi, dist = T.ray_cast(cam, d.normalized(), L + 0.01)
        if loc is not None and (dist >= L - 0.012 or owner[tris[fi][0]] == "Mane"):
            mv += 1
    row["mane_vis"] = round(mv / max(1, mf), 3)
    out["%s:%d" % (clip, f)] = row
print("ROD " + json.dumps(out))
