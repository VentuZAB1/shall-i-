import sys, os, json, math
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\TPTrees")
sys.argv = ["x"]
import tptree as T
import bpy, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

bpy.ops.wm.open_mainfile(filepath=T.TREE_BLEND)
ob = bpy.data.objects["TP"]
me = ob.data
me.calc_loop_triangles()
uv = me.uv_layers.active.data
V = np.array([v.co[:] for v in me.vertices])
NV = np.array([v.normal[:] for v in me.vertices])
tris = [(lt.loops[:], lt.vertices[:]) for lt in me.loop_triangles]
UVt = np.array([[uv[l].uv[:] for l in Lp] for Lp, Vv in tris])
VI = np.array([Vv for Lp, Vv in tris])
e1 = UVt[:, 1] - UVt[:, 0]
e2 = UVt[:, 2] - UVt[:, 0]
area = np.abs(e1[:, 0] * e2[:, 1] - e1[:, 1] * e2[:, 0])
good = area > 1e-9
UVt, VI = UVt[good], VI[good]
img = bpy.data.images.load(os.path.join(T.MAPS, "TPTree_TP_normal.png"))
H = img.size[1]
im = np.array(img.pixels[:], np.float32).reshape(H, H, 4)[::-1, :, :3]
bad = np.argwhere(im[..., 2] < 0.62)
rng = np.random.default_rng(3)
pick = bad[rng.choice(len(bad), 120, replace=False)]
his = [o for o in bpy.data.objects if o.name.startswith("TPHi_")]
hb = []
for o in his:
    o.data.calc_loop_triangles()
    hb.append((o.name, BVHTree.FromPolygons([v.co[:] for v in o.data.vertices],
                                            [lt.vertices[:] for lt in o.data.loop_triangles])))
stats = []
for (r, c) in pick:
    u, v = (c + 0.5) / H, 1 - (r + 0.5) / H
    a, b, cc = UVt[:, 0], UVt[:, 1], UVt[:, 2]
    v0, v1 = b - a, cc - a
    v2 = np.array([u, v]) - a
    d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1)
    d20 = (v2 * v0).sum(1); d21 = (v2 * v1).sum(1)
    den = d00 * d11 - d01 * d01
    bv = (d11 * d20 - d01 * d21) / den
    bw = (d00 * d21 - d01 * d20) / den
    bu = 1 - bv - bw
    ok = np.nonzero((bu >= -1e-4) & (bv >= -1e-4) & (bw >= -1e-4))[0]
    if not len(ok):
        continue
    t = ok[0]
    w = np.array([bu[t], bv[t], bw[t]])
    p = (V[VI[t]] * w[:, None]).sum(0)
    n = (NV[VI[t]] * w[:, None]).sum(0)
    n /= np.linalg.norm(n)
    fn = np.cross(V[VI[t][1]] - V[VI[t][0]], V[VI[t][2]] - V[VI[t][0]])
    fn /= np.linalg.norm(fn)
    o = Vector((p + n * 0.045).tolist())
    d = Vector((-n).tolist())
    best = None
    for name, b in hb:
        loc, hn, idx, dist = b.ray_cast(o, d, 0.075)
        if loc is not None and (best is None or dist < best[3]):
            best = (name, loc, hn, dist)
    # distance from the low point to the nearest hi surface + that normal
    near = None
    for name, b in hb:
        loc, hn, idx, dist = b.find_nearest(Vector(p.tolist()), 0.3)
        if loc is not None and (near is None or dist < near[3]):
            near = (name, loc, hn, dist)
    stats.append(dict(p=[round(x, 3) for x in p], n_dot_face=round(float(np.dot(n, fn)), 3),
                      hit=None if best is None else (best[0], round(best[3], 4), round(best[2].dot(Vector(n.tolist())), 3)),
                      near=None if near is None else (near[0], round(near[3], 4),
                                                      round(near[2].dot(Vector(n.tolist())), 3),
                                                      round((Vector(p.tolist()) - near[1]).dot(Vector(n.tolist())), 4))))
import collections
print("n samples", len(stats))
print("hit none", sum(1 for s in stats if s["hit"] is None))
print("hit backface", sum(1 for s in stats if s["hit"] and s["hit"][2] < 0))
print("smooth-vs-face normal dot < 0.9", sum(1 for s in stats if s["n_dot_face"] < 0.9))
for s in stats[:25]:
    print(s)
