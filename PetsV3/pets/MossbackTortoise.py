# Mossback Tortoise (Wood egg #1, T1 Grass, quad) - FIERCE style (2026-10-09, FIERCE_PLAN.md "the tank"): a giant
# tortoise body on tall columnar elephant legs with an alligator-snapping-turtle head and armour: a high domed shell of
# real scutes (5 vertebral, 4+4 costal, a marginal ring) with 3 rows of keeled pyramid ridges, a serrated back rim of
# 6 saw points and a front HOOD over the neck opening; a wedge skull with a hooked dark beak, heavy brows and narrow
# lime eyes (with eyelid bones for the doze); scaled forelegs, 5/4 black claws, a spiked tail; lime moss tufts in the
# ridge valleys and a fern crest (Tree bone). Old chibi version: _tools/chibi_specs/MossbackTortoise.py
import math
from mathutils import Vector, Matrix, Euler

DISPLAY = "Mossback Tortoise"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 7.0

SHELL = (120, 106, 64)      # olive-brown scutes (Roblox renders ~0.6x darker -> dark tank shell in game)
SHELL_L = (176, 158, 100)   # keel ridges (lit tops)
SEAM = (64, 56, 38)         # seams between scutes / the dark shell interior
SKIN = (118, 130, 102)      # grey-olive reptile skin
SKIN_D = (82, 90, 70)       # brows, neck wrinkles, foot pads
SCALE = (156, 160, 120)     # big armour scales on the forelegs
PLAS = (204, 188, 134)      # plastron, jaw, throat
BEAK = (46, 40, 34)
BLACK = (14, 14, 22)
MOSS = (150, 230, 50)       # THE accent: moss, ferns, eyes
MOSS_D = (100, 172, 40)
EYE = (176, 244, 64)
EYE_HOT = (234, 255, 180)
MOUTH = (96, 34, 36)

PITCH = 0.0445              # stud pitch: 0.042 x (U / U_raiju), U = model height / HEIGHT

ZC, EA, EB, EC = 0.40, 0.64, 0.80, 0.68      # shell dome = upper half-ellipsoid (centre z, semi-axes x, y, z)
# leg joints (left side): hip (inside the shell), elbow/knee (out under the rim), ankle
LEGS = {"F": ((0.30, -0.44, 0.56), (0.50, -0.52, 0.34), (0.47, -0.56, 0.10)),
        "B": ((0.30, 0.44, 0.56), (0.48, 0.50, 0.34), (0.45, 0.54, 0.10))}
NECK0, NECK1 = Vector((0, -0.30, 0.60)), Vector((0, -1.14, 0.63))
EYE_P = (0.128, -1.29, 0.762)               # left eye centre on the skull (skull/snout junction)
EYE_YAW = 42
# faceted dome blocks (centre, half, bottom taper, top taper): each block's top = the next block's bottom
RIM = ((0, 0.0, 0.48), (0.64, 0.80, 0.10), (1, 1), (1, 1))
MID = ((0, 0.0, 0.76), (0.62, 0.776, 0.18), (1, 1), (0.77, 0.79))
MOUTH_X, MOUTH_Y, MOUTH_Z = 0.30, -0.24, 0.88          # shell mouth: half width, back wall y, roof z
CAP = ((0, 0.0, 1.05), (0.477, 0.613, 0.11), (1, 1), (0.60, 0.62))
T0, T1 = Vector((0, 0.72, 0.42)), Vector((0, 1.10, 0.25))


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def frame(xh, n):
    """rotation: local z = n, local x = xh projected onto the plane, local y = z x x"""
    z = Vector(n).normalized()
    x = Vector(xh)
    x = (x - z * x.dot(z)).normalized()
    return Matrix((x, z.cross(x), z)).transposed()


def frame_y(yh, n):
    """rotation: local z = n, local y = yh projected onto the plane, local x = y x z"""
    z = Vector(n).normalized()
    y = Vector(yh)
    y = (y - z * y.dot(z)).normalized()
    return Matrix((y.cross(z), y, z)).transposed()


def face_pt(blk, key, u, v):
    """point, outward normal and the across axis on a face of an unrotated tapered block: u in [-1, 1] across,
    v in [0, 1] bottom edge -> top edge (on '+z': u across x, v in [-1, 1] along y)"""
    c, h, bt, tp = Vector(blk[0]), Vector(blk[1]), blk[2], blk[3]
    if key == "+z":
        return c + Vector((u * h.x * tp[0], v * h.y * tp[1], h.z)), Vector((0, 0, 1)), Vector((1, 0, 0))
    ax = 0 if key[1] == "x" else 1
    ot = 1 - ax
    sg = 1 if key[0] == "+" else -1
    ea, eo = Vector((0, 0, 0)), Vector((0, 0, 0))
    ea[ax], eo[ot] = sg, 1
    xa = h[ax] * (bt[ax] + (tp[ax] - bt[ax]) * v)
    ac = h[ot] * (bt[ot] + (tp[ot] - bt[ot]) * v)
    p = c + ea * xa + eo * (u * ac) + Vector((0, 0, -h.z + 2 * h.z * v))
    along = ea * (h[ax] * (tp[ax] - bt[ax])) + Vector((0, 0, 2 * h.z))
    n = eo.cross(along).normalized()
    if n.dot(ea) < 0:
        n = -n
    return p, n, eo


def fern_base():
    return face_pt(CAP, "-x", -0.55, 0.15)[:2]


def dome(a, b):
    """point + outward normal on the shell dome; a = lateral angle from the top (deg, + toward +x), b = toward the tail"""
    ra, rb = math.radians(a), math.radians(b)
    u = Vector((math.sin(ra) * math.cos(rb), math.sin(rb), math.cos(ra) * math.cos(rb)))
    p = Vector((EA * u.x, EB * u.y, ZC + EC * u.z))
    return p, Vector((u.x / EA, u.y / EB, u.z / EC)).normalized()


def eye_frames(s):
    R = Euler((0, math.radians(-s * 18), math.radians(s * EYE_YAW)), "XYZ").to_matrix()
    Rb = Euler((0, math.radians(-s * 26), math.radians(s * (EYE_YAW - 12))), "XYZ").to_matrix()
    return R, Rb


def lid_hinge(s):
    R, _ = eye_frames(s)
    return X(EYE_P, s) + R @ Vector((0, -0.017, 0.030))


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=41, tier=1, plates=False, th=0.60)
    # ---------------- shell: a faceted dome of 3 continuously tapered dark blocks (no ledges) covered in flat
    # scute tiles (the dark gaps = seams); a cavity at the front of the rim (neck + forelegs retract into it)
    B.seg((0, 0.70, 0.37), (0, -0.72, 0.37), 0.52, 0.05, PLAS, "Spine", top=(0.52, 1), role="mass")     # plastron
    B.add((0, 0.28, 0.48), (0.64, 0.52, 0.10), SEAM, "Spine", rnd=0.3, role="mass")                     # rim
    for s in (1, -1):
        B.add((s * 0.47, -0.52, 0.48), (0.17, 0.28, 0.10), SEAM, "Spine", rnd=0.3, role="mass")       # rim corners
    # MID split round the mouth: back block, 2 side walls, a roof (top_shift keeps the outer faces = MID's faces)
    (mc, mh, _, mt) = MID
    zt = mc[2] + mh[2]
    ytop = mh[1] * mt[1]
    xtop = mh[0] * mt[0]
    yb0, yb1 = MOUTH_Y, mh[1]
    B.add((0, (yb0 + yb1) / 2, mc[2]), (mh[0], (yb1 - yb0) / 2, mh[2]), SEAM, "Spine",
          top=(mt[0], (ytop - yb0) / (yb1 - yb0)), top_shift=(0, (yb0 + ytop) / 2 - (yb0 + yb1) / 2), rnd=0.3,
          role="mass")
    for s in (1, -1):
        x0, x1b, x1t = MOUTH_X, mh[0], xtop
        y0b, y0t = -mh[1], -ytop
        B.add((s * (x0 + x1b) / 2, (y0b + MOUTH_Y) / 2, mc[2]), ((x1b - x0) / 2, (MOUTH_Y - y0b) / 2, mh[2]), SEAM,
              "Spine", top=((x1t - x0) / (x1b - x0), (MOUTH_Y - y0t) / (MOUTH_Y - y0b)),
              top_shift=(s * ((x0 + x1t) / 2 - (x0 + x1b) / 2), (y0t + MOUTH_Y) / 2 - (y0b + MOUTH_Y) / 2), rnd=0.3,
              role="mass")
    yr0 = -mh[1] * (1 - (1 - mt[1]) * (MOUTH_Z - (mc[2] - mh[2])) / (2 * mh[2]))      # MID front at the roof bottom
    B.add((0, (yr0 + MOUTH_Y) / 2, (MOUTH_Z + zt) / 2), (MOUTH_X + 0.02, (MOUTH_Y - yr0) / 2, (zt - MOUTH_Z) / 2),
          SEAM, "Spine", top=(1, (MOUTH_Y + ytop) / (MOUTH_Y - yr0)),
          top_shift=(0, ((-ytop + MOUTH_Y) - (yr0 + MOUTH_Y)) / 2), role="mass")                     # roof
    B.add((0, (MOUTH_Y - 0.776) / 2, 0.428), (MOUTH_X, (0.776 + MOUTH_Y) / 2, 0.01), SEAM, "Spine", nostud=True,
          role="limb")                                                                                   # dark floor
    B.add(CAP[0], CAP[1], SEAM, "Spine", bot=CAP[2], top=CAP[3], rnd=0.3, role="mass")

    def tile(blk, key, u, v, hu, hv, t=0.08, keel=0.0, kw=0.0, col=SHELL):  # noqa: E741
        p, n, ax = face_pt(blk, key, u, v)
        B.add(p + n * (t / 2 - 0.014), (hu, hv, t / 2), col, "Spine", R=frame(ax, n), top=(0.80, 0.80), rnd=0.3,
              role="limb")
        if keel:
            nk = (n + Vector((0, 0.30 if key in ("+z", "-y", "+y") else 0.12, 0))).normalized()
            B.add(p + n * (t - 0.03) + nk * keel / 2, (kw, kw * 1.6, keel / 2), SHELL_L, "Spine",
                  R=frame_y((0, 1, 0), nk), top=(0.14, 0.40), rnd=0.18, role="limb")
        return p, n
    # vertebral row (5 big keels, 0.10 S): cap front slope, 3 on the cap top, cap back slope
    tile(CAP, "-y", 0, 0.5, 0.21, 0.13, keel=0.15, kw=0.08)
    for v in (-0.62, 0.0, 0.62):
        tile(CAP, "+z", 0, v, 0.215, 0.105, keel=0.17, kw=0.085)
    tile(CAP, "+y", 0, 0.5, 0.21, 0.13, keel=0.15, kw=0.08)
    for key in ("+x", "-x"):
        for u in (-0.62, 0.0, 0.62):
            tile(CAP, key, u, 0.5, 0.15, 0.13)
        for u in (-0.75, -0.25, 0.25, 0.75):                  # costal rows (0.07 S keels)
            tile(MID, key, u, 0.5, 0.158, 0.17, keel=0.14, kw=0.078)
        for u in (-0.8, -0.4, 0.0, 0.4, 0.8):                 # marginals
            tile(RIM, key, u, 0.5, 0.135, 0.088)
    for key in ("-y", "+y"):
        for u in ((-0.62, 0.0, 0.62) if key == "+y" else (-0.70, 0.70)):    # front: 2 cheeks round the mouth
            tile(MID, key, u, 0.5, 0.16 if key == "+y" else 0.12, 0.17)
    for u in (-0.75, 0.75):
        tile(RIM, "-y", u, 0.5, 0.135, 0.088)
    for blk, v, hu, hv in ((CAP, 0.5, 0.10, 0.12), (MID, 0.5, 0.12, 0.16), (RIM, 0.5, 0.10, 0.088)):
        for sx in (1, -1):
            for sy in (1, -1):
                if blk is RIM and sy < 0:
                    continue
                p1, n1, _ = face_pt(blk, "+x" if sx > 0 else "-x", sy, v)
                p2, n2, _ = face_pt(blk, "+y" if sy > 0 else "-y", sx, v)
                n = (n1 + n2).normalized()
                ax = n.cross(Vector((0, 0, 1))).normalized()
                B.add(p1 + n * (0.04 - 0.03), (hu, hv, 0.04), SHELL, "Spine", R=frame(ax, n), top=(0.8, 0.8), rnd=0.3,
                      role="limb")
    # serrated back rim: 6 saw points under the back + rear-side marginals
    for key, u in (("+y", -0.75), ("+y", -0.25), ("+y", 0.25), ("+y", 0.75), ("+x", 0.8), ("-x", -0.8)):
        if key == "-x":
            u = 0.8
        p, n, ax = face_pt(RIM, key, u, 0.15)
        B.spike(p + n * 0.02, n + Vector((0, 0.35, -0.55)), 0.16, 0.07, SHELL, "Spine", side=ax, top=(0.08, 0.35))
    # front HOOD: a raised brim over the top edge of the mouth (~0.12 overhang)
    B.add((0, -0.75, 0.875), (0.32, 0.105, 0.045), SHELL, "Spine", rot=(14, 0, 0), top=(0.84, 0.84), rnd=0.3,
          role="limb")
    B.add((0, -0.785, 0.915), (0.06, 0.085, 0.035), SHELL_L, "Spine", rot=(14, 0, 0), top=(0.25, 0.6), role="limb")
    # moss tufts (accent) in the valleys between the ridge rows
    for blk, key, u, v, sc in ((CAP, "+x", -0.40, 0.05, 1.3), (CAP, "-x", 0.15, 0.05, 1.17), (CAP, "+x", 0.70, 0.08, 1.04),
                               (MID, "-x", -0.45, 0.97, 1.1), (CAP, "+y", 0.6, 0.1, 1.0), (MID, "+x", 0.55, 0.97, 1.1),
                               (MID, "-x", 0.55, 0.97, 1.05)):
        p, n, ax = face_pt(blk, key, u, v)
        R = frame(ax, n)
        B.add(p + n * 0.03, (0.10 * sc, 0.075 * sc, 0.05), MOSS_D, "Spine", R=R, rnd=0.4, role="limb")
        B.add(p + n * 0.07 + R @ Vector((0.035 * sc, 0.01, 0)), (0.055 * sc, 0.05 * sc, 0.045 * sc), MOSS, "Spine", R=R,
              rnd=0.4, role="limb")
        B.add(p + n * 0.06 + R @ Vector((-0.05 * sc, -0.02, 0)), (0.04 * sc, 0.04 * sc, 0.04), MOSS, "Spine", R=R,
              rnd=0.4, role="limb")
        for ang in (40, 160, 280):
            d = R @ Vector((math.cos(math.radians(ang)), math.sin(math.radians(ang)), 1.3))
            B.spike(p + n * 0.05, d, 0.11 * sc, 0.022, MOSS, "Spine", side=n.cross(d), top=(0.1, 1))
    # fern crest (Tree bone): broad pointed fronds from one valley
    fp, fn = fern_base()
    for d, L, col in (((-0.2, -0.3, 1), 0.32, MOSS), ((-0.75, 0.1, 0.7), 0.28, MOSS_D), ((0.3, 0.45, 0.9), 0.26, MOSS),
                      ((-0.45, 0.7, 0.6), 0.24, MOSS_D)):
        dv = Vector(d).normalized()
        B.seg(fp, fp + dv * L, 0.055, 0.015, col, "Tree", side=(-dv.y, dv.x, 0), top=(0.12, 1), ext=0.03, role="limb")
    B.add(fp + fn * 0.02, (0.07, 0.07, 0.05), MOSS_D, "Tree", R=frame((1, 0, 0), fn), rnd=0.4, role="limb")
    # ---------------- neck: thick, 2 wrinkle rings, pale throat, a few tubercles
    nd = (NECK1 - NECK0).normalized()
    B.seg(NECK0, NECK1, 0.13, 0.13, SKIN, "Neck", ext=0.02, ext1=0.04, rnd=0.30)
    B.seg(NECK0 + Vector((0, -0.08, -0.115)), NECK1 + Vector((0, 0, -0.112)), 0.09, 0.02, PLAS, "Neck")
    for t in (0.42, 0.66):
        c = NECK0.lerp(NECK1, t)
        B.seg(c - nd * 0.02, c + nd * 0.02, 0.142, 0.142, SKIN_D, "Neck", rnd=0.3, role="limb")
    for s in (1, -1):
        for t, dz in ((0.30, 0.06), (0.55, 0.0), (0.82, 0.05)):
            c = NECK0.lerp(NECK1, t) + Vector((s * 0.12, 0, dz))
            B.spike(c, (s, 0.3, 0.2), 0.05, 0.022, SKIN_D, "Neck")
    # ---------------- head: wide-backed wedge skull (snapper), jaw-muscle bulges, dark crown, hooked beak
    B.seg((0, -1.04, 0.745), (0, -1.46, 0.675), 0.20, 0.15, SKIN, "Head", top=(0.50, 0.42), rnd=0.22, role="mass")
    for s in (1, -1):
        B.add((s * 0.15, -1.13, 0.645), (0.05, 0.09, 0.06), SKIN, "Head", rot=(-15, 0, s * 12), top=(0.6, 0.6),
              rnd=0.45, role="limb")                                                                        # cheeks
    B.seg((0, -1.05, 0.885), (0, -1.30, 0.825), 0.15, 0.026, SKIN_D, "Head", top=(0.55, 1), role="limb")   # crown
    B.seg((0, -1.34, 0.705), (0, -1.60, 0.655), 0.112, 0.068, BEAK, "Head", top=(0.55, 0.6), rnd=0.2, role="limb")
    B.seg((0, -1.565, 0.69), (0, -1.645, 0.548), 0.06, 0.045, BEAK, "Head", top=(0.35, 0.45), role="limb")  # hook
    for s in (1, -1):
        B.add((s * 0.032, -1.545, 0.69), (0.013, 0.016, 0.008), BLACK, "Head", rot=(-14, 0, 0), studs=[],
              role="detail", bevel=0.003)                                                                # nostrils
    B.add((0, -1.30, 0.585), (0.075, 0.19, 0.006), MOUTH, "Head", studs=[], role="detail", bevel=0.003)   # mouth roof
    # lower jaw (Jaw): pale, dark lower beak tucked behind the hook, mouth, chin barbels
    B.seg((0, -1.09, 0.56), (0, -1.55, 0.57), 0.17, 0.06, SKIN, "Jaw", top=(0.42, 0.40), rnd=0.25)
    B.seg((0, -1.11, 0.503), (0, -1.50, 0.546), 0.13, 0.012, PLAS, "Jaw", top=(0.50, 1), role="limb")   # pale chin
    B.seg((0, -1.42, 0.578), (0, -1.585, 0.585), 0.08, 0.05, BEAK, "Jaw", top=(0.5, 0.7), role="limb")
    B.add((0, -1.29, 0.615), (0.07, 0.17, 0.006), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike((s * 0.10, -1.19, 0.535), (s * 0.3, 0.2, -1), 0.06, 0.024, SKIN_D, "Jaw")
    # eyes (+ lids, hidden at rest under the brow; they swing down to close)
    for s, side in ((1, "L"), (-1, "R")):
        R, Rb = eye_frames(s)
        c = X(EYE_P, s)

        def P(Rm, dx, dy, dz):
            return c + Rm @ Vector((s * dx, dy, dz))
        B.add(P(R, 0, 0, 0), (0.056, 0.012, 0.027), BLACK, "Head", R=R, studs=[], role="detail", bevel=0.004)
        B.add(P(R, 0.002, -0.009, 0), (0.047, 0.006, 0.0145), EYE, "Head", R=R, studs=[], role="detail", bevel=0.003)
        B.add(P(R, 0.010, -0.014, 0.002), (0.020, 0.004, 0.007), EYE_HOT, "Head", R=R, studs=[], role="detail",
              bevel=0.002)
        B.add(P(Rb, -0.016, -0.011, 0.054), (0.11, 0.05, 0.042), SKIN_D, "Head", R=Rb, role="detail", bevel=0.012)
        for dz, dy, L in ((0.03, 0.10, 0.055), (-0.02, 0.10, 0.05), (-0.055, 0.04, 0.045)):    # fleshy tubercles
            B.spike(c + Vector((-s * 0.01, 0.06, dz)), (s * 0.5, dy * 6, dz * 4), L, 0.02, SKIN_D, "Head")
        H = lid_hinge(s)
        Ro = R @ Matrix.Rotation(math.radians(90), 3, "X")
        B.add(H + R @ Vector((0, 0.033, 0)), (0.060, 0.007, 0.033), SKIN, "Lid_" + side, R=Ro, studs=[],
              role="detail", bevel=0.004)
    # ---------------- columnar legs: upper (in the shell), scaled column, round pad foot with black claws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A = (X(p, s) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            B.seg(H, K, 0.115, 0.12, SKIN, leg, ext=0.04, ext1=0.06, rnd=0.3)
            B.seg(K, A, 0.14, 0.14, SKIN, shin, ext=0.07, bot=(0.95, 0.95), top=(1.08, 1.06), rnd=0.3)
            B.add((A.x, A.y - 0.015, 0.055), (0.165, 0.17, 0.055), SKIN_D, foot, top=(0.9, 0.88), rnd=0.3)
            nc = 5 if fb == "F" else 4
            for i in range(nc):
                gx = (i - (nc - 1) / 2) * (0.27 / (nc - 1))
                B.spike((A.x + gx, A.y - 0.165, 0.04), (gx * 0.6, -1, -0.5), 0.08, 0.022, BLACK, foot)
            # big overlapping armour scales: front face of the forelegs (3 rows), heel of the hind legs
            if fb == "F":
                for r, t in enumerate((0.10, 0.40, 0.70)):
                    for cx in ((-0.065, 0.065) if r != 1 else (0.0,)):
                        c = K.lerp(A, t) + Vector((cx, -0.148, 0))
                        B.add(c, (0.068 if r != 1 else 0.10, 0.025, 0.068), SCALE, shin, rot=(-12, 0, 0),
                              bot=(0.82, 1), rnd=0.3, role="limb")
                for t in (0.25, 0.6):
                    c = K.lerp(A, t) + Vector((s * 0.15, -0.03, 0))
                    B.add(c, (0.025, 0.06, 0.055), SCALE, shin, bot=(1, 0.6), role="limb")
            else:
                for t in (0.3, 0.65):
                    c = K.lerp(A, t) + Vector((0, 0.15, 0))
                    B.add(c, (0.08, 0.025, 0.06), SCALE, shin, rot=(12, 0, 0), bot=(0.6, 1), role="limb")
    # ---------------- spiked tail
    B.seg(T0, T1, 0.085, 0.07, SKIN_D, "Tail1", top=(0.22, 0.32), ext=0.05, rnd=0.3)
    for t, ln, rd in ((0.16, 0.09, 0.040), (0.45, 0.075, 0.034), (0.74, 0.06, 0.028)):   # 3 big dorsal spikes
        c = T0.lerp(T1, t) + Vector((0, 0, 0.055 * (1 - t * 0.7)))
        B.spike(c, (0, 0.7, 1), ln, rd, SHELL, "Tail1")
    for s in (1, -1):                                                   # + a side pair -> spiked from behind too
        c = T0.lerp(T1, 0.30) + Vector((s * 0.06, 0, 0.0))
        B.spike(c, (s, 0.6, 0.35), 0.05, 0.024, SHELL, "Tail1")
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.0, 0.56), "Root", tail=(0, -0.4, 0))
    fp, fn = fern_base()
    k.joint("Tree", tuple(fp), "Spine", tail=tuple(fn * 0.3))
    k.joint("Neck", tuple(NECK0), "Spine", tail=(0, -0.4, 0.1))
    k.joint("Head", (0, -1.09, 0.60), "Neck", tail=(0, -0.4, 0))              # throat pivot
    k.joint("Jaw", (0, -1.12, 0.60), "Head", tail=(0, -0.3, 0))
    for s, side in ((1, "L"), (-1, "R")):
        R, _ = eye_frames(s)
        k.joint("Lid_" + side, tuple(lid_hinge(s)), "Head", tail=tuple(R @ Vector((0, 0.06, 0))))
        for fb in ("F", "B"):
            H, K, A = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, "Spine")
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.25, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=(s, 0, 0))
    k.joint("Tail1", tuple(T0), "Spine", tail=tuple((T1 - T0).normalized() * 0.3))


# ------------------------------------------------------------------ animation (FIERCE_PLAN: doze / stand-tall hiss /
# act_hide). Conventions: k.key rot = (pitch, yaw, roll) deg in armature axes relative to the parent; pitch + tips a
# -Y bone's nose DOWN; Neck loc moves the whole head chain (armature axes).
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
FERN_B = "Tree"


def lids(k, f, l=0.0, r=None):
    """0 = open (lid tucked under the brow) .. 1 = closed (swung down over the slit)"""
    r = l if r is None else r
    for side, a in (("L", l), ("R", r)):
        s = 1 if side == "L" else -1
        R, _ = eye_frames(s)
        cm.key_axis(k, "Lid_" + side, f, R @ Vector((1, 0, 0)), -92 * a)


def head(k, f, nk=0.0, ny=0.0, ly=0.0, lz=0.0, hd=0.0, hy=0.0, jaw=0.0):
    k.key("Neck", f, rot=(nk, ny, 0), loc=(0, ly, lz))
    k.key("Head", f, rot=(hd, hy, 0))
    k.key("Jaw", f, rot=(jaw, 0, 0))


def fern(k, f, n, amp=1.0, pitch=0.0):
    k.key(FERN_B, f, rot=(amp * 3 * pk.wave(f, n, 0, 2) + pitch, 0, amp * 4 * pk.wave(f, n, 0.3, 2)))


def ankle_target(k, leg, A):
    """ground-point T for solve_leg that puts the ankle at world point A"""
    L = k.legs2[leg]
    hipR, ankR = k.J[leg], k.J[L["foot"]]
    return Vector((A.x - (ankR.x - hipR.x), A.y - (ankR.y - hipR.y), A.z - ankR.z))


def idle(k):
    """DOZE: sleeps standing. The neck sinks until the chin rests on the ground, the lids close, two slow breaths
    lift the shell, one lid cracks open to look and closes again, then the head drifts back up (loops)."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        br = 0.0
        for c in (48, 88):
            if c - 14 <= f <= c + 14:
                br += 0.5 + 0.5 * math.cos(math.pi * (f - c) / 14)
        k.key("Spine", f, rot=(-0.6 * br, 0, 0), loc=(0, 0, 0.016 * br))
        fern(k, f, n, 0.6)
        k.key("Tail1", f, rot=(0, 3 * pk.wave(f, n, 0.1, 1), 0))
    for f, nk, ly, hd, hy in ((0, 0, 0, 0, 0), (6, 2, 0, -1, 0), (25, 29, -0.02, -27, 0), (66, 29, -0.02, -27, 0),
                              (70, 28, -0.02, -27, 8), (76, 28, -0.02, -27, 8), (80, 29, -0.02, -27, 0),
                              (95, 29, -0.02, -27, 0), (112, 3, 0, -2, 0), (120, 0, 0, 0, 0)):
        head(k, f, nk=nk, ly=ly, hd=hd, hy=hy)
    for f, l, r in ((0, 0, 0), (25, 0, 0), (35, 1, 1), (68, 1, 1), (72, 0.35, 1), (77, 0.35, 1), (80, 1, 1),
                    (100, 1, 1), (110, 0, 0), (120, 0, 0)):
        lids(k, f, l, r)
    cm.plant(k, n, legs=LEGS4)
    k.finish()


def walk(k):
    n = 40

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.5 * pk.wave(f, n, 0.1, 2), 1.2 * pk.wave(f, n, 0.0), 2.6 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.015 * b))
        head(k, f, nk=2 * pk.wave(f, n, 0.15, 2), ny=3 * pk.wave(f, n, 0.25), ly=-0.04 * pk.wave(f, n, 0.1, 2),
             hd=-2 * pk.wave(f, n, 0.15, 2), hy=-2 * pk.wave(f, n, 0.25))
        k.key("Tail1", f, rot=(0, 7 * pk.wave(f, n, 0.3), 0))
        fern(k, f, n, 0.8)
        lids(k, f, 0)
    return cm.quad_walk(k, n, 0.10, 0.08, body, gait="walk")


def roar(k):
    """STAND TALL & HISS: straightens all 4 legs (the shell rises as far as the columns reach), shoots the neck up and
    out, beak gapes wide with a trembling hiss (the moss shakes), one hard SNAP, sinks back down."""
    n = 60
    k.new_action("roar", n, False)
    for f, z, sp, nk, ly, hd, jaw in ((0, 0, 0, 0, 0, 0, 0), (12, 0.045, -4, 2, 0, 0, 0), (20, 0.045, -4, -30, -0.07, 6, 6),
                                      (24, 0.045, -4, -31, -0.08, 7, 34), (44, 0.045, -4, -31, -0.08, 7, 33),
                                      (46, 0.045, -4, -33, -0.09, 8, 0), (48, 0.04, -4, -30, -0.08, 6, 2),
                                      (54, 0.01, -1, -6, -0.01, 1, 0), (60, 0, 0, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        head(k, f, nk=nk, ly=ly, hd=hd, jaw=jaw)
        lids(k, f, 0)
    for f in range(26, 44, 2):
        k.key("Jaw", f, rot=(33 + (3 if (f // 2) % 2 else -3), 0, 0))
    for f in range(0, n + 1, 2):
        shake = 5 * math.sin(f * 1.9) if 22 <= f <= 46 else 0.0
        k.key(FERN_B, f, rot=(shake, 0, -shake * 0.6))
        k.key("Tail1", f, rot=(10 if 12 <= f <= 48 else 0, 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def hide(k):
    """SIGNATURE act_hide - RETREAT INTO THE SHELL: startled awake it jerks its head up, then withdraws fast: the
    neck slides back into the mouth, the scaled forelegs swing in to plug the opening, the hind legs fold, the tail
    tucks and the shell THUDS onto its plastron. Holds (one rock), peeks out half way, looks left and right, snaps back
    in, then the legs push the shell up and the neck extends to rest with a small overshoot."""
    import bpy
    n = 96
    DROP = -0.26
    k.new_action("act_hide", n, False)
    # shell height + rock (f, z, pitch, roll)
    for f, z, p, r in ((0, 0, 0, 0), (8, 0, 0, 0), (14, 0.01, -2, 0), (18, -0.10, 0, 0), (22, DROP, 0, 0),
                       (24, DROP + 0.012, 1.5, 0), (27, DROP, 0, 0), (32, DROP, 0, 0), (34, DROP, 0, 2), (37, DROP, 0, -1),
                       (40, DROP, 0, 0), (82, DROP, 0, 0), (90, 0.01, -1, 0), (93, -0.004, 0.5, 0), (96, 0, 0, 0)):
        k.key("Spine", f, rot=(p, 0, r), loc=(0, 0, z))
    # neck / head: startle, withdraw deep, peek (look L / R), snap in, emerge with an overshoot
    IN = 0.97
    for f, nk, ny, ly, lz, hd, hy, jaw in ((0, 0, 0, 0, 0, 0, 0, 0), (8, 0, 0, 0, 0, 0, 0, 0),
                                           (11, -10, 0, 0.02, 0, -2, 0, 4), (14, -10, 0, 0.02, 0, -2, 0, 0),
                                           (17, -4, 0, 0.50, 0.0, 0, 0, 0), (20, 0, 0, IN, 0.0, 0, 0, 0),
                                           (48, 0, 0, IN, 0.0, 0, 0, 0), (56, -2, 0, 0.47, 0.0, 2, 0, 0),
                                           (60, -2, 0, 0.47, 0.0, 2, 0, 0), (63, -2, 4, 0.47, 0.0, 2, 24, 0),
                                           (67, -2, 4, 0.47, 0.0, 2, 24, 0), (70, -2, -4, 0.47, 0.0, 2, -24, 0),
                                           (72, -2, -4, 0.47, 0.0, 2, -24, 0), (74, 0, 0, IN, 0.0, 0, 0, 0),
                                           (84, 0, 0, IN, 0.0, 0, 0, 0), (91, -3, 0, -0.03, 0, -1, 0, 0),
                                           (94, 1, 0, 0.0, 0, 0.5, 0, 0), (96, 0, 0, 0, 0, 0, 0, 0)):
        head(k, f, nk=nk, ny=ny, ly=ly, lz=lz, hd=hd, hy=hy, jaw=jaw)
    for f, a in ((0, 0), (10, 0), (12, 0), (48, 0), (96, 0)):
        lids(k, f, a)
    for f, tp, ty in ((0, 0, 0), (14, 0, 0), (22, 30, 0), (84, 30, 0), (92, -4, 0), (96, 0, 0)):
        k.key("Tail1", f, rot=(tp, ty, 0))
    for f, fp in ((0, 0), (20, 0), (23, -12), (26, 6), (30, 0), (34, 4), (38, 0), (90, -6), (94, 2), (96, 0)):
        k.key(FERN_B, f, rot=(fp, 0, 0))
    k.bake_bezier_now()

    def tuck(f):
        if f <= 15 or f >= 92:
            return 0.0
        if f < 23:
            u = (f - 15) / 8
        elif f <= 82:
            return 1.0
        else:
            u = 1 - (f - 82) / 10
        return 0.5 - 0.5 * math.cos(math.pi * u)

    def part(f):
        for a, b, c, d in ((46, 52, 74, 78), (78, 82, 92, 94)):
            if a < f < d:
                u = (f - a) / (b - a) if f < b else 1.0 if f <= c else 1 - (f - c) / (d - c)
                return 0.5 - 0.5 * math.cos(math.pi * u)
        return 0.0

    sc = bpy.context.scene
    sp = k.arm.pose.bones["Spine"]
    sp_rest_inv = k.arm.data.bones["Spine"].matrix_local.inverted()
    for f in range(0, n + 1):
        sc.frame_set(f)
        M = sp.matrix @ sp_rest_inv
        u = tuck(f)
        for leg in LEGS4:
            s = 1 if leg.endswith("L") else -1
            T = Vector((k.J[leg].x, k.J[leg].y, 0.0))
            if u > 0:
                if leg[4] == "F":        # forelegs: elbows out, forearms across the mouth (scaled faces out); they
                    o = part(f)          # part to let the head peek out
                    A = M @ Vector((s * (0.20 + 0.30 * o), -0.86 + 0.06 * o, 0.55 - 0.02 * o))
                else:                    # hind legs: folded flat beside the plastron
                    A = M @ Vector((s * 0.50, 0.58, 0.40))
                    A.z = max(A.z, 0.13)
                T = T.lerp(ankle_target(k, leg, A), u)
            k.solve_leg(leg, f, T, toe=(0.0 if leg[4] == "B" else 60 * u) if u > 0 else None)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    hide(k)
    return stride


def check_pairs():
    P = [("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"), ("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR"):
        P.append(("Tail1", b))
    return P


def joints():
    """the lids hinge inside the brow (rest contact) - nothing else"""
    return []


HEAD_XF = []
