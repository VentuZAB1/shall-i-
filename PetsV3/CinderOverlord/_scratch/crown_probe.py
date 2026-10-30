# blender -b --factory-startup --python CinderOverlord/_scratch/crown_probe.py -- CinderOverlord [clip:frame,...] [pair=Crown_3,Head]
# Where do two bone groups cross? Crossing points mapped back to the rest pose (via bone B's deform matrix) and to the
# pre-HEAD_XF build space (the coordinates used in model()); the A-triangle centroids likewise (via bone A).
import sys, runpy, json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
picks = [(t.split(":")[0], int(t.split(":")[1])) for t in argv[1].split(",")]
opts = dict(a.split("=", 1) for a in argv[2:] if "=" in a)
A, Bn = opts.get("pair", "Crown_3,Head").split(",")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
bk = R3["blockkit"]
R3["full"](name, save=False)
k = R3["STATE"]["k"]
arm = k.arm
sc = bpy.context.scene
names = {g.index: g.name for g in k.main.vertex_groups}
own = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in k.main.data.vertices]
xf = k.head_xf[0]
pv, s, off = xf[0], xf[1], Vector(xf[3])


HEADB = set(xf[2])


def pre(w):                     # build space only for head-group bones (both bones of the pair must agree)
    return pv + (w - off - pv) / s if Bn in HEADB else w


def defm(b):
    pb = arm.pose.bones[b]
    return arm.matrix_world @ pb.matrix @ arm.data.bones[b].matrix_local.inverted()


def run(tag):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    em = ev.to_mesh()
    em.calc_loop_triangles()
    co = [ev.matrix_world @ v.co for v in em.vertices]
    ta = [tuple(t.vertices) for t in em.loop_triangles if own[t.vertices[0]] == A]
    tb = [tuple(t.vertices) for t in em.loop_triangles if own[t.vertices[0]] == Bn]
    TA = BVHTree.FromPolygons(co, [list(t) for t in ta], all_triangles=True)
    TB = BVHTree.FromPolygons(co, [list(t) for t in tb], all_triangles=True)
    MA, MB = defm(A).inverted(), defm(Bn).inverted()
    pts, cents = [], []
    for x, y in TA.overlap(TB):
        pp = bk._tri_hits([co[i] for i in ta[x]], [co[i] for i in tb[y]])
        for p in pp:
            pts.append(pre(MB @ p))
        if pp:
            cents.append(pre(MA @ (sum((co[i] for i in ta[x]), Vector()) / 3)))
    ev.to_mesh_clear()
    if not pts:
        print("XPROBE", tag, "none")
        return
    lo = [min(p[i] for p in pts) for i in range(3)]
    hi = [max(p[i] for p in pts) for i in range(3)]
    clo = [min(p[i] for p in cents) for i in range(3)]
    chi = [max(p[i] for p in cents) for i in range(3)]
    print("XPROBE", tag, len(pts), "cross_pre_box", [round(v, 3) for v in lo], [round(v, 3) for v in hi],
          "A_tri_pre_box", [round(v, 3) for v in clo], [round(v, 3) for v in chi])


arm.data.pose_position = "REST"
bpy.context.view_layer.update()
run("rest")
arm.data.pose_position = "POSE"
for clip, f in picks:
    k.set_action(clip)
    sc.frame_set(f)
    run("%s:%d" % (clip, f))
