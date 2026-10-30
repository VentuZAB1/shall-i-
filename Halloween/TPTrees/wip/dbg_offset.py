import sys, os, json, math
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\TPTrees")
sys.argv = ["x"]
import tptree as T
import bpy, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

bpy.ops.wm.open_mainfile(filepath=T.TREE_BLEND)
lo = bpy.data.objects["TP"]
lo.data.calc_loop_triangles()
bl = BVHTree.FromPolygons([v.co[:] for v in lo.data.vertices], [lt.vertices[:] for lt in lo.data.loop_triangles])
for name in ("TPHi_00", "TPHi_05", "TPHi_01"):
    hi = bpy.data.objects[name]
    Vh = np.array([v.co[:] for v in hi.data.vertices])
    nring = (len(Vh)) // 18
    top = Vh[: nring * 18].reshape(nring, 18, 3)[:, 4]       # top centre of every hi section
    bot = Vh[: nring * 18].reshape(nring, 18, 3)[:, 13]      # bottom centre
    nn = top - bot
    nn /= np.linalg.norm(nn, axis=1, keepdims=True)
    d = []
    for i in range(nring):
        loc, n, idx, dist = bl.find_nearest(Vector(top[i].tolist()), 0.5)
        d.append(9 if loc is None else (Vector(top[i].tolist()) - loc).dot(Vector(nn[i].tolist())))
    d = np.array(d)
    big = np.nonzero(np.abs(d) > 0.03)[0]
    print(name, "sections", nring, "max |top offset|", round(float(np.abs(d).max()), 4),
          "n>0.03:", len(big), "first idx", big[:30].tolist())
    if len(big):
        i = big[0]
        print("   at", np.round(top[i], 3), "offsets around:", np.round(d[max(0, i - 6): i + 7], 3).tolist())
        # section spacing of the hi around there
        sp = np.linalg.norm(np.diff(Vh[: nring * 18].reshape(nring, 18, 3)[:, 4], axis=0), axis=1)
        print("   hi spacing around:", np.round(sp[max(0, i - 6): i + 6], 4).tolist())
