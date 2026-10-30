# blender -b --factory-startup --python _tools/headless_pose_close.py -- <Name> <act:frame,...> <Bone> <dist>
#   [views=tq,side,front] [res=500] [off=x,y,z]
# Posed close-ups: for each pick, aim at the posed head of <Bone> (+ off, armature axes) from each view direction
# -> renders/pclose_<view>_<act>_<f>.png
import sys, runpy, os, json
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name, bone, dist = argv[0], argv[2], float(argv[3])
picks = [(t.rsplit(":", 1)[0], int(t.rsplit(":", 1)[1])) for t in argv[1].split(",")]
opts = dict(a.split("=", 1) for a in argv[4:] if "=" in a)
views = opts.get("views", "tq,side,front").split(",")
res = int(opts.get("res", "500"))
off = Vector([float(v) for v in opts.get("off", "0,0,0").split(",")])
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"](name, save=False)
k = R3["STATE"]["k"]
pk = R3["pk"]
import bpy
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
D = {"tq": (0.8, -1.0, 0.35), "side": (1.0, 0.0, 0.1), "front": (0.0, -1.0, 0.15), "back": (-0.5, 1.0, 0.45),
     "game": (0.45, 1.0, 0.85), "below": (0.6, -0.6, -0.35)}
files = []
for act, f in picks:
    k.set_action(act)
    sc.frame_set(f)
    t = k.arm.matrix_world @ k.arm.pose.bones[bone].head + off
    for v in views:
        pk.aim(sc.camera, t + Vector(D[v]).normalized() * dist, t)
        p = os.path.join(k.dir, "renders", "pclose_%s_%s_%02d.png" % (v, act, f))
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        files.append(p)
print("HEADLESS_RESULT " + json.dumps(files))
