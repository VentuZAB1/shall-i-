# Shared animation helpers for the PetsV2 specs (2026-10-08). Conventions (petkit.Pet.key):
#   rot = (pitch, yaw, roll) degrees in ARMATURE axes, relative to the parent. Model faces -Y, up +Z.
#   pitch + : a bone pointing -Y (spine/head) tips its nose DOWN; a bone pointing +Y (tail) LIFTS; a bone pointing -Z
#             (leg) swings its foot BACKWARD; a bone pointing +Z (ear/antenna) tips FORWARD.
#   yaw +   : turns toward the pet's left-back (+X toward +Y).   roll + : +X side goes down (about +Y).
import math
from mathutils import Vector
import petkit as pk

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
LEGS2 = ["Leg_L", "Leg_R"]


def plant(k, n, legs=LEGS4, frames=None, foot_z=0.0):
    """Bake the body keys to Bezier, then key every leg so its foot stays on its rest spot (no sliding)."""
    import bpy
    k.bake_bezier_now()
    for f in (frames if frames is not None else range(0, n + 1)):
        bpy.context.scene.frame_set(f)
        for leg in legs:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, foot_z)))


def drop_keys(k, bone, f0, f1):
    """Remove a bone's keys in [f0, f1] (e.g. to free a planted leg for a gesture)."""
    for fc in k.fcurves():
        if fc.data_path.startswith(f'pose.bones["{bone}"]'):
            for i in reversed(range(len(fc.keyframe_points))):
                if f0 <= fc.keyframe_points[i].co.x <= f1:
                    fc.keyframe_points.remove(fc.keyframe_points[i])
            fc.update()


def chain(k, f, n, bones, sway=0.0, pitch=0.0, phase=0.0, cycles=1, lag=0.12, grow=0.45, pitch_amp=0.0,
          pitch_each=None):
    """Wave down a chain (tails, tentacles, necks): yaw sway grows along the chain, each bone lags behind."""
    for i, b in enumerate(bones):
        ph = phase - lag * i
        p = (pitch_each[i] if pitch_each else pitch) + pitch_amp * pk.wave(f, n, ph, cycles)
        k.key(b, f, rot=(p, sway * (1 + grow * i) * pk.wave(f, n, ph, cycles), 0))


def ears(k, f, pitch=0.0, spread=0.0, twitch_r=0.0, names=("Ear_L", "Ear_R")):
    k.key(names[0], f, rot=(pitch, 0, -spread))
    k.key(names[1], f, rot=(pitch + twitch_r, 0, spread - twitch_r * 0.5))


def keyed_track(k, bone, frames_vals, fn):
    """frames_vals: [(f, value)], fn(value) -> dict(rot=..., loc=...)"""
    for f, v in frames_vals:
        k.key(bone, f, **fn(v))


# ------------------------------------------------------------------ flyers
def wing_pair(k, f, up, fwd=0.0, tip_up=0.0, tip_fwd=0.0, twist=0.0, names=("Wing_", "WingTip_")):
    """up + = wing raised, fwd + = swept forward, twist + = leading edge down."""
    for side, sx in (("L", 1), ("R", -1)):
        k.key(names[0] + side, f, rot=(twist, -sx * fwd, -sx * up))
        if names[1]:
            k.key(names[1] + side, f, rot=(0, -sx * tip_fwd, -sx * tip_up))


def flap(ph):
    """phase 0..1 -> (flap, down, lag, rise): flap +1 = top of the stroke at ph 0, -1 = bottom at 0.5."""
    return (math.cos(2 * math.pi * ph), math.sin(2 * math.pi * ph), math.cos(2 * math.pi * (ph - 0.13)),
            -math.sin(2 * math.pi * (ph - 0.05)))


class Flight:
    """Real flight for a winged pet. cfg keys:
       n (20), body_pitch (deg nose-down), neck/head (look ahead, deg), amp (stroke), mid (stroke centre),
       sweep (forward sweep on the downstroke), tuck {leg: deg}, tail [bones], tail_pitch, extra(k, f, ph)"""

    def __init__(self, k, **cfg):
        self.k = k
        self.c = dict(n=20, body_pitch=16, neck=-12, head=-10, amp=52, mid=8, sweep=14, tuck=None, tail=(),
                      tail_pitch=10, tail_wave=7, bob=0.08, extra=None, neck_bone="Neck")
        self.c.update(cfg)

    def pose(self, f, n=None, legs=True):
        k, c = self.k, self.c
        n = n or c["n"]
        ph = f / n
        fl, down, lag, rise = flap(ph)
        k.key("Spine", f, rot=(c["body_pitch"] + 2.5 * fl, 0, 0), loc=(0, 0, -c["bob"] * rise))
        if c["neck_bone"]:
            k.key(c["neck_bone"], f, rot=(c["neck"] - 2 * lag, 0, 0))
        k.key("Head", f, rot=(c["head"] + 2 * lag, 0, 0))
        wing_pair(k, f, up=c["mid"] + c["amp"] * fl, fwd=c["sweep"] * down - 4,
                  tip_up=-6 + 30 * lag + 12 * max(0.0, -down), tip_fwd=-14 * max(0.0, -down) + 6 * down,
                  twist=8 * down)
        if legs and c["tuck"]:
            for leg, a in c["tuck"].items():
                k.key(leg, f, rot=(a + 6 * lag, 0, 0), loc=(0, 0, 0.05))
        for i, b in enumerate(c["tail"]):
            k.key(b, f, rot=(c["tail_pitch"] + c["tail_wave"] * math.sin(2 * math.pi * (ph - 0.12 * (i + 1))),
                             3 * math.sin(2 * math.pi * (ph - 0.2 * i)), 0))
        if c["extra"]:
            c["extra"](k, f, ph)

    def fly(self):
        n = self.c["n"]
        self.k.new_action("fly", n, True)
        for f in range(0, n + 1):
            self.pose(f, n)
        self.k.finish()

    def takeoff(self, rest_keys, legs=LEGS4, n=27):
        """rest_keys(f) keys the ground pose extras (wings folded etc). Crouch 0-10, launch 11, flight from 13."""
        import bpy
        k, c = self.k, self.c
        k.new_action("takeoff", n, False)
        P = [(0, 0.0, 0, None), (6, -0.10, -6, (30, -12, 10, -10)), (10, -0.13, -8, (62, -6, 24, -4)),
             (13, 0.22, 10, (-30, 12, -8, 6)), (17, 0.34, 14, (20, 0, 18, -6))]
        for f, z, p, w in P:
            if w is None:
                rest_keys(f)
            else:
                k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
                if c["neck_bone"]:
                    k.key(c["neck_bone"], f, rot=(-8 - p * 0.5, 0, 0))
                k.key("Head", f, rot=(-6, 0, 0))
                wing_pair(k, f, *w)
                for i, b in enumerate(c["tail"]):
                    k.key(b, f, rot=(6 + p * 0.4, 0, 0))
        self.pose(n, c["n"], legs=False)
        k.bake_bezier_now()
        for f in range(0, 12):
            bpy.context.scene.frame_set(f)
            for leg in legs:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
        tuck = c["tuck"] or {}
        for f, t in ((14, 0.45), (20, 0.85), (n, 1.0)):
            for leg in legs:
                a = tuck.get(leg, 50) * t
                k.key(leg, f, rot=(a, 0, 0), loc=(0, 0, 0.05 if f == n else 0.0))
        k.finish(loop=False)
        k.events["takeoff"] = {"launch": round(11 / n, 3)}

    def land(self, rest_keys, legs=LEGS4, n=27):
        import bpy
        k, c = self.k, self.c
        k.new_action("land", n, False)
        self.pose(0, c["n"])
        P = [(7, 0.10, -16, (34, -26, 24, -18)), (12, 0.06, -10, (-12, -14, 4, -6)), (16, -0.09, 5, (10, -8, -10, -14)),
             (21, 0.02, -1, None), (27, 0.0, 0, None)]
        for f, z, p, w in P:
            if w is None:
                rest_keys(f)
                if f == 21:
                    k.key("Spine", f, rot=(-1, 0, 0), loc=(0, 0, z))
            else:
                k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
                if c["neck_bone"]:
                    k.key(c["neck_bone"], f, rot=(-6 - p * 0.4, 0, 0))
                k.key("Head", f, rot=(-5, 0, 0))
                wing_pair(k, f, *w)
                for i, b in enumerate(c["tail"]):
                    k.key(b, f, rot=(6 - p * 0.3, 0, 0))
        for leg in legs:
            k.key(leg, 7, rot=(-22 if ("F" in leg[4:] or leg in ("Leg_L", "Leg_R")) else -8, 0, 0), loc=(0, 0, 0))
        k.bake_bezier_now()
        for f in range(16, n + 1):
            bpy.context.scene.frame_set(f)
            for leg in legs:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
        k.finish(loop=False)
        k.events["land"] = {"touch": round(16 / n, 3)}


# ------------------------------------------------------------------ biped walk helper
def biped_walk(k, n, stride_half, lift, body_keys, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.58):
    k.meta["legs"] = list(legs)
    k.meta["duty"] = duty
    return pk.walk_cycle(k, n, list(legs), stride_half, lift, body_keys, duty=duty)


def quad_walk(k, n, stride_half, lift, body_keys, gait="trot", duty=None):
    if gait == "trot":
        legs = [("Leg_FL", 0.0), ("Leg_BR", 0.0), ("Leg_FR", 0.5), ("Leg_BL", 0.5)]
        duty = duty or 0.5
    else:  # lateral-sequence walk (cats, cows, elephants)
        legs = [("Leg_BL", 0.0), ("Leg_FL", 0.25), ("Leg_BR", 0.5), ("Leg_FR", 0.75)]
        duty = duty or 0.62
    k.meta["legs"] = legs
    k.meta["duty"] = duty
    return pk.walk_cycle(k, n, legs, stride_half, lift, body_keys, duty=duty)


def key_axis(k, bone, f, axis, deg, loc=None, extra=None):
    """Key a rotation of `deg` about an arbitrary armature-space axis (tentacles, radial limbs).
    extra: optional Quaternion applied after (armature space)."""
    from mathutils import Quaternion
    pb = k.arm.pose.bones[bone]
    R0 = k.arm.data.bones[bone].matrix_local.to_quaternion()
    q = Quaternion(Vector(axis).normalized(), math.radians(deg))
    if extra is not None:
        q = extra @ q
    pb.rotation_quaternion = R0.inverted() @ q @ R0
    pb.keyframe_insert("rotation_quaternion", frame=f, group=bone)
    if loc is not None:
        pb.location = R0.inverted() @ Vector(loc)
        pb.keyframe_insert("location", frame=f, group=bone)


def crack(k, bm, L, yaw_deg, z0, seed, color, steps=7, step=0.075, width=0.045, axis_y=0.0, branch=True):
    """A glowing lava/energy crack wandering over the body surface. Starts on the body at azimuth yaw_deg
    (0 = front -Y, 90 = +X side) and height z0; random-walks in (azimuth, height)."""
    import random
    rnd = random.Random(seed)
    ang, z = math.radians(yaw_deg), z0
    heading = rnd.uniform(-1.0, 1.0)
    pts = []
    for i in range(steps):
        d = Vector((math.sin(ang), -math.cos(ang), 0))
        try:
            q, qn = k.surf(Vector((d.x * 3, axis_y + d.y * 3, z)), Vector((0, axis_y, z)))
        except RuntimeError:
            break
        pts.append(q + qn * 0.012)
        heading += rnd.uniform(-0.9, 0.9)
        heading = max(-1.4, min(1.4, heading))
        ang += math.cos(heading) * step * 1.6
        z += math.sin(heading) * step
    if len(pts) > 2:
        n0 = (pts[0] - Vector((0, axis_y, pts[0].z)))
        strip(k, bm, L, pts, width, color)
        if branch and len(pts) > 4:
            crack(k, bm, L, math.degrees(math.atan2(pts[3].x, -(pts[3].y - axis_y))), pts[3].z, seed + 7, color,
                  steps=4, step=step, width=width * 0.7, axis_y=axis_y, branch=False)


def strip(k, bm, L, pts, width, color):
    """surface-hugging ribbon: normal = direction from the body axis"""
    def nrm(t):
        i = min(int(t * (len(pts) - 1) + 0.5), len(pts) - 1)
        p = pts[i]
        v = Vector((p.x, p.y, 0))
        return v.normalized() if v.length > 1e-6 else Vector((0, -1, 0))
    pk.strip(bm, L, pts, lambda t: width * (1 - 0.6 * t) + 0.01, nrm, color, thick=0.02)
