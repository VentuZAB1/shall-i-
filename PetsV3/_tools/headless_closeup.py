# blender -b --factory-startup --python _tools/headless_closeup.py -- <Name> <tx,ty,tz> <dist> [res] [views] [prefix]
#   views = "name=dx,dy,dz;..." camera directions from the target (default tq / side / front), prefix default "close_"
# Model build + close-up renders (front 3/4, side, front) aimed at a target point (e.g. the head) -> renders/close_*.png
import sys, runpy, os
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
tgt = Vector([float(v) for v in argv[1].split(",")])
dist = float(argv[2])
res = int(argv[3]) if len(argv) > 3 else 700
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["model"](name, views=("tq",), res=200)
import bpy
k = R3["STATE"]["k"]
pk = R3["pk"]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
cam = sc.camera
VIEWS = (("tq", (0.8, -1.0, 0.35)), ("side", (1.0, 0.0, 0.1)), ("front", (0.0, -1.0, 0.15)))
if len(argv) > 4 and argv[4]:
    VIEWS = tuple((t.split("=")[0], tuple(float(v) for v in t.split("=")[1].split(","))) for t in argv[4].split(";"))
prefix = argv[5] if len(argv) > 5 else "close_"
for v, d in VIEWS:
    pk.aim(cam, tgt + Vector(d).normalized() * dist, tgt)
    sc.render.filepath = os.path.join(k.dir, "renders", prefix + v + ".png")
    bpy.ops.render.render(write_still=True)
print("HEADLESS_RESULT ok")
