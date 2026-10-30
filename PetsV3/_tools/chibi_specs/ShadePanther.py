# Shade Panther (Void egg #1, tier 5): a sleek shadow panther rebuilt to STYLE_BIBLE.md (2026-10-08 pro pass): a long
# low indigo-violet feline with a big cat head (almond wedge eyes with a light rim, slit pupils, 2 highlights, a lilac
# muzzle with a dark nose, whiskers and one small fang), tall lined ears, dark rosettes (4 dark plates around a mid
# tone plate) on the flanks, a lilac bib, belly and socks, violet crystal clusters on both shoulder blades and at the
# tip of a thick tail that curls up at the end. No glow (wisps = particle VFX at the paws).
# Own moves: idle = the big-cat STRETCH (paws forward, chest down, rump up), tail-tip twitches, looks around, ear flicks;
# walk = low prowl; roar = HISS (back arched, ears flat, jaw wide, tail straight up); signature = STALK & POUNCE (creeps
# low, butt wiggle, leaps forward through the air, pins and bites, springs back).
import math
from mathutils import Vector, Euler

DISPLAY = "Shade Panther"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 7.5

FUR = (60, 48, 100)
LIGHT = (124, 108, 182)
MID = (92, 78, 141)
DARK = (28, 22, 48)
CRYS = (190, 130, 255)
CRYS_L = (236, 200, 255)
IRIS = (150, 80, 235)          # deeper than the bible's (186,116,255) so it reads against the light rim
MOUTH = (110, 26, 44)
FANG = (246, 244, 250)
RIM = (232, 226, 255)

# leg joints (left side): hip, knee (set back: IK slack, elbows/hocks fold back), ankle
LEGS = {"FL": ((0.185, -0.36, 0.58), (0.185, -0.26, 0.32), (0.185, -0.36, 0.10)),   # outer faces flush with the
        "BL": ((0.15, 0.34, 0.58), (0.15, 0.44, 0.32), (0.15, 0.34, 0.10))}         # tapered chest / hips flanks
TAILP = [(0, 0.50, 0.86), (0, 0.76, 0.74), (0, 1.02, 0.72), (0, 1.24, 0.84), (0, 1.36, 1.08)]
TH = 0.62
HEAD_FWD = 0.12        # head group sits this far forward of where it is modelled (room to yaw / nod)
HEADB = ("Head", "Jaw", "Ear_L", "Ear_R")


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def flank(blk, s, y, z, off=0.004):
    """point + normal on the +-x flank of a bottom-tapered block (local y, z), following the taper"""
    hx, hz = blk.h.x, blk.h.z
    tb = 1 - blk.bot[0]
    t = (z + hz) / (2 * hz)
    p = blk.world(Vector((s * (hx * (1 - tb * (1 - t)) + off), y, z)))
    n = (blk.R @ Vector((s, 0, -hx * tb / (2 * hz)))).normalized()
    return p, n


def rosette(B, blk, s, y, z, r=0.062, a=0.034):
    """rosette: 4 dark plates (a broken ring of short bars) around 1 mid-tone plate, laid on a flank"""
    import blockkit as bk
    p, n = flank(blk, s, y, z)
    R = bk.frame_from(Vector(), n, Vector((0, 0, 1)))       # local z = normal, local x = up
    B.add(p + n * 0.010, (a * 0.95, a * 0.95, 0.012), MID, blk.bone, R=R, studs=[], bevel=0.008, role="detail")
    for du, dv in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        hu, hv = (a * 0.55, a * 1.45) if du else (a * 1.45, a * 0.55)
        B.add(p + n * 0.012 + R @ Vector((du * r, dv * r, 0)), (hu, hv, 0.014), DARK, blk.bone, R=R, studs=[],
              bevel=0.008, role="detail")


def cluster(B, base, d, L, w, bone, splay=24, n=3, seed=0):
    """crystal cluster: 1 main shard (rotated 45 deg about its axis) + n smaller shards splayed around it; lower
    60 % mid tone, tip light; dark rock collar at the base"""
    import blockkit as bk
    d = Vector(d).normalized()
    base = Vector(base)
    side = d.orthogonal().normalized()
    B.add(base + d * 0.01, (w * 1.6, w * 1.6, w * 0.8), DARK, bone, R=bk.frame_from(base, base + d, side), studs=[],
          role="limb")
    shards = [(d, L, w)]
    for i in range(n):
        ang = math.radians(splay)
        rot = (d.cross(side).normalized() * math.cos(2 * math.pi * i / n + seed) + side * math.sin(2 * math.pi * i / n + seed))
        dd = (d * math.cos(ang) + rot * math.sin(ang)).normalized()
        shards.append((dd, L * (0.55 + 0.15 * ((i + 1) % 2)), w * 0.75))
    for dd, ln, ww in shards:
        sd = (dd.orthogonal().normalized() + dd.cross(dd.orthogonal()).normalized()).normalized()   # 45 deg twist
        R = bk.frame_from(base, base + dd, sd)
        B.add(base + dd * (0.60 * ln / 2), (ww, ww, 0.60 * ln / 2), CRYS, bone, R=R, top=(0.82, 0.82), studs=[],
              role="limb")
        B.add(base + dd * (0.60 * ln + 0.40 * ln / 2 - 0.004), (ww * 0.82, ww * 0.82, 0.40 * ln / 2), CRYS_L, bone, R=R,
              top=(0.10, 0.10), studs=[], role="limb")


def model(k):
    """STYLE_BIBLE ShadePanther: see the header."""
    import blockkit as bk
    B = bk.Blocks(k, seed=131, tier=5, th=TH)
    D = 0.62
    # ---- one torso: deep chest 15 % bigger than the hips, 41 % overlap
    chest = B.add((0, -0.20, 0.72), (0.33, 0.36, 0.31), FUR, "Chest", bot=(0.90, 0.95), density=D)
    hips = B.add((0, 0.22, 0.70), (0.28, 0.32, 0.26), FUR, "Spine", bot=(0.90, 0.95), density=D)
    B.add((0, -0.56, 0.72), (0.20, 0.03, 0.17), LIGHT, "Chest", bot=(0.55, 1), studs=[], role="limb")        # bib
    B.add((0, -0.12, 0.415), (0.20, 0.36, 0.012), LIGHT, "Chest", studs=[], role="limb")                      # belly
    B.add((0, 0.22, 0.445), (0.17, 0.26, 0.012), LIGHT, "Spine", studs=[], role="limb")
    for s in (1, -1):        # rosettes (2x the old size) on the flanks
        for y, z in ((-0.24, 0.10), (0.04, -0.08), (0.10, 0.14)):
            rosette(B, chest, s, y, z)
        for y, z in ((0.10, 0.06), (-0.10, -0.08)):
            rosette(B, hips, s, y, z, r=0.056, a=0.031)
    # crystal clusters on both shoulder blades
    for s in (1, -1):
        cluster(B, (s * 0.17, -0.30, 1.02), (s * 0.35, 0.45, 1), 0.26, 0.052, "Chest", seed=s)
    # ---- neck (hidden bridge) + big cat head: HW 0.63 (0.95 TW), HH 0.50 (0.81 TH)
    B.add((0, -0.68, 0.93), (0.29, 0.15, 0.18), FUR, "Neck", studs=[])
    head = B.add((0, -0.86, 1.02), (0.315, 0.26, 0.25), FUR, "Head", top=(0.92, 0.94), density=D,
                 studs=["+x", "-x", "+z", "+y"])
    muz = B.add((0, -1.16, 0.87), (0.17, 0.145, 0.10), LIGHT, "Head", top=(0.86, 1.0), studs=[], role="limb")
    B.add((0, -1.312, 0.952), (0.066, 0.03, 0.04), DARK, "Head", bot=(0.45, 0.8), studs=[], role="limb")    # cat nose
    B.add((-0.024, -1.345, 0.972), (0.011, 0.004, 0.011), (246, 244, 250), "Head", studs=[], bevel=0.003)
    for s in (1, -1):        # "w" mouth + one small fang, 3 light whiskers per side
        B.add((s * 0.035, -1.309, 0.885), (0.04, 0.006, 0.010), DARK, "Head", rot=(0, s * 24, 0), studs=[], bevel=0.004)
        for i, (dz, dd) in enumerate(((0.05, 0.10), (0.0, 0.0), (-0.05, -0.10))):
            p0 = Vector((s * 0.15, -1.23, 0.88 + dz))
            p1 = p0 + Vector((s * 0.22, 0.03, dd * 0.6))
            B.bar(p0, p1, (0, -1, 0), 0.022, 0.008, CRYS_L, "Head", studs=[], bevel=0.004)
    B.spike((0.05, -1.31, 0.882), (0, 0, -1), 0.05, 0.016, FANG, "Head", role="limb")
    for s in (1, -1):        # cheek fur: 2 tapered blades per side growing from the lower back edge of the head
        for z, dz, L in ((0.84, -0.40, 0.17), (0.93, -0.05, 0.14)):
            root = Vector((s * 0.29, -0.98, z))
            d = Vector((s * 0.75, 0.50, dz)).normalized()
            B.seg(root, root + d * L, 0.065, 0.03, MID, "Head", side=(0, 0, 1), ext=0.05, top=(0.15, 0.5), studs=[],
                  role="limb")
    B.add((0, -1.13, 0.75), (0.15, 0.13, 0.04), LIGHT, "Jaw", bot=(0.85, 0.9), studs=[], role="limb")
    B.add((0, -1.14, 0.792), (0.12, 0.10, 0.004), MOUTH, "Jaw", studs=[], bevel=0.003)
    # almond wedge eyes with a light rim, slit pupils, 2 highlights (kept clear of the slit), dark 20 deg brows
    B.face_eyes(head, "fierce", IRIS, base=FUR, brow=DARK, outline=RIM, look=(0.6, 0.5), z=0.60, scale=1.12,
                pupil_size=(0.05, 0.09), hl_size=(0.045, 0.022), brow_spec=(0.28, 0.06, 20))
    # tall cat ears lined with lilac
    for s, side in ((1, "L"), (-1, "R")):
        R = Euler((math.radians(-6), math.radians(s * 8), math.radians(-s * 10)), "XYZ").to_matrix()
        root = Vector((s * 0.21, -0.82, 1.24))
        ear = B.add(root + R @ Vector((0, 0, 0.14)), (0.105, 0.045, 0.16), FUR, "Ear_" + side, R=R, top=(0.15, 0.5),
                    studs=[], role="limb")
        B.add(ear.world((0, -0.047, -0.03)), (0.07, 0.008, 0.10), CRYS, "Ear_" + side, R=R, top=(0.15, 1), studs=[],
              bevel=0.006)
    # ---- legs: thicker thigh, shin with a flush lilac sock, lilac paw with 3 pale claw nubs
    for s, side in ((1, "L"), (-1, "R")):
        for fb, (H, K, A) in (("F", LEGS["FL"]), ("B", LEGS["BL"])):
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            x, y = s * H[0], H[1]
            tw = 0.13 if fb == "F" else 0.12
            B.add((x, y, 0.50), (tw, 0.15, 0.24), FUR, leg, bot=(0.88, 0.90), density=D)
            B.add((x, y - 0.01, 0.20), (0.10, 0.125, 0.16), FUR, shin, density=D)
            B.add((x, y - 0.01, 0.10), (0.102, 0.1275, 0.06), LIGHT, shin, studs=[], role="limb")
            B.add((x, y - 0.035, 0.04), (0.118, 0.15, 0.04), LIGHT, foot, studs=[], role="limb")
            for gx in (-0.07, 0.0, 0.07):
                B.add((x + gx, y - 0.19, 0.028), (0.02, 0.025, 0.018), CRYS_L, foot, studs=[])
    # ---- thick tail (root 0.25 TW) curling up at the end, crystal cluster at the tip
    P = [Vector(p) for p in TAILP]
    for i, ((a, b), w) in enumerate(zip(zip(P, P[1:]), (0.085, 0.072, 0.06, 0.05))):
        B.seg(a, b, w, w, FUR, "Tail%d" % (i + 1), ext=0.035, studs=[], role="limb")
    B.add(P[4] - Vector((0, 0.03, 0.08)), (0.055, 0.055, 0.05), DARK, "Tail4", rot=(-30, 0, 0), studs=[], role="limb")
    cluster(B, P[4] - Vector((0, 0.0, 0.02)), (0, 0.35, 1), 0.24, 0.048, "Tail4", seed=0.4)
    for blk in B.items:
        if blk.bone in HEADB:
            blk.c = blk.c + Vector((0, -HEAD_FWD, 0))
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.22, 0.72), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.04, 0.72), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.52, 0.86), "Chest", tail=(0, -0.3, 0.12))
    k.joint("Head", (0, -0.66 - HEAD_FWD, 0.82), "Neck", tail=(0, -0.35, 0))            # throat pivot
    k.joint("Jaw", (0, -1.00 - HEAD_FWD, 0.78), "Head", tail=(0, -0.2, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.21, -0.82 - HEAD_FWD, 1.24), "Head", tail=(s * 0.05, 0, 0.2))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, 1, 0))):
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.2, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    for i in range(4):
        k.joint("Tail%d" % (i + 1), TAILP[i], "Spine" if i == 0 else "Tail%d" % i,
                tail=tuple(Vector(TAILP[i + 1]) - Vector(TAILP[i])))


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3", "Tail4"]


def ears(k, f, a=0.0, b=None, back=0.0):
    b = a if b is None else b
    k.key("Ear_L", f, rot=(back, -a, 0))
    k.key("Ear_R", f, rot=(back, b, 0))


def tail(k, f, n, sway=8.0, lift=0.0, cycles=2, twitch=0.0):
    cm.chain(k, f, n, TAIL, sway=sway, pitch=lift, cycles=cycles, lag=0.14, grow=0.45)
    if twitch:
        k.key("Tail4", f, rot=(lift, sway * 2 * pk.wave(f, n, 0.5, cycles) + twitch, 0))


def idle(k):
    """the big-cat STRETCH (front paws slide forward, chest sinks, rump stays high, head low), back up; then watches
    something off to the left with the tail tip twitching; ear flicks."""
    import bpy
    n = 150
    k.new_action("idle", n, True)

    def st(f):
        if 22 <= f <= 34:
            return 0.5 - 0.5 * math.cos(math.pi * (f - 22) / 12)
        if 34 < f < 58:
            return 1.0
        if 58 <= f <= 72:
            return 0.5 + 0.5 * math.cos(math.pi * (f - 58) / 14)
        return 0.0

    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 4)
        u = st(f)
        k.key("Spine", f, rot=(6 * u, 0, 0), loc=(0, 0, 0.006 * b - 0.03 * u))
        k.key("Chest", f, rot=(-0.8 * b + 14 * u, 0, 0))
        tw = 18 * math.sin(2 * math.pi * f / 9) if 90 <= f <= 126 else 0.0
        tail(k, f, n, sway=6, lift=4 + 20 * u, cycles=2, twitch=tw)
    for f, nk, h, hy, jw in ((0, 0, 0, 0, 0), (22, 0, 0, 0, 0), (34, 18, -24, 0, 0), (44, 18, -28, 0, 26), (50, 18, -24, 0, 2),
                             (58, 18, -24, 0, 0), (72, 0, 0, 0, 0), (88, 0, 0, 0, 0), (96, -4, -4, 26, 0), (124, -4, -4, 26, 0),
                             (134, 0, 0, 0, 0), (150, 0, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, hy * 0.3, 0))
        k.key("Head", f, rot=(h, hy * 0.7, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
    for f, a, b, bk_ in ((0, 0, 0, 0), (34, 0, 0, -20), (58, 0, 0, -20), (72, 0, 0, 0), (96, 20, 20, 0), (124, 20, 20, 0),
                         (130, 0, 0, 0), (138, 0, -30, 0), (141, 0, 0, 0), (150, 0, 0, 0)):
        ears(k, f, a, b, bk_)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        u = st(f)
        for leg in LEGS4:
            T = Vector((k.J[leg].x, k.J[leg].y, 0.0))
            if leg[4] == "F":
                T.y -= 0.22 * u
                T.z = 0.03 * math.sin(math.pi * u) if f < 46 else 0.0
            k.solve_leg(leg, f, T)
    k.finish()
    k.meta["planted"] = ["Leg_BL", "Leg_BR"]


def walk(k):
    n = 32

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.6 * pk.wave(f, n, 0.1, 2), 1.5 * pk.wave(f, n, 0.0), 1.5 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.04 - 0.015 * b))
        k.key("Chest", f, rot=(3, -2 * pk.wave(f, n, 0.25), -3 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(8, 0, 0))
        k.key("Head", f, rot=(-6, 2 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        ears(k, f, 6)
        tail(k, f, n, sway=10, lift=-4, cycles=1)
    return cm.quad_walk(k, n, 0.17, 0.09, body, gait="walk")


def roar(k):
    """HISS: the back arches up high (rump and shoulders drop), head low and forward, ears pinned flat, jaw wide with
    the fangs bared, the tail shoots straight up; holds and hisses, then smooths back down."""
    n = 66
    k.new_action("roar", n, False)
    for f, z, sp, ch, nk, h, jw, tl, eb in ((0, 0, 0, 0, 0, 0, 0, 0, 0), (10, -0.04, 4, 6, 4, 4, 2, 10, -10),
                                            (20, 0.05, -10, 14, 14, -10, 38, 70, -60), (46, 0.05, -10, 14, 14, -12, 40, 72, -60),
                                            (56, 0.0, -2, 2, 2, -2, 4, 20, -10), (66, 0, 0, 0, 0, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(h, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        ears(k, f, 0, 0, eb)
        k.key("Tail1", f, rot=(tl, 0, 0))
        for i, bn in enumerate(TAIL[1:]):
            k.key(bn, f, rot=(tl * 0.12, 0, 0))
    for f in range(22, 46, 2):
        k.key("Jaw", f, rot=(39 + (2 if (f // 2) % 2 else -2), 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def pounce(k):
    """SIGNATURE - STALK & POUNCE: sinks into a low stalk (front paws creep in slow motion, eyes locked), the butt
    wiggle, then LEAPS forward through the air (front paws reaching, hind legs trailing), lands, pins and bites, and
    springs back to its spot."""
    import bpy
    n = 116
    k.new_action("act_pounce", n, False)
    D = 0.42                                   # pounce distance

    def body(f):
        """(y, z, pitch) of the body"""
        if f <= 12:
            u = (0.5 - 0.5 * math.cos(math.pi * f / 12))
            return 0.0, -0.22 * u, 4 * u
        if f <= 44:
            return 0.0, -0.22, 4
        if f <= 48:
            u = (f - 44) / 4
            return -0.04 * u, -0.22 - 0.06 * u, 6
        if f <= 62:
            u = (f - 48) / 14
            return -D * u, -0.28 + (0.28 - 0.10) * u + 0.62 * math.sin(math.pi * u), -14 * math.cos(math.pi * u)
        if f <= 68:
            u = (f - 62) / 6
            return -D, -0.10 - 0.10 * math.sin(math.pi * u), 10
        if f <= 82:
            return -D, -0.12, 10
        if f <= 94:
            u = (f - 82) / 12
            return -D * (1 - u), -0.12 + 0.12 * u + 0.18 * math.sin(math.pi * u), 6 * (1 - u)
        if f <= 100:
            u = (f - 94) / 6
            return 0.0, -0.06 * math.sin(math.pi * u), 0
        return 0.0, 0.0, 0.0

    body0 = body

    def body(f):                              # heights scaled to the shorter (bible) legs
        y, z, p = body0(f)
        return y, 0.65 * z, p

    for f in range(0, n + 1):
        y, z, p = body(f)
        wig = 7 * math.sin(2 * math.pi * (f - 30) / 5) if 30 <= f <= 44 else 0.0
        k.key("Spine", f, rot=(p, wig, wig * 0.4), loc=(0, y, z))
    for f, nk, h, jw in ((0, 0, 0, 0), (12, 12, -8, 0), (44, 12, -8, 0), (48, 8, -10, 10), (54, -6, -10, 34), (62, 8, 6, 30),
                         (66, 14, 16, 0), (72, 14, 18, 20), (75, 14, 16, 0), (82, 6, 4, 0), (94, 0, 0, 0), (n, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(h, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
    for f in range(0, n + 1, 2):
        lift = -10 if f < 46 else (30 if f < 64 else 0)
        tw = 22 * math.sin(2 * math.pi * f / 6) if 14 <= f <= 44 else 0.0
        tail(k, f, n, sway=4, lift=lift, cycles=3, twitch=tw)
        ears(k, f, 22 if f < 62 else 0, None, -20 if 46 <= f <= 62 else 0)
    k.bake_bezier_now()
    sc = bpy.context.scene

    def creep(leg, f):
        """slow-motion creeping steps of the front paws while stalking"""
        if leg not in ("Leg_FL", "Leg_FR") or not 14 <= f <= 40:
            return 0.0
        ph = 0.0 if leg == "Leg_FL" else 0.5
        u = ((f - 14) / 26 + ph) % 1.0
        return 0.05 * math.sin(math.pi * u / 0.4) if u < 0.4 else 0.0

    for f in range(0, n + 1):
        sc.frame_set(f)
        y, z, p = body(f)
        for leg in LEGS4:
            fr = leg[4] == "F"
            T = Vector((k.J[leg].x, k.J[leg].y, creep(leg, f)))
            if 48 < f < 62:                                         # airborne: front reach forward, hind trail
                u = (f - 48) / 14
                T = Vector((k.J[leg].x, k.J[leg].y + y + (-0.18 if fr else 0.15) * math.sin(math.pi * u),
                            max(0.0, z + 0.14 + (0.10 if fr else 0.01) * math.sin(math.pi * u))))
            elif 62 <= f <= 82:
                T = Vector((k.J[leg].x, k.J[leg].y - D, 0.0))
                if fr and 66 <= f <= 74:                            # pin: paws press and pump
                    T.z = 0.03 * abs(math.sin(math.pi * (f - 66) / 4))
            elif 82 < f < 94:                                       # spring back (airborne)
                u = (f - 82) / 12
                T = Vector((k.J[leg].x, k.J[leg].y + y, max(0.0, z + 0.06 * math.sin(math.pi * u))))
            k.solve_leg(leg, f, T)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    pounce(k)
    return stride


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    P.append(("Head", "Chest"))
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR"):
        P.append(("Tail1", b))
        P.append(("Tail2", b))
    return P
