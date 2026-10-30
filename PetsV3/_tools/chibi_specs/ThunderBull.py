# Thunder Bull (Thunder egg): a front-heavy storm bull, rebuilt to STYLE_BIBLE.md (2026-10-08 pro pass): a huge
# shoulder hump carrying a two-tone storm cloud, the head held low with a light muzzle + gold nose ring, a heavy dark
# 20 deg brow ridge over fierce yellow eyes, wide upswept 3-segment horns, short pillar legs with light fetlock socks
# and split hooves, chunky bolt inlays on the shoulders. No glow (sparks = particle VFX in Studio).
# Own moves: idle = chews its cud, tail swishes, glares aside, ear flicks; roar = deep BELLOW; signature =
# THUNDER CHARGE (scrapes the ground twice, drops its horns, lunges, finishes with an upward horn toss).
import math
from mathutils import Vector

DISPLAY = "Thunder Bull"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 9.0

SLATE = (74, 86, 146)
LIGHT = (176, 188, 236)
DARK = (34, 38, 64)
HORN = (242, 234, 212)
HORN_T = (70, 70, 96)
CLOUD = (238, 242, 255)
CLOUD_D = (184, 194, 226)
BOLT = (255, 206, 46)
GOLD = (246, 196, 64)
IRIS = (255, 214, 60)
MOUTH = (110, 26, 44)

# leg joints (left side; right = mirrored x): hip, knee/hock, ankle
LEGS = {"FL": ((0.27, -0.40, 0.92), (0.27, -0.56, 0.42), (0.27, -0.41, 0.13)),
        "BL": ((0.21, 0.42, 0.90), (0.21, 0.58, 0.42), (0.21, 0.43, 0.13))}   # bent at rest: IK reach for the stride


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def flank_band(B, cx, hx, bot, cz, hz, s, y0, y1, z0, z1, color, bone, out=0.006, thick=0.011):
    """flush band on the +-x flank of a block with a bot taper (lesson 2): x follows the taper, normal tilted"""
    dxdz = hx * (1 - bot) / (2 * hz)
    zm = (z0 + z1) / 2
    t = (zm - (cz - hz)) / (2 * hz)
    x = s * (cx + hx * (bot + (1 - bot) * t) + out)
    n = Vector((s, 0, -dxdz)).normalized()
    return B.bar(Vector((x, y0, zm)), Vector((x, y1, zm)), n, z1 - z0, thick, color, bone, studs=[], bevel=0.008)


def model(k):
    """STYLE_BIBLE ThunderBull: chest 1.25 x hips (W) with a hump, head 0.80 chest W, legs 0.50 TH x 0.38 TW,
    slate / light / dark zones + ivory horns, cloud, yellow bolts and a gold nose ring."""
    import blockkit as bk
    B = bk.Blocks(k, seed=31, tier=3)
    D = 0.62
    # ---- one torso: the chest is the big mass (25 % wider, 36 % taller than the hips), hips overlap 37 %
    chest = B.add((0, -0.22, 0.95), (0.50, 0.50, 0.45), SLATE, "Chest", bot=(0.90, 0.95), density=D)
    B.add((0, 0.38, 0.90), (0.40, 0.40, 0.33), SLATE, "Spine", bot=(0.92, 0.95), density=D)
    B.add((0, -0.30, 1.47), (0.40, 0.36, 0.14), SLATE, "Chest", top=(0.70, 0.70), density=D)       # shoulder hump
    # light belly slab + brisket inlay (flush, following the chest front taper)
    B.add((0, -0.22, 0.495), (0.30, 0.40, 0.03), LIGHT, "Chest", studs=[], role="limb")
    B.add((0, -0.703, 0.70), (0.27, 0.008, 0.17), LIGHT, "Chest", bot=(0.55, 1), studs=[], bevel=0.006)
    # ---- two-tone storm cloud riding the hump
    for p, h, c in (((0, -0.30, 1.66), (0.27, 0.25, 0.13), CLOUD), ((0.21, -0.17, 1.60), (0.17, 0.17, 0.11), CLOUD_D),
                    ((-0.19, -0.44, 1.60), (0.18, 0.16, 0.11), CLOUD_D), ((-0.08, -0.06, 1.62), (0.15, 0.14, 0.10), CLOUD),
                    ((0.07, -0.38, 1.80), (0.16, 0.15, 0.10), CLOUD)):
        B.add(p, h, c, "Chest", studs=[], rnd=0.45, role="mass")
    # ---- flat lightning bolts laid on the tapered chest flanks (shoulders), ending in a point
    for s in (1, -1):
        n = Vector((s, 0, -0.0556)).normalized()
        P = [Vector((s * (0.452 + 0.0556 * (z - 0.50)), y, z)) for y, z in ((-0.56, 1.26), (-0.40, 1.02),
                                                                           (-0.26, 1.10), (-0.12, 0.84))]
        for a, b in zip(P, P[1:]):
            B.bar(a, b, n, 0.10, 0.014, BOLT, "Chest", studs=[], bevel=0.006)
        dl = (P[3] - P[2]).normalized()
        B.bar(P[3], P[3] + dl * 0.11, n, 0.10, 0.014, BOLT, "Chest", studs=[], bevel=0.006, top=(1, 0.1))
    # ---- light belly underline on both flanks, between the legs: chest band with a 2-step top edge + hips band
    for s in (1, -1):
        for y0, y1, z0, z1 in ((-0.15, 0.24, 0.53, 0.64), (-0.15, 0.11, 0.635, 0.69), (-0.15, -0.02, 0.685, 0.74)):
            flank_band(B, 0, 0.50, 0.90, 0.95, 0.45, s, y0, y1, z0, z1, LIGHT, "Chest")
        flank_band(B, 0, 0.40, 0.92, 0.90, 0.33, s, 0.25, 0.70, 0.60, 0.68, LIGHT, "Spine", out=0.013)
    # ---- thick neck bridging chest and head (mostly hidden)
    B.add((0, -0.84, 1.06), (0.38, 0.17, 0.27), SLATE, "Neck", studs=["+x", "-x"], density=D)
    # ---- head: HW 0.80 (= 0.80 chest W), HH 0.69 (= 0.75 chest H), held low in front of the chest
    head = B.add((0, -1.24, 1.00), (0.42, 0.31, 0.35), SLATE, "Head", top=(0.94, 0.94), top_shift=(0, -0.04),
                 density=D)
    muz = B.add((0, -1.60, 0.81), (0.27, 0.18, 0.13), LIGHT, "Head", top=(0.88, 0.85), role="limb")
    for s in (1, -1):                                                                  # 2 dark nostril plates
        B.add((s * 0.11, -1.770, 0.85), (0.05, 0.014, 0.036), DARK, "Head", rot=(-5, 0, 0), studs=[], bevel=0.008)
    # gold nose ring of 4 blocks hanging from the septum
    for p, h in (((0, -1.775, 0.77), (0.07, 0.02, 0.02)), ((0.058, -1.775, 0.705), (0.02, 0.02, 0.055)),
                 ((-0.058, -1.775, 0.705), (0.02, 0.02, 0.055)), ((0, -1.775, 0.642), (0.07, 0.02, 0.02))):
        B.add(p, h, GOLD, "Head", studs=[], bevel=0.008)
    # mouth (shows when the jaw drops) + light lower jaw
    B.add((0, -1.53, 0.663), (0.19, 0.12, 0.006), MOUTH, "Head", studs=[], bevel=0.004)
    B.add((0, -1.55, 0.64), (0.22, 0.16, 0.05), LIGHT, "Jaw", bot=(0.85, 0.9), role="limb")
    # glaring eyes: bold eyes, lightly lidded, one glint ON each pupil, under ONE heavy dark 20 deg brow ridge
    # (2 brows + a keystone joining their inner ends into a continuous V)
    B.face_eyes(head, "bold", IRIS, base=SLATE, brow=DARK, lids=0.22, look=(0, 0.6), scale=0.90, z=0.60,
                pupil_size=(0.085, 0.09), hl_on_pupil=True, hl_size=(0.05, 0.0), brow_spec=(0.40, 0.09, 20))
    vk = 1.19 - head.c.z
    fk = (vk / head.h.z + 1) / 2
    fyk = -head.h.y * (head.bot[1] + (head.top[1] - head.bot[1]) * fk) + head.ts[1] * fk
    B.add((0, head.c.y + fyk - 0.0146, 1.19), (0.07, 0.0126, 0.045), DARK, "Head", studs=[], rnd=0.15, bevel=0.015)
    # ---- horns: 3 curving tapered segments, ivory with a dark 2-tone tip (span ~2.2 HW)
    for s in (1, -1):
        h0, h1 = Vector((s * 0.30, -1.12, 1.27)), Vector((s * 0.62, -1.14, 1.34))
        h2, h3 = Vector((s * 0.82, -1.24, 1.56)), Vector((s * 0.84, -1.46, 1.74))         # tips hook forward
        B.seg(h0, h1, 0.10, 0.10, HORN, "Head", side=(0, 0, 1), ext=0.04, studs=[], top=(0.85, 0.85), role="limb")
        B.seg(h1, h2, 0.085, 0.085, HORN, "Head", side=(0, 0, 1), ext=0.04, studs=[], top=(0.82, 0.82), role="limb")
        d = (h3 - h2)
        B.spike(h2 - d.normalized() * 0.03, d, d.length * 0.70 + 0.03, 0.07, HORN, "Head", top=(0.45, 0.45))
        B.spike(h2 + d * 0.62, d, d.length * 0.42, 0.047, HORN_T, "Head")
    # ---- ears under the horns, lined light
    for s, side in ((1, "L"), (-1, "R")):
        ear = B.add((s * 0.49, -1.06, 1.12), (0.13, 0.06, 0.075), SLATE, "Ear_" + side, rot=(0, -s * 28, 0),
                    studs=[], role="limb")
        B.add(ear.world((s * 0.03, -0.062, -0.005)), (0.08, 0.008, 0.045), LIGHT, "Ear_" + side, R=ear.R, studs=[],
              bevel=0.006)
    # ---- legs: thigh + shin (top buried 30 %), flush light fetlock sock, split dark hoof
    for s, side in ((1, "L"), (-1, "R")):
        for fb, (thw, thd, shw, shd) in (("F", (0.19, 0.20, 0.16, 0.17)), ("B", (0.16, 0.19, 0.14, 0.16))):
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            x, y = H.x, H.y
            B.add((x, y, 0.62), (thw, thd, 0.26), SLATE, leg, bot=(0.92, 0.94), density=D)
            B.add((x, y - 0.01, 0.29), (shw, shd, 0.19), SLATE, shin, density=D)
            B.add((x, y - 0.01, 0.225), (shw * 1.02, shd * 1.02, 0.105), LIGHT, shin, studs=[], role="limb")
            for gx in (-1, 1):
                B.add((x + gx * 0.088, y - 0.03, 0.065), (0.082, shd * 1.12, 0.065), DARK, foot, studs=[],
                      role="limb")
            B.add((x, y + 0.04, 0.07), (shw * 1.05, shd * 0.8, 0.06), DARK, foot, studs=[], role="limb")
    # ---- tail: dark rope swung clear of the rump, two-tone cloud tuft
    B.seg((0, 0.76, 1.16), (0, 0.98, 0.84), 0.10, 0.075, DARK, "Tail1", ext=0.06, top=(0.75, 0.8), studs=[],
          role="limb")
    B.seg((0, 0.98, 0.84), (0, 1.04, 0.60), 0.075, 0.06, DARK, "Tail2", ext=0.03, top=(0.85, 0.85), studs=[],
          role="limb")
    B.add((0, 1.05, 0.52), (0.11, 0.11, 0.11), CLOUD, "Tail2", studs=[], rnd=0.45, role="mass")
    B.add((0, 1.06, 0.42), (0.08, 0.08, 0.07), CLOUD_D, "Tail2", studs=[], rnd=0.45, role="mass")
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.38, 0.92), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, 0.0, 0.95), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.72, 1.22), "Chest")
    k.joint("Head", (0, -0.98, 0.92), "Neck", tail=(0, -0.4, -0.05))          # low-back pivot (nods + horn toss)
    k.joint("Jaw", (0, -1.40, 0.67), "Head", tail=(0, -0.3, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.40, -1.08, 1.12), "Head", tail=(s * 0.2, 0, 0))
        for fb, parent, knee in (("F", "Chest", (0, -1, 0)), ("B", "Spine", (0, 1, 0))):
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.25, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", (0, 0.76, 1.12), "Spine")
    k.joint("Tail2", (0, 0.98, 0.84), "Tail1", tail=(0, 0.02, -0.3))


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2"]


def ears(k, f, a=0.0, b=None):
    b = a if b is None else b
    k.key("Ear_L", f, rot=(0, 0, a))
    k.key("Ear_R", f, rot=(0, 0, -b))


def idle(k):
    """grumpy guard: heavy breaths, chews its cud, tail swishes at flies, turns its head to glare and holds it,
    ear flicks."""
    n = 140
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 4)
        k.key("Spine", f, rot=(0, 0, 0.6 * pk.wave(f, n, 0.2)), loc=(0, 0, 0.012 * b))
        k.key("Chest", f, rot=(-1.0 * b, 0, 0))
        chew = 0 if 60 <= f <= 100 else 1
        k.key("Jaw", f, rot=(4 + 3.5 * chew * (0.5 + 0.5 * math.sin(2 * math.pi * f / 14)), 0,
                             2.5 * chew * math.sin(2 * math.pi * f / 14)))
    for f, nk, hd, yaw in ((0, 0, 0, 0), (50, 0, 0, 0), (60, -4, -6, 30), (96, -4, -6, 30), (108, 0, 0, 0), (140, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, 0))
    # tail swishes at flies: quick swing out and back, twice
    for f, yaw, pt in ((0, 0, 0), (20, 0, 0), (25, 16, 18), (31, -13, 16), (37, 0, 0), (110, 0, 0), (115, -16, 18),
                       (121, 13, 16), (127, 0, 0), (140, 0, 0)):
        k.key("Tail1", f, rot=(pt, yaw, 0))
        k.key("Tail2", f, rot=(pt * 0.5, yaw * 0.8, 0))
    for f, a, b in ((0, 0, 0), (40, 0, 0), (43, -26, 0), (47, 0, 0), (84, 0, 0), (87, 0, -26), (91, 0, 0), (140, 0, 0)):
        ears(k, f, a, b)
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    n = 32

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 1.5 * pk.wave(f, n, 0.0), 2.0 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.03 * b))
        k.key("Chest", f, rot=(0, -2 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(3 * pk.wave(f, n, 0.1, 2), 0, 0))
        k.key("Head", f, rot=(-2 * pk.wave(f, n, 0.2, 2), 2 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(4, 0, 0))
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(10, 6 * pk.wave(f, n, 0.3 + 0.1 * i), 0))
        ears(k, f, 0, 0)
    return cm.quad_walk(k, n, 0.22, 0.14, body, gait="walk")


def roar(k):
    """BELLOW: braces, drops the head, then swings the neck forward and up with the mouth wide, tail lifts."""
    n = 62
    k.new_action("roar", n, False)
    for f, ch, nk, hd, jw, tl in ((0, 0, 0, 0, 4, 0), (12, 4, 10, 12, 6, 0), (22, -6, -16, -14, 32, 26),
                                  (46, -6, -18, -16, 34, 30), (54, 0, -2, 0, 8, 6), (62, 0, 0, 0, 4, 0)):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, -0.03 * (12 <= f <= 46)))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Tail1", f, rot=(tl, 0, 0))
        k.key("Tail2", f, rot=(tl * 0.6, 0, 0))
        ears(k, f, -20 * (22 <= f <= 46), -20 * (22 <= f <= 46))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def charge(k):
    """SIGNATURE - THUNDER CHARGE: paws the ground twice with the right fore-hoof, lowers the horns with the body
    rocked back, LUNGES forward, then one powerful upward horn toss with the hind end bucking up."""
    import bpy
    n = 84
    k.new_action("act_charge", n, False)
    P = [  # f, spine (y, z, pitch), chest pitch, neck, head, tail, jaw
        (0, 0.0, 0.0, 0, 0, 0, 0, 0, 4),
        (34, 0.08, -0.04, -3, 2, 8, 14, 14, 6),
        (44, 0.12, -0.08, -5, 3, 10, 16, 20, 6),
        (52, -0.22, -0.06, 6, 3, 6, 12, 26, 10),
        (58, -0.18, -0.02, -8, -6, -22, -24, 30, 24),
        (64, -0.08, 0.02, 4, -2, -8, -6, 10, 8),
        (74, 0.0, 0.0, 0, 0, 0, 0, 0, 4),
        (84, 0.0, 0.0, 0, 0, 0, 0, 0, 4)]
    for f, y, z, p, ch, nk, hd, tl, jw in P:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, y, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Tail1", f, rot=(tl, 0, 0))
        k.key("Tail2", f, rot=(tl * 0.5, 0, 0))
        ears(k, f, -24 * (40 <= f <= 60), -24 * (40 <= f <= 60))
    k.bake_bezier_now()
    sc = bpy.context.scene
    J = k.J
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS4:
            T = Vector((J[leg].x, J[leg].y, 0.0))
            if leg == "Leg_FR" and 4 <= f <= 30:        # two scrapes: lift, drag the hoof back along the ground
                u = ((f - 4) % 13) / 13
                if u < 0.35:
                    T = Vector((J[leg].x, J[leg].y - 0.18 * math.sin(math.pi * u / 0.35 * 0.5), 0.10 * math.sin(math.pi * u / 0.35)))
                else:
                    v = (u - 0.35) / 0.65
                    T = Vector((J[leg].x, J[leg].y - 0.18 + 0.30 * v, 0.0))
            if leg in ("Leg_BL", "Leg_BR") and 56 <= f <= 64:          # hind end bucks up with the toss
                T = Vector((J[leg].x, J[leg].y, 0.20 * math.sin(math.pi * (f - 56) / 8)))
            k.solve_leg(leg, f, T)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    charge(k)
    return stride


def check_pairs():
    pairs = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
             ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Head", "Leg_FL"), ("Head", "Leg_FR"),
             ("Jaw", "Leg_FL"), ("Jaw", "Leg_FR"), ("Head", "Shin_FL"), ("Head", "Shin_FR"),
             ("Tail1", "Leg_BL"), ("Tail1", "Leg_BR"), ("Tail2", "Leg_BL"), ("Tail2", "Leg_BR"), ("Head", "Chest")]
    return pairs
