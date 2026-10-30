# blender -b --factory-startup --python <Pet>/_scratch/verify.py -- <Name> [track=Bone,Bone] [knees=Shin_FL,Shin_FR] [frames=clip:f;clip:f]
# One saved verification run (writes <Name>/_scratch/verify.json and prints VERIFY_RESULT):
#  - per clip: chest_vs_spine = max angle of the Chest bone's LOCAL rotation (the Chest is parented to the Spine, so
#    this is the chest-vs-spine angle); neck_max (Neck local angle); jaw_max (Jaw local angle); head_pitch_up (head
#    forward axis vs rest, armature space, + = up); max_swing (largest armature-space change of any bone between two
#    adjacent frames); end_vs_start (largest per-bone rotation between frame 0 and the last frame) and end_vs_rest /
#    start_vs_rest for one-shots
#  - track: world z of the listed bones' heads per frame (min + the frames asked)
#  - knees: interior knee-angle change vs rest (deg, + = folded more) at the frames asked
#  - collisions: overlap_report step 1 WITH the joints() hinges and WITHOUT them (raw), per clip
import sys, runpy, json, math, os
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
track = [b for b in opts.get("track", "").split(",") if b]
knees = [b for b in opts.get("knees", "").split(",") if b]
asked = {}
for t in [t for t in opts.get("frames", "").split(";") if t]:
    c, f = t.split(":")
    asked.setdefault(c, []).append(int(f))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"](name, save=False)
k, m = R3["STATE"]["k"], R3["STATE"]["m"]
import bpy
arm = k.arm
sc = bpy.context.scene


def ang(q):
    a = math.degrees(q.angle)
    return min(a, 360.0 - a)


def local(b):
    return ang(arm.pose.bones[b].rotation_quaternion) if b in arm.pose.bones else 0.0


def knee_angle(shin):
    pb = arm.pose.bones[shin]
    par = pb.parent
    a = (par.head - pb.head).normalized()
    c = (pb.tail - pb.head).normalized()
    return math.degrees(a.angle(c))


rest_knee = {}
k.set_action("idle")
for p in arm.pose.bones:
    p.rotation_quaternion = (1, 0, 0, 0)
    p.location = (0, 0, 0)
bpy.context.view_layer.update()
for s in knees:
    rest_knee[s] = knee_angle(s)
out = {"clips": {}}
hb = arm.data.bones.get("Head")
rest_fwd = (hb.tail_local - hb.head_local).normalized()
rest_pitch = math.degrees(math.atan2(rest_fwd.z, -rest_fwd.y))
for clip, (n, loop) in k.clips.items():
    k.set_action(clip)
    r = {"frames": n, "loop": loop, "chest_vs_spine": [0, -1], "neck_max": [0, -1], "jaw_max": [0, -1],
         "head_pitch_up": [0, -1], "max_swing": [0, "", -1]}
    prev = None
    poses = {}
    tr = {b: {} for b in track}
    for f in range(0, n + 1):
        sc.frame_set(f)
        cur = {p.name: p.matrix.to_quaternion() for p in arm.pose.bones}
        poses[f] = {p.name: p.rotation_quaternion.copy() for p in arm.pose.bones}
        if prev:
            for b, q in cur.items():
                a = ang(prev[b].rotation_difference(q))
                if a > r["max_swing"][0]:
                    r["max_swing"] = [round(a, 1), b, f]
        prev = cur
        for key, b in (("chest_vs_spine", "Chest"), ("neck_max", "Neck"), ("jaw_max", "Jaw")):
            a = local(b)
            if a > r[key][0]:
                r[key] = [round(a, 2), f]
        p = arm.pose.bones["Head"]
        d = (p.tail - p.head).normalized()
        up = math.degrees(math.atan2(d.z, -d.y)) - rest_pitch
        if up > r["head_pitch_up"][0]:
            r["head_pitch_up"] = [round(up, 2), f]
        for b in track:
            tr[b][f] = round((arm.matrix_world @ arm.pose.bones[b].head).z, 4)
        if f in asked.get(clip, []) and knees:
            r.setdefault("knee_fold", {})[f] = {s: round(rest_knee[s] - knee_angle(s), 1) for s in knees}
    def maxdiff(A, B):
        best = (0.0, "")
        for b in A:
            a = ang(A[b].rotation_difference(B[b]))
            if a > best[0]:
                best = (round(a, 3), b)
        return list(best)
    ident = {b: q.copy() for b, q in poses[0].items()}
    for b in ident:
        ident[b].identity()
    r["end_vs_start"] = maxdiff(poses[0], poses[n])
    if not loop:
        r["end_vs_rest"] = maxdiff(ident, poses[n])
        r["start_vs_rest"] = maxdiff(ident, poses[0])
    for b in track:
        lo = min(tr[b].items(), key=lambda x: x[1])
        r.setdefault("track", {})[b] = {"min": [lo[1], lo[0]], "at": {f: tr[b][f] for f in asked.get(clip, [])}}
    out["clips"][clip] = r
# collisions with and without the joints() hinge exemption (step 1)
bk = R3["blockkit"]
js = m.joints() if hasattr(m, "joints") else None
with_j = bk.overlap_report(k, m.check_pairs(), step=1, joints=js)
raw = bk.overlap_report(k, m.check_pairs(), step=1, joints=None)
out["collisions_with_hinges"] = {c: v for c, v in with_j.items() if v}
out["collisions_raw_no_hinges"] = {c: v for c, v in raw.items() if v}
out["hinges"] = [[list(map(float, a)), list(map(float, b)), r_, bn] for a, b, r_, bn in (js or [])]
path = os.path.join(k.dir, "_scratch", "verify.json")
with open(path, "w") as fh:
    json.dump(out, fh, indent=1, default=str)
print("VERIFY_RESULT " + json.dumps(out, default=str))
