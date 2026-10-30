# blender -b --factory-startup --python EclipseSeraph/_scratch/vis_cands.py -- <json> <bones,comma> [view=tq]
# (builder D scratch) six-wing candidates (pose_cands2 json, per-side keys allowed) -> how many camera-facing verts of
# the given bones are VISIBLE from the view camera (ray test), their screen-space spread, and cut-throughs. No renders.
import sys, runpy, os, json
argv = sys.argv[sys.argv.index("--") + 1:]
cands = json.load(open(argv[0]))
bones = set(argv[1].split(","))
view = argv[2] if len(argv) > 2 else "tq"
name = "EclipseSeraph"
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from mathutils.bvhtree import BVHTree
m = R3["spec"](name)
k = R3["new_pet"](m, name)
m.model(k)
m.rig(k)
k.build_rig()
pk = R3["pk"]
for lab in cands:
    k.new_action("c_" + lab, 2, False)
    for f in (0, 2):
        for P, w in cands[lab].items():
            if "_" not in P:
                m.wings(k, f, P, *w)
        for P, w in cands[lab].items():
            if "_" in P:
                pp, sd = P.split("_")
                m.wings(k, f, pp, *w, side=sd)
    k.finish(loop=False)
pk.stage(k)
body = k.main
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
idx = [i for i, o in enumerate(owner) if o in bones]
pairs = m.check_pairs()
js = m.joints()
out = {}
for lab in cands:
    k.set_action("c_" + lab)
    bpy.context.scene.frame_set(0)
    cam, tgt = pk.camera_for(k, view)
    fwd = (tgt - cam).normalized()
    right = fwd.cross((0, 0, 1)).normalized()
    up = right.cross(fwd)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    em = ev.to_mesh()
    em.calc_loop_triangles()
    co = [ev.matrix_world @ v.co for v in em.vertices]
    nr = [ev.matrix_world.to_3x3() @ v.normal for v in em.vertices]
    tris = [tuple(t.vertices) for t in em.loop_triangles]
    T = BVHTree.FromPolygons(co, [list(t) for t in tris], all_triangles=True)
    vis = []
    for i in idx:
        d = co[i] - cam
        if nr[i].dot(d) >= 0:
            continue
        L = d.length
        loc, n_, fi, dist = T.ray_cast(cam, d.normalized(), L + 0.01)
        if loc is not None and (dist >= L - 0.012 or owner[tris[fi][0]] in bones):
            vis.append(co[i])
    xs = [round((p - cam).dot(right) / (p - cam).dot(fwd), 3) for p in vis]
    ev.to_mesh_clear()
    rep = R3["blockkit"].overlap_report(k, pairs, step=1, clips=["c_" + lab], frames={"c_" + lab: [0]}, joints=js)
    out[lab] = {"visible": len(vis), "x_min": min(xs) if xs else None,
                "cuts": {kk: v[0] for kk, v in rep.get("c_" + lab, {}).items() if v[0]}}
print("VIS " + json.dumps(out))
