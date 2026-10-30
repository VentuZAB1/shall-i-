import sys, runpy
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, bone = argv[0], argv[1], argv[2]
f0, f1 = int(argv[3]), int(argv[4])
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
k.set_action(clip)
pb = k.arm.pose.bones[bone]
for f in range(f0, f1 + 1):
    bpy.context.scene.frame_set(f)
    q = pb.rotation_quaternion
    print("Q", f, [round(v, 3) for v in q], [round(v, 3) for v in pb.location])
act = k.arm.animation_data.action
for fc in R3["pk"].Pet.fcurves(k) if hasattr(R3["pk"].Pet, "fcurves") else []:
    pass
