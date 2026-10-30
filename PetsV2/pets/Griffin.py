# Griffin (Celestial egg #2): a chibi sky griffin - a fluffy white eagle head with a golden hooked beak, big amber
# eyes and feather ear-tufts, a white feather ruff, a golden lion body + tufted tail, scaly golden eagle front legs
# with talons, and big feathered wings that fade from cream to sky blue to royal blue, trimmed with a glowing gold
# edge. Personality: a noble, alert guardian - snappy bird-like head turns, preens a wing, ruffles its feathers;
# screeches with wings flung wide (roar); flies with powerful strokes, body level, legs tucked.
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Griffin"
MOTION = "Fly"
RIG = "wingquad"
HEIGHT = 9.0
C = pk.lin
WHITE_F = C((252, 250, 244))
WHITE_D = C((214, 220, 232))
LION = C((236, 186, 104))
LION_D = C((204, 146, 70))
BEAK = C((255, 196, 70))
BEAK_D = C((222, 140, 40))
TALON = C((60, 48, 40))
SKY = C((150, 200, 255))
ROYAL = C((70, 110, 225))
TRIM = "ffd36a"
HEAD = Vector((0, -0.58, 1.46))


def body_color(co, n):
    # eagle front (white) -> lion back (gold), blended across the chest
    t = pk.smooth(-0.10, 0.30, co.y)
    feather = pk.mix(WHITE_F, WHITE_D, pk.smooth(0.0, -0.8, n.z) * 0.6)
    lion = pk.mix(LION, LION_D, pk.smooth(0.3, 0.95, n.z) * 0.4)
    c = pk.mix(feather, lion, t * pk.smooth(1.25, 1.0, co.z))
    # front legs are scaly gold, back legs lion
    if co.z < 0.62 and co.y < 0.25:
        c = pk.mix(c, BEAK, pk.smooth(0.55, 0.40, co.z))
    for sx in (1, -1):
        c = pk.mix(c, C((255, 170, 170)), pk.smooth(0.11, 0.03, (co - Vector((sx * 0.30, -0.86, 1.36))).length) * 0.5)
    return c


def model(k):
    E = [
        ("ell", (0, 0.26, 0.88), (0.40, 0.62, 0.38)),
        ("ell", (0, -0.14, 0.96), (0.42, 0.36, 0.42)),
        ("ell", tuple(HEAD), (0.42, 0.40, 0.40)),
        ("cap", (0, 0.86, 1.00), (0, 1.12, 0.80), 0.06), ("cap", (0, 1.12, 0.80), (0, 1.32, 0.90), 0.05),
    ]
    for sx in (1, -1):
        E += [("ell", (sx * 0.30, -0.42, 1.18), (0.20, 0.16, 0.20)),         # cheek fluff
              ("cap", (sx * 0.24, -0.14, 0.76), (sx * 0.25, -0.18, 0.10), 0.09),
              ("ell", (sx * 0.25, -0.24, 0.06), (0.10, 0.14, 0.06)),
              ("ell", (sx * 0.26, 0.60, 0.84), (0.20, 0.26, 0.28)),
              ("cap", (sx * 0.26, 0.62, 0.68), (sx * 0.26, 0.62, 0.10), 0.12),
              ("ell", (sx * 0.26, 0.59, 0.07), (0.13, 0.15, 0.075))]
    for i in range(9):    # feather ruff around the neck
        a = math.radians(-80 + 160 * i / 8)
        E.append(("ball", (0.42 * math.sin(a), -0.28 - 0.10 * math.cos(a), 1.08 - 0.08 * abs(math.sin(a))), 0.13))
    k.body(E, body_color, tris=6200)

    k.eyes([((0.62, -2.6, 1.56), (0.21, -0.7, 1.50)), ((-0.62, -2.6, 1.56), (-0.21, -0.7, 1.50))],
           size=(0.15, 0.17), style="big", iris=(255, 170, 40))

    def face(bm, L):
        p, n = k.surf((0, -2.4, 1.40), (0, -0.6, 1.40))
        # hooked beak: upper (curving down) + lower
        up = pk.arc_points(p - n * 0.04, (0, -1, 0.15), 0.26, bend_axis=(1, 0, 0), bend_deg=70, n=7)
        pk.tube(bm, L, up, lambda t: 0.10 * (1 - t) ** 0.7 + 0.012, lambda t, a: pk.mix(BEAK_D, BEAK, 0.6 + 0.4 * t), sides=10)
        pk.cone(bm, L, p - n * 0.04 + Vector((0, 0, -0.06)), (0, -1, -0.3), 0.14, 0.06, BEAK_D, sides=8, n=4)
        # feather ear-tufts
        for sx in (1, -1):
            base, bn = k.surf(HEAD + Vector((sx * 0.6, 0.1, 0.9)), HEAD + Vector((sx * 0.15, 0.1, 0.1)))
            for j, (dx, h) in enumerate(((0.0, 0.26), (0.06, 0.20), (-0.06, 0.18))):
                pk.cone(bm, L, base - bn * 0.04 + Vector((sx * dx, 0.04 * j, 0)), (sx * 0.5, 0.5, 1.0), h, 0.06, WHITE_F,
                        bend_axis=(1, 0, 0), bend_deg=25, sides=6, n=4)
        # talons on the eagle feet + lion paw toes
        for sx in (1, -1):
            for dx in (-0.06, 0.0, 0.06):
                pk.cone(bm, L, (sx * 0.25 + dx, -0.34, 0.05), (0, -1, -0.5), 0.10, 0.03, TALON, bend_axis=(1, 0, 0), bend_deg=40,
                        sides=6, n=4)
        for a in range(6):    # tail tuft
            ang = 2 * math.pi * a / 6
            pk.ellipsoid(bm, L, (0.05 * math.cos(ang), 1.36 + 0.05 * math.sin(ang), 0.94), (0.07, 0.07, 0.08), LION_D,
                         useg=8, vseg=6)

    def face_w(co):
        if co.z > 1.1 and co.y < -0.2:
            return {"Head": 1.0}
        if co.y > 1.0:
            return {"Tail1": 1.0}
        return {("Leg_F" if co.y < 0.2 else "Leg_B") + ("L" if co.x > 0 else "R"): 1.0}
    k.part("Face", face, face_w)

    k.J_wing = {}
    for side, sx in (("L", 1), ("R", -1)):
        root, _ = k.surf((sx * 0.9, 0.18, 1.70), (0, 0.18, 0.95))
        root = root + Vector((0, 0, -0.02))
        arm = Vector((sx * 1.0, 0.45, 0.80))
        w, arm_point = pk.feather_wing(k, side, root, arm, 1.15, "Wing_" + side, "WingTip_" + side, WHITE_F, SKY, ROYAL,
                                       glow_trim=(TRIM, pk.lin((255, 211, 106))), prim_len=(0.78, 0.98), sec_len=0.62)
        k.J_wing[side] = (root, arm_point(0.5) + Vector((0, 0, 0.04)))


def rig(k):
    k.joint("Spine", (0, 0.26, 0.90), "Root", tail=(0, -0.45, 0.1))
    k.joint("Neck", (0, -0.22, 1.08), "Spine")
    k.joint("Head", (0, -0.46, 1.32), "Neck", tail=(0, -0.3, 0.05))
    k.joint("Tail1", (0, 0.86, 1.00), "Spine", tail=(0, 0.3, -0.16))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Leg_F" + side, (sx * 0.24, -0.14, 0.80), "Spine", tail=(0, 0, -0.5))
        k.joint("Leg_B" + side, (sx * 0.26, 0.62, 0.80), "Spine", tail=(0, 0, -0.5))
        S, W = k.J_wing[side]
        k.joint("Wing_" + side, S, "Spine")
        k.joint("WingTip_" + side, W, "Wing_" + side, tail=Vector((sx * 0.5, 0.25, 0.25)))
    k.body_bones = ["Spine", "Neck", "Head", "Tail1"] + cm.LEGS4


FOLD = dict(up=-28, fwd=-46, tip_up=-24, tip_fwd=-56)


def folded(k, f, d_up=0.0, d_fwd=0.0, d_tip=0.0):
    cm.wing_pair(k, f, FOLD["up"] + d_up, FOLD["fwd"] + d_fwd, FOLD["tip_up"] + d_tip, FOLD["tip_fwd"])


def flight(k):
    return cm.Flight(k, n=22, body_pitch=14, neck=-12, head=-10, amp=50, mid=10, sweep=16,
                     tuck={"Leg_FL": 64, "Leg_FR": 64, "Leg_BL": 80, "Leg_BR": 80}, tail=["Tail1"], tail_pitch=-6,
                     tail_wave=6, bob=0.08)


def rest_keys(k):
    def f_(f):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Neck", f, rot=(-6, 0, 0))
        k.key("Head", f, rot=(-4, 0, 0))
        folded(k, f)
        k.key("Tail1", f, rot=(0, 0, 0))
    return f_


def idle(k):
    """Alert guardian: snappy bird head turns (hold - snap - hold), preens its left wing, ruffles its feathers."""
    n = 96
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(0.8 * s, 0, 0), loc=(0, 0, 0.012 * (1 + s) / 2))
        k.key("Tail1", f, rot=(4 * pk.wave(f, n, 0.0, 2), 14 * pk.wave(f, n, 0.1, 3), 0))
    head = [(0, 0, -4, 0), (10, 0, -4, 0), (12, 34, -6, 8), (22, 34, -6, 8), (24, -30, -4, -6), (34, -30, -4, -6), (36, 0, -4, 0),
            (44, 0, -4, 0), (52, 60, 18, 20), (66, 60, 22, 20), (70, 60, 16, 20), (74, 60, 22, 20), (82, 0, -4, 0), (96, 0, -4, 0)]
    for f, yaw, hd, roll in head:
        k.key("Neck", f, rot=(hd * 0.4, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd * 0.6, yaw * 0.6, roll))
    for f, du, dt in ((0, 0, 0), (46, 0, 0), (52, 26, 18), (76, 26, 18), (84, 0, 0), (88, 10, 6), (90, -4, 0), (92, 8, 4), (96, 0, 0)):
        folded(k, f, du, 0, dt)
    cm.plant(k, n)
    k.finish()
    k.meta["planted"] = cm.LEGS4


def walk(k):
    n = 22

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.2 * pk.wave(f, n, 0.1, 2), 2 * pk.wave(f, n, 0.1), 3 * pk.wave(f, n)), loc=(0, 0, 0.04 * b))
        k.key("Neck", f, rot=(-6 + 4 * pk.wave(f, n, 0.0, 2), 0, 0))      # bird head-bob
        k.key("Head", f, rot=(-4 - 4 * pk.wave(f, n, 0.0, 2), 0, -2 * pk.wave(f, n)))
        k.key("Tail1", f, rot=(4 * pk.wave(f, n, 0.0, 2), 12 * pk.wave(f, n, 0.1), 0))
        folded(k, f, 3 * pk.wave(f, n, 0.1, 2))
    return cm.quad_walk(k, n, 0.68 * math.sin(math.radians(19)), 0.12, body, gait="walk")


def roar(k):
    """Screech: rears back a little, wings flung wide and high, beak to the sky, tail lashes; folds back."""
    n = 56
    k.new_action("roar", n, False)
    for f, sp, nk, hd, w in ((0, 0, -6, -4, 0), (10, 6, 2, 4, 0.2), (18, -14, -18, -18, 1), (40, -14, -20, -20, 1),
                             (48, 2, -6, -4, 0.2), (56, 0, -6, -4, 0)):
        k.key("Spine", f, rot=(sp, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        if w >= 1:
            cm.wing_pair(k, f, 46, 8, 20, 6)
        elif w > 0:
            folded(k, f, 20, 20, 10)
        else:
            folded(k, f)
        k.key("Tail1", f, rot=(20 * w, 0, 0))
    for f in range(20, 40, 3):
        w = 1 if (f // 3) % 2 else -1
        cm.wing_pair(k, f, 46 + 4 * w, 8, 20 + 6 * w, 6)
    cm.plant(k, n, legs=["Leg_BL", "Leg_BR"])
    cm.plant(k, n, legs=["Leg_FL", "Leg_FR"], frames=list(range(0, 13)) + list(range(46, n + 1)))
    for f in (22, 32, 40):
        for leg in ("Leg_FL", "Leg_FR"):
            k.key(leg, f, rot=(-50 if leg == "Leg_FL" else -30, 0, 0), loc=(0, 0, 0))
    k.finish(loop=False)


def ruffle(k):
    """act: a full-body feather ruffle - shimmy from head to tail, wings flick up twice, settles proudly."""
    n = 46
    k.new_action("act_ruffle", n, False)
    for f in (0, 6, 40, 46):
        k.key("Spine", f, rot=(0, 0, 0))
        k.key("Neck", f, rot=(-6, 0, 0))
        k.key("Head", f, rot=(-4, 0, 0))
        k.key("Tail1", f, rot=(0, 0, 0))
        folded(k, f)
    for i, f in enumerate(range(8, 38, 3)):
        w = 1 if i % 2 else -1
        d = 1 - i / 10
        k.key("Head", f, rot=(-4, 16 * w * d, 12 * w * d))
        k.key("Neck", f, rot=(-6, -6 * w * d, 0))
        k.key("Spine", f, rot=(0, 3 * w * d, -6 * w * d))
        k.key("Tail1", f, rot=(0, -14 * w * d, 0))
        folded(k, f, 18 if i in (2, 5) else 4, 0, 10 if i in (2, 5) else 0)
    cm.plant(k, n)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fl = flight(k)
    fl.fly()
    fl.takeoff(rest_keys(k))
    fl.land(rest_keys(k))
    roar(k)
    ruffle(k)
    return stride
