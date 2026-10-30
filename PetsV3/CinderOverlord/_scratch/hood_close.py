# blender -b --factory-startup --python CinderOverlord/_scratch/hood_close.py -- CinderOverlord [frames=0,20] [res=800]
# r12: back-view close-ups of the cobra hood from FIXED cameras (aimed once at the rest pose, so the idle sway shows as
# the hood moving with the neck): views back (0,1,0.25) and game (0.45,1,0.85), target = the Neck3 joint + 0.12 z,
# distance 3.4 -> renders/hood_<view>_idle_<f>.png (the sheet is made outside Blender)
import sys, runpy, os, json
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
frames = [int(v) for v in opts.get("frames", "0,20").split(",")]
res = int(opts.get("res", "800"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
pk = R3["pk"]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
k.set_action("idle")
sc.frame_set(0)
arm = k.arm
arm.data.pose_position = "REST"
bpy.context.view_layer.update()
t = arm.matrix_world @ arm.pose.bones["Neck3"].head + Vector((0, 0, 0.12))
arm.data.pose_position = "POSE"
VIEWS = {"back": (0.0, 1.0, 0.25), "game": (0.45, 1.0, 0.85)}
files = []
for f in frames:
    sc.frame_set(f)
    for v, d in VIEWS.items():
        pk.aim(sc.camera, t + Vector(d).normalized() * 3.4, t)
        p = os.path.join(k.dir, "renders", "hood_%s_idle_%02d.png" % (v, f))
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        files.append(p)
print("HOODCLOSE " + json.dumps(files))
