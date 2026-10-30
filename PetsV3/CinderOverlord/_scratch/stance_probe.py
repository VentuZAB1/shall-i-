# blender -b --factory-startup --python CinderOverlord/_scratch/stance_probe.py -- CinderOverlord [step=2]
# r11 (raised cobra stance) - per clip, every `step` frames:
#   angles : each neck bone's rotation vs rest (deg, matrix_basis), the Spine (chest base) vs rest, the summed neck
#            pitch (x) and the head + neck world pitch-up of the Head bone vs rest (deg, + = nose up)
#   screen : on the fixed GAME camera (gamelook framing, idle f0), the head group's centre / top / bottom in px (600 px
#            frame, y down) and the GAP between the head group's lowest pixel and the highest pixel of the ground body
#            (Spine..Tail4, Body*): > 0 = the head and crown stand clear above the body line
import sys, runpy, json, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
step = int(opts.get("step", "2"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from bpy_extras.object_utils import world_to_camera_view
R3["full"](name, save=False)
k = R3["STATE"]["k"]
pk = R3["pk"]
sc = bpy.context.scene
RES = 600
sc.render.resolution_x = sc.render.resolution_y = RES
arm = k.arm
k.set_action("idle")
sc.frame_set(0)
loc, tgt = pk.camera_for(k, "game")
pk.aim(sc.camera, loc, tgt)
cam = sc.camera
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]
HEADG = set(["Head", "Jaw", "Mouth"] + ["Crown_%d" % i for i in range(1, 6)])
BODYG = set(["Spine", "Body1", "Body2", "Body3", "Body4", "Tail1", "Tail2", "Tail3", "Tail4", "Tail_Tip"])
hidx = [i for i, g in enumerate(own) if g in HEADG]
bidx = [i for i, g in enumerate(own) if g in BODYG]
R0 = {b.name: b.matrix_local.to_quaternion() for b in arm.data.bones}


def head_fwd():
    pb = arm.pose.bones["Head"]
    M = (arm.matrix_world @ pb.matrix).to_3x3()
    return (M @ (arm.data.bones["Head"].matrix_local.to_3x3().inverted() @ Vector((0, -1, 0)))).normalized()


def pitch_of(v):
    return math.degrees(math.atan2(v.z, math.hypot(v.x, v.y)))


res = {}
for clip, (n, loop) in k.clips.items():
    k.set_action(clip)
    sc.frame_set(0)
    bpy.context.view_layer.update()
    arm.data.pose_position = "REST"
    bpy.context.view_layer.update()
    p_rest = pitch_of(head_fwd())
    arm.data.pose_position = "POSE"
    mx = {}
    scr = {"head_cy": [], "gap": [], "top": []}
    for f in range(0, n + 1, step):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        for b in ("Neck1", "Neck2", "Neck3", "Head", "Spine"):
            a = math.degrees(arm.pose.bones[b].matrix_basis.to_quaternion().angle)
            a = min(a, 360 - a)
            if a > mx.get(b, (0, 0))[0]:
                mx[b] = (round(a, 2), f)
        npitch = sum(math.degrees(arm.pose.bones[b].matrix_basis.to_euler().x) for b in ("Neck1", "Neck2", "Neck3"))
        hp = pitch_of(head_fwd()) - p_rest
        for key, v in (("neck_pitch_sum", npitch), ("head_pitch_up", hp)):
            lo, hi = mx.get(key, (9e9, -9e9))
            mx[key] = (round(min(lo, v), 2), round(max(hi, v), 2))
        dg = bpy.context.evaluated_depsgraph_get()
        ev = k.main.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        hy = [(1 - world_to_camera_view(sc, cam, mw @ me.vertices[i].co).y) * RES for i in hidx]
        by = [(1 - world_to_camera_view(sc, cam, mw @ me.vertices[i].co).y) * RES for i in bidx]
        ev.to_mesh_clear()
        scr["head_cy"].append(round(sum(hy) / len(hy), 1))
        scr["top"].append(round(min(hy), 1))
        scr["gap"].append(round(min(by) - max(hy), 1))
    res[clip] = {"max_angle": mx, "screen": {k2: (min(v), max(v)) for k2, v in scr.items()},
                 "screen_f0": {k2: v[0] for k2, v in scr.items()}}
print("STANCE " + json.dumps(res))
