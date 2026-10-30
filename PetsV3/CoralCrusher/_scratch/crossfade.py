# blender -b --factory-startup --python CoralCrusher/_scratch/crossfade.py -- <Name> [secs=0.3] [view=tq]
# Review M1 evidence: simulates the CreatureAnimator idle -> walk crossfade (walk weight ramps 0 -> 1 over `secs`,
# idle weight 1 - w; per bone quaternion slerp / location lerp of idle f0 and the walk clip running from phase 0 at
# its natural 30 fps). Renders 9 frames to renders/xfade_<view>_<i>.png + prints per-frame body yaw and the ankle
# drift of every leg against frame 0 (the feet are NOT re-planted during a runtime blend - this shows how much
# they move).
import sys, runpy, json, os, math
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
secs = float(opts.get("secs", "0.3"))
view = opts.get("view", "tq")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from mathutils import Vector, Quaternion
pk = R3["pk"]
R3["full"](name, save=False)
k = R3["STATE"]["k"]
arm = k.arm
sc = bpy.context.scene
acts = {a.name: a for a in bpy.data.actions}


def grab(action, frame):
    arm.animation_data.action = acts[action]
    fi = int(math.floor(frame))
    sc.frame_set(fi, subframe=frame - fi)
    out = {}
    for pb in arm.pose.bones:
        q = pb.rotation_quaternion.copy() if pb.rotation_mode == "QUATERNION" else pb.rotation_euler.to_quaternion()
        out[pb.name] = (q, pb.location.copy())
    return out


idle0 = grab("idle", 0)
N = 9
poses = []
for i in range(N):
    t = secs * i / (N - 1)
    w = t / secs
    wk = grab("walk", t * 30.0)
    poses.append((t, w, {b: (idle0[b][0].slerp(wk[b][0], w), idle0[b][1].lerp(wk[b][1], w)) for b in idle0}))
arm.animation_data.action = None
g = bpy.data.objects.get("Ground")
loc, tgt = pk.camera_for(k, view)
pk.aim(sc.camera, loc, tgt)
sc.render.resolution_x = sc.render.resolution_y = 300
feet = [b.name for b in arm.pose.bones if b.name.startswith("Foot_")]
rep = []
base = None
for i, (t, w, P) in enumerate(poses):
    for pb in arm.pose.bones:
        q, l = P[pb.name]
        if pb.rotation_mode == "QUATERNION":
            pb.rotation_quaternion = q
        else:
            pb.rotation_euler = q.to_euler(pb.rotation_mode)
        pb.location = l
    bpy.context.view_layer.update()
    fp = {f: arm.matrix_world @ arm.pose.bones[f].head for f in feet}
    if base is None:
        base = fp
    yaw = math.degrees(P["Spine"][0].to_euler("XYZ").z) if "Spine" in P else 0
    rep.append({"t": round(t, 3), "w": round(w, 3), "spine_q_angle_deg": round(math.degrees(P["Spine"][0].angle), 1),
                "max_foot_drift": round(max((fp[f] - base[f]).length for f in feet), 3),
                "min_foot_z": round(min(fp[f].z for f in feet), 3)})
    sc.render.filepath = os.path.join(k.dir, "renders", "xfade_%s_%d.png" % (view, i))
    bpy.ops.render.render(write_still=True)
print("XFADE_RESULT " + json.dumps(rep))
