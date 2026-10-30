# blender -b --python pose_close.py -- <Name> <clip> <frame> <tx,ty,tz> <dist> [res] [views]
# full build (model+rig+anim, no audit), then renders the posed pet from tq/side/front/back at a target -> renders/pc_<view>.png
import sys, runpy, os
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, frame = argv[0], argv[1], int(argv[2])
tgt = Vector([float(v) for v in argv[3].split(",")])
dist = float(argv[4])
res = int(argv[5]) if len(argv) > 5 else 600
views = argv[6].split(",") if len(argv) > 6 else ["tq", "side", "front", "back"]
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
sc.frame_set(frame)
sc.render.resolution_x = sc.render.resolution_y = res
cam = sc.camera
D = {"tq": (0.8, -1.0, 0.35), "side": (1.0, 0.0, 0.1), "front": (0.0, -1.0, 0.15), "back": (-0.7, 1.0, 0.45),
     "top": (0.3, -0.2, 1.0), "low": (0.9, -0.6, -0.05)}
out = []
for v in views:
    pk.aim(cam, tgt + Vector(D[v]).normalized() * dist, tgt)
    p = os.path.join(k.dir, "renders", "pc_" + v + ".png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    out.append(p)
print("HEADLESS_RESULT", out)
