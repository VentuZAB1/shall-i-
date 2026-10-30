import bpy, sys, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
fbx = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=fbx)
objs = [o for o in bpy.context.scene.objects if o.type == "MESH" and not o.name.endswith(("_Web", "_WebSilk", "_Leaves", "_Branches"))]
V, P, off = [], [], 0
for o in objs:
    vs = [(o.matrix_world @ v.co) * 100 for v in o.data.vertices]
    V += vs; P += [[i + off for i in p.vertices] for p in o.data.polygons]; off += len(vs)
bvh = BVHTree.FromPolygons(V, P)
# rays along +-X and along diagonals through the face slab: y (Blender) -1.7..-0.5, z 3.0..5.6
hits = []
for dname, d in (("+X", Vector((1, 0, 0))), ("-X", Vector((-1, 0, 0))), ("diag(+X,+Y)", Vector((0.7, 0.7, 0)).normalized()), ("diag(-X,+Y)", Vector((-0.7, 0.7, 0)).normalized())):
    thr = []
    for y in np.arange(-1.7, -0.45, 0.05):
        for z in np.arange(3.0, 5.65, 0.05):
            # only rays that cross the trunk's outer envelope: test the trunk centreline distance
            org = Vector((0, y, z)) - d * 6
            h = bvh.ray_cast(org, d, 12)
            if h[0] is None:
                continue  # misses the trunk entirely (outside silhouette)
            # walk through: count entry/exit; a "tunnel" = ray enters, exits, and the gap before re-entry passes the trunk middle
            pts = []
            o2 = org
            for _ in range(12):
                h = bvh.ray_cast(o2, d, 12)
                if h[0] is None: break
                pts.append(h[0]); o2 = h[0] + d * 0.002
            # parity of crossings; a ray that crosses the trunk fully has >=2 hits; tunnel = an exit then re-entry with a gap > 0.15 inside the outer envelope
            for k in range(1, len(pts) - 1, 2):
                gap = (pts[k + 1] - pts[k]).length
                mid = (pts[k + 1] + pts[k]) / 2
                if gap > 0.15 and abs(mid.x) < 1.1:
                    thr.append((round(y, 2), round(z, 2), round(mid.x, 2), round(gap, 2)))
    if thr:
        a = np.array(thr)
        print("TUN", dname, "rays with an open gap inside the trunk envelope:", len(thr), "y range", a[:, 0].min(), a[:, 0].max(), "z range", a[:, 1].min(), a[:, 1].max())
        # cluster by z
        for lo in np.arange(3.0, 5.7, 0.25):
            s = a[(a[:, 1] >= lo) & (a[:, 1] < lo + 0.25)]
            if len(s): print("TUN    z %.2f-%.2f: %d rays, y %.2f..%.2f, gap mid x %.2f..%.2f" % (lo, lo + 0.25, len(s), s[:, 0].min(), s[:, 0].max(), s[:, 2].min(), s[:, 2].max()))
