# ------------------------------------------------------------------ animation (plan section 7 + ANIM_REFS.md)
import petkit as pk
import _common as cm
import bpy

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]
TRK = ["Trunk1", "Trunk2", "Trunk3", "Trunk4"]


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


def trunk(k, f, pitch=(0, 0, 0, 0), roll=(0, 0, 0, 0)):
    """pitch - curls the hanging trunk FORWARD / UP (each bone relative to the one above), roll + swings it to -x"""
    for b, p, r in zip(TRK, pitch, roll):
        k.key(b, f, rot=(p, 0, r))
    k.key("Trunk_Tip", f, rot=(0, 0, 0))


def tail(k, f, pitch=0.0, roll=0.0, lag=(1.0, 0.8, 0.6)):
    """pitch + lifts the hanging tail backward, roll swings it sideways"""
    for b, g in zip(TAIL, lag):
        k.key(b, f, rot=(pitch * g, 0, roll * g))


def ears(k, f, flare=0.0):
    """flare + swings the back edge of both ear flaps out from the head"""
    k.key("Ear_L", f, rot=(0, -flare, 0))
    k.key("Ear_R", f, rot=(0, flare, 0))


def bell(f, c, w):
    """smooth 0..1..0 bump centred on frame c, half width w"""
    u = abs(f - c) / w
    return 0.0 if u >= 1 else 0.5 + 0.5 * math.cos(math.pi * u)


def idle(k):
    """TRUNK SWING: the trunk swings slowly side to side as a lagged chain (tip +-12 deg, two cycles), three slow
    breaths, an exhale at f80 (the trunk tip lifts, the ears flick out). Tusks still, feet planted."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        br = 0.5 + 0.5 * pk.wave(f, n, 0.25, 3)                     # 0..1, three breaths
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, -0.004 * br))
        k.key("Chest", f, rot=(0.5 * br, 0, 0))
        ex = bell(f, 80, 12)                                        # the exhale
        k.key("Neck", f, rot=(0.6 * br - 1.0 * ex, 0, 0))
        k.key("Head", f, rot=(0.8 * pk.wave(f, n, 0.1, 2) - 1.5 * ex, 0, 0))
        k.key("Jaw", f, rot=(1.5 * ex, 0, 0))
        rl = [a * pk.wave(f, n, -0.07 * i, 2) for i, a in enumerate((2.0, 3.0, 3.5, 3.5))]
        pt = [1.0 * pk.wave(f, n, 0.25 - 0.07 * i, 2) - c * ex for i, c in enumerate((2, 4, 8, 12))]
        trunk(k, f, pt, rl)
        tail(k, f, 4 + 3 * br, 9 * pk.wave(f, n, 0.15, 2), lag=(1.0, 0.9, 0.8))
        ears(k, f, 3 * pk.wave(f, n, 0.3, 2) + 9 * bell(f, 82, 8))
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4
    k.events["idle"] = {"exhale": round(80 / n, 3)}


def walk(k):
    """HEAVY LATERAL-SEQUENCE WALK (Muybridge plate 733): hind then fore on the same side, high duty, the body sinks
    after each contact and rolls away from the swinging side, the trunk swings 3 deg per step, the tail lags."""
    n = 40

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.4 * pk.wave(f, n, 0.1, 2), 1.0 * pk.wave(f, n, 0.0), 1.5 * pk.wave(f, n, 0.05)),
              loc=(0, 0, -0.022 - 0.008 * b))
        k.key("Chest", f, rot=(0.6, -1.2 * pk.wave(f, n, 0.25), -1.0 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(0.8 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(-0.8 * pk.wave(f, n, 0.25, 2), 1.0 * pk.wave(f, n, 0.3), 0))
        k.key("Jaw", f, rot=(1.0, 0, 0))
        pt = [a * pk.wave(f, n, 0.2 - 0.06 * i, 2) for i, a in enumerate((0.6, 0.8, 0.8, 0.8))]
        rl = [a * pk.wave(f, n, 0.3 - 0.07 * i) for i, a in enumerate((0.6, 0.8, 0.8, 0.8))]
        trunk(k, f, pt, rl)
        tail(k, f, 6, 9 * pk.wave(f, n, 0.3), lag=(1.0, 0.9, 0.8))
        ears(k, f, 3 * pk.wave(f, n, 0.2, 2))
    stride = cm.quad_walk(k, n, 0.115, 0.075, body, gait="walk", duty=0.72)
    k.events["walk"] = {"stomp": 0.75}                             # Leg_FL (offset 0.25) touches down at f30
    return stride


ROAR_P = [  # f, chest z, chest pitch, neck, head, jaw, trunk pitch x4, tail pitch, ear flare
    (0, 0.0, 0.0, 0, 0, 0, (0, 0, 0, 0), 0, 0),
    (8, -0.006, 0.5, 1, 4, 0, (2, 4, 6, 10), 6, -4),
    (16, -0.010, -0.6, -2, -10, 2, (-34, -24, -20, -12), 30, 8),
    (22, -0.010, -1.0, -3, -15, 8, (-50, -35, -30, -25), 42, 14),
    (26, -0.010, -1.0, -3, -15, 14, (-52, -37, -32, -30), 45, 16),
    (50, -0.010, -1.0, -3, -15, 13, (-52, -37, -32, -30), 45, 16),
    (58, -0.006, -0.4, -1, -6, 4, (-24, -16, -12, -8), 22, 6),
    (66, 0.0, 0.0, 0, 0, 0, (0, 0, 0, 0), 0, 0)]


def roar(k):
    """TRUMPET: a small tuck of the head (anticipation), then the head lifts 15 deg and the trunk rises fast and curls
    up to the sky in front of the brow; the mouth opens after the lift (jaw lag); hold with a trunk tremble, ears
    spread, tail up; the trunk lowers more slowly than it rose. Legs planted."""
    n = 66
    k.new_action("roar", n, False)
    for f, cz, cp, nk, hd, jw, tp, tl, er in ROAR_P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Chest", f, rot=(cp, 0, 0), loc=(0, 0, cz))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        trunk(k, f, tp)
        tail(k, f, tl, 0, lag=(1.0, 0.5, 0.3))
        ears(k, f, er)
    for f in range(28, 50, 2):                                     # trunk tremble +-2 deg (the trumpet)
        d = 2.0 if (f // 2) % 2 else -2.0
        tp = tuple(v + d * w for v, w in zip((-52, -37, -32, -30), (0.2, 0.4, 0.7, 1.0)))
        trunk(k, f, tp)
        ears(k, f, 16 + 0.5 * d)
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)
    k.events["roar"] = {"trumpet": round(26 / n, 3)}


DUST_P = [  # f, head pitch, neck, trunk pitch x4, tail pitch, tail roll
    (0, 0, 0, (0, 0, 0, 0), 0, 0),
    (10, 4, 1, (6, 6, 8, 12), 4, 0),                 # the trunk swings back toward the forefeet
    (20, 6, 2, (-4, 10, 18, 30), 6, 0),              # scoop: the tip curls in (holding the snow)
    (32, -4, 0, (-26, -18, -4, 18), 8, 0),           # lift, the tip still curled in
    (44, -14, -2, (-44, -38, -28, -10), 12, 0),      # cocked hold in front of the face (the tell)
    (48, -15, -2, (-46, -40, -30, -12), 12, 0),
    (52, -15, -2, (-50, -50, -44, -32), 14, 0),      # in-between of the snap
    (56, -15, -2, (-52, -55, -54, -46), 16, 0),      # FLICK over the brow: dust1
    (60, -13, -2, (-50, -52, -50, -40), 14, 0),      # follow-through drift
    (66, 3, 1, (-6, 6, 14, 24), 8, 0),               # scoop 2
    (70, -8, -1, (-32, -30, -18, 0), 10, 0),
    (74, -12, -2, (-44, -46, -42, -32), 12, 0),      # flick 2: dust2
    (78, 2, 0, (-4, 6, 12, 22), 8, 0),               # scoop 3
    (82, -6, -1, (-28, -26, -16, 0), 9, 0),
    (86, -10, -1, (-38, -40, -36, -26), 10, 0),      # flick 3: dust3
    (92, -2, 0, (-8, -6, -4, -2), 6, 0),
    (95, 0, 0, (-2, -1, 0, 0), 14, 22),              # one tail flick
    (98, 0, 0, (0, 0, 0, 0), 4, -6),
    (100, 0, 0, (0, 0, 0, 0), 0, 0)]


def dustover(k):
    """SIGNATURE - DUST OVER THE BACK: the trunk scoops snow at the forefeet, lifts it in front of the face, holds a
    beat, then flicks it back over the brow onto the hump (dust1); two smaller scoops and flicks (dust2, dust3);
    the trunk returns, one tail flick, exact rest. Legs planted, no shake, no spin."""
    n = 100
    k.new_action("act_dustover", n, False)
    for f, hd, nk, tp, tlp, tlr in DUST_P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Chest", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(2 if hd < -8 else 0, 0, 0))
        trunk(k, f, tp)
        tail(k, f, tlp, tlr, lag=(1.0, 0.9, 0.8))
        ears(k, f, 6 if hd < -8 else 0)
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)
    k.events["act_dustover"] = {"scoop1": round(20 / n, 3), "dust1": round(56 / n, 3), "scoop2": round(66 / n, 3),
                                "dust2": round(74 / n, 3), "scoop3": round(78 / n, 3), "dust3": round(86 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    dustover(k)
    return stride


HEAD_XF = []
