# blender -b --factory-startup --python PermafrostTitan/_scratch/clip_views.py -- <Name> <clip:frame,...> [views=side,front]
#     [res=300] [prefix=cv]
# Clip-frame renders from FIXED cameras (framed once on the rest pose, so poses compare 1:1) for any kit view
# (tq / side / front / back / game) -> <Name>/renders/<prefix>_<view>_<clip>_<frame>.png, plus a sheet per view
# renders/_<prefix>_<view>_sheet.png (PIL from system python is not available inside Blender, so the sheet is made
# by the caller with sheet tools if needed).
import sys, runpy, os, json
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
picks = [(t.rsplit(":", 1)[0], int(t.rsplit(":", 1)[1])) for t in argv[1].split(",") if t]
opts = dict(a.split("=", 1) for a in argv[2:] if "=" in a)
views = opts.get("views", "side,front").split(",")
res = int(opts.get("res", "300"))
prefix = opts.get("prefix", "cv")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
pk = R3["pk"]
R3["full"](name, save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
k.set_action("idle")
sc.frame_set(0)
cams = {v: pk.camera_for(k, v) for v in views}
files = []
for clip, fr in picks:
    k.set_action(clip)
    sc.frame_set(fr)
    for v in views:
        loc, tgt = cams[v]
        pk.aim(sc.camera, loc, tgt)
        p = os.path.join(k.dir, "renders", "%s_%s_%s_%02d.png" % (prefix, v, clip, fr))
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        files.append(p)
print("CLIPVIEWS " + json.dumps(files))
