# blender -b --factory-startup --python _tools/pose_try.py -- <Name> "<label>=<Bone>:p,y,r[;<Bone>:p,y,r]...|<label2>=..."
#   [views=tq,game,front] [res=360] [pairs=A|B,C|D]   (default pairs = the spec's check_pairs())
# Quick pose test (2026-10-14, Mantis wing fan): builds model + rig only (NO clips, ~1 min), keys each labelled
# candidate pose (kit rot = (pitch, yaw, roll) armature axes, same as k.key) as a 2-frame action, reports real
# cut-throughs per pair (blockkit.overlap_report incl. the spec's joints) and renders pose_<view>_<label>_00.png.
# Bones may also take a 4th..6th value = loc (x, y, z). "{s}" in a bone name expands to L / R with the mirrored
# yaw / roll sign (e.g. Wing_{s}:60,-55,30 -> Wing_L:60,-55,30 and Wing_R:60,55,-30).
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
cands = []
opts = dict(a.split("=", 1) for a in argv[2:] if "=" in a)
for blk in argv[1].split("|"):
    label, spec = blk.split("=", 1)
    keys = []
    for tok in spec.split(";"):
        if not tok.strip():
            continue
        b, vals = tok.split(":")
        v = [float(x) for x in vals.split(",")]
        if b == "WINGS":                              # WINGS:up,fwd,twist,tip -> the spec's wings() (wing3 flyers)
            keys.append(("__WINGS__", tuple(v), None))
            continue
        rot = tuple(v[:3])
        loc = tuple(v[3:6]) if len(v) >= 6 else None
        if "{s}" in b:
            keys.append((b.replace("{s}", "L"), rot, loc))
            keys.append((b.replace("{s}", "R"), (rot[0], -rot[1], -rot[2]), (-loc[0], loc[1], loc[2]) if loc else None))
        else:
            keys.append((b, rot, loc))
    cands.append((label, keys))
views = opts.get("views", "tq,game,front").split(",")
res = int(opts.get("res", "360"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
m = R3["spec"](name)
k = R3["new_pet"](m, name)
m.model(k)
m.rig(k)
k.build_rig()
pk = R3["pk"]
bk = R3["blockkit"]
k.new_action("idle", 1, False)                       # pose_renders aims the camera from idle f0 (rest pose)
for f in (0, 1):
    k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
k.finish(loop=False)
for label, keys in cands:
    k.new_action(label, 1, False)
    for f in (0, 1):
        for b, rot, loc in keys:
            if b == "__WINGS__":
                m.wings(k, f, *rot)
            elif loc is not None:
                k.key(b, f, rot=rot, loc=loc)
            else:
                k.key(b, f, rot=rot)
    if opts.get("plant"):                                    # plant=1: feet back on their rest spots (IK legs)
        if hasattr(m, "plant8"):                             # plant=Leg3_L,Leg3_R,...: only those legs (8-leg specs)
            m.plant8(k, [0, 1], None if opts["plant"] == "1" else opts["plant"].split(","))
        elif hasattr(m, "plant_frames"):
            m.plant_frames(k, [0, 1])
    if opts.get("ankle"):                                    # ankle=Leg4_L:x,y,z[:toe];... raised ankle at a world point
        import bpy
        from mathutils import Vector
        k.bake_bezier_now()
        for tok in opts["ankle"].split(";"):
            parts = tok.split(":")
            leg, P = parts[0], Vector(tuple(float(v) for v in parts[1].split(",")))
            toe = float(parts[2]) if len(parts) > 2 else None
            hipR, ankR = k.J[leg], k.J[k.legs2[leg]["foot"]]
            for f in (0, 1):
                bpy.context.scene.frame_set(f)
                k.solve_leg(leg, f, Vector((P.x - (ankR.x - hipR.x), P.y - (ankR.y - hipR.y), P.z - ankR.z)), toe=toe)
    k.finish(loop=False)
pairs = m.check_pairs()
if opts.get("pairs"):
    pairs = [tuple(p.split("|")) for p in opts["pairs"].split(",")]
js = list(m.joints()) if hasattr(m, "joints") else []
if opts.get("joints"):                              # joints=x0,y0,z0,x1,y1,z1,r,Bone;...  ({s} = mirrored L / R)
    for tok in opts["joints"].split(";"):
        v = tok.split(",")
        a0, a1, r, bn = tuple(map(float, v[0:3])), tuple(map(float, v[3:6])), float(v[6]), v[7]
        if "{s}" in bn:
            js.append((a0, a1, r, bn.replace("{s}", "L")))
            js.append(((-a0[0], a0[1], a0[2]), (-a1[0], a1[1], a1[2]), r, bn.replace("{s}", "R")))
        else:
            js.append((a0, a1, r, bn))
js = js or None
rep = bk.overlap_report(k, pairs, step=1, joints=js)
where = {}
if opts.get("where"):                              # where=label:A|B -> rest-space centroids of the crossings
    import bpy
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    lab, pr = opts["where"].split(":")
    A, Bn = pr.split("|")
    body = k.main
    nm = {g.index: g.name for g in body.vertex_groups}
    owner = [nm[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
    rest = [v.co.copy() for v in body.data.vertices]

    def hits():
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
        out = set()
        for x, y in T[A].overlap(T[Bn]):
            if bk._tri_hits([co[i] for i in tl[A][x]], [co[i] for i in tl[Bn][y]]):
                out.add((tl[A][x], tl[Bn][y]))
        return out
    k.arm.data.pose_position = "REST"
    bpy.context.view_layer.update()
    base = hits()
    k.arm.data.pose_position = "POSE"
    k.set_action(lab)
    bpy.context.scene.frame_set(0)
    new = hits() - base
    ca = sorted(set(tuple(round(v, 2) for v in sum((rest[i] for i in ta), Vector()) / 3) for ta, tb in new))
    cb = sorted(set(tuple(round(v, 2) for v in sum((rest[i] for i in tb), Vector()) / 3) for ta, tb in new))
    def bbox(c):
        return [[min(v[i] for v in c) for i in range(3)], [max(v[i] for v in c) for i in range(3)]] if c else None
    where = {"pairs": len(new), A: ca[:16], Bn: cb[:16], "bbox_" + A: bbox(ca), "bbox_" + Bn: bbox(cb)}
pts = {}
if opts.get("pts"):                                # pts=Bone,Bone:tail -> posed world head (or tail) per candidate
    import bpy
    for label, _ in cands:
        k.set_action(label)
        bpy.context.scene.frame_set(0)
        row = {}
        for tok in opts["pts"].split(","):
            bn, _, end = tok.partition(":")
            pb = k.arm.pose.bones[bn]
            v = k.arm.matrix_world @ (pb.tail if end == "tail" else pb.head)
            row[tok] = [round(x, 3) for x in v]
        pts[label] = row
lowz = {}                                          # lowest posed vertex per candidate (+ its bone)
import bpy
_nm = {g.index: g.name for g in k.main.vertex_groups}
for label, _ in cands:
    k.set_action(label)
    bpy.context.scene.frame_set(0)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    i, z = min(((v.index, (ev.matrix_world @ v.co).z) for v in me.vertices), key=lambda t: t[1])
    ev.to_mesh_clear()
    vg = k.main.data.vertices[i].groups
    lowz[label] = [round(z, 3), _nm[max(vg, key=lambda g: g.weight).group] if len(vg) else None]
pk.stage(k)
files = []
for v in views:
    files += pk.pose_renders(k, [(label, 0) for label, _ in cands], view=v, res=res)
print("HEADLESS_RESULT " + json.dumps({"collisions": {c: rep.get(c) for c, _ in cands}, "where": where, "pts": pts,
                                       "lowz": lowz,
                                       "files": files}, default=str))
