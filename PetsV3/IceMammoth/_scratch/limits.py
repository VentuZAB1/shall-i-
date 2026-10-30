# blender -b --factory-startup --python IceMammoth/_scratch/limits.py -- <Name> [neck_bones] [head_bone]
# Pose-limit report per clip: max adjacent-frame swing of any bone (armature space, deg), max Neck local angle,
# max Chest-vs-Spine local angle, max head pitch-up vs rest (head forward axis in the YZ plane, + = up).
import sys, runpy, json, math
import bpy
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
necks = argv[1].split(",") if len(argv) > 1 and argv[1] else ["Neck"]
headb = argv[2] if len(argv) > 2 else "Head"
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"](name, save=False)
k = R3["STATE"]["k"]
arm = k.arm
sc = bpy.context.scene
out = {}
skip = ("Root",)
for clip, (n, loop) in k.clips.items():
    k.set_action(clip)
    prev = None
    swing = (0.0, "", -1)
    neck = (0.0, -1)
    chest = (0.0, -1)
    up = (0.0, -1)
    hb = arm.data.bones.get(headb)
    rest_fwd = (hb.tail_local - hb.head_local).normalized() if hb else None
    rest_pitch = math.degrees(math.atan2(rest_fwd.z, -rest_fwd.y)) if hb else 0.0
    for f in range(0, n + 1):
        sc.frame_set(f)
        cur = {pb.name: pb.matrix.to_quaternion() for pb in arm.pose.bones if pb.name not in skip}
        if prev:
            for b, q in cur.items():
                a = math.degrees(prev[b].rotation_difference(q).angle)
                a = min(a, 360.0 - a)
                if a > swing[0]:
                    swing = (round(a, 1), b, f)
        prev = cur
        for nb in necks:
            if nb in arm.pose.bones:
                a = math.degrees(arm.pose.bones[nb].rotation_quaternion.angle)
                if a > neck[0]:
                    neck = (round(a, 1), f)
        if "Chest" in arm.pose.bones:
            a = math.degrees(arm.pose.bones["Chest"].rotation_quaternion.angle)
            if a > chest[0]:
                chest = (round(a, 1), f)
        if hb:
            pb = arm.pose.bones[headb]
            d = (pb.tail - pb.head).normalized()
            p = math.degrees(math.atan2(d.z, -d.y)) - rest_pitch
            if p > up[0]:
                up = (round(p, 1), f)
    out[clip] = {"max_swing_deg": swing, "neck_max": neck, "chest_vs_spine": chest, "head_pitch_up": up}
print("LIMITS_RESULT " + json.dumps(out))
