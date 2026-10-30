# Cvetibara rig + animation + export (run in the persistent Blender GUI via MCP, after cvetibara_model.build()).
# Follows the animate-roblox-characters skill's workflow by hand (its automatic gate only accepts R6/R15 humans):
# key poses on POSE BONES only, Bezier/auto-clamped curves with a Cycles modifier on loops (no seam), contact
# audit for the walk (planted feet), loop endpoint audit, then export + GIF preview.
# Output matches the SLINGSHOT CreatureClips format (Claude Design/_pipeline/cd_build.py): bones with axis-aligned
# rest (tail +Z), root-space rotation/translation deltas, Blender (x, y, z) -> Roblox (-x, z, y).
import bpy, bmesh, math, json, os
from mathutils import Vector, Quaternion, Matrix
from bpy_extras import anim_utils

OUT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\FriendPets\Cvetibara"
NAME = "Cvetibara"
FPS = 30
GOLD_HEX = "ffc840"

# ------------------------------------------------------------------ joints (Blender coords, model faces -Y)
def joints(g):
    body = bpy.data.objects["Body"]
    surface = g["surface"]
    J = {}
    J["Spine"] = Vector((0, 0.45, 0.88))
    J["Head"] = Vector((0, -0.30, 1.30))
    for side, sx in (("L", 1), ("R", -1)):
        J["Leg_F" + side] = Vector((sx * 0.40, -0.16, 0.46))
        J["Leg_B" + side] = Vector((sx * 0.42, 1.06, 0.48))
        root, _ = surface(body, (sx * 0.9, 0.15, 1.85), (0, 0.15, 0.9))
        root = root + Vector((0, 0, -0.02))
        arm = Vector((sx * 1.0, 0.45, 0.80)).normalized()
        J["Wing_" + side] = root
        J["WingTip_" + side] = root + arm * 1.2 * 0.5 + Vector((0, 0, 0.16))
    ears = bpy.data.objects["Ears"]
    for side, sx in (("L", 1), ("R", -1)):
        vs = [v.co for v in ears.data.vertices if v.co.x * sx > 0]
        c = sum(vs, Vector()) / len(vs)
        low = min(v.z for v in vs)
        J["Ear_" + side] = Vector((c.x, c.y, low + 0.03))
    for nm, obj in (("Flower", "Glow_FlowerCore"), ("Halo", "Glow_Halo")):
        vs = [v.co for v in bpy.data.objects[obj].data.vertices]
        J[nm] = sum(vs, Vector()) / len(vs)
    return J


PARENT = {"Spine": "Root", "Head": "Spine", "Ear_L": "Head", "Ear_R": "Head", "Flower": "Head", "Halo": "Head",
          "Leg_FL": "Spine", "Leg_FR": "Spine", "Leg_BL": "Spine", "Leg_BR": "Spine",
          "Wing_L": "Spine", "Wing_R": "Spine", "WingTip_L": "Wing_L", "WingTip_R": "Wing_R"}


def smooth(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ weights
def weight_body(o, J):
    groups = {b: o.vertex_groups.new(name=b) for b in ("Spine", "Head", "Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR")}
    for v in o.data.vertices:
        co = v.co
        w = {}
        # legs: below the hip line, near each leg column
        for leg in ("Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"):
            p = J[leg]
            d = Vector((co.x - p.x, co.y - p.y)).length
            wl = smooth(p.z + 0.12, p.z - 0.10, co.z) * smooth(0.42, 0.24, d)
            if wl > 0:
                w[leg] = wl
        legs = sum(w.values())
        # head: everything in front of the neck, blended over ~0.35 BU
        wh = smooth(-0.12, -0.42, co.y) * (1 - min(1, legs))
        if wh > 0:
            w["Head"] = wh
        rest = max(0.0, 1 - sum(w.values()))
        if rest > 0:
            w["Spine"] = rest
        tot = sum(w.values())
        for b, x in w.items():
            groups[b].add([v.index], x / tot, "REPLACE")


def weight_rigid(o, bone):
    g = o.vertex_groups.new(name=bone)
    g.add([v.index for v in o.data.vertices], 1.0, "REPLACE")


def weight_by_side(o, left, right):
    gl, gr = o.vertex_groups.new(name=left), o.vertex_groups.new(name=right)
    for v in o.data.vertices:
        (gl if v.co.x > 0 else gr).add([v.index], 1.0, "REPLACE")


def weight_wing(o, J, side):
    sx = 1 if side == "L" else -1
    root = J["Wing_" + side]
    arm = Vector((sx * 1.0, 0.45, 0.80)).normalized()
    g0, g1 = o.vertex_groups.new(name="Wing_" + side), o.vertex_groups.new(name="WingTip_" + side)
    for v in o.data.vertices:
        u = (v.co - root).dot(arm) / 1.2
        t = smooth(0.38, 0.62, u)
        if t < 1:
            g0.add([v.index], 1 - t, "REPLACE")
        if t > 0:
            g1.add([v.index], t, "REPLACE")


def join(objs, name):
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    with bpy.context.temp_override(active_object=objs[0], selected_editable_objects=objs, selected_objects=objs):
        bpy.ops.object.join()
    objs[0].name = name
    objs[0].data.name = name
    return objs[0]


def build_rig(g):
    J = joints(g)
    body = bpy.data.objects["Body"]
    pts = [o.matrix_world @ Vector(c) for o in bpy.data.collections["Cvetibara"].objects if o.type == "MESH"
           for c in o.bound_box]
    mn = Vector([min(p[i] for p in pts) for i in range(3)])
    mx = Vector([max(p[i] for p in pts) for i in range(3)])
    J["Root"] = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, 0.0))
    # weights per part
    weight_body(body, J)
    weight_rigid(bpy.data.objects["Face"], "Head")
    weight_by_side(bpy.data.objects["Ears"], "Ear_L", "Ear_R")
    weight_rigid(bpy.data.objects["Flower"], "Flower")
    weight_rigid(bpy.data.objects["Glow_FlowerCore"], "Flower")
    weight_rigid(bpy.data.objects["Glow_Halo"], "Halo")
    weight_rigid(bpy.data.objects["Glow_Stars"], "Spine")
    for side in ("L", "R"):
        weight_wing(bpy.data.objects["Wing_" + side], J, side)
        weight_wing(bpy.data.objects["Glow_WingTrim_" + side], J, side)
    O = bpy.data.objects
    main = join([O["Body"], O["Face"], O["Ears"], O["Wing_L"], O["Wing_R"], O["Flower"]], "Body")
    glow = join([O["Glow_Halo"], O["Glow_WingTrim_L"], O["Glow_WingTrim_R"], O["Glow_Stars"], O["Glow_FlowerCore"]],
                "Glow_" + GOLD_HEX)
    # armature: every bone head at its pivot, tail straight up (axis-aligned rest, like cd_build)
    ad = bpy.data.armatures.new("Armature")
    arm = bpy.data.objects.new("Armature", ad)
    bpy.data.collections["Cvetibara"].objects.link(arm)
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    L = 0.12
    order = ["Root", "Spine", "Head", "Ear_L", "Ear_R", "Flower", "Halo", "Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR",
             "Wing_L", "Wing_R", "WingTip_L", "WingTip_R"]
    for b in order:
        e = ad.edit_bones.new(b)
        e.head, e.tail = J[b], J[b] + Vector((0, 0, L))
        e.roll = 0
        if b in PARENT:
            e.parent = ad.edit_bones[PARENT[b]]
    bpy.ops.object.mode_set(mode="OBJECT")
    for o in (main, glow):
        o.parent = arm
        m = o.modifiers.new("Armature", "ARMATURE")
        m.object = arm
    for pb in arm.pose.bones:
        pb.rotation_mode = "QUATERNION"
    return arm, main, glow, J


# ------------------------------------------------------------------ keyframing helpers (world-axis intent)
def Rq(pitch=0.0, yaw=0.0, roll=0.0):
    """pitch about +X (nose down = +), yaw about +Z, roll about +Y; degrees, armature axes."""
    return (Quaternion((0, 0, 1), math.radians(yaw)) @ Quaternion((1, 0, 0), math.radians(pitch))
            @ Quaternion((0, 1, 0), math.radians(roll)))


def key(arm, bone, f, rot=None, loc=None):
    pb = arm.pose.bones[bone]
    R0 = arm.data.bones[bone].matrix_local.to_quaternion()
    if rot is not None:
        q = R0.inverted() @ Rq(*rot) @ R0
        pb.rotation_quaternion = q
        pb.keyframe_insert("rotation_quaternion", frame=f, group=bone)
    if loc is not None:
        pb.location = R0.inverted() @ Vector(loc)
        pb.keyframe_insert("location", frame=f, group=bone)


def fcurves(arm):
    ad = arm.animation_data
    cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
    return cb.fcurves if cb else []


def new_action(arm, name):
    if arm.animation_data is None:
        arm.animation_data_create()
    old = bpy.data.actions.get(name)
    if old:
        bpy.data.actions.remove(old)
    act = bpy.data.actions.new(name)
    act.use_fake_user = True
    arm.animation_data.action = act
    for pb in arm.pose.bones:
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.location = (0, 0, 0)
    return act


def finish(arm, loop, n):
    """Bezier + auto-clamped everywhere; loops get a Cycles modifier so the seam tangents match."""
    for fc in fcurves(arm):
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
        if loop and not any(m.type == "CYCLES" for m in fc.modifiers):
            fc.modifiers.new("CYCLES")
        fc.update()
    act = arm.animation_data.action
    act.frame_range = (0, n)
    act.use_frame_range = True


def wave(f, n, phase=0.0, cycles=1):
    return math.sin(2 * math.pi * (cycles * f / n + phase))


# ------------------------------------------------------------------ clips
def clip_idle(arm, n=48):
    new_action(arm, "idle")
    for f in range(0, n + 1, 6):
        s = wave(f, n)
        c = wave(f, n, 0.25)
        key(arm, "Spine", f, rot=(1.2 * s, 0, 0), loc=(0, 0, 0.018 * (1 + s) / 2))       # slow breath
        key(arm, "Head", f, rot=(-2.5 * c, 3 * wave(f, n, 0.1), 2 * s), loc=(0, 0, 0))   # soft nod + look
        for side, sx in (("L", 1), ("R", -1)):
            key(arm, "Wing_" + side, f, rot=(0, sx * 3 * c, -sx * (6 + 6 * wave(f, n, 0, 2))))
            key(arm, "WingTip_" + side, f, rot=(0, 0, -sx * 5 * wave(f, n, -0.08, 2)))
        key(arm, "Halo", f, rot=(4 * wave(f, n, 0.3), 0, 4 * c), loc=(0, 0, 0.05 * (1 + wave(f, n, 0.15)) / 2))
        key(arm, "Flower", f, rot=(0, 0, 6 * wave(f, n, 0.4)))
    for side, sx in (("L", 1), ("R", -1)):  # one quick ear twitch (left) per cycle
        for f, a in ((0, 0), (28, 0), (31, -18), (34, 4), (38, 0), (n, 0)):
            key(arm, "Ear_" + side, f, rot=(0, 0, sx * a if side == "L" else 0))
    for leg in ("Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"):
        key(arm, leg, 0, rot=(0, 0, 0))
        key(arm, leg, n, rot=(0, 0, 0))
    finish(arm, True, n)


SWING = 24.0  # leg swing (deg) each side of straight down
LIFT = 0.12   # foot lift during the swing (BU)


def foot_target(f, n, offset, J, leg):
    """Trot foot path (armature space, in-place): planted + sweeping back at constant speed for half the cycle,
    then a quick eased swing forward with a lift."""
    h = J[leg].z
    S = h * math.sin(math.radians(SWING))
    t = ((f / n) + offset) % 1.0
    if t < 0.5:
        y, z = -S + 4 * S * t, 0.0
    else:
        u = (t - 0.5) / 0.5
        y = S - 2 * S * (0.5 - 0.5 * math.cos(math.pi * u))
        z = LIFT * math.sin(math.pi * u)
    return Vector((J[leg].x, J[leg].y + y, z))


def solve_leg(arm, leg, f, T, J):
    """Point the (single-bone) leg at foot target T given the parent's current pose, and stretch it by a hair if
    needed (bone location along the leg), so a planted foot sits exactly on T. Keys the pose bone."""
    pb = arm.pose.bones[leg]
    pb.rotation_quaternion = (1, 0, 0, 0)
    pb.location = (0, 0, 0)
    bpy.context.view_layer.update()
    P = pb.head.copy()
    par = pb.parent
    Rp = par.matrix.to_quaternion() @ arm.data.bones[par.name].matrix_local.to_quaternion().inverted()
    h = J[leg].z
    d = T - P
    Qw = Vector((0, 0, -1)).rotation_difference(d.normalized())
    R0 = arm.data.bones[leg].matrix_local.to_quaternion()
    pb.rotation_quaternion = R0.inverted() @ (Rp.inverted() @ Qw) @ R0
    pb.location = R0.inverted() @ (Rp.inverted() @ (d.normalized() * (d.length - h)))
    pb.keyframe_insert("rotation_quaternion", frame=f, group=leg)
    pb.keyframe_insert("location", frame=f, group=leg)


def clip_walk(arm, n=24, J=None):
    new_action(arm, "walk")
    # 1) body, head and the extras (every 2 frames)
    for f in range(0, n + 1, 2):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)          # bob up twice per cycle (mid-stance)
        key(arm, "Spine", f, rot=(1.5 * wave(f, n, 0, 2), 0, 2.5 * wave(f, n)), loc=(0, 0, 0.04 * b))
        key(arm, "Head", f, rot=(-3 * wave(f, n, 0.12, 2), 4 * wave(f, n, 0.1), -2 * wave(f, n, 0.05)))
        for side, sx in (("L", 1), ("R", -1)):
            key(arm, "Wing_" + side, f, rot=(0, sx * 12, -sx * (-4 + 7 * wave(f, n, 0.1, 2))))
            key(arm, "WingTip_" + side, f, rot=(0, 0, -sx * 6 * wave(f, n, 0.0, 2)))
            key(arm, "Ear_" + side, f, rot=(0, 0, sx * 5 * wave(f, n, 0.2, 2)))
        key(arm, "Halo", f, rot=(3 * wave(f, n, 0.2, 2), 0, 2 * wave(f, n, 0.25)), loc=(0, 0, 0.03 * wave(f, n, 0.3, 2)))
        key(arm, "Flower", f, rot=(0, 0, 8 * wave(f, n, 0.35, 2)))
    for fc in fcurves(arm):  # body keys final before the legs are solved against them
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
        fc.modifiers.new("CYCLES")
        fc.update()
    # 2) legs: every frame, aimed at the planted / swinging foot targets (diagonal pairs)
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg, off in (("Leg_FL", 0.0), ("Leg_BR", 0.0), ("Leg_FR", 0.5), ("Leg_BL", 0.5)):
            solve_leg(arm, leg, f, foot_target(f, n, off, J, leg), J)
    finish(arm, True, n)


def clip_fly(arm, n=18):
    new_action(arm, "fly")
    for f in range(0, n + 1, 1):
        flap = math.cos(2 * math.pi * f / n)                  # +1 = wings up (f0), -1 = down (f9)
        lag = math.cos(2 * math.pi * (f / n - 0.09))
        for side, sx in (("L", 1), ("R", -1)):
            key(arm, "Wing_" + side, f, rot=(0, sx * 6, -sx * (10 + 38 * flap)))
            key(arm, "WingTip_" + side, f, rot=(0, 0, -sx * 22 * lag))
            key(arm, "Ear_" + side, f, rot=(-6, 0, -sx * 6 * lag))
        up = -math.sin(2 * math.pi * f / n)                     # the body rises on the down-stroke
        key(arm, "Spine", f, rot=(-4 + 2 * flap, 0, 0), loc=(0, 0, 0.07 * up))
        key(arm, "Head", f, rot=(-6 - 2 * lag, 0, 0))
        for leg, base in (("Leg_FL", 38), ("Leg_FR", 38), ("Leg_BL", 48), ("Leg_BR", 48)):
            key(arm, leg, f, rot=(base + 6 * lag, 0, 0), loc=(0, 0, 0.05))   # tucked back, dangling
        key(arm, "Halo", f, loc=(0, 0, -0.05 * up), rot=(4 * lag, 0, 0))
        key(arm, "Flower", f, rot=(10 * lag, 0, 0))
    finish(arm, True, n)


def clip_happy(arm, n=36):
    """One-shot: anticipation crouch -> hop with a double wing flap -> land + settle."""
    new_action(arm, "act_happy")
    P = [  # frame, body z, body pitch, head pitch, wing roll (up = +), legs pitch, ear roll
        (0, 0.00, 0, 0, 0, 0, 0),
        (6, -0.07, 4, 6, -8, -6, 6),
        (12, 0.34, -6, -10, 40, 14, -10),
        (16, 0.42, -4, -8, -10, 18, -6),
        (20, 0.34, -2, -6, 40, 14, -10),
        (25, 0.00, 3, 4, -6, -4, 6),
        (29, -0.04, 2, 3, 6, -2, 2),
        (36, 0.00, 0, 0, 0, 0, 0),
    ]
    for f, bz, bp, hp, wr, lp, er in P:
        key(arm, "Spine", f, rot=(bp, 0, 0), loc=(0, 0, bz))
        key(arm, "Head", f, rot=(hp, 0, 0))
        for side, sx in (("L", 1), ("R", -1)):
            key(arm, "Wing_" + side, f, rot=(0, 0, -sx * wr))
            key(arm, "WingTip_" + side, f, rot=(0, 0, -sx * wr * 0.4))
            key(arm, "Ear_" + side, f, rot=(0, 0, sx * er))
        for leg in ("Leg_FL", "Leg_FR"):
            key(arm, leg, f, rot=(-lp, 0, 0))
        for leg in ("Leg_BL", "Leg_BR"):
            key(arm, leg, f, rot=(lp, 0, 0))
        key(arm, "Halo", f, loc=(0, 0, max(0, bz) * 0.25), rot=(0, 0, 0))
        key(arm, "Flower", f, rot=(0, 0, er))
    finish(arm, False, n)


# ------------------------------------------------------------------ audits (the skill's checks, for this rig)
def foot_world(arm, leg, J):
    pb = arm.pose.bones[leg]
    rest = arm.data.bones[leg].matrix_local
    return (pb.matrix @ rest.inverted()) @ Vector((J[leg].x, J[leg].y, 0.0))


def audit(arm, J, clips):
    sc = bpy.context.scene
    report = {}
    for name, (n, loop) in clips.items():
        set_action(arm, name)
        r = {}
        # no linear final keys, nothing keyed on meshes
        lin = sum(1 for fc in fcurves(arm) for k in fc.keyframe_points if k.interpolation == "LINEAR")
        r["linear_keys"] = lin
        if loop:
            sc.frame_set(0)
            a = {pb.name: (pb.matrix.copy()) for pb in arm.pose.bones}
            sc.frame_set(n)
            b = {pb.name: (pb.matrix.copy()) for pb in arm.pose.bones}
            r["loop_pos_err"] = round(max((a[k].translation - b[k].translation).length for k in a), 6)
            r["loop_rot_err_deg"] = round(max(math.degrees(a[k].to_quaternion().rotation_difference(
                b[k].to_quaternion()).angle) for k in a), 4)
        if name == "walk":
            # planted feet: during stance the foot must move backward at a steady speed and stay on the ground
            drift, low = 0.0, 0.0
            for leg, off in (("Leg_FL", 0.0), ("Leg_BR", 0.0), ("Leg_FR", 0.5), ("Leg_BL", 0.5)):
                ys, zs = [], []
                for f in range(n + 1):
                    t = ((f / n) + off) % 1.0
                    if t <= 0.5:
                        sc.frame_set(f)
                        p = foot_world(arm, leg, J)
                        ys.append((t, p.y))
                        zs.append(p.z)
                ys.sort()
                if len(ys) > 2:
                    speed = (ys[-1][1] - ys[0][1]) / (ys[-1][0] - ys[0][0])
                    for t, y in ys:
                        drift = max(drift, abs(y - (ys[0][1] + speed * (t - ys[0][0]))))
                low = max(low, max(zs) - min(zs))
            r["stance_slide_dev"] = round(drift, 4)   # deviation from constant-speed sweep (BU)
            r["stance_height_var"] = round(low, 4)
        report[name] = r
    return report


def set_action(arm, name):
    # channels a clip doesn't key must sit at rest, not keep the previous clip's last value
    for pb in arm.pose.bones:
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.location = (0, 0, 0)
    act = bpy.data.actions[name]
    arm.animation_data.action = act
    if arm.animation_data.action_slot is None and act.slots:
        arm.animation_data.action_slot = act.slots[0]


# ------------------------------------------------------------------ sample -> CreatureClips JSON (cd_build format)
def rq(q):
    return (-q.x, q.z, q.y, q.w)


def rv(v):
    return (-v.x, v.z, v.y)


def sample(arm, J, clips):
    sc = bpy.context.scene
    bones = [b.name for b in arm.data.bones if b.name != "Root"]
    rest = {b: arm.data.bones[b].matrix_local for b in bones}
    R0q = {b: rest[b].to_quaternion() for b in bones}
    P0 = {b: rest[b].translation.copy() for b in bones}
    P0["Root"] = J["Root"]
    QI = Quaternion()
    out = {}
    for name, (n, loop) in clips.items():
        set_action(arm, name)
        frames = []
        steps = range(n) if loop else range(n + 1)
        for f in steps:
            sc.frame_set(f)
            W = {"Root": (QI, J["Root"])}
            for b in bones:
                m = arm.pose.bones[b].matrix
                W[b] = (m.to_quaternion() @ R0q[b].inverted(), m.translation.copy())
            fr = {}
            for b in bones:
                Bq, P = W[b]
                Bpq, Pp = W[PARENT[b]]
                D = Bpq.inverted() @ Bq
                v = Bpq.inverted() @ (P - Pp) - (P0[b] - P0[PARENT[b]])
                fr[b] = (D.normalized(), v)
            frames.append(fr)
        rot, pos, big = {}, {}, 0.0
        for b in bones:
            seq, moving = [], False
            for fr in frames:
                q = fr[b][0]
                if q.w < 0:
                    q = -q
                if abs(q.w) < 0.99999:
                    moving = True
                seq.extend(round(c, 5) for c in rq(q))
            if moving:
                rot[b] = seq
            vs = [fr[b][1] for fr in frames]
            if max(v.length for v in vs) > 1e-4:
                pos[b] = [round(c, 5) for v in vs for c in rv(v)]
                big = max(big, max(abs(c) for c in pos[b]))
        out[name] = {"n": len(frames), "loop": loop, "len": round((n if loop else n) / FPS, 4), "rot": rot,
                     "pos": pos, "ps": round(big * 1.05 + 1e-4, 5)}
    return out


def walk_stride(arm, J, n=24):
    """Distance the body must travel per walk cycle so planted feet don't slide (50% stance)."""
    set_action(arm, "walk")
    sc = bpy.context.scene
    ys = []
    for f in range(n + 1):
        t = (f / n) % 1.0
        if t <= 0.5:
            sc.frame_set(f)
            ys.append(foot_world(arm, "Leg_FL", J).y)
    sweep = max(ys) - min(ys)
    return 2 * sweep


def run(g):
    arm, main, glow, J = build_rig(g)
    clips = {"idle": (48, True), "walk": (24, True), "fly": (18, True), "act_happy": (36, False)}
    clip_idle(arm, 48)
    clip_walk(arm, 24, J)
    clip_fly(arm, 18)
    clip_happy(arm, 36)
    rep = audit(arm, J, clips)
    stride = walk_stride(arm, J, 24)
    data = sample(arm, J, clips)
    data["walk"]["stride"] = round(stride, 4)
    pts = [o.matrix_world @ Vector(c) for o in (main, glow) for c in o.bound_box]
    mn = Vector([min(p[i] for p in pts) for i in range(3)])
    mx = Vector([max(p[i] for p in pts) for i in range(3)])
    js = {"name": NAME, "fps": FPS, "ref": {"bone": "Head", "dist": round((J["Head"] - J["Root"]).length, 5)},
          "stride": round(stride, 4), "height": round(mx.z - mn.z, 4), "length": round(mx.y - mn.y, 4),
          "width": round(mx.x - mn.x, 4), "glow": {glow.name: GOLD_HEX}, "clips": data,
          "bones": {b: PARENT[b] for b in PARENT}}
    with open(os.path.join(OUT, NAME + ".json"), "w") as fh:
        json.dump(js, fh, separators=(",", ":"))
    set_action(arm, "idle")
    bpy.context.scene.frame_set(0)
    return {"audit": rep, "stride": round(stride, 4), "size": [round(v, 3) for v in (mx - mn)],
            "bones": len(arm.data.bones), "body_tris": sum(len(p.vertices) - 2 for p in main.data.polygons),
            "glow_tris": sum(len(p.vertices) - 2 for p in glow.data.polygons)}
