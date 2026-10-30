# Wraith Hound (Void / Shadow egg, MEDIUM-HIGH 10 %) - FIERCE style (2026-10-27, Glacier update batch 1).
# Plan: _review/WraithHound_plan.md (v2) + review _review/GLACIER_PLAN_REVIEW.md 2.11.
# A ghost hound: lean deep-chested hound on long legs, lavender-ash studded hide, a solid soot saddle over the back
# (the upper layer of the torso blocks), a tall soot smoke mane in 3 rows of curling plumes that stream back and up
# (indigo tips), a long low tail stepping down to a soot tuft, a long flat wedge head with narrow indigo slit eyes
# under heavy soot brows, tall pinned-back ears, fangs. No glow (wisps / fog = VFX).
import math
import os
from mathutils import Vector, Euler

DISPLAY = "Wraith Hound"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 9.0                  # total height in studs at x1 (review 2 MUST 2: ties NightmareStallion's 9.0)

ASH_LAV = (158, 148, 198)     # body, legs, head (studded) - lavender-ash (9+: 170,160,206 -> a deeper lavender)
MIST = (226, 226, 236)        # underside, muzzle, chest, inside legs
SOOT = (92, 92, 116)          # spine saddle (>= 18 % side), mane, ears, tail tuft, brows - review MUST 2
INDIGO = (112, 120, 240)      # THE accent: eye slits, mane tip accents (smooth) - model review 1 M4 (off Raiju)
INDIGO_L = (200, 206, 255)    # eye rims (review 2 NICE 2: brighter so the eye reads at icon size)
WISP_ROOT = (128, 124, 166)   # final85 M1: mid-slate mane roots + middles (smoke over a lavender back)
BLACK = (14, 14, 22)          # nose, claws, pupils
IVORY = (238, 234, 220)       # fangs
MOUTH = (56, 28, 70)

PITCH = 0.034                 # ~0.08 x torso height

# leg joints (left side): shoulder/hip, elbow/knee, wrist/hock, paw centre (long hound legs)
LEGS = {"F": ((0.125, -0.42, 0.68), (0.130, -0.34, 0.42), (0.130, -0.40, 0.105), (0.130, -0.45, 0.040)),
        "B": ((0.125, 0.38, 0.72), (0.130, 0.24, 0.455), (0.130, 0.47, 0.205), (0.130, 0.42, 0.040))}
TAILP = [(0, 0.54, 0.84), (0, 0.74, 0.72), (0, 0.91, 0.54), (0, 1.02, 0.37), (0, 1.08, 0.24)]
HJ = Vector((0, -0.76, 0.95))           # throat (Head pivot)
# mane rows: (bone, parent, root, [(dir, length) x 3 segments], half width/depth at the root, side splay)
MANE = [("Mane1", "Neck", Vector((0, -0.635, 0.985)), 0.95),
        ("Mane2", "Chest", Vector((0, -0.40, 0.935)), 1.22),          # clip review 3 M2: roots +0.03 so the
        ("Mane3", "Spine", Vector((0, -0.13, 0.905)), 0.95)]          # rows' tips lie on one swept line


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def tdims(T, lz):
    t = (lz / T.h.z + 1) / 2
    return (T.h.x * (T.bot[0] + (T.top[0] - T.bot[0]) * t), T.h.y * (T.bot[1] + (T.top[1] - T.bot[1]) * t),
            T.ts[0] * t, T.ts[1] * t)


def upper(B, T, lz0, color, p=0.006, ky=1.0, cy=0.0, rnd_t=0.30):
    """the slab of block T above its local z = lz0, grown by p (a colour layer that follows T's own shape: the soot
    saddle). ky / cy shorten / shift it along T's local y."""
    x0, y0, ox0, oy0 = tdims(T, lz0)
    x1, y1, ox1, oy1 = tdims(T, T.h.z)
    hz = (T.h.z + p - lz0) / 2
    hx, hy = x0 + p, y0 * ky + p
    c = Vector((ox0, oy0 + cy, lz0 + hz))
    mnT = min(T.h.x * min(T.top[0], T.bot[0]), T.h.y * min(T.top[1], T.bot[1]), T.h.z)
    mnS = min(min(hx, x1 + p), min(hy, y1 * ky + p), hz)
    rnd = min(0.45, rnd_t * mnT / mnS)
    return B.add(T.world(c), (hx, hy, hz), color, T.bone, R=T.R, top=((x1 + p) / hx, (y1 * ky + p) / hy),
                 top_shift=(ox1 - ox0, oy1 - oy0), rnd=rnd)


def wisp(B, root, d0, d1, L0, L1, w, d, bone, side=(1, 0, 0), tipfrac=0.42, tipcol=INDIGO, body=None, tipw=None):
    """one smoke wisp of the mane: a fat rounded root rising steeply (d0, L0), bending back into a long tapering
    tail (d1, L1) that ends in an indigo point. Returns the tip."""
    root = Vector(root)
    m = root + Vector(d0).normalized() * L0
    q = m + Vector(d1).normalized() * L1
    j = m + (q - m) * (1 - tipfrac)
    body = body or WISP_ROOT                           # final85 M1: mid-slate roots + middles (was SOOT)
    if tipcol == INDIGO:                               # the indigo points carry the accent: a longer tip (>= 5 % game)
        tipfrac = 0.58                                 # (r2: 0.58 keeps game INDIGO >= 5 % with one blue line)
        j = m + (q - m) * (1 - tipfrac)
    B.seg(root, m, w, d, body, bone, side=side, top=(0.70, 0.70), ext=0.04, ext1=0.0, rnd=0.42)
    B.seg(m, j, w * 0.70, d * 0.70, body, bone, side=side, top=(0.62, 0.62), ext=0.035, ext1=0.0, rnd=0.42)
    tw = tipw or (0.85 if tipcol == INDIGO else 0.62)  # r2 M1: fatter indigo points (read at 64 px)
    B.seg(j, q, w * 0.70 * tw, d * 0.70 * tw, tipcol, bone, side=side, top=(0.10, 0.22), ext=0.01,
          studs=[], nostud=True, rnd=0.35)
    return q


def mane_row(B, bone, root, sc):
    """one mane row: a tall centre wisp (bone) + two side wisps splayed out (bone_L / bone_R, for the fan-out)"""
    out = {"C": wisp(B, root, (0, 0.85, 0.55), (0, 1.0, 0.36), 0.21 * sc, (0.44 if bone == "Mane2" else 0.36) * sc,
                     0.070 * sc, 0.088 * sc, bone, tipcol=(INDIGO if bone == "Mane2" else SOOT))}   # final85 M2
    wisp(B, root + Vector((0, 0.075, -0.012)), (0, 0.95, 0.42), (0, 1.0, 0.22), 0.14 * sc, 0.28 * sc, 0.058 * sc,
         0.072 * sc, bone, tipcol=SOOT)                      # back wisp (fills the side view; soot tip: review 3 M2)
    for s_, sd in ((1, "L"), (-1, "R")):
        r = root + Vector((s_ * 0.052, 0.035, -0.020))
        out[sd] = wisp(B, r, (s_ * 0.40, 0.85, 0.60), (s_ * 0.20, 1.0, 0.42), 0.19 * sc, 0.28 * sc, 0.056 * sc,
                       0.072 * sc, bone + "_" + sd, tipcol=(INDIGO if bone == "Mane2" else SOOT),
                       tipw=(1.0 if bone == "Mane2" else None))   # r2: one line; 9+: fatter Mane2 side tips
        wisp(B, root + Vector((s_ * 0.085, 0.06, -0.050)), (s_ * 0.75, 0.45, 0.80), (s_ * 0.35, 1.0, 0.0),
             0.10 * sc, 0.15 * sc, 0.046 * sc, 0.060 * sc, bone + "_" + sd, tipcol=SOOT, body=SOOT)   # outer-low
    return out


def lower(B, T, lz1, color, p=0.006, ky=1.0, cy=0.0, rnd_t=0.30):
    """the slab of block T below its local z = lz1, grown by p (a colour layer following T's shape: the mist belly)"""
    x0, y0, ox0, oy0 = tdims(T, -T.h.z)
    x1, y1, ox1, oy1 = tdims(T, lz1)
    hz = (lz1 - (-T.h.z - p)) / 2
    hx, hy = x0 + p, y0 * ky + p
    c = Vector((ox0, oy0 + cy, -T.h.z - p + hz))
    mnT = min(T.h.x * min(T.top[0], T.bot[0]), T.h.y * min(T.top[1], T.bot[1]), T.h.z)
    mnS = min(min(hx, x1 + p), min(hy, y1 * ky + p), hz)
    rnd = min(0.45, rnd_t * mnT / mnS)
    return B.add(T.world(c), (hx, hy, hz), color, T.bone, R=T.R, top=((x1 + p) / hx, (y1 * ky + p) / hy),
                 top_shift=(ox1 - ox0, oy1 - oy0), rnd=rnd)


def seg_cap(B, T, zcut, color):
    """soot cap on the upper (p0 = shoulder / hip) end of a leg seg block T, down to world height zcut"""
    z0 = T.world(Vector((0, 0, -T.h.z))).z
    z1 = T.world(Vector((0, 0, T.h.z))).z
    f = max(0.05, min(0.95, (z0 - zcut) / (z0 - z1)))
    return lower(B, T, -T.h.z + 2 * T.h.z * f, color)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=313, tier=3, plates=False)
    # ---------------- torso: deep narrow chest, strong sloped tuck, narrow waist, hips (lean hound)
    rib = B.add((0, -0.28, 0.685), (0.165, 0.30, 0.215), ASH_LAV, "Chest", bot=(0.62, 0.52), top=(0.86, 0.92),
                rnd=0.30)
    B.seg((0, -0.10, 0.505), (0, 0.27, 0.645), 0.105, 0.065, ASH_LAV, "Spine", top=(0.82, 0.75), side=(1, 0, 0))
    waist = B.add((0, 0.12, 0.775), (0.122, 0.20, 0.118), ASH_LAV, "Spine", bot=(0.72, 0.70), top=(0.95, 1),
                  rnd=0.30)
    hips = B.add((0, 0.38, 0.745), (0.140, 0.18, 0.150), ASH_LAV, "Spine", rot=(-8, 0, 0), top=(0.84, 0.90),
                 bot=(0.85, 0.9), rnd=0.30)
    # the SOOT saddle: the upper layer of each torso block (withers -> hips), a solid dark blanket >= 18 % side
    sad = (255, 0, 255) if os.environ.get("WH_SADDLEDBG") else SOOT      # debug colour = saddle-only share test
    SADDLE[0] = sad
    upper(B, rib, 0.043, sad, rnd_t=0.45)              # model review 1 M1: the top ~40 % of each block
    upper(B, waist, 0.024, sad, rnd_t=0.45)            # r2 T: rounder saddle tops (no dark plank in game_view)
    upper(B, hips, 0.030, sad, rnd_t=0.45)
    # mist underside following the tuck + a mist chest front
    lower(B, rib, -0.125, MIST, ky=0.86, cy=0.02)
    B.seg((0, -0.10, 0.498), (0, 0.24, 0.626), 0.100, 0.042, MIST, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03,
          rnd=0.45)
    B.add((0, -0.567, 0.66), (0.075, 0.046, 0.175), ASH_LAV, "Chest", bot=(0.40, 0.8), top=(0.95, 1), rot=(-14, 0, 0),
          rnd=0.50)                                     # clip review 3 NICE 5: thicker = a rounder plate
    # ---------------- neck (low and forward) + long flat wedge head (pivot at the throat)
    B.seg((0, -0.48, 0.78), (0, -0.74, 0.97), 0.105, 0.118, ASH_LAV, "Neck", ext=0.05)
    B.seg((0, -0.54, 0.71), (0, -0.78, 0.90), 0.075, 0.060, MIST, "Neck", side=(1, 0, 0), ext=0.02, rnd=0.45,
          top=(0.85, 0.85))                                                                  # mist throat (r2: round)
    B.add((0, -0.84, 1.035), (0.112, 0.105, 0.085), ASH_LAV, "Head", top=(0.86, 0.86), bot=(0.92, 0.95), rnd=0.38)
    B.add((0, -0.82, 1.118), (0.080, 0.080, 0.012), SOOT, "Head", top=(0.8, 0.8))                       # dark crown
    for s in (1, -1):                                                                       # lean cheeks
        B.add((s * 0.080, -0.88, 0.995), (0.040, 0.065, 0.045), ASH_LAV, "Head", rot=(0, 0, s * 8), rnd=0.40)
    B.seg((0, -0.92, 1.040), (0, -1.17, 1.010), 0.072, 0.055, ASH_LAV, "Head", top=(0.70, 0.78), ext=0.02)  # snout
    B.seg((0, -0.99, 0.985), (0, -1.168, 0.975), 0.069, 0.040, ASH_LAV, "Head", top=(0.76, 0.86), ext=0.01)  # muzzle
    for s in (1, -1):                                                                       # mist cheek / jowl
        B.add((s * 0.072, -0.910, 0.962), (0.028, 0.055, 0.018), MIST, "Head", rot=(0, 0, s * 8), rnd=0.40)
    B.add((0, -1.178, 1.032), (0.026, 0.018, 0.020), BLACK, "Head", bot=(0.7, 1), role="detail", bevel=0.007)  # nose
    for s in (1, -1):
        B.spike((s * 0.042, -1.115, 0.955), (0, -0.05, -1), 0.075, 0.014, IVORY, "Head")               # fangs
    # lower jaw (opens in the roar) + mouth
    B.seg((0, -0.86, 0.925), (0, -1.12, 0.922), 0.058, 0.022, MIST, "Jaw", top=(0.8, 1), ext=0.02)
    B.add((0, -1.00, 0.948), (0.046, 0.11, 0.006), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike((s * 0.036, -1.10, 0.940), (0, 0, 1), 0.040, 0.011, IVORY, "Jaw")
    # narrow indigo slit eyes: black socket, indigo-light rim, indigo slit, black slit pupil; heavy soot V brow
    for s in (1, -1):
        rot = (0, -s * 18, s * 16)
        c = Vector((s * 0.066, -0.942, 1.068))
        B.add(c, (0.052, 0.008, 0.028), BLACK, "Head", rot=rot, studs=[], role="detail", bevel=0.003)   # r2 M2
        B.add(c + Vector((0, -0.005, 0)), (0.047, 0.006, 0.024), INDIGO_L, "Head", rot=rot, studs=[],
              role="detail", bevel=0.002)
        B.add(c + Vector((0, -0.008, 0)), (0.042, 0.006, 0.022), INDIGO, "Head", rot=rot, studs=[],   # 9+: 0.022
              role="detail", bevel=0.002)
        B.add(c + Vector((-s * 0.004, -0.0125, -0.001)), (0.0060, 0.004, 0.0210), BLACK, "Head",
              rot=(0, 0, s * 16), studs=[], role="detail", bevel=0.0012)                    # slit pupil
        B.add(c + Vector((-s * 0.002, -0.006, 0.022)), (0.054, 0.020, 0.016), SOOT, "Head", rot=(0, -s * 22, s * 16),
              role="detail", bevel=0.006)                                                   # heavy V brow
    # tall pointed ears pinned back 12 deg: soot backs, lavender fronts
    for s, side in ((1, "L"), (-1, "R")):
        R = Euler((math.radians(-12 - 10), math.radians(s * 6), math.radians(-s * 10)), "XYZ").to_matrix()
        root = Vector((s * 0.068, -0.80, 1.105))
        ear = B.add(root + R @ Vector((0, 0, 0.080)), (0.040, 0.018, 0.085), SOOT, "Ear_" + side, R=R,
                    top=(0.12, 0.5), rnd=0.25)
        B.add(ear.world((0, -0.018, -0.010)), (0.026, 0.005, 0.060), ASH_LAV, "Ear_" + side, R=R, top=(0.15, 1),
              studs=[], role="detail", bevel=0.003)
    # ---------------- the smoke mane: 3 rows of curling soot plumes with indigo tips (blocks only)
    global MANE_TIPS
    MANE_TIPS = {}
    if not os.environ.get("WH_NOMANE"):
        B.seg((0, -0.71, 0.985), (0, -0.44, 0.915), 0.058, 0.040, SOOT, "Neck", side=(1, 0, 0), ext=0.02,
              top=(0.92, 1), rnd=0.45)                                                       # mane ridge
        for bone, parent, root, sc in MANE:
            MANE_TIPS[bone] = mane_row(B, bone, root, sc)
    else:
        MANE_TIPS = {m[0]: {"C": m[2]} for m in MANE}
    # ---------------- legs: muscled upper, long slim lower, narrow paws with 4 black claws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, Pw = (X(p, s) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                up = B.seg(H + Vector((-s * 0.006, 0.01, 0.04)), K, 0.050, 0.074, ASH_LAV, leg, ext=0.0,
                           ext1=0.03, top=(0.86, 0.72), rnd=0.45)
                B.seg(K, A, 0.054, 0.060, ASH_LAV, shin, top=(0.85, 0.85), ext=0.03, ext1=0.02, rnd=0.40)
                B.seg(A + (K - A) * 0.18, A, 0.050, 0.056, MIST, shin, ext1=0.02, rnd=0.40, top=(1.02, 1.02))  # sock
                B.seg(K + Vector((-s * 0.012, -0.012, -0.03)), A + Vector((-s * 0.012, 0, 0.03)), 0.030, 0.040,
                      MIST, shin, ext=0.0, rnd=0.40)                                        # mist inside leg
            else:
                up = B.seg(H + Vector((0, 0.03, 0.05)), K, 0.066, 0.112, ASH_LAV, leg, bot=(0.85, 1),
                           top=(0.75, 0.62), ext=0.0, ext1=0.03, rnd=0.45)
                B.seg(K, A, 0.056, 0.064, ASH_LAV, shin, top=(0.80, 0.80), ext=0.03, ext1=0.02, rnd=0.40)
                B.seg(A, Pw + Vector((0, 0.03, 0.025)), 0.049, 0.051, MIST, foot, ext=0.03, rnd=0.40)   # sock
            B.add(Pw, (0.054, 0.072, 0.036), MIST, foot, top=(0.86, 0.80), rnd=0.35)              # narrow paw
            for gx in (-0.030, -0.010, 0.010, 0.030):
                B.spike((Pw.x + gx, Pw.y - 0.062, 0.030), (0, -1, -0.55), 0.052, 0.010, BLACK, foot)
    # ---------------- long low tail: lavender root, three soot blocks stepping down to a soot tuft
    P = [Vector(p) for p in TAILP]
    for i, ((a, b), (w, d), tp) in enumerate(zip(zip(P, P[1:]), ((0.046, 0.056), (0.060, 0.070), (0.068, 0.078),
                                                                 (0.064, 0.074)), (1.15, 1.10, 0.95, 0.85))):
        B.seg(a, b, w, d, ASH_LAV if i < 3 else SOOT, "Tail%d" % (i + 1), ext=0.06 if i < 3 else 0.015, ext1=0.03,
              top=(tp, tp),                                      # the soot Tail4 must not poke through lavender Tail3
              rnd=0.45)                                                  # bushy smoke brush (thickest mid-tail)
    B.seg(P[4] - Vector((0, 0.05, -0.03)), P[4] + Vector((0, 0.07, -0.12)), 0.070, 0.080, SOOT, "Tail4",
          top=(0.30, 0.40), rnd=0.45)                                                       # soft tuft
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.20, 0.74), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.10, 0.74), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.48, 0.80), "Chest", tail=(0, -0.2, 0.15))
    k.joint("Head", tuple(HJ), "Neck", tail=(0, -0.30, 0.05))                 # throat pivot
    k.joint("Jaw", (0, -0.86, 0.935), "Head", tail=(0, -0.26, 0))
    k.joint("FX_Fog", (0, -0.56, 0.62), "Chest", tail=(0, -0.1, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.068, -0.80, 1.105), "Head", tail=(0, 0.05, 0.15))
        k.joint("FX_IndigoWisp_" + side, (s * 0.075, -0.955, 1.068), "Head", tail=(s * 0.03, -0.05, 0))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, Pw = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.12, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
            if fb == "F":
                k.joint("FX_SmokePuff_F" + side, (Pw.x, Pw.y, 0.01), "Foot_F" + side, tail=(0, 0, 0.05))
    for i, (bone, parent, root, sc) in enumerate(MANE):
        k.joint(bone, tuple(root), parent, tail=(0, 0.10, 0.15))
        for s, sd in ((1, "L"), (-1, "R")):
            k.joint(bone + "_" + sd, tuple(root + Vector((s * 0.040, 0.03, -0.02))), bone, tail=(s * 0.05, 0.08, 0.12))
        k.joint("FX_SmokeWisp_%d" % (i + 1), tuple(MANE_TIPS[bone]["C"]), bone, tail=(0, 0.06, 0.02))
    for i in range(4):
        k.joint("Tail%d" % (i + 1), TAILP[i], "Spine" if i == 0 else "Tail%d" % i,
                tail=tuple(Vector(TAILP[i + 1]) - Vector(TAILP[i])))
    k.joint("FX_SmokeTrail", TAILP[4], "Tail4", tail=(0, 0.05, -0.08))


MANE_TIPS = {}
SADDLE = [SOOT]


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR"), ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    P += [("Head", "Chest"), ("Jaw", "Chest"), ("Ear_L", "Ear_R")]
    for m in ("Mane1", "Mane1_L", "Mane1_R"):
        P += [(m, "Head"), (m, "Ear_L"), (m, "Ear_R")]
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR"):
        for t in ("Tail1", "Tail2", "Tail3"):
            P.append((t, b))
    return P


def joints():
    return [((0, -0.74, 0.92), (0, -0.80, 0.99), 0.14, "Head")]


HEAD_XF = []


# ------------------------------------------------------------------ animation (WraithHound/ANIM_REFS.md)
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
ROWS = ["Mane1", "Mane2", "Mane3"]
TAILB = ["Tail1", "Tail2", "Tail3", "Tail4"]
H_U = 1.27                       # model height in units (ear tips, HEIGHT 9.0 studs): 0.05H = 0.064
CROUCH = 0.20                    # act_smokecloak body drop (units)


def tab(T, f):
    """eased (smoothstep) interpolation through [(frame, value | tuple)]"""
    if f <= T[0][0]:
        return T[0][1]
    for (f0, v0), (f1, v1) in zip(T, T[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / (f1 - f0) if f1 > f0 else 1.0
            u = u * u * (3 - 2 * u)
            if isinstance(v0, tuple):
                return tuple(a + (b - a) * u for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * u
    return T[-1][1]


def ears(k, f, p=0.0, splay=0.0):
    """tall pinned ears: p = pitch (+ forward, - back), splay = outward roll"""
    k.key("Ear_L", f, rot=(p, 0, splay))
    k.key("Ear_R", f, rot=(p, 0, -splay))


def mane(k, f, lift, splay, sway):
    """the smoke mane, row by row (lists of 3, Mane1 = the front row): lift = pitch (+ = the plumes rise),
    splay = the side wisps roll outward, sway = yaw"""
    for i, r in enumerate(ROWS):
        k.key(r, f, rot=(lift[i], sway[i], 0))
        k.key(r + "_L", f, rot=(0, 0, splay[i]))
        k.key(r + "_R", f, rot=(0, 0, -splay[i]))


def tail(k, f, n, lift=0.0, sway=0.0, cycles=1, phase=0.0, lag=0.10):
    """the long smoke tail: a lagging sway down the chain (+ lift = the tail rises)"""
    for i, b in enumerate(TAILB):
        y = sway * (0.6 + 0.3 * i) * pk.wave(f, n, phase - lag * i, cycles) if sway else 0.0
        k.key(b, f, rot=(lift * (1.0 - 0.15 * i), y, 0))


def wv(f, n, ph, c):
    """a loop wave shifted to 0 at f0 (and so at fn): the idle's first frame is the exact rest of the acts"""
    return pk.wave(f, n, ph, c) - pk.wave(0, n, ph, c)


def idle(k):
    """SCENT DRIFT (ref W2, The Pointer): the nose lowers and lifts in slow 15-20 f moves while the body stays
    still, the ears flick back (f40) and forward (f80), the mane rows drift with a 3 f lag per row, the tail
    streams slowly."""
    n = 120
    k.new_action("idle", n, True)
    HP = [(0, 0.0), (10, 0.0), (28, 10.0), (42, 10.0), (60, -8.0), (72, -8.0), (90, 5.0), (100, 5.0), (116, 0.0),
          (120, 0.0)]
    SN = [(0, 0.0), (30, 0.0), (33, 1.0), (36, 0.0), (39, 1.0), (42, 0.0), (120, 0.0)]          # sniffs (low)
    EF = [(0, 0.0), (38, 0.0), (41, -14.0), (47, -14.0), (54, 0.0), (78, 0.0), (81, 8.0), (86, 8.0), (92, 0.0),
          (120, 0.0)]
    for f in range(0, n + 1, 2):
        hp = tab(HP, f)
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.003 * b))
        k.key("Chest", f, rot=(-0.6 * b, 0, 0))
        k.key("Neck", f, rot=(0.35 * hp, 0, 0))
        k.key("Head", f, rot=(0.65 * hp - 2.0 * tab(SN, f), 0, 0))
        k.key("Jaw", f, rot=(1.5, 0, 0))
        ears(k, f, tab(EF, f))
        mane(k, f, [3.0 * wv(f, n, -0.025 * i, 2) for i in range(3)], [2.0 * wv(f, n, 0.25 - 0.025 * i, 2)
             for i in range(3)], [4.0 * wv(f, n, 0.1 - 0.025 * i, 1) for i in range(3)])
        for i, tb in enumerate(TAILB):                  # the tail drifts down the chain (0 at f0 = the acts' rest)
            k.key(tb, f, rot=(1.5 * b * (1.0 - 0.15 * i), 5.0 * (0.6 + 0.3 * i) * wv(f, n, -0.10 * i, 1), 0))
    cm.plant(k, n)
    k.finish()
    k.meta["planted"] = list(LEGS4)


def walk(k):
    """LEAN TROT-WALK (refs W1 + W4): long diagonal steps, the head low and level, the mane rows lag the body by
    4 f (2 lifts per cycle), the tail streams behind with a lagging sway."""
    n = 30

    def body(f):
        bob = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.6 * pk.wave(f, n, 0.1, 2), 2.0 * pk.wave(f, n), 2.0 * pk.wave(f, n)),
              loc=(0, 0, -0.020 - 0.014 * bob))          # 0.02 lower: legs never straighten (no knee snap)
        k.key("Chest", f, rot=(0, -2.5 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(3.0 + 1.0 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(1.0 - 1.5 * pk.wave(f, n, 0.20, 2), -1.5 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(1.5, 0, 0))
        ears(k, f, -4.0)
        lagc = 4.0 / n                                   # the mane lags the body by 4 f
        mane(k, f, [-3.0 + 3.0 * pk.wave(f, n, 0.1 - lagc - 0.03 * i, 2) for i in range(3)],
             [3.0 + 2.0 * pk.wave(f, n, 0.35 - lagc - 0.03 * i, 2) for i in range(3)],
             [-3.0 * pk.wave(f, n, 0.25 - lagc - 0.03 * i) for i in range(3)])
        tail(k, f, n, lift=2.0 + 2.0 * pk.wave(f, n, 0.3, 2), sway=6.0, cycles=1, phase=0.3)
    return cm.quad_walk(k, n, 0.15, 0.060, body, gait="trot")


def roar(k):
    """MANE FLARE (refs W1 + W3): the smoke mane lifts and splays out 25 deg row by row (2 f lag) and the ears go
    back; the chest pushes forward 0.05H, the head pitches down 10 deg and the jaw opens 25 deg (a silent snarl,
    fangs out, ears follow the mouth); hold with a 2 deg mane tremble; the mane falls back and the jaw closes."""
    n = 60
    k.new_action("roar", n, False)
    MF = [(0, 0.0), (12, 1.0), (44, 1.0), (54, 0.0), (60, 0.0)]          # ends f54: the 4 f row lag settles by f58
    EA = [(0, 0.0), (14, -24.0), (46, -24.0), (56, 0.0), (60, 0.0)]
    PU = [(0, 0.0), (14, 0.0), (26, 1.0), (44, 1.0), (56, 0.0), (60, 0.0)]
    JW = [(0, 1.5), (11, 1.5), (26, 25.0), (44, 25.0), (54, 1.5), (60, 1.5)]   # review 4: opens over 15 f (W0)
    push = 0.05 * H_U
    for f in range(0, n + 1):
        pu = tab(PU, f)
        tr = 2.0 * math.sin(2 * math.pi * f / 10) if 26 <= f <= 44 else 0.0     # final85 C1: 3 Hz, not 7.5 Hz
        k.key("Spine", f, rot=(2.0 * pu, 0, 0), loc=(0, -push * pu, -0.020 * pu))
        k.key("Chest", f, rot=(1.5 * pu, 0, 0))
        k.key("Neck", f, rot=(4.0 * pu, 0, 0))
        k.key("Head", f, rot=(6.0 * pu + 0.3 * tr, 0, 0))
        k.key("Jaw", f, rot=(tab(JW, f) + 0.5 * tr, 0, 0))
        ears(k, f, tab(EA, max(0, f - 3)), splay=6.0 * tab(MF, f))           # the ears follow ~3 f late
        mf = [tab(MF, max(0, f - 2 * i)) for i in range(3)]
        mane(k, f, [18.0 * m + (tr if i == 1 else -tr) * m for i, m in enumerate(mf)],
             [12.0 * m for m in mf], [0.0, 0.0, 0.0])                    # final85 C2: 12 deg (was 25)
        tail(k, f, n, lift=8.0 * tab(MF, f), sway=0.0)
    cm.plant(k, n)
    k.finish(loop=False)
    k.events["roar"] = {"fog": round(14 / n, 3), "snarl": round(26 / n, 3)}


def smokecloak(k):
    """SIGNATURE act_smokecloak - THE CLOAK SPREADS (refs W3 + W4): the hound crouches flat, the smoke mane lifts and
    fans out wide row by row (3 f lag) like a cloak, holds and drifts (two slow sway cycles), folds back in as the
    hound rises, and settles to the exact rest pose. All four paws planted every frame."""
    n = 100
    k.new_action("act_smokecloak", n, False)
    CR = [(0, 0.0), (18, 1.0), (68, 1.0), (86, 0.0), (100, 0.0)]
    FAN = [(0, 0.0), (18, 0.0), (32, 1.0), (68, 1.0), (84, 0.0), (100, 0.0)]
    HOLD = [(0, 0.0), (38, 0.0), (44, 1.0), (64, 1.0), (70, 0.0), (100, 0.0)]
    EA = [(0, 0.0), (14, -18.0), (66, -18.0), (84, 0.0), (100, 0.0)]
    for f in range(0, n + 1):
        c, hd = tab(CR, f), tab(HOLD, f)
        k.key("Spine", f, rot=(2.0 * c, 0, 0), loc=(0, 0.015 * c, -CROUCH * c))
        k.key("Chest", f, rot=(1.5 * c, 0, 0))
        k.key("Neck", f, rot=(-5.0 * c, 0, 0))
        k.key("Head", f, rot=(-2.0 * c, 0, 0))
        k.key("Jaw", f, rot=(1.5 + 3.0 * c, 0, 0))
        ears(k, f, tab(EA, f))
        fan = [tab(FAN, max(0, f - 3 * i)) for i in range(3)]
        dr = [6.0 * hd * math.sin(2 * math.pi * (f - 40 - 3 * i) / 14.0) for i in range(3)]   # two drift cycles
        mane(k, f, [6.0 * fan[0], 4.0 * fan[1], 2.0 * fan[2]], [60.0 * a + 0.5 * d for a, d in zip(fan, dr)], dr)
        # (r2: staggered row lift 6 / 4 / 2 deg, so the fan does not read as a ring from behind)
        for i, b in enumerate(TAILB):        # the tail streams out behind (lifts clear of the floor) and sways
            k.key(b, f, rot=(10.0 * c * (1.0 - 0.15 * i), 4.0 * hd * math.sin(2 * math.pi * (f - 44 - 3 * i) / 14.0),
                             0))
    cm.plant(k, n)
    k.finish(loop=False)
    k.events["act_smokecloak"] = {"smoke_puff": round(16 / n, 3), "cloak": round(28 / n, 3),
                                  "drift": round(54 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    smokecloak(k)
    return stride
