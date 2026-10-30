# Solar Lion (Celestial egg #1): a golden lion king rebuilt to STYLE_BIBLE.md (2026-10-08 pro pass): stocky golden
# body with cream muzzle, paws and bib, bold amber eyes under brown 10 deg brows, a sun emblem on the forehead, a
# two-ring SUN MANE (8 rounded orange blocks round the face + TWELVE gold rays with pale tips, each on its own bone
# under a "Rays" wheel bone carried by the head) and a flat sun-shaped tail tuft.
# Own moves: idle = SITS DOWN on its haunches like a king, surveys, tail swishing on the ground, stands back up;
# walk = majestic shoulder-rolling walk; roar = LION ROAR (head thrust forward, jaw wide, the ray wheel spinning);
# signature = SUNBURST (chest out, chin high, the twelve rays shoot outward and spin a full turn, then snap back).
import math
from mathutils import Vector, Euler

DISPLAY = "Solar Lion"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 9.0

FUR = (240, 180, 70)          # gold fur
CREAM = (255, 236, 190)       # muzzle, bib, socks, paws, ear inners
BROWN = (120, 60, 30)         # nose, brows, tail tuft, toe grooves
LINE = (82, 40, 24)           # mouth line
MANE = (255, 140, 40)         # inner mane ring
RAY = (255, 214, 80)          # sun rays
RAY_T = (255, 248, 200)       # ray tips
IRIS = (230, 120, 20)
MOUTH = (150, 50, 46)
TONGUE = (236, 110, 140)
FANG = (250, 246, 236)
SHEEN = (250, 248, 240)

# hip, knee, ankle (left side): legs 0.65 TH x 0.38 TW, knees slightly bent so the 2-bone IK has slack
LEGS = {"FL": ((0.22, -0.36, 0.74), (0.22, -0.47, 0.38), (0.22, -0.36, 0.12)),
        "BL": ((0.17, 0.36, 0.72), (0.17, 0.47, 0.37), (0.17, 0.36, 0.12))}
HC = Vector((0, -1.10, 1.24))          # cranium centre (HW 0.80 = 0.95 TW, HH 0.60 = 0.85 TH)
RC = Vector((0, -0.99, 1.24))          # centre of the sun-ray wheel (mid-depth of the head, in front of the chest)
NR = 12
TAILP = [(0, 0.60, 0.98), (0, 0.86, 0.90), (0, 1.04, 0.66), (0, 1.10, 0.42)]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def ray_dir(i):
    a = 2 * math.pi * i / NR
    return Vector((math.sin(a), 0, math.cos(a)))


def inlay(B, blk, u, v, hu, hv, thick, color, ang=0.0, key="-y", **kw):
    """flush plate on the front (-y) or top (+z) face of a block whose face is flat there, rotated `ang` deg"""
    if key == "-y":
        loc = Vector((u, -(blk.h.y + thick / 2 + 0.002), v))
        half, rot = (hu, thick / 2, hv), Euler((0, math.radians(ang), 0), "XYZ")
    else:
        loc = Vector((u, v, blk.h.z + thick / 2 + 0.002))
        half, rot = (hu, hv, thick / 2), Euler((0, 0, math.radians(ang)), "XYZ")
    kw.setdefault("studs", [])
    kw.setdefault("bevel", min(0.012, thick * 0.6))
    return B.add(blk.world(loc), half, color, blk.bone, R=blk.R @ rot.to_matrix(), **kw)


def model(k):
    """STYLE_BIBLE SolarLion (T6 Celestial, quad majestic): stocky one-piece torso (chest 20 % bigger than the
    hips), legs 0.65 TH x 0.38 TW with cream socks and big cream paws, a big head (HW 0.95 TW) with bold amber eyes,
    10 deg brown brows, a sun emblem, a broad cream muzzle, brown nose, "w" mouth and 2 small fangs; the two-ring
    sun mane (8 rounded orange blocks + 12 gold rays alternating long / short, pale tips) and a flat sun tail tuft.
    No glow (sparkles = particle VFX in Studio)."""
    import blockkit as bk
    B = bk.Blocks(k, seed=151, tier=6)
    D = 0.62
    # ---- one torso: chest 20 % bigger than the hips in W and H, 43 % overlap
    chest = B.add((0, -0.20, 0.81), (0.42, 0.42, 0.35), FUR, "Chest", bot=(0.90, 0.95), density=0.7)
    B.add((0, 0.27, 0.78), (0.35, 0.36, 0.29), FUR, "Spine", bot=(0.88, 0.92), density=0.7)
    # cream belly band under the chest and a cream V bib on the chest front (flush, follows the taper)
    B.on_face(chest, "-z", 0, 0.02, 0.30, 0.34, 0.012, CREAM)
    nf = Vector((0, -0.42, -0.0147)).normalized()
    def chest_front(z):
        return Vector((0, -0.20 - 0.42 * (0.95 + 0.05 * (z - 0.46) / 0.70) - 0.008, z))
    B.bar(chest_front(0.54), chest_front(1.02), nf, 0.46, 0.012, CREAM, "Chest", bot=(1, 0.3), studs=[], rnd=0.3)
    # ---- neck bridging the chest front-top and the back of the head (mostly behind the mane)
    B.seg((0, -0.50, 0.96), (0, -0.92, 1.14), 0.30, 0.22, FUR, "Neck", side=(1, 0, 0), ext=0.04, studs=["+x", "-x"])
    # ---- head: cranium HW 0.80, HH 0.60, faces -y
    head = B.add(HC, (0.40, 0.26, 0.30), FUR, "Head", top=(0.94, 1.0), density=D, studs=["+x", "-x", "+z"])
    # broad cream muzzle (0.58 HW x 0.45 HH, protrudes 0.17, buried 35 %), brown nose with sheen
    muz = B.add(HC + Vector((0, -0.30, -0.205)), (0.23, 0.13, 0.135), CREAM, "Head", top=(0.88, 1.0), role="limb",
                studs=[])
    B.add(HC + Vector((0, -0.44, -0.10)), (0.08, 0.04, 0.048), BROWN, "Head", top=(0.85, 1.0), studs=[], role="limb")
    B.add(HC + Vector((-0.04, -0.482, -0.083)), (0.014, 0.004, 0.012), SHEEN, "Head", studs=[], bevel=0.004)
    # closed "w" mouth (philtrum + 2 bars) and 2 small fangs
    inlay(B, muz, 0, 0.005, 0.009, 0.03, 0.008, LINE)
    for s in (1, -1):
        inlay(B, muz, s * 0.042, -0.032, 0.040, 0.009, 0.008, LINE, ang=-s * 22)
        B.spike(HC + Vector((s * 0.085, -0.425, -0.33)), (0, 0, -1), 0.07, 0.02, FANG, "Head")
    B.add(HC + Vector((0, -0.29, -0.343)), (0.20, 0.11, 0.006), MOUTH, "Head", studs=[], bevel=0.004)
    # lower jaw / chin (opens in the roar) with a tongue
    B.add(HC + Vector((0, -0.29, -0.385)), (0.19, 0.12, 0.045), CREAM, "Jaw", bot=(0.85, 0.9), role="limb")
    B.add(HC + Vector((0, -0.29, -0.338)), (0.16, 0.10, 0.004), MOUTH, "Jaw", studs=[], bevel=0.003)
    B.add(HC + Vector((0, -0.31, -0.334)), (0.08, 0.06, 0.004), TONGUE, "Jaw", studs=[], bevel=0.003)
    # bold amber eyes (pupil 64 % of the iris height, 1 glint on the pupil), brown 10 deg brows
    B.face_eyes(head, "bold", IRIS, base=FUR, brow=BROWN, z=0.55, brow_spec=(0.26, 0.055, 10), look=(0.0, -0.2),
                pupil_size=(0.11, 0.135), hl_size=(0.07, 0.0), hl_on_pupil=True)    # 1 glint ON the pupil
    # sun emblem on the forehead: orange diamond with a pale inner diamond (flush)
    inlay(B, head, 0, 0.175, 0.052, 0.052, 0.012, MANE, ang=45)
    inlay(B, head, 0, 0.175, 0.026, 0.026, 0.018, RAY_T, ang=45)
    # round ears in front of the mane, cream lined
    for s in (1, -1):
        ear = B.add(HC + Vector((s * 0.27, -0.10, 0.33)), (0.10, 0.055, 0.085), FUR, "Head", rot=(0, s * 14, 0),
                    top=(0.70, 0.8), studs=[], role="limb")
        B.add(ear.world((0, -0.057, -0.01)), (0.065, 0.008, 0.055), CREAM, "Head", R=ear.R, top=(0.7, 1),
              studs=[], bevel=0.006)
    # ---- sun mane, ring 1: 8 rounded orange blocks round the back edge of the head (all on the Head bone)
    for i in range(8):
        a = math.radians(22.5 + 45 * i)
        dr = Vector((math.sin(a), 0, math.cos(a)))
        low = max(0.0, -dr.z)                       # tuck the chin blocks in (clear of the chest + front legs)
        r = 0.46 - 0.06 * low
        B.add(RC + dr * r + Vector((0, 0.02 * low, 0)), (0.21 - 0.03 * low, 0.13, 0.17 - 0.03 * low), MANE, "Head",
              rot=(0, math.degrees(a), 0), studs=["-y", "+z"], density=0.55)
    # ---- ring 2: twelve flat gold rays (long / short) with pale tips, each on its own bone
    for i in range(NR):
        d = ray_dir(i)
        low = max(0.0, -d.z)
        ln = (0.58 if i % 2 == 0 else 0.42) * (1 - 0.45 * low)
        w = (0.15 if i % 2 == 0 else 0.12) * (1 - 0.45 * low)
        base = RC + d * 0.50
        a = math.degrees(2 * math.pi * i / NR)
        ray = B.add(base + d * (ln / 2), (w, 0.06, ln / 2), RAY, "Ray%d" % (i + 1), rot=(0, a, 0), top=(0.10, 0.55),
                    studs=[], role="limb")
        B.add(ray.world((0, 0, ln * 0.27)), (w * 0.50, 0.066, ln * 0.23), RAY_T, "Ray%d" % (i + 1), R=ray.R,
              top=(0.12, 0.6), studs=[], role="limb")
    # ---- legs: upper block + flush shin, cream sock band, big cream paw with 2 brown toe grooves
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            hw, hd = (0.16, 0.16) if fb == "F" else (0.135, 0.16)
            B.seg(H - Vector((0, 0, 0.02)), K, hw, hd, FUR, leg, ext1=0.06, bot=(0.92, 0.92), density=D)
            sw, sd = hw * 0.92, hd * 0.92
            B.seg(K, A, sw, sd, FUR, shin, ext=0.05, ext1=0.02, density=D)
            dn = (A - K).normalized()
            B.seg(A - dn * 0.12, A + dn * 0.02, sw * 1.03, sd * 1.03, CREAM, shin, studs=[], role="limb")
            paw = B.add(A + Vector((0, -0.035, -0.066)), (hw * 1.12, hd * 1.2, 0.056), CREAM, foot, studs=[],
                        role="limb", top=(0.95, 0.92))
            for gx in (-0.33, 0.33):
                B.add(paw.world((gx * hw * 1.12, -hd * 1.2 - 0.002, 0.004)), (0.008, 0.006, 0.040), BROWN, foot,
                      studs=[], bevel=0.003)
                B.add(paw.world((gx * hw * 1.12, -hd * 0.6, 0.056 + 0.002)), (0.008, hd * 0.6, 0.006), BROWN, foot,
                      studs=[], bevel=0.003)
    # ---- tail: tapering gold tail and a FLAT sun-shaped brown tuft (8 short rays in the side-view plane)
    P = [Vector(p) for p in TAILP]
    for i, (a, b) in enumerate(zip(P, P[1:])):
        w = (0.10, 0.08, 0.065)[i]
        B.seg(a, b, w, w, FUR, "Tail%d" % (i + 1), ext=0.05, studs=[], role="limb")
    tip = P[3] + Vector((0, 0.04, -0.08))
    B.add(tip, (0.075, 0.12, 0.12), BROWN, "Tail3", rot=(45, 0, 0), studs=[], role="limb")
    for j in range(8):
        a = 2 * math.pi * j / 8 + math.pi / 8
        dv = Vector((0, math.sin(a), math.cos(a)))
        ln = 0.14 if j % 2 == 0 else 0.10
        B.spike(tip + dv * 0.09, dv, ln, 0.05, BROWN, "Tail3", side=(1, 0, 0), top=(0.7, 0.1))
        B.spike(tip + dv * (0.09 + ln * 0.55), dv, ln * 0.45, 0.04, RAY, "Tail3", side=(1, 0, 0), top=(0.8, 0.1))
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.40, 0.76), "Root", tail=(0, -0.4, 0))            # at the hips: sitting pivots here
    k.joint("Chest", (0, -0.02, 0.80), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.52, 0.98), "Chest", tail=(0, -0.3, 0.15))
    k.joint("Head", (0, -0.92, 1.00), "Neck", tail=(0, -0.35, 0))           # throat pivot
    k.joint("Jaw", tuple(HC + Vector((0, -0.17, -0.36))), "Head", tail=(0, -0.2, 0))
    k.joint("Rays", tuple(RC), "Head", tail=(0, -0.3, 0))                  # the sun wheel is carried by the head
    for i in range(NR):
        d = ray_dir(i)
        k.joint("Ray%d" % (i + 1), tuple(RC + d * 0.50), "Rays", tail=tuple(d * 0.25))
    for s, side in ((1, "L"), (-1, "R")):
        for fb, parent, knee in (("F", "Chest", (0, -1, 0)), ("B", "Spine", (0, 1, 0))):
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.2, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    for i in range(3):
        k.joint("Tail%d" % (i + 1), TAILP[i], "Spine" if i == 0 else "Tail%d" % i,
                tail=tuple(Vector(TAILP[i + 1]) - Vector(TAILP[i])))


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]


def wheel(k, f, spin=0.0, out=0.0):
    """spin = degrees the ray wheel has turned (about the forward axis); out = how far the rays have shot outward"""
    cm.key_axis(k, "Rays", f, (0, -1, 0), spin)
    for i in range(NR):
        k.key("Ray%d" % (i + 1), f, rot=(0, 0, 0), loc=tuple(ray_dir(i) * out))


def idle(k):
    """SITS DOWN like a king (haunches lower, chest high), surveys left and right with long holds, tail swishing along
    the ground, the sun wheel drifting slowly, then stands back up."""
    import bpy
    n = 170
    k.new_action("idle", n, True)

    def sit(f):
        if 16 <= f <= 36:
            return 0.5 - 0.5 * math.cos(math.pi * (f - 16) / 20)
        if 36 < f < 128:
            return 1.0
        if 128 <= f <= 148:
            return 0.5 + 0.5 * math.cos(math.pi * (f - 128) / 20)
        return 0.0

    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 5)
        u = sit(f)
        k.key("Spine", f, rot=(-20 * u, 0, 0), loc=(0, 0, 0.01 * b - 0.29 * u))
        k.key("Chest", f, rot=(-0.8 * b - 4 * u, 0, 0))
        sw = 16 * pk.wave(f, n, 0, 3) * (1 - 0.6 * u)
        k.key("Tail1", f, rot=(46 * u, sw - 34 * u, 0))           # sitting: tail laid out behind, curving to the left
        k.key("Tail2", f, rot=(12 * u, sw * 1.3 - 24 * u, 0))
        k.key("Tail3", f, rot=(10 * u, sw * 1.6 - 14 * u, 0))
        wheel(k, f, spin=8 * pk.wave(f, n, 0.2, 2), out=0.0)
    for f, nk, h, hy in ((0, 0, 0, 0), (16, 0, 0, 0), (36, 11, 4, 0), (54, 11, 4, 0), (62, 11, 4, 26), (84, 11, 4, 26),
                         (94, 11, 4, -26), (116, 11, 4, -26), (124, 11, 4, 0), (148, 0, 0, 0), (n, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, hy * 0.4, 0))
        k.key("Head", f, rot=(h, hy * 0.6, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    n = 34

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.6 * pk.wave(f, n, 0.1, 2), 1.5 * pk.wave(f, n, 0.0), 1.5 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.03 * b))
        k.key("Chest", f, rot=(0, -2 * pk.wave(f, n, 0.25), -3 * pk.wave(f, n, 0.25)))          # shoulder roll
        k.key("Neck", f, rot=(2 * pk.wave(f, n, 0.2, 2), 0, 0))
        k.key("Head", f, rot=(-2 * pk.wave(f, n, 0.3, 2), 2 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(6 + 3 * i, 10 * pk.wave(f, n, 0.3 + 0.12 * i), 0))
        wheel(k, f, spin=12 * pk.wave(f, n, 0.2, 2))
    return cm.quad_walk(k, n, 0.15, 0.11, body, gait="walk")


def roar(k):
    """LION ROAR: sinks onto its front, then thrusts the head forward and up with the jaw gaping, the sun wheel spinning
    a full fast turn behind its head; tail lashes; recovers."""
    n = 70
    k.new_action("roar", n, False)
    for f, ch, nk, h, jw, z in ((0, 0, 0, 0, 0, 0), (12, 6, 10, 12, 2, -0.04), (22, -4, -10, -12, 36, 0.0),
                                (48, -4, -12, -14, 38, 0.0), (58, 0, -2, -2, 6, 0), (70, 0, 0, 0, 0, 0)):
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(h, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
    for f in range(24, 48, 2):
        k.key("Jaw", f, rot=(37 + (3 if (f // 2) % 2 else -3), 0, 0))
    for f in range(0, n + 1, 2):
        u = min(1.0, max(0.0, (f - 18) / 34))
        wheel(k, f, spin=360 * (0.5 - 0.5 * math.cos(math.pi * u)), out=0.06 * math.sin(math.pi * u))
        lash = 24 * math.sin(2 * math.pi * f / 16) if 20 <= f <= 52 else 0.0
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(10 + 4 * i, lash * (0.6 + 0.3 * i), 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def sunburst(k):
    """SIGNATURE - SUNBURST: plants its paws, puffs the chest out and lifts its chin high; the twelve rays SHOOT outward
    and the blazing wheel spins a full turn, holds, the rays snap back in, a proud huff."""
    n = 96
    k.new_action("act_sunburst", n, False)
    for f, ch, nk, h, jw, z in ((0, 0, 0, 0, 0, 0), (12, 4, 6, 6, 0, -0.06), (24, -10, -18, -12, 6, 0.04),
                                (64, -10, -18, -12, 6, 0.04), (74, 2, -2, 0, 14, -0.02), (78, 0, 0, 0, 0, 0), (n, 0, 0, 0, 0, 0)):
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(h, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Spine", f, rot=(-4 * (24 <= f <= 64), 0, 0), loc=(0, 0, z))
    for f in range(0, n + 1):
        if f < 22:
            out, spin = 0.0, 0.0
        elif f <= 30:
            out, spin = 0.30 * math.sin(math.pi * (f - 22) / 16), 0.0
        elif f <= 62:
            u = (f - 30) / 32
            out, spin = 0.30 + 0.02 * math.sin(2 * math.pi * f / 6), 360 * (0.5 - 0.5 * math.cos(math.pi * u))
        elif f <= 70:
            out, spin = 0.30 * (1 - (f - 62) / 8) ** 2, 360.0
        else:
            out, spin = 0.0, 360.0
        wheel(k, f, spin=spin, out=out)
    for f in range(0, n + 1, 2):
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(8 + 4 * i + (14 if 24 <= f <= 64 else 0), 8 * pk.wave(f, n, 0.2 + 0.1 * i, 3), 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    sunburst(k)
    return stride


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    P.append(("Head", "Chest"))
    for i in range(NR):
        P.append(("Ray%d" % (i + 1), "Chest"))
    for i in (4, 5, 6, 7, 8):                       # lower rays pass in front of the front legs
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append(("Ray%d" % (i + 1), b))
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR"):
        P.append(("Tail2", b))
        P.append(("Tail3", b))
    return P


def joints():
    out = []
    for i in range(NR):
        p = RC + ray_dir(i) * 0.50
        out.append((p, p, 0.10, "Ray%d" % (i + 1)))
    return out
