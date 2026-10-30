"""Side-wall thickness of the HauntedTree face pockets + a see-through test.
For rays along +-X through the face slab, every gap (exit then re-entry) whose middle lies in the face (|x| < 1.1) is
a pocket crossed sideways: report the solid wall thickness on the ray's entry side.  See-through: rays from side
directions (60..120 deg off the face normal, horizontal and +-25 deg pitch) that start outside the trunk, pass through
the face slab and hit NOTHING although their closest approach to the trunk axis is < 0.9 * trunk radius."""
import bpy, sys, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
fbx = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=fbx)
objs = [o for o in bpy.context.scene.objects if o.type == "MESH" and o.name.endswith(("_Trunk", "_Limbs"))]
V, P, off = [], [], 0
for o in objs:
    vs = [(o.matrix_world @ v.co) * 100 for v in o.data.vertices]
    V += vs; P += [[i + off for i in p.vertices] for p in o.data.polygons]; off += len(vs)
bvh = BVHTree.FromPolygons(V, P)
walls = []
for d in (Vector((1, 0, 0)), Vector((-1, 0, 0))):
    for y in np.arange(-1.85, -0.45, 0.05):
        for z in np.arange(3.0, 5.65, 0.05):
            o2 = Vector((0, y, z)) - d * 6
            pts = []
            for _ in range(12):
                h = bvh.ray_cast(o2, d, 12)
                if h[0] is None:
                    break
                pts.append(h[0]); o2 = h[0] + d * 0.002
            gaps = [k for k in range(1, len(pts) - 1, 2)
                    if (pts[k + 1] - pts[k]).length > 0.15 and abs(((pts[k + 1] + pts[k]) / 2).x) < 1.1]
            if gaps:
                # OUTER walls only: from the outside entry to the first face pocket, and from the last pocket out
                walls.append(((pts[gaps[0]] - pts[gaps[0] - 1]).length, y, z))
                walls.append(((pts[gaps[-1] + 2] - pts[gaps[-1] + 1]).length if gaps[-1] + 2 < len(pts) else 9.0, y, z))
w = np.array(walls)
if len(w):
    print("WALL pockets crossed sideways: %d rays; side wall min %.3f p5 %.3f median %.3f" % (
        len(w), w[:, 0].min(), np.percentile(w[:, 0], 5), np.median(w[:, 0])))
    thin = w[w[:, 0] < 0.3]
    print("WALL rays with a wall < 0.3:", len(thin), thin[:10].round(3).tolist())
# see-through from the side
n_see, n_tot = 0, 0
for az in np.radians(np.arange(60, 121, 5)):
    for sgn in (1, -1):
        for pitch in np.radians((-25, -10, 0, 10, 25)):
            d = Vector((-sgn * np.sin(az) * np.cos(pitch), np.cos(az) * np.cos(pitch) * -1, np.sin(pitch))).normalized()
            for y in np.arange(-1.5, -0.6, 0.1):
              for x in np.arange(-0.9, 0.91, 0.15):
                for z in np.arange(3.0, 5.7, 0.1):
                    c = Vector((x, y, z))
                    org = c - d * 8
                    n_tot += 1
                    h = bvh.ray_cast(org, d, 16)
                    if h[0] is None:
                        n_see += 1
print("SEE side rays through the face slab:", n_tot, "that hit nothing:", n_see)
if len(w):
    for y0 in np.arange(-1.85, -0.45, 0.1):
        s = w[(w[:, 1] >= y0 - 1e-6) & (w[:, 1] < y0 + 0.1 - 1e-6)]
        if len(s):
            print("WALLY y %.2f..%.2f: %d rays, wall min %.3f p10 %.3f median %.3f, <0.3: %d" % (
                y0, y0 + 0.1, len(s), s[:, 0].min(), np.percentile(s[:, 0], 10), np.median(s[:, 0]), int((s[:, 0] < 0.3).sum())))
if len(w):
    s = w[(w[:, 1] >= -1.45) & (w[:, 0] < 0.3)]
    print("THIN deeper than y -1.45:", s.round(3).tolist())
