# blender -b --factory-startup --python _tools/collide_where.py -- <Name> <clip> <frame> <BoneA|BoneB>
# Where do two bones' parts cut through each other at one frame? Prints REST-space centroids of the colliding
# triangles of each side (so you know which block to move/shrink), ignoring contacts already present at rest.
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


def trees():
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
    return T, tl, co


def hits():
    T, tl, co = trees()
    out = set()
    for x, y in T[A].overlap(T[Bn]):
        if bk._tri_hits([co[i] for i in tl[A][x]], [co[i] for i in tl[Bn][y]]):
            out.add((tl[A][x], tl[Bn][y]))
    return out


arm.data.pose_position = "REST"
bpy.context.view_layer.update()
base = hits()
arm.data.pose_position = "POSE"
k.set_action(clip)
bpy.context.scene.frame_set(frame)
new = hits() - base
ca = {}
cb = {}
for ta, tb in new:
    pa = sum((rest[i] for i in ta), Vector()) / 3
    pb = sum((rest[i] for i in tb), Vector()) / 3
    ca[tuple(round(v, 2) for v in pa)] = 1
    cb[tuple(round(v, 2) for v in pb)] = 1
print("COLLIDE", pair, clip, frame, "pairs", len(new))
print("COLLIDE", A, "rest centroids:", list(ca)[:12])
print("COLLIDE", Bn, "rest centroids:", list(cb)[:12])
