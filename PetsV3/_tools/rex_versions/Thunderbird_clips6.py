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
TAIL_SPREAD = 34.0                                   # rest fan half-angle (deg)
ANCH = {}

# wing: designed flat, raised ELEV deg about the root line for the bind pose (Griffin recipe); the root sits ON the
# shoulder (review: +0.07 x so the cloak fold lays the wing along the flank without cutting the breast)
ELEV = 16.0
WDX = 0.07                                       # wing x offset vs v1 (review 2: no shoulder blocks, +0.07)
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
    Wm = S0.lerp(W, 0.38)
    B.seg(S0, Wm, 0.06, 0.09, TEAL, wb, side=nrm, ext=0.05, role="limb", top=(0.95, 0.95))
    B.seg(Wm, W, 0.057, 0.085, STORM, wb, side=nrm, ext=0.01, role="limb", top=(0.85, 0.8))
    B.add(W, (0.05, 0.065, 0.065), STORM, wb, R=frame(W - S, nrm), role="limb")
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
    B.add(c + R @ Vector((s * 0.003, 0, 0.007 * sc)), (0.053 * sc, 0.008, 0.026 * sc), BLACK, bone, R=R, studs=[],
          role="detail", bevel=0.004)                                   # lid-heavy socket
    B.add(c + R @ Vector((0.002 * s, -0.006, -0.002)), (0.042 * sc, 0.006, 0.014 * sc), BOLT, bone, R=R, studs=[],
          role="detail", bevel=0.003)
    B.add(c + R @ Vector((s * 0.016 * sc, -0.010, 0.0)), (0.017 * sc, 0.004, 0.006 * sc), HOT, bone, R=R,
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
    low = B.add((0, 0.10, 0.64), (0.20, 0.20, 0.17), TEAL, "Spine", rot=(52, 0, 0), bot=(0.22, 0.66),
                top=(0.92, 0.9), rnd=0.38)
    # breast shingles: 4 brick rows on the breast face (top COVERT, middle TEAL, bottom tips STORM) + white V bib
    face_shingles(B, chest, -1, [(0.16, (-0.15, -0.05, 0.05, 0.15)), (0.05, (-0.10, 0.0, 0.10)),
                                 (-0.06, (-0.15, -0.05, 0.05, 0.15)), (-0.17, (-0.10, 0.0, 0.10))],
                  lambda r, x: COVERT if r == 0 else (STORM if r == 3 else TEAL), "Chest")
    face_shingles(B, chest, -1, [(0.25, (-0.06, 0.0, 0.06))], lambda r, x: WHITE, "Chest", size=(0.05, 0.024, 0.08))
    # storm mantle: 3 brick rows of shingles down the back (nape -> tail base), fills the strip between the wings
    face_shingles(B, chest, 1, [(0.18, (0.0,)), (0.06, (-0.18, -0.06, 0.06, 0.18)),
                                (-0.08, (-0.12, 0.0, 0.12))], lambda r, x: STORM, "Chest", size=(0.065, 0.022, 0.09))
    face_shingles(B, low, 1, [(0.08, (-0.10, 0.0, 0.10)), (-0.06, (-0.05, 0.05))], lambda r, x: STORM, "Spine",
                  size=(0.06, 0.02, 0.08))
    B.add(chest.world(Vector((0, 0.09, 0.0))), (0.25, 0.17, 0.25), STORM, "Chest", R=chest.R, bot=(0.62, 0.56),
          top=(0.92, 0.92), rnd=0.40)                      # dorsal saddle: chest back
    B.add(low.world(Vector((0, 0.07, 0.0))), (0.185, 0.14, 0.16), STORM, "Spine", R=low.R, bot=(0.72, 0.66),
          top=(0.92, 0.9), rnd=0.38)                       # dorsal saddle: lower back
    # flank skirt: 3 rows of down-back feathers over the knee (top TEAL, lower STORM) - no thigh is ever visible
    for s in (1, -1):
        for dy in (-0.06, 0.04):                                                  # TEAL top row over the hip
            B.spike((s * 0.18, dy, 0.70), (s * 0.25, 0.65, -0.72), 0.20, 0.06, TEAL, "Spine", side=(s, 0, 0),
                    top=(0.2, 0.3))
        dv = Vector((s * 0.40, 0.62, -0.68)).normalized()
        for z, x0, L in ((0.61, 0.225, 0.16),):                                  # STORM flank blades, hung outside
            for dy in (-0.06, 0.04):                                              # the trousers' swing band
                b0 = Vector((s * x0, dy, z))
                B.bar(b0, b0 + dv * L, Vector((s, 0, 0)), 0.11, 0.02, STORM, "Spine", top=(0.2, 0.5), studs=[])
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
    B.spike(HC + Vector((0, -0.365, -0.05)), (0, -0.55, -1), 0.09, 0.038, GOLD_D, "Head", top=(0.15, 0.2))  # hook
    B.add(HC + Vector((0, -0.25, -0.078)), (0.058, 0.08, 0.005), MOUTH, "Head", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.add(HC + Vector((s * 0.07, -0.23, -0.068)), (0.004, 0.07, 0.008), MOUTH, "Head", rot=(-8, 0, 0), studs=[],
              role="detail", bevel=0.002)
    B.seg(HC + Vector((0, -0.16, -0.10)), HC + Vector((0, -0.315, -0.10)), 0.058, 0.022, GOLD, "Jaw", top=(0.7, 1),
          ext=0.02)                                                                                    # mandible
    for s in (1, -1):
        eye(B, HC + Vector((s * 0.11, -0.142, 0.024)), s, sc=1.25)
        B.add(HC + Vector((s * 0.086, -0.104, 0.076)), (0.092, 0.05, 0.034), WHITE_D, "Head",
              rot=(0, -s * 21, s * 22), role="detail", bevel=0.012)                       # fused V brow (buried)
    # harpy double crest from the BACK of the crown: 4 long back-row + 3 short front-row feathers, bolt tips
    crest_n = Vector((0, -0.45, 0.89))
    for x, L, up, row in ((-0.075, 0.42, 16, 0), (-0.025, 0.46, 22, 0), (0.025, 0.40, 19, 0), (0.075, 0.44, 14, 0),
                          (-0.05, 0.24, 26, 1), (0.0, 0.26, 30, 1), (0.05, 0.22, 24, 1)):
        root = HC + Vector((x, 0.07 + 0.03 * row - 0.03, 0.105 - 0.01 * row))
        ang = math.radians(up)
        d = Vector((x * 3.0 * (1 if row == 0 else 0.6), math.cos(ang), math.sin(ang))).normalized()
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
        B.seg(K, A + Vector((0, 0, 0.04)), 0.07, 0.075, STORM, "Shin_" + side, ext=0.05, top=(1.0, 1.15), rnd=0.45)
        for i in range(7):                                                                    # ragged trouser cuff
            ang = 2 * math.pi * i / 7 + 0.3
            rv = Vector((s * math.cos(ang) * 0.075, math.sin(ang) * 0.08, 0))                 # mirrored L / R
            L = 0.12 + 0.03 * ((i * 3) % 4) / 3.0
            B.spike(A + rv + Vector((0, 0, 0.11)), (rv.x * (3 if rv.x * s > 0 else 0), rv.y * 6 - 0.15, -1), L, 0.04,
                    STORM if i % 2 == 0 else PRIMARY, "Shin_" + side, top=(0.2, 0.4))
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
        d = Vector((math.sin(ang), math.cos(ang), -0.30 * math.cos(ang) + 0.05 * abs(a))).normalized()
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
    P += [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Head", "Chest"), ("Jaw", "Chest"),
          ("Head", "Neck"), ("Shin_L", "Spine"), ("Shin_R", "Spine")]
    for b in ("Shin_L", "Shin_R", "Foot_L", "Foot_R"):
        P.append(("Tail2", b))
    return P


def joints():
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.12, "Wing_" + sd))
        # knee: the trouser top emerges from the belly skirt (a bird's leg out of its body feathers)
        K, A = Vector(X(KNEE, s)), Vector(X(ANKLE, s))
        d = (A - K).normalized()
        out.append((tuple(K - d * 0.10), tuple(K + d * 0.20), 0.13, "Shin_" + sd))
    # throat pivot under the ruff (stops below the crest so crest-vs-cape still counts)
    out.append(((0, -0.28, 1.40), (0, -0.56, 1.40), 0.20, "Head"))
    return out


def wings(k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WING.key(k, f, up, fwd, twist, tip, side)


HEAD_XF = []


# ------------------------------------------------------------------ ground fold (searched 2026-10-14 on the v2 body)
# CLOAK FOLD: big raise + big twist about the rest arm axis lays the arm along the top of the flank, the dark wing over
# flank + thigh, the bolt-tipped primaries trailing back beside the tail fan. 0 cut-throughs incl. Wing-vs-Chest/Spine
# (wing root x 0.35, tail fan +-38 deg at rest). Every fold <-> open change goes through LIFT1 -> LIFT4 in order
# (tested at step 1: fold->open, open->fold, land brake->fold, raised-V roar loop, wing breath = 0 hits).
FOLD = (86.0, 10.0, -80.0, 0.0)          # review 2: 0 hits, half-width 0.549 / 0.461 (90 %)
LIFT1 = (84.0, 16.0, -80.0, -15.0)
LIFT2 = (70.0, 24.0, -55.0, 0.0)
LIFT3 = (50.0, 20.0, -25.0, 10.0)
LIFT4 = (35.0, 8.0, -8.0, 10.0)
RAISED_V = (40.0, 0.0, 0.0, -10.0)
BREATH = (80.0, 26.0, -65.0, -10.0)


# ------------------------------------------------------------------ animation (v2, review 1 section 4 + review 2 section 3)
# Reference (owner rule 2026-10-10, notes in _review/ANIM_REFERENCES_1014.md): animationreference.org "Bird Flight
# Animation Tutorial - Flapping": the leading edge (arm) leads and the tips trail; the primaries spread and the wing
# half-folds on the upstroke; the body RISES on the downstroke; the tail fans to brake and turn (landing flare);
# "Dragon Walk Cycle" (C. Sophocleous): the head settles a few frames after each contact, the tail wave lags.
# Rules: every ground clip starts and ends at FOLD and every fold <-> open change runs LIFT1 -> LIFT4 in order; the head
# is gyro-stabilised in walk and fly; no yaw reversal faster than 6 f (no head shakes).
import petkit as pk
import _common as cm

LEGS = ["Leg_L", "Leg_R"]
FOOT_LIFT = 0.012            # the modelled talon tips sit 0.028 under z 0: keep every planted claw >= -0.02


def ease(u):
    u = max(0.0, min(1.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u)


def wp(k, f, P, side=None):
    wings(k, f, *P, side=side)


def folded(k, f, du=0.0, dfwd=0.0, dtw=0.0, dtip=0.0, side=None):
    wings(k, f, FOLD[0] + du, FOLD[1] + dfwd, FOLD[2] + dtw, FOLD[3] + dtip, side)


def blend(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def tail(k, f, pitch=0.0, yaw=0.0):
    """kit pitch + LIFTS the fan (flare)"""
    k.key("Tail1", f, rot=(pitch * 0.6, yaw * 0.5, 0))
    k.key("Tail2", f, rot=(pitch * 0.4, yaw * 0.5, 0))


def rest_keys(k, f, z=0.0, pitch=0.0):
    k.key("Spine", f, rot=(pitch, 0, 0), loc=(0, 0, z))
    for b in ("Chest", "Neck", "Head"):
        k.key(b, f, rot=(0, 0, 0))
    k.key("Jaw", f, rot=(0, 0, 0))
    folded(k, f)
    tail(k, f, 0, 0)


def plant_frames(k, frames, dy=0.0, regrip=None):
    """feet on their rest spots (+dy); regrip = {leg: (f0, f1)}: that foot lifts 0.03 and curls its toes (+20)"""
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        for leg in LEGS:
            z, toe = FOOT_LIFT, 0.0
            if regrip and leg in regrip and regrip[leg][0] <= f <= regrip[leg][1]:
                u = (f - regrip[leg][0]) / float(regrip[leg][1] - regrip[leg][0])
                z, toe = FOOT_LIFT + 0.07 * math.sin(math.pi * u), 14 * math.sin(math.pi * u)
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y + dy, z)), toe=toe)


def lift_air_frames(k, frames, target=0.02):
    """airborne frames: raise the Spine just enough that no vertex goes below `target` (keeps its x/y and rotation)"""
    import bpy
    sc = bpy.context.scene
    pb = k.arm.pose.bones["Spine"]
    R0 = k.arm.data.bones["Spine"].matrix_local.to_quaternion()
    k.bake_bezier_now()
    rows = []
    for f in frames:
        sc.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        ev = k.main.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        mz = min((mw @ v.co).z for v in me.vertices)
        ev.to_mesh_clear()
        rows.append((f, mz, pb.rotation_quaternion.copy(), (R0 @ pb.location).copy()))
    for f, mz, q, loc in rows:
        if mz < target:
            pb.rotation_quaternion = q
            pb.keyframe_insert("rotation_quaternion", frame=f, group="Spine")
            k.key("Spine", f, loc=(loc.x, loc.y, loc.z + target - mz))


def legs_fk(k, f, thigh, shin, foot, spread=5.0):
    for s, side in ((1, "L"), (-1, "R")):
        k.key("Leg_" + side, f, rot=(thigh, 0, -s * spread), loc=(0, 0, 0))
        k.key("Shin_" + side, f, rot=(shin, 0, 0))
        k.key("Foot_" + side, f, rot=(foot, 0, 0))


# ---- ground
def idle(k):
    """STORM WATCH: a breath swell; bird head turns L -> hold -> centre -> R -> hold (at most 28 deg in 4 f, no whip);
    the HUNTING STARE (head down at the ground in front, dead still 20 f); a sky glance with a tail flick; a WING
    BREATH through the tested waypoints; a talon re-grip, one foot then the other."""
    n = 132
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.008 * b))
        k.key("Chest", f, rot=(0, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
    look = [(0, 0, 0, 0), (12, 0, 0, 0), (16, 0, 0, 28), (26, 0, 0, 28), (32, 0, 0, 0), (36, 0, 0, -28),
            (46, 0, 0, -28), (52, 0, 0, 0), (54, 0, 0, 0), (58, 10, 12, 0), (78, 10, 12, 0), (84, 0, 0, 0),
            (86, 0, 0, 0), (90, -4, -12, 0), (96, -4, -12, 0), (102, 0, 0, 0), (132, 0, 0, 0)]
    for f, nk, hd, y in look:                              # (frame, neck pitch, head pitch, total yaw)
        k.key("Neck", f, rot=(nk, y * 0.3, 0))
        k.key("Head", f, rot=(hd, y * 0.7, 0))
    for f, P in ((0, FOLD), (102, FOLD), (108, LIFT1), (114, BREATH), (120, LIFT1), (126, FOLD), (132, FOLD)):
        wp(k, f, P)
    for f, p in ((0, 0), (85, 0), (88, -5), (92, -1), (96, 0), (132, 0)):   # tail pump DOWN (pitch only: the
        tail(k, f, p, 0)                                                      # folded primaries ride beside the fan)
    plant_frames(k, range(0, n + 1), regrip={"Leg_L": (18, 24), "Leg_R": (38, 44)})
    k.finish()
    k.meta["planted"] = LEGS


def walk(k):
    """ROLLING STRUT: the body rolls over the stance leg (+-5) and yaws +-3, an asymmetric contact dip (-0.04 within
    3 f, slow rise), the head GYRO-stabilised (cancels 75 pct of the body's pitch / roll / yaw), toes curled in the
    swing and spread before contact, wings folded with a 0-15 pct blend toward LIFT1 on each contact."""
    n = 28

    def dip(f):
        t = f % (n // 2)
        if t <= 3:
            u = t / 3.0
            return -0.04 * (u * u * (3 - 2 * u))
        u = (t - 3) / (n / 2 - 3)
        return -0.04 * (1 - u * u * (3 - 2 * u))

    def body(f):
        sp = 1.2 * pk.wave(f, n, 0.1, 2)
        sy = 3 * pk.wave(f, n, 0.0)
        sr = 4 * pk.wave(f, n, 0.05)
        cp, cy, cr = 0.0, -1.5 * pk.wave(f, n, 0.05), -1.5 * pk.wave(f, n, 0.05)
        k.key("Spine", f, rot=(sp, sy, sr), loc=(0, 0, dip(f)))
        k.key("Chest", f, rot=(cp, cy, cr))
        k.key("Neck", f, rot=(-0.3 * (sp + cp), -0.3 * (sy + cy), -0.3 * (sr + cr)))
        k.key("Head", f, rot=(-0.45 * (sp + cp), -0.45 * (sy + cy), -0.45 * (sr + cr)))
        k.key("Jaw", f, rot=(0, 0, 0))
        c = max(0.0, math.cos(2 * math.pi * (2 * f / n)))  # contact pulse (2 per cycle)
        wp(k, f, blend(FOLD, LIFT1, 0.15 * c ** 3))
        tail(k, f, -2.5 + 1.5 * pk.wave(f, n, 0.2, 2), cy)               # below the folded primaries, with the chest
    orig = k.solve_leg

    def strut(leg, f, T, foot_z=0.0, toe=None):
        lift = max(0.0, T.z)
        T = Vector(T) + Vector((0, 0, FOOT_LIFT))
        return orig(leg, f, T, foot_z, toe=22.0 * min(1.0, lift / 0.09))
    k.solve_leg = strut
    try:
        return cm.biped_walk(k, n, 0.15, 0.09, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.6)
    finally:
        del k.solve_leg


def roar(k):
    """SKY SCREECH: gathers (head in, wings LIFT1 -> LIFT2), rears up with the wings through LIFT3 into the RAISED V
    (upper wing + lightning edges to the camera), head up, beak 34-38 with a buzz, TWO THUNDER BEATS of the V (the body
    lifts on each downbeat, the fan flares; bolts from the WingBolt anchors), folds back through LIFT3-1, settles."""
    n = 70
    k.new_action("roar", n, False)
    rest_keys(k, 0)
    K = [  # f, spine pitch, z, chest, neck, head, jaw, wings, tail
        (4, 3, -0.02, 2, 6, 4, 0, LIFT1, 0), (8, 4, -0.04, 3, 8, 6, 2, LIFT2, 2),
        (11, -4, 0.0, -2, 0, -4, 10, LIFT3, 6), (14, -10, 0.02, -4, -6, -12, 34, RAISED_V, 8),
        (20, -10, 0.02, -4, -6, -12, 36, RAISED_V, 8), (23, -10, 0.05, -4, -6, -12, 38, (4, 4, 4, -6), 14),
        (26, -10, 0.02, -4, -6, -12, 34, RAISED_V, 8), (32, -10, 0.02, -4, -6, -12, 36, RAISED_V, 8),
        (35, -10, 0.05, -4, -6, -12, 38, (4, 4, 4, -6), 14), (38, -10, 0.02, -4, -6, -12, 34, RAISED_V, 8),
        (48, -8, 0.01, -3, -5, -10, 30, RAISED_V, 6), (52, -4, 0.0, -1, -2, -4, 8, LIFT3, 3),
        (56, 0, 0.0, 0, 0, 0, 0, LIFT2, 1), (60, 0, 0.0, 0, 0, 0, 0, LIFT1, 0), (64, 0, 0.0, 0, 0, 0, 0, FOLD, 0)]
    for f, p, z, ch, nk, hd, jw, w, tp in K:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        wp(k, f, w)
        tail(k, f, tp, 0)
    for f in (16, 18, 28, 30, 41, 44):                    # jaw buzz (the head stays still)
        k.key("Jaw", f, rot=(36 + (2 if (f // 2) % 2 else -2), 0, 0))
    rest_keys(k, n)
    plant_frames(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["roar"] = {"screech": round(14 / n, 3), "beat1": round(23 / n, 3), "beat2": round(35 / n, 3)}


# ---- flight (eagle: deep full-arm downstroke, outer wing tucks on the upstroke, talons balled under the fan)
FPITCH, FNECK, FHEAD = 40.0, -10.0, -30.0
THI, SHI, FOO = 70.0, -40.0, 76.0


def fly_legs(k, f, ph, amt=1.0):
    for s, side in ((1, "L"), (-1, "R")):
        p = ph + 0.03 * s
        k.key("Leg_" + side, f, rot=((THI + 3 * math.sin(2 * math.pi * (p - 0.15))) * amt, 0, -s * 3 * amt),
              loc=(0, 0, 0))
        k.key("Shin_" + side, f, rot=((SHI - 4 * math.sin(2 * math.pi * (p - 0.30))) * amt, 0, 0))
        k.key("Foot_" + side, f, rot=((FOO + 6 * math.sin(2 * math.pi * (p - 0.42))) * amt, 0, 0))


def fly_pose(k, f, ph, legs=True):
    w = wing3.stroke(ph, top=34, bot=-40, down=0.45, sweep=10, twist=10, fold=36)
    wings(k, f, w["up"], w["fwd"], w["twist"], w["tip"])
    rise = math.cos(2 * math.pi * (ph - 0.45))            # the body rises on the downstroke
    sp = FPITCH - 3 * math.sin(2 * math.pi * (ph - 0.1))
    k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, 0.10 + 0.07 * rise))
    k.key("Chest", f, rot=(-2 * math.sin(2 * math.pi * (ph - 0.2)), 0, 0))
    k.key("Neck", f, rot=(FNECK + 1.5 * math.sin(2 * math.pi * (ph - 0.1)), 0, 0))
    k.key("Head", f, rot=(FHEAD - 1.5 * math.sin(2 * math.pi * (ph - 0.1)) + 2 * math.sin(2 * math.pi * (ph - 0.2)),
                          0, 0))
    k.key("Jaw", f, rot=(0, 0, 0))
    tail(k, f, 6 + 4 * math.sin(2 * math.pi * (ph - 0.3)), 0)
    if legs:
        fly_legs(k, f, ph)


def fly(k):
    n = 28
    k.new_action("fly", n, True)
    for f in range(0, n + 1):
        fly_pose(k, f, f / n)
    k.finish()


def takeoff(k):
    """crouch with the wings opening through FOLD -> LIFT1 -> LIFT2 (f0-6) -> LIFT3 -> LIFT4 (f6-9) -> stroke top by
    f10; LAUNCH on the big downstroke at f11 (event), the legs push then tuck, into the flight cycle"""
    n = 30
    k.new_action("takeoff", n, False)
    rest_keys(k, 0)
    for f, z, p, ch, hd, w in ((3, -0.04, 4, 2, -2, LIFT1), (6, -0.08, 8, 4, -6, LIFT2), (8, -0.10, 9, 5, -9, LIFT3),
                               (9, -0.115, 10, 6, -11, LIFT4), (10, -0.12, 10, 6, -12, (30, 0, 0, 0)),
                               (13, 0.08, 20, 0, -20, (-14, 8, 8, -6)), (16, 0.14, 30, -2, -26, (-38, 8, 6, 4))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(-p * 0.25, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        wp(k, f, w)
        tail(k, f, 6 + p * 0.2, 0)
    fly_pose(k, 23, 0.0)
    fly_pose(k, n, 0.45)
    plant_frames(k, range(0, 13))
    legs_fk(k, 15, 24, -10, 40)
    legs_fk(k, 19, 50, -30, 66)
    fly_legs(k, 23, 0.0)
    fly_legs(k, n, 0.45)
    lift_air_frames(k, range(13, n + 1))
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    """(ref: bird flight - the tail fans to brake) flares upright, brakes with the wings swept forward, the legs reach
    and the open talons are THROWN forward, TOUCH (event), absorbs in a crouch holding the RAISED V, then folds through
    LIFT4 -> LIFT1 -> FOLD"""
    n = 32
    k.new_action("land", n, False)
    fly_pose(k, 0, 0.0)
    for f, p, z, nk, hd, w, lg in (
            (6, 16, 0.10, -4, -18, (24, 16, -10, -4), (40, -20, 50)),
            (10, -4, 0.10, 0, -8, (-24, 22, -10, 8), (-24, 4, -8)),
            (13, -6, 0.08, 0, -6, (22, 18, -8, -6), (-24, 10, -20)),
            (15, -4, 0.04, 0, -4, (30, 10, -6, -8), (-14, 6, -20))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(-3, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        wp(k, f, w)
        tail(k, f, 14, 0)
        legs_fk(k, f, *lg)
    for f, z, p, w in ((17, -0.09, 8, RAISED_V), (22, -0.06, 4, RAISED_V), (24, -0.045, 3, LIFT4),
                       (26, -0.03, 2, LIFT3), (28, -0.015, 1, LIFT2), (30, -0.005, 0, LIFT1)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(2, 0, 0))
        k.key("Neck", f, rot=(p * 0.5, 0, 0))
        k.key("Head", f, rot=(-p * 0.4, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        wp(k, f, w)
        tail(k, f, 8 if f < 24 else 2, 0)
    rest_keys(k, n)
    lift_air_frames(k, range(0, 17))
    plant_frames(k, range(17, n + 1))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(17 / n, 3)}


def stoop(k):
    """SIGNATURE (Thunderbird only) - STOOP STRIKE: locks on in a crouch, LAUNCHES on one huge downbeat, hangs at the
    apex nose-down on the target, then STOOPS (the wings snap back to the fold and it drops like a teardrop), throws
    both feet forward with the talons open as the wings flare into the raised V, STRIKES 0.18 in front (lightning
    impact), grips with a chest shudder, then screams to the sky with the talons clenched; folds and hops back."""
    import bpy
    n = 84
    k.new_action("act_stoop", n, False)
    rest_keys(k, 0)
    K = [  # f, spine z, pitch, chest, neck, head, jaw, wings, tail
        (4, -0.04, 4, 2, 6, 6, 0, LIFT1, 2), (8, -0.08, 8, 3, 10, 10, 0, LIFT2, 4),
        (10, -0.08, 8, 3, 10, 10, 0, LIFT3, 4), (11, -0.06, 6, 2, 8, 8, 0, LIFT4, 4),
        (12, -0.02, 2, 0, 4, 6, 0, (30, 0, 0, 0), 4), (14, 0.12, 6, 0, 0, 4, 0, (-34, 8, 6, 4), 6),
        (18, 0.30, 10, 0, -2, 10, 0, (20, 4, 4, -4), 14), (21, 0.31, 10, 0, -2, 10, 0, (-20, 6, 4, 2), 14),
        (24, 0.30, 12, 0, -2, 10, 0, LIFT4, 14), (25, 0.28, 15, 0, -2, 10, 0, LIFT3, 12),
        (26, 0.25, 19, 0, -2, 10, 0, LIFT2, 8), (27, 0.21, 22, 0, -2, 10, 0, LIFT1, 3),
        (28, 0.16, 25, 0, -2, 10, 0, FOLD, 0), (30, 0.10, 25, 0, -2, 10, 0, FOLD, 0),
        (31, 0.07, 12, 0, 0, 8, 0, LIFT1, 0), (32, 0.04, 0, 0, 2, 8, 0, LIFT2, 6),
        (33, 0.0, -12, 0, 4, 8, 0, LIFT3, 10), (34, -0.06, -10, 2, 6, 10, 0, RAISED_V, 14),
        (36, -0.05, -8, 2, 6, 10, 0, RAISED_V, 12), (42, -0.05, -8, 2, 6, 10, 0, RAISED_V, 10),
        (46, -0.05, -10, -2, -6, -12, 36, RAISED_V, 10), (58, -0.05, -10, -2, -6, -12, 36, RAISED_V, 10),
        (62, -0.03, -4, 0, -2, -4, 6, LIFT3, 4), (65, -0.02, 0, 0, 0, 0, 0, LIFT2, 2),
        (68, -0.01, 0, 0, 0, 0, 0, LIFT1, 0), (72, 0.0, 0, 0, 0, 0, 0, FOLD, 0)]
    for f, z, p, ch, nk, hd, jw, w, tp in K:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        wp(k, f, w)
        tail(k, f, tp, 0)
    for f, d in ((38, 2), (39, -2), (40, 2), (41, 0)):              # chest shudder in the grip (not the head)
        k.key("Chest", f, rot=(2 + d, 0, 0))
    for f in (48, 50, 52, 54, 56):                                   # scream buzz
        k.key("Jaw", f, rot=(36 + (2 if (f // 2) % 2 else -2), 0, 0))
    rest_keys(k, n)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, 13):                                           # crouch: planted
        sc.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, FOOT_LIFT)), toe=0.0)
    legs_fk(k, 16, 50, -30, 66)                                      # launch: push then tuck
    legs_fk(k, 20, THI, SHI, FOO)                                    # balled talons under the fan
    legs_fk(k, 29, THI, SHI, FOO)
    legs_fk(k, 31, -20, 30, -10)                                     # THROW: feet swing forward, talons open
    legs_fk(k, 32, -36, 40, -16)
    reach = Vector((0, -0.18, 0))
    for f in range(33, 61):                                          # STRIKE + grip + scream: planted 0.18 ahead
        sc.frame_set(f)
        for leg in LEGS:
            zg = FOOT_LIFT + 0.01 + (0.02 if 35 <= f < 57 else 0.0) + (0.025 if f >= 58 else 0.0)
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, zg)) + reach,
                        toe=-8.0 if f < 35 else (6.0 if f < 57 else 0.0))   # open, clenched (claws >= -0.02), released
    for f in range(61, n + 1):                                       # two hop-steps back to the rest spots
        sc.frame_set(f)
        for leg in LEGS:
            if f <= 66:
                u = (f - 61) / 5.0
                T = Vector((k.J[leg].x, k.J[leg].y - 0.18 + 0.09 * ease(u), FOOT_LIFT + 0.05 * math.sin(math.pi * u)))
            elif f <= 72:
                u = (f - 66) / 6.0
                T = Vector((k.J[leg].x, k.J[leg].y - 0.09 + 0.09 * ease(u), FOOT_LIFT + 0.05 * math.sin(math.pi * u)))
            else:
                T = Vector((k.J[leg].x, k.J[leg].y, FOOT_LIFT))
            k.solve_leg(leg, f, T, toe=0.0)
    lift_air_frames(k, range(13, 33))
    k.finish(loop=False)
    k.events["act_stoop"] = {"launch": round(14 / n, 3), "strike": round(33 / n, 3), "scream": round(46 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    stoop(k)
    return stride
