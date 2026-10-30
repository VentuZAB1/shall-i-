# blender -b --factory-startup --python CinderOverlord/_scratch/face_id.py -- CinderOverlord [res=160] [out=face_id]
# r10 MUST 2 check on the close_front camera (target 0,-1.0,1.86, dist 2.6, dir 0,-1,0.15 = rend.sh / headless_closeup):
# a per-pixel ray cast gives the bone group seen at each pixel; per image row, the width (BU at the target depth) of
# the contiguous Head + Jaw + Mouth run through the face centre line, and the Jaw's own visible width. Rows from the
# nostril line down to the chin: one taper = the width never grows going down. Also writes a group-id PNG.
import sys, runpy, json, os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
RES = int(opts.get("res", "160"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
k.arm.data.pose_position = "REST"            # the model renders (close_front) are the rest pose
pk = R3["pk"]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = RES
cam = sc.camera
tgt = Vector((0, -1.05, 2.10))                 # r12: the close_front aim of the raised, larger head (r10: 0,-1.0,1.86 / 2.6)
pk.aim(cam, tgt + Vector((0, -1, 0.15)).normalized() * 2.9, tgt)
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
ev = k.main.evaluated_get(dg)
me = ev.to_mesh()
me.calc_loop_triangles()
co = [ev.matrix_world @ v.co for v in me.vertices]
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]
tris = [list(t.vertices) for t in me.loop_triangles]
tg = [own[t[0]] for t in tris]
T = BVHTree.FromPolygons(co, tris, all_triangles=True)
fr = [cam.matrix_world @ v for v in cam.data.view_frame(scene=sc)]     # tr, br, bl, tl
o = cam.matrix_world.to_translation()
img = []
for j in range(RES):
    row = []
    v = (j + 0.5) / RES
    for i in range(RES):
        u = (i + 0.5) / RES
        top = fr[3].lerp(fr[0], u)
        bot = fr[2].lerp(fr[1], u)
        p = top.lerp(bot, v)
        h = T.ray_cast(o, (p - o).normalized())
        row.append(tg[h[2]] if h[0] is not None else None)
    img.append(row)
# BU per pixel at the target depth
w_bu = (fr[0] - fr[3]).length * ((tgt - o).length / (fr[0] - o).dot((tgt - o).normalized()))
px_bu = w_bu / RES
FACE = ("Head", "Jaw", "Mouth")
c = RES // 2
rows = []
for j, row in enumerate(img):
    if row[c] not in FACE:
        rows.append((j, None, None, row[c]))
        continue
    l = r = c
    while l > 0 and row[l - 1] in FACE:
        l -= 1
    while r < RES - 1 and row[r + 1] in FACE:
        r += 1
    jaw = [i for i, g in enumerate(row) if g == "Jaw"]
    rows.append((j, round((r - l + 1) * px_bu, 3), round((max(jaw) - min(jaw) + 1) * px_bu, 3) if jaw else 0, row[c]))
ev.to_mesh_clear()
out = opts.get("out", "face_id")
json.dump(img, open(os.path.join(k.dir, "_scratch", out + ".json"), "w"))     # group grid -> PNG outside Blender (no PIL)
print("FACEID " + json.dumps({"px_bu": round(px_bu, 4), "rows": rows}))
