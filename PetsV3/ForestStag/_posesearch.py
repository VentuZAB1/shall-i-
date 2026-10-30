# blender -b --factory-startup --python ForestStag/_posesearch.py -- <samples> <seed>
# Random search for the act_scratch contact pose: a tine tip on the LEFT flank, no Head / Neck2 parts cutting the body.
import sys, runpy, random, math
argv = sys.argv[sys.argv.index("--") + 1:]
N = int(argv[0]) if argv else 400
seed = int(argv[1]) if len(argv) > 1 else 1
CEN = [float(x) for x in argv[2].split(",")] if len(argv) > 2 else None
SIG = float(argv[3]) if len(argv) > 3 else 5.0
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
pk = R3["pk"]
m = R3["spec"]("ForestStag")
k = R3["new_pet"](m, "ForestStag")
m.model(k)
m.rig(k)
k.build_rig()
arm, body = k.arm, k.main
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
# rest-space tine tips (both antlers) carried by Head
tips = []
for s in (1, -1):
    P = [m.X(p, s) for p in m.BEAM]
    for base, d, L in ((P[0].lerp(P[1], 0.30), (s * 0.15, -1, 0.18), 0.26), (P[0].lerp(P[1], 0.85), (s * 0.25, -1, 0.80), 0.20),
                       (P[2], (s * 0.30, -0.8, 1), 0.20)):
        tips.append(base + Vector(d).normalized() * L)
TGT = [Vector((0.19, y, z)) for y in (-0.25, -0.1, 0.05, 0.2) for z in (0.62, 0.75, 0.88)]
GROUPS = ("Head", "Neck2", "Neck", "Chest", "Spine", "Leg_FL", "Shin_FL", "Leg_BL")


def setpose(vals):
    n1, y1, n2, y2, hd, hy, hr = vals
    for b, rot in (("Neck", (n1, y1, 0)), ("Neck2", (n2, y2, 0)), ("Head", (hd, hy, hr))):
        pb = arm.pose.bones[b]
        R0 = arm.data.bones[b].matrix_local.to_quaternion()
        pb.rotation_quaternion = R0.inverted() @ pk.Rq(*rot) @ R0
    bpy.context.view_layer.update()


def trees():
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    em = ev.to_mesh()
    em.calc_loop_triangles()
    co = [ev.matrix_world @ v.co for v in em.vertices]
    tri = {}
    for t in em.loop_triangles:
        g = owner[t.vertices[0]]
        if g in GROUPS:
            tri.setdefault(g, []).append(list(t.vertices))
    T = {g: BVHTree.FromPolygons(co, tri.get(g, []), all_triangles=True) for g in GROUPS}
    ev.to_mesh_clear()
    return T


setpose((0, 0, 0, 0, 0, 0, 0))
T0 = trees()
base_ov = {(a, b): len(T0[a].overlap(T0[b])) for a in ("Head", "Neck2") for b in ("Chest", "Spine", "Leg_FL", "Shin_FL", "Leg_BL")}
base_ov[("Head", "Neck")] = len(T0["Head"].overlap(T0["Neck"]))
if len(argv) > 4 and argv[4] != "RAKE":                                   # explicit candidate list "a;b;c" -> report each
    for cand in argv[4].split(";"):
        v = [float(x) for x in cand.split(",")]
        setpose(v)
        T = trees()
        bad = {"%s|%s" % ab: len(T[ab[0]].overlap(T[ab[1]])) - b0 for ab, b0 in base_ov.items()
               if len(T[ab[0]].overlap(T[ab[1]])) > b0}
        M = arm.matrix_world @ arm.pose.bones["Head"].matrix @ arm.data.bones["Head"].matrix_local.inverted()
        d = min((M @ t - g).length for t in tips for g in TGT)
        print("CAND %s d=%.3f bad=%s" % (cand, d, bad))
    raise SystemExit
rng = random.Random(seed)
best = []
RAKE = "RAKE" in sys.argv
if RAKE:                                            # contact tine of the base pose + its world position
    BASE = (32, 73, 10, 28, 54, 31, 84)
    setpose(BASE)
    M0 = arm.matrix_world @ arm.pose.bones["Head"].matrix @ arm.data.bones["Head"].matrix_local.inverted()
    ti = min(range(len(tips)), key=lambda i: min((M0 @ tips[i] - g).length for g in TGT))
    P0 = M0 @ tips[ti]
    DIR = Vector((0, 1, -1)).normalized()
    print("SEARCH base tip", ti, [round(c, 3) for c in P0])
for i in range(N):
    if CEN:
        v = tuple(c + rng.gauss(0, SIG) for c in CEN)
    else:
        v = (rng.uniform(-10, 35), rng.uniform(30, 75), rng.uniform(-5, 45), rng.uniform(15, 60), rng.uniform(-10, 70),
             rng.uniform(-10, 70), rng.uniform(-80, 80))
    setpose(v)
    T = trees()
    bad = 0
    for (a, b), b0 in base_ov.items():
        c = len(T[a].overlap(T[b]))
        if c > b0:
            bad += c - b0
    if bad:
        continue
    M = arm.matrix_world @ arm.pose.bones["Head"].matrix @ arm.data.bones["Head"].matrix_local.inverted()
    if RAKE:
        q = M @ tips[ti]
        trav = (q - P0).dot(DIR)
        off = abs(q.x - 0.21)
        ln = (q - P0).length
        if trav < 0.03 or ln < 0.11:
            continue
        d = abs(ln - 0.15) + 2 * off
        best.append((d, [round(x, 1) for x in v] + [round(trav, 3), round((q - P0).length, 3), round(q.x, 3)]))
        continue
    d = min((M @ t - g).length for t in tips for g in TGT)
    best.append((d, [round(x, 1) for x in v]))
best.sort()
for d, v in best[:8]:
    print("SEARCH %.3f %s" % (d, v))
print("SEARCH valid %d of %d" % (len(best), N))
