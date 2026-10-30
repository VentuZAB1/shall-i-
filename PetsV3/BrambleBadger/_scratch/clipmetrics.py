# blender -b --factory-startup --python BrambleBadger/_scratch/clipmetrics.py -- <Name>
# Builder A clip evidence (review 3 M-4): per clip, every frame (step 1):
#   swing      max per-frame orientation change of any bone (armature space), limb bones and all bones
#   qflips     quaternion sign flips: consecutive rotation keys with dot < 0 (fcurves) + sampled basis frames with dot < 0
#   end_delta  max basis rotation (deg) / location (units) of any bone at the last frame and at last-1, vs the bind pose
#   chest      max Chest-vs-Spine angle (Chest basis), neck = max Neck basis angle
#   head_up    max world pitch-up of the Head bone direction vs rest (deg), head_yaw_rate = max |d yaw| / frame (deg)
# -> <Name>/_scratch/clipmetrics.json
import sys, runpy, os, json, math
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
R3 = runpy.run_path(os.path.join(ROOT, "run3.py"))
R3["full"](name, save=False)
k = R3["STATE"]["k"]
import bpy
sc = bpy.context.scene
arm = k.arm
LIMB = ("Leg_", "Shin_", "Foot_", "Claw")


def ang(q):
    w = max(-1.0, min(1.0, abs(q.w)))
    return math.degrees(2 * math.acos(w))


def head_dir(pb):
    m = pb.matrix
    return Vector((m[0][1], m[1][1], m[2][1])).normalized()


rest_head = arm.data.bones["Head"].matrix_local
d0 = Vector((rest_head[0][1], rest_head[1][1], rest_head[2][1])).normalized()
el0 = math.degrees(math.asin(max(-1, min(1, d0.z))))
out = {}
IDLE0 = None


def snap():
    return {pb.name: (pb.rotation_quaternion.copy(), pb.location.copy()) for pb in arm.pose.bones}


def delta(a, b):
    r = max((math.degrees(a[x][0].rotation_difference(b[x][0]).angle), x) for x in a)
    l = max((a[x][1] - b[x][1]).length for x in a)
    return round(min(r[0], 360 - r[0]), 3), round(l, 4), r[1]


for clip, (n, loop) in k.clips.items():
    k.set_action(clip)
    prevq, prevb = {}, {}
    sw_all, sw_limb, sw_loc = (0.0, "", 0), (0.0, "", 0), (0.0, "", 0)
    sw_loc_limb = (0.0, "", 0)
    by_bone = {}
    flips_s = 0
    chest = neck = head_up = 0.0
    yaw_rate = (0.0, 0)
    prev_yaw = None
    ends = {}
    for f in range(0, n + 1):
        sc.frame_set(f)
        for pb in arm.pose.bones:
            q = pb.matrix.to_quaternion()
            qb = pb.rotation_quaternion.copy()
            if pb.name in prevq:
                a = math.degrees(prevq[pb.name].rotation_difference(q).angle)
                a = min(a, 360 - a)
                if a > sw_all[0]:
                    sw_all = (a, pb.name, f)
                if pb.name.startswith(LIMB) and a > sw_limb[0]:
                    sw_limb = (a, pb.name, f)
                al = math.degrees(prevb[pb.name].rotation_difference(qb).angle)
                al = min(al, 360 - al)
                if al > sw_loc[0]:
                    sw_loc = (al, pb.name, f)
                if pb.name.startswith(LIMB) and al > sw_loc_limb[0]:
                    sw_loc_limb = (al, pb.name, f)
                if pb.name.startswith(LIMB) and al > by_bone.get(pb.name, (0.0, 0))[0]:
                    by_bone[pb.name] = (round(al, 2), f)
                if prevb[pb.name].dot(qb) < 0:
                    flips_s += 1
            prevq[pb.name], prevb[pb.name] = q, qb
        cq = arm.pose.bones["Chest"].rotation_quaternion
        chest = max(chest, ang(cq))
        if "Neck" in arm.pose.bones:
            neck = max(neck, ang(arm.pose.bones["Neck"].rotation_quaternion))
        d = head_dir(arm.pose.bones["Head"])
        head_up = max(head_up, math.degrees(math.asin(max(-1, min(1, d.z)))) - el0)
        yw = math.degrees(math.atan2(d.x, -d.y))
        if prev_yaw is not None and abs(yw - prev_yaw) > yaw_rate[0]:
            yaw_rate = (abs(yw - prev_yaw), f)
        prev_yaw = yw
        if f == 0:
            F0 = snap()
            if IDLE0 is None:
                IDLE0 = F0
        if f in (n - 1, n):
            S = snap()
            ends["f%d_vs_f0" % f] = delta(S, F0)
            ends["f%d_vs_idle_f0" % f] = delta(S, IDLE0)
            mr = max(ang(pb.rotation_quaternion) for pb in arm.pose.bones)
            ml = max(pb.location.length for pb in arm.pose.bones)
            br = max(arm.pose.bones, key=lambda p: ang(p.rotation_quaternion)).name
            ends["f%d_vs_bind" % f] = {"max_rot_deg": round(mr, 3), "max_loc": round(ml, 4), "worst_bone": br}
    # key-level sign flips (fcurve rotation_quaternion keys)
    flips_k = 0
    keys = {}
    for fc in k.fcurves():
        if fc.data_path.endswith("rotation_quaternion"):
            b = fc.data_path.split('"')[1]
            for kp in fc.keyframe_points:
                keys.setdefault(b, {}).setdefault(int(round(kp.co.x)), [0, 0, 0, 0])[fc.array_index] = kp.co.y
    for b, fr in keys.items():
        fs = sorted(fr)
        for a_, b_ in zip(fs, fs[1:]):
            if sum(x * y for x, y in zip(fr[a_], fr[b_])) < 0:
                flips_k += 1
    out[clip] = {"frames": n, "loop": loop,
                 "swing_max_all": [round(sw_all[0], 2), sw_all[1], sw_all[2]],
                 "swing_max_limb": [round(sw_limb[0], 2), sw_limb[1], sw_limb[2]],
                 "swing_local_max": [round(sw_loc[0], 2), sw_loc[1], sw_loc[2]],
                 "swing_local_max_limb": [round(sw_loc_limb[0], 2), sw_loc_limb[1], sw_loc_limb[2]],
                 "local_max_by_limb_bone": by_bone,
                 "quat_flips_keys": flips_k, "quat_flips_sampled": flips_s,
                 "chest_vs_spine_max": round(chest, 2), "neck_max": round(neck, 2),
                 "head_pitch_up_world_max": round(head_up, 2),
                 "head_yaw_rate_max": [round(yaw_rate[0], 2), yaw_rate[1]],
                 "end": ends}
out["_definitions"] = {
    "swing_max_all / swing_max_limb": "[deg, bone, frame]: the largest change between two adjacent frames (f-1 -> f, step 1) of a bone's "
        "ARMATURE-SPACE orientation (pose_bone.matrix rotation, so it includes the parents' motion = the limb as seen in "
        "the world), over every bone / over Leg_*, Shin_*, Foot_*, Claw* bones. Limit ~60 deg.",
    "swing_local_max": "[deg, bone, frame]: the same, but of the bone's LOCAL rotation (pose_bone.rotation_quaternion, relative "
        "to its parent) - comparable to decoding the raw keyed / exported bone quaternions.",
    "quat_flips_keys": "consecutive rotation_quaternion keys of one bone with a 4D dot product < 0 (a sign flip), all bones",
    "quat_flips_sampled": "the same test on the evaluated local quaternion at every frame",
    "chest_vs_spine_max": "largest rotation angle of the Chest bone's local rotation (= the bend between chest and spine)",
    "neck_max": "largest rotation angle of the Neck bone's local rotation",
    "head_pitch_up_world_max": "largest rise (deg) of the Head bone's direction above its rest elevation, world space",
    "head_yaw_rate_max": "[deg, frame]: largest change of the Head bone's world heading between adjacent frames",
    "end": "fN_vs_f0 / fN_vs_idle_f0 = [max local rotation diff deg, max location diff, bone] of the last frames vs the clip's "
        "own frame 0 / vs the idle's frame 0; fN_vs_bind = vs the bind pose (the planted-leg solve sits ~4.6 deg off bind)",
}
p = os.path.join(ROOT, name, "_scratch", "clipmetrics.json")
open(p, "w").write(json.dumps(out, indent=1))
print("HEADLESS_RESULT " + json.dumps(out))
