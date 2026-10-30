# ------------------------------------------------------------------ animation (plan section 7 + ANIM_REFS.md)
import petkit as pk
import _common as cm
import bpy

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]


def tab(T, f):
    """eased (smoothstep) interpolation through [(frame, value | tuple)]"""
    if f <= T[0][0]:
        return T[0][1]
    for (f0, v0), (f1, v1) in zip(T, T[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / (f1 - f0) if f1 > f0 else 1.0
            u = u * u * (3 - 2 * u)
            if isinstance(v0, tuple):
                return tuple(a + (b - a) * u for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * u
    return T[-1][1]


def ears(k, f, l=0.0, r=None, fwd=0.0):
    """roll the upright ears: + tips them outward; fwd + tips them forward"""
    r = l if r is None else r
    k.key("Ear_L", f, rot=(fwd, 0, l))
    k.key("Ear_R", f, rot=(fwd, 0, -r))


def tail(k, f, pitch=0.0, roll=0.0, lag=(1.0, 0.8, 0.6)):
    """pitch + lifts the hanging tail backward, roll swings it sideways"""
    for b, g in zip(TAIL, lag):
        k.key(b, f, rot=(pitch * g, 0, roll * g))


def plant(k, f, moves=None):
    """IK every foot on its rest spot; moves = {leg: T} overrides (a lifted foot)"""
    bpy.context.scene.frame_set(f)
    for leg in LEGS4:
        T = moves[leg] if moves and leg in moves else Vector((k.J[leg].x, k.J[leg].y, 0.0))
        k.solve_leg(leg, f, T)


def idle(k):
    """HORN TILT: slow weight shift, the head yaws +-6 deg so the horn tilts side to side, the left foreleg lifts 0.03
    and stamps down (f46), ear twitches, one tail flick (f90). Legs planted otherwise."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        br = 0.5 + 0.5 * pk.wave(f, n, 0.25, 3)
        sw = pk.wave(f, n, 0.0, 1)                                  # weight shift (one cycle)
        k.key("Spine", f, rot=(0, 0, 1.2 * sw), loc=(0.010 * sw, 0, -0.004 * br))
        k.key("Chest", f, rot=(0.4 * br, 0, -0.6 * sw))
        k.key("Neck", f, rot=(0.5 * br, 2.0 * pk.wave(f, n, 0.1, 1), 0))
        k.key("Head", f, rot=(0.6 * pk.wave(f, n, 0.3, 2), 4.0 * pk.wave(f, n, 0.15, 1), 0))
        k.key("Jaw", f, rot=(1.0 + 1.0 * br, 0, 0))
    for f, l, r in ((0, 0, 0), (16, 0, 0), (18, 14, 0), (21, 0, 0), (60, 0, 0), (62, 0, 12), (65, 0, 0),
                    (104, 0, 0), (106, 10, 10), (109, 0, 0), (120, 0, 0)):
        ears(k, f, l, r)
    for f, p, r in ((0, 4, 0), (84, 4, 0), (88, 22, 30), (90, 28, 38), (93, 18, 22), (98, 6, 4), (104, 4, 0),
                    (120, 4, 0)):
        tail(k, f, p, r)
    k.bake_bezier_now()
    J = k.J
    for f in range(0, n + 1):
        mv = None
        if 30 <= f <= 46:                                           # the foreleg lift + stamp
            u = (f - 30) / 16
            mv = {"Leg_FL": Vector((J["Leg_FL"].x, J["Leg_FL"].y - 0.015 * math.sin(math.pi * u),
                                    0.032 * math.sin(math.pi * u) ** 0.8))}
        plant(k, f, mv)
    k.finish()
    k.meta["planted"] = ["Leg_FR", "Leg_BL", "Leg_BR"]
    k.events["idle"] = {"stamp": round(46 / n, 3), "flick": round(90 / n, 3)}


def walk(k):
    """HEAVY LATERAL-SEQUENCE WALK (Muybridge walking bison + plate 733): hind then fore on the same side, the head
    carried low and dipping on each front contact, the body sinks 0.02H per step and rolls, the tail lags."""
    n = 40

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.5 * pk.wave(f, n, 0.1, 2), 1.2 * pk.wave(f, n, 0.0), 2.0 * pk.wave(f, n, 0.05)),
              loc=(0, 0, -0.022 - 0.014 * b))
        k.key("Chest", f, rot=(0.8, -1.5 * pk.wave(f, n, 0.25), -1.2 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(1.5 + 1.0 * pk.wave(f, n, 0.12, 2), 0, 0))
        k.key("Head", f, rot=(1.5 * pk.wave(f, n, 0.18, 2), 1.5 * pk.wave(f, n, 0.3), 0))
        k.key("Jaw", f, rot=(1.5, 0, 0))
        tail(k, f, 6, 8 * pk.wave(f, n, 0.3))
        ears(k, f, 3 * pk.wave(f, n, 0.2, 2), 3 * pk.wave(f, n, 0.7, 2))
    stride = cm.quad_walk(k, n, 0.12, 0.08, body, gait="walk", duty=0.70)
    return stride


ROAR_P = [  # f, chest pitch, chest z, neck, head, jaw, tail pitch, ears
    (0, 0.0, 0.0, 0, 0, 0, 0, 0),
    (6, 1.0, -0.006, 1, 4, 0, 4, -6),
    (16, -1.0, -0.004, -4, -12, 4, 20, 10),
    (40, -1.0, -0.004, -4, -12, 14, 26, 12),
    (50, 0.0, -0.002, -2, -5, 4, 12, 4),
    (60, 0.0, 0.0, 0, 0, 0, 0, 0)]


def roar(k):
    """HORN-TO-THE-SKY BELLOW: tuck (anticipation), the head lifts 16 deg with the snout forward, the jaw opens late
    and the bellow pulses three times (jaw + flank pump: bellow1-3 on Mouth), slow return. Legs planted."""
    n = 60
    k.new_action("roar", n, False)
    for f, cp, cz, nk, hd, jw, tp, er in ROAR_P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Chest", f, rot=(cp, 0, 0), loc=(0, 0, cz))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        tail(k, f, tp, 0, lag=(1.0, 0.6, 0.4))
        ears(k, f, er, er, fwd=-er * 0.5)
    for f in (20, 28, 36):                                          # the three bellow pulses
        k.key("Jaw", f, rot=(19, 0, 0))
        k.key("Chest", f, rot=(-1.6, 0, 0), loc=(0, 0, 0.004))
        k.key("Head", f, rot=(-13, 0, 0))
    for f in (24, 32):
        k.key("Jaw", f, rot=(12, 0, 0))
        k.key("Chest", f, rot=(-0.8, 0, 0), loc=(0, 0, -0.004))
        k.key("Head", f, rot=(-12, 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)
    k.events["roar"] = {"bellow1": round(20 / n, 3), "bellow2": round(28 / n, 3), "bellow3": round(36 / n, 3)}


TAP_P = [  # f, spine z, chest pitch, neck, head pitch, jaw, tail pitch, ears
    (0, 0.0, 0, 0, 0, 0, 0, 0),
    (8, -0.006, 1.5, 3, 14, 0, 4, 0),
    (16, -0.016, 3.5, 7, 44, 0, 10, -8),
    (22, -0.020, 4.0, 8, 54, 0, 14, -10),          # face down, horn forward just above the snow
    (27, -0.020, 4.0, 8, 50, 0, 14, -10),          # cocked: the tip lifts
    (30, -0.020, 4.0, 8, 58, 0, 16, -10),          # tap1 (2 f strike)
    (36, -0.020, 4.0, 8, 52, 0, 16, -10),
    (39, -0.020, 4.0, 8, 50, 0, 16, -10),
    (42, -0.020, 4.0, 8, 58, 0, 18, -10),          # tap2
    (48, -0.020, 4.0, 8, 52, 0, 18, -10),
    (51, -0.020, 4.0, 8, 50, 0, 18, -10),
    (54, -0.020, 4.0, 8, 58, 0, 20, -10),          # tap3
    (56, -0.020, 4.0, 8, 58, 0, 20, -10),
    (58, -0.014, 2.0, 4, 30, 2, 26, 0),            # SNAP UP (in-betweens every 2 f)
    (60, -0.006, -0.5, -1, 2, 6, 30, 8),
    (62, 0.0, -1.0, -4, -12, 8, 32, 12),           # horn to the sky
    (66, 0.0, -1.0, -4, -11, 6, 30, 12),
    (86, 0.0, -1.0, -4, -11, 5, 26, 10),
    (94, 0.0, -0.3, -1, -3, 2, 8, 3),
    (100, 0.0, 0.0, 0, 0, 0, 0, 0)]


def horntap(k):
    """SIGNATURE - LIGHTNING TAPS: the forequarters lower and the head drives down at the throat, horn forward, the snout
    clear of the snow; three taps of the horn tip (tap1-3, a cocked lift then a 2-frame strike); the head snaps up and
    the horn points at the sky in 6 frames; hold while the lightning inlays flash (charge); slow return to rest."""
    n = 100
    k.new_action("act_horntap", n, False)
    for f, sz, cp, nk, hd, jw, tp, er in TAP_P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, sz))
        k.key("Chest", f, rot=(cp, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        tail(k, f, tp, 0, lag=(1.0, 0.6, 0.4))
        ears(k, f, abs(er), abs(er), fwd=er)
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)
    k.events["act_horntap"] = {"tap1": round(30 / n, 3), "tap2": round(42 / n, 3), "tap3": round(54 / n, 3),
                               "snap": round(60 / n, 3), "charge": round(70 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    horntap(k)
    return stride


HEAD_XF = []
