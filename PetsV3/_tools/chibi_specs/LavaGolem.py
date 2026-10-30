# Lava Golem (Magma egg #2, tier 4): a hulking living volcano rebuilt to STYLE_BIBLE.md (2026-10-08 pro pass) as a
# gorilla brute: a basalt boulder torso with a MAGMA HEART (a recessed diamond cluster of orange plates framed by
# rock) and lava cracks running from the heart to the shoulders and hips, huge spiked shoulder boulders, the head
# sunk between them (deep brow shelf, fierce ember eyes, an underbite with 4 square teeth), long thick arms ending in
# boulder fists with knuckle plates, short pillar legs with knee plates and dark stone feet. No glow (embers/drips =
# particle VFX). Own moves: idle = heavy breaths, lifts a fist to inspect it, punches its own palm twice, cracks its
# knuckles; walk = slow earth-shaking stomp; roar = FLEX ROAR (double-biceps flex, head back, jaw wide); signature =
# GROUND POUND (right fist, left fist, then a jumping double-fisted smash).
import math
from mathutils import Vector, Euler

DISPLAY = "Lava Golem"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 10.0

BASALT = (62, 54, 66)
TOPS = (98, 88, 102)
DARK = (30, 26, 34)
MAGMA = (255, 118, 30)
MAGMA_Y = (255, 200, 70)
IRIS = (255, 200, 70)
TEETH = (236, 226, 206)
MOUTH = (255, 118, 30)          # lava glows inside the mouth (plain orange, no Neon)

S = (0.74, 0.02, 1.52)          # shoulder / elbow / wrist (left side)
E = (0.86, -0.04, 1.08)
W = (0.90, -0.12, 0.66)
LEG = ((0.30, 0.04, 0.64), (0.30, -0.06, 0.36), (0.30, 0.04, 0.12))
TH = 0.70           # plate grid from the pelvis-to-chest core (the boulder chest is 0.90 tall)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def zig(B, pts, n, bone, w=0.08, color=MAGMA, tip=True):
    """lava crack: zigzag of flat bars through world points pts on a surface with normal n, last one pointed"""
    P = [Vector(p) for p in pts]
    for i, (a, b) in enumerate(zip(P, P[1:])):
        last = tip and i == len(P) - 2
        B.bar(a, b, n, w, 0.014, color, bone, studs=[], bevel=0.008, **({"top": (1, 0.3)} if last else {}))


def side_crack(B, blk, s, pts, w=0.075):
    """lava crack on the +-x face of a top-tapered block, following the taper; pts = [(y, z)] local"""
    hx, hz, tk = blk.h.x, blk.h.z, 1 - blk.top[0]

    def P(y, z):
        return blk.world(Vector((s * (hx * (1 - tk * (z + hz) / (2 * hz)) + 0.006), y, z)))
    n = (blk.R @ Vector((s, 0, hx * tk / (2 * hz)))).normalized()
    zig(B, [P(y, z) for y, z in pts], n, blk.bone, w=w)


def model(k):
    """STYLE_BIBLE LavaGolem (brute biped): see the header."""
    import blockkit as bk
    B = bk.Blocks(k, seed=113, tier=4, th=TH)
    D = 0.62
    # ---- torso: V-shaped boulder chest (bottom 0.78) over a dark pelvis 11 % narrower
    chest = B.add((0, 0.02, 1.20), (0.60, 0.40, 0.45), BASALT, "Chest", bot=(0.78, 0.85), top=(0.95, 0.92), density=D)
    B.add((0, 0.04, 0.66), (0.42, 0.30, 0.17), DARK, "Spine", density=D)

    def front(x, z, off=0.004):
        """point on the chest front face (taper-aware) and its normal"""
        t = (z - (chest.c.z - chest.h.z)) / (2 * chest.h.z)
        sy = chest.bot[1] + (chest.top[1] - chest.bot[1]) * t
        sx = chest.bot[0] + (chest.top[0] - chest.bot[0]) * t
        y = chest.c.y - chest.h.y * sy - off
        n = Vector((0, -1, -chest.h.y * (chest.top[1] - chest.bot[1]) / (2 * chest.h.z))).normalized()
        return Vector((x, y, z)), n, chest.h.x * sx
    # ---- magma heart: an orange diamond with a 2x2 cluster of bright plates, framed by a raised rock diamond
    hc, n, _ = front(0, 1.10)
    Rd = bk.frame_from(Vector(), n, Vector((1, 0, 1)))           # local z = out of the chest, x along a diagonal
    B.add(hc + n * 0.012, (0.13, 0.13, 0.018), MAGMA, "Chest", R=Rd, studs=[], bevel=0.012, role="limb")
    for du, dv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        B.add(hc + n * 0.034 + Rd @ Vector((du * 0.063, dv * 0.063, 0)), (0.049, 0.049, 0.016), MAGMA_Y, "Chest",
              R=Rd, top=(0.7, 0.7), studs=[], bevel=0.008, role="detail")
    for i in range(4):                                             # raised rock frame (4 bars on the diamond edges)
        a = math.radians(45 + 90 * i)
        u = Vector((math.cos(a), 0, math.sin(a)))
        v = Vector((-math.sin(a), 0, math.cos(a)))
        mid = hc + u * 0.185 + n * 0.03
        B.bar(mid - v * 0.225, mid + v * 0.225, n, 0.075, 0.035, TOPS, "Chest", studs=[], role="limb")
    # lava cracks from the heart corners to the shoulders and down to the hips
    for s in (1, -1):
        pts = [front(s * x, z)[0] for x, z in ((0.20, 1.17), (0.31, 1.24), (0.27, 1.32), (0.42, 1.42))]
        zig(B, pts, n, "Chest")
        pts = [front(s * x, z)[0] for x, z in ((0.15, 0.99), (0.25, 0.93), (0.20, 0.86), (0.29, 0.79))]
        zig(B, pts, n, "Chest", w=0.07)
    # a fissure down the back (seen when it follows the player), with one branch
    def back(x, z, off=0.004):
        t = (z - (chest.c.z - chest.h.z)) / (2 * chest.h.z)
        sy = chest.bot[1] + (chest.top[1] - chest.bot[1]) * t
        return Vector((x, chest.c.y + chest.h.y * sy + off, z))
    nb = Vector((0, 1, -chest.h.y * (chest.top[1] - chest.bot[1]) / (2 * chest.h.z))).normalized()
    zig(B, [back(x, z) for x, z in ((0.02, 1.56), (0.12, 1.42), (-0.04, 1.28), (0.09, 1.13), (-0.03, 0.98))], nb, "Chest",
        w=0.08)
    zig(B, [back(-0.04, 1.28), back(-0.17, 1.22), back(-0.26, 1.30)], nb, "Chest", w=0.065)
    # ---- spiked shoulder boulders (rock tops) with 3 two-tone spikes each
    for s in (1, -1):
        bd = B.add((s * 0.66, 0.08, 1.64), (0.27, 0.28, 0.26), TOPS, "Chest", top=(0.82, 0.85), density=D)
        for p, d, ln, w in (((s * 0.66, 0.02, 1.86), (s * 0.10, 0.45, 1), 0.28, 0.10),
                            ((s * 0.52, 0.22, 1.85), (s * 0.10, 0.55, 1), 0.24, 0.085),
                            ((s * 0.78, 0.26, 1.80), (s * 0.45, 0.65, 0.6), 0.20, 0.075)):
            d = Vector(d).normalized()
            B.spike(p, d, ln, w, BASALT, "Chest", top=(0.40, 0.40), role="limb")
            B.spike(Vector(p) + d * ln * 0.62, d, ln * 0.42, w * 0.58, MAGMA, "Chest", top=(0.12, 0.12), role="limb")
    # ---- head sunk between the shoulders: deep brow shelf, fierce eyes, underbite with 4 square teeth
    head = B.add((0, -0.20, 1.66), (0.42, 0.30, 0.27), BASALT, "Head", top=(0.92, 0.94), density=D,
                 studs=["+x", "-x", "+z"])
    B.face_eyes(head, "fierce", IRIS, base=BASALT, brow=None, look=(0, 0.6), z=0.60, pupil_size=(0.085, 0.088),
                hl_size=(0.06, 0.0), hl_on_pupil=True)
    for s in (1, -1):                                              # brow shelf: 2 slabs, inner ends down 18 deg
        B.add((s * 0.20, -0.545, 1.865), (0.22, 0.07, 0.055), TOPS, "Head", rot=(0, -s * 18, 0), studs=[], role="limb")
    B.add((0, -0.505, 1.475), (0.30, 0.008, 0.022), MOUTH, "Head", studs=[], bevel=0.006)          # mouth line
    B.add((0, -0.40, 1.42), (0.35, 0.18, 0.075), BASALT, "Jaw", bot=(0.9, 0.9), studs=[], role="limb")
    B.add((0, -0.38, 1.497), (0.30, 0.15, 0.006), MOUTH, "Jaw", studs=[], bevel=0.004)
    for x in (-0.21, -0.07, 0.07, 0.21):
        B.add((x, -0.53, 1.525), (0.048, 0.035, 0.05), TEETH, "Jaw", top=(0.8, 0.8), studs=[], role="limb")
    # ---- arms: thick upper arm, thicker gorilla forearm, boulder fist with knuckle plates
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        B.seg(Sv, Ev, 0.20, 0.21, BASALT, "Arm_" + side, ext=0.12, density=D)
        B.seg(Ev, Wv, 0.25, 0.26, BASALT, "Fore_" + side, ext=0.06, density=D)
        ax = (Wv - Ev).normalized()
        ny = (Vector((0, -1, 0)) - ax * (-ax.y)).normalized()                 # front face normal of the forearm
        nx = (Vector((s, 0, 0)) - ax * ax.x * s).normalized()
        cp = [Ev + (Wv - Ev) * t + ny * 0.266 + nx * dx for t, dx in
              ((-0.06, 0.13 * s), (0.20, 0.05 * s), (0.38, 0.12 * s), (0.62, 0.0), (0.86, 0.07 * s))]
        zig(B, cp, ny, "Fore_" + side, w=0.07, tip=False)                     # fissure down the forearm front
        zig(B, [cp[2], cp[2] + (Wv - Ev) * 0.16 + nx * (0.10 * s)], ny, "Fore_" + side, w=0.06)   # branch
        fc = Wv + Vector((0, -0.04, -0.28))
        B.add(fc, (0.32, 0.31, 0.27), TOPS, "Hand_" + side, top=(0.92, 0.92), density=D)
        for dx in (-0.22, -0.075, 0.075, 0.22):
            B.add(fc + Vector((dx, -0.29, 0.15)), (0.065, 0.06, 0.075), BASALT, "Hand_" + side, studs=[], role="limb")
    # ---- short pillar legs: thigh, shin with a knee plate, dark stone feet with 3 toe nubs
    for s, side in ((1, "L"), (-1, "R")):
        x = s * LEG[0][0]
        B.add((x, 0.04, 0.49), (0.22, 0.24, 0.21), BASALT, "Leg_" + side, bot=(0.9, 0.92), density=D)
        B.add((x, 0.02, 0.235), (0.18, 0.20, 0.155), BASALT, "Shin_" + side, density=D)
        B.add((x, -0.215, 0.34), (0.14, 0.035, 0.09), TOPS, "Shin_" + side, studs=[], role="limb")
        B.add((x, -0.06, 0.065), (0.23, 0.30, 0.065), DARK, "Foot_" + side, studs=[], role="limb")
        for dx in (-0.14, 0.0, 0.14):
            B.add((x + dx, -0.37, 0.05), (0.05, 0.035, 0.04), TOPS, "Foot_" + side, studs=[], role="limb")
        fy = lambda z: 0.04 - 0.24 * (0.92 + 0.08 * (z - 0.28) / 0.42) - 0.006      # thigh front (bot taper)
        zig(B, [(x + s * 0.06, fy(0.64), 0.64), (x - s * 0.04, fy(0.55), 0.55), (x + s * 0.03, fy(0.46), 0.46),
                (x - s * 0.02, fy(0.37), 0.37)], (0, -1, -0.046), "Leg_" + side, w=0.07)
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.04, 0.66), "Root", tail=(0, 0, 0.3))
    k.joint("Chest", (0, 0.02, 0.84), "Spine", tail=(0, 0, 0.5))
    k.joint("Head", (0, -0.06, 1.46), "Chest", tail=(0, 0, 0.3))           # pivot low at the back of the throat
    k.joint("Jaw", (0, -0.24, 1.47), "Head", tail=(0, -0.3, 0))
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        k.joint("Arm_" + side, Sv, "Chest")
        k.joint("Fore_" + side, Ev, "Arm_" + side)
        k.joint("Hand_" + side, Wv, "Fore_" + side, tail=(0, -0.05, -0.25))
        H, K, A = (X(p, s) for p in LEG)
        k.joint("Leg_" + side, H, "Spine")
        k.joint("Shin_" + side, K, "Leg_" + side)
        k.joint("Foot_" + side, A, "Shin_" + side, tail=(0, -0.25, 0))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS2 = ["Leg_L", "Leg_R"]


def arm(k, f, side, pitch=0.0, yaw=0.0, roll=0.0, elbow=0.0, hand=0.0, ef=0.0):
    """pitch - raises the arm forward, roll + lifts it out to the side, yaw + swings it inward (across the body),
    elbow + bends the forearm forward/up, ef + bends it UP in the side plane (flex), hand + curls the fist."""
    s = 1 if side == "L" else -1
    k.key("Arm_" + side, f, rot=(pitch, s * yaw, -s * roll))
    k.key("Fore_" + side, f, rot=(-elbow, 0, -s * ef))
    k.key("Hand_" + side, f, rot=(-hand, 0, 0))


REST = dict(pitch=-6, roll=8, elbow=16, hand=0)


def idle(k):
    """heavy slow breaths; lifts the right fist and turns it to inspect it, punches its left palm twice, then holds
    both fists together and cracks its knuckles."""
    n = 150
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 4)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.012 * b))
        k.key("Chest", f, rot=(4 - 1.8 * b, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
    for f, hp, hy in ((0, 0, 0), (18, 0, 0), (28, 10, -22), (50, 10, -22), (58, 6, 0), (82, 6, 0), (96, 8, 0), (120, 8, 0),
                      (132, 0, 0), (150, 0, 0)):
        k.key("Head", f, rot=(hp, hy, 0))
    R = {0: REST, 18: REST, 28: dict(pitch=-60, yaw=0, roll=16, elbow=78, hand=10),
         36: dict(pitch=-60, yaw=-4, roll=18, elbow=82, hand=-20), 44: dict(pitch=-60, yaw=0, roll=16, elbow=78, hand=20),
         52: dict(pitch=-50, yaw=20, roll=4, elbow=70, hand=0), 58: dict(pitch=-56, yaw=26, roll=2, elbow=96, hand=10),
         62: dict(pitch=-62, yaw=30, roll=2, elbow=56, hand=10), 66: dict(pitch=-56, yaw=26, roll=2, elbow=96, hand=10),
         70: dict(pitch=-62, yaw=30, roll=2, elbow=56, hand=10), 76: dict(pitch=-50, yaw=24, roll=4, elbow=90, hand=0),
         96: dict(pitch=-54, yaw=24, roll=4, elbow=74, hand=0), 104: dict(pitch=-54, yaw=24, roll=4, elbow=74, hand=32),
         108: dict(pitch=-54, yaw=24, roll=4, elbow=74, hand=0), 112: dict(pitch=-54, yaw=24, roll=4, elbow=74, hand=32),
         120: dict(pitch=-54, yaw=24, roll=4, elbow=74, hand=0), 134: REST, 150: REST}
    L = {0: REST, 50: REST, 58: dict(pitch=-52, yaw=26, roll=4, elbow=84, hand=-20), 76: dict(pitch=-52, yaw=26, roll=4, elbow=84, hand=-20),
         96: dict(pitch=-54, yaw=24, roll=4, elbow=74, hand=0), 104: dict(pitch=-54, yaw=24, roll=4, elbow=74, hand=32),
         108: dict(pitch=-54, yaw=24, roll=4, elbow=74, hand=0), 112: dict(pitch=-54, yaw=24, roll=4, elbow=74, hand=32),
         120: dict(pitch=-54, yaw=24, roll=4, elbow=74, hand=0), 134: REST, 150: REST}
    for f, a in R.items():
        arm(k, f, "R", **a)
    for f, a in L.items():
        arm(k, f, "L", **a)
    for f, z in ((60, 0), (62, -0.015), (65, 0), (68, 0), (70, -0.015), (73, 0)):
        k.key("Spine", f, loc=(0, 0, z))
    cm.plant(k, n, legs=LEGS2)
    k.finish()
    k.meta["planted"] = LEGS2


def walk(k):
    n = 40

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(2, 4 * pk.wave(f, n, 0.0), 6 * pk.wave(f, n, 0.0)), loc=(0, 0, -0.03 * b))
        k.key("Chest", f, rot=(6, -6 * pk.wave(f, n, 0.0), -3 * pk.wave(f, n, 0.05)))
        k.key("Head", f, rot=(-4, 3 * pk.wave(f, n, 0.0), 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        for side, ph in (("L", 0.5), ("R", 0.0)):
            arm(k, f, side, pitch=-6 + 16 * pk.wave(f, n, ph + 0.05), roll=10, elbow=20 + 8 * pk.wave(f, n, ph + 0.15),
                hand=0)
    return cm.biped_walk(k, n, 0.17, 0.09, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.62)


def roar(k):
    """FLEX ROAR: crouches, then rises into a double-biceps flex (both fists up beside the head), chest out, head
    thrown back with the rock jaw wide; pulses the flex twice, then drops the arms with a grunt."""
    n = 76
    k.new_action("roar", n, False)
    FLEX = dict(pitch=-12, roll=88, elbow=6, ef=94, hand=30)
    for f, z, ch, hd, jw, a in ((0, 0, 4, 0, 0, REST), (12, -0.06, 12, 6, 0, dict(pitch=-20, roll=40, elbow=20, ef=30, hand=20)),
                                (22, 0.02, -8, -18, 24, FLEX), (32, 0.0, -6, -16, 20, dict(pitch=-10, roll=86, elbow=6, ef=102, hand=40)),
                                (38, 0.02, -8, -18, 26, FLEX), (46, 0.0, -6, -16, 20, dict(pitch=-10, roll=86, elbow=6, ef=102, hand=40)),
                                (52, 0.02, -8, -18, 24, FLEX), (62, -0.03, 6, 2, 4, dict(pitch=-10, roll=20, elbow=30, hand=0)),
                                (76, 0, 4, 0, 0, REST)):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        arm(k, f, "L", **a)
        arm(k, f, "R", **a)
    cm.plant(k, n, legs=LEGS2)
    k.finish(loop=False)


def pound(k):
    """SIGNATURE - GROUND POUND: raises the right fist high and pounds the ground, then the left; then clasps both fists
    overhead, JUMPS and smashes them into the ground with its full weight, holds the impact, rises."""
    import bpy
    n = 124
    k.new_action("act_pound", n, False)
    UPR = dict(pitch=-150, roll=20, elbow=40, hand=20)
    HIT = dict(pitch=-52, roll=10, elbow=0, hand=20)
    CLASP = dict(pitch=-160, yaw=24, roll=0, elbow=30, hand=20)
    SMASH = dict(pitch=-56, yaw=18, roll=0, elbow=0, hand=20)
    R = {0: REST, 12: UPR, 22: HIT, 28: HIT, 36: dict(pitch=-20, roll=12, elbow=40, hand=0), 50: dict(pitch=-30, roll=10, elbow=40),
         62: CLASP, 74: CLASP, 84: SMASH, 96: SMASH, 110: dict(pitch=-20, roll=10, elbow=30), 124: REST}
    L = {0: REST, 22: dict(pitch=-20, roll=12, elbow=40), 34: UPR, 44: HIT, 50: HIT, 56: dict(pitch=-30, roll=10, elbow=40),
         62: CLASP, 74: CLASP, 84: SMASH, 96: SMASH, 110: dict(pitch=-20, roll=10, elbow=30), 124: REST}
    for f, a in R.items():
        arm(k, f, "R", **a)
    for f, a in L.items():
        arm(k, f, "L", **a)
    body = {0: (0, 4, 0, 0, 0), 12: (0.0, -6, -6, -8, 0), 22: (-0.03, 38, -10, 6, 14), 28: (-0.02, 36, -10, 4, 0),
            36: (0.0, 6, 6, 0, 0), 44: (-0.03, 38, 10, 6, 14), 50: (-0.02, 36, 10, 4, 0), 56: (-0.01, 6, 0, 0, 0),
            62: (-0.04, -10, 0, -14, 0), 70: (-0.10, -4, 0, -10, 0), 76: (0.22, -12, 0, -16, 20), 84: (-0.04, 41, 0, 8, 26),
            96: (-0.03, 37, 0, 6, 4), 110: (-0.01, 8, 0, 0, 0), 124: (0, 4, 0, 0, 0)}
    for f, (z, ch, yw, hd, jw) in body.items():
        k.key("Spine", f, rot=(0, yw * 0.4, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, yw, 0))
        k.key("Head", f, rot=(hd - ch * 0.5, -yw * 0.3, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene

    def air(f):
        if 72 <= f <= 82:
            return 0.30 * math.sin(math.pi * (f - 72) / 10)
        return 0.0

    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS2:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, air(f))))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    pound(k)
    return stride


def check_pairs():
    P = [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R")]
    for s in ("L", "R"):
        for a in ("Fore_" + s, "Hand_" + s):
            for b in ("Spine", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Foot_L", "Foot_R", "Head", "Jaw"):
                P.append((a, b))
        P.append(("Hand_" + s, "Chest"))
    return P


def joints():
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        Wv = X(W, s)
        out.append((Wv, Wv, 0.14, "Hand_" + side))
    return out
