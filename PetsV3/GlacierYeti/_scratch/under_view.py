# blender -b --factory-startup --python <this> -- <Name> [res] [dx,dy,dz]
# Model build + an UNDERSIDE render with the ground hidden -> <Name>/renders/under.png (review deliverable)
import sys, runpy, os
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
res = int(argv[1]) if len(argv) > 1 else 600
d = Vector([float(v) for v in argv[2].split(",")]) if len(argv) > 2 else Vector((0.55, -0.45, -0.70))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["model"](name, views=("tq",), res=200)
import bpy
k = R3["STATE"]["k"]
pk = R3["pk"]
sc = bpy.context.scene
g = bpy.data.objects.get("Ground")
if g:
    g.hide_render = True
sc.render.resolution_x = sc.render.resolution_y = res
mn, mx = k.bounds()
c = (mn + mx) / 2
size = max((mx - mn).length, 2.0)
pk.aim(sc.camera, c + d.normalized() * size * 1.6, c)
sc.render.filepath = os.path.join(k.dir, "renders", "under.png")
bpy.ops.render.render(write_still=True)
print("HEADLESS_RESULT under ok")
