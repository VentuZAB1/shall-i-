"""Every game tube's open start ring must be hidden: inside the decimated core mesh, or inside its parent tube."""
import sys, math, bmesh, numpy as np
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\DeadTrees")
import bpy
import trees
from treekit import tube_rings, frames_along, pick_rings
from mathutils import Vector
from mathutils.bvhtree import BVHTree
kind = sys.argv[-1]
ctx = trees.setup(kind)
core_items, tubes = trees.split_items(ctx["tree"])
name = ctx["spec"]["name"]
bpy.ops.wm.open_mainfile(filepath=trees.blend_path(kind))
vs, ps, off = [], [], 0
for nm in ("_Trunk", "_Limbs"):
    o = bpy.data.objects[name + nm]
    bm = bmesh.new(); bm.from_mesh(o.data); bm.transform(o.matrix_world)
    vs += [v.co.copy() for v in bm.verts]; ps += [[v.index + off for v in f.verts] for f in bm.faces]; off += len(bm.verts)
    bm.free()
cbvh = BVHTree.FromPolygons(vs, ps)
def inside_core(p):
    votes = 0
    for d in (Vector((0.31, 0.52, 0.8)), Vector((-0.6, 0.2, 0.77)), Vector((0.1, -0.7, -0.7))):
        n, o2 = 0, p.copy()
        for _ in range(40):
            h = cbvh.ray_cast(o2, d, 50)
            if h[0] is None: break
            n += 1; o2 = h[0] + d * 1e-4
        votes += n % 2
    return votes >= 2
tube_of = {id(br): (P, R) for br, P, R, s0 in tubes}
def inside_tube(p, P, R, k=0.97):
    p = np.array(p)
    best = 9.0
    for i in range(len(P) - 1):
        a, b = P[i], P[i + 1]
        D = b - a; L2 = D @ D
        t = np.clip((p - a) @ D / max(L2, 1e-12), 0, 1)
        d = np.linalg.norm(p - (a + t * D)) - k * (R[i] + t * (R[i + 1] - R[i]))
        best = min(best, d)
    return best < 0
bad = []
for br, P, R, s0 in tubes:
    sides = trees.lo_sides(float(R.max()))
    pts, rr, ss = tube_rings(P, R, 0.05)
    T, N, B = frames_along(pts[:3])
    kfit = 1.0 / math.cos(math.pi / sides) ** 0.5
    ring = [Vector(pts[0] + (N[0] * math.cos(a) + B[0] * math.sin(a)) * rr[0] * kfit) for a in np.linspace(0, 2 * math.pi, sides, endpoint=False)]
    par = br.parent
    out = 0
    for q in ring:
        if inside_core(q):
            continue
        if par is not None and id(par) in tube_of and inside_tube(q, *tube_of[id(par)]):
            continue
        out += 1
    if out:
        bad.append((out, sides, tuple(round(float(x), 2) for x in pts[0]), round(float(rr[0]), 3), br.level,
                    "core-cut" if s0 > 0 else ("parent-tube" if par is not None and id(par) in tube_of else "parent-core")))
print("STARTS2 tubes", len(tubes), "with exposed start verts", len(bad))
from collections import Counter
print("STARTS2 by kind", Counter(b[5] for b in bad))
for b in sorted(bad, key=lambda t: -t[3])[:30]:
    print("STARTS2  %d/%d verts out, start %s r %.3f level %d %s" % b)
