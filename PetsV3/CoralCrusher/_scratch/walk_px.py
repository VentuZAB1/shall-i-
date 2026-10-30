# blender -b --factory-startup --python CoralCrusher/_scratch/walk_px.py -- <Name> [clip=walk] [f0=0] [f1=15] [res=390]
# Per-clip audit check: on the GAME camera (fixed, aimed at rest, res x res px) how far do the body (carapace top:
# the 30 highest Spine-owned vertices) and each leg tip (the lowest vertex owned by each leg's foot bone) move on
# screen over frames f0..f1? Prints per point: the px range (bbox diagonal of its screen track) and the largest
# frame-to-f0 distance.
import sys, runpy, json
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
clip = opts.get("clip", "walk")
f0, f1 = int(opts.get("f0", "0")), int(opts.get("f1", "15"))
res = int(opts.get("res", "390"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from bpy_extras.object_utils import world_to_camera_view
pk = R3["pk"]
R3["full"](name, save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
cam = sc.camera
k.set_action(clip)
sc.frame_set(0)
loc, tgt = pk.camera_for(k, "game")
pk.aim(cam, loc, tgt)
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]
co = [v.co for v in k.main.data.vertices]
spine = sorted([i for i in range(len(co)) if own[i] == "Spine"], key=lambda i: -co[i].z)[:30]
tips = {}
for leg, d in k.legs2.items():
    fb = d["foot"]
    ids = [i for i in range(len(co)) if own[i] == fb]
    if ids:
        tips[leg] = min(ids, key=lambda i: co[i].z)
spi = [i for i in range(len(co)) if own[i] == "Spine"]
rimL = sorted(spi, key=lambda i: -co[i].x)[:12]                    # carapace rim, +x side (the body silhouette edge)
rimR = sorted(spi, key=lambda i: co[i].x)[:12]
track = {"body": [], "rim_px": [], "rim_nx": [], **{leg: [] for leg in tips}}
for f in range(f0, f1 + 1):
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world

    def px(p):
        c = world_to_camera_view(sc, cam, p)
        return (c.x * res, (1 - c.y) * res)
    b = sum((mw @ me.vertices[i].co for i in spine), Vector()) / len(spine)
    track["body"].append(px(b))
    track["rim_px"].append(px(sum((mw @ me.vertices[i].co for i in rimL), Vector()) / len(rimL)))
    track["rim_nx"].append(px(sum((mw @ me.vertices[i].co for i in rimR), Vector()) / len(rimR)))
    for leg, i in tips.items():
        track[leg].append(px(mw @ me.vertices[i].co))
    ev.to_mesh_clear()
out = {}
for key, tr in track.items():
    xs, ys = [p[0] for p in tr], [p[1] for p in tr]
    rng = ((max(xs) - min(xs)) ** 2 + (max(ys) - min(ys)) ** 2) ** 0.5
    far = max(((p[0] - tr[0][0]) ** 2 + (p[1] - tr[0][1]) ** 2) ** 0.5 for p in tr)
    out[key] = {"range_px": round(rng, 1), "max_from_f0_px": round(far, 1), "dy_px": round(max(ys) - min(ys), 1)}
print("WALKPX " + json.dumps({"clip": clip, "frames": [f0, f1], "res": res, "points": out}))
