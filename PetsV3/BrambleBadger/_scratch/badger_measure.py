# blender -b --factory-startup --python BrambleBadger/_scratch/badger_measure.py -- [breath|clear|all]
# r4 M1 / M2 measurements on the posed, skinned mesh (world units):
#  breath: mantle-top Z, Spine-hull-top Z at the shoulder, their difference, snout Z, at the breath peaks / troughs;
#          lowest Head / Jaw Z over idle f0-120.
#  clear:  signed clearance (min distance, negative = cutting in) between the head group (Head, Jaw, Ear_L/R) and the
#          Chest blocks (mantle + grey shoulder + chest plate), and between the Neck blocks and the Chest blocks,
#          per frame over act_burrow f5-68 and roar f0-45, plus the rest pose.
import sys, runpy, json, os
from mathutils import Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
mode = argv[0] if argv else "all"
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"]("BrambleBadger", save=False)
k = R3["STATE"]["k"]
import bpy
sc = bpy.context.scene
body = k.main
me = body.data
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in me.vertices]
rest = [body.matrix_world @ v.co for v in me.vertices]


def posed():
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    em = ev.to_mesh()
    em.calc_loop_triangles()
    co = [ev.matrix_world @ v.co for v in em.vertices]
    tris = [tuple(t.vertices) for t in em.loop_triangles]
    ev.to_mesh_clear()
    return co, tris


def pick(bone, xr, yr, key):
    x0, x1 = xr                                                  # signed x range
    ids = [i for i, o in enumerate(owner) if o == bone and x0 <= rest[i].x < x1 and yr[0] < rest[i].y < yr[1]]
    return key(ids, key=lambda i: rest[i].z)


out = {}
if mode in ("breath", "all"):
    i_mantle = pick("Chest", (-0.25, -0.05), (-0.40, -0.26), max)   # MANTLE top edge (left side)
    i_centre = pick("Chest", (-0.05, 0.05), (-0.40, -0.26), max)    # shoulder-top centre (thorn-2 base, Chest)
    i_hull = pick("Spine", (-0.25, -0.05), (-0.25, -0.15), max)     # grey hull top behind the cape (left side)
    heads = [i for i, o in enumerate(owner) if o == "Head"]
    i_snout = min(heads, key=lambda i: rest[i].y)              # nose tip (front-most Head point)
    hj = [i for i, o in enumerate(owner) if o in ("Head", "Jaw")]
    k.set_action("idle")
    rows = {}
    lo = (9.0, -1)
    for f in range(0, 121):
        sc.frame_set(f)
        co, _ = posed()
        z = min(co[i].z for i in hj)
        if z < lo[0]:
            lo = (round(z, 4), f)
        if f in (0, 10, 30, 40, 50, 70, 90, 110):
            rows[f] = {"mantle_top": round(co[i_mantle].z, 4), "hull_top": round(co[i_hull].z, 4),
                       "centre_top": round(co[i_centre].z, 4),
                       "mantle_minus_hull": round(co[i_mantle].z - co[i_hull].z, 4),
                       "snout": round(co[i_snout].z, 4)}
    out["breath"] = {"BREATH": os.environ.get("BADGER_BREATH", "1.0"), "rows": rows, "head_jaw_min_z": lo,
                     "rest_points": {"mantle_top": [round(c, 3) for c in rest[i_mantle]],
                                     "hull_top": [round(c, 3) for c in rest[i_hull]],
                                     "centre_top": [round(c, 3) for c in rest[i_centre]],
                                     "snout": [round(c, 3) for c in rest[i_snout]]}}

if mode in ("clear", "all"):
    HG = {"Head", "Jaw", "Ear_L", "Ear_R"}
    NG = {"Neck"}
    CG = {"Chest"}

    WHERE = []

    def clearance(co, tris, A, B):
        """min signed distance of A's vertices to B's surface and of B's vertices to A's surface (- = inside)."""
        best = 9.0
        for P, Q in ((A, B), (B, A)):
            tq = [t for t in tris if owner[t[0]] in Q]
            tree = BVHTree.FromPolygons(co, [list(t) for t in tq], all_triangles=True)
            for i, o in enumerate(owner):
                if o not in P:
                    continue
                hit = tree.find_nearest(co[i], 0.12)
                if hit[0] is None:
                    continue
                loc, nrm, _, dist = hit
                sd = dist if (co[i] - loc).dot(nrm) >= 0 else -dist
                if sd < best:
                    best = sd
                    WHERE[:] = [owner[i], [round(c, 3) for c in rest[i]], [round(c, 3) for c in co[i]]]
        return round(best, 4)

    res = {}
    # rest pose
    k.set_action("idle")
    for pb in k.arm.pose.bones:
        pass
    k.arm.data.pose_position = "REST"
    co, tris = posed()
    res["rest"] = {"head_vs_chest": clearance(co, tris, HG, CG), "neck_vs_chest": clearance(co, tris, NG, CG)}
    k.arm.data.pose_position = "POSE"
    for clip, fr in (("act_burrow", range(5, 69)), ("roar", range(0, 46)), ("act_burrow_all", range(0, 101)), ("roar_all", range(0, 61)), ("walk", range(0, 31))):
        k.set_action(clip.replace("_all", ""))
        hmin, nmin = (9.0, -1), (9.0, -1)
        for f in fr:
            sc.frame_set(f)
            co, tris = posed()
            h = clearance(co, tris, HG, CG)
            nn = clearance(co, tris, NG, CG)
            if h < hmin[0]:
                hmin = (h, f)
            if nn < nmin[0]:
                nmin = (nn, f)
        res[clip] = {"head_vs_chest_min": hmin, "neck_vs_chest_min": nmin}
        if clip not in ("act_burrow", "roar"):
            continue
        sc.frame_set(hmin[1])
        co, tris = posed()
        res[clip]["at_worst_frame"] = {g: clearance(co, tris, {g}, CG) for g in ("Head", "Ear_L", "Ear_R")}
        clearance(co, tris, {"Head"}, CG)
        res[clip]["worst_point(owner, rest, posed)"] = list(WHERE)
        res[clip]["head_vs_chest_per_frame"] = []
        for f in (list(range(5, 69, 3)) if clip == "act_burrow" else list(range(0, 46, 5))):
            sc.frame_set(f)
            co, tris = posed()
            res[clip]["head_vs_chest_per_frame"].append((f, clearance(co, tris, HG, CG)))
    out["clear"] = res

print("MEASURE_RESULT " + json.dumps(out))
open(os.path.join(k.dir, "_scratch", "measure_%s_b%s.json" % (mode, os.environ.get("BADGER_BREATH", "1.0"))),
     "w").write(json.dumps(out, indent=1))
