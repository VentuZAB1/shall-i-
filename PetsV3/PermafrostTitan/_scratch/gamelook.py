# blender -b --factory-startup --python PermafrostTitan/_scratch/gamelook.py -- <Name> [factor=0.6] [views=tq,game]
# In-game colour preview: the model with every vertex colour scaled by `factor` (sRGB, Roblox shows pets ~0.6x as
# bright) -> renders/gamelook_<view>.png. Review aid only (the shipped colours are unchanged).
import sys, runpy, os
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
fac = float(opts.get("factor", "0.6"))
views = opts.get("views", "tq,game").split(",")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
if hasattr(R3["spec"](name), "anim"):           # pets with clips: the idle f0 pose (what the game shows at rest)
    R3["full"](name, save=False)
    k = R3["STATE"]["k"]
    k.set_action("idle")
    bpy.context.scene.frame_set(0)
else:
    R3["model"](name, views=("tq",), res=200)
    k = R3["STATE"]["k"]
pk = R3["pk"]
lin = fac ** 2.2
for o in k.coll.objects:
    if o.type != "MESH":
        continue
    at = o.data.color_attributes.get("Col")
    if at is None:
        continue
    for d in at.data:
        c = d.color
        d.color = (c[0] * lin, c[1] * lin, c[2] * lin, c[3])
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = 600
for v in views:
    loc, tgt = pk.camera_for(k, v)
    pk.aim(sc.camera, loc, tgt)
    sc.render.filepath = os.path.join(k.dir, "renders", "gamelook_%s.png" % v)
    bpy.ops.render.render(write_still=True)
print("HEADLESS_RESULT gamelook ok")
