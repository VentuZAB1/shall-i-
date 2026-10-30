# blender -b --factory-startup --python BlizzardRoc/_scratch/step_check.py -- <Name> : (builder D scratch) the largest
# per-frame bone rotation step in every clip (rule: never > ~60 deg between adjacent frames) + pose-limit maxima
# (Neck / Neck2 local angles, Chest vs Spine) from the baked pose bones
import sys, runpy, json, math
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
out = {}
for clip, (n, loop) in k.clips.items():
    k.set_action(clip)
    prev = None
    worst = (0.0, "", -1)
    lim = {"Neck": 0.0, "Neck2": 0.0, "Chest": 0.0}
    for f in range(0, n + 1):
        sc.frame_set(f)
        cur = {pb.name: pb.matrix.to_quaternion() for pb in k.arm.pose.bones}
        for b in lim:
            if b in k.arm.pose.bones:
                q = k.arm.pose.bones[b].rotation_quaternion
                lim[b] = max(lim[b], math.degrees(2 * math.acos(min(1.0, abs(q.w)))))
        if prev:
            for b, q in cur.items():
                d = math.degrees(q.rotation_difference(prev[b]).angle)
                if d > 180:
                    d = 360 - d
                if d > worst[0]:
                    worst = (round(d, 1), b, f)
        prev = cur
    out[clip] = {"max_step": worst, "local_max": {b: round(v, 1) for b, v in lim.items()}}
print("STEP_RESULT " + json.dumps(out))
