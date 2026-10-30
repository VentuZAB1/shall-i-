# blender -b --factory-startup --python _tools/headless_clips.py -- <Name> <act:frame,...> [views=tq,side] [res=300]
#   [mins=act:frame:Group+Group|Group,...]
# Clip pass for review rounds: model + rig + all clips + audit + collision report (step 1) + ground_min_z per clip,
# then pose renders of the picks in every view (file names pose_<view>_<act>_<f>.png) and optional per-group
# minimum z at chosen frames (e.g. the hammer contact test). One JSON line: HEADLESS_RESULT {...}
import sys, runpy, json, os
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
picks = []
if len(argv) > 1 and argv[1] not in ("-", ""):
    for tok in argv[1].split(","):
        a, f = tok.rsplit(":", 1)
        picks.append((a, int(f)))
opts = dict(a.split("=", 1) for a in argv[2:] if "=" in a)
views = opts.get("views", "tq,side").split(",")
res = int(opts.get("res", "300"))
step = int(opts.get("step", "1"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
out = R3["full"](name, pose_picks=None, save=False)
k, m = R3["STATE"]["k"], R3["STATE"]["m"]
pk = R3["pk"]
import bpy
rep = {}
if hasattr(m, "check_pairs"):
    js = m.joints() if hasattr(m, "joints") else None
    rep = R3["blockkit"].overlap_report(k, m.check_pairs(), step=step, joints=js)
names = {g.index: g.name for g in k.main.vertex_groups}
dom = [names[max(v.groups, key=lambda g: g.weight).group] if v.groups else "" for v in k.main.data.vertices]


def posed():
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    pts = [mw @ v.co for v in me.vertices]
    ev.to_mesh_clear()
    return pts


gmin = {}
for clip, (n, loop) in k.clips.items():
    k.set_action(clip)
    lo = (9.0, -1, "")
    for f in range(0, n + 1):                  # every frame (review: odd frames can dip)
        bpy.context.scene.frame_set(f)
        pts = posed()
        i = min(range(len(pts)), key=lambda j: pts[j].z)
        if pts[i].z < lo[0]:
            lo = (round(pts[i].z, 3), f, dom[i])
    gmin[clip] = lo
mins = {}
if opts.get("mins"):
    rest = [k.main.data.vertices[i].co for i in range(len(dom))]
    for tok in opts["mins"].split(","):
        a, f, groups = tok.split(":")
        k.set_action(a)
        bpy.context.scene.frame_set(int(f))
        pts = posed()
        row = {}
        for g in groups.split("|"):
            gs = g.split("+")
            sel = [i for i in range(len(dom)) if dom[i] in gs]
            if g.startswith("HeadLobes"):
                sel = [i for i in range(len(dom)) if dom[i] == "Head" and abs(rest[i].x) > 0.38]
            row[g] = round(min(pts[i].z for i in sel), 4) if sel else None
        mins[a + ":" + f] = row
gaps = {}
if opts.get("gap"):                      # gap=act:frame:GroupA:GroupB,... -> min distance between the two parts
    from mathutils.bvhtree import BVHTree
    for tok in opts["gap"].split(","):
        a_, f_, ga, gb = tok.split(":")
        k.set_action(a_)
        bpy.context.scene.frame_set(int(f_))
        dg = bpy.context.evaluated_depsgraph_get()
        ev = k.main.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        mw = ev.matrix_world
        co = [mw @ v.co for v in me.vertices]
        tb = [list(t.vertices) for t in me.loop_triangles if dom[t.vertices[0]] == gb]
        tree = BVHTree.FromPolygons(co, tb, all_triangles=True)
        best = 9.0
        for i in range(len(co)):
            if dom[i] == ga:
                hit = tree.find_nearest(co[i])
                if hit[0] is not None:
                    best = min(best, hit[3])
        ev.to_mesh_clear()
        gaps[tok] = round(best, 4)
out["gaps"] = gaps
files = []
if opts.get("follow") == "1" and picks:            # re-aim per pick at the posed mesh centre (acts that travel)
    sc = bpy.context.scene
    sc.render.resolution_x = sc.render.resolution_y = res
    k.set_action("idle")
    sc.frame_set(0)
    pts0 = posed()
    c0 = sum(pts0, pts0[0] * 0) / len(pts0)
    for v in views:
        loc, tgt = pk.camera_for(k, v)
        for act, f in picks:
            k.set_action(act)
            sc.frame_set(f)
            pts = posed()
            d = sum(pts, pts[0] * 0) / len(pts) - c0
            pk.aim(sc.camera, loc + d, tgt + d)
            p = os.path.join(k.dir, "renders", "pose_%s_%s_%02d.png" % (v, act, f))
            sc.render.filepath = p
            bpy.ops.render.render(write_still=True)
            files.append(p)
else:
    for v in views:
        files += pk.pose_renders(k, picks, view=v, res=res) if picks else []
k.set_action("idle")
out.pop("bones", None)
out["ground_min_z"] = gmin
out["collisions"] = {c: v for c, v in rep.items() if v}
out["collision_free"] = not any(rep.values())
out["group_min_z"] = mins
out["poses"] = files
print("HEADLESS_RESULT " + json.dumps(out, default=str))
