# blender -b --factory-startup --python CoralCrusher/_scratch/plant_probe.py -- <Name> <clip> [bone,...]
# per planted foot: max drift of the foot bone head + tail from frame 0 over the clip (are the IK feet still planted?)
# + optional: per-frame rotation angle (deg) of extra bones vs the rest pose (to read wave peaks / holds)
import sys, runpy, json, math
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip = argv[0], argv[1]
extra = argv[2].split(",") if len(argv) > 2 else []
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
n = k.clips[clip][0]
k.set_action(clip)
arm = k.arm
feet = [k.legs2[l]["foot"] for l in k.legs2]
sc = bpy.context.scene
base, drift, ang = {}, {b: 0.0 for b in feet}, {b: [] for b in extra}
for f in range(0, n + 1):
    sc.frame_set(f)
    for b in feet:
        pb = arm.pose.bones[b]
        p = (arm.matrix_world @ pb.head, arm.matrix_world @ pb.tail)
        if f == 0:
            base[b] = p
        else:
            drift[b] = max(drift[b], (p[0] - base[b][0]).length, (p[1] - base[b][1]).length)
    for b in extra:
        q = arm.pose.bones[b].matrix_basis.to_quaternion()
        ang[b].append(round(math.degrees(q.angle), 1))
print("PROBE " + json.dumps({"foot_drift": {b: round(v, 4) for b, v in drift.items()}, "angles": ang}))
