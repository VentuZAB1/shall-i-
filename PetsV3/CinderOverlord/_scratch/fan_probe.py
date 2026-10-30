# blender -b --factory-startup --python CinderOverlord/_scratch/fan_probe.py -- <Name> <clip> <f,f,...>
# Front-view (x-z plane, camera looking along +y) tilt of each Crown_* bone from vertical (deg, + = toward +x) per
# frame, the change vs f0, and the fan spread (Crown_5 - Crown_1). Also the 3-D angle each blade moved vs f0.
import sys, runpy, json, math
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, frames = argv[0], argv[1], [int(v) for v in argv[2].split(",")]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
k.set_action(clip)
arm = k.arm
sc = bpy.context.scene
bones = ["Crown_%d" % i for i in range(1, 6)]
out = {}
ref = {}
for f in frames:
    sc.frame_set(f)
    bpy.context.view_layer.update()
    row = {}
    for b in bones:
        pb = arm.pose.bones[b]
        h = arm.matrix_world @ pb.head
        t = arm.matrix_world @ pb.tail
        d = (t - h).normalized()
        tilt = math.degrees(math.atan2(d.x, d.z))
        if f == frames[0]:
            ref[b] = (tilt, d.copy())
        moved = math.degrees(ref[b][1].angle(d)) if b in ref else 0.0
        row[b] = {"front_tilt": round(tilt, 1), "d_front": round(tilt - ref[b][0], 1), "moved3d": round(moved, 1)}
    row["fan_spread_1_5"] = round(row["Crown_5"]["front_tilt"] - row["Crown_1"]["front_tilt"], 1)
    out[f] = row
print("FAN_RESULT " + json.dumps(out))
