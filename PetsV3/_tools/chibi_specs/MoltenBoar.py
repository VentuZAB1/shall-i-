# Molten Boar (Magma egg #1, tier 4): a massive volcanic boar rebuilt to STYLE_BIBLE.md (2026-10-08 pro pass) as
# ARMOUR-OVER-CORE (ref_17): an orange magma body (no Neon: plain orange) under rock armour shells on the back,
# shoulders, head and thighs, orange showing on the belly, lower flanks and legs; a wedge build (big head and high
# shoulders, the back sloping down to small hips), short chunky legs on dark split hooves, big upturned ivory tusks, a
# flat snout pad, fierce rock-socket eyes, a laid-back crest of 7 two-tone rock spikes with orange tips, a flame tail.
# Own moves: idle = snuffles and roots the ground with its snout, lifts its head and SNORTS (crest flares); walk =
# heavy trot; roar = SQUEAL-ROAR (head up, jaw wide, crest erupting); signature = LAVA WALLOW (kneels, flops on its
# side, rolls onto its back kicking its legs in the air and wriggling in the lava mud, rolls back and springs up).
import math
from mathutils import Vector, Euler

DISPLAY = "Molten Boar"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 8.0

ROCK = (54, 46, 62)
ROCK_T = (90, 78, 98)
DARK = (30, 26, 34)
MAGMA = (255, 112, 32)
MAGMA_Y = (255, 192, 64)
TUSK = (250, 240, 222)
PAD = (150, 96, 96)
IRIS = (255, 184, 44)
MOUTH = (110, 26, 44)

# leg joints (left side): hip, knee, ankle
LEGS = {"FL": ((0.27, -0.36, 0.74), (0.27, -0.26, 0.42), (0.27, -0.36, 0.11)),     # knees set back: IK slack
        "BL": ((0.22, 0.38, 0.72), (0.22, 0.48, 0.42), (0.22, 0.38, 0.11))}
TH = 0.72
HEAD_FWD = 0.10        # head group sits this far forward of where it was modelled (room to nod / roar)
HEADB = ("Head", "Jaw", "Ear_L", "Ear_R")
EYE_RIM = DARK          # dark rock socket framing the light rim (None = no socket)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def crack(B, blk, s, pts, branch=None, w=0.075):
    """orange crack inlay on the +-x flank of a top-tapered block, following the taper.
    pts = [(y, z)] in the block's LOCAL frame (z from -h.z to +h.z); branch = (index, (y, z))"""
    hx, hz = blk.h.x, blk.h.z
    tk = 1 - blk.top[0]

    def P(y, z):
        t = (z + hz) / (2 * hz)
        return blk.world(Vector((s * (hx * (1 - tk * t) + 0.006), y, z)))

    n = (blk.R @ Vector((s, 0, hx * tk / (2 * hz)))).normalized()
    Q = [P(y, z) for y, z in pts]
    for a, b in zip(Q, Q[1:]):
        B.bar(a, b, n, w, 0.014, MAGMA, blk.bone, studs=[], bevel=0.008)
    if branch:
        i, (y, z) = branch
        B.bar(Q[i], P(y, z), n, w * 0.85, 0.014, MAGMA, blk.bone, studs=[], bevel=0.008, top=(1, 0.25))


def spike2(B, base, d, L, w, bone, col=ROCK_T, tip=MAGMA):
    """two-tone crest fin-spike laid back along the spine: long base along the back, thin across, pointed; the last
    35 % in orange"""
    import blockkit as bk
    d = Vector(d).normalized()
    base = Vector(base)
    for b0, ln, hx, hy, c, tp in ((base, L, w * 0.55, w, col, (0.30, 0.10)),
                                  (base + d * (0.60 * L), 0.42 * L, w * 0.40, w * 0.52, tip, (0.25, 0.08))):
        B.add(b0 + d * (ln / 2), (hx, hy, ln / 2), c, bone, R=bk.frame_from(b0, b0 + d, (1, 0, 0)), top=tp,
              studs=[], role="limb")


def socket(B, n0, color):
    """frame each light eye rim (added since item n0) with a dark rock socket"""
    import blockkit as bk
    rim = bk.rgb((232, 226, 255))
    for o in [b for b in B.items[n0:] if tuple(b.color) == tuple(rim)]:
        B.add(o.c + o.R @ Vector((0, o.h.y * 0.5, 0)), (o.h.x + 0.028, o.h.y * 0.6, o.h.z + 0.024), color, o.bone,
              R=o.R, top=o.top, studs=[], rnd=0.0, bevel=0.01)


def model(k):
    """STYLE_BIBLE MoltenBoar: armour-over-core wedge boar (see the header). No glow (embers/smoke = VFX)."""
    import blockkit as bk
    saved = {key: bk.STYLE[key] for key in ("relief", "mix", "mix2x2")}
    bk.STYLE.update(relief=0.42, mix=(0.40, 0.20, 0.40), mix2x2=0.30)       # chunky 2x1 / 2x2 rock slabs
    try:
        B = bk.Blocks(k, seed=101, tier=4, th=TH)
        D = 0.66
        # ---- torso: orange magma core under rock armour shells (chest shell 20 % bigger than the hips shell)
        B.add((0, -0.16, 0.84), (0.40, 0.42, 0.38), MAGMA, "Chest", bot=(0.92, 0.95), density=0.40)
        armc = B.add((0, -0.18, 1.07), (0.45, 0.46, 0.27), ROCK, "Chest", top=(0.92, 0.92), density=D)
        B.add((0, 0.30, 0.78), (0.32, 0.30, 0.30), MAGMA, "Spine", bot=(0.92, 0.95), density=0.40)
        armh = B.add((0, 0.33, 0.95), (0.36, 0.31, 0.19), ROCK, "Spine", rot=(-8, 0, 0), top=(0.92, 0.92), density=D)
        for s in (1, -1):        # lava cracks running down the chest shell into the orange core (local coords)
            crack(B, armc, s, ((-0.15, 0.19), (-0.05, 0.07), (-0.14, -0.05), (-0.04, -0.21)))
        # neck (hidden bridge between chest and head)
        B.add((0, -0.72, 0.87), (0.42, 0.16, 0.25), ROCK, "Neck", studs=[])
        # ---- head: HW 0.94 (1.04 TW), HH 0.70, wedge snout with a flat pad, tusks, fierce rock-socket eyes
        head = B.add((0, -1.00, 0.90), (0.47, 0.30, 0.35), ROCK, "Head", top=(0.86, 0.94), density=D,
                     studs=["+x", "-x", "+z", "+y"])
        snout = B.add((0, -1.37, 0.71), (0.30, 0.23, 0.15), ROCK, "Head", top=(0.88, 1.0), studs=[], role="limb")
        B.on_face(snout, "-y", 0, -0.005, 0.245, 0.115, 0.02, PAD)
        for s in (1, -1):
            B.on_face(snout, "-y", s * 0.10, -0.01, 0.048, 0.065, 0.036, DARK)
        B.add((0, -1.56, 0.565), (0.23, 0.04, 0.012), MOUTH, "Head", studs=[], bevel=0.006)          # mouth line
        B.add((0, -1.26, 0.53), (0.27, 0.26, 0.07), ROCK, "Jaw", bot=(0.85, 0.9), role="limb", studs=[])
        B.add((0, -1.28, 0.602), (0.22, 0.20, 0.006), MOUTH, "Jaw", studs=[], bevel=0.004)
        B.add((0, -1.33, 0.612), (0.10, 0.14, 0.012), (236, 110, 140), "Jaw", studs=[], bevel=0.006)      # tongue
        B.add((0, -1.36, 0.552), (0.25, 0.20, 0.006), MOUTH, "Head", studs=[], bevel=0.004)            # mouth roof
        for s in (1, -1):                                                                             # lower teeth
            B.spike((s * 0.17, -1.49, 0.59), (0, 0, 1), 0.06, 0.02, TUSK, "Jaw", top=(0.3, 0.3), role="limb")
        for s in (1, -1):                                                         # upturned ivory tusks
            b0, b1 = Vector((s * 0.27, -1.46, 0.63)), Vector((s * 0.41, -1.60, 0.86))
            B.seg(b0, b1, 0.072, 0.072, TUSK, "Head", ext=0.05, top=(0.85, 0.85), studs=[], role="limb")
            B.spike(b1, (s * 0.12, 0.10, 1), 0.30, 0.062, TUSK, "Head", top=(0.18, 0.18), role="limb")
        n0 = len(B.items)
        B.face_eyes(head, "fierce", IRIS, base=ROCK, brow=ROCK_T, look=(0, 0.6), z=0.64, pupil_size=(0.085, 0.088),
                    hl_size=(0.06, 0.0), brow_spec=(0.32, 0.07, 22), hl_on_pupil=True)
        if EYE_RIM:
            socket(B, n0, EYE_RIM)
        # ears: pointed, laid out and back, lined with magma
        for s, side in ((1, "L"), (-1, "R")):
            R = Euler((math.radians(-30), math.radians(s * 48), math.radians(-s * 6)), "XYZ").to_matrix()
            root = Vector((s * 0.34, -0.84, 1.17))
            ear = B.add(root + R @ Vector((0, 0, 0.14)), (0.145, 0.05, 0.155), ROCK, "Ear_" + side, R=R,
                        top=(0.30, 0.5), studs=[], role="limb")
            B.add(ear.world((0, -0.052, -0.02)), (0.10, 0.01, 0.10), MAGMA, "Ear_" + side, R=R, top=(0.2, 1),
                  studs=[], bevel=0.008)
        # ---- crest: 5 laid-back two-tone spikes on the Mane bone (shoulders) + 2 smaller on the sloping hips
        back = Vector((0, math.sin(math.radians(52)), math.cos(math.radians(52))))
        for y, z, L, w in ((-0.55, 1.31, 0.36, 0.15), (-0.41, 1.31, 0.46, 0.18), (-0.26, 1.31, 0.42, 0.17),
                           (-0.10, 1.31, 0.34, 0.15), (0.06, 1.31, 0.28, 0.13)):
            spike2(B, (0, y, z), back, L, w, "Mane")
        for y, z, L, w in ((0.30, 1.09, 0.24, 0.12), (0.46, 1.06, 0.18, 0.10)):
            spike2(B, (0, y, z), back, L, w, "Spine")
        # ---- legs: rock thigh armour, orange magma shin, dark split hooves
        for s, side in ((1, "L"), (-1, "R")):
            for fb, x, y, th, sh, ht in (("F", 0.27, -0.36, (0.18, 0.19), (0.145, 0.155), (0.082, 0.20)),
                                         ("B", 0.22, 0.38, (0.16, 0.20), (0.13, 0.15), (0.074, 0.18))):
                leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
                X0 = s * x
                B.add((X0, y, 0.51), (th[0], th[1], 0.23), ROCK, leg, bot=(0.92, 0.92), density=D)
                B.add((X0, y - 0.01, 0.23), (sh[0], sh[1], 0.17), MAGMA, shin, density=0.45)
                for dx in (-1, 1):
                    B.add((X0 + dx * (ht[0] + 0.006), y - 0.03, 0.055), (ht[0], ht[1], 0.055), DARK, foot,
                          studs=[], role="limb")
        # ---- tail: rock root + a flat orange flame point
        B.seg((0, 0.58, 0.95), (0, 0.74, 1.04), 0.075, 0.065, ROCK, "Tail1", ext=0.04, studs=[], role="limb")
        B.seg((0, 0.73, 1.03), (0, 0.80, 1.27), 0.035, 0.10, MAGMA, "Tail2", top=(1, 0.12), studs=[], role="limb")
        for blk in B.items:
            if blk.bone in HEADB:
                blk.c = blk.c + Vector((0, -HEAD_FWD, 0))
        B.build()
    finally:
        bk.STYLE.update(saved)
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.28, 0.84), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.08, 0.86), "Spine", tail=(0, -0.4, 0))
    k.joint("Mane", (0, 0.14, 1.30), "Chest", tail=(0, 0, 0.3))
    k.joint("Neck", (0, -0.56, 0.88), "Chest", tail=(0, -0.3, -0.05))
    k.joint("Head", (0, -0.74 - HEAD_FWD, 0.62), "Neck", tail=(0, -0.4, 0.0))          # throat pivot (low back of the head)
    k.joint("Jaw", (0, -1.06 - HEAD_FWD, 0.57), "Head", tail=(0, -0.3, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.33, -0.84 - HEAD_FWD, 1.18), "Head", tail=(s * 0.2, 0.1, 0.3))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, 1, 0))):   # carpus folds back
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.2, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", (0, 0.60, 0.96), "Spine", tail=(0, 0.16, 0.08))
    k.joint("Tail2", (0, 0.74, 1.04), "Tail1", tail=(0, 0.06, 0.2))


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]


def ears(k, f, a=0.0, b=None):
    b = a if b is None else b
    k.key("Ear_L", f, rot=(a, 0, 0))
    k.key("Ear_R", f, rot=(b, 0, 0))


def tail(k, f, n, amp=14.0, curl=0.0, cycles=3):
    k.key("Tail1", f, rot=(curl, amp * pk.wave(f, n, 0, cycles), 0))
    k.key("Tail2", f, rot=(curl * 0.6, amp * 1.3 * pk.wave(f, n, 0.15, cycles), 0))


def idle(k):
    """snuffles along the ground: head low, quick sniffs, roots twice with the snout, lifts the head and SNORTS (body
    jolts, mane flares), ear flicks, tail twirls."""
    n = 140
    k.new_action("idle", n, True)
    def env(f):          # rooting envelope: the whole front end tips down (head never swings back into the chest)
        if 10 <= f <= 20:
            return 0.5 - 0.5 * math.cos(math.pi * (f - 10) / 10)
        if 20 < f < 76:
            return 1.0
        if 76 <= f <= 86:
            return 0.5 + 0.5 * math.cos(math.pi * (f - 76) / 10)
        return 0.0

    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 4)
        k.key("Spine", f, rot=(3 * env(f), 0, 0), loc=(0, 0, 0.01 * b - 0.02 * env(f)))
        k.key("Chest", f, rot=(-0.8 * b + 5 * env(f), 0, 0))
        tail(k, f, n, amp=16, cycles=5)
    sniff = lambda f: 2.5 * math.sin(2 * math.pi * f / 5)
    rows = [(0, 0, 0, 0, 0)]
    for f in range(14, 60, 2):
        rows.append((f, 2, 6 + sniff(f), 0, 0))
    rows += [(62, 4, 10, 0, 0), (66, 2, 4, 0, 0), (70, 4, 10, 0, 0), (74, 2, 4, 0, 0), (82, 0, 0, 0, 0),
             (90, -8, -12, 8, 0), (93, -4, -6, 2, 0), (100, -6, -8, 0, 0), (112, 0, 0, 0, 0), (140, 0, 0, 0, 0)]
    for f, nk, hd, jw, _ in rows:
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
    for f, mp in ((0, 0), (86, 0), (90, -16), (100, -10), (112, 0), (140, 0)):
        k.key("Mane", f, rot=(mp, 0, 0), loc=(0, 0, 0))
    for f, a, b in ((0, 0, 0), (30, 0, 0), (32, -30, 0), (35, 0, 0), (96, 0, 0), (98, 0, -30), (101, 0, 0), (140, 0, 0)):
        ears(k, f, a, b)
    for f, z in ((88, 0), (90, 0.03), (93, -0.01), (98, 0)):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    n = 24

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 1.5 * pk.wave(f, n, 0.0), 2.0 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.03 * b))
        k.key("Chest", f, rot=(0, -2 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(6 + 3 * pk.wave(f, n, 0.1, 2), 0, 0))
        k.key("Head", f, rot=(6 - 2 * pk.wave(f, n, 0.2, 2), 2 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        k.key("Mane", f, rot=(-3 * pk.wave(f, n, 0.3, 2), 0, 2 * pk.wave(f, n, 0.3)))
        ears(k, f, 8 * pk.wave(f, n, 0.2, 2))
        tail(k, f, n, amp=10, curl=6, cycles=2)
    return cm.quad_walk(k, n, 0.15, 0.09, body, gait="trot")


def roar(k):
    """SQUEAL-ROAR: drops the head, then throws it up and forward with the jaw wide and tusks bared, the mane erupts
    up and back, ears pinned, tail straight up."""
    n = 64
    k.new_action("roar", n, False)
    for f, ch, nk, hd, jw, mp, el, tl in ((0, 0, 0, 0, 0, 0, 0, 0), (12, 2, 8, 10, 2, 4, 0, -10),
                                          (22, -6, -14, -12, 32, -34, 40, 50), (46, -6, -16, -12, 34, -36, 40, 50),
                                          (54, 0, -4, 0, 6, -8, 10, 10), (64, 0, 0, 0, 0, 0, 0, 0)):
        k.key("Chest", f, rot=(ch, 0, 0))
        t = 1.0 if 22 <= f <= 46 else 0.0
        k.key("Neck", f, rot=(nk, 0, 0), loc=(0, -0.10 * t, 0.08 * t))          # throws the head up AND forward
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Mane", f, rot=(mp, 0, 0))
        ears(k, f, el)
        k.key("Tail1", f, rot=(tl, 0, 0))
        k.key("Tail2", f, rot=(tl * 0.5, 0, 0))
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, -0.03 * (12 <= f <= 46)))
    for f in range(24, 46, 2):
        k.key("Jaw", f, rot=(33 + (3 if (f // 2) % 2 else -3), 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def wallow(k):
    """SIGNATURE - LAVA WALLOW: kneels, flops onto its left side, rolls onto its back and kicks all four legs in the air
    while wriggling its back in the lava mud (squealing), rolls back onto its side, springs up and SNORTS, mane
    flaring."""
    import bpy
    n = 124
    k.new_action("act_wallow", n, False)
    # body: (f, z, roll, yaw, pitch)
    rows = [(0, 0, 0, 0, 0), (10, -0.16, 0, 0, 8), (16, -0.24, 30, 0, 4), (24, -0.33, 90, 0, 0), (34, -0.28, 178, 0, 0)]
    for f in range(38, 72, 4):
        rows.append((f, -0.28, 178 + (4 if (f // 4) % 2 else -4), 10 * math.sin(2 * math.pi * (f - 38) / 16), 0))
    rows += [(74, -0.28, 178, 0, 0), (84, -0.33, 90, 0, 0), (92, -0.20, 20, 0, 6), (98, -0.10, 0, 0, 4),
             (104, 0.03, 0, 0, -4), (110, 0, 0, 0, 0), (124, 0, 0, 0, 0)]
    for f, z, r, y, p in rows:
        k.key("Spine", f, rot=(p, y, r), loc=(0, 0, z))
    for f, nk, hd, jw, mz, mp in ((0, 0, 0, 0, 0, 0), (10, -8, -8, 0, 0, 0), (16, 0, 0, 0, -0.06, 0), (24, -10, -8, 0, -0.08, 0),
                                  (34, -10, -8, 20, -0.14, 0), (70, -10, -8, 24, -0.14, 0), (84, -8, -6, 0, -0.08, 0),
                                  (92, 0, 0, 0, -0.05, 0), (100, 0, 0, 0, 0, 0), (104, -10, -12, 16, 0, -18),
                                  (108, -8, -10, 2, 0, -10), (116, 0, 0, 0, 0, 0), (124, 0, 0, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Mane", f, rot=(mp, 0, 0), loc=(0, 0, mz))
    for f in range(40, 70, 3):
        k.key("Jaw", f, rot=(22 + (6 if (f // 3) % 2 else -6), 0, 0))
    for f in range(0, n + 1, 2):
        tail(k, f, n, amp=22 if 34 <= f <= 74 else 10, cycles=8)
        ears(k, f, 20 if 16 <= f <= 90 else 0)
    k.bake_bezier_now()
    sc = bpy.context.scene

    def fk_legs(f, kick):
        for leg in LEGS4:
            fr = leg[4] == "F"
            s = 1 if leg.endswith("L") else -1
            ph = (0.0 if fr else 0.5) + (0.0 if s > 0 else 0.25)
            w = math.sin(2 * math.pi * (f / 10 + ph)) * kick
            k.key(leg, f, rot=((-26 if fr else 26) + 18 * w, 0, -s * 8))
            k.key("Shin_" + leg[4:], f, rot=((30 if fr else -30) + 20 * w, 0, 0))
            k.key("Foot_" + leg[4:], f, rot=(10 * w, 0, 0))

    for f in range(0, n + 1):
        sc.frame_set(f)
        if f <= 14 or f >= 94:
            for leg in LEGS4:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
        elif 20 <= f <= 88 and f % 2 == 0:
            fk_legs(f, 1.0 if 34 <= f <= 74 else 0.35)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    wallow(k)
    return stride


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR"):
        P.append(("Tail2", b))
    P += [("Ear_L", "Mane"), ("Ear_R", "Mane"), ("Head", "Chest"), ("Mane", "Neck")]
    return P
