# Pharaoh Asparuh (SECRET, Void egg): the V2 Persian-cat pharaoh rebuilt in the Steal-an-Egg block style
# (STYLE_BIBLE 3 "PharaohAsparuh"): a SPHINX at rest - belly on the ground, front paws stretched forward (0.6 TL) with
# gold anklets, round haunches with the hind paws tucked beside the belly, the fluffy tail curled along his right side,
# chest up and a huge regal head: big copper half-lidded eyes with kohl wings and 2 highlights, a tiny pink nose, a "w"
# mouth, blush, a fluffy chin ruff. Hero set: a stepped nemes of alternating gold / lapis stripes with striped side
# flaps and lappets past the chin, a gold uraeus with a red gem, a 3-band usekh collar (gold / turquoise / gold) with
# drop gems. 2-bone legs: he gets up and struts in the walk (the sphinx pose unfolds), lies regally in everything else.
# Clips ported from PetsV2: royal idle (look down his nose, slow blink, ear twitch, tail-tip flick), dainty strut walk,
# roar = royal yawn, signature act_groom = licks his raised paw and wipes his face. (V2 act_wiggle dropped: the
# butt-wiggle pounce is ShadePanther's signature.)
import math
from mathutils import Vector, Quaternion, Matrix

DISPLAY = "Pharaoh Asparuh"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 7.0

FUR = (250, 244, 236)
SHADE = (222, 206, 188)
WHITE = (255, 252, 248)
KOHL = (34, 26, 40)
GOLD = (245, 196, 60)
GOLD_D = (214, 156, 36)
LAPIS = (40, 80, 200)
TURQ = (40, 200, 190)
NOSE = (240, 150, 170)
INNER = (246, 168, 180)
IRIS = (240, 150, 40)
BLUSH = (255, 160, 176)
RED_GEM = (220, 40, 60)
MOUTH = (110, 26, 44)
TONGUE = (236, 110, 140)
SHEEN = (250, 250, 255)
GROOVE = (196, 176, 158)

BODY_C, BODY_H = (0, 0.22, 0.27), (0.40, 0.46, 0.25)
CHEST_C, CHEST_H = (0, -0.26, 0.44), (0.46, 0.28, 0.40)
HEAD_C, HEAD_H = (0, -0.46, 1.30), (0.46, 0.35, 0.38)            # HW 0.92 (1.15 TW), HH 0.76
# 2-bone legs (rest = sphinx): front shoulder -> elbow (on the ground) -> wrist (paw stretched forward)
FRONT = ((0.26, -0.36, 0.44), (0.26, -0.44, 0.10), (0.26, -0.98, 0.08))
# hind hip -> hock (back of the haunch, on the ground) -> paw (tucked forward beside the belly)
HIND = ((0.30, 0.42, 0.34), (0.37, 0.58, 0.08), (0.37, 0.06, 0.07))
TAILP = [(-0.06, 0.76, 0.22), (-0.44, 0.98, 0.12), (-0.72, 0.64, 0.10), (-0.75, 0.18, 0.10), (-0.70, -0.10, 0.14)]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def front_y(blk, z):
    t = ((z - blk.c.z) / blk.h.z + 1) / 2
    sy = blk.bot[1] + (blk.top[1] - blk.bot[1]) * t
    return blk.c.y + blk.ts[1] * t - blk.h.y * sy


def front_n(blk):
    dydz = -blk.h.y * (blk.top[1] - blk.bot[1]) / (2 * blk.h.z)
    return Vector((0, -1, dydz)).normalized()


def on_front(B, blk, p0, p1, width, thick, color, bone, **kw):
    """flush bar from (x0, z0) to (x1, z1) on the tapered -y face of an unrotated block"""
    n = front_n(blk)
    a = Vector((p0[0], front_y(blk, p0[1]), p0[1])) + n * (thick + 0.002)
    b = Vector((p1[0], front_y(blk, p1[1]), p1[1])) + n * (thick + 0.002)
    kw.setdefault("studs", [])
    kw.setdefault("bevel", min(0.010, thick * 0.6))
    return B.bar(a, b, n, width, thick, color, bone, **kw)


def model(k):
    """Pharaoh Asparuh, bible SECRET Void: sphinx pose, huge regal head, nemes + uraeus + usekh hero set. Fill .45."""
    import blockkit as bk
    B = bk.Blocks(k, seed=73, tier="S")
    D = 0.70
    body = B.add(BODY_C, BODY_H, SHADE, "Spine", bot=(0.92, 0.95), rnd=0.36, density=D, studs=["+x", "-x", "+y", "+z"])
    chest = B.add(CHEST_C, CHEST_H, FUR, "Spine", bot=(0.90, 0.92), rnd=0.34, density=D)
    # ---- usekh collar on the chest front: 3 U-bands (gold / turquoise / gold) + drop gems
    cz = 0.80
    for r0, r1, col in ((0.13, 0.19, GOLD), (0.19, 0.25, TURQ), (0.25, 0.30, GOLD)):
        r = (r0 + r1) / 2
        N = 7
        for i in range(N):
            a0 = math.radians(-78 + 156 * i / N)
            a1 = math.radians(-78 + 156 * (i + 1) / N)
            p0 = (r * math.sin(a0), cz - r * math.cos(a0))
            p1 = (r * math.sin(a1), cz - r * math.cos(a1))
            on_front(B, chest, p0, p1, r1 - r0 + 0.004, 0.010 if col == TURQ else 0.013, col, "Spine")
    for i in range(7):
        a = math.radians(-66 + 132 * i / 6)
        x, z = 0.335 * math.sin(a), cz - 0.335 * math.cos(a)
        n = front_n(chest)
        p = Vector((x, front_y(chest, z), z)) + n * 0.018
        R = bk.frame_from(p, p + Vector((0, 0, 1)), n) @ Matrix.Rotation(math.radians(45), 3, "X")
        B.add(p, (0.012, 0.032, 0.032), LAPIS if i % 2 else TURQ, "Spine", R=R, studs=[], bevel=0.006)
    # neck (hidden under the ruff) joining chest and head
    B.add((0, -0.32, 0.90), (0.36, 0.20, 0.14), FUR, "Neck", studs=[], rnd=0.4)
    # ---- haunches (round, Leg_B) + tucked hind paws (Shin_B lower leg lying forward, Foot_B paw)
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A = (X(p, s) for p in HIND)
        B.add((s * 0.34, 0.44, 0.25), (0.15, 0.24, 0.23), SHADE, "Leg_B" + side, rnd=0.42, density=D,
              studs=["+x" if s > 0 else "-x", "+z"])
        B.add((s * 0.37, 0.30, 0.065), (0.10, 0.25, 0.065), SHADE, "Shin_B" + side, studs=[], role="limb", rnd=0.4)
        B.add(A + Vector((0, -0.02, -0.005)), (0.115, 0.09, 0.065), WHITE, "Foot_B" + side, studs=[], role="limb",
              rnd=0.4)
        for gx in (-0.04, 0.04):
            B.add(A + Vector((gx, -0.112, 0.0)), (0.006, 0.004, 0.035), GROOVE, "Foot_B" + side, studs=[],
                  bevel=0.002)
    # ---- front legs: upper arm hidden in the chest, forearm stretched forward on the ground, white paw, gold anklet
    for s, side in ((1, "L"), (-1, "R")):
        S, E, W = (X(p, s) for p in FRONT)
        B.seg(S, E, 0.11, 0.11, FUR, "Leg_F" + side, side=(1, 0, 0), ext=0.06, studs=[], role="limb")
        B.seg(E, W, 0.11, 0.08, FUR, "Shin_F" + side, side=(1, 0, 0), ext=0.08, studs=[], role="limb", rnd=0.4)
        B.add(W + Vector((0, -0.05, -0.012)), (0.13, 0.10, 0.068), WHITE, "Foot_F" + side, studs=[], role="limb",
              rnd=0.4)
        for gx in (-0.045, 0.045):
            B.add(W + Vector((gx, -0.152, -0.01)), (0.007, 0.004, 0.04), GROOVE, "Foot_F" + side, studs=[],
                  bevel=0.002)
        B.add(W + Vector((0, 0.12, 0.0)), (0.125, 0.035, 0.092), GOLD, "Shin_F" + side, studs=[], role="limb")
        B.add(W + Vector((0, 0.12, 0.0)) + Vector((0, -0.04, 0)), (0.03, 0.012, 0.03), TURQ, "Shin_F" + side,
              studs=[], bevel=0.006)
    # ---- tail curled along his right side, 2 gold rings
    T = [Vector(p) for p in TAILP]
    for i, (a, b) in enumerate(((0, 1), (1, 2), (2, 4))):
        bone = "Tail%d" % (i + 1)
        if i < 2:
            B.seg(T[a], T[b], 0.10, 0.095, SHADE, bone, side=(0, 0, 1), ext=0.05, studs=[],
                  role="limb", rnd=0.45)
        else:
            B.seg(T[2], T[3], 0.10, 0.095, SHADE, bone, side=(0, 0, 1), ext=0.05, studs=[], role="limb", rnd=0.45)
            B.seg(T[3], T[4], 0.09, 0.09, FUR, bone, side=(0, 0, 1), ext=0.05, top=(0.7, 0.7), studs=[],
                  role="limb", rnd=0.45)
    for (a, b, t, bone) in ((1, 2, 0.45, "Tail2"), (2, 3, 0.55, "Tail3")):
        p = T[a].lerp(T[b], t)
        d = (T[b] - T[a]).normalized()
        B.add(p, (0.112, 0.106, 0.03), GOLD, bone, R=bk.frame_from(p, p + d, (0, 0, 1)), studs=[], role="limb")
    # ---- head (final size): round Persian head, flat face, tiny muzzle, pink nose, w mouth, blush, chin ruff
    head = B.add(HEAD_C, HEAD_H, FUR, "Head", top=(0.94, 0.94), rnd=0.24, density=D, studs=["+y"])
    muz = B.add((0, -0.84, 1.08), (0.20, 0.07, 0.11), WHITE, "Head", top=(0.9, 0.9), studs=[], role="limb", rnd=0.45)
    ny = front_y(muz, 1.15)
    B.add((0, ny - 0.012, 1.15), (0.058, 0.024, 0.034), NOSE, "Head", top=(1.0, 1.0), bot=(0.55, 1.0), studs=[],
          role="limb", rnd=0.3)
    B.add((-0.025, ny - 0.038, 1.168), (0.013, 0.004, 0.009), SHEEN, "Head", studs=[], bevel=0.003)
    my = front_y(muz, 1.07) - 0.006
    for (x, a) in ((-0.06, 35), (-0.02, -35), (0.02, 35), (0.06, -35)):
        B.add((x, my, 1.075), (0.026, 0.005, 0.009), KOHL, "Head", rot=(0, a, 0), studs=[], bevel=0.003)
    # mouth interior behind the lower jaw (shows when the yawn opens the Jaw)
    B.add((0, -0.79, 0.962), (0.12, 0.05, 0.022), MOUTH, "Head", studs=[], bevel=0.01)
    jaw = B.add((0, -0.80, 0.985), (0.15, 0.08, 0.045), WHITE, "Jaw", studs=[], role="limb", rnd=0.4)
    B.add((0, -0.81, 1.026), (0.10, 0.055, 0.006), TONGUE, "Jaw", studs=[], bevel=0.004)
    # regal half-lidded copper eyes, 2 highlights, kohl wing bars sweeping up at the outer corners
    E = B.face_eyes(head, "lovely", IRIS, base=FUR, lids=0.30, z=0.60, x=0.225, scale=0.98)
    HW = E["HW"]
    for s, side in ((1, "L"), (-1, "R")):
        c = E[side]
        ow, oh = 0.30 * HW * 0.98, 0.32 * HW * 0.98
        p0 = c + Vector((s * (ow / 2 - 0.03), -0.008, -oh * 0.22))
        d = Vector((s * math.cos(math.radians(15)), 0, math.sin(math.radians(15))))
        B.bar(p0, p0 + d * 0.11, (0, -1, 0), 0.05, 0.006, KOHL, "Head", studs=[], top=(1, 0.35), bevel=0.004)
    hz = 1.13
    for s in (1, -1):
        B.add((s * 0.33, front_y(head, hz) - 0.008, hz), (0.062, 0.006, 0.024), BLUSH, "Head", studs=[], bevel=0.006)
    # blink lids (own bones): fur plates with a kohl lash line, hidden INSIDE the head at rest, pop forward to blink
    for s, side in ((1, "L"), (-1, "R")):
        c = E[side]
        B.add(c + Vector((0, 0.05, 0.0)), (0.30 * HW / 2 * 1.06, 0.006, 0.32 * HW / 2 * 1.06), FUR, "Lid_" + side,
              studs=[], bevel=0.006)
        B.add(c + Vector((0, 0.044, -0.32 * HW / 2 * 0.9)), (0.30 * HW / 2 * 1.08, 0.007, 0.012), KOHL, "Lid_" + side,
              studs=[], bevel=0.004)
    # fluffy cheek ruff: 3 tapered tufts per side fanning out and down from the lower cheeks, in front of the lappets
    for sx in (1, -1):
        for ang, L, col in ((42, 0.17, WHITE), (66, 0.21, FUR), (90, 0.16, WHITE)):
            root = Vector((sx * 0.34, -0.78, 1.01))
            d = Vector((sx * math.sin(math.radians(ang)), -0.15, -math.cos(math.radians(ang)))).normalized()
            B.seg(root, root + d * L, 0.075, 0.05, col, "Head", side=(0, -1, 0), ext=0.06, top=(0.3, 0.6), studs=[],
                  role="limb")
    # ---- nemes: stepped striped dome (gold brow band at the bottom), striped side flaps and lappets, back queue
    for j, (z0, z1, sx, sy, col) in enumerate(((1.54, 1.63, 0.51, 0.40, GOLD), (1.63, 1.71, 0.49, 0.385, LAPIS),
                                               (1.71, 1.78, 0.45, 0.36, GOLD), (1.78, 1.84, 0.39, 0.32, LAPIS),
                                               (1.84, 1.88, 0.30, 0.26, GOLD))):
        B.add((0, -0.45 + 0.012 * j, (z0 + z1) / 2), (sx, sy, (z1 - z0) / 2 + 0.006), col, "Head", studs=[],
              role="limb", rnd=0.3)
    for s in (1, -1):
        for j in range(5):
            z1 = 1.54 - 0.088 * j
            z0 = z1 - 0.088
            flare = 0.012 * j
            B.add((s * (0.505 + flare), -0.42, (z0 + z1) / 2), (0.05, 0.30 - 0.01 * j, 0.044 + 0.003),
                  LAPIS if j % 2 == 0 else GOLD, "Head", rot=(0, s * 6, 0), studs=[], role="limb", rnd=0.3)
        top, bot = Vector((s * 0.50, -0.70, 1.40)), Vector((s * 0.46, -0.63, 0.78))
        for j in range(7):
            c = top.lerp(bot, (j + 0.5) / 7)
            w = 0.085 + 0.006 * j
            B.add(c, (w, 0.05, 0.045 + 0.003), GOLD if j % 2 == 0 else LAPIS, "Head", rot=(-8, 0, 0), studs=[],
                  role="limb", rnd=0.3)
    B.add((0, -0.04, 1.42), (0.13, 0.08, 0.16), LAPIS, "Head", top=(0.7, 0.8), studs=[], role="limb", rnd=0.35)
    B.add((0, -0.04, 1.30), (0.11, 0.085, 0.03), GOLD, "Head", studs=[], role="limb")
    # uraeus: gold cobra rising from the brow band, hood with a red gem
    B.add((0, -0.865, 1.62), (0.03, 0.025, 0.07), GOLD, "Head", studs=[], role="limb")
    B.add((0, -0.875, 1.70), (0.065, 0.016, 0.07), GOLD_D, "Head", top=(0.6, 1), bot=(0.7, 1), studs=[], role="limb")
    B.add((0, -0.893, 1.70), (0.026, 0.006, 0.032), RED_GEM, "Head", rot=(0, 45, 0), studs=[], bevel=0.005)
    B.add((0, -0.88, 1.78), (0.03, 0.04, 0.025), GOLD, "Head", studs=[], role="limb")
    # ears poking out of the nemes, pink inner, gold cuff
    for s, side in ((1, "L"), (-1, "R")):
        ear = B.add((s * 0.30, -0.36, 1.92), (0.12, 0.06, 0.13), FUR, "Ear_" + side, rot=(-6, 0, -s * 14),
                    top=(0.25, 0.55), studs=[], role="limb")
        B.add(ear.world((0, -0.064, -0.02)), (0.075, 0.008, 0.085), INNER, "Ear_" + side, R=ear.R, top=(0.3, 1),
              studs=[], bevel=0.006)
        B.add(ear.world((0, 0, -0.10)), (0.13, 0.068, 0.03), GOLD, "Ear_" + side, R=ear.R, studs=[], role="limb")
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.16, 0.36), "Root", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.34, 0.84), "Spine", tail=(0, -0.1, 0.3))
    k.joint("Head", (0, -0.36, 0.98), "Neck", tail=(0, -0.35, 0.1))          # throat pivot
    k.joint("Jaw", (0, -0.74, 1.02), "Head", tail=(0, -0.2, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.28, -0.36, 1.82), "Head", tail=(0, 0, 0.2))
        k.joint("Lid_" + side, (s * 0.235, -0.80, 1.376), "Head", tail=(0, -0.1, 0))
        S, E, W = (X(p, s) for p in FRONT)
        k.joint("Leg_F" + side, S, "Spine")
        k.joint("Shin_F" + side, E, "Leg_F" + side)
        k.joint("Foot_F" + side, W, "Shin_F" + side, tail=(0, -0.2, 0))
        k.add_leg2("Leg_F" + side, "Shin_F" + side, "Foot_F" + side, knee=(0, 1, 0))
        H, K, A = (X(p, s) for p in HIND)
        k.joint("Leg_B" + side, H, "Spine")
        k.joint("Shin_B" + side, K, "Leg_B" + side)
        k.joint("Foot_B" + side, A, "Shin_B" + side, tail=(0, -0.2, 0))
        k.add_leg2("Leg_B" + side, "Shin_B" + side, "Foot_B" + side, knee=(0, 1, 0))
    k.joint("Tail1", TAILP[0], "Spine", tail=Vector(TAILP[1]) - Vector(TAILP[0]))
    k.joint("Tail2", TAILP[1], "Tail1", tail=Vector(TAILP[2]) - Vector(TAILP[1]))
    k.joint("Tail3", TAILP[2], "Tail2", tail=Vector(TAILP[3]) - Vector(TAILP[2]))


def check_pairs():
    L = ["Leg_FL", "Shin_FL", "Foot_FL", "Leg_FR", "Shin_FR", "Foot_FR"]
    P = [("Shin_FL", "Shin_FR"), ("Foot_FL", "Foot_FR"), ("Shin_FL", "Foot_FR"), ("Foot_FL", "Shin_FR"),
         ("Leg_BL", "Shin_FL"), ("Leg_BR", "Shin_FR"), ("Shin_BL", "Shin_FL"), ("Shin_BR", "Shin_FR"),
         ("Foot_BL", "Foot_FL"), ("Foot_BR", "Foot_FR"), ("Foot_BL", "Shin_FL"), ("Foot_BR", "Shin_FR"),
         ("Shin_BL", "Shin_BR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in L:
            P.append((a, b))
    for t in ("Tail1", "Tail2", "Tail3"):
        for b in ("Leg_BR", "Shin_BR", "Foot_BR", "Leg_BL", "Shin_BL", "Foot_BL", "Shin_FR", "Foot_FR"):
            P.append((t, b))
    P += [("Ear_L", "Ear_R"), ("Jaw", "Spine")]
    return P


def joints():
    out = [((0, -0.32, 0.90), (0, -0.40, 1.00), 0.30, "Head"), (TAILP[0], TAILP[0], 0.13, "Tail1")]
    for s, side in ((1, "L"), (-1, "R")):
        S, E, W = (X(p, s) for p in FRONT)
        H, K, A = (X(p, s) for p in HIND)
        out += [(E, E, 0.14, "Shin_F" + side), (W, W, 0.14, "Foot_F" + side), (K, K, 0.12, "Shin_B" + side),
                (A, A, 0.12, "Foot_B" + side)]
    return out


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]
LID_IN, LID_OUT = 0.0, -0.085            # lid plate y offset: hidden in the head / covering the eye


def key_q(k, bone, f, q):
    pb = k.arm.pose.bones[bone]
    R0 = k.arm.data.bones[bone].matrix_local.to_quaternion()
    pb.rotation_quaternion = R0.inverted() @ q @ R0
    pb.keyframe_insert("rotation_quaternion", frame=f, group=bone)


def lids(k, f, shut):
    for s in ("L", "R"):
        k.key("Lid_" + s, f, rot=(0, 0, 0), loc=(0, LID_OUT if shut else LID_IN, 0))


def ears(k, f, l=0.0, r=None, back=0.0):
    r = l if r is None else r
    k.key("Ear_L", f, rot=(back, 0, l))
    k.key("Ear_R", f, rot=(back, 0, -r))


def tail_rest(k, f, flick=0.0, lift=0.0):
    """lying tail: stays on the ground along his side, only the tip flicks"""
    k.key("Tail1", f, rot=(lift, 0, 0))
    k.key("Tail2", f, rot=(0, 0, 0))
    k.key("Tail3", f, rot=(0, flick, 0))


def tail_up(k, f, sway=0.0, curl=0.0):
    """walking tail: Tail1 swung back and up behind the rump, Tail2 up, Tail3 curling forward at the tip"""
    T = [Vector(p) for p in TAILP]
    dr = [(T[1] - T[0]).normalized(), (T[2] - T[1]).normalized(), (T[4] - T[2]).normalized()]
    sw = math.radians(sway)
    dt = [Vector((0.12 + 0.4 * math.sin(sw), 0.55, 0.85)).normalized(),
          Vector((0.6 * math.sin(sw), 0.10, 1.0)).normalized(),
          Vector((0.8 * math.sin(sw), -0.55 - 0.3 * curl, 0.80)).normalized()]
    qw = [dr[i].rotation_difference(dt[i]) for i in range(3)]
    key_q(k, "Tail1", f, qw[0])
    key_q(k, "Tail2", f, qw[0].inverted() @ qw[1])
    key_q(k, "Tail3", f, qw[1].inverted() @ qw[2])


def plant(k, n, frames=None, legs=LEGS4):
    cm.plant(k, n, legs=legs, frames=frames)


def idle(k):
    """royal idle (sphinx): chin up, looks down his nose to one side then the other, a slow royal blink in the
    middle, an ear twitch, the tail tip flicks lazily on the ground."""
    n = 90
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n)
        k.key("Spine", f, rot=(-0.8 * s, 0, 0), loc=(0, 0, 0.008 * (1 + s) / 2))
        look = 20 * pk.wave(f, n, 0.0) * abs(pk.wave(f, n, 0.0)) ** 0.4
        k.key("Neck", f, rot=(-3 + 1.5 * pk.cwave(f, n), look * 0.4, 0))
        k.key("Head", f, rot=(-4 + 2.0 * pk.wave(f, n, 0.15, 2), look * 0.6, 4 * pk.wave(f, n, 0.05) * pk.cwave(f, n, 0.05)))
        k.key("Jaw", f, rot=(0, 0, 0))
        tail_rest(k, f, flick=4 * pk.wave(f, n, 0.1, 3))
    for f, shut in ((0, 0), (40, 0), (41, 1), (52, 1), (53, 0), (77, 0), (78, 1), (80, 1), (81, 0), (90, 0)):
        lids(k, f, shut)
    for f, tw in ((0, 0), (62, 0), (65, -22), (68, 6), (71, -18), (76, 0), (90, 0)):
        ears(k, f, 0, tw)
    plant(k, n)
    k.finish()
    k.meta["planted"] = LEGS4


RAISE = 0.31          # he gets up for the walk: the sphinx pose unfolds into a standing strut
STAND_DY = {"F": -0.04, "B": 0.0}


def walk(k):
    """dainty proud strut: up on his legs, lateral-sequence cat walk, head held level and high, tail up in a curl."""
    import bpy
    n = 28
    SH, LIFT, duty = 0.13, 0.09, 0.62
    legs = [("Leg_BL", 0.0), ("Leg_FL", 0.25), ("Leg_BR", 0.5), ("Leg_FR", 0.75)]
    k.new_action("walk", n, True)
    for f in range(0, n + 1, 2):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.0 * pk.wave(f, n, 0.1, 2), 2.0 * pk.wave(f, n, 0.1), 2.5 * pk.wave(f, n)),
              loc=(0, 0, RAISE + 0.022 * b))
        k.key("Neck", f, rot=(-1.0 * pk.wave(f, n, 0.15, 2), -2.0 * pk.wave(f, n, 0.1), 0))
        k.key("Head", f, rot=(-3 + 1.5 * pk.wave(f, n, 0.2, 2), -1.5 * pk.wave(f, n, 0.1), -2.5 * pk.wave(f, n)))
        k.key("Jaw", f, rot=(0, 0, 0))
        tail_up(k, f, sway=8 * pk.wave(f, n, 0.2), curl=0.5 + 0.5 * pk.wave(f, n, 0.3, 2))
        lids(k, f, 0)
        ears(k, f, 0, 0)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg, off in legs:
            g = pk.gait_target(k, leg, f, n, off, SH, LIFT, duty)
            hip = k.J[leg]
            ank = k.J[k.legs2[leg]["foot"]]
            ty = 2 * hip.y - ank.y + (g.y - hip.y) + STAND_DY[leg[4]]
            k.solve_leg(leg, f, Vector((hip.x, ty, g.z)))
    k.finish()
    k.meta["legs"] = legs
    k.meta["duty"] = duty
    k.meta["walk_cycle"] = n
    return (2 * SH) / duty


def roar(k):
    """'roar' slot = ROYAL YAWN: lifts his chest a little, tips his chin to the sky, eyes squeezed shut, jaw wide
    open, ears back, the tail tip curls up and quivers, then a satisfied settle."""
    n = 54
    k.new_action("roar", n, False)
    for f, sp, nk, hd, jw, shut, t in ((0, 0, 0, 0, 0, 0, 0.0), (12, -2, -4, -8, 4, 0, 0.3), (22, -4, -8, -20, 30, 1, 1.0),
                                       (36, -4, -9, -22, 32, 1, 1.0), (44, -1, -3, -6, 4, 0, 0.3), (54, 0, 0, 0, 0, 0, 0.0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        lids(k, f, shut)
        ears(k, f, 0, 0, back=-20 * t)
        tail_rest(k, f, flick=0, lift=0)
        k.key("Tail3", f, rot=(0, 0, 0))
    for f in range(24, 37, 3):       # tail tip quivers
        k.key("Tail3", f, rot=(0, 4 * (1 if (f // 3) % 2 else -1), 0))
    plant(k, n)
    k.finish(loop=False)


def groom(k):
    """SIGNATURE (Pharaoh only) - ROYAL GROOMING: lifts his right front paw to his mouth, licks it a few times (little
    head bobs, eyes half shut), wipes it over his face with a head tilt, sets it back down with dignity."""
    import bpy
    n = 72
    k.new_action("act_groom", n, False)
    for f, nk, hd, yaw, roll, shut in ((0, 0, 0, 0, 0, 0), (10, 2, 4, -10, 0, 0), (16, 4, 8, -10, -6, 0),
                                       (44, 4, 8, -10, -6, 0), (52, 0, -2, -22, -4, 1), (58, 0, -2, -22, -4, 1),
                                       (64, 0, 0, 0, 0, 0), (72, 0, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(0, 0, 2 * (10 <= f <= 58)), loc=(0, 0, 0))
        k.key("Neck", f, rot=(nk, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, roll))
        k.key("Jaw", f, rot=(0, 0, 0))
        lids(k, f, shut)
        ears(k, f, 0, 0)
        tail_rest(k, f, flick=4 * (1 if f in (16, 44) else 0))
    for f in range(18, 44, 4):          # licks: little head bobs with the jaw
        u = 1 if (f // 4) % 2 else 0
        k.key("Head", f, rot=(8 + 5 * u, -10, -6))
        k.key("Jaw", f, rot=(5 * u, 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    W = k.J["Foot_FR"]
    # paw path (ankle): ground -> up in front of the mouth (licks) -> wipe over the face -> back down
    path = [(0, None), (8, None), (14, (-0.20, -1.02, 0.46)), (18, (-0.12, -1.02, 0.64)), (44, (-0.12, -1.02, 0.64)),
            (50, (-0.20, -1.16, 0.80)), (56, (-0.22, -1.14, 0.76)), (63, (-0.26, -1.08, 0.30)), (68, None), (72, None)]
    keyed = {}
    for f, p in path:
        keyed[f] = p
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in ("Leg_FL", "Leg_BL", "Leg_BR"):
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    fr = sorted(keyed)
    for f in range(0, n + 1):
        sc.frame_set(f)
        # interpolate the ankle target along the path (smoothstep between waypoints)
        i = max(j for j in range(len(fr)) if fr[j] <= f)
        f0 = fr[i]
        f1 = fr[min(i + 1, len(fr) - 1)]
        p0 = keyed[f0] or (W.x, W.y, W.z)
        p1 = keyed[f1] or (W.x, W.y, W.z)
        u = 0.0 if f1 == f0 else (f - f0) / (f1 - f0)
        u = u * u * (3 - 2 * u)
        A = Vector(p0).lerp(Vector(p1), u)
        lift = max(0.0, min(1.0, (A.z - W.z) / 0.35))
        hip = k.J["Leg_FR"]
        T = Vector((A.x - W.x + hip.x, A.y - W.y + hip.y, A.z - W.z))
        k.solve_leg("Leg_FR", f, T, toe=-75 * lift)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    groom(k)
    return stride
