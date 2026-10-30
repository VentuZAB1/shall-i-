import sys, os, json
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\TPTrees")
sys.argv = ["x"]
import tptree as T
import bpy, numpy as np
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath=T.TREE_BLEND)
ob = bpy.data.objects["TP"]
me = ob.data
me.calc_loop_triangles()
uv = me.uv_layers.active.data
V = np.array([v.co[:] for v in me.vertices])
tris = [(lt.loops[:], lt.vertices[:]) for lt in me.loop_triangles]
UVt = np.array([[uv[l].uv[:] for l in L] for L, Vv in tris])  # (n,3,2)
Vt = np.array([[V[i] for i in Vv] for L, Vv in tris])
e1 = UVt[:, 1] - UVt[:, 0]; e2 = UVt[:, 2] - UVt[:, 0]
area = np.abs(e1[:, 0] * e2[:, 1] - e1[:, 1] * e2[:, 0])
good = area > 1e-9
UVt, Vt = UVt[good], Vt[good]
img = bpy.data.images.load(os.path.join(T.MAPS, "TPTree_TP_normal.png"))
H = img.size[1]
im = np.array(img.pixels[:], np.float32).reshape(H, H, 4)[::-1, :, :3]
bad = np.argwhere(im[..., 2] < 0.62)   # tangent z < 0.24
print("bad texels", len(bad))
rng = np.random.default_rng(1)
pick = bad[rng.choice(len(bad), min(400, len(bad)), replace=False)]
pts = []
for (r, c) in pick:
    u, v = (c + 0.5) / H, 1 - (r + 0.5) / H
    a, b, cc = UVt[:, 0], UVt[:, 1], UVt[:, 2]
    v0, v1 = b - a, cc - a
    v2 = np.array([u, v]) - a
    d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1)
    d20 = (v2 * v0).sum(1); d21 = (v2 * v1).sum(1)
    den = d00 * d11 - d01 * d01
    den[np.abs(den) < 1e-14] = 1e-14
    bv = (d11 * d20 - d01 * d21) / den
    bw = (d00 * d21 - d01 * d20) / den
    bu = 1 - bv - bw
    ok = np.nonzero((bu >= -1e-3) & (bv >= -1e-3) & (bw >= -1e-3))[0]
    if len(ok):
        t = ok[0]
        p = Vt[t, 0] * bu[t] + Vt[t, 1] * bv[t] + Vt[t, 2] * bw[t]
        pts.append(p)
pts = np.array(pts)
print("mapped", len(pts))
# cluster report: z histogram + nearest canopy/trunk distance
from mathutils.bvhtree import BVHTree
def bv(name):
    o = bpy.data.objects[name]; o.data.calc_loop_triangles()
    VV = [v.co[:] for v in o.data.vertices]; TT = [lt.vertices[:] for lt in o.data.loop_triangles]
    return BVHTree.FromPolygons(VV, TT)
bc = [bv("CanopyA"), bv("CanopyB")]; bt = bv("Trunk")
hiT = bv("TPHi")
import collections
cnt = collections.Counter()
for p in pts:
    P = Vector(p.tolist())
    dc = min(b.find_nearest(P)[3] for b in bc)
    dt = bt.find_nearest(P)[3]
    loc, n, i, dh = hiT.find_nearest(P)
    cnt[("canopy<0.15" if dc < 0.15 else "free") + ("|trunk<0.15" if dt < 0.15 else "")] += 1
print(cnt)
np.save(os.path.join(T.WIP, "blotch_pts.npy"), pts)
print("zrange", pts[:, 2].min(), pts[:, 2].max())
print(np.round(pts[:40], 2))
# which ribbon: nearest TP low triangle -> which y row; also: distance to the nearest OTHER part of the TP low

