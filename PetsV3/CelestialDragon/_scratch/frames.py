# blender -b --python frames.py -- <Name> <clip> <f,f,..> <view> <tx,ty,tz> <dist> [res]  -> _scratch/fr_<f>.png + strip
import sys, runpy, os
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip = argv[0], argv[1]
frames = [int(x) for x in argv[2].split(",")]
view = argv[3]
tgt = Vector([float(v) for v in argv[4].split(",")])
dist = float(argv[5])
res = int(argv[6]) if len(argv) > 6 else 360
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
pk = R3["pk"]
m = R3["spec"](name)
k = R3["new_pet"](m, name)
m.model(k)
m.rig(k)
k.build_rig()
m.anim(k)
pk.stage(k)
k.set_action(clip)
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
D = {"tq": (0.8, -1.0, 0.35), "side": (1.0, 0.0, 0.1), "front": (0.0, -1.0, 0.15), "back": (-0.7, 1.0, 0.45)}
pk.aim(sc.camera, tgt + Vector(D[view]).normalized() * dist, tgt)
files = []
for f in frames:
    sc.frame_set(f)
    p = os.path.join(k.dir, "_scratch", "fr_%03d.png" % f)
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    files.append(p)
print("HEADLESS_RESULT ok")
