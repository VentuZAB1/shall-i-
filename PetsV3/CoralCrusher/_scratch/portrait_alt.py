# blender -b --factory-startup --python CoralCrusher/_scratch/portrait_alt.py -- <Name> [dir=1,-1.36,1.3] [dist=1.9]
#     [out=<Name>_portrait_alt.png]
# Review M5 (Coral Crusher r1) + lead ruling 2026-10-27: the kit portrait camera (tq, ~20 deg up) shows a low crab as a
# flat lozenge, so the Index portrait is this ALTERNATIVE: same pose as the kit portrait (idle f0 when clips exist, else
# rest), camera ~37 deg up, transparent 512 px, distance chosen so the fill matches the other pets' portraits
# (max side ~0.75 of the frame; kit portraits measure 0.58-0.88) -> <Name>/<out>.
import sys, runpy, os
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
dv = [float(v) for v in opts.get("dir", "1,-1.36,1.3").split(",")]
fac = float(opts.get("dist", "1.9"))
out = opts.get("out", name + "_portrait_alt.png")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from mathutils import Vector
pk = R3["pk"]
if hasattr(R3["spec"](name), "anim"):
    R3["full"](name, save=False)
    k = R3["STATE"]["k"]
    k.set_action("idle")
    bpy.context.scene.frame_set(0)
else:
    R3["model"](name, views=("tq",), res=200)
    k = R3["STATE"]["k"]
sc = bpy.context.scene
g = bpy.data.objects.get("Ground")
if g:
    g.hide_render = True
sc.render.film_transparent = True
sc.render.resolution_x = sc.render.resolution_y = 512
mn, mx = k.bounds()
c = (mn + mx) / 2
size = max((mx - mn).length, 2.0)
pk.aim(sc.camera, c + Vector(dv).normalized() * size * fac, c)
sc.render.filepath = os.path.join(k.dir, out)
sc.render.image_settings.color_mode = "RGBA"
bpy.ops.render.render(write_still=True)
print("ALT_PORTRAIT_DONE", os.path.join(k.dir, out))
