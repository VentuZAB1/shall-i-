# blender ... -- <Name> <clip> <frame> bone,bone  -> world head positions
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, fr, bones = argv[0], argv[1], int(argv[2]), argv[3].split(",")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
k.set_action(clip)
bpy.context.scene.frame_set(fr)
print("JOINTS " + json.dumps({b: [round(v, 3) for v in (k.arm.matrix_world @ k.arm.pose.bones[b].head)] for b in bones}))
