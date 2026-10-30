# blender -b --factory-startup --python GlacierYeti/_scratch/hinge_where.py -- <Name> <clip> <frame> <BoneA|BoneB>
# Like _tools/collide_where.py but WITH the joints() hinges applied (the same filter as overlap_report): prints the
# crossing points (posed world) and rest centroids of the triangle pairs that survive the hinge filter.
import sys, runpy
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, frame, pair = argv[0], argv[1], int(argv[2]), argv[3]
A, Bn = pair.split("|")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from mathutils.bvhtree import BVHTree
bk = R3["blockkit"]
R3["full"](name, save=False)
k, m = R3["STATE"]["k"], R3["STATE"]["m"]
arm, body = k.arm, k.main
me = body.data
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in me.vertices]
rest = [v.co.copy() for v in me.vertices]
J = []
for a, b, r, bn in m.joints():
    a2, hs = bk.head_point(k, bn, a)
    b2, _ = bk.head_point(k, bn, b)
    J.append((a2, b2, r * hs, bn))


def pj():
    out = []
    for a, b, r, bn in J:
        pbn = arm.pose.bones[bn]
        M = arm.matrix_world @ pbn.matrix @ arm.data.bones[bn].matrix_local.inverted()
        out.append((M @ a, M @ b, r))
    return out


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
    joints = pj()
    out = {}
    for x, y in T[A].overlap(T[Bn]):
        pts = bk._tri_hits([co[i] for i in tl[A][x]], [co[i] for i in tl[Bn][y]])
        if not pts:
            continue
        if all(any(bk._seg_dist(p, j0, j1) < r for j0, j1, r in joints) for p in pts):
            continue
        out[(tl[A][x], tl[Bn][y])] = pts
    return out


arm.data.pose_position = "REST"
bpy.context.view_layer.update()
base = set(hits())
arm.data.pose_position = "POSE"
k.set_action(clip)
bpy.context.scene.frame_set(frame)
cur = hits()
new = {kk: v for kk, v in cur.items() if kk not in base}
print("HINGE_WHERE %s %s %d surviving pairs %d" % (pair, clip, frame, len(new)))
seen = set()
for (ta, tb), pts in new.items():
    pa = tuple(round(v, 2) for v in sum((rest[i] for i in ta), Vector()) / 3)
    pb = tuple(round(v, 2) for v in sum((rest[i] for i in tb), Vector()) / 3)
    pw = tuple(round(v, 3) for v in sum(pts, Vector()) / len(pts))
    key = (pa, pb)
    if key in seen:
        continue
    seen.add(key)
    print("HINGE_WHERE  A rest %s | B rest %s | posed crossing %s" % (pa, pb, pw))
