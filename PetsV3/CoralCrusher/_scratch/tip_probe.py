# blender -b --factory-startup --python CoralCrusher/_scratch/tip_probe.py -- <Name> <clip> <bone> f,f,f  -> world head/tail per frame
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, bone = argv[0], argv[1], argv[2]
frames = [int(x) for x in argv[3].split(",")]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
k.set_action(clip)
arm = k.arm
out = {}
for f in frames:
    bpy.context.scene.frame_set(f)
    pb = arm.pose.bones[bone]
    out[f] = [round(c, 3) for c in (arm.matrix_world @ pb.tail)]
print("TIP " + json.dumps(out))
