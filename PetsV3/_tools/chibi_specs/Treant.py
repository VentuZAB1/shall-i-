# Treant (Wood egg #3, T1 top, biped): a friendly barrel-trunk tree spirit in the Steal-an-Egg block style, rebuilt
# to STYLE_BIBLE.md (2026-10-08 pro pass): the upper half of the trunk IS the face (a face barrel 16 % wider than the
# lower trunk, like ref_19), big green eyes in dark-bark sockets under flat mossy brows, a wide grin with 2 square
# wooden teeth on a light carved face panel, a canopy of 5 overlapping rounded leaf blocks with blossoms, bark of
# vertical 1x2 plates, moss pads on the shoulders, a red mushroom shelf on one hip, stubby root legs and short arms
# ending in 3 chunky twig fingers.
# Own moves: idle = creaks and sways like a tree in the wind (arms swing like branches), strokes its chin, a gust
# rustles the canopy; walk = slow lumbering stride, arms swinging low; roar = TIMBER ROAR (leans back, arms spread like
# branches, canopy flares, mouth wide); signature = BRANCH LASH (winds up, whips the right arm forward and the arm GROWS
# out on a vine, grabs, yanks back, thumps its chest).
import math
from mathutils import Vector

DISPLAY = "Treant"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 10.0

BARK = (128, 88, 54)
FACE = (206, 162, 106)
GROOVE = (78, 52, 32)
ROOT = (109, 75, 46)           # BARK x0.85: root feet
LEAF = (92, 186, 74)
LEAF_L = (156, 222, 96)
BLOSSOM = (255, 172, 208)
POLLEN = (255, 226, 120)
SHROOM = (226, 70, 60)
SPOT = (255, 240, 230)
IRIS = (120, 210, 80)
MOUTH = (44, 28, 22)
TOOTH = (244, 226, 184)
VINE = (118, 160, 64)

S = (0.58, -0.02, 1.16)      # shoulder
E = (0.66, -0.06, 0.86)      # elbow
W = (0.69, -0.12, 0.60)      # wrist
LEG = ((0.22, 0.02, 0.72), (0.24, -0.08, 0.40), (0.24, 0.02, 0.12))
VINE_LEN = 0.30
TH = 0.60                    # plate-grid torso height (finer grid than the 0.76 trunk)
HEAD_C = Vector((0, -0.01, 1.56))
HEAD_H = Vector((0.50, 0.40, 0.34))          # the face barrel: W 1.00, H 0.68


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def arm_dir(s):
    return (X(E, s) - X(S, s)).normalized()


def frame(u, n):
    """rotation: local x = u, local z = n (surface normal), local y = z x x"""
    from mathutils import Matrix
    z = Vector(n).normalized()
    x = Vector(u)
    x = (x - z * x.dot(z)).normalized()
    return Matrix((x, z.cross(x), z)).transposed()


def flower(B, c, n, petal, mid, bone, size=0.042):
    """a "+" blossom half-buried in a canopy face (normal n): 4 rounded petals around a pollen centre"""
    c, n = Vector(c), Vector(n).normalized()
    R = frame((0, 0, 1) if abs(n.z) < 0.7 else (1, 0, 0), n)
    ux, vy = R.col[0], R.col[1]
    for d in (ux, -ux, vy, -vy):
        B.add(c + d * size * 1.15, (size, size, 0.03), petal, bone, R=R, studs=[], role="limb", rnd=0.4)
    B.add(c + n * 0.016, (0.034, 0.034, 0.025), mid, bone, R=R, studs=[], role="limb", rnd=0.3)


def model(k):
    """STYLE_BIBLE Treant: face barrel on the trunk, a rounded dome crown 1.3 x trunk W, stubby root legs, arms to the
    knee. Gate round 1 fixes: dome canopy, flush face panel, bark twig fingers, 2-tone root toes, bark cracks on the
    trunk front, mushroom shelf on the back hip."""
    import blockkit as bk
    B = bk.Blocks(k, seed=61, tier=1, th=TH)
    D = 0.64                                    # fill .70 (bible: bark fill .70)
    BARKMIX = (0.0, 1.0, 0.0)                   # bark = vertical 1x2 plates only
    LEAFMIX = (0.85, 0.15, 0.0)                 # leaves = mostly separate 1x1 plates (no letter clusters)
    # ---- trunk: pelvis < lower trunk < face barrel (each step >= 15 %), overlaps ~40 %
    B.add((0, 0.02, 0.86), (0.30, 0.26, 0.16), BARK, "Spine", studs=[], role="mass")          # hidden pelvis
    B.add((0, 0.02, 1.10), (0.43, 0.35, 0.38), BARK, "Chest", bot=(0.92, 0.94), density=D, pmix=BARKMIX,
          studs=["+x", "-x", "+y"])
    head = B.add(HEAD_C, HEAD_H, BARK, "Head", top=(0.95, 0.95), density=D, pmix=BARKMIX)
    hb = HEAD_C.z - HEAD_H.z
    fy = HEAD_C.y - HEAD_H.y
    # 3 parallel vertical bark cracks on the trunk front, flush on the tapered face (LESSONS 2)
    nf = Vector((0, -1, -0.35 * 0.06 / 0.76)).normalized()
    for x, L in ((-0.20, 0.30), (0.02, 0.22), (0.22, 0.26)):
        P = []
        for z in (0.80, 0.80 + L):
            t = (z - 0.72) / 0.76
            P.append(Vector((x, 0.02 - 0.35 * (0.94 + 0.06 * t), z)) + nf * 0.004)
        B.bar(P[0], P[1], nf, 0.055, 0.006, GROOVE, "Chest", studs=[], bevel=0.004)
    # ---- face: light carved panel (0.012 proud), dark-bark eye sockets, big green eyes, mossy brows, knot nose, grin
    panel = B.add((0, fy + 0.018, hb + 0.38), (0.42, 0.03, 0.25), FACE, "Head", bot=(0.86, 1), studs=[], role="limb")
    for s in (1, -1):
        B.add((s * 0.235, fy - 0.010, hb + 0.41), (0.165, 0.006, 0.165), GROOVE, "Head", studs=[], bevel=0.02)
    B.face_eyes(panel, "bold", IRIS, base=FACE, brow=LEAF, scale=1.16, z=0.62, x=0.30,
                brow_spec=(0.30, 0.07, 6), pupil_size=(0.09, 0.10), hl_size=(0.07, 0.0), look=(0, -0.7))
    B.add((0, fy - 0.04, hb + 0.27), (0.065, 0.04, 0.05), BARK, "Head", studs=[], role="limb")       # knot nose
    B.add((-0.025, fy - 0.082, hb + 0.29), (0.012, 0.004, 0.012), FACE, "Head", studs=[], bevel=0.003)
    # grin: dark slot with tipped-up corners + 2 square wooden teeth hanging from the upper lip
    B.add((0, fy - 0.010, hb + 0.165), (0.21, 0.006, 0.045), MOUTH, "Head", studs=[], bevel=0.01)
    for s in (1, -1):
        B.add((s * 0.235, fy - 0.010, hb + 0.19), (0.05, 0.006, 0.03), MOUTH, "Head", rot=(0, -s * 30, 0), studs=[],
              bevel=0.008)
        B.add((s * 0.055, fy - 0.018, hb + 0.185), (0.045, 0.006, 0.036), TOOTH, "Head", studs=[], bevel=0.008)
    B.add((0, fy + 0.09, hb + 0.13), (0.22, 0.10, 0.05), MOUTH, "Head", studs=[], role="detail")       # mouth inside
    # chin (Jaw): the lower lip of the face panel, drops to open the mouth
    B.add((0, fy + 0.018, hb + 0.075), (0.30, 0.03, 0.055), FACE, "Jaw", bot=(0.85, 1), studs=[], role="limb")
    # ---- canopy (Crown): a round dome of 11 rounded near-cube leaf puffs (low ring dark green, top light green)
    ht = hb + 2 * HEAD_H.z
    puffs = [((0, 0.06, ht + 0.30), 0.34, LEAF),                                            # core
             ((-0.50, 0.08, ht + 0.10), 0.24, LEAF), ((0.50, 0.02, ht + 0.10), 0.24, LEAF),  # low ring
             ((0.02, 0.44, ht + 0.10), 0.24, LEAF), ((-0.27, -0.28, ht + 0.20), 0.20, LEAF),
             ((0.28, -0.26, ht + 0.22), 0.21, LEAF),
             ((-0.34, 0.24, ht + 0.42), 0.22, LEAF_L), ((0.34, 0.24, ht + 0.44), 0.22, LEAF_L),  # middle
             ((0.00, -0.22, ht + 0.50), 0.20, LEAF_L),
             ((-0.08, 0.04, ht + 0.66), 0.24, LEAF_L), ((0.22, 0.18, ht + 0.62), 0.18, LEAF_L)]  # top
    for c, r, col in puffs:
        B.add(c, (r, r * 0.95, r * 0.92), col, "Crown", rnd=0.45, role="mass", density=0.55, pmix=LEAFMIX)
    for i, n, du, dv in ((4, (0, -1, 0), 0.0, 0.0), (5, (0, -1, 0), 0.02, 0.0), (1, (-1, 0, 0), 0.0, 0.02),
                         (2, (1, 0, 0), 0.0, 0.0), (8, (0, -1, 0), -0.04, 0.02), (9, (0, 0, 1), 0.0, 0.0),
                         (3, (0, 1, 0), 0.06, 0.0), (6, (-1, 0, 0), 0.0, 0.0), (7, (0, 1, 0), 0.0, 0.0)):
        c, r, _ = puffs[i]
        h = Vector((r, r * 0.95, r * 0.92))
        nn = Vector(n)
        p = Vector(c) + Vector((nn.x * h.x, nn.y * h.y, nn.z * h.z))
        p += Vector((du, 0, dv)) if abs(nn.y) > 0.5 else Vector((0, du, dv)) if abs(nn.x) > 0.5 else Vector((du, dv, 0))
        flower(B, p, nn, BLOSSOM, POLLEN, "Crown")
    # ---- shoulders: rounded bark knots with moss pads; a red mushroom shelf on the back-left hip
    for s in (1, -1):
        B.add((s * 0.50, -0.02, 1.19), (0.16, 0.17, 0.15), BARK, "Chest", studs=[], role="limb", rnd=0.42)
        B.add((s * 0.53, -0.02, 1.32), (0.13, 0.14, 0.05), LEAF, "Chest", studs=[], role="limb", rnd=0.45)
    for c, h, dots in (((0.24, 0.42, 0.98), (0.15, 0.08, 0.035), ((0.15, 0.45), (0.25, 0.47), (0.34, 0.43))),
                       ((0.20, 0.40, 0.86), (0.11, 0.06, 0.03), ((0.13, 0.42), (0.21, 0.43), (0.28, 0.41)))):
        B.add(c, h, SHROOM, "Chest", top=(0.85, 0.85), studs=[], role="limb")
        for x, y in dots:
            B.add((x, y, c[2] + h[2] + 0.004), (0.025, 0.025, 0.008), SPOT, "Chest", studs=[], role="detail")
    # ---- arms: upper arm, hidden vine (telescopes out in the lash), forearm, hand with 3 chunky bark twig fingers
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        d = arm_dir(s)
        B.seg(Sv, Ev, 0.12, 0.13, BARK, "Arm_" + side, ext=0.06, density=D, role="limb", pmix=BARKMIX)
        B.seg(Ev - d * VINE_LEN, Ev, 0.07, 0.07, VINE, "Vine_" + side, studs=[], role="limb")
        B.seg(Ev, Wv, 0.11, 0.12, BARK, "Fore_" + side, ext=0.05, density=D, role="limb", pmix=BARKMIX)
        hc = Wv + Vector((0, -0.02, -0.07))
        B.add(hc, (0.13, 0.12, 0.08), BARK, "Hand_" + side, studs=[], role="limb")
        for dx, dz in ((-0.09, 0.0), (0.0, 0.01), (0.09, 0.0)):
            B.spike(hc + Vector((dx, -0.05, -0.05 + dz)), (s * 0.05 * (dx != 0), -0.45, -1), 0.13, 0.055, BARK,
                    "Hand_" + side, top=(0.6, 0.6))
        B.spike(hc + Vector((-s * 0.11, -0.04, 0.0)), (-s * 0.7, -0.4, -0.5), 0.11, 0.05, BARK, "Hand_" + side,
                top=(0.6, 0.6))
    # ---- stubby root legs: thigh, shin, wide root foot with 4 two-tone root toes (dark tip on the last 30 %)
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A = (X(p, s) for p in LEG)
        B.seg(H, K, 0.18, 0.19, BARK, "Leg_" + side, ext=0.08, density=0.9, role="limb", pmix=BARKMIX)
        B.seg(K, A, 0.165, 0.175, BARK, "Shin_" + side, ext=0.06, density=0.9, role="limb", bot=(1.12, 1.10),
              pmix=BARKMIX)
        B.add(A + Vector((0, -0.03, -0.06)), (0.21, 0.21, 0.06), ROOT, "Foot_" + side, studs=[], role="limb")
        for dx, dy in ((-0.13, -0.30), (0.0, -0.33), (0.13, -0.30), (s * 0.30, -0.12)):     # short: no toe dip in the swing
            p0 = A + Vector((dx * 0.6, -0.18 if dx != s * 0.30 else -0.04, -0.06))
            p1 = A + Vector((dx, dy, -0.08))
            pm = p0.lerp(p1, 0.70)
            B.seg(p0, pm, 0.05, 0.04, ROOT, "Foot_" + side, side=(0, 0, 1), studs=[], top=(0.80, 0.85), role="limb")
            B.seg(pm, p1, 0.04, 0.034, GROOVE, "Foot_" + side, side=(0, 0, 1), ext=0.015, studs=[], top=(0.55, 0.6),
                  role="limb")
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.02, 0.80), "Root", tail=(0, 0, 0.4))
    k.joint("Chest", (0, 0.02, 1.00), "Spine", tail=(0, 0, 0.5))
    k.joint("Head", (0, 0.0, 1.30), "Chest", tail=(0, 0, 0.4))               # waist pivot under the face barrel
    k.joint("Jaw", (0, -0.36, 1.30), "Head", tail=(0, -0.2, 0))
    k.joint("Crown", (0, 0.02, 1.92), "Head", tail=(0, 0, 0.4))
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        k.joint("Arm_" + side, Sv, "Chest")
        k.joint("Vine_" + side, Ev - arm_dir(s) * 0.02, "Arm_" + side, tail=tuple(arm_dir(s) * 0.2))
        k.joint("Fore_" + side, Ev, "Vine_" + side)
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


def jaw(k, f, a):
    """a = 0 closed .. 1 wide open: the jaw plate drops and tips its lower edge forward"""
    k.key("Jaw", f, rot=(-10 * a, 0, 0), loc=(0, -0.02 * a, -0.10 * a))


def arm(k, f, side, pitch=0.0, yaw=0.0, roll=0.0, elbow=0.0, hand=0.0, grow=0.0):
    """pitch - raises the arm forward, roll (outward +) lifts it to the side, elbow + bends the forearm forward/up,
    hand + curls the twig fingers, grow = how far the vine has telescoped out (0..1)."""
    s = 1 if side == "L" else -1
    k.key("Arm_" + side, f, rot=(pitch, s * yaw, -s * roll))
    k.key("Vine_" + side, f, rot=(0, 0, 0), loc=tuple(arm_dir(s) * VINE_LEN * grow))
    k.key("Fore_" + side, f, rot=(-elbow, 0, 0))
    k.key("Hand_" + side, f, rot=(-hand, 0, 0))


def idle(k):
    """ancient and slow: creaks and sways like a tree in the wind (arms swing after the body like heavy branches),
    lifts its left hand to stroke its mossy beard, then a gust makes the canopy rustle hard."""
    n = 160
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        sw = pk.wave(f, n, 0, 2)
        gust = math.sin(math.pi * (f - 118) / 34) if 118 <= f <= 152 else 0.0
        k.key("Spine", f, rot=(0, 0, 1.5 * sw), loc=(0, 0, 0.008 * pk.wave(f, n, 0.1, 4)))
        k.key("Chest", f, rot=(-1.2 * pk.wave(f, n, 0.1, 4) - 2 * gust, 1.5 * pk.wave(f, n, 0.2, 2), 1.8 * sw))
        k.key("Crown", f, rot=(2 * pk.wave(f, n, 0.3, 2) - 6 * gust + 2.5 * gust * math.sin(2 * math.pi * f / 8), 0,
                               2 * pk.wave(f, n, 0.15, 2) + 3 * gust * math.sin(2 * math.pi * f / 10)))
        jaw(k, f, 0)
        r = 2.5 * pk.wave(f, n, 0.12, 2)
        arm(k, f, "R", pitch=-3 * pk.wave(f, n, 0.2, 2), roll=4 - r, elbow=8, hand=10)
    # left arm: hangs, then strokes the beard twice
    for f, p, y, ro, el, hd in ((0, 0, 0, 4, 8, 10), (56, 0, 0, 4, 8, 10), (72, -40, 20, 0, 92, 30), (78, -38, 26, 0, 96, 40),
                                (84, -42, 18, 0, 90, 26), (90, -38, 26, 0, 96, 40), (96, -42, 18, 0, 90, 26),
                                (112, 0, 0, 4, 8, 10), (160, 0, 0, 4, 8, 10)):
        arm(k, f, "L", pitch=p, yaw=y, roll=ro, elbow=el, hand=hd)
    for f, hp, hy in ((0, 0, 0), (60, 0, 0), (72, 8, -10), (100, 8, -10), (114, 0, 0), (126, -6, 6), (148, -6, 6),
                      (160, 0, 0)):
        k.key("Head", f, rot=(hp, hy, 0))
    cm.plant(k, n, legs=LEGS2)
    k.finish()
    k.meta["planted"] = LEGS2


def walk(k):
    n = 44

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(2, 4 * pk.wave(f, n, 0.0), 4.5 * pk.wave(f, n, 0.0)), loc=(0, 0, -0.04 * b))
        k.key("Chest", f, rot=(4 + 1.5 * pk.wave(f, n, 0.1, 2), -6 * pk.wave(f, n, 0.0), -2.5 * pk.wave(f, n, 0.05)))
        k.key("Head", f, rot=(-4 - 1.5 * pk.wave(f, n, 0.2, 2), 3 * pk.wave(f, n, 0.0), 0))
        jaw(k, f, 0)
        k.key("Crown", f, rot=(-2 * pk.wave(f, n, 0.3, 2), 0, -3 * pk.wave(f, n, 0.15)))
        for side, ph in (("L", 0.5), ("R", 0.0)):
            arm(k, f, side, pitch=18 * pk.wave(f, n, ph + 0.05), roll=5, elbow=14 + 8 * pk.wave(f, n, ph + 0.15),
                hand=12)
    return cm.biped_walk(k, n, 0.14, 0.09, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.62)


def roar(k):
    """TIMBER ROAR: sinks, then leans back with both arms flung wide and up like branches, head back, mouth wide,
    canopy flaring back; holds with a creaking tremble; slams forward to finish."""
    n = 72
    k.new_action("roar", n, False)
    for f, ch, hd, jw, ro, p, el, cr, z in ((0, 0, 0, 0, 4, 0, 8, 0, 0), (12, 8, 6, 2, 8, 6, 30, 4, -0.06),
                                            (22, -10, -14, 34, 62, -30, 12, -12, 0.0), (46, -11, -15, 36, 64, -32, 10, -14, 0.0),
                                            (54, 10, 6, 10, 24, -10, 40, 8, -0.05), (62, 2, 0, 0, 6, 0, 10, 0, 0),
                                            (72, 0, 0, 0, 4, 0, 8, 0, 0)):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        jaw(k, f, jw / 36)
        k.key("Crown", f, rot=(cr, 0, 0))
        for side in ("L", "R"):
            arm(k, f, side, pitch=p, roll=ro, elbow=el, hand=-10 if 20 <= f <= 48 else 10)
    for f in range(24, 46, 3):
        k.key("Chest", f, rot=(-10.5 + (0.8 if (f // 3) % 2 else -0.8), 0, 0))
    cm.plant(k, n, legs=LEGS2)
    k.finish(loop=False)


def lash(k):
    """SIGNATURE - BRANCH LASH: twists back winding the right arm up behind, whips it forward and the arm GROWS out on a
    vine (telescopes ~0.6), fingers snap shut on the grab, holds, yanks back hard leaning away, the vine retracts,
    then two thumps of the fist on its chest."""
    n = 100
    k.new_action("act_branchlash", n, False)
    # body
    for f, sp_yaw, ch_p, ch_y, hd, z in ((0, 0, 0, 0, 0, 0), (14, -6, -4, -22, -4, -0.04), (24, 4, 8, 18, 6, -0.06),
                                         (30, 6, 10, 20, 6, -0.07), (44, 6, 10, 20, 6, -0.07), (50, -4, -10, -10, -8, -0.03),
                                         (62, -2, -6, -4, -4, -0.02), (72, 0, 2, 0, 0, 0), (78, 0, 4, 0, 4, -0.02),
                                         (82, 0, 1, 0, 0, 0), (86, 0, 4, 0, 4, -0.02), (90, 0, 1, 0, 0, 0), (100, 0, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(0, sp_yaw, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch_p, ch_y, 0))
        k.key("Head", f, rot=(hd, -ch_y * 0.4, 0))
        jaw(k, f, 0.5 if 24 <= f <= 32 else 0)
        k.key("Crown", f, rot=(-ch_p * 0.6, 0, 0))
    # right arm: wind-up, lash + grow, grab, yank, retract, chest thumps
    for f, p, y, ro, el, hd, g in ((0, 0, 0, 4, 8, 10, 0), (14, -120, -20, 30, 60, -10, 0), (22, -96, 0, 10, 10, -20, 0.2),
                                   (26, -88, 0, 6, 0, -25, 0.85), (29, -86, 0, 6, 0, -25, 1.0), (32, -86, 0, 6, 0, 60, 1.0),
                                   (44, -84, 0, 6, 0, 60, 1.0), (50, -60, 10, 8, 30, 60, 0.5), (58, -40, 14, 6, 70, 55, 0.0),
                                   (66, -30, 16, 4, 90, 40, 0.0), (72, -46, 34, 0, 116, 60, 0), (76, -40, 30, 0, 110, 60, 0),
                                   (78, -46, 36, 0, 118, 60, 0), (82, -40, 30, 0, 110, 60, 0), (86, -46, 36, 0, 118, 60, 0),
                                   (90, -36, 28, 0, 104, 60, 0), (100, 0, 0, 4, 8, 10, 0)):
        arm(k, f, "R", pitch=p, yaw=y, roll=ro, elbow=el, hand=hd, grow=g)
    for f, p, ro, el in ((0, 0, 4, 8), (14, 20, 14, 30), (24, -20, 8, 50), (44, -20, 8, 50), (50, 10, 12, 30), (64, 0, 6, 12),
                         (100, 0, 4, 8)):
        arm(k, f, "L", pitch=p, roll=ro, elbow=el, hand=10)
    cm.plant(k, n, legs=LEGS2)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    lash(k)
    return stride


def check_pairs():
    P = [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R")]
    for s in ("L", "R"):
        for a in ("Fore_" + s, "Hand_" + s):
            for b in ("Spine", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Head", "Jaw"):
                P.append((a, b))
        P.append(("Hand_" + s, "Chest"))
        P.append(("Fore_" + s, "Chest"))
        P.append(("Vine_" + s, "Chest"))
        P.append(("Hand_" + s, "Crown"))
    return P


def joints():
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        Ev, Wv = X(E, s), X(W, s)
        out.append((Wv, Wv, 0.10, "Hand_" + side))
        Sv = X(S, s)                      # shoulder: the hidden vine's inner end sits inside the upper arm there
        out.append((Sv, Sv, 0.32, "Vine_" + side))
    return out
