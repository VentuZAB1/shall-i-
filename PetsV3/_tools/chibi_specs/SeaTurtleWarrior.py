# Sea Turtle Warrior (Tide egg #2): a heroic sea-turtle soldier, rebuilt to STYLE_BIBLE.md (2026-10-08 pro pass):
# a big head under a red bandana (2 tails blowing back), bold blue eyes with thick 8 deg brows and a one-sided smirk,
# a pear torso with a cream plastron in 3 armour segments, a blue domed shell on a gold rim with raised scutes,
# shell-blue shoulder guards, stocky legs in a broad A-stance with red ankle wraps, fists with red wrist wraps and a
# chunky golden TRIDENT (barbed prongs, pearl in the fork) planted at its side, taller than the pet.
# Own moves: idle = guard stance, watches left and right, taps the trident butt on the ground twice, bandana tails
# flutter; walk = steady guard march (trident kept upright); roar = BATTLE CRY (fist pump, beak wide); signature =
# HELICOPTER TWIRL & SLAM (raises the trident, spins it flat over its head twice, drives it back into the ground).
import math
from mathutils import Vector, Quaternion

DISPLAY = "Sea Turtle Warrior"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 8.0

SKIN = (98, 204, 140)
CREAM = (246, 234, 184)
DARK = (24, 60, 70)
SHELL = (34, 112, 146)
SHELL_P = (56, 150, 184)
GOLD = (246, 196, 64)
BAND = (222, 52, 52)
BAND_D = (160, 30, 40)
PEARL = (230, 244, 255)
IRIS = (34, 70, 130)
MOUTH = (110, 26, 44)

S = (0.50, 0.0, 1.22)                         # shoulder
E = (0.57, 0.05, 0.96)                        # elbow
W = (0.62, -0.10, 0.78)                       # wrist
LEG = ((0.18, 0.02, 0.72), (0.22, -0.10, 0.36), (0.25, 0.02, 0.11))   # hip, knee, ankle joints (bent: IK reach)
LEG_GEO = ((0.18, 0.02, 0.60), (0.22, -0.02, 0.34), (0.25, 0.02, 0.11))   # straight A-stance leg blocks
GRIP = Vector((-0.62, -0.27, 0.68))           # right fist grip on the shaft
SHAFT = (0.03, 2.30)                          # shaft bottom / top z (trident upright at rest)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def model(k):
    """STYLE_BIBLE SeaTurtleWarrior: HW 1.05 TW, HH 0.92 TH, legs 0.55 TH x 0.42 TW, arms 0.30 TW, fists 1.3 x arm."""
    import blockkit as bk
    B = bk.Blocks(k, seed=83, tier=2, th=0.72)
    D = 0.62
    # ---- one torso: pear chest (18 % wider than the pelvis at the waist), pelvis overlap 39 %
    chest = B.add((0, 0.0, 1.00), (0.40, 0.28, 0.36), SKIN, "Chest", bot=(0.85, 0.92), density=D)
    B.add((0, 0.02, 0.60), (0.30, 0.24, 0.19), SKIN, "Spine", density=D)
    # waist belt (dark) with a gold buckle
    B.add((0, 0.0, 0.665), (0.35, 0.27, 0.045), DARK, "Spine", studs=[], role="limb")
    B.add((0, -0.272, 0.665), (0.075, 0.012, 0.058), GOLD, "Spine", studs=[], bevel=0.01)
    # cream plastron: 3 raised armour segments following the chest front taper (top widest)
    for zc, hw, hz in ((1.19, 0.29, 0.085), (1.00, 0.27, 0.08), (0.82, 0.22, 0.075)):
        t = (zc - 0.64) / 0.72
        yf = -0.28 * (0.92 + 0.08 * t)
        B.add((0, yf - 0.004, zc), (hw, 0.02, hz), CREAM, "Chest", rot=(-1.9, 0, 0), bot=(0.88, 1), studs=[],
              role="limb")
    # ---- shell: gold rim wider than the torso, a deep blue dome on it (peeks out behind the shoulders), raised scutes
    B.add((0, 0.33, 0.93), (0.53, 0.06, 0.48), GOLD, "Chest", studs=[], role="limb")
    dome = B.add((0, 0.57, 0.93), (0.49, 0.46, 0.20), SHELL, "Chest", rot=(-90, 0, 0), top=(0.70, 0.72),
                 studs=["+x", "-x", "-y"], density=D, role="mass", rnd=0.30)
    for u, v, hu, hv in ((0, -0.195, 0.10, 0.09), (0, 0.0, 0.10, 0.09), (0, 0.195, 0.10, 0.09),
                         (-0.215, -0.105, 0.09, 0.095), (0.215, -0.105, 0.09, 0.095), (-0.215, 0.105, 0.09, 0.095),
                         (0.215, 0.105, 0.09, 0.095)):
        B.on_face(dome, "+z", u * 1.12, v * 1.12, hu * 1.12, hv * 1.12, 0.05, SHELL_P, bevel=0.032)
    # ---- neck + head: HW 0.84, HH 0.66 (head sits on a short thick neck)
    B.add((0, 0.0, 1.42), (0.38, 0.20, 0.10), SKIN, "Neck", studs=[])
    head = B.add((0, -0.06, 1.80), (0.42, 0.30, 0.33), SKIN, "Head", top=(0.94, 0.94), density=0.50,
                 pmix=(0.85, 0.15, 0.0))
    # snout (skin, rounded beak, below the eye band) over a cream lower jaw (opens in the roar); the mouth line at
    # the seam curls up on one side (smirk)
    B.add((0, -0.40, 1.615), (0.24, 0.16, 0.10), SKIN, "Head", top=(0.86, 0.80), role="limb")
    for s in (1, -1):                                                     # nostrils
        B.add((s * 0.06, -0.541, 1.685), (0.022, 0.01, 0.014), DARK, "Head", rot=(-10, 0, 0), studs=[], bevel=0.005)
    for x0, z0, x1, z1 in ((-0.17, 1.522, 0.06, 1.522), (0.05, 1.522, 0.13, 1.538), (0.12, 1.535, 0.175, 1.575)):
        B.bar((x0, -0.562, z0), (x1, -0.562, z1), (0, -1, 0), 0.026, 0.008, DARK, "Head", studs=[], bevel=0.005)
    B.add((0, -0.40, 1.518), (0.20, 0.10, 0.006), MOUTH, "Head", studs=[], bevel=0.004)
    B.add((0, -0.42, 1.47), (0.225, 0.12, 0.055), CREAM, "Jaw", bot=(0.85, 0.9), role="limb")
    # bold eyes (2 highlights) under thick dark 8 deg brows that tuck under the bandana
    B.face_eyes(head, "bold", IRIS, base=SKIN, brow=DARK, z=0.54, scale=0.86, look=(0, 0.6),
                hl_on_pupil=True, hl_size=(0.05, 0.0), brow_spec=(0.30, 0.075, 8))
    # red bandana round the forehead (follows the head's top taper), knot + 2 flat tails blowing back
    tz = (2.05 - 1.47) / 0.66
    sx = 1 - 0.06 * tz
    B.add((0, -0.06, 2.05), (0.42 * sx + 0.014, 0.30 * sx + 0.014, 0.052), BAND, "Head", studs=[], role="limb")
    B.add((0, 0.27, 2.03), (0.08, 0.05, 0.065), BAND_D, "Head", studs=[], role="limb")
    for s in (1, -1):
        a, b, c = Vector((s * 0.05, 0.28, 2.03)), Vector((s * 0.15, 0.47, 1.96)), Vector((s * 0.22, 0.67, 1.91))
        n2 = (s * 0.5, -0.25, 1)                                     # Band2 twisted ~35 deg: broad face from behind
        B.bar(a, b, (0, -0.25, 1), 0.10, 0.03, BAND, "Band1", studs=[], role="limb")
        B.bar(b - (b - a).normalized() * 0.03, c, n2, 0.10, 0.03, BAND, "Band2", studs=[], role="limb")
        B.bar(c - (c - b).normalized() * 0.02, c + (c - b).normalized() * 0.11, n2, 0.10, 0.03, BAND,
              "Band2", studs=[], role="limb", top=(1, 0.1))
    # ---- arms: shoulder guard, upper arm, forearm with a red wrist wrap, big fist (1.3 x arm W)
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        B.seg(Sv, Ev, 0.12, 0.12, SKIN, "Arm_" + side, ext=0.10, studs=["-y", "+x" if s > 0 else "-x"], density=D)
        B.add(Sv + Vector((s * 0.06, 0, 0.05)), (0.13, 0.15, 0.055), SHELL, "Arm_" + side, rot=(0, -s * 22, 0),
              top=(0.72, 0.75), studs=[], role="limb")
        B.add(Sv + Vector((s * 0.06, 0, 0.015)), (0.14, 0.16, 0.022), GOLD, "Arm_" + side, rot=(0, -s * 22, 0),
              studs=[], role="limb")
        fa = B.seg(Ev, Wv, 0.11, 0.11, SKIN, "Fore_" + side, ext=0.05, studs=[])
        B.seg(Ev.lerp(Wv, 0.62), Wv.lerp(Ev, -0.02), 0.11 * 1.04, 0.11 * 1.04, BAND_D, "Fore_" + side, studs=[],
              role="limb")
        B.add(Wv + Vector((0, -0.10, -0.10)), (0.155, 0.15, 0.13), SKIN, "Hand_" + side, studs=[], role="limb")
        B.add(Wv + Vector((-s * 0.10, -0.20, -0.05)), (0.05, 0.06, 0.07), SKIN, "Hand_" + side, studs=[],
              role="limb")                                                   # thumb
    # ---- trident (own bone, child of the right hand): thick gold shaft, red grip wraps, barbed prongs, pearl
    x, y = GRIP.x, GRIP.y
    B.seg((x, y, SHAFT[0]), (x, y, SHAFT[1]), 0.044, 0.044, GOLD, "Trident", studs=[], role="limb")
    for zc in (0.52, 0.90):
        B.add((x, y, zc), (0.052, 0.052, 0.035), BAND_D, "Trident", studs=[], role="limb")
    B.add((x, y, SHAFT[0] + 0.04), (0.055, 0.055, 0.05), GOLD, "Trident", studs=[], role="limb")
    top = SHAFT[1]
    B.add((x, y, top), (0.075, 0.06, 0.06), GOLD, "Trident", studs=[], role="limb")              # collar
    B.add((x, y, top + 0.08), (0.24, 0.045, 0.04), GOLD, "Trident", studs=[], role="limb")       # crossbar
    for dx, ln in ((-0.20, 0.24), (0.0, 0.34), (0.20, 0.24)):
        p0 = Vector((x + dx, y, top + 0.08))
        p1 = p0 + Vector((0, 0, ln))
        B.seg(p0, p1, 0.04, 0.04, GOLD, "Trident", studs=[], role="limb")
        B.spike(p1 - Vector((0, 0, 0.02)), (0, 0, 1), 0.15, 0.06, GOLD, "Trident", side=(0, 1, 0), top=(0.1, 0.5))
        sd = -1 if dx < 0 else 1
        B.spike(p1 + Vector((sd * 0.03, 0, -0.02)), (sd * 0.6, 0, -1), 0.10, 0.025, GOLD, "Trident",
                side=(0, 1, 0), top=(0.15, 0.6))                                                  # barb
    B.add((x, y, top + 0.21), (0.075, 0.07, 0.075), PEARL, "Trident", studs=[], rnd=0.45, role="limb")   # pearl
    # ---- stocky legs in an A-stance: thigh + shin (top buried), red ankle wrap, foot with 3 cream claw nubs
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A = (X(p, s) for p in LEG_GEO)
        B.seg(H + Vector((0, 0, 0.06)), K, 0.17, 0.18, SKIN, "Leg_" + side, ext=0.0, ext1=0.04, density=D)
        B.seg(K, A, 0.145, 0.155, SKIN, "Shin_" + side, ext=0.08, density=D)
        B.seg(A.lerp(K, 0.32), A.lerp(K, 0.02), 0.145 * 1.04, 0.155 * 1.04, BAND_D, "Shin_" + side, studs=[],
              role="limb")
        B.add(A + Vector((s * 0.01, -0.06, -0.05)), (0.17, 0.215, 0.06), SKIN, "Foot_" + side, studs=[], role="limb")
        for gx in (-0.10, 0.0, 0.10):
            B.add(A + Vector((s * 0.01 + gx, -0.28, -0.07)), (0.03, 0.03, 0.026), CREAM, "Foot_" + side, studs=[])
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.02, 0.62), "Root", tail=(0, 0, 0.3))
    k.joint("Chest", (0, 0.0, 0.76), "Spine", tail=(0, 0, 0.4))
    k.joint("Neck", (0, 0.0, 1.36), "Chest", tail=(0, 0, 0.12))
    k.joint("Head", (0, 0.0, 1.48), "Neck", tail=(0, 0, 0.3))                # neck-top pivot
    k.joint("Jaw", (0, -0.28, 1.51), "Head", tail=(0, -0.2, 0))
    k.joint("Band1", (0, 0.27, 2.03), "Head", tail=(0, 0.18, -0.06))
    k.joint("Band2", (0, 0.47, 1.96), "Band1", tail=(0, 0.2, -0.06))
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        k.joint("Arm_" + side, Sv, "Chest")
        k.joint("Fore_" + side, Ev, "Arm_" + side)
        k.joint("Hand_" + side, Wv, "Fore_" + side, tail=(0, -0.05, -0.2))
        H, K, A = (X(p, s) for p in LEG)
        k.joint("Leg_" + side, H, "Spine")
        k.joint("Shin_" + side, K, "Leg_" + side)
        k.joint("Foot_" + side, A, "Shin_" + side, tail=(0, -0.2, 0))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))
    k.joint("Trident", GRIP, "Hand_R", tail=(0, 0, 0.5))


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS2 = ["Leg_L", "Leg_R"]


def arm(k, f, side, pitch=0.0, yaw=0.0, roll=0.0, elbow=0.0, hand=0.0):
    s = 1 if side == "L" else -1
    k.key("Arm_" + side, f, rot=(pitch, s * yaw, -s * roll))
    k.key("Fore_" + side, f, rot=(-elbow, 0, 0))
    k.key("Hand_" + side, f, rot=(-hand, 0, 0))


def hold(k, f, pitch, roll, elbow, hand=0.0):
    """keep the trident upright in the chest frame: cancel the right arm's pitch / roll (the big head sits right
    next to the shaft, so it must not lean back over the head)"""
    k.key("Trident", f, rot=(elbow + hand - pitch, 0, -roll))


def band(k, f, n, amp=8.0, lift=0.0, phase=0.0, cycles=2):
    cm.chain(k, f, n, ["Band1", "Band2"], sway=amp, pitch=lift, phase=phase, cycles=cycles, lag=0.18, grow=0.6)


def idle(k):
    """guard stance: steady breathing bob, watches left, then right, taps the trident butt twice on the ground,
    bandana tails flutter in the sea breeze."""
    n = 140
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 4)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.01 * b))
        k.key("Chest", f, rot=(-1.2 * b, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        band(k, f, n, amp=7, lift=4 + 3 * pk.wave(f, n, 0.2, 4), cycles=4)
        arm(k, f, "L", pitch=-4 + 1.5 * b, roll=10, elbow=20, hand=30)
    for f, ny, hy, hp in ((0, 0, 0, 0), (26, 0, 0, 0), (34, 10, 22, 2), (54, 10, 22, 2), (62, -8, -20, 2), (82, -8, -20, 2),
                          (92, 0, 0, 0), (140, 0, 0, 0)):
        k.key("Neck", f, rot=(0, ny, 0))
        k.key("Head", f, rot=(hp, hy, 0))
    for f, p, el in ((0, -8, 12), (96, -8, 12), (100, -12, 30), (103, -8, 12), (106, -12, 30), (109, -8, 12),
                     (140, -8, 12)):
        arm(k, f, "R", pitch=p, roll=4, elbow=el, hand=0)
        hold(k, f, p, 4, el)
    cm.plant(k, n, legs=LEGS2)
    k.finish()
    k.meta["planted"] = LEGS2


def walk(k):
    n = 28

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(2, 4 * pk.wave(f, n, 0.0), 3 * pk.wave(f, n, 0.0)), loc=(0, 0, -0.025 * b))
        k.key("Chest", f, rot=(2, -5 * pk.wave(f, n, 0.0), -2 * pk.wave(f, n, 0.0)))
        k.key("Neck", f, rot=(0, 0, 0))
        k.key("Head", f, rot=(-2, 3 * pk.wave(f, n, 0.0), 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        band(k, f, n, amp=10, lift=14, cycles=2)
        hold(k, f, -14 + 2 * pk.wave(f, n, 0.0, 2), 4, 16)
        arm(k, f, "L", pitch=-4 + 22 * pk.wave(f, n, 0.55), roll=10, elbow=24 + 8 * pk.wave(f, n, 0.7), hand=30)
        arm(k, f, "R", pitch=-14 + 2 * pk.wave(f, n, 0.0, 2), roll=4, elbow=16, hand=0)
    return cm.biped_walk(k, n, 0.18, 0.12, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.6)


def roar(k):
    """BATTLE CRY: braces, plants the trident at its side, leans back and punches its left fist at the sky twice,
    chest out, head thrown back with the beak wide open; bandana tails whip."""
    n = 66
    k.new_action("roar", n, False)
    for f, z, ch, hd, jw, lp, lel in ((0, 0, 0, 0, 2, -4, 20), (12, -0.08, 8, 6, 2, -10, 70), (20, 0.02, -12, -20, 36, -160, 8),
                                      (28, 0.0, -10, -16, 30, -130, 44), (34, 0.02, -12, -20, 38, -162, 6),
                                      (46, 0.02, -12, -20, 36, -160, 8), (56, -0.02, 2, -4, 8, -30, 50), (66, 0, 0, 0, 2, -4, 20)):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(0, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        hold(k, f, -8 if f in (0, 66) else -6, 4, 12 if f in (0, 66) else 8)
        arm(k, f, "R", pitch=-8 if f in (0, 66) else -6, roll=4, elbow=12 if f in (0, 66) else 8, hand=0)
        arm(k, f, "L", pitch=lp, roll=18, elbow=lel, hand=24)          # straight-wrist fist pump
    for f in range(0, n + 1, 2):
        band(k, f, n, amp=12, lift=10 + 20 * (16 <= f <= 50), cycles=3)
    for f in range(22, 46, 2):
        k.key("Jaw", f, rot=(35 + (2 if (f // 2) % 2 else -2), 0, 0))
    cm.plant(k, n, legs=LEGS2)
    k.finish(loop=False)


def _key_q(k, bone, f, q):
    pb = k.arm.pose.bones[bone]
    R0 = k.arm.data.bones[bone].matrix_local.to_quaternion()
    pb.rotation_quaternion = R0.inverted() @ q @ R0
    pb.keyframe_insert("rotation_quaternion", frame=f, group=bone)


def twirl(k):
    """SIGNATURE - HELICOPTER TWIRL & SLAM: raises the trident overhead, tips it flat and spins it twice over its head
    (body braced, left fist out), then drives it back down and SLAMS the butt into the ground with a stomp."""
    import bpy
    n = 112
    k.new_action("act_twirl", n, False)
    for f, z, ch, hd, jw in ((0, 0, 0, 0, 2), (10, -0.05, 4, 2, 2), (16, 0.0, -6, -10, 2), (54, 0.0, -6, -10, 2),
                             (62, 0.02, -4, -6, 20), (70, -0.12, 10, 4, 30), (74, -0.10, 8, 2, 10), (88, -0.06, 4, 0, 2),
                             (100, 0, 0, 0, 2), (112, 0, 0, 0, 2)):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(0, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
    UP = dict(pitch=-168, roll=6, elbow=6, hand=0)
    for f, a in ((0, dict(pitch=-8, roll=4, elbow=12, hand=0)), (10, dict(pitch=-60, roll=6, elbow=50, hand=0)), (16, UP),
                 (54, UP), (58, dict(pitch=-166, roll=16, elbow=6, hand=0)), (64, dict(pitch=-90, roll=16, elbow=0, hand=0)),
                 (70, dict(pitch=-14, roll=4, elbow=14, hand=0)),
                 (100, dict(pitch=-14, roll=4, elbow=14, hand=0)), (112, dict(pitch=-8, roll=4, elbow=12, hand=0))):
        arm(k, f, "R", **a)
    for f, p, ro, el, hd in ((0, -4, 10, 20, 30), (16, -20, 70, 20, 60), (54, -20, 70, 20, 60), (66, -10, 20, 40, 60),
                             (74, -40, 14, 90, 60), (100, -30, 12, 70, 60), (112, -4, 10, 20, 30)):
        arm(k, f, "L", pitch=p, roll=ro, elbow=el, hand=hd)
    for f in range(0, n + 1, 2):
        spin = 16 <= f <= 54
        band(k, f, n, amp=16 if spin else 8, lift=24 if spin else 8, cycles=6)
    hold(k, 0, -8, 4, 12)
    k.bake_bezier_now()
    sc = bpy.context.scene
    hb = k.arm.pose.bones["Hand_R"]

    def upright(f):
        """trident rotation (hand frame) that keeps it upright in the world at frame f"""
        sc.frame_set(f)
        Rf = hb.matrix.to_quaternion() @ k.arm.data.bones["Hand_R"].matrix_local.to_quaternion().inverted()
        return Rf.inverted()
    _key_q(k, "Trident", 8, upright(8))
    # spin: world-vertical axis expressed in the trident's parent (hand) frame, measured at the overhead pose
    sc.frame_set(35)
    Rh = hb.matrix.to_quaternion() @ k.arm.data.bones["Hand_R"].matrix_local.to_quaternion().inverted()
    axis = Rh.inverted() @ Vector((0, 0, 1))
    flat = Vector((0, 0, 1)).rotation_difference(Rh.inverted() @ Vector((0, -1, 0)))
    # the big head is taller than the raised fist: the spinning trident rides up the grip so it whirls ABOVE the head
    tb = k.arm.pose.bones["Trident"]
    R0 = k.arm.data.bones["Trident"].matrix_local.to_quaternion()
    gz = (k.arm.matrix_world @ tb.head).z
    up = R0.inverted() @ (Rh.inverted() @ Vector((0, 0, max(0.0, 2.36 - gz))))
    for f, l in ((0, Vector()), (8, Vector()), (16, up), (54, up), (62, Vector()), (n, Vector())):   # keys span 0..n (CYCLES)
        tb.location = l
        tb.keyframe_insert("location", frame=f, group="Trident")
    _key_q(k, "Trident", 16, flat)
    for f in range(17, 55):
        u = (f - 16) / 38
        deg = 720 * (0.5 - 0.5 * math.cos(math.pi * u))
        _key_q(k, "Trident", f, Quaternion(axis, math.radians(deg)) @ flat)
    # still overhead: turn the trident UPRIGHT in the world (q = inverse of the hand's rotation), then lower it beside
    # the body like a flag pole and drive it into the ground - the shaft never sweeps through the body
    prev = Quaternion(axis, math.radians(720)) @ flat
    for f in (58, 64):
        sc.frame_set(f)
        Rf = hb.matrix.to_quaternion() @ k.arm.data.bones["Hand_R"].matrix_local.to_quaternion().inverted()
        q = Rf.inverted()
        if q.dot(prev) < 0:
            q = -q
        _key_q(k, "Trident", f, q)
        prev = q
    for f in (70, 100, 112):                 # slammed in upright beside the body, held upright back to the guard
        q = upright(f)
        if q.dot(prev) < 0:
            q = -q
        _key_q(k, "Trident", f, q)
        prev = q
    k.bake_bezier_now()
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS2:
            T = Vector((k.J[leg].x, k.J[leg].y, 0.0))
            if leg == "Leg_L" and 62 <= f <= 70:                  # stomp with the slam
                T.z = 0.16 * math.sin(math.pi * (f - 62) / 8)
            k.solve_leg(leg, f, T)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    twirl(k)
    return stride


def check_pairs():
    P = [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R")]
    for b in ("Head", "Neck", "Chest", "Spine", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Foot_L", "Foot_R", "Arm_L",
              "Fore_L", "Hand_L", "Band1", "Band2"):
        P.append(("Trident", b))
    for s in ("L", "R"):
        for a in ("Fore_" + s, "Hand_" + s):
            for b in ("Spine", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Head", "Jaw"):
                P.append((a, b))
    for b in ("Chest", "Arm_L", "Arm_R"):
        P.append(("Band2", b))
    P += [("Head", "Chest"), ("Jaw", "Chest"), ("Band1", "Chest"), ("Head", "Arm_L"), ("Head", "Arm_R")]
    P += [("Fore_L", "Chest"), ("Fore_R", "Chest"), ("Hand_L", "Chest"), ("Hand_R", "Chest")]   # shell vs arms
    return P


def joints():
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        Wv = X(W, s)
        out.append((Wv, Wv, 0.09, "Hand_" + side))
    out.append((GRIP + Vector((0, 0, -0.1)), GRIP + Vector((0, 0, 0.1)), 0.10, "Trident"))
    return out
