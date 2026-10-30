# blender -b --factory-startup --python CinderOverlord/_scratch/coll_probe.py -- CinderOverlord [step=1]
# r10 MUST 3 (collision proof):
#  A. overlap_report (the kit's collision_free) with the pet's check_pairs / joints, every frame of all four clips
#  B. minimum surface clearance per non-attached pair, every frame of all four clips (paws, skull, jaw, frill vs crown)
#  C. sensitivity: push the left paw into Neck1 / swing Crown_5 down into the frill and count what the checker reports
#     with the pet's joints() and with the review's proposed extra proxies (paw r 0.07, skull side r 0.12).
#     blockkit.overlap_report: a crossing whose points ALL lie within r of a joints() segment is a HINGE SLIVER and is
#     IGNORED - so a proxy is an exclusion zone, not a sensor.
import sys, runpy, json, math
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
step = int(opts.get("step", "1"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
bk = R3["blockkit"]
R3["full"](name, save=False)
k, m = R3["STATE"]["k"], R3["STATE"]["m"]
sc = bpy.context.scene
arm = k.arm
out = {}
pairs = m.check_pairs()
J = m.joints()
# ---- A
rep = bk.overlap_report(k, pairs, step=step, joints=J)
out["A_pairs"] = len(pairs)
out["A_collisions"] = {c: v for c, v in rep.items() if v}
out["A_collision_free"] = not any(rep.values())
# ---- A2: the same pairs with ONLY each pair's own hinge proxy (the child bone's joints() entry when one bone is the
# other's parent; none otherwise) - no neighbouring sphere can hide a crossing
par = {b.name: (b.parent.name if b.parent else None) for b in arm.data.bones}
groups2 = {}
for a, b in pairs:
    js = tuple(i for i, j in enumerate(J) if (j[3] == a and par.get(a) == b) or (j[3] == b and par.get(b) == a))
    groups2.setdefault(js, []).append((a, b))
rep2 = {}
for js, prs in groups2.items():
    r = bk.overlap_report(k, prs, step=step, joints=[J[i] for i in js])
    for c, v in r.items():
        if v:
            rep2.setdefault(c, {}).update(v)
out["A2_groups"] = {",".join(J[i][3] for i in js) or "-": len(prs) for js, prs in groups2.items()}
out["A2_collisions"] = rep2
out["A2_collision_free"] = not rep2
# ---- A detail: where the crossings are (world points), first offending frame per clip / pair
names = {g.index: g.name for g in k.main.vertex_groups}
own0 = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in k.main.data.vertices]
det = {}
for clip, prs in out["A_collisions"].items():
    k.set_action(clip)
    for key, (cnt, f) in prs.items():
        a, b = key.split("|")
        sc.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        ev = k.main.evaluated_get(dg)
        em = ev.to_mesh()
        em.calc_loop_triangles()
        co = [ev.matrix_world @ v.co for v in em.vertices]
        ta = [tuple(t.vertices) for t in em.loop_triangles if own0[t.vertices[0]] == a]
        tb = [tuple(t.vertices) for t in em.loop_triangles if own0[t.vertices[0]] == b]
        A_ = BVHTree.FromPolygons(co, [list(t) for t in ta], all_triangles=True)
        B_ = BVHTree.FromPolygons(co, [list(t) for t in tb], all_triangles=True)
        pts = []
        for x, y in A_.overlap(B_):
            pp = bk._tri_hits([co[i] for i in ta[x]], [co[i] for i in tb[y]])
            if pp:
                rb = k.main.matrix_world @ k.main.data.vertices[tb[y][0]].co
                pts.append((tuple(round(c, 3) for c in pp[0]), tuple(round(c, 3) for c in rb)))
        ev.to_mesh_clear()
        det[clip + ":" + key] = pts[:6] + [len(pts)]
out["A_detail"] = det
# ---- D (r11 MUST 3b): penetration DEPTH of the seated / strict-run pairs, every `dstep` frames of all four clips.
# depth(A in B) = the deepest A vertex inside B's main solid (its largest connected island = the tube / ball), measured
# to B's surface; both directions, the larger is reported. Rest depth too (the seat as modelled).
SEAT = [("Arm_L", "Neck1"), ("Arm_R", "Neck1"), ("Arm_L", "Neck2"), ("Arm_R", "Neck2"), ("Arm_L", "Spine"),
        ("Arm_R", "Spine"), ("Neck2", "Spine"), ("Body4", "Body2")]
for c, prs in out["A2_collisions"].items():
    for key in prs:
        a, b = key.split("|")
        if (a, b) not in SEAT and (b, a) not in SEAT:
            SEAT.append((a, b))
dstep = int(opts.get("dstep", "2"))
names_d = {g.index: g.name for g in k.main.vertex_groups}
own_d = [names_d[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in k.main.data.vertices]
seat_groups = sorted(set(g for pr in SEAT for g in pr))


def depth_snapshot():
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    em = ev.to_mesh()
    em.calc_loop_triangles()
    co = [ev.matrix_world @ v.co for v in em.vertices]
    tri = {}
    for t in em.loop_triangles:
        g = own_d[t.vertices[0]]
        if g in seat_groups:
            tri.setdefault(g, []).append(tuple(t.vertices))
    ev.to_mesh_clear()
    main, verts = {}, {}
    for g, tl in tri.items():
        par = {}

        def fnd(x):
            while par.get(x, x) != x:
                par[x] = par.get(par[x], par[x])
                x = par[x]
            return x
        for t in tl:
            r0 = fnd(t[0])
            for v in t[1:]:
                rv = fnd(v)
                if rv != r0:
                    par[rv] = r0
        isl = {}
        for t in tl:
            isl.setdefault(fnd(t[0]), []).append(t)
        big = max(isl.values(), key=len)
        main[g] = BVHTree.FromPolygons(co, [list(t) for t in big], all_triangles=True)
        verts[g] = sorted(set(v for t in tl for v in t))
    return co, main, verts


def depth(co, main, verts, a, b):
    best = 0.0
    for x, y in ((a, b), (b, a)):
        t = main[y]
        for i in verts[x]:
            q, nrm, _, d = t.find_nearest(co[i])
            if q is not None and (co[i] - q).dot(nrm) < 0 and d > best:
                best = d
    return best


arm.data.pose_position = "REST"
bpy.context.view_layer.update()
co, mn, vs = depth_snapshot()
d_rest = {a + "|" + b: round(depth(co, mn, vs, a, b), 4) for a, b in SEAT}
arm.data.pose_position = "POSE"
bpy.context.view_layer.update()
d_frames = {a + "|" + b: {} for a, b in SEAT}
for clip, (n, loop) in k.clips.items():
    k.set_action(clip)
    for f in range(0, n + 1, dstep):
        sc.frame_set(f)
        co, mn, vs = depth_snapshot()
        for a, b in SEAT:
            d_frames[a + "|" + b]["%s:%d" % (clip, f)] = round(depth(co, mn, vs, a, b), 4)
out["D_depth_rest"] = d_rest
out["D_depth_max"] = {kk: max(v.items(), key=lambda kv: kv[1]) for kk, v in d_frames.items()}
json.dump({"rest": d_rest, "per_frame": d_frames}, open(opts.get("depth_out", "coll_depths.json"), "w"), indent=0)
# ---- B
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]
rest = [v.co.copy() for v in k.main.data.vertices]
SPIKE = set(i for i, g in enumerate(own) if g == "Head" and abs((k.main.matrix_world @ rest[i]).x) > 0.36
            and (k.main.matrix_world @ rest[i]).y > -0.55)        # cheek spikes + frill (not the crown mount ends)
HOODV = set(i for i, g in enumerate(own) if (g == "Neck2" and abs((k.main.matrix_world @ rest[i]).x) > 0.25) or
            (g == "Neck3" and abs((k.main.matrix_world @ rest[i]).x) > 0.215))   # outside the neck tube (+ band)
                                                                   # r12: the cobra hood panels / rim / ribs / spots
# r14: the crown BLADES = Crown_i verts more than 0.07 above their (rest) hinge point, i.e. above the crown mount; the
# socket below that is seated IN the mount (a hinge, like the shoulder seats) and is reported by the strict run
BLADEV = {}
for ci in range(1, 6):
    hb = arm.matrix_world @ arm.data.bones["Crown_%d" % ci].head_local
    BLADEV["BLADE_%d" % ci] = set(i for i, g in enumerate(own) if g == "Crown_%d" % ci and
                                  (k.main.matrix_world @ rest[i]).z > hb.z + 0.07)
CL = [("Claw_L", "Neck1"), ("Claw_L", "Neck2"), ("Claw_L", "Spine"), ("Claw_L", "Body1"), ("Claw_L", "Jaw"),
      ("Claw_L", "Head"), ("Claw_R", "Neck1"), ("Claw_R", "Neck2"), ("Claw_R", "Spine"), ("Claw_R", "Body1"),
      ("Claw_R", "Jaw"), ("Claw_R", "Head"), ("Claw_L", "Claw_R"), ("Arm_L", "Neck2"), ("Arm_R", "Neck2"),
      ("Head", "Neck1"), ("Head", "Neck2"), ("Jaw", "Neck2"), ("Head", "Arm_L"), ("Head", "Arm_R"),
      ("SPIKES", "Crown_1"), ("SPIKES", "Crown_2"), ("SPIKES", "Crown_4"), ("SPIKES", "Crown_5"),
      ("SPIKES", "Neck2"), ("SPIKES", "Neck3"),
      ("Crown_1", "Crown_2"), ("Crown_2", "Crown_3"), ("Crown_3", "Crown_4"), ("Crown_4", "Crown_5"),
      ("HOOD", "Head"), ("HOOD", "Jaw"), ("HOOD", "SPIKES"), ("HOOD", "Crown_1"), ("HOOD", "Crown_2"),
      ("HOOD", "Crown_3"), ("HOOD", "Crown_4"), ("HOOD", "Crown_5"), ("HOOD", "Claw_L"), ("HOOD", "Claw_R"),
      ("HOOD", "Arm_L"), ("HOOD", "Arm_R"), ("HOOD", "Spine"), ("HOOD", "Neck1"),
      ("BLADE_1", "Head"), ("BLADE_2", "Head"), ("BLADE_3", "Head"), ("BLADE_4", "Head"), ("BLADE_5", "Head")]
groups = sorted(set(g for pr in CL for g in pr))


def snapshot():
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    em = ev.to_mesh()
    em.calc_loop_triangles()
    co = [ev.matrix_world @ v.co for v in em.vertices]
    tris = {}
    for t in em.loop_triangles:
        a = t.vertices[0]
        g = "SPIKES" if a in SPIKE else ("HOOD" if a in HOODV else own[a])
        tris.setdefault(g, []).append(list(t.vertices))
    ev.to_mesh_clear()
    for bg, vs in BLADEV.items():                                      # r14: blade-only sub-groups of Crown_i
        tris[bg] = [t for t in tris.get("Crown_" + bg[-1], []) if all(v in vs for v in t)]
    T = {g: BVHTree.FromPolygons(co, tris.get(g, []), all_triangles=True) for g in groups}
    V = {g: sorted(set(i for t in tris.get(g, []) for i in t)) for g in groups}
    return co, T, V


def dist(co, T, V, a, b):
    d = 9.0
    for x, y in ((a, b), (b, a)):
        t = T[y]
        for i in V[x]:
            h = t.find_nearest(co[i], d)
            if h[0] is not None and h[3] < d:
                d = h[3]
    return d


clear = {}
arm.data.pose_position = "REST"
bpy.context.view_layer.update()
co, T, V = snapshot()
out["B_rest"] = {a + "|" + b: round(dist(co, T, V, a, b), 4) for a, b in CL}
arm.data.pose_position = "POSE"
bpy.context.view_layer.update()
for clip, (n, loop) in k.clips.items():
    k.set_action(clip)
    for f in range(0, n + 1, step):
        sc.frame_set(f)
        co, T, V = snapshot()
        for a, b in CL:
            d = dist(co, T, V, a, b)
            key = a + "|" + b
            if d < clear.get(key, (9, "", 0))[0]:
                clear[key] = (round(d, 4), clip, f)
out["B_min_clearance"] = clear
out["B_overall_min"] = min(clear.items(), key=lambda kv: kv[1][0])
# ---- C
k.set_action("idle")
sc.frame_set(0)
fcs = k.fcurves()


def inject(bone, M):
    for fc in fcs:
        if fc.data_path.startswith('pose.bones["%s"]' % bone):
            fc.mute = True
    pb = arm.pose.bones[bone]
    sc.frame_set(0)
    pb.matrix = M @ pb.matrix
    bpy.context.view_layer.update()


def release(bone):
    for fc in fcs:
        if fc.data_path.startswith('pose.bones["%s"]' % bone):
            fc.mute = False
    pb = arm.pose.bones[bone]
    pb.location = (0, 0, 0)
    pb.rotation_quaternion = (1, 0, 0, 0)
    sc.frame_set(0)


def count(pr, joints):
    keep = k.set_action
    k.set_action = lambda name: None            # set_action() calls rest_pose(), which would wipe the injected pose
    try:
        r = bk.overlap_report(k, [pr], clips=["idle"], frames={"idle": [0]}, joints=joints)
    finally:
        k.set_action = keep
    v = r["idle"].get(pr[0] + "|" + pr[1])
    return v[0] if v else 0


paw_px = [((0.39, -0.93, 0.59), (0.39, -0.93, 0.59), 0.07, "Claw_L"), ((-0.39, -0.93, 0.59), (-0.39, -0.93, 0.59), 0.07, "Claw_R")]
# skull-side proxies at the Head group's widest point (rest), r 0.12, as the review proposes
hv = [k.main.matrix_world @ rest[i] for i, g in enumerate(own) if g == "Head" and i not in SPIKE]
wide = max(hv, key=lambda p: abs(p.x))
cz = sum((p.z for p in hv)) / len(hv)
# joints() points are rest-space, head-scaled by blockkit.head_point -> give the pre-scale point
pv, s, bones, off = k.head_xf[0][0], k.head_xf[0][1], k.head_xf[0][2], Vector(k.head_xf[0][3])
inv = lambda p: pv + (Vector(p) - off - pv) / s
skull_px = []
for sx in (1, -1):
    q = inv(Vector((sx * abs(wide.x) * 0.85, wide.y, cz)))
    skull_px.append((tuple(q), tuple(q), 0.12, "Head"))
out["C_skull_proxy_world"] = [round(abs(wide.x) * 0.85, 3), round(wide.y, 3), round(cz, 3)]
res = {}
for tag, mv in (("paw_in_0.10", (-0.10, 0.10, 0)), ("paw_in_0.16", (-0.16, 0.16, 0)), ("paw_in_0.22", (-0.22, 0.20, 0))):
    inject("Claw_L", Matrix.Translation(Vector(mv)))
    res[tag] = {"no_proxies": count(("Claw_L", "Neck1"), []), "pet_joints": count(("Claw_L", "Neck1"), J),
                "plus_paw_proxies": count(("Claw_L", "Neck1"), J + paw_px)}
    release("Claw_L")
cb = arm.matrix_world @ arm.pose.bones["Crown_5"].head
for ang in (60, 80, 100):
    R = (Matrix.Translation(cb) @ Matrix.Rotation(math.radians(-ang), 4, "Y") @ Matrix.Translation(-cb))
    inject("Crown_5", R)
    res["crown5_down_%d" % ang] = {"no_proxies": count(("Crown_5", "Head"), []), "pet_joints": count(("Crown_5", "Head"), J),
                                   "plus_skull_proxies": count(("Crown_5", "Head"), J + skull_px)}
    release("Crown_5")
out["C_sensitivity"] = res
print("COLLPROBE " + json.dumps(out, default=str))
