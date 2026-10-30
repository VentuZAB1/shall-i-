# blender -b --factory-startup --python MossbackTortoise/_posecam.py -- <Name> clip:f,clip:f dx,dy,dz tx,ty,tz dist [res]
# posed close-ups from a chosen direction (dx,dy,dz) aimed at (tx,ty,tz) -> <Name>/renders/pc_<clip>_<f>.png
import sys, runpy, os
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
picks = [(t.split(":")[0], int(t.split(":")[1])) for t in argv[1].split(",")]
d = Vector([float(v) for v in argv[2].split(",")]).normalized()
tgt = Vector([float(v) for v in argv[3].split(",")])
dist = float(argv[4])
res = int(argv[5]) if len(argv) > 5 else 400
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
pk = R3["pk"]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
cam = sc.camera
pk.aim(cam, tgt + d * dist, tgt)
for clip, f in picks:
    k.set_action(clip)
    sc.frame_set(f)
    sc.render.filepath = os.path.join(k.dir, "renders", "pc_%s_%03d.png" % (clip, f))
    bpy.ops.render.render(write_still=True)
print("HEADLESS_RESULT ok")
