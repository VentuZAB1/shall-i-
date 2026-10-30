# blender -b --factory-startup --python CoralCrusher/_scratch/eye_px.py -- <Name> <clip> <f,f,...> [res=390]
# Crab r4 9+ check: where each eye lands on the GAME camera image (res x res px, the phone-size frame), per frame.
#   tip  = the Eye_* vertex farthest from the eye joint (the bulb / lid top), projected to px
#   cen  = centroid of the eye's front cluster (verts within 0.05 of the most forward eye vertex) = the slit eye
#   vis  = fraction of that front cluster NOT hidden by another bone's faces (camera ray cast)
# Prints travel (px) of tip / cen between each frame and the first frame.
import sys, runpy, json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, frames = argv[0], argv[1], [int(v) for v in argv[2].split(",")]
opts = dict(a.split("=", 1) for a in argv[3:] if "=" in a)
res = int(opts.get("res", "390"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from bpy_extras.object_utils import world_to_camera_view
pk = R3["pk"]
R3["full"](name, save=False)
k = R3["STATE"]["k"]
k.set_action(clip)
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
cam = sc.camera
vg = {g.index: g.name for g in k.main.vertex_groups}
own = []
for v in k.main.data.vertices:
    own.append(vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?")


def px(p):
    c = world_to_camera_view(sc, cam, p)
    return (c.x * res, (1.0 - c.y) * res)


sc.frame_set(0)
loc, tgt = pk.camera_for(k, "game")          # fixed camera, aimed once at the rest pose (the game cam does not track poses)
pk.aim(cam, loc, tgt)
out = {}
base = {}                                     # first frame: eye points in Spine-local space (rigid-with-body reference)
own_px = {}
for f in frames:
    sc.frame_set(f)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    W = [mw @ v.co for v in me.vertices]
    pown = []
    for pl in me.polygons:
        cnt = {}
        for i in pl.vertices:
            cnt[own[i]] = cnt.get(own[i], 0) + 1
        pown.append(max(cnt, key=cnt.get))
    bvh = BVHTree.FromPolygons(W, [list(pl.vertices) for pl in me.polygons])
    camp = cam.matrix_world.to_translation()
    row = {}
    for e in ("Eye_L", "Eye_R"):
        j = k.arm.matrix_world @ k.arm.pose.bones[e].head
        ids = [i for i in range(len(W)) if own[i] == e]
        tip = max(ids, key=lambda i: (W[i] - j).length)
        # the most camera-facing-forward eye vertex (pet faces -Y) -> its 0.05 cluster = slit eye + bulb front
        fr = min(ids, key=lambda i: W[i].y)
        clu = [i for i in ids if (W[i] - W[fr]).length < 0.05]
        cen = sum((W[i] for i in clu), Vector()) / len(clu)
        vis = 0
        for i in clu:
            d = W[i] - camp
            hit = bvh.ray_cast(camp, d.normalized(), d.length + 0.01)
            if hit[0] is None or hit[3] >= d.length - 0.004 or pown[hit[2]] == e:
                vis += 1
        Ms = k.arm.matrix_world @ k.arm.pose.bones["Spine"].matrix
        if e not in base:
            base[e] = (Ms.inverted() @ W[tip], Ms.inverted() @ cen)
        rt, rc = Ms @ base[e][0], Ms @ base[e][1]          # where the points would be if rigid with the body
        a, b, c2, d2 = px(W[tip]), px(rt), px(cen), px(rc)
        row[e] = {"tip": [round(v, 1) for v in a], "cen": [round(v, 1) for v in c2],
                  "vis": round(vis / len(clu), 2),
                  "own_tip_px": round(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5, 1),
                  "own_cen_px": round(((c2[0] - d2[0]) ** 2 + (c2[1] - d2[1]) ** 2) ** 0.5, 1)}
    out[f] = row
    ev.to_mesh_clear()
f0 = frames[0]
trav = {}
for f in frames[1:]:
    t = {}
    for e in ("Eye_L", "Eye_R"):
        for key in ("tip", "cen"):
            a, b = out[f0][e][key], out[f][e][key]
            t[e + "_" + key] = round(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5, 1)
    trav["%d->%d" % (f0, f)] = t
print("EYEPX " + json.dumps({"res": res, "frames": out, "travel_px": trav}))
