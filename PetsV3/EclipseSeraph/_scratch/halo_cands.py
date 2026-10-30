# blender -b --factory-startup --python EclipseSeraph/_scratch/halo_cands.py -- <json> [views] [res]
# (builder D scratch) six-wing pose candidates (json {"label": {"A": [up,fwd,twist,tip], ...}}) -> halo share hidden by
# other parts from the GAME camera (camera-facing halo verts, ray test), cut-throughs, renders cand_<label>_<view>.png
import sys, runpy, os, json
from collections import Counter
argv = sys.argv[sys.argv.index("--") + 1:]
cands = json.load(open(argv[0]))
views = argv[1].split(",") if len(argv) > 1 else ["game", "tq"]
res = int(argv[2]) if len(argv) > 2 else 300
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
            m.wings(k, f, P, *w)
    k.finish(loop=False)
pk.stage(k)
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
body = k.main
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
halo_idx = [i for i, o in enumerate(owner) if o == "Halo"]
pairs = m.check_pairs()
js = m.joints()
out = {}
for lab in cands:
    k.set_action("c_" + lab)
    sc.frame_set(0)
    cam, _ = pk.camera_for(k, "game")
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    em = ev.to_mesh()
    em.calc_loop_triangles()
    co = [ev.matrix_world @ v.co for v in em.vertices]
    nr = [ev.matrix_world.to_3x3() @ v.normal for v in em.vertices]
    tris = [tuple(t.vertices) for t in em.loop_triangles]
    T = BVHTree.FromPolygons(co, [list(t) for t in tris], all_triangles=True)
    vis = hid = 0
    by = Counter()
    for i in halo_idx:
        d = co[i] - cam
        if nr[i].dot(d) >= 0:
            continue
        L = d.length
        loc, n_, fi, dist = T.ray_cast(cam, d.normalized(), L + 0.01)
        if loc is None:
            continue
        if dist >= L - 0.012:
            vis += 1
        elif owner[tris[fi][0]] != "Halo":
            hid += 1
            by[owner[tris[fi][0]]] += 1
    ev.to_mesh_clear()
    for v in views:
        loc, tgt = pk.camera_for(k, v)
        pk.aim(sc.camera, loc, tgt)
        sc.render.filepath = os.path.join(k.dir, "renders", "cand_%s_%s.png" % (lab, v))
        bpy.ops.render.render(write_still=True)
    rep = R3["blockkit"].overlap_report(k, pairs, step=1, clips=["c_" + lab], frames={"c_" + lab: [0]}, joints=js)
    out[lab] = {"halo_hidden_pct": round(100.0 * hid / max(1, vis + hid), 1), "by": by.most_common(2),
                "cuts": {kk: v[0] for kk, v in rep.get("c_" + lab, {}).items() if v[0]}}
print("HCANDS " + json.dumps(out))
