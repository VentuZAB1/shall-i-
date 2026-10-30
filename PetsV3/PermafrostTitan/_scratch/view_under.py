# blender -b --factory-startup --python PermafrostTitan/_scratch/view_under.py -- <Name> [dirs=name:x,y,z;...] [dist=1.6]
# Belly-up / from-below check renders (review: "parts visible from below"): the ground is hidden so the camera can
# look up from under the pet. -> renders/under_<name>.png (600 px) + renders/_under_sheet.png
import sys, runpy, os
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
dirs = [(t.split(":")[0], [float(v) for v in t.split(":")[1].split(",")])
        for t in opts.get("dirs", "belly:0.25,-0.35,-1;lowfront:0.35,-1,-0.55;lowback:-0.35,1,-0.55").split(";")]
fac = float(opts.get("dist", "1.6"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from mathutils import Vector
pk = R3["pk"]
R3["model"](name, views=("tq",), res=120)
k = R3["STATE"]["k"]
sc = bpy.context.scene
g = bpy.data.objects.get("Ground")
if g:
    g.hide_render = True
sc.render.resolution_x = sc.render.resolution_y = 600
mn, mx = k.bounds()
c = (mn + mx) / 2
size = max((mx - mn).length, 2.0)
files = []
for nm, dv in dirs:
    pk.aim(sc.camera, c + Vector(dv).normalized() * size * fac, c)
    p = os.path.join(k.dir, "renders", "under_%s.png" % nm)
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    files.append(p)
try:
    from PIL import Image
    ims = [Image.open(f).convert("RGB") for f in files]
    S = Image.new("RGB", (600 * len(ims), 600))
    for i, im in enumerate(ims):
        S.paste(im, (600 * i, 0))
    S.save(os.path.join(k.dir, "renders", "_under_sheet.png"))
except Exception as e:
    print("no PIL in blender:", e)
print("UNDER_DONE")
