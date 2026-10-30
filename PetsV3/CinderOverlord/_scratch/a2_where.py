# blender -b --factory-startup --python CinderOverlord/_scratch/a2_where.py -- CinderOverlord "A|B@clip:f;..."
# For a proxy-free crossing (A2), are the crossing points buried inside a THIRD bone group's solid (= hidden
# interior junction overlap) or out in the open (= a visible cut)? Inside test: nearest surface point of that group,
# (p - q) . normal < 0. Also the crossing region's spread vs the same pair at rest (a fixed seated contact vs a cut).
import sys, runpy, json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
jobs = []
for t in argv[1].split(";"):
    pr, cf = t.split("@")
    c, f = cf.split(":")
    jobs.append((pr.split("|"), c, int(f)))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
bk = R3["blockkit"]
R3["full"](name, save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
names = {g.index: g.name for g in k.main.vertex_groups}
own = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in k.main.data.vertices]
res = {}
for (A, Bn), clip, f in jobs:
    k.set_action(clip)
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    em = ev.to_mesh()
    em.calc_loop_triangles()
    co = [ev.matrix_world @ v.co for v in em.vertices]
    by = {}
    for t in em.loop_triangles:
        by.setdefault(own[t.vertices[0]], []).append(list(t.vertices))
    ev.to_mesh_clear()
    T = {g: BVHTree.FromPolygons(co, tl, all_triangles=True) for g, tl in by.items() if g}
    ta, tb = by[A], by[Bn]
    pts = []
    for x, y in T[A].overlap(T[Bn]):
        pts += bk._tri_hits([co[i] for i in ta[x]], [co[i] for i in tb[y]])
    inside = 0
    where = {}
    for p in pts:
        hit = None
        for g, t in T.items():
            if g in (A, Bn):
                continue
            q, n, _, d = t.find_nearest(p)
            if q is not None and (p - q).dot(n) < 0:
                hit = g
                break
        if hit:
            inside += 1
            where[hit] = where.get(hit, 0) + 1
    res["%s|%s@%s:%d" % (A, Bn, clip, f)] = {"cross": len(pts), "buried": inside, "in": where}
print("A2WHERE " + json.dumps(res))
