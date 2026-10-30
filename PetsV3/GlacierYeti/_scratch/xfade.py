# blender -b --factory-startup --python GlacierYeti/_scratch/xfade.py -- <Name> [render=1]
# OFFLINE PROXY of the CreatureAnimator idle <-> walk cross-fade (final85 C5). Studio is off-limits for builders, so
# this replays the runtime's blend in Blender, using the logic of ReplicatedStorage/CreatureAnimator.lua (read-only
# snapshot in ROBLOX PLAYBOOK/slingshot-code):
#   - weights: w += (target - w) * min(1, dt * 6) per step (approach(), rate 6 for idle / walk), stepped at 60 fps;
#   - pose: per bone, cf = Lerp(idle frame, walk frame, w_walk / (w_idle + w_walk)) on the Motor6D (local) transform
#     = per pose bone: quaternion slerp + location lerp of matrix_basis;
#   - phases: idle advances dt / len; walk starts at phase 0 and advances at the clip rate (pet moving at clip speed).
# Cases: START idle f0 / f40 / f75 -> walk, STOP walk f24 -> idle f0. Each case is baked into a temporary one-shot
# action (one key per 60 fps step) and checked with the same gates as step 1: ground min z, overlap_report (step 1,
# with the joints() hinges), plus the largest per-step bone rotation change in the blend vs in the pure walk ("pop").
import sys, runpy, json, math, os
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
do_render = len(argv) > 1 and argv[1].endswith("1")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"](name, save=False)
k, m = R3["STATE"]["k"], R3["STATE"]["m"]
bk = R3["blockkit"]
pk = R3["pk"]
import bpy
sc = bpy.context.scene
arm = k.arm
FPS, DT, RATE, STEPS = 30.0, 1.0 / 60.0, 6.0, 40
n_idle = k.clips["idle"][0]
n_walk = k.clips["walk"][0]
bones = [pb.name for pb in arm.pose.bones]


def pose_at(clip, f):
    k.set_action(clip)
    fi = int(math.floor(f))
    sc.frame_set(fi, subframe=f - fi)
    return {b: (arm.pose.bones[b].rotation_quaternion.copy(), arm.pose.bones[b].location.copy()) for b in bones}


def blend(pa, pb, w):
    out = {}
    for b in bones:
        qa, la = pa[b]
        qb, lb = pb[b]
        if qa.dot(qb) < 0:
            qb = -qb
        out[b] = (qa.slerp(qb, w), la.lerp(lb, w))
    return out


def qang(a, b):
    d = abs(a.dot(b))
    return math.degrees(2 * math.acos(min(1.0, d)))


cases = [("start_idle00", "start", 0.0), ("start_idle40", "start", 40.0), ("start_idle75", "start", 75.0),
         ("stop_walk24", "stop", 24.0)]
res = {}
made = []
for cname, kind, f0 in cases:
    w_walk = 0.0 if kind == "start" else 1.0
    tgt = 1.0 if kind == "start" else 0.0
    ph_i = (f0 / n_idle) if kind == "start" else 0.0
    ph_w = 0.0 if kind == "start" else f0 / n_walk
    poses, ws, pure = [], [], []
    for i in range(STEPS + 1):
        pi = pose_at("idle", (ph_i % 1.0) * n_idle)
        pw = pose_at("walk", (ph_w % 1.0) * n_walk)
        poses.append(blend(pi, pw, w_walk))
        pure.append(pw if kind == "start" else pi)
        ws.append(round(w_walk, 3))
        w_walk += (tgt - w_walk) * min(1.0, DT * RATE)
        ph_i += DT / (n_idle / FPS)
        ph_w += DT / (n_walk / FPS)
    # largest per-step change (deg) of any bone's local rotation: blend vs the pure target clip
    def maxstep(seq):
        best = (0.0, "", -1)
        for j in range(len(seq) - 1):
            for b in bones:
                a = qang(seq[j][b][0], seq[j + 1][b][0])
                if a > best[0]:
                    best = (round(a, 2), b, j)
        return best
    act = k.new_action("xf_" + cname, STEPS, False)
    for j, P in enumerate(poses):
        for b in bones:
            pb = arm.pose.bones[b]
            pb.rotation_quaternion, pb.location = P[b]
            pb.keyframe_insert("rotation_quaternion", frame=j, group=b)
            pb.keyframe_insert("location", frame=j, group=b)
    for fc in k.fcurves():
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    made.append("xf_" + cname)
    # ground min z + lowest / highest foot sole per step
    lo = (9.0, -1)
    for f in range(0, STEPS + 1):
        sc.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        ev = k.main.evaluated_get(dg)
        me = ev.to_mesh()
        z = min((ev.matrix_world @ v.co).z for v in me.vertices)
        ev.to_mesh_clear()
        if z < lo[0]:
            lo = (round(z, 3), f)
    res[cname] = {"weights_walk": [ws[0], ws[6], ws[12], ws[24], ws[-1]], "ground_min_z": lo,
                  "max_step_blend": maxstep(poses), "max_step_pure": maxstep(pure)}
js = m.joints() if hasattr(m, "joints") else None
rep = bk.overlap_report(k, m.check_pairs(), step=1, clips=made, joints=js)
for cname, _, _ in cases:
    res[cname]["collisions"] = {kk: v for kk, v in rep.get("xf_" + cname, {}).items() if v}
out = os.path.join(k.dir, "_scratch", "xfade.json")
json.dump(res, open(out, "w"), indent=1, default=str)
if do_render:
    import json as _j
    cam = sc.camera
    sc.render.resolution_x = sc.render.resolution_y = 300
    k.set_action("idle")
    sc.frame_set(0)
    loc, c = pk.camera_for(k, "tq")
    pk.aim(cam, loc, c)
    files = []
    for cname in ("start_idle40", "stop_walk24"):
        k.set_action("xf_" + cname)
        for f in (0, 3, 6, 10, 16, 24, 40):
            sc.frame_set(f)
            p = os.path.join(k.dir, "renders", "xfade_%s_%02d.png" % (cname, f))
            sc.render.filepath = p
            bpy.ops.render.render(write_still=True)
            files.append(p)
    _j.dump({"files": files}, open(os.path.join(k.dir, "renders", "_xfade.json"), "w"))
print("XFADE_RESULT " + json.dumps(res, default=str))
