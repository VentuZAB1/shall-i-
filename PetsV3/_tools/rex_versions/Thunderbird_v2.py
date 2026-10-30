# Thunderbird v2 (Storm egg, NEW 5% pet, 2026-10-14) - FIERCE style "THE STORM HERALD" (review 1 brief): a giant
# thunder eagle built from tapered blocks under a Roblox stud skin, in the family of our approved flyers (Griffin's
# 3-row feather wing + eagle head, Storm Wyvern's keel + flight muscles). Eagle posture: a big keeled storm-TEAL breast
# leaning 46 deg, the knee hidden in the belly, dark storm trousers over bare gold tarsi and black hooked talons. HERO:
# THUNDER WINGS - every primary, tail and crest feather ends in a kinked 2-step lightning bolt (BOLT -> HOT). White
# bald-eagle head with a fused white brow and a harpy double crest, a white bolt-tipped tail fan, a storm mantle and
# breast shingles. Ground pose = the CLOAK FOLD (wings along the flanks). No glow (lightning = Studio VFX anchors).
# Old version: _tools/rex_versions/Thunderbird_v1.py
import math
import os
from mathutils import Vector, Euler, Matrix
import wing3

DISPLAY = "Thunderbird"
MOTION = "Fly"
RIG = "wingbiped"
HEIGHT = 8.5

# Blender colours (Roblox renders ~0.6x darker)
STORM = (26, 80, 100)        # back mantle, folded-wing outside (secondaries), trousers, tail base, crest band
PRIMARY = (16, 46, 62)       # primary + tail-feather bodies (max contrast for the bolts)
TEAL = (36, 138, 160)        # breast, belly, shoulders, upper skirt, arm bar
COVERT = (82, 176, 190)      # upper-wing coverts, top breast row, secondary tip edges
WHITE = (236, 240, 248)      # head, ruff, bib, tail fan
WHITE_D = (194, 206, 224)    # brow ridge, ruff shading, nape hackles
GOLD = (246, 166, 38)        # beak, cere, tarsus, toes
GOLD_D = (204, 120, 24)      # hook, scale bands
BOLT = (255, 234, 56)        # HERO accent: lightning tips, iris
HOT = (255, 252, 214)        # bolt points, eye hot spot
BLACK = (14, 14, 22)
MOUTH = (96, 26, 30)

HC = Vector((0, -0.46, 1.50))                      # cranium centre
H_MODEL = 1.86                                     # crest tips
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)

HIP, KNEE, ANKLE, TOE = (0.14, 0.12, 0.62), (0.16, -0.04, 0.50), (0.16, 0.07, 0.22), (0.16, -0.05, 0.035)
TAILP = [(0, 0.26, 0.60), (0, 0.44, 0.48), (0, 0.66, 0.36)]
TAIL_SPREAD = float(os.environ.get("TB_TS", "38"))   # rest fan half-angle (deg)
ANCH = {}

# wing: designed flat, raised ELEV deg about the root line for the bind pose (Griffin recipe); the root sits ON the
# shoulder (review: +0.07 x so the cloak fold lays the wing along the flank without cutting the breast)
ELEV = 16.0
WDX = float(os.environ.get("TB_DX", "0.15"))     # wing x offset vs v1 (review: +0.07; fold tests may override)
_S0, _BB0 = Vector((0.20 + WDX, -0.10, 1.16)), Vector((0.17 + WDX, 0.22, 0.98))
_ROT = Matrix.Rotation(math.radians(-ELEV), 3, (_BB0 - _S0).normalized())


def _raise(p):
    return _S0 + _ROT @ (Vector(p) - _S0)


_W, _H2, _T = _raise((0.86 + WDX, -0.04, 1.32)), _raise((0.72 + WDX, 0.62, 1.12)), _raise((1.72 + WDX, 0.30, 1.42))
_N = (_T - _W).cross(_H2 - _W).normalized()
if _N.z < 0:
    _N = -_N
WING = wing3.Wing(S=tuple(_S0), W=tuple(_W), H=tuple(_W + _N * 0.30), BB=tuple(_BB0))
H2 = tuple(_H2)
TIP = tuple(_T)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def frame(z, n):
    z = Vector(z).normalized()
    x = Vector(n)
    x = (x - z * x.dot(z)).normalized()
    return Matrix((x, z.cross(x), z)).transposed()


def bolt(B, p, d, L, w, nrm, thick, bone, flip=1):
    """kinked 2-step lightning tip in the feather plane: BOLT jog one way (55 %), HOT point jogs back (45 %)"""
    d = Vector(d).normalized()
    back = d.cross(Vector(nrm)).normalized() * flip
    p1 = Vector(p)
    p2 = p1 + d * L * 0.55 + back * w * 0.35
    R = frame(p2 - p1, nrm)
    B.add((p1 + p2) / 2, (thick / 2 + 0.002, w * 0.82 / 2, (p2 - p1).length / 2 + 0.008), BOLT, bone, R=R,
          top=(1.0, 0.78), role="limb", bevel=0.005, studs=[], nostud=True)
    p3 = p2 - d * 0.012 + d * L * 0.45 - back * w * 0.35
    R = frame(p3 - p2, nrm)
    B.add((p2 + p3) / 2, (thick / 2 + 0.003, w * 0.66 / 2, (p3 - p2).length / 2), HOT, bone, R=R, top=(1.0, 0.14),
          role="limb", bevel=0.004, studs=[], nostud=True)
    return p3


def feather(B, root, tip, nrm, width, thick, color, bone, taper=0.22, edge=None, tipf=0.30, bolted=False, flip=1):
    """flat tapered feather in the wing plane. bolted: the last tipf of the length is a kinked lightning bolt;
    edge: a coloured tip edge (last tipf) instead"""
    root, tip = Vector(root), Vector(tip)
    R = frame(tip - root, nrm)
    L = (tip - root).length
    if not bolted and edge is None:
        return B.add((root + tip) / 2, (thick / 2, width / 2, L / 2), color, bone, R=R, top=(1.0, taper),
                     role="limb", bevel=0.008)
    m = root.lerp(tip, 1 - tipf)
    B.add((root + m) / 2 + (tip - root).normalized() * 0.01, (thick / 2, width / 2, (m - root).length / 2 + 0.01),
          color, bone, R=R, top=(1.0, 0.82), role="limb", bevel=0.008)
    if bolted:
        return bolt(B, m - (tip - root).normalized() * 0.01, tip - root, L * tipf, width * 0.82, nrm, thick, bone,
                    flip)
    w2 = width * 0.82
    B.add((m + tip) / 2, (thick / 2 + 0.002, w2 / 2, (tip - m).length / 2), edge, bone, R=R, top=(1.0, taper / 0.82),
          role="limb", bevel=0.006)
    return tip


def wing(B, s, side):
    """Griffin's 3-row wing in storm colours: COVERT coverts over STORM secondaries (COVERT edges) on the arm; PRIMARY
    primaries with kinked lightning tips fanned from the wrist (outer ones on the tip bone); TEAL tapered arm bar."""
    S0, W, H, bb = X(WING.S, s), X(WING.W, s), X(H2, s), X(WING.BB, s)
    T = X(TIP, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    nrm = (T - W).cross(H - W).normalized()
    if nrm.z < 0:
        nrm = -nrm

    def pl(p):
        p = Vector(p)
        return p - nrm * (p - W).dot(nrm)

    S, H, bb = pl(S0), pl(H), pl(bb)
    B.seg(S0, W, 0.06, 0.09, TEAL, wb, side=nrm, ext=0.05, role="limb", top=(0.8, 0.75))
    B.add(W, (0.05, 0.065, 0.065), TEAL, wb, R=frame(W - S, nrm), role="limb")
    B.seg(W + nrm * 0.078, W.lerp(T, 0.28) + nrm * 0.078, 0.026, 0.048, TEAL, tb, side=nrm, role="limb",
          top=(0.7, 0.7))
    n_sec = 7
    for i in range(n_sec):
        t = (i + 0.5) / n_sec
        a = S.lerp(W, 0.04 + 0.92 * t)
        end = bb.lerp(H, t)
        d = end - a
        end = end + d.normalized() * (0.07 + 0.04 * ((i % 2) * 2 - 1))
        feather(B, a - nrm * 0.016, end - nrm * 0.016, nrm, 0.27, 0.034, STORM, wb, taper=0.35, edge=COVERT,
                tipf=0.15)
    for i in range(6):
        t = (i + 0.5) / 6
        a = S.lerp(W, 0.03 + 0.94 * t)
        end = a.lerp(bb.lerp(H, t), 0.50)
        feather(B, a + nrm * 0.02, end + nrm * 0.02, nrm, 0.22, 0.034, COVERT, wb, taper=0.5)
    for i, (t, f) in enumerate(((0.12, 0.68), (0.32, 0.78), (0.50, 0.86))):
        dv = (H - W).normalized().lerp((T - W).normalized(), t).normalized()
        ln = (T - W).length * f
        feather(B, W + dv * 0.04 - nrm * 0.016, W + dv * ln - nrm * 0.016, nrm, 0.25, 0.034, PRIMARY, wb,
                tipf=0.30, bolted=True, flip=1 if i % 2 else -1)
    n_pri = 5
    for i in range(n_pri):
        t = i / (n_pri - 1)
        dv = (H - W).normalized().lerp((T - W).normalized(), 0.66 + 0.34 * t).normalized()
        ln = (T - W).length * (0.92 + 0.10 * t) * (1.0 + 0.04 * ((i % 2) * 2 - 1))
        o = nrm * (0.065 + 0.004 * (n_pri - 1 - i))
        tipp = feather(B, W + dv * 0.04 + o, W + dv * ln + o, nrm, 0.23, 0.034, PRIMARY, tb, tipf=0.30, bolted=True,
                       flip=1 if i % 2 else -1)
        if i == 2:
            ANCH["WingBolt_" + side] = tuple(tipp)
    for i in range(4):
        t = (i + 0.5) / 4
        dv = (H - W).normalized().lerp((T - W).normalized(), 0.60 + 0.40 * t).normalized()
        o = nrm * 0.11
        feather(B, W + dv * 0.03 + o, W + dv * 0.36 + o, nrm, 0.20, 0.034, COVERT, tb, taper=0.5)


def eye(B, c, s, yaw=26, bone="Head", sc=1.0):
    R = Euler((0, math.radians(-s * 18), math.radians(s * yaw)), "XYZ").to_matrix()
    c = Vector(c)
    B.add(c, (0.05 * sc, 0.008, 0.026 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + R @ Vector((0.002 * s, -0.006, -0.002)), (0.042 * sc, 0.006, 0.014 * sc), BOLT, bone, R=R, studs=[],
          role="detail", bevel=0.003)
    B.add(c + R @ Vector((s * 0.016 * sc, -0.010, 0.0)), (0.017 * sc, 0.004, 0.006 * sc), HOT, bone, R=R,
          studs=[], role="detail", bevel=0.002)
    B.add(c + R @ Vector((-s * 0.004 * sc, -0.011, 0.0)), (0.005 * sc, 0.004, 0.013 * sc), BLACK, bone, R=R,
          studs=[], role="detail", bevel=0.002)


def face_shingles(B, blk, face, rows, color_of, bone, size=(0.055, 0.02, 0.07)):
    """down-pointing shingle feathers laid on the -y (face=-1, breast) or +y (face=+1, back) face of a rotated
    tapered block, rows = [(local z, [local x...]), ...] (Griffin chest ruff, generalised to a leaning block)"""
    h = blk.h
    tilt = math.degrees(math.atan(h.y * (blk.top[1] - blk.bot[1]) / (2 * h.z)))
    Rf = blk.R @ Euler((math.radians(-face * tilt), 0, 0), "XYZ").to_matrix()
    for r, (lz, xs) in enumerate(rows):
        t = (lz / h.z + 1) / 2
        fy = blk.bot[1] + (blk.top[1] - blk.bot[1]) * t
        fx = blk.bot[0] + (blk.top[0] - blk.bot[0]) * t
        for x in xs:
            p = blk.world(Vector((x * fx, face * (h.y * fy + 0.012), lz)))
            B.add(p, size, color_of(r, x), bone, R=Rf, bot=(0.2, 1.0), role="detail", bevel=0.008)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=211, tier=3, plates=False)
    # ================= body: big keeled breast leaning 46 deg, flight-muscle shoulders, lower body swallows the knee
    chest = B.add((0, -0.12, 0.98), (0.27, 0.25, 0.27), TEAL, "Chest", rot=(46, 0, 0), bot=(0.62, 0.56),
                  top=(0.92, 0.92), rnd=0.40)
    B.seg((0, -0.38, 1.10), (0, -0.20, 0.68), 0.17, 0.08, TEAL, "Chest", top=(0.55, 0.8), ext=0.02, rnd=0.4)  # keel
    for s in (1, -1):
        B.add((s * 0.20, -0.10, 1.12), (0.10, 0.12, 0.11), TEAL, "Chest", rot=(46, 0, 0), top=(0.8, 0.85),
              rnd=0.40)                                                                         # flight muscles
    low = B.add((0, 0.10, 0.64), (0.20, 0.20, 0.17), TEAL, "Spine", rot=(52, 0, 0), bot=(0.72, 0.66),
                top=(0.92, 0.9), rnd=0.38)
    # breast shingles: 4 brick rows on the breast face (top COVERT, middle TEAL, bottom tips STORM) + white V bib
    face_shingles(B, chest, -1, [(0.16, (-0.15, -0.05, 0.05, 0.15)), (0.05, (-0.10, 0.0, 0.10)),
                                 (-0.06, (-0.15, -0.05, 0.05, 0.15)), (-0.17, (-0.10, 0.0, 0.10))],
                  lambda r, x: COVERT if r == 0 else (STORM if r == 3 else TEAL), "Chest")
    face_shingles(B, chest, -1, [(0.25, (-0.06, 0.0, 0.06))], lambda r, x: WHITE, "Chest", size=(0.05, 0.024, 0.08))
    # storm mantle: 3 brick rows of shingles down the back (nape -> tail base), fills the strip between the wings
    face_shingles(B, chest, 1, [(0.20, (-0.12, 0.0, 0.12)), (0.06, (-0.18, -0.06, 0.06, 0.18)),
                                (-0.08, (-0.12, 0.0, 0.12))], lambda r, x: STORM, "Chest", size=(0.065, 0.022, 0.09))
    face_shingles(B, low, 1, [(0.08, (-0.10, 0.0, 0.10)), (-0.06, (-0.05, 0.05))], lambda r, x: STORM, "Spine",
                  size=(0.06, 0.02, 0.08))
    # flank skirt: 3 rows of down-back feathers over the knee (top TEAL, lower STORM) - no thigh is ever visible
    for s in (1, -1):
        for z, L, c in ((0.70, 0.20, TEAL), (0.60, 0.19, STORM), (0.50, 0.16, STORM)):
            for dy in (-0.06, 0.04):
                B.spike((s * 0.18, dy, z), (s * 0.25, 0.65, -0.72), L, 0.06, c, "Spine", side=(s, 0, 0),
                        top=(0.2, 0.3))
    # ================= neck: short thick white neck, ruff spikes, hackle cape over the shoulders (white -> teal)
    B.seg((0, -0.24, 1.10), (0, -0.38, 1.40), 0.17, 0.16, WHITE, "Neck", ext=0.06, ext1=0.03, top=(0.9, 0.9))
    for s in (1, -1):
        for y, z, L in ((-0.36, 1.38, 0.16), (-0.30, 1.28, 0.18), (-0.24, 1.18, 0.17)):
            B.spike((s * 0.14, y, z), (s * 0.45, 0.8, -0.35), L, 0.058, WHITE, "Neck", top=(0.12, 0.35))
    dn = Vector((0, -0.55, 0.83))
    nn = Vector((0, 0.83, 0.55))
    Rn = Matrix.Rotation(math.radians(-14), 3, Vector((1, 0, 0))) @ Matrix((Vector((1, 0, 0)), nn, dn)).transposed()
    for t, xs, c in ((0.62, (-0.10, 0.0, 0.10), WHITE), (0.36, (-0.15, -0.05, 0.05, 0.15), WHITE),
                     (0.10, (-0.10, 0.0, 0.10), WHITE_D)):
        p = Vector((0, -0.20 - 0.16 * t, 1.14 + 0.26 * t)) + nn * 0.13
        for x in xs:
            B.add(p + Vector((x, 0, 0)), (0.065, 0.02, 0.095), c, "Neck" if t > 0.2 else "Chest", R=Rn,
                  bot=(0.2, 1.0), role="limb", bevel=0.008)
    # ================= eagle head (+10 %, throat pivot): white cranium, fused WHITE_D V brow, gold cere + big hook
    B.add(HC, (0.148, 0.143, 0.125), WHITE, "Head", top=(0.85, 0.85))                                  # cranium
    B.add(HC + Vector((0, -0.11, -0.05)), (0.11, 0.066, 0.082), WHITE, "Head", top=(0.9, 1))           # face
    B.add(HC + Vector((0, -0.18, -0.016)), (0.08, 0.038, 0.04), GOLD, "Head", top=(0.85, 1))           # cere
    for s in (1, -1):
        B.add(HC + Vector((s * 0.08, -0.188, -0.005)), (0.004, 0.011, 0.008), BLACK, "Head", studs=[],
              role="detail", bevel=0.003)
    B.seg(HC + Vector((0, -0.175, -0.013)), HC + Vector((0, -0.335, -0.04)), 0.074, 0.066, GOLD, "Head",
          top=(0.6, 0.6), ext=0.0)                                                                     # upper bill
    B.seg(HC + Vector((0, -0.29, -0.005)), HC + Vector((0, -0.37, -0.057)), 0.043, 0.05, GOLD_D, "Head",
          top=(0.8, 0.8), ext=0.01)
    B.spike(HC + Vector((0, -0.36, -0.046)), (0, -0.25, -1), 0.13, 0.038, GOLD_D, "Head", top=(0.15, 0.2))  # hook
    B.add(HC + Vector((0, -0.25, -0.078)), (0.058, 0.08, 0.005), MOUTH, "Head", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.add(HC + Vector((s * 0.07, -0.23, -0.068)), (0.004, 0.07, 0.008), MOUTH, "Head", rot=(-8, 0, 0), studs=[],
              role="detail", bevel=0.002)
    B.seg(HC + Vector((0, -0.16, -0.10)), HC + Vector((0, -0.315, -0.10)), 0.058, 0.022, GOLD, "Jaw", top=(0.7, 1),
          ext=0.02)                                                                                    # mandible
    for s in (1, -1):
        eye(B, HC + Vector((s * 0.11, -0.142, 0.024)), s, sc=1.25)
        B.add(HC + Vector((s * 0.086, -0.118, 0.076)), (0.092, 0.05, 0.034), WHITE_D, "Head",
              rot=(0, -s * 21, s * 22), role="detail", bevel=0.012)                       # fused V brow (buried)
    # harpy double crest from the BACK of the crown: 4 long back-row + 3 short front-row feathers, bolt tips
    crest_n = Vector((0, -0.45, 0.89))
    for x, L, up, row in ((-0.075, 0.42, 30, 0), (-0.025, 0.46, 36, 0), (0.025, 0.40, 33, 0), (0.075, 0.44, 27, 0),
                          (-0.05, 0.24, 42, 1), (0.0, 0.26, 46, 1), (0.05, 0.22, 40, 1)):
        root = HC + Vector((x, 0.07 + 0.03 * row - 0.03, 0.105 - 0.01 * row))
        ang = math.radians(up)
        d = Vector((x * 6.5 * (1 if row == 0 else 0.6), math.cos(ang), math.sin(ang))).normalized()
        m1 = root + d * L * 0.52
        B.seg(root - d * 0.02, m1, 0.034, 0.024, WHITE, "Head", side=(1, 0, 0), top=(0.92, 0.92), role="limb")
        m2 = m1 + d * L * 0.12
        B.seg(m1 - d * 0.005, m2, 0.031, 0.022, STORM, "Head", side=(1, 0, 0), role="limb", studs=[])
        tp = bolt(B, m2 - d * 0.005, d, L * 0.38, 0.06, Vector((1, 0, 0)), 0.04, "Head",
                  flip=1 if (x > 0) == (row == 0) else -1)
        if row == 0 and abs(x - (-0.025)) < 1e-6:
            ANCH["Crest"] = tuple(tp)
    ANCH["Beak"] = tuple(HC + Vector((0, -0.37, -0.06)))
    # ================= feathered wings (thunder wings)
    for s, side in ((1, "L"), (-1, "R")):
        wing(B, s, side)
    # ================= legs: hidden thigh, STORM trousers (Shin) with a fringe over the tarsus, bare GOLD tarsus
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A, T = X(HIP, s), X(KNEE, s), X(ANKLE, s), X(TOE, s)
        B.seg(H, K, 0.08, 0.09, TEAL, "Leg_" + side, ext=0.02, ext1=0.04, rnd=0.4)                    # hidden thigh
        B.seg(K, A + Vector((0, 0, 0.04)), 0.08, 0.085, STORM, "Shin_" + side, ext=0.05, top=(1.25, 1.2), rnd=0.4)
        for i, dx in enumerate((-0.07, -0.035, 0.0, 0.035, 0.07)):                                # trouser fringe
            L = 0.10 + 0.03 * (i % 2)
            B.spike(A + Vector((s * dx, -0.02 + 0.015 * abs(dx) / 0.07, 0.11)), (s * dx * 0.6, -0.15, -1), L, 0.045,
                    STORM, "Shin_" + side, top=(0.2, 0.4))
        B.seg(A, T + Vector((0, 0.0, 0.03)), 0.058, 0.058, GOLD, "Foot_" + side, ext=0.03, role="limb")   # tarsus
        for t in (0.25, 0.5, 0.75):
            B.add(A.lerp(T + Vector((0, 0, 0.03)), t), (0.061, 0.062, 0.008), GOLD_D, "Foot_" + side, rot=(-30, 0, 0),
                  studs=[], role="detail", bevel=0.004)
        B.add(T + Vector((0, 0.005, 0.0)), (0.066, 0.066, 0.036), GOLD, "Foot_" + side, role="limb")
        for dx, dy, ang in ((-0.05, -0.08, -18 * s), (0.0, -0.10, 0), (0.05, -0.08, 18 * s)):
            d = Vector((math.sin(math.radians(-ang)) * s * 0 + dx * 1.2, dy, 0)).normalized()
            tb = T + Vector((dx, 0, 0)) + d * 0.10 + Vector((0, 0, -0.005))
            B.seg(T + Vector((dx * 0.5, -0.02, 0.0)), tb, 0.028, 0.026, GOLD, "Foot_" + side, role="limb")
            h0 = tb + d * 0.005 + Vector((0, 0, 0.008))
            B.spike(h0, d - Vector((0, 0, 0.62)), 0.075, 0.024, BLACK, "Foot_" + side)              # talon
            B.spike(h0 + (d - Vector((0, 0, 0.62))).normalized() * 0.06, Vector((0, 0, -1)) + d * 0.3, 0.035, 0.016,
                    BLACK, "Foot_" + side)                                                       # hooked tip
        B.spike(T + Vector((0, 0.05, 0.0)), (0, 1, -0.55), 0.11, 0.026, BLACK, "Foot_" + side)    # hallux talon
    # ================= tail: storm base + 3 covert shingles, 9 WHITE feathers fanned +-50 deg, kinked bolt tips
    T = [Vector(p) for p in TAILP]
    B.seg(T[0], T[1], 0.13, 0.085, STORM, "Tail1", ext=0.10, top=(0.9, 0.8), rnd=0.35)
    for x in (-0.07, 0.0, 0.07):
        B.add(T[0].lerp(T[1], 0.55) + Vector((x, 0, 0.075)), (0.06, 0.085, 0.02), STORM, "Tail1", rot=(-30, 0, 0),
              bot=(1, 0.3), role="limb", bevel=0.008)
    fan_n = Vector((0, 0.45, 0.89)).normalized()
    for i in range(9):
        a = (i - 4) / 4.0
        ang = math.radians(TAIL_SPREAD * a)
        d = Vector((math.sin(ang), math.cos(ang), -0.30 * math.cos(ang))).normalized()
        root = T[1] + Vector((a * 0.06, -0.05, 0.0))
        L = 0.78 - 0.09 * abs(a)
        tp = feather(B, root, root + d * L, fan_n, 0.15, 0.03, WHITE, "Tail2", tipf=0.24, bolted=True,
                     flip=1 if i % 2 else -1)
        if i == 4:
            ANCH["TailBolt"] = tuple(tp)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.12, 0.66), "Root", tail=(0, -0.2, 0.35))
    k.joint("Chest", (0, -0.02, 0.86), "Spine", tail=(0, -0.25, 0.3))
    k.joint("Neck", (0, -0.24, 1.12), "Chest", tail=(0, -0.12, 0.3))
    k.joint("Head", tuple(HC + Vector((0, 0.08, -0.12))), "Neck", tail=(0, -0.35, 0))       # throat pivot
    k.joint("Jaw", tuple(HC + Vector((0, -0.14, -0.09))), "Head", tail=(0, -0.2, 0))
    k.joint("Crest", ANCH.get("Crest", tuple(HC + Vector((0, 0.3, 0.35)))), "Head", tail=(0, 0.1, 0.1))
    k.joint("Beak", ANCH.get("Beak", tuple(HC + Vector((0, -0.37, -0.06)))), "Head", tail=(0, -0.15, 0))
    k.joint("Strike", (0, -0.23, 0.02), "Root", tail=(0, -0.15, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Wing_" + side, X(WING.S, s), "Chest")
        k.joint("WingTip_" + side, X(WING.W, s), "Wing_" + side, tail=(s * 0.6, 0.2, 0.1))
        k.joint("WingBolt_" + side, ANCH.get("WingBolt_" + side, X(TIP, s)), "WingTip_" + side, tail=(s * 0.15, 0, 0))
        k.joint("Leg_" + side, X(HIP, s), "Spine")
        k.joint("Shin_" + side, X(KNEE, s), "Leg_" + side)
        k.joint("Foot_" + side, X(ANKLE, s), "Shin_" + side, tail=(0, -0.15, -0.1))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1", tail=tuple(Vector(TAILP[2]) - Vector(TAILP[1])))
    k.joint("TailBolt", ANCH.get("TailBolt", (0, 1.05, 0.25)), "Tail2", tail=(0, 0.15, 0))


def check_pairs():
    W = ["Wing_L", "WingTip_L", "Wing_R", "WingTip_R"]
    P = [("Wing_L", "WingTip_L"), ("Wing_R", "WingTip_R"), ("WingTip_L", "WingTip_R"), ("Wing_L", "Wing_R"),
         ("WingTip_L", "Wing_R"), ("Wing_L", "WingTip_R")]
    for w in W:
        for b in ("Head", "Neck", "Tail1", "Tail2", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Foot_L", "Foot_R",
                  "Chest", "Spine"):
            P.append((w, b))
    P += [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Head", "Chest"), ("Jaw", "Chest")]
    for b in ("Shin_L", "Shin_R", "Foot_L", "Foot_R"):
        P.append(("Tail2", b))
    return P


def joints():
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.12, "Wing_" + sd))
    return out


def wings(k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WING.key(k, f, up, fwd, twist, tip, side)


HEAD_XF = []


# ------------------------------------------------------------------ ground fold (searched 2026-10-14 on the v2 body)
# CLOAK FOLD: big raise + big twist about the rest arm axis lays the arm along the top of the flank, the dark wing over
# flank + thigh, the bolt-tipped primaries trailing back beside the tail fan. 0 cut-throughs incl. Wing-vs-Chest/Spine
# (wing root x 0.35, tail fan +-38 deg at rest). Every fold <-> open change goes through LIFT1 -> LIFT4 in order
# (tested at step 1: fold->open, open->fold, land brake->fold, raised-V roar loop, wing breath = 0 hits).
FOLD = (86.0, 4.0, -95.0, -15.0)
LIFT1 = (84.0, 16.0, -80.0, -15.0)
LIFT2 = (70.0, 24.0, -55.0, 0.0)
LIFT3 = (50.0, 20.0, -25.0, 10.0)
LIFT4 = (35.0, 8.0, -8.0, 10.0)
RAISED_V = (40.0, 0.0, 0.0, -10.0)
BREATH = (80.0, 26.0, -65.0, -10.0)
