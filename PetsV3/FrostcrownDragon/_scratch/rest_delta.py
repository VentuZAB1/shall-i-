# blender -b --factory-startup --python FrostcrownDragon/_scratch/rest_delta.py -- <Name> : (builder D scratch) for every
# clip, the largest per-bone rotation difference (deg, armature-space pose matrices) and the largest root-of-bone
# position difference between the LAST frame and (a) the clip's frame 0, (b) f0 of a reference clip (arg 2, default idle) = the ground rest pose
import sys, runpy, json, math
argv = sys.argv[sys.argv.index("--") + 1:]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](argv[0], save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene


def snap(clip, f):
    k.set_action(clip)
    sc.frame_set(f)
    return {pb.name: (pb.matrix.to_quaternion(), pb.matrix.translation.copy()) for pb in k.arm.pose.bones}


def diff(a, b):
    worst, wb, dpos = 0.0, "", 0.0
    for n in a:
        qa, pa = a[n]
        qb, pb_ = b[n]
        ang = math.degrees(qa.rotation_difference(qb).angle)
        if ang > 180:
            ang = 360 - ang
        if ang > worst:
            worst, wb = ang, n
        dpos = max(dpos, (pa - pb_).length)
    return [round(worst, 2), wb, round(dpos, 4)]


REF = argv[1] if len(argv) > 1 else "idle"          # clip whose f0 is the ground rest pose
rest = snap(REF, 0)
out = {}
for clip, (n, loop) in k.clips.items():
    last = snap(clip, n)
    out[clip] = {"last": n, "vs_own_f0": diff(last, snap(clip, 0)), "vs_rest(" + REF + " f0)": diff(last, rest)}
print("REST_DELTA " + json.dumps(out))
