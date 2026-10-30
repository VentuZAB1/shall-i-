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
COATS = {"warm": ((190, 172, 150), (126, 116, 110)),          # v2 (beige in game - final85 review T2)
         "sand": ((170, 156, 138), (108, 98, 92)),            # deeper sand
         "frost": ((168, 176, 188), (100, 106, 122))}         # cool frost-silver
COAT = os.environ.get("LYNX_COAT", "frost")            # final85 T2: frost-silver chosen (see MODEL_NOTES round 5)
WARM_SILVER, BACK_SHADE = COATS[COAT]
ROSE_C = {"warm": (214, 200, 180), "sand": (198, 186, 168), "frost": (204, 210, 222)}[COAT]   # r2 T1: rosette centre
SNOW = (240, 244, 250)         # underside, muzzle, cheek ruff, paw socks, ear fronts
ICE = (150, 236, 255)          # THE accent: eye slits, tuft tips
# (ICE_CLAW (214,244,255) retired in final85 M3: the frost fangs are ICE now)
BLACK = (14, 14, 22)
MOUTH = (86, 18, 30)

PITCH = 0.034                  # ~0.08 x torso height

# leg joints (left side): shoulder/hip, elbow/knee, wrist/ankle, paw centre (long cat legs, withers ~0.79)
LEGS = {"F": ((0.108, -0.30, 0.555), (0.114, -0.235, 0.312), (0.118, -0.285, 0.085), (0.118, -0.335, 0.042)),
        "B": ((0.106, 0.30, 0.575), (0.112, 0.175, 0.352), (0.115, 0.365, 0.148), (0.115, 0.320, 0.042))}
DZ = -0.030                    # the whole body / head / tail sits this much lower than the coordinates below
BODYB = ("Chest", "Spine", "Neck", "Head", "Jaw", "Ear_L", "Ear_R", "Ruff_L", "Ruff_R", "Tail1", "Tail2", "Tail3")
TAILP = [(0, 0.43, 0.725), (0, 0.50, 0.70), (0, 0.55, 0.66), (0, 0.59, 0.63)]    # lynx bobtail (review 1 M2)
HJ = Vector((0, -0.535, 0.850))    # head group scale pivot = the throat (Head joint)
HEAD_S = 1.28
HEADBONES = ("Head", "Jaw", "Ear_L", "Ear_R", "Ruff_L", "Ruff_R")
CLAWX = (-0.043, -0.015, 0.015, 0.043)
CLAWZ, CLAWD = 0.042, (0, -1, -0.42)      # claw base height + direction (0.072 long: tips stay above the floor)  # claw x offsets on each paw (front claws: one bone each, Claw_FL1..4)
RUFFJ = (0.072, -0.636, 0.858)         # cheek-ruff hinge (draft space), clips: the ruff flare


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


def blob(B, b, s, ly, lz, r, seed, el=1.25, ang=0.0, n=8, col=None, off=0.003):
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
        pts.append(side_pt(b, s, ly + du, lz + dv, off=off)[0])
    B.poly(pts, 0.010, col or SPOT, b.bone)


def rosette(B, b, s, ly, lz, r, seed, ang=0.0):
    """lynx rosette (final85 T1 / r2 T1): a broken ring of 6 irregular dark blobs (over ~300 deg) around an OPEN centre
    filled with a lighter coat tone (ROSE_C), so each spot reads as a ring at 128 px, not a blotch"""
    rng = random.Random(seed * 7 + 3)
    for i in range(5):                                  # uneven spacing + sizes: an open rosette, not a cog wheel
        a = math.radians(ang + 58 * i + rng.uniform(-14, 14))
        rr = r * (0.98 + 0.16 * rng.random())
        blob(B, b, s, ly + math.cos(a) * rr, lz + math.sin(a) * rr, r * (0.42 + 0.16 * rng.random()), seed + i,
             el=1.55, ang=math.degrees(a) + 90, n=7)
    blob(B, b, s, ly, lz, r * 0.52, seed + 17, el=1.10, ang=ang, n=8, col=ROSE_C, off=0.0022)   # light open centre


def frost_point(B, base, d, L, w, bone, soft=False):
    """a SNOW fur point with a frosted ICE tip (outer 45 %, smooth) - the cheek-ruff method (final85 M3)"""
    dn = Vector(d).normalized()
    kb = dict(top=(0.45, 0.60), rnd=0.40) if soft else dict(top=(0.57, 0.62))
    B.spike(base, d, L * 0.55, w, SNOW, bone, **kb)
    kt = dict(top=(0.45, 0.60), rnd=0.40) if soft else dict(top=(0.38, 0.50))
    B.spike(Vector(base) + dn * (L * 0.55 - 0.004), d, L * 0.45 + 0.004, w * (0.62 if soft else 0.57), ICE,
            bone, role="detail", nostud=True, **kt)


def top_z(blk, y):
    """height of the rounded top of torso block blk along its centre line at world y (None = not over it).
    Edge rounding = the blockkit bevel: rnd x the smallest half-size (capped at 0.45 x)."""
    mn = min(blk.h.x * min(blk.top[0], blk.bot[0]), blk.h.y * min(blk.top[1], blk.bot[1]), blk.h.z)
    r = min(blk.rnd if blk.rnd is not None else 0.3, 0.45) * mn
    hy = blk.h.y * blk.top[1]
    best = None
    for i in range(81):                                   # walk the local top edge, keep the sample nearest world y
        ly = -hy + 2 * hy * i / 80
        d = max(0.0, abs(ly) - (hy - r))
        lz = blk.h.z - (r - math.sqrt(max(0.0, r * r - d * d)))
        p = blk.world(Vector((0, ly + blk.ts[1], lz)))
        if best is None or abs(p.y - y) < abs(best.y - y):
            best = p
    return best.z if best is not None and abs(best.y - y) < 0.006 else None


def dorsal_band(B, blocks, w=0.050):
    """final85 M1: one continuous dark dorsal band (a studded closed Tube lofted along y) lying on the union of the
    torso block tops: nape scruff -> chest -> waist -> hips -> tail root. The top line is smoothed (running max, then
    mean) so the band bridges the small steps between the torso blocks as ONE line; its bottom is buried 0.03 deep.
    Two tubes (Chest / Spine) overlap at y 0.016-0.032."""
    Y = [-0.40 + 0.008 * i for i in range(107)]
    Z = []
    for y in Y:
        zs = [z for z in (top_z(b, y) for b in blocks) if z is not None]
        Z.append(max(zs) if zs else None)
    Z = [z if z is not None else next(q for q in Z if q is not None) for z in Z]
    M = [max(Z[max(0, i - 4):i + 5]) for i in range(len(Z))]                   # bridge the dips (+-0.032)
    S = [sum(M[max(0, i - 3):i + 4]) / len(M[max(0, i - 3):i + 4]) for i in range(len(M))]   # smooth the line
    for bone, y0, y1 in (("Chest", -0.40, 0.032), ("Spine", 0.016, 0.445)):
        rings = []
        for y, z in zip(Y, S):
            if y < y0 - 1e-6 or y > y1 + 1e-6:
                continue
            ww = w * (0.80 + 0.20 * max(0.0, min(1.0, (y + 0.40) / 0.12, (0.445 - y) / 0.10)))   # tapered ends
            top, bot = z + 0.004, z - 0.034
            rings.append([Vector((-ww, y, bot)), Vector((ww, y, bot)), Vector((ww, y, top)), Vector((-ww, y, top))])
        B.tube(rings, BACK_SHADE, bone)


SPOT = BACK_SHADE
SPOT_K = 1.24                  # spot size factor (rosettes >= 20 % of the side view)


def model(k):
    import blockkit as bk
    global SPOT
    SPOT = (255, 0, 255) if os.environ.get("LYNX_SPOTDBG") else BACK_SHADE
    nospots = bool(os.environ.get("LYNX_NOSPOTS"))
    B = bk.Blocks(k, seed=271, tier=3, plates=False)
    # ---------------- torso: compact deep chest, strong tuck, narrow waist, high hips (lynx: hind legs longer)
    rib = B.add((0, -0.19, 0.598), (0.152, 0.235, 0.192), WARM_SILVER, "Chest", bot=(0.62, 0.52), top=(0.88, 0.92),
                rnd=0.30)
    B.seg((0, -0.06, 0.428), (0, 0.20, 0.560), 0.092, 0.055, WARM_SILVER, "Spine", top=(0.82, 0.75), side=(1, 0, 0))
    waist = B.add((0, 0.08, 0.6675), (0.120, 0.16, 0.0995), WARM_SILVER, "Spine", bot=(0.72, 0.70), top=(0.95, 1),
                  rnd=0.30)
    hips = B.add((0, 0.30, 0.660), (0.136, 0.155, 0.134), WARM_SILVER, "Spine", rot=(-6, 0, 0), top=(0.84, 0.90),
                 bot=(0.85, 0.9), rnd=0.32)
    # final85 M1: ONE continuous dark dorsal band from the nape scruff over chest, waist and hips to the tail root
    dorsal_band(B, (rib, waist, hips))
    # snow underside following the tuck + chest-ruff points (review 2 M1: the flat chest bib is gone; the neck's
    # snow throat seg now runs down to the chest front)
    B.seg((0, -0.31, 0.432), (0, -0.08, 0.418), 0.066, 0.030, SNOW, "Chest", side=(1, 0, 0), top=(0.85, 1),
          ext=0.02, rnd=0.45)                                   # rounded snow underside (no flat plank, final85)
    B.seg((0, -0.06, 0.420), (0, 0.18, 0.543), 0.062, 0.018, SNOW, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    for s in (1, -1):                                       # chest-ruff points between the forelegs, ICE tips (M3)
        frost_point(B, (s * 0.030, -0.355, 0.515), (s * 0.15, -0.30, -1), 0.062, 0.028, "Chest")
    # ---------------- neck (40 deg up) + head (built at draft size, then scaled x HEAD_S about the throat)
    neck = B.seg((0, -0.33, 0.66), (0, -0.53, 0.845), 0.096, 0.106, WARM_SILVER, "Neck", ext=0.05)
    B.seg((0, -0.27, 0.770), (0, -0.50, 0.880), 0.068, 0.040, BACK_SHADE, "Neck", side=(1, 0, 0), ext=0.02,
          top=(0.80, 1), rnd=0.45)                                                          # dark nape scruff
    B.seg((0, -0.385, 0.560), (0, -0.56, 0.785), 0.045, 0.040, SNOW, "Neck", side=(1, 0, 0), ext=0.02, rnd=0.45)    # snow throat
    for t, sx in ((0.30, 1), (0.30, -1), (0.62, 1), (0.62, -1)):        # clip review 3 M1: throat fur tufts
        q = Vector((0, -0.385, 0.560)).lerp(Vector((0, -0.56, 0.785)), t) + Vector((sx * 0.022, -0.020, -0.010))
        B.spike(q, (sx * 0.25, -0.45, -1), 0.058, 0.026, SNOW, "Neck", top=(0.45, 0.60), rnd=0.40)  # r2 T2: plain
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
        B.spike((s * 0.033, -0.757, 0.846), (0, -0.1, -1), 0.066, 0.014, ICE, "Head", role="detail")  # frost fangs (M3)
    # lower jaw + mouth
    B.seg((0, -0.60, 0.818), (0, -0.750, 0.816), 0.056, 0.020, SNOW, "Jaw", top=(0.8, 1), ext=0.02)
    B.add((0, -0.69, 0.837), (0.038, 0.062, 0.005), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    # narrow ice-cyan slit eyes (black socket, vertical pupil) under heavy V brows that cover the eye tops (lids)
    for s in (1, -1):
        rot = (0, -s * 18, s * 20)
        B.add((s * 0.050, -0.700, 0.938), (0.040, 0.008, 0.018), BLACK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.003)
        B.add((s * 0.051, -0.706, 0.937), (0.034, 0.006, 0.0120), ICE, "Head", rot=rot, studs=[], role="detail",
              bevel=0.002)
        B.add((s * 0.051, -0.7200, 0.937), (0.0072, 0.0040, 0.0130), BLACK, "Head", rot=(0, 0, s * 20), studs=[],
              role="detail", bevel=0.0012)                                                  # vertical cat pupil
        B.add((s * 0.047, -0.706, 0.962), (0.046, 0.016, 0.013), BACK_SHADE, "Head", rot=(0, -s * 26, s * 20),
              role="detail", bevel=0.006)                                                   # V brow / lid
    # the lynx beard: snow ruff points flaring sideways from the cheeks, frosted ICE tips (no chin tuft)
    for s in (1, -1):
        rb = "Ruff_L" if s > 0 else "Ruff_R"
        B.add((s * 0.086, -0.640, 0.846), (0.030, 0.048, 0.046), SNOW, rb, rot=(-12, 0, s * 14), bot=(0.8, 0.7),
              rnd=0.40)                                                                     # ruff base (sideburn)
        for y, z, d, L, w in ((-0.664, 0.822, (s * 0.45, 0.35, -0.82), 0.080, 0.027),
                              (-0.645, 0.828, (s * 0.72, 0.45, -0.52), 0.088, 0.030),
                              (-0.622, 0.848, (s * 0.88, 0.50, -0.22), 0.078, 0.029),
                              (-0.610, 0.880, (s * 0.88, 0.48, 0.08), 0.066, 0.024)):
            dn = Vector(d).normalized()                   # snow base (40 %) + frosted ICE tip (60 %, final85 M3)
            B.spike((s * 0.096, y, z), d, L * 0.40, w, SNOW, rb, top=(0.66, 0.70))
            B.spike(Vector((s * 0.096, y, z)) + dn * (L * 0.40 - 0.004), d, L * 0.66 + 0.004, w * 0.74, ICE, rb,
                    top=(0.30, 0.45), role="detail", nostud=True)
    # tall ears with snow fronts and ice tufts (blocks only, no strands)
    for s, side in ((1, "L"), (-1, "R")):
        R = Euler((math.radians(-8), math.radians(s * 6), math.radians(-s * 12)), "XYZ").to_matrix()
        root = Vector((s * 0.060, -0.585, 0.985))
        ear = B.add(root + R @ Vector((0, 0, 0.054)), (0.044, 0.015, 0.058), BACK_SHADE, "Ear_" + side, R=R,
                    top=(0.26, 0.6), rnd=0.25)
        B.add(ear.world((0, -0.015, -0.006)), (0.024, 0.004, 0.040), SNOW, "Ear_" + side, R=R, top=(0.35, 1),
              studs=[], role="detail", bevel=0.003)
        B.add(root + R @ Vector((0, 0, 0.094)), (0.018, 0.0165, 0.020), ICE, "Ear_" + side, R=R, top=(0.35, 0.7),
              studs=[], role="detail", bevel=0.004)                                         # frosted ear tip
        tip = root + R @ Vector((0, 0, 0.100))
        for dx, L in ((-0.25, 0.045), (0.15, 0.040)):                       # the tuft: two short ice pencils
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
                eb, ed = K + Vector((0, 0.035, 0.02)), Vector((0, 0.55, -0.80)).normalized()   # elbow tuft,
                B.spike(eb, ed, 0.030, 0.026, WARM_SILVER, leg, top=(0.62, 0.66))               # frosted tip (M3)
                B.spike(eb + ed * 0.026, ed, 0.030, 0.017, ICE, leg, top=(0.30, 0.45), role="detail", nostud=True)
                lo = B.seg(K, A, 0.056, 0.062, WARM_SILVER, shin, top=(0.86, 0.86), ext=0.03, ext1=0.02, rnd=0.40)
                B.seg(A + Vector((0, 0.002, 0.020)), A, 0.060, 0.064, SNOW, shin, ext1=0.02, rnd=0.40)  # sock (r2: 0.02)
            else:
                up = B.seg(H + Vector((0, 0.03, 0.06)), K, 0.068, 0.112, WARM_SILVER, leg, bot=(0.85, 1),
                           top=(0.75, 0.62), ext=0.0, ext1=0.03, rnd=0.45)
                lo = B.seg(K, A, 0.054, 0.062, WARM_SILVER, shin, top=(0.82, 0.82), ext=0.03, ext1=0.02, rnd=0.40)
                B.seg(A, Pw + Vector((0, 0.03, 0.025)), 0.050, 0.050, WARM_SILVER, foot, ext=0.03, rnd=0.40)
            LEGBLK.append((s, fb, up, lo))
            B.add(Pw, (0.076, 0.088, 0.042), WARM_SILVER, foot, top=(0.86, 0.80), rnd=0.40)     # snowshoe paw (M2)
            B.add((Pw.x, Pw.y, 0.006), (0.078, 0.090, 0.006), SNOW, foot, studs=[], role="detail",
                  bevel=0.003)                                                              # thin snow sole (M2)
            for j, gx in enumerate(CLAWX):
                cb = ("Claw_%s%s%d" % (fb, side, j + 1)) if fb == "F" else foot   # review 3 M2: one bone per claw
                B.spike((Pw.x + gx, Pw.y - 0.076, CLAWZ), CLAWD, 0.095, 0.017, ICE, cb)   # r2 C1: 0.095 x 0.017
    # ---------------- rosette spots: big organic blobs on flanks, shoulders, thighs, upper legs (>= 20 % side view)
    if not nospots:
        for s in (1, -1):
            sd = 11 if s > 0 else 53
            for i, (ly, lz, r, a, ros) in enumerate(((-0.150, 0.080, 0.046, 15, True), (-0.045, 0.110, 0.040, 70, False),
                                                     (0.075, 0.070, 0.048, 40, True), (-0.100, -0.015, 0.042, 120, False),
                                                     (0.015, -0.005, 0.050, 10, True), (0.125, -0.030, 0.038, 80, False),
                                                     (-0.180, -0.070, 0.030, 30, False), (0.180, 0.120, 0.030, 50, False),
                                                     (-0.050, -0.090, 0.032, 100, False), (0.075, -0.095, 0.030, 20, False),
                                                     (0.150, 0.040, 0.028, 70, False))):
                (rosette if ros else blob)(B, rib, s, ly, lz, r, sd + 7 * i, ang=a)
            for i, (ly, lz, r, a, ros) in enumerate(((-0.070, 0.030, 0.046, 30, True), (0.065, 0.050, 0.040, 70, False))):
                (rosette if ros else blob)(B, waist, s, ly, lz, r, sd + 101 + 7 * i, ang=a)
            for i, (ly, lz, r, a, ros) in enumerate(((-0.060, 0.060, 0.048, 15, True), (0.070, 0.035, 0.042, 50, False),
                                                     (-0.010, -0.050, 0.046, 85, True), (0.090, -0.075, 0.034, 20, False),
                                                     (-0.100, -0.060, 0.030, 60, False))):
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
            else:
                rosette(B, up, s, 0.000, -0.050, 0.056, sd, ang=20)
                blob(B, up, s, 0.020, 0.070, 0.036, sd + 3, el=1.2, ang=60)
    # ---------------- short bobtail with a black tip band
    P = [Vector(p) for p in TAILP]
    for i, ((a, b), (w, d)) in enumerate(zip(zip(P, P[1:]), ((0.046, 0.054), (0.046, 0.050), (0.042, 0.046)))):
        B.seg(a, b, w, d, BLACK if i == 2 else WARM_SILVER, "Tail%d" % (i + 1), ext=0.03, top=(0.92, 0.92), rnd=0.40)
    dz = Vector((0, 0, DZ))
    for blk in B.items:
        if blk.bone in BODYB:
            if isinstance(blk, bk.Tube):                  # review 1 M1: the tube mesh is built from rings
                blk.map(lambda q: q + dz)
                continue
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
        k.joint("Ruff_" + side, bz(hs((s * RUFFJ[0], RUFFJ[1], RUFFJ[2]))), "Head", tail=(s * 0.07, 0.02, -0.04))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, Pw = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.12, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
            if fb == "F":
                k.joint("Claw_F" + side, (Pw.x, Pw.y - 0.05, 0.035), "Foot_F" + side, tail=(0, -0.06, -0.02))
                k.joint("FX_IceSpark_" + side, (Pw.x, Pw.y - 0.12, 0.03), "Claw_F" + side, tail=(0, -0.05, 0))
                for j, gx in enumerate(CLAWX):
                    k.joint("Claw_F%s%d" % (side, j + 1), (Pw.x + gx, Pw.y - 0.076, CLAWZ), "Claw_F" + side,
                            tail=(0, -0.05, -0.025))
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
    P += [("Head", "Chest"), ("Jaw", "Chest"), ("Ear_L", "Ear_R"), ("Ruff_L", "Chest"), ("Ruff_R", "Chest")]
    for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR"):
        P += [("Ruff_L", b), ("Ruff_R", b)]
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR"):
        P.append(("Tail1", b))
    return P


def joints():
    return [(bz((0, -0.52, 0.82)), bz((0, -0.56, 0.89)), 0.14, "Head")]


HEAD_XF = []


# ------------------------------------------------------------------ animation (FrostfangLynx/ANIM_REFS.md)
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAILB = ["Tail1", "Tail2", "Tail3"]
H_U = 1.18                       # model height in units (ear-tuft tips, HEIGHT 7.0 studs): 0.05H = 0.059


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


def feet(k, f, T=None):
    """solve all four legs at frame f; T = {leg: (dx, dy, lift)} offsets from the rest ground spot"""
    import bpy
    T = T or {}
    bpy.context.scene.frame_set(f)
    for leg in LEGS4:
        dx, dy, lift = T.get(leg, (0.0, 0.0, 0.0))
        k.solve_leg(leg, f, Vector((k.J[leg].x + dx, k.J[leg].y + dy, lift)))


def ears(k, f, p=0.0, splay=0.0, pr=None):
    """ear tufts: p = pitch (+ forward / pricked, - flattened back), splay = outward roll"""
    k.key("Ear_L", f, rot=(p, 0, -splay))
    k.key("Ear_R", f, rot=(p if pr is None else pr, 0, splay))


def ruffs(k, f, flare=0.0):
    """cheek ruffs (the lynx beard): flare = degrees the ruff lifts out to the side"""
    k.key("Ruff_L", f, rot=(0, 0, -flare))
    k.key("Ruff_R", f, rot=(0, 0, flare))


def bobtail(k, f, lift=0.0, flick=0.0, sway=0.0):
    """short bobtail: lift (- = up), sway on the base, a flick on the black tip"""
    k.key("Tail1", f, rot=(lift, sway, 0))
    k.key("Tail2", f, rot=(0.5 * lift, 0.6 * sway + 0.4 * flick, 0))
    k.key("Tail3", f, rot=(0, flick, 0))


def idle(k):
    """WATCHFUL LOOK-AROUND (ref L1, Figaro): head turns of ~18 f with 10-12 f holds, the neck takes at most 6 deg
    of the yaw, ears follow 4 f late; ear twitch at f70, tail-tip flick at f90; slow breathing."""
    n = 120
    k.new_action("idle", n, True)
    YAW = [(0, 0.0), (8, 0.0), (26, 14.0), (40, 14.0), (58, -8.0), (68, -8.0), (84, 0.0), (120, 0.0)]
    TW = [(0, 0.0), (68, 0.0), (70, 1.0), (72, -0.5), (75, 0.0), (120, 0.0)]           # ear twitch
    FL = [(0, 0.0), (88, 0.0), (91, 1.0), (94, -0.4), (98, 0.0), (120, 0.0)]          # tail-tip flick
    for f in range(0, n + 1, 2):
        yw = tab(YAW, f)
        ylag = tab(YAW, max(0, f - 4))
        b = pk.wave(f, n, 0, 3)
        rb = 0.5 - 0.5 * math.cos(2 * math.pi * 3 * f / n)            # final85 M5: breathing rise 0..0.01H
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, -0.02 * H_U * rb))  # breath: a 0.01H settle + rise (legs never overreach)
        k.key("Chest", f, rot=(-0.6 * b - 1.2 * rb, 0, 0))
        k.key("Neck", f, rot=(0.6 * b, 0.40 * yw, 0))
        k.key("Head", f, rot=(-0.4 * b, 0.60 * yw, -0.15 * yw))
        k.key("Jaw", f, rot=(0.0, 0, 0))                                # review 4: jaw shut at rest
        tw = 3.0 * tab(TW, f)
        ears(k, f, tw, splay=0.15 * ylag, pr=-0.6 * tw)                 # 0 at f0: idle f0 = the acts' rest
        ruffs(k, f, 0.0)
        bobtail(k, f, lift=-2.0 * b, flick=10.0 * tab(FL, f), sway=14.0 * math.sin(2 * math.pi * f / n))  # M5 / r2 C2: 14
    cm.plant(k, n)
    k.finish()
    k.meta["planted"] = list(LEGS4)


def walk(k):
    """LIGHT SNOWSHOE WALK: lateral-sequence cat walk, a springy body (two small lifts per cycle), the head steady
    (cat gyro head), the bobtail lifted a little and bobbing late."""
    n = 24

    def body(f):
        bob = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.5 * pk.wave(f, n, 0.1, 2), 1.8 * pk.wave(f, n), 1.6 * pk.wave(f, n)),
              loc=(0, 0, -0.02 * H_U * bob))                     # springy: 0.02H between contact and passing
        k.key("Chest", f, rot=(0, -2.4 * pk.wave(f, n, 0.25), -1.2 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(1.0 + 1.0 * pk.wave(f, n, 0.15, 2), 0.8 * pk.wave(f, n, 0.25), 0))
        k.key("Head", f, rot=(-1.0 - 1.4 * pk.wave(f, n, 0.20, 2), -1.6 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(0.0, 0, 0))
        ears(k, f, 3.0 + 1.0 * pk.wave(f, n, 0.3, 2))
        ruffs(k, f, 1.5 * pk.wave(f, n, 0.3, 2))
        bobtail(k, f, lift=-6.0 + 3.0 * pk.wave(f, n, 0.35, 2), sway=4.0 * pk.wave(f, n, 0.3))
    return cm.quad_walk(k, n, 0.11, 0.050, body, gait="walk")


def roar(k):
    """RUFF-FLARE THREAT (refs L4 + L5): the shoulders drop 0.05H and the cheek ruffs + ear tufts flare out fast
    (6-8 f, then held); the head drops 8 deg and pushes forward 0.04H twice while the jaw opens to the frost fangs
    (a hiss with a small tremble); it closes and settles, rising slower than it dropped."""
    n = 60
    k.new_action("roar", n, False)
    SH = [(0, 0.0), (14, 1.0), (46, 1.0), (58, 0.0), (60, 0.0)]          # shoulders drop (0.05H)
    FLR = [(0, 0.0), (6, 0.0), (13, 1.0), (48, 1.0), (57, 0.0), (60, 0.0)]  # ruff / tuft flare
    HD = [(0, 0.0), (20, 0.0), (25, 1.0), (46, 1.0), (55, 0.0), (60, 0.0)]  # head drop 8 deg
    PU = [(0, 0.0), (20, 0.0), (26, 1.0), (31, 0.35), (38, 1.0), (44, 0.25), (50, 0.0), (60, 0.0)]  # 2 pushes
    JW = [(0, 0.0), (22, 0.0), (30, 24.0), (44, 24.0), (52, 0.0), (60, 0.0)]
    drop = 0.05 * H_U
    for f in range(0, n + 1):
        sh, fl, hd, pu = tab(SH, f), tab(FLR, f), tab(HD, f), tab(PU, f)
        tr = 1.2 * math.sin(2 * math.pi * f / 4) if 30 <= f <= 44 else 0.0
        k.key("Spine", f, rot=(3.0 * sh, 0, 0), loc=(0, -0.022 * pu, -drop * sh))
        k.key("Chest", f, rot=(2.0 * sh, 0, 0))
        k.key("Neck", f, rot=(-4.0 * sh + 5.0 * pu, 0, 0))
        k.key("Head", f, rot=(8.0 * hd - 1.0 * sh + 0.5 * tr, 0, 0))
        k.key("Jaw", f, rot=(tab(JW, f) + tr, 0, 0))
        ears(k, f, -24.0 * fl, splay=12.0 * fl)
        ruffs(k, f, 20.0 * fl + 0.6 * tr)
        bobtail(k, f, lift=-10.0 * fl, flick=4.0 * math.sin(2 * math.pi * f / 6) * fl)
    cm.plant(k, n)
    k.finish(loop=False)
    k.events["roar"] = {"ruff_flare": round(13 / n, 3), "hiss": round(30 / n, 3)}


def clawflex(k):
    """SIGNATURE act_clawflex - THE CLAW FLEX (refs L2 + L3, Figaro): a fast crouch into a low stare (front lower than
    the rump) with the head turned 14 deg and the tufts flattened; the tufts rise; the left then the right forepaw
    flexes its ice claws up and out (paws stay on the ground, a small knead on the hold, an ICE spark each); the claws
    retract, the bobtail flicks once, it rises back to the exact rest pose. All four paws planted every frame."""
    n = 96
    k.new_action("act_clawflex", n, False)
    CR = [(0, 0.0), (10, 1.0), (72, 1.0), (88, 0.0), (96, 0.0)]                 # crouch 0.10H (L2: ~8-10 f)
    YW = [(0, 0.0), (4, 0.0), (14, 18.0), (40, 18.0), (48, 0.0), (96, 0.0)]     # T3: an 18 deg locked stare
    LK = [(0, 0.0), (40, 0.0), (48, 1.0), (72, 1.0), (84, 0.0), (96, 0.0)]      # look down at the claws
    TF = [(0, 0.0), (4, 0.0), (12, -12.0), (24, -12.0), (34, 4.0), (72, 4.0), (86, 0.0), (96, 0.0)]  # tufts (T3)
    CL = [(0, 0.0), (40, 0.0), (48, 1.0), (72, 1.0), (82, 0.0), (96, 0.0)]      # left claws (claw1 f48)
    CRt = [(0, 0.0), (52, 0.0), (60, 1.0), (72, 1.0), (84, 0.0), (96, 0.0)]     # right claws (claw2 f60)
    PR = [(0, 0.0), (40, 0.0), (47, 1.0), (54, 0.0), (59, -1.0), (66, 0.0), (96, 0.0)]  # shoulder press L / R
    FL = [(0, 0.0), (74, 0.0), (77, 1.0), (80, -0.5), (84, 0.0), (96, 0.0)]     # tail flick
    drop = 0.10 * H_U                                                     # final85 M4: 0.10H (was 0.05H)
    for f in range(0, n + 1):
        c, yw, lk, pr = tab(CR, f), tab(YW, f), tab(LK, f), tab(PR, f)
        kn = math.sin(2 * math.pi * (f - 48) / 8) if 50 <= f <= 70 else 0.0       # knead on the hold
        k.key("Spine", f, rot=(6.0 * c, 0, -1.5 * pr), loc=(0, 0, -drop * c))
        k.key("Chest", f, rot=(3.0 * c, 0, -1.5 * pr))
        k.key("Neck", f, rot=(-5.0 * c + 4.0 * lk, 0.30 * yw, 0))          # neck total <= 7.4 deg (limit 8)
        k.key("Head", f, rot=(-4.0 * c + 6.0 * lk, 0.70 * yw, -0.2 * yw))  # the face stays level in the crouch
        k.key("Jaw", f, rot=(0.0, 0, 0))
        ears(k, f, tab(TF, f))
        ruffs(k, f, 4.0 * lk)
        k.key("Claw_FL", f, rot=(-55.0 * tab(CL, f) + 4.0 * kn * tab(CL, f), 0, 0))     # M4: -55 (was -35)
        k.key("Claw_FR", f, rot=(-55.0 * tab(CRt, f) - 4.0 * kn * tab(CRt, f), 0, 0))
        for side, a in (("L", tab(CL, f)), ("R", tab(CRt, f))):        # review 3 M2: the four claws fan out
            for j, gx in enumerate(CLAWX):
                outer = abs(gx) > 0.03
                k.key("Claw_F%s%d" % (side, j + 1), f,
                      rot=((8.0 if outer else -6.0) * a, math.copysign(18.0 if outer else 6.0, gx) * a, 0))
        bobtail(k, f, lift=-4.0 * c, flick=10.0 * tab(FL, f))
    cm.plant(k, n)
    # ref L3: the flexing paw rolls its toes up 12 deg on the heel (heel stays down: +0.008 to clear the floor)
    import bpy
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        for leg, a in (("Leg_FL", tab(CL, f)), ("Leg_FR", tab(CRt, f))):
            if a > 1e-4:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.008 * a)), toe=-20.0 * a)   # M4: -20
    k.finish(loop=False)
    k.events["act_clawflex"] = {"claw1": round(48 / n, 3), "claw2": round(60 / n, 3),
                                "snow_flick": round(77 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    clawflex(k)
    return stride
