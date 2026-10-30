# blender -b --factory-startup --python EclipseSeraph/_scratch/path6where.py -- <paths.json> <label> <frame> <A|B>
# (builder D scratch) rest-space centroids of the colliding triangles of a path6 path at one frame (cf collide_where)
import sys, runpy, json
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
paths = json.load(open(argv[0]))
lab, frame, (A, Bn) = argv[1], int(argv[2]), argv[3].split("|")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from mathutils.bvhtree import BVHTree
bk = R3["blockkit"]
m = R3["spec"]("EclipseSeraph")
k = R3["new_pet"](m, "EclipseSeraph")
m.model(k)
m.rig(k)
k.build_rig()
keys = paths[lab]
k.new_action("p_" + lab, keys[-1][0], False)
for f, d in keys:
    for b, v in d.items():
        if b in ("A", "B", "C"):
            m.wings(k, f, b, *v)
        elif len(v) >= 6:
            k.key(b, f, rot=tuple(v[:3]), loc=tuple(v[3:6]))
        else:
            k.key(b, f, rot=tuple(v[:3]))
k.bake_bezier_now()
arm, body = k.arm, k.main
me = body.data
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in me.vertices]
rest = [v.co.copy() for v in me.vertices]


def hits():
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    em = ev.to_mesh()
    em.calc_loop_triangles()
    co = [ev.matrix_world @ v.co for v in em.vertices]
    tl = {A: [], Bn: []}
    for t in em.loop_triangles:
        g = owner[t.vertices[0]]
        if g in tl:
            tl[g].append(tuple(t.vertices))
    T = {g: BVHTree.FromPolygons(co, [list(t) for t in tl[g]], all_triangles=True) for g in tl}
    ev.to_mesh_clear()
    out = set()
    for x, y in T[A].overlap(T[Bn]):
        if bk._tri_hits([co[i] for i in tl[A][x]], [co[i] for i in tl[Bn][y]]):
            out.add((tl[A][x], tl[Bn][y]))
    return out


arm.data.pose_position = "REST"
bpy.context.view_layer.update()
base = hits()
arm.data.pose_position = "POSE"
k.set_action("p_" + lab)
bpy.context.scene.frame_set(frame)
new = hits() - base
ca, cb = {}, {}
for ta, tb in new:
    ca[tuple(round(v, 2) for v in sum((rest[i] for i in ta), Vector()) / 3)] = 1
    cb[tuple(round(v, 2) for v in sum((rest[i] for i in tb), Vector()) / 3)] = 1
print("WHERE", A, Bn, lab, frame, "pairs", len(new))
print("WHERE", A, list(ca)[:10])
print("WHERE", Bn, list(cb)[:10])
