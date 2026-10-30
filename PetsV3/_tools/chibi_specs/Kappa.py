# Kappa (Tide egg #1, T2 Water, biped lovely-mischief): a cheeky river kappa in the Steal-an-Egg block style, rebuilt
# to STYLE_BIBLE.md (2026-10-08 pro pass): a pear shape - a big head (HW 1.10 TW, ~40 % of H) with a yellow duck beak
# and a grin line, lovely navy eyes under asymmetric brows (left flat, right raised for mischief), a water dish ringed
# by 7 dark hair tufts on the head, a round belly with a plated cream plastron over a chunky navy mawashi, a scute shell
# backpack, short arms with dark claws and webbed 3-toe feet.
# Own moves: idle = frog crouch, reaches up to steady the dish and levels its head, a deep frog-squat bounce;
# walk = quick waddle with the head kept level; roar = KAPPA SCREECH (claws spread wide, beak gaping, lunges low);
# signature = SUMO SHIKO (deep squat, raises each leg high to the side and STOMPS, then three palm thrusts).
import math
from mathutils import Vector

DISPLAY = "Kappa"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 7.0

SKIN = (66, 196, 166)
CREAM = (236, 232, 176)
TEAL_D = (28, 96, 84)
BEAK = (255, 190, 56)
BEAK_D = (214, 140, 30)
SHELL = (88, 132, 74)
SHELL_L = (101, 152, 85)       # SHELL x1.15 V: raised scutes
CREAM_D = (217, 213, 162)      # CREAM x0.92: flush plastron zone
DISH = (214, 240, 255)
WATER = (96, 190, 244)
BELT = (64, 72, 170)
BELT_L = (236, 232, 176)
IRIS = (40, 64, 130)
MOUTH = (120, 34, 44)

S = (0.40, 0.0, 0.94)        # shoulder
E = (0.47, -0.03, 0.73)      # elbow
W = (0.49, -0.07, 0.55)      # wrist
LEG = ((0.20, 0.02, 0.44), (0.22, -0.07, 0.27), (0.22, 0.0, 0.10))
HEAD_C = Vector((0, -0.02, 1.49))
HEAD_H = Vector((0.43, 0.35, 0.34))           # HW 0.86 = 1.13 TW (belly 0.76), HH 0.68


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def frame(u, n):
    from mathutils import Matrix
    z = Vector(n).normalized()
    x = Vector(u).normalized()
    return Matrix((x, z.cross(x), z)).transposed()


def model(k):
    """STYLE_BIBLE Kappa: pear shape, big beaked head with a dish + hair ring, round belly, mawashi, shell backpack."""
    import blockkit as bk
    B = bk.Blocks(k, seed=71, tier=2)
    D = 0.62
    # ---- round belly (wide at the bottom = pear) over the pelvis; chunky navy mawashi wrapping the hips
    B.add((0, 0.02, 0.48), (0.32, 0.26, 0.16), SKIN, "Spine", studs=[], role="mass")
    chest = B.add((0, 0.0, 0.78), (0.38, 0.29, 0.24), SKIN, "Chest", top=(0.80, 1.0), density=D)
    B.add((0, 0.02, 0.46), (0.35, 0.29, 0.10), BELT, "Spine", density=0.5, role="mass")
    B.add((0, -0.29, 0.40), (0.11, 0.035, 0.12), BELT, "Spine", studs=[], role="limb")            # front knot
    for x in (-0.07, 0.0, 0.07):
        B.add((x, -0.33, 0.30), (0.022, 0.014, 0.075), BELT_L, "Spine", studs=[], role="detail")   # sagari strings
    # plated cream plastron on the belly front
    B.add((0, -0.294, 0.77), (0.25, 0.004, 0.22), CREAM_D, "Chest", studs=[], bevel=0.01)
    R0 = frame((1, 0, 0), (0, -1, 0))
    for i in range(2):
        for j in range(3):
            p = Vector(((i - 0.5) * 0.205, -0.30, 0.66 + j * 0.13))
            w = 0.092 - 0.008 * j
            B.add(p, (w, 0.055, 0.025), CREAM, "Chest", R=R0, top=(0.86, 0.80), studs=[], role="limb", rnd=0.25)
    # ---- shell backpack (gate round 2): 7 big rounded scutes straight on the dark rim, ~0.03 dark gaps between
    # them, the centre column 0.04 prouder than the sides -> a stepped dome in the side view, not a slab
    B.add((0, 0.34, 0.78), (0.32, 0.08, 0.27), TEAL_D, "Chest", studs=[], role="limb", rnd=0.35)
    for z in (-0.18, 0.0, 0.18):
        B.add((0, 0.42 + 0.05, 0.78 + z), (0.085, 0.07, 0.075), SHELL_L, "Chest", studs=[], role="limb", rnd=0.35)
    for x in (0.20, -0.20):
        for z in (0.10, -0.10):
            B.add((x, 0.42 + 0.03, 0.78 + z), (0.085, 0.05, 0.085), SHELL, "Chest", studs=[], role="limb", rnd=0.35)
    # ---- neck (hidden bridge) + big head
    B.add((0, 0.0, 1.08), (0.26, 0.22, 0.10), SKIN, "Neck", studs=[], role="limb")
    head = B.add(HEAD_C, HEAD_H, SKIN, "Head", top=(0.94, 0.94), density=0.45, studs=["+x", "-x", "+y", "+z"],
                 pmix=(0.75, 0.25, 0.0))
    hb = HEAD_C.z - HEAD_H.z
    fy = HEAD_C.y - HEAD_H.y
    ht = hb + 2 * HEAD_H.z
    # duck beak: upper (Head) + lower (Jaw), a grin line with one corner tipped higher (mischief)
    B.add((0, fy - 0.075, hb + 0.165), (0.215, 0.12, 0.062), BEAK, "Head", top=(0.86, 0.80), studs=[], role="limb")
    for s in (1, -1):
        B.add((s * 0.07, fy - 0.17, hb + 0.205), (0.022, 0.012, 0.012), BEAK_D, "Head", studs=[], role="detail")
    B.add((0, fy - 0.03, hb + 0.10), (0.18, 0.10, 0.006), MOUTH, "Head", studs=[], bevel=0.003)          # mouth roof
    B.add((0, fy - 0.065, hb + 0.068), (0.195, 0.11, 0.036), BEAK, "Jaw", bot=(0.85, 0.85), studs=[], role="limb")
    B.add((0, fy - 0.04, hb + 0.104), (0.16, 0.09, 0.004), MOUTH, "Jaw", studs=[], bevel=0.002)
    gy = fy - 0.177
    B.add((0, gy, hb + 0.104), (0.11, 0.008, 0.016), TEAL_D, "Head", studs=[], bevel=0.004)
    for s, ang, dz in ((1, 22, 0.022), (-1, 34, 0.032)):
        B.add((s * 0.145, gy + 0.014, hb + 0.104 + dz), (0.05, 0.008, 0.016), TEAL_D, "Head", rot=(0, -s * ang, 0),
              studs=[], bevel=0.004)
    # lovely eyes + asymmetric brows (left flat, right raised 12 deg)
    E_ = B.face_eyes(head, "lovely", IRIS, base=SKIN, z=0.62, pupil_size=(0.10, 0.12), hl_size=(0.08, 0.0), look=(0, -0.6))
    HW = 2 * HEAD_H.x
    for s, side, ang, dz in ((1, "L", 0, 0.0), (-1, "R", 12, 0.03)):
        c = E_[side]
        B.add((c.x, fy - 0.012, hb + E_["top"] + HEAD_H.z + 0.035 * HW + dz), (0.13 * HW, 0.012, 0.026 * HW), TEAL_D,
              "Head", rot=(0, s * ang, 0), studs=[], role="detail", bevel=0.008)
    # ---- the dish: rim frame + inset water, ringed by 7 dark hair tufts laid outwards
    dz0 = ht + 0.012
    B.add((0, -0.02, dz0 - 0.01), (0.24, 0.24, 0.02), DISH, "Head", studs=[], role="limb")
    for (x, y, hx, hy) in ((0, -0.24, 0.25, 0.035), (0, 0.20, 0.25, 0.035), (0.215, -0.02, 0.035, 0.25),
                           (-0.215, -0.02, 0.035, 0.25)):
        B.add((x, y, dz0 + 0.025), (hx, hy, 0.03), DISH, "Head", studs=[], role="limb", rnd=0.3)
    B.add((0, -0.02, dz0 + 0.018), (0.18, 0.185, 0.008), WATER, "Head", studs=[], role="detail")
    for adeg in (90, 50, 130, 10, 170, 330, 210):                # 7 locks; a wide 120 deg gap over the forehead
        a = math.radians(adeg)
        d = Vector((math.cos(a), math.sin(a), 0))
        base = Vector((d.x * 0.33, -0.02 + d.y * 0.28, ht - 0.01))
        out = (d * 1.0 + Vector((0, 0, -0.55))).normalized()       # locks droop over the head edge (bowl cut)
        L = 0.22 if d.y > -0.3 else 0.18
        B.seg(base, base + out * L, 0.10, 0.05, TEAL_D, "Head", side=(-d.y, d.x, 0), ext=0.05, top=(0.30, 0.55),
              studs=[], role="limb")
    # ---- short arms: hands reach the hips, 3 dark claws
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        B.add(Sv + Vector((-s * 0.02, 0, 0.0)), (0.11, 0.11, 0.10), SKIN, "Arm_" + side, studs=[], role="limb",
              rnd=0.35)
        B.seg(Sv, Ev, 0.085, 0.09, SKIN, "Arm_" + side, ext=0.05, density=D, role="limb")
        B.seg(Ev, Wv, 0.08, 0.085, SKIN, "Fore_" + side, ext=0.04, density=D, role="limb")
        hc = Wv + Vector((0, -0.02, -0.06))
        B.add(hc, (0.09, 0.09, 0.06), SKIN, "Hand_" + side, studs=[], role="limb")
        roots, dirs = [], []
        for dx, a in ((-0.065, -15), (0.0, 0), (0.065, 15)):
            d = Vector((math.sin(math.radians(a)), -0.40, -math.cos(math.radians(a)))).normalized()
            r0 = hc + Vector((dx, -0.03, -0.04))
            B.seg(r0, r0 + d * 0.08, 0.03, 0.035, SKIN, "Hand_" + side, side=(1, 0, 0), ext=0.02, studs=[],
                  role="limb")
            B.spike(r0 + d * 0.07, d, 0.06, 0.032, TEAL_D, "Hand_" + side, top=(0.3, 0.3))
            roots.append(r0)
            dirs.append(d)
        for i in range(2):
            dm = (dirs[i] + dirs[i + 1]).normalized()
            q0 = (roots[i] + roots[i + 1]) / 2 + Vector((0, -0.012, 0))
            B.seg(q0, q0 + dm * 0.06, 0.022, 0.012, CREAM, "Hand_" + side, side=(1, 0, 0), studs=[], role="detail",
                  top=(1.3, 1.0))
    # ---- short thick legs, webbed 3-toe feet (cream webs, dark claws)
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A = (X(p, s) for p in LEG)
        B.seg(H, K, 0.14, 0.155, SKIN, "Leg_" + side, ext=0.07, density=D, role="limb")
        B.seg(K, A, 0.125, 0.135, SKIN, "Shin_" + side, ext=0.05, density=D, role="limb")
        B.add(A + Vector((0, -0.08, -0.075)), (0.17, 0.18, 0.025), SKIN, "Foot_" + side, top=(1.0, 0.9), studs=[],
              role="limb")
        toes = []
        for dx, sp in ((-0.11, -14), (0.0, 0), (0.11, 14)):
            r = math.radians(sp)
            d = Vector((math.copysign(math.sin(abs(r)), dx) if dx else 0.0, -math.cos(r), 0))
            p0 = A + Vector((dx * 0.5, 0.02, -0.03))
            B.seg(p0, p0 + d * 0.24, 0.035, 0.03, SKIN, "Foot_" + side, side=(0, 0, 1), studs=[], role="limb")
            B.add(p0 + d * 0.26 + Vector((0, 0, -0.005)), (0.028, 0.03, 0.022), TEAL_D, "Foot_" + side, studs=[],
                  role="detail", bevel=0.008)
            toes.append((p0, d))
        for i in range(2):
            (pa, da), (pb, db) = toes[i], toes[i + 1]
            dm = (da + db).normalized()
            q0 = Vector(((pa.x + pb.x) / 2, (pa.y + pb.y) / 2, 0.054)) + dm * 0.03
            B.seg(q0, q0 + dm * 0.17, 0.004, 0.022, CREAM, "Foot_" + side, side=(0, 0, 1), studs=[], role="detail",
                  top=(1.0, 1.9))
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.02, 0.50), "Root", tail=(0, 0, 0.3))
    k.joint("Chest", (0, 0.0, 0.62), "Spine", tail=(0, 0, 0.4))
    k.joint("Neck", (0, 0.24, 1.06), "Chest", tail=(0, 0, 0.12))               # back pivots: nose-up tilts keep
    k.joint("Head", (0, 0.30, 1.15), "Neck", tail=(0, 0, 0.3))                 # the skull's back edge off the shell
    k.joint("Jaw", (0, -0.31, 1.22), "Head", tail=(0, -0.2, 0))
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        k.joint("Arm_" + side, Sv, "Chest")
        k.joint("Fore_" + side, Ev, "Arm_" + side)
        k.joint("Hand_" + side, Wv, "Fore_" + side, tail=(0, -0.05, -0.2))
        H, K, A = (X(p, s) for p in LEG)
        k.joint("Leg_" + side, H, "Spine")
        k.joint("Shin_" + side, K, "Leg_" + side)
        k.joint("Foot_" + side, A, "Shin_" + side, tail=(0, -0.2, 0))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(s * 0.45, -0.9, 0))


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS2 = ["Leg_L", "Leg_R"]


def arm(k, f, side, pitch=0.0, yaw=0.0, roll=0.0, elbow=0.0, hand=0.0):
    """pitch - raises the arm forward, roll + lifts it out to the side, elbow + bends the forearm forward/up,
    hand + curls the fingers"""
    s = 1 if side == "L" else -1
    k.key("Arm_" + side, f, rot=(pitch, s * yaw, -s * roll))
    k.key("Fore_" + side, f, rot=(-elbow, 0, 0))
    k.key("Hand_" + side, f, rot=(-hand, 0, 0))


def idle(k):
    """frog crouch, breathing through the beak; reaches up with the right hand to steady the dish while leveling its
    head very carefully, wipes the hand on its belt, then one deep frog-squat bounce."""
    n = 150
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 5)
        sq = -0.07 * math.sin(math.pi * (f - 96) / 22) if 96 <= f <= 118 else 0.0
        k.key("Spine", f, rot=(4, 0, 0), loc=(0, 0, 0.008 * b + sq))
        k.key("Chest", f, rot=(6 - 1.5 * b, 0, 0))
        k.key("Jaw", f, rot=(3 + 2 * max(0.0, b), 0, 0))
        arm(k, f, "L", pitch=-6 + 2 * b, roll=8, elbow=24 + 30 * max(0.0, -sq / 0.07), hand=10)
    for f, nk, hd, hr in ((0, -4, -4, 0), (30, -4, -4, 0), (40, -4, -8, 4), (48, -4, -8, -3), (54, -4, -7, 2),
                          (62, -4, -6, 0), (72, -4, -4, 0), (150, -4, -4, 0)):
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, hr))
    for f, p, y, ro, el, hd in ((0, -6, 0, 8, 24, 10), (28, -6, 0, 8, 24, 10), (38, -128, -20, 34, 48, -10),
                                (44, -130, -16, 34, 50, 5), (50, -128, -22, 34, 48, -8), (56, -130, -16, 34, 50, 5),
                                (66, -20, 0, 6, 30, 10), (72, -4, -10, 4, 20, 20), (78, 2, -8, 4, 16, 20),
                                (86, -6, 0, 8, 24, 10), (150, -6, 0, 8, 24, 10)):
        arm(k, f, "R", pitch=p, yaw=y, roll=ro, elbow=el, hand=hd)
    cm.plant(k, n, legs=LEGS2)
    k.finish()
    k.meta["planted"] = LEGS2


def walk(k):
    n = 26

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(6, 5 * pk.wave(f, n, 0.0), 5 * pk.wave(f, n, 0.0)), loc=(0, 0, -0.02 * b))
        k.key("Chest", f, rot=(6, -6 * pk.wave(f, n, 0.0), -4 * pk.wave(f, n, 0.0)))
        k.key("Neck", f, rot=(-6, 0, 0))
        k.key("Head", f, rot=(-4, 0, 6 * pk.wave(f, n, 0.0)))           # keeps the dish level against the waddle
        k.key("Jaw", f, rot=(3, 0, 0))
        for side, ph in (("L", 0.5), ("R", 0.0)):
            arm(k, f, side, pitch=-6 + 24 * pk.wave(f, n, ph + 0.05), roll=10, elbow=30 + 10 * pk.wave(f, n, ph + 0.2),
                hand=10)
    return cm.biped_walk(k, n, 0.10, 0.07, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.58)


def roar(k):
    """KAPPA SCREECH: drops into a low crouch, then lunges its head forward with the beak gaping, arms flung wide with
    the claws spread, holds (beak quivering), snaps back up."""
    n = 64
    k.new_action("roar", n, False)
    for f, sp, z, ch, nk, hd, jw, ro, p, el, hn in ((0, 4, 0, 6, -4, -4, 3, 8, -6, 24, 10),
                                                    (10, 8, -0.055, 14, 6, 4, 3, 10, 0, 50, 20),
                                                    (18, 14, -0.08, 16, -20, -10, 38, 70, -40, 10, -30),
                                                    (44, 14, -0.08, 16, -20, -10, 36, 72, -42, 10, -30),
                                                    (52, 6, -0.02, 8, -6, -4, 8, 20, -10, 30, 10),
                                                    (64, 4, 0, 6, -4, -4, 3, 8, -6, 24, 10)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0), loc=(0, -0.05 * (18 <= f <= 44), 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        for side in ("L", "R"):
            arm(k, f, side, pitch=p, roll=ro, elbow=el, hand=hn)
    for f in range(20, 44, 2):
        k.key("Jaw", f, rot=(37 + (3 if (f // 2) % 2 else -3), 0, 0))
    cm.plant(k, n, legs=LEGS2)
    k.finish(loop=False)


def sumo(k):
    """SIGNATURE - SUMO SHIKO: sinks into a deep sumo squat with the hands on the thighs, swings the left leg high out to
    the side and STOMPS it down, then the right; finishes with three hard palm thrusts (tsuppari) and rises."""
    import bpy
    n = 124
    k.new_action("act_sumo", n, False)
    # body: (f, z, roll, chest_pitch, spine_pitch)
    for f, z, r, ch, sp in ((0, 0, 0, 6, 4), (12, -0.11, 0, 14, 10), (24, -0.11, 0, 14, 10), (34, -0.06, -14, 8, 6),
                            (44, -0.03, -18, 6, 4), (50, -0.12, -4, 16, 10), (52, -0.14, 0, 18, 12), (58, -0.11, 0, 14, 10),
                            (68, -0.06, 14, 8, 6), (78, -0.03, 18, 6, 4), (84, -0.12, 4, 16, 10), (86, -0.14, 0, 18, 12),
                            (92, -0.11, 0, 14, 10), (96, -0.1, 0, 8, 8), (99, -0.1, 0, 4, 8), (102, -0.1, 0, 8, 8),
                            (105, -0.1, 0, 4, 8), (108, -0.1, 0, 8, 8), (111, -0.1, 0, 4, 8), (118, -0.02, 0, 6, 4),
                            (124, 0, 0, 6, 4)):
        k.key("Spine", f, rot=(sp, 0, r), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, -r * 0.3))
        k.key("Neck", f, rot=(-8, 0, 0))
        k.key("Head", f, rot=(-6, 0, r * 0.5))
        k.key("Jaw", f, rot=(20 if f in (52, 86) else 3, 0, 0))
    # arms: hands on thighs, balance arm out during the leg raise, palm thrusts
    on_thigh = dict(pitch=-24, roll=12, elbow=40, hand=-10)
    for side, raise_f in (("L", (34, 44, 50)), ("R", (68, 78, 84))):
        other = "R" if side == "L" else "L"
        for f in (0,):
            arm(k, f, side, pitch=-6, roll=8, elbow=24, hand=10)
    keysL = {0: dict(pitch=-6, roll=8, elbow=24, hand=10), 12: on_thigh, 24: on_thigh,
             34: dict(pitch=-20, roll=70, elbow=10, hand=-20), 44: dict(pitch=-20, roll=74, elbow=10, hand=-20),
             50: on_thigh, 58: on_thigh, 68: dict(pitch=-30, roll=20, elbow=60, hand=-10),
             78: dict(pitch=-30, roll=20, elbow=60, hand=-10), 84: on_thigh, 92: on_thigh,
             96: dict(pitch=-40, roll=14, elbow=70, hand=-30), 99: dict(pitch=-84, roll=6, elbow=6, hand=-40),
             102: dict(pitch=-40, roll=14, elbow=70, hand=-30), 108: dict(pitch=-40, roll=14, elbow=70, hand=-30),
             111: dict(pitch=-84, roll=6, elbow=6, hand=-40), 118: dict(pitch=-10, roll=8, elbow=30, hand=10),
             124: dict(pitch=-6, roll=8, elbow=24, hand=10)}
    keysR = {0: dict(pitch=-6, roll=8, elbow=24, hand=10), 12: on_thigh, 24: on_thigh,
             34: dict(pitch=-30, roll=20, elbow=60, hand=-10), 44: dict(pitch=-30, roll=20, elbow=60, hand=-10),
             50: on_thigh, 58: on_thigh, 68: dict(pitch=-20, roll=70, elbow=10, hand=-20),
             78: dict(pitch=-20, roll=74, elbow=10, hand=-20), 84: on_thigh, 92: on_thigh,
             96: dict(pitch=-84, roll=6, elbow=6, hand=-40), 99: dict(pitch=-40, roll=14, elbow=70, hand=-30),
             102: dict(pitch=-84, roll=6, elbow=6, hand=-40), 105: dict(pitch=-40, roll=14, elbow=70, hand=-30),
             108: dict(pitch=-40, roll=14, elbow=70, hand=-30), 118: dict(pitch=-10, roll=8, elbow=30, hand=10),
             124: dict(pitch=-6, roll=8, elbow=24, hand=10)}
    for f, a in keysL.items():
        arm(k, f, "L", **a)
    for f, a in keysR.items():
        arm(k, f, "R", **a)
    k.bake_bezier_now()
    sc = bpy.context.scene

    def raise_t(f, a, b, c):
        """leg up from a to b (hold), slam down b -> c"""
        if a <= f <= b:
            u = (f - a) / (b - a)
            return 0.5 - 0.5 * math.cos(math.pi * min(1.0, u * 1.25))
        if b < f <= c:
            u = (f - b) / (c - b)
            return 1 - u * u
        return 0.0

    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg, (a, b, c) in (("Leg_L", (30, 44, 50)), ("Leg_R", (64, 78, 84))):
            s = 1 if leg.endswith("L") else -1
            t = raise_t(f, a, b, c)
            T = Vector((k.J[leg].x + s * 0.30 * t, k.J[leg].y + 0.02 * t, 0.32 * t))
            k.solve_leg(leg, f, T)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    sumo(k)
    return stride


def check_pairs():
    P = [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R")]
    for s in ("L", "R"):
        for a in ("Fore_" + s, "Hand_" + s):
            for b in ("Spine", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Head", "Jaw", "Chest"):
                P.append((a, b))
    P.append(("Head", "Chest"))
    return P


def joints():
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        Wv = X(W, s)
        out.append((Wv, Wv, 0.08, "Hand_" + side))
    return out
