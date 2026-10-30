# blender -b --factory-startup --python CinderOverlord/_scratch/ang_probe.py -- <Name> <clip> bone,bone
# per-frame rotation angle (deg) of each bone vs its rest (matrix_basis), + max, + max step per frame (rise vs fall)
import sys, runpy, json, math
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, bones = argv[0], argv[1], argv[2].split(",")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
n = k.clips[clip][0]
k.set_action(clip)
arm = k.arm
A = {b: [] for b in bones}
for f in range(0, n + 1):
    bpy.context.scene.frame_set(f)
    for b in bones:
        A[b].append(math.degrees(arm.pose.bones[b].matrix_basis.to_quaternion().angle))
out = {}
for b, a in A.items():
    steps = [a[i + 1] - a[i] for i in range(len(a) - 1)]
    out[b] = {"max": round(max(a), 2), "rise_peak": round(max(steps), 2), "fall_peak": round(-min(steps), 2),
              "fall_peak_frame": steps.index(min(steps))}
print("ANG " + json.dumps(out))
