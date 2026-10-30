# Frostfang Lynx (Glacier egg, STARTER 50 %) - FIERCE style (2026-10-27, Glacier update batch 1).
# Plan: _review/FrostfangLynx_plan.md (v2) + review _review/GLACIER_PLAN_REVIEW.md 2.1.
# A lean ice lynx: compact body on long legs, big snowshoe paws with smooth icy claws, a sand-silver coat covered in
# dark rosette spots, a darker saddle, snow-white underside + the lynx "beard" (a snow ruff hanging from the cheeks),
# tall ears with ice tufts, narrow ice-cyan slit eyes under heavy V brows, a short bobtail with a black tip.
# v2 (builder A): head group x1.28 about the throat (HEAD_S, ShadePanther pattern), rounded shoulders/thighs instead of
# slabs, thicker forearms + bigger paws, big organic rosette blobs (Poly inlays), beard ruff hangs down, V brows.
import math
import os
import random
from mathutils import Vector, Euler

DISPLAY = "Frostfang Lynx"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 7.0                  # total height (ear-tuft tips) in studs at x1

WARM_SILVER = (190, 172, 150)  # body / legs / head sides (studded)
BACK_SHADE = (126, 116, 110)   # saddle, brows, ear backs, rosette spots (>= 20 % of the side view)
SNOW = (240, 244, 250)         # underside, muzzle, cheek ruff, paw socks, ear fronts
ICE = (150, 236, 255)          # THE accent: eye slits, tuft tips
ICE_CLAW = (214, 244, 255)     # claws (smooth)
BLACK = (14, 14, 22)
MOUTH = (86, 18, 30)
TEETH = (238, 234, 220)

PITCH = 0.034                  # ~0.08 x torso height

# leg joints (left side): shoulder/hip, elbow/knee, wrist/ankle, paw centre (long cat legs, withers ~0.79)
LEGS = {"F": ((0.108, -0.30, 0.555), (0.114, -0.235, 0.312), (0.118, -0.285, 0.085), (0.118, -0.335, 0.042)),
        "B": ((0.106, 0.30, 0.575), (0.112, 0.175, 0.352), (0.115, 0.365, 0.148), (0.115, 0.320, 0.042))}
DZ = -0.030                    # the whole body / head / tail sits this much lower than the coordinates below
BODYB = ("Chest", "Spine", "Neck", "Head", "Jaw", "Ear_L", "Ear_R", "Tail1", "Tail2", "Tail3")
TAILP = [(0, 0.43, 0.725), (0, 0.54, 0.69), (0, 0.64, 0.63), (0, 0.715, 0.56)]
HJ = Vector((0, -0.535, 0.850))    # head group scale pivot = the throat (Head joint)
HEAD_S = 1.28
HEADBONES = ("Head", "Jaw", "Ear_L", "Ear_R")


def hs(p):
    """rest-space point of the head group after its scale about the throat"""
    return HJ + (Vector(p) - HJ) * HEAD_S


def bz(p):
    """body-group rest point (the body is lowered by DZ after it is built)"""
    return tuple(Vector(p) + Vector((0, 0, DZ)))


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def prof(b, lz):
    t = (lz / b.h.z + 1) / 2
    fx = b.bot[0] + (b.top[0] - b.bot[0]) * t
    fy = b.bot[1] + (b.top[1] - b.bot[1]) * t
    return b.h.x * fx, b.h.y * fy, b.ts[1] * t


def side_pt(b, s, ly, lz, off=0.006):
    """point on the +-x flank of tapered block b at local (ly, lz) + the flank normal"""
    hx, _, oy = prof(b, lz)
    p = b.world(Vector((s * (hx + off), ly + oy, lz)))
    dx = b.h.x * (b.top[0] - b.bot[0]) / (2 * b.h.z)
    return p, (b.R @ Vector((s, 0, -dx))).normalized()


def blob(B, b, s, ly, lz, r, seed, el=1.25, ang=0.0, n=8, col=None):
    """an organic dark spot lying flush on a flank: an irregular convex n-gon (Poly inlay, smooth, no studs)"""
    rng = random.Random(seed)
    r *= SPOT_K
    a0 = math.radians(ang)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (0.84 + 0.26 * rng.random())
        u, v = math.cos(a) * rr * el, math.sin(a) * rr
        du, dv = u * math.cos(a0) - v * math.sin(a0), u * math.sin(a0) + v * math.cos(a0)
        pts.append(side_pt(b, s, ly + du, lz + dv, off=0.003)[0])
    B.poly(pts, 0.010, col or SPOT, b.bone)


def rosette(B, b, s, ly, lz, r, seed, ang=0.0):
    """lynx rosette: 3 crescent blobs around an open centre (reads as one spot at 64 px, a rosette up close)"""
    for i in range(3):
        a = math.radians(ang + 120 * i)
        blob(B, b, s, ly + math.cos(a) * r * 0.64, lz + math.sin(a) * r * 0.64, r * 0.58, seed + i, el=1.45,
             ang=ang + 120 * i + 90, n=7)


SPOT = BACK_SHADE
SPOT_K = 1.10                  # spot size factor (rosettes >= 20 % of the side view)


def saddle(B, b, w, seed):
    """a darker-back inlay lying flush on the top face of torso block b: an irregular elongated octagon"""
    rng = random.Random(seed)
    L = b.h.y * b.top[1] - 0.034
    ts = Vector((b.ts[0], b.ts[1], 0))
    pts = []
    for u, v in ((-0.62, -1), (0.62, -1), (1, -0.72), (1, 0.72), (0.62, 1), (-0.62, 1), (-1, 0.72), (-1, -0.72)):
        j = 0.94 + 0.10 * rng.random()
        pts.append((u * w * j, v * L))
    rings = [[b.world(Vector((x, y, b.h.z + z)) + ts) for x, y in pts] for z in (-0.004, 0.006)]
    B.tube(rings, BACK_SHADE, b.bone)                    # a thin studded prism (Tube takes the stud skin)


def model(k):
    import blockkit as bk
    global SPOT
    SPOT = (255, 0, 255) if os.environ.get("LYNX_SPOTDBG") else BACK_SHADE
    nospots = bool(os.environ.get("LYNX_NOSPOTS"))
    B = bk.Blocks(k, seed=271, tier=3, plates=False)
    # ---------------- torso: compact deep chest, strong tuck, narrow waist, high hips (lynx: hind legs longer)
    rib = B.add((0, -0.19, 0.598), (0.152, 0.235, 0.192), WARM_SILVER, "Chest", bot=(0.62, 0.52), top=(0.88, 0.92),
                rnd=0.30)
    B.seg((0, -0.06, 0.428), (0, 0.20, 0.535), 0.092, 0.055, WARM_SILVER, "Spine", top=(0.82, 0.75), side=(1, 0, 0))
    waist = B.add((0, 0.08, 0.655), (0.120, 0.16, 0.112), WARM_SILVER, "Spine", bot=(0.72, 0.70), top=(0.95, 1),
                  rnd=0.30)
    hips = B.add((0, 0.30, 0.660), (0.136, 0.155, 0.134), WARM_SILVER, "Spine", rot=(-6, 0, 0), top=(0.84, 0.90),
                 bot=(0.85, 0.9), rnd=0.32)
    # darker saddle along the top line: flush irregular inlays on the tops of chest, waist and hips (no plates)
    for blk, w, sd in ((rib, 0.092, 5), (waist, 0.080, 6), (hips, 0.082, 7)):
        saddle(B, blk, w, sd)
    # (flush dorsal inlays on each torso top: see saddle() below the torso blocks)
    # snow underside following the tuck + a V-shaped snow chest ruff under the throat
    B.add((0, -0.20, 0.418), (0.080, 0.12, 0.02), SNOW, "Chest", bot=(0.8, 0.9), studs=[])
    B.seg((0, -0.06, 0.420), (0, 0.18, 0.518), 0.062, 0.018, SNOW, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    B.add((0, -0.418, 0.600), (0.086, 0.028, 0.135), SNOW, "Chest", bot=(0.30, 0.8), top=(1.0, 1), rot=(-14, 0, 0),
          rnd=0.35)
    for s in (1, -1):                                       # chest-ruff points between the forelegs
        B.spike((s * 0.030, -0.425, 0.500), (s * 0.15, -0.25, -1), 0.060, 0.026, SNOW, "Chest", top=(0.15, 0.45))
    # ---------------- neck (40 deg up) + head (built at draft size, then scaled x HEAD_S about the throat)
    neck = B.seg((0, -0.33, 0.66), (0, -0.53, 0.845), 0.096, 0.106, WARM_SILVER, "Neck", ext=0.05)
    B.seg((0, -0.27, 0.770), (0, -0.50, 0.880), 0.090, 0.040, BACK_SHADE, "Neck", side=(1, 0, 0), ext=0.02,
          top=(0.80, 1), rnd=0.45)                                                          # dark nape scruff
    B.seg((0, -0.39, 0.61), (0, -0.56, 0.785), 0.070, 0.056, SNOW, "Neck", side=(1, 0, 0), ext=0.02)    # snow throat
    n0 = len(B.items)
    B.add((0, -0.612, 0.922), (0.098, 0.085, 0.082), WARM_SILVER, "Head", top=(0.84, 0.86), bot=(0.92, 0.95),
          rnd=0.42)                                                                         # cranium
    for s in (1, -1):                                                                       # broad lynx cheeks
        B.add((s * 0.066, -0.646, 0.880), (0.036, 0.050, 0.040), WARM_SILVER, "Head", rot=(0, 0, s * 10), rnd=0.45)
    B.add((0, -0.598, 0.999), (0.066, 0.058, 0.012), BACK_SHADE, "Head", top=(0.8, 0.8))               # dark crown
    B.seg((0, -0.672, 0.894), (0, -0.756, 0.884), 0.058, 0.038, SNOW, "Head", top=(0.80, 0.84), ext=0.02)  # muzzle
    B.seg((0, -0.672, 0.945), (0, -0.758, 0.918), 0.034, 0.018, WARM_SILVER, "Head", top=(0.8, 1), ext=0.01)  # bridge
    for sx in (1, -1):                                                                      # whisker pads
        B.add((sx * 0.029, -0.752, 0.860), (0.030, 0.024, 0.021), SNOW, "Head", rnd=0.45)
    B.add((0, -0.770, 0.906), (0.023, 0.011, 0.014), BLACK, "Head", bot=(0.45, 0.8), role="detail", bevel=0.004)
    for s in (1, -1):
        B.spike((s * 0.033, -0.757, 0.846), (0, -0.1, -1), 0.050, 0.011, TEETH, "Head")
    # lower jaw + mouth
    B.seg((0, -0.60, 0.818), (0, -0.750, 0.816), 0.056, 0.020, SNOW, "Jaw", top=(0.8, 1), ext=0.02)
    B.add((0, -0.69, 0.837), (0.038, 0.062, 0.005), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    # narrow ice-cyan slit eyes (black socket, vertical pupil) under heavy V brows that cover the eye tops (lids)
    for s in (1, -1):
        rot = (0, -s * 18, s * 20)
        B.add((s * 0.050, -0.700, 0.938), (0.036, 0.008, 0.017), BLACK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.003)
        B.add((s * 0.051, -0.706, 0.937), (0.030, 0.006, 0.0098), ICE, "Head", rot=rot, studs=[], role="detail",
              bevel=0.002)
        B.add((s * 0.049, -0.7140, 0.935), (0.0072, 0.0040, 0.0120), BLACK, "Head", rot=(0, 0, s * 20), studs=[],
              role="detail", bevel=0.0012)                                                  # vertical cat pupil
        B.add((s * 0.047, -0.706, 0.958), (0.046, 0.016, 0.013), BACK_SHADE, "Head", rot=(0, -s * 26, s * 20),
              role="detail", bevel=0.006)                                                   # V brow / lid
    # the lynx beard: snow ruff points hanging from the cheeks, down + back + a little out, plus a chin tuft
    for s in (1, -1):
        B.add((s * 0.086, -0.640, 0.846), (0.030, 0.048, 0.046), SNOW, "Head", rot=(-12, 0, s * 14), bot=(0.8, 0.7),
              rnd=0.40)                                                                     # ruff base (sideburn)
        for y, z, d, L, w in ((-0.664, 0.822, (s * 0.45, 0.35, -0.82), 0.080, 0.027),
                              (-0.645, 0.828, (s * 0.72, 0.45, -0.52), 0.098, 0.030),
                              (-0.622, 0.848, (s * 0.88, 0.50, -0.22), 0.094, 0.029),
                              (-0.610, 0.880, (s * 0.88, 0.48, 0.08), 0.070, 0.024)):
            B.spike((s * 0.096, y, z), d, L, w, SNOW, "Head", top=(0.22, 0.30))
    # tall ears with snow fronts and ice tufts (blocks only, no strands)
    for s, side in ((1, "L"), (-1, "R")):
        R = Euler((math.radians(-8), math.radians(s * 6), math.radians(-s * 12)), "XYZ").to_matrix()
        root = Vector((s * 0.060, -0.585, 0.985))
        ear = B.add(root + R @ Vector((0, 0, 0.054)), (0.040, 0.015, 0.058), BACK_SHADE, "Ear_" + side, R=R,
                    top=(0.26, 0.6), rnd=0.25)
        B.add(ear.world((0, -0.015, -0.006)), (0.024, 0.004, 0.040), SNOW, "Ear_" + side, R=R, top=(0.35, 1),
              studs=[], role="detail", bevel=0.003)
        B.add(root + R @ Vector((0, 0, 0.094)), (0.018, 0.0165, 0.020), ICE, "Ear_" + side, R=R, top=(0.35, 0.7),
              studs=[], role="detail", bevel=0.004)                                         # frosted ear tip
        tip = root + R @ Vector((0, 0, 0.100))
        for dx, L in ((-0.25, 0.070), (0.15, 0.058)):                       # the tuft: two ice pencils
            B.spike(tip - R @ Vector((0, 0, 0.010)), R @ Vector((s * dx * 0.5, 0.10, 1)), L, 0.0115, ICE,
                    "Ear_" + side, top=(0.15, 0.35))
    for blk in B.items[n0:]:
        if blk.bone in HEADBONES and hasattr(blk, "h"):
            blk.c = hs(blk.c)
            blk.h = blk.h * HEAD_S
    LEGBLK = []
    # ---------------- legs: rounded shoulders + thighs, thick forearms, snowshoe paws with smooth icy claws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, Pw = (X(p, s) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                up = B.seg(H + Vector((-s * 0.008, 0.01, 0.03)), K, 0.047, 0.072, WARM_SILVER, leg, ext=0.0,
                           ext1=0.03, top=(0.88, 0.72), rnd=0.45)
                B.spike(K + Vector((0, 0.035, 0.02)), (0, 0.55, -0.80), 0.050, 0.026, WARM_SILVER, leg,
                        top=(0.15, 0.45))                                                   # elbow tuft
                lo = B.seg(K, A, 0.056, 0.062, WARM_SILVER, shin, top=(0.86, 0.86), ext=0.03, ext1=0.02, rnd=0.40)
                B.seg(A + Vector((0, 0.005, 0.07)), A, 0.060, 0.064, SNOW, shin, ext1=0.02, rnd=0.40)  # snow sock
            else:
                up = B.seg(H + Vector((0, 0.03, 0.06)), K, 0.068, 0.112, WARM_SILVER, leg, bot=(0.85, 1),
                           top=(0.75, 0.62), ext=0.0, ext1=0.03, rnd=0.45)
                lo = B.seg(K, A, 0.054, 0.062, WARM_SILVER, shin, top=(0.82, 0.82), ext=0.03, ext1=0.02, rnd=0.40)
                B.seg(A, Pw + Vector((0, 0.03, 0.025)), 0.050, 0.050, SNOW, foot, ext=0.03, rnd=0.40)
            LEGBLK.append((s, fb, up, lo))
            B.add(Pw, (0.076, 0.088, 0.042), SNOW, foot, top=(0.86, 0.80), rnd=0.40)            # snowshoe paw
            cb = ("Claw_" + fb + side) if fb == "F" else foot
            for gx in (-0.043, -0.015, 0.015, 0.043):
                B.spike((Pw.x + gx, Pw.y - 0.076, 0.032), (0, -1, -0.55), 0.056, 0.012, ICE_CLAW, cb)
    # ---------------- rosette spots: big organic blobs on flanks, shoulders, thighs, upper legs (>= 20 % side view)
    if not nospots:
        for s in (1, -1):
            sd = 11 if s > 0 else 53
            for i, (ly, lz, r, a, ros) in enumerate(((-0.150, 0.080, 0.046, 15, True), (-0.045, 0.110, 0.040, 70, False),
                                                     (0.075, 0.070, 0.048, 40, True), (-0.100, -0.015, 0.042, 120, False),
                                                     (0.015, -0.005, 0.050, 10, True), (0.125, -0.030, 0.038, 80, False),
                                                     (-0.180, -0.070, 0.030, 30, False), (0.180, 0.120, 0.030, 50, False),
                                                     (-0.050, -0.090, 0.032, 100, False), (0.075, -0.095, 0.030, 20, False),
                                                     (0.150, 0.040, 0.028, 70, False), (-0.130, 0.140, 0.024, 10, False))):
                (rosette if ros else blob)(B, rib, s, ly, lz, r, sd + 7 * i, ang=a)
            for i, (ly, lz, r, a, ros) in enumerate(((-0.070, 0.030, 0.046, 30, True), (0.065, 0.050, 0.040, 70, False),
                                                     (0.010, -0.045, 0.036, 0, False))):
                (rosette if ros else blob)(B, waist, s, ly, lz, r, sd + 101 + 7 * i, ang=a)
            for i, (ly, lz, r, a, ros) in enumerate(((-0.060, 0.060, 0.048, 15, True), (0.070, 0.035, 0.042, 50, False),
                                                     (-0.010, -0.050, 0.046, 85, True), (0.090, -0.075, 0.034, 20, False),
                                                     (-0.100, -0.060, 0.030, 60, False), (0.040, 0.105, 0.028, 30, False))):
                (rosette if ros else blob)(B, hips, s, ly, lz, r, sd + 201 + 7 * i, ang=a)
            for i, (ly, lz, r, a) in enumerate(((0.035, -0.040, 0.034, 20), (-0.030, 0.055, 0.030, 70),
                                                (0.050, 0.070, 0.024, 40), (-0.050, -0.050, 0.026, 10))):
                blob(B, neck, s, ly, lz, r, sd + 301 + 7 * i, el=1.2, ang=a)
        for s, fb, up, lo in LEGBLK:                         # spots down the legs (upper: 2, lower: 1)
            sd = (300 if fb == "F" else 400) + (0 if s > 0 else 50)
            if fb == "F":
                blob(B, up, s, 0.010, -0.040, 0.040, sd, el=1.1, ang=70)
                blob(B, up, s, -0.020, 0.065, 0.034, sd + 3, el=1.2, ang=20)
                blob(B, lo, s, 0.000, -0.050, 0.024, sd + 5, el=1.2, ang=80)
                blob(B, lo, s, 0.010, 0.040, 0.020, sd + 7, el=1.2, ang=10)
            else:
                rosette(B, up, s, 0.000, -0.050, 0.056, sd, ang=20)
                blob(B, up, s, 0.020, 0.070, 0.036, sd + 3, el=1.2, ang=60)
                blob(B, lo, s, 0.000, -0.040, 0.024, sd + 5, el=1.2, ang=80)
    # ---------------- short bobtail with a black tip band
    P = [Vector(p) for p in TAILP]
    for i, ((a, b), (w, d)) in enumerate(zip(zip(P, P[1:]), ((0.042, 0.052), (0.042, 0.048), (0.038, 0.042)))):
        B.seg(a, b, w, d, BLACK if i == 2 else WARM_SILVER, "Tail%d" % (i + 1), ext=0.03, top=(0.92, 0.92), rnd=0.40)
    dz = Vector((0, 0, DZ))
    for blk in B.items:
        if blk.bone in BODYB:
            if hasattr(blk, "pts"):
                blk.pts = [q + dz for q in blk.pts]
            blk.c = blk.c + dz
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", bz((0, 0.16, 0.65)), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", bz((0, -0.08, 0.65)), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", bz((0, -0.34, 0.685)), "Chest", tail=(0, -0.15, 0.14))
    k.joint("Head", bz(HJ), "Neck", tail=(0, -0.25, 0.0))                     # throat pivot
    k.joint("Jaw", bz(hs((0, -0.605, 0.826))), "Head", tail=(0, -0.15, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, bz(hs((s * 0.060, -0.585, 0.985))), "Head", tail=(s * 0.02, 0, 0.1))
        k.joint("FX_IceDust_" + side, bz(hs((s * 0.066, -0.575, 1.140))), "Ear_" + side, tail=(0, 0, 0.05))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, Pw = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.12, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
            if fb == "F":
                k.joint("Claw_F" + side, (Pw.x, Pw.y - 0.05, 0.035), "Foot_F" + side, tail=(0, -0.06, -0.02))
                k.joint("FX_IceSpark_" + side, (Pw.x, Pw.y - 0.12, 0.03), "Claw_F" + side, tail=(0, -0.05, 0))
                k.joint("FX_SnowPuff_F" + side, (Pw.x, Pw.y, 0.01), "Foot_F" + side, tail=(0, 0, 0.05))
    for i in range(3):
        k.joint("Tail%d" % (i + 1), bz(TAILP[i]), "Spine" if i == 0 else "Tail%d" % i,
                tail=tuple(Vector(TAILP[i + 1]) - Vector(TAILP[i])))
    k.joint("FX_SnowFlick", bz(TAILP[3]), "Tail3", tail=(0, 0.05, -0.03))


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR"), ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"),
         ("Claw_FL", "Claw_FR")]
    for a in ("Head", "Jaw"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    P += [("Head", "Chest"), ("Jaw", "Chest"), ("Ear_L", "Ear_R")]
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR"):
        P.append(("Tail1", b))
    return P


def joints():
    return [(bz((0, -0.52, 0.82)), bz((0, -0.56, 0.89)), 0.14, "Head")]


HEAD_XF = []
