# Inferno Phoenix v1 (Magma egg, NEW 2 % SECRET, 2026-10-14) - "BLACKBODY" fire-raptor, built to the plan review
# _review/InfernoPhoenix_plan_review.md on the approved Thunderbird kit (wingbiped rig, wing3 3-row feather wing, the
# CLOAK FOLD + LIFT waypoints). A slim ash-basalt raptor leaning 40 deg on a 2-bone S-neck: basalt hood, vermilion
# hide, a molten-cream upward breast tongue, scarlet scaled tarsi. HERO 1: a plain GOLD CIRCLET on the hood with a
# 5-plume FLAME CREST rising 44-55 deg from inside it (the model top). HERO 2: three long STREAMERS (lanceolate vanes +
# straight stepped tongues) on narrow round knuckles. One owned fire language: every fire part is a curved stepped
# tongue EMBER -> LAVA -> FLAME -> HOT, all curling the same way (never the Thunderbird's kinked bolt). No tail fan,
# no seams, no sun-disc, no breath anchor. No glow (fire = Studio VFX anchors).
import math
from mathutils import Vector, Euler, Matrix
import wing3

DISPLAY = "Inferno Phoenix"
MOTION = "Fly"
RIG = "wingbiped"
HEIGHT = 10.0

# Blender colours (Roblox renders ~0.6x darker) - plan review section 3 "BLACKBODY"
BASALT = (80, 70, 74)        # hood, saddles, mantle, rump, arm bar outer, hand bar, secondaries, trousers, streamer 1
BASALT_D = (54, 46, 52)      # primary bodies, brows, malar stripes, tarsus scale bands, cuff alternates
EMBER = (232, 78, 32)        # neck, cape, breast, flanks, cheeks, coverts, crest roots, streamer 2, tarsi + toes
PALE = (248, 216, 160)       # belly keel strip, the upward breast tongue
LAVA = (255, 128, 24)        # ramp step 2 only
FLAME = (255, 214, 72)       # ramp step 3 only; the eye iris
HOT = (255, 244, 210)        # ramp points, eye hot spot
GOLD = (255, 196, 50)        # circlet, upper beak, hook segment
GOLD_D = (214, 150, 30)      # cere, mandible, tomial tooth
BLACK = (14, 14, 22)
MOUTH = (96, 26, 30)

HC = Vector((0, -0.47, 1.62))                      # cranium centre
H_MODEL = 2.034                                    # centre crest tip at idle f0 (measured; review 1 F5)
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)

HIP, KNEE, ANKLE, TOE = (0.12, 0.10, 0.68), (0.14, -0.06, 0.55), (0.14, 0.06, 0.27), (0.14, -0.06, 0.035)
FOOT_LIFT = 0.014
ANCH = {}

# wing: the Thunderbird points shifted by (-0.05, -0.02, +0.06), raised ELEV deg about the root line for the bind pose
ELEV = 16.0
_S0, _BB0 = Vector((0.22, -0.12, 1.22)), Vector((0.19, 0.20, 1.04))
_ROT = Matrix.Rotation(math.radians(-ELEV), 3, (_BB0 - _S0).normalized())


def _raise(p):
    return _S0 + _ROT @ (Vector(p) - _S0)


_W, _H2, _T = _raise((0.88, -0.06, 1.38)), _raise((0.74, 0.60, 1.18)), _raise((1.74, 0.28, 1.48))
_N = (_T - _W).cross(_H2 - _W).normalized()
if _N.z < 0:
    _N = -_N
WING = wing3.Wing(S=tuple(_S0), W=tuple(_W), H=tuple(_W + _N * 0.30), BB=tuple(_BB0))
H2 = tuple(_H2)
TIP = tuple(_T)

# streamers (plan review 4.6): knuckle centre, then seg1 end, seg2 end, vane end, tongue tip (left chain; R mirrored)
STREAM = {"C": [(0, 0.38, 0.60), (0, 0.80, 0.31), (0, 1.24, 0.15), (0, 1.70, 0.265), (0, 1.91, 0.32)],
          "L": [(0.095, 0.37, 0.53), (0.14, 0.73, 0.27), (0.25, 1.13, 0.155), (0.38, 1.55, 0.265), (0.435, 1.735, 0.315)]}
STREAM_START = {"C": (0, 0.40, 0.58), "L": (0.10, 0.39, 0.51)}   # x-separated roots: pitch never crosses
CREST_P = Vector((0, -0.43, 1.72))


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def frame(z, n):
    z = Vector(z).normalized()
    x = Vector(n)
    x = (x - z * x.dot(z)).normalized()
    return Matrix((x, z.cross(x), z)).transposed()


def tongue(B, p, d, L, w, nrm, thick, bone, cols, fracs, curl=12.0):
    """the owned fire language: consecutive stepped blocks in the plane normal to nrm, each turned by `curl` deg about
    nrm (one sign for the whole wing / plume = a flowing flame, never a jog); widths 0.82w -> x0.75 per step; the last
    step tapers to a point (top 0.14). Returns the tip."""
    d = Vector(d).normalized()
    nrm = Vector(nrm).normalized()
    cur = Vector(p)
    wi = w * 0.82
    for i, (c, fr) in enumerate(zip(cols, fracs)):
        if i:
            d = (Matrix.Rotation(math.radians(curl), 3, nrm) @ d).normalized()
        sl = L * fr
        end = cur + d * sl
        last = i == len(cols) - 1
        w1 = wi * 0.75
        B.add((cur + end) / 2, (thick / 2 + 0.002 + 0.001 * i, wi / 2, sl / 2 + 0.006), c, bone, R=frame(end - cur, nrm),
              top=(1.0, 0.14 if last else w1 / wi), role="limb", bevel=0.004, studs=[], nostud=True)
        cur = end - d * 0.006
        wi = w1
    return cur + d * 0.006


def feather(B, root, tip, nrm, width, thick, color, bone, taper=0.22, tipf=0.30, cols=None, fracs=None, curl=0.0):
    """flat tapered feather in the wing plane; with cols the last tipf of the length is a curved stepped fire tongue"""
    root, tip = Vector(root), Vector(tip)
    R = frame(tip - root, nrm)
    L = (tip - root).length
    if not cols:
        return B.add((root + tip) / 2, (thick / 2, width / 2, L / 2), color, bone, R=R, top=(1.0, taper),
                     role="limb", bevel=0.008)
    m = root.lerp(tip, 1 - tipf)
    B.add((root + m) / 2 + (tip - root).normalized() * 0.01, (thick / 2, width / 2, (m - root).length / 2 + 0.01),
          color, bone, R=R, top=(1.0, 0.82), role="limb", bevel=0.008)
    return tongue(B, m - (tip - root).normalized() * 0.01, tip - root, L * tipf, width, nrm, thick, bone, cols, fracs,
                  curl)


def wing(B, s, side):
    """3-row wing in BLACKBODY: EMBER coverts over BASALT secondaries (EMBER -> LAVA tongue tips); BASALT_D primaries
    with 3-step LAVA -> FLAME -> HOT tongues fanned from the wrist; the arm bar EMBER at the shoulder, BASALT outward."""
    S0, W, H, bb = X(WING.S, s), X(WING.W, s), X(H2, s), X(WING.BB, s)
    T = X(TIP, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    nrm = (T - W).cross(H - W).normalized()
    if nrm.z < 0:
        nrm = -nrm
    cs = s                                                   # curl sign: toward the trailing edge, mirrored L / R

    def pl(p):
        p = Vector(p)
        return p - nrm * (p - W).dot(nrm)

    S, H, bb = pl(S0), pl(H), pl(bb)
    Wm = S0.lerp(W, 0.38)
    Wa = S0.lerp(W, 0.22)                                    # a small EMBER shoulder, BASALT outward (shares)
    B.seg(S0, Wa, 0.06, 0.09, EMBER, wb, side=nrm, ext=0.05, role="limb", top=(0.98, 0.98))
    B.seg(Wa, Wm, 0.059, 0.088, BASALT, wb, side=nrm, ext=0.005, role="limb", top=(0.97, 0.97))
    B.seg(Wm, W, 0.057, 0.085, BASALT, wb, side=nrm, ext=0.01, role="limb", top=(0.85, 0.8))
    B.add(W, (0.05, 0.065, 0.065), BASALT, wb, R=frame(W - S, nrm), role="limb")
    B.seg(W + nrm * 0.078, W.lerp(T, 0.28) + nrm * 0.078, 0.026, 0.048, BASALT, tb, side=nrm, role="limb",
          top=(0.7, 0.7))
    n_sec = 7
    for i in range(n_sec):
        t = (i + 0.5) / n_sec
        a = S.lerp(W, 0.04 + 0.92 * t)
        end = bb.lerp(H, t)
        d = end - a
        end = end + d.normalized() * (0.07 + 0.04 * ((i % 2) * 2 - 1))
        feather(B, a - nrm * 0.016, end - nrm * 0.016, nrm, 0.27, 0.034, BASALT, wb, tipf=0.22, cols=(EMBER, LAVA),
                fracs=(0.55, 0.45), curl=10 * cs)
    for i in range(6):
        t = (i + 0.5) / 6
        a = S.lerp(W, 0.03 + 0.94 * t)
        end = a.lerp(bb.lerp(H, t), 0.50)
        feather(B, a + nrm * 0.02, end + nrm * 0.02, nrm, 0.22, 0.034, EMBER, wb, taper=0.5)
    for i, (t, f) in enumerate(((0.12, 0.68), (0.32, 0.78), (0.50, 0.86))):
        dv = (H - W).normalized().lerp((T - W).normalized(), t).normalized()
        ln = (T - W).length * f
        feather(B, W + dv * 0.04 - nrm * 0.016, W + dv * ln - nrm * 0.016, nrm, 0.25, 0.034, BASALT_D, wb,
                tipf=0.42, cols=(LAVA, FLAME, HOT), fracs=(0.30, 0.40, 0.30), curl=12 * cs)
    n_pri = 5
    for i in range(n_pri):
        t = i / (n_pri - 1)
        dv = (H - W).normalized().lerp((T - W).normalized(), 0.66 + 0.34 * t).normalized()
        ln = (T - W).length * (0.92 + 0.10 * t) * (1.0 + 0.04 * ((i % 2) * 2 - 1))
        o = nrm * (0.065 + 0.004 * (n_pri - 1 - i))
        tipp = feather(B, W + dv * 0.04 + o, W + dv * ln + o, nrm, 0.23, 0.034, BASALT_D, tb, tipf=0.42,
                       cols=(LAVA, FLAME, HOT), fracs=(0.30, 0.40, 0.30), curl=12 * cs)
        if i == 2:
            ANCH["WingFire_" + side] = tuple(tipp)
    for i in range(4):
        t = (i + 0.5) / 4
        dv = (H - W).normalized().lerp((T - W).normalized(), 0.60 + 0.40 * t).normalized()
        o = nrm * 0.11
        feather(B, W + dv * 0.03 + o, W + dv * 0.36 + o, nrm, 0.20, 0.034, EMBER, tb, taper=0.5)


def eye(B, c, s, yaw=26, bone="Head", sc=1.0):
    """the Thunderbird's approved raptor eye: lid-heavy BLACK socket, FLAME iris, HOT spot, no pupil, no glint"""
    R = Euler((0, math.radians(-s * 18), math.radians(s * yaw)), "XYZ").to_matrix()
    c = Vector(c)
    B.add(c + R @ Vector((s * 0.003, 0, 0.007 * sc)), (0.053 * sc, 0.008, 0.026 * sc), BLACK, bone, R=R, studs=[],
          role="detail", bevel=0.004)
    B.add(c + R @ Vector((0.002 * s, -0.006, -0.002)), (0.042 * sc, 0.006, 0.014 * sc), FLAME, bone, R=R, studs=[],
          role="detail", bevel=0.003)
    B.add(c + R @ Vector((s * 0.016 * sc, -0.010, 0.0)), (0.017 * sc, 0.004, 0.006 * sc), HOT, bone, R=R,
          studs=[], role="detail", bevel=0.002)


def face_shingles(B, blk, face, rows, color_of, bone, size=(0.055, 0.02, 0.07)):
    """down-pointing shingles on the -y (face=-1, breast) or +y (face=+1, back) face of a rotated tapered block"""
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


def neck_cape(B, a, b, r, rows, bone, hem=False, col=EMBER, last_col=None):
    """flat-laid hackle cape (NOT standing blades): down-pointing EMBER shingles on the nape side of a neck segment;
    hem=True gives the lowest row a LAVA tip (a burning collar hem over the basalt mantle)"""
    a, b = Vector(a), Vector(b)
    dn = (b - a).normalized()
    xa = Vector((1, 0, 0))
    nn = (Vector((0, 1, 0)) - dn * dn.y).normalized()
    Rn = Matrix.Rotation(math.radians(-14), 3, xa) @ Matrix((xa, nn, dn)).transposed()
    for t, xs, last in rows:
        c = a.lerp(b, t)
        for x in xs:
            p = c + xa * x + nn * max(0.03, math.sqrt(max(0.0, r * r - x * x)) - 0.004)
            B.add(p, (0.06, 0.02, 0.09), (last_col or col) if last else col, bone, R=Rn, bot=(0.2, 1.0), role="limb",
                  bevel=0.008)
            if hem and last:
                B.add(p - dn * 0.075 + nn * 0.004, (0.034, 0.016, 0.03), LAVA, bone, R=Rn, bot=(0.14, 1.0), role="limb",
                      bevel=0.004, studs=[], nostud=True)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=313, tier=3, plates=False)
    # ================= body: slim EMBER breast leaning 40 deg, keel, lower body swallowing the knee, basalt saddles
    chest = B.add((0, -0.14, 1.02), (0.22, 0.21, 0.27), EMBER, "Chest", rot=(40, 0, 0), bot=(0.60, 0.55),
                  top=(0.90, 0.90), rnd=0.40)
    keel = B.seg((0, -0.22, 0.74), (0, -0.36, 1.14), 0.14, 0.07, EMBER, "Chest", bot=(0.55, 0.8), ext1=0.02,
                 rnd=0.4)                                          # keel (local z UP the keel: face -1 = its front)
    low = B.add((0, 0.08, 0.70), (0.17, 0.17, 0.16), EMBER, "Spine", rot=(48, 0, 0), bot=(0.22, 0.66),
                top=(0.92, 0.90), rnd=0.38)
    B.add(chest.world(Vector((0, 0.08, 0.0))), (0.20, 0.15, 0.25), BASALT, "Chest", R=chest.R, bot=(0.60, 0.55),
          top=(0.90, 0.90), rnd=0.40)                      # dorsal saddle: chest back
    B.add(low.world(Vector((0, 0.06, 0.0))), (0.155, 0.12, 0.15), BASALT, "Spine", R=low.R, bot=(0.72, 0.66),
          top=(0.92, 0.9), rnd=0.38)                       # dorsal saddle: lower back
    rump = B.add((0, 0.30, 0.60), (0.11, 0.10, 0.08), BASALT, "Spine", rot=(30, 0, 0), rnd=0.4)
    for x in (-0.06, 0.0, 0.06):                                                   # rump shingles over the knuckles
        p = Vector((x, 0.34, 0.66))
        B.add(p, (0.055, 0.02, 0.08), BASALT, "Spine", rot=(-60, 0, 0), bot=(0.2, 1.0), role="limb", bevel=0.008)
    B.seg((0, -0.06, 0.60), (0, 0.20, 0.52), 0.09, 0.03, PALE, "Spine", top=(0.7, 1.0))           # belly keel strip
    # breast: the upward-pointing PALE flame tongue rising from the belly - never a down V bib. It lies on the KEEL
    # front (the keel bulge is the most forward mass and hides the chest face): 1 / 2 / 3 / 4 PALE from the tip down
    xs4, xs3 = (-0.12, -0.04, 0.04, 0.12), (-0.08, 0.0, 0.08)

    def keel_col(r, x):
        if r == 0:
            return PALE if abs(x) < 1e-6 else EMBER
        if r == 1:
            return PALE if abs(x) < 0.05 else EMBER
        return PALE
    face_shingles(B, keel, -1, [(0.15, (-0.09, 0.0, 0.09)), (0.045, xs4), (-0.06, (-0.09, 0.0, 0.09)), (-0.165, xs4)],
                  keel_col, "Chest")
    face_shingles(B, chest, -1, [(0.16, xs4), (0.05, xs3), (-0.06, xs4), (-0.17, xs3)],
                  lambda r, x: PALE if r >= 2 or abs(x) < 0.05 else EMBER, "Chest")  # broad base + the centre column
    # tonal basalt mantle (no seams): 1, 4, 3 rows on the chest back, 3, 2 on the lower back
    face_shingles(B, chest, 1, [(0.18, (0.0,)), (0.06, xs4), (-0.08, xs3)], lambda r, x: BASALT, "Chest",
                  size=(0.06, 0.022, 0.085))
    face_shingles(B, low, 1, [(0.08, (-0.08, 0.0, 0.08)), (-0.06, (-0.04, 0.04))], lambda r, x: BASALT, "Spine",
                  size=(0.055, 0.02, 0.075))
    # flank skirt over the knee: EMBER top spikes, BASALT blades hung OUTSIDE the trousers' swing band (x 0.225)
    for s in (1, -1):
        for dy in (-0.06, 0.04):
            B.spike((s * 0.15, dy, 0.72), (s * 0.25, 0.65, -0.72), 0.18, 0.05, EMBER, "Spine", side=(s, 0, 0),
                    top=(0.2, 0.3))
        dv = Vector((s * 0.40, 0.62, -0.68)).normalized()
        for dy in (-0.06, 0.04):
            b0 = Vector((s * 0.225, dy, 0.63))
            B.bar(b0, b0 + dv * 0.15, Vector((s, 0, 0)), 0.10, 0.02, BASALT, "Spine", top=(0.2, 0.5), studs=[])
    # ================= the S-neck (2 bones) + flat hackle cape with a burning LAVA hem on the lowest row
    n1a, n1b = (0, -0.24, 1.12), (0, -0.43, 1.38)
    n2a, n2b = (0, -0.43, 1.34), (0, -0.37, 1.57)
    B.seg(n1a, n1b, 0.15, 0.15, EMBER, "Neck", ext=0.06, rnd=0.35)
    B.seg(n2a, n2b, 0.13, 0.13, EMBER, "Neck2", ext=0.03, ext1=0.03, rnd=0.35)
    # the PALE tongue's TIP climbs the throat (Neck front): 2 stepped blocks narrowing to a point = an upward flame
    na, nb = Vector(n1a), Vector(n1b)
    dn = (nb - na).normalized()
    nf = Vector((0, -dn.z, dn.y)) if dn.z > 0 else Vector((0, dn.z, -dn.y))      # the neck's front normal (-y)
    if nf.y > 0:
        nf = -nf
    sf = lambda t: na.lerp(nb, t) + nf * 0.142
    B.seg(sf(0.40), sf(0.82), 0.066, 0.018, PALE, "Neck", top=(0.66, 1.0), role="detail", bevel=0.006)
    B.seg(sf(0.80), sf(1.10), 0.044, 0.016, PALE, "Neck", top=(0.15, 0.8), role="detail", bevel=0.005)
    neck_cape(B, n2a, n2b, 0.13, [(0.80, (-0.065, 0.0, 0.065), False), (0.45, (-0.065, 0.0, 0.065), False)],
              "Neck2", col=BASALT)                         # a clean dark hood tail down the nape
    neck_cape(B, n1a, n1b, 0.15, [(0.90, (-0.11, -0.04, 0.04, 0.11), True)],
              "Neck", hem=True, col=EMBER, last_col=EMBER)     # one burning collar row (EMBER + LAVA tips) above the mantle
    # ================= falcon head (basalt hood, ember cheeks, gold hook)
    B.add(HC, (0.13, 0.125, 0.115), BASALT, "Head", top=(0.85, 0.85))                                  # cranium
    B.add(HC + Vector((0, -0.10, -0.045)), (0.10, 0.06, 0.075), BASALT, "Head", top=(0.9, 1))           # face
    B.add(HC + Vector((0, -0.03, -0.075)), (0.118, 0.10, 0.055), EMBER, "Head", rnd=0.35)              # cheeks/throat
    for s in (1, -1):
        B.bar(HC + Vector((s * 0.104, -0.13, -0.01)), HC + Vector((s * 0.12, -0.08, -0.10)), Vector((s, -0.2, 0)),
              0.03, 0.006, BASALT_D, "Head", studs=[], role="detail", bevel=0.003)                    # malar stripe
        eye(B, HC + Vector((s * 0.098, -0.128, 0.024)), s, sc=1.15)
        B.add(HC + Vector((s * 0.078, -0.088, 0.070)), (0.082, 0.038, 0.031), BASALT_D, "Head",
              rot=(0, -s * 21, s * 22), top=(0.8, 0.85), role="detail", bevel=0.012)            # fused V brow
    B.add(HC + Vector((0, -0.155, -0.015)), (0.068, 0.034, 0.036), GOLD_D, "Head", top=(0.85, 1))     # cere
    for s in (1, -1):
        B.add(HC + Vector((s * 0.07, -0.163, -0.005)), (0.004, 0.011, 0.008), BLACK, "Head", studs=[],
              role="detail", bevel=0.003)
    B.seg(HC + Vector((0, -0.15, -0.012)), HC + Vector((0, -0.28, -0.036)), 0.064, 0.056, GOLD, "Head",
          top=(0.6, 0.6), role="limb", nostud=True)                                                   # upper bill
    B.seg(HC + Vector((0, -0.25, -0.024)), HC + Vector((0, -0.325, -0.058)), 0.040, 0.036, GOLD, "Head",
          top=(0.8, 0.8), role="limb", nostud=True)                                                   # hook segment
    B.spike(HC + Vector((0, -0.322, -0.054)), (0, -0.45, -1), 0.07, 0.032, BLACK, "Head", top=(0.15, 0.2))  # hook tip
    for s in (1, -1):
        B.spike(HC + Vector((s * 0.052, -0.255, -0.058)), (0, 0, -1), 0.028, 0.020, GOLD_D, "Head", top=(0.2, 0.3))
    B.add(HC + Vector((0, -0.22, -0.066)), (0.05, 0.07, 0.005), MOUTH, "Head", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.add(HC + Vector((s * 0.06, -0.21, -0.058)), (0.004, 0.06, 0.008), MOUTH, "Head", rot=(-8, 0, 0), studs=[],
              role="detail", bevel=0.002)
    B.seg(HC + Vector((0, -0.15, -0.088)), HC + Vector((0, -0.27, -0.088)), 0.050, 0.020, GOLD_D, "Jaw",
          top=(0.7, 1), role="limb", nostud=True)                                                     # mandible
    B.add(HC + Vector((0, -0.21, -0.072)), (0.04, 0.055, 0.004), MOUTH, "Jaw", studs=[], role="detail", bevel=0.002)
    ANCH["Beak"] = tuple(HC + Vector((0, -0.34, -0.09)))
    # ================= the GOLD CIRCLET: a closed plain band on the crown top (no points, no gem)
    kwg = dict(studs=[], nostud=True, role="limb")
    zc = 1.725
    for y in (-0.53, -0.37):
        B.add((0, y, zc), (0.115, 0.015, 0.025), GOLD, "Head", bevel=0.007, **kwg)
    for s in (1, -1):
        B.add((s * 0.118, -0.45, zc - 0.01), (0.015, 0.08, 0.025), GOLD, "Head", bevel=0.007, **kwg)
        for y in (-0.53, -0.37):
            B.add((s * 0.115, y, zc - 0.005), (0.022, 0.022, 0.028), GOLD_D, "Head", bevel=0.009, **kwg)
    # ================= HERO 1: the FLAME CREST - 5 diamond leaf plumes from inside the circlet's back half
    for nm, root, d, L, w in (("C", (0, -0.44, 1.725), (0, 0.57, 0.82), 0.52, 0.10),
                              ("IL", (0.045, -0.45, 1.725), (0.20, 0.60, 0.77), 0.40, 0.09),
                              ("IR", (-0.045, -0.45, 1.725), (-0.20, 0.60, 0.77), 0.40, 0.09),
                              ("OL", (0.085, -0.43, 1.72), (0.38, 0.62, 0.69), 0.29, 0.08),
                              ("OR", (-0.085, -0.43, 1.72), (-0.38, 0.62, 0.69), 0.29, 0.08)):
        d = Vector(d).normalized()
        nrm = Vector((1, 0, 0)) - d * d.x
        nrm.normalize()
        crl = 11.0
        if (Matrix.Rotation(math.radians(crl), 3, nrm) @ d).y < d.y:
            crl = -crl
        cur = Vector(root) - d * 0.02
        wi = w
        for i, (c, fr, w1) in enumerate(((EMBER, 0.32, 0.9), (LAVA, 0.28, 0.75), (FLAME, 0.24, 0.5), (HOT, 0.16, 0.0))):
            if i:
                d = (Matrix.Rotation(math.radians(crl), 3, nrm) @ d).normalized()
            end = cur + d * L * fr
            top = (1.0, 0.14) if w1 == 0 else (w1 / (wi / w) / 1.0 if False else 1.0, (w * w1) / wi)
            B.add((cur + end) / 2, (wi / 4 + 0.002, wi / 2, (end - cur).length / 2 + 0.006), c, "Crest",
                  R=frame(end - cur, nrm), top=(1.0, 0.14) if w1 == 0 else (1.0, (w * w1) / wi), role="limb",
                  bevel=0.005, studs=[], nostud=True)
            cur = end - d * 0.006
            wi = w * w1 if w1 else wi
        if nm == "C":
            ANCH["CrestTip"] = tuple(cur + d * 0.006)
    # ================= wings
    for s, side in ((1, "L"), (-1, "R")):
        wing(B, s, side)
    # ================= legs: hidden EMBER thigh, BASALT trousers with a ragged cuff, bare SCARLET scaled tarsus
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A, T = X(HIP, s), X(KNEE, s), X(ANKLE, s), X(TOE, s)
        B.seg(H, K, 0.07, 0.08, EMBER, "Leg_" + side, ext=0.02, ext1=0.04, rnd=0.4)                   # hidden thigh
        B.seg(K, A + Vector((0, 0, 0.04)), 0.065, 0.068, BASALT, "Shin_" + side, ext=0.05, top=(1.23, 1.18), rnd=0.45)
        for i in range(7):                                                                    # ragged trouser cuff
            ang = 2 * math.pi * i / 7 + 0.3
            rv = Vector((s * math.cos(ang) * 0.072, math.sin(ang) * 0.076, 0))                # mirrored L / R
            L = 0.11 + 0.03 * ((i * 3) % 4) / 3.0
            B.spike(A + rv + Vector((0, 0, 0.11)), (rv.x * (3 if rv.x * s > 0 else 0), rv.y * 6 - 0.15, -1), L, 0.038,
                    BASALT if i % 2 == 0 else BASALT_D, "Shin_" + side, top=(0.2, 0.4))
        B.seg(A, T + Vector((0, 0.0, 0.03)), 0.052, 0.052, EMBER, "Foot_" + side, ext=0.03, role="limb")  # tarsus
        for t in (0.25, 0.5, 0.75):
            B.add(A.lerp(T + Vector((0, 0, 0.03)), t), (0.055, 0.056, 0.008), BASALT_D, "Foot_" + side,
                  rot=(-30, 0, 0), studs=[], role="detail", bevel=0.004)
        B.add(T + Vector((0, 0.005, 0.0)), (0.058, 0.058, 0.034), EMBER, "Foot_" + side, role="limb")
        for dx, spl in ((-0.040, -14.0), (0.0, 0.0), (0.045, 20.0)):          # inner / middle / outer, mirrored
            d = Vector((s * math.sin(math.radians(spl)), -math.cos(math.radians(spl)), 0))
            tb = T + Vector((s * dx, 0, 0)) + d * 0.10 + Vector((0, 0, -0.005))
            B.seg(T + Vector((s * dx * 0.5, -0.02, 0.0)), tb, 0.026, 0.024, EMBER, "Foot_" + side, role="limb")
            h0 = tb + d * 0.005 + Vector((0, 0, 0.008))
            B.spike(h0, d - Vector((0, 0, 0.62)), 0.072, 0.022, BLACK, "Foot_" + side)              # talon
            B.spike(h0 + (d - Vector((0, 0, 0.62))).normalized() * 0.058, Vector((0, 0, -1)) + d * 0.3, 0.034, 0.015,
                    BLACK, "Foot_" + side)                                                       # hooked tip
        B.spike(T + Vector((0, 0.05, 0.0)), (0, 1, -0.55), 0.11, 0.026, BLACK, "Foot_" + side)    # hallux talon
    # ================= HERO 2: the STREAMERS - round knuckle, BASALT shaft, EMBER shaft, LAVA lanceolate vane,
    # straight FLAME -> HOT tongue (collinear: a raised streamer never forms a hook)
    for nm, s in (("C", 1), ("L", 1), ("R", -1)):
        P = [X(p, s) for p in STREAM["C" if nm == "C" else "L"]]
        st = X(STREAM_START["C" if nm == "C" else "L"], s)
        b1, b2, b3 = "Streamer%s1" % nm, "Streamer%s2" % nm, "Streamer%s3" % nm
        B.add(P[0], (0.045, 0.05, 0.045), BASALT, b1, rnd=0.45)                                      # knuckle
        side = Vector((1, 0, 0))
        B.seg(st, P[1], 0.045, 0.04, BASALT, b1, side=side, ext=0.03, ext1=0.02, top=(0.92, 0.9))
        B.seg(P[1], P[2], 0.046, 0.036, EMBER, b2, side=side, ext=0.02, ext1=0.02, top=(0.9, 0.9))
        d = (P[3] - P[2]).normalized()
        up = (Vector((0, 0, 1)) - d * d.z).normalized()
        sx = d.cross(up).normalized()
        dia = (sx + up).normalized()                                                       # diamond section
        m = P[2].lerp(P[3], 0.45)
        kw = dict(studs=[], nostud=True, role="limb")
        B.seg(P[2] - d * 0.01, m, 0.042, 0.032, LAVA, b3, side=dia, top=(1.19, 1.0), **kw)             # lanceolate vane
        B.seg(m - d * 0.006, P[3], 0.050, 0.032, LAVA, b3, side=dia, top=(0.70, 0.8), **kw)             # (0.376 x 0.10 = 3.8 : 1)
        dt = (P[4] - P[3]).normalized()
        Lt = (P[4] - P[3]).length
        m2 = P[3] + dt * Lt * 0.6
        B.seg(P[3] - dt * 0.006, m2, 0.035, 0.026, FLAME, b3, side=dia, top=(0.6, 0.8), **kw)
        B.seg(m2 - dt * 0.006, P[4], 0.021, 0.021, HOT, b3, side=dia, top=(0.14, 0.3), **kw)
        ANCH["StreamerEnd_" + nm] = tuple(P[4])
    B.build()
    bk.stud_skin(k, PITCH)
    mn, mx = k.bounds()
    return {"TH": round(B.th, 3), "PITCH": PITCH, "H": round(mx.z, 3), "lowest": round(mn.z, 3),
            "crest_tip": [round(v, 3) for v in ANCH.get("CrestTip", (0, 0, 0))]}


# ------------------------------------------------------------------ rig (plan review 5.1)
def rig(k):
    k.joint("Spine", (0, 0.10, 0.70), "Root", tail=(0, -0.2, 0.35))
    k.joint("Chest", (0, -0.04, 0.92), "Spine", tail=(0, -0.25, 0.3))
    k.joint("Neck", (0, -0.24, 1.14), "Chest", tail=(0, -0.19, 0.22))
    k.joint("Neck2", (0, -0.43, 1.36), "Neck", tail=(0, 0.04, 0.16))
    k.joint("Head", tuple(HC + Vector((0, 0.08, -0.10))), "Neck2", tail=(0, -0.35, 0))       # throat pivot
    k.joint("Jaw", tuple(HC + Vector((0, -0.12, -0.075))), "Head", tail=(0, -0.2, 0))
    k.joint("Crest", tuple(CREST_P), "Head", tail=(0, 0.1, 0.12))
    k.joint("CrestTip", ANCH.get("CrestTip", (0, -0.19, 2.05)), "Crest", tail=(0, 0.05, 0.05))
    k.joint("Beak", ANCH.get("Beak", tuple(HC + Vector((0, -0.34, -0.09)))), "Head", tail=(0, -0.15, 0))
    k.joint("Core", (0, -0.30, 1.00), "Chest", tail=(0, -0.1, 0))
    k.joint("Pyre", (0, 0.05, 0.02), "Root", tail=(0, 0, 0.1))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Wing_" + side, X(WING.S, s), "Chest")
        k.joint("WingTip_" + side, X(WING.W, s), "Wing_" + side, tail=(s * 0.6, 0.2, 0.1))
        k.joint("WingFire_" + side, ANCH.get("WingFire_" + side, X(TIP, s)), "WingTip_" + side, tail=(s * 0.15, 0, 0))
        k.joint("Leg_" + side, X(HIP, s), "Spine")
        k.joint("Shin_" + side, X(KNEE, s), "Leg_" + side)
        k.joint("Foot_" + side, X(ANKLE, s), "Shin_" + side, tail=(0, -0.15, -0.1))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))
    k.joint("Tail", (0, 0.36, 0.56), "Spine", tail=(0, 0.15, -0.05))
    for nm, s in (("C", 1), ("L", 1), ("R", -1)):
        P = [X(p, s) for p in STREAM["C" if nm == "C" else "L"]]
        k.joint("Streamer%s1" % nm, tuple(P[0]), "Tail", tail=tuple(P[1] - P[0]))
        k.joint("Streamer%s2" % nm, tuple(P[1]), "Streamer%s1" % nm, tail=tuple(P[2] - P[1]))
        k.joint("Streamer%s3" % nm, tuple(P[2]), "Streamer%s2" % nm, tail=tuple(P[3] - P[2]))
        k.joint("StreamerEnd_" + nm, tuple(P[4]), "Streamer%s3" % nm, tail=tuple((P[4] - P[3]).normalized() * 0.08))


STREAMERS = ["Streamer%s%d" % (c, i) for c in "CLR" for i in (1, 2, 3)]


def check_pairs():
    W = ["Wing_L", "WingTip_L", "Wing_R", "WingTip_R"]
    P = [("Wing_L", "WingTip_L"), ("Wing_R", "WingTip_R"), ("WingTip_L", "WingTip_R"), ("Wing_L", "Wing_R"),
         ("WingTip_L", "Wing_R"), ("Wing_L", "WingTip_R")]
    for w in W:
        for b in ["Head", "Neck", "Neck2", "Crest", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Foot_L", "Foot_R",
                  "Chest", "Spine"] + STREAMERS:
            P.append((w, b))
    P += [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Shin_L", "Spine"), ("Shin_R", "Spine"),
          ("Head", "Chest"), ("Jaw", "Chest"), ("Jaw", "Neck"), ("Head", "Neck"), ("Crest", "Neck"),
          ("Crest", "Neck2"), ("Crest", "Chest")]
    ch = {c: ["Streamer%s%d" % (c, i) for i in (1, 2, 3)] for c in "CLR"}
    for a_, b_ in (("L", "C"), ("C", "R"), ("L", "R")):
        for x in ch[a_]:
            for y in ch[b_]:
                P.append((x, y))
    for x in STREAMERS:
        for y in ("Shin_L", "Shin_R", "Foot_L", "Foot_R"):
            P.append((x, y))
    for c in "CLR":
        P.append(("Streamer%s1" % c, "Spine"))
    return P


def joints():
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.12, "Wing_" + sd))
        K, A = Vector(X(KNEE, s)), Vector(X(ANKLE, s))
        d = (A - K).normalized()
        out.append((tuple(K - d * 0.08), tuple(K + d * 0.15), 0.10, "Shin_" + sd))     # knee (trouser top)
    out.append(((0, -0.36, 1.36), (0, -0.50, 1.36), 0.15, "Neck2"))                       # Neck -> Neck2
    out.append(((0, -0.33, 1.52), (0, -0.55, 1.52), 0.15, "Head"))                        # throat
    out.append(((0, -0.47, 1.72), (0, -0.40, 1.72), 0.06, "Crest"))                       # crest root
    out.append(((-0.08, -0.59, 1.545), (0.08, -0.59, 1.545), 0.04, "Jaw"))                # jaw hinge
    for nm, s in (("C", 1), ("L", 1), ("R", -1)):
        P = [X(p, s) for p in STREAM["C" if nm == "C" else "L"]]
        d = (P[1] - P[0]).normalized()
        out.append((tuple(P[0] - d * 0.03), tuple(P[0] + d * 0.06), 0.07, "Streamer%s1" % nm))
        for j, bn in ((1, "Streamer%s2" % nm), (2, "Streamer%s3" % nm)):
            dj = (P[j + 1] - P[j]).normalized()
            out.append((tuple(P[j] - dj * 0.03), tuple(P[j] + dj * 0.04), 0.055, bn))
    return out


def wings(k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WING.key(k, f, up, fwd, twist, tip, side)


HEAD_XF = []

# ------------------------------------------------------------------ ground fold (start = the Thunderbird's tested set;
# re-search with fold_search.py on this body per plan review 4.7)
FOLD = (86.0, 6.0, -80.0, 10.0)           # fold_search on this body: 0 hits, w90 0.349, min z 0.33, tip->vane 0.39
LIFT1 = (84.0, 16.0, -80.0, -15.0)
LIFT2 = (70.0, 24.0, -55.0, 0.0)
LIFT3 = (50.0, 20.0, -25.0, 10.0)
LIFT4 = (35.0, 8.0, -8.0, 10.0)
BREATH = (80.0, 26.0, -65.0, -10.0)


# ------------------------------------------------------------------ animation v1 (brief section 7). References (owner
# rule, _review/ANIM_REFERENCES_1014.md): #5 bird flapping + #8 banshee stroke (fly, takeoff, land, the rebirth rise;
# the body rises on the downstroke, the plumes stream nearly straight), #3 Sea Beasts (the jaw lags the head lift),
# #6 Monsters University (the train rise: crouch, then the spread in 5-7 f), #7 HTTYD (the look-back hold), #9 humpback
# mass timing (the pyre slump falls 2-3x slower than the rise), #4 dragon walk (strut weight, the head settles late).
# Rules: every ground clip starts and ends at FOLD and fold <-> open runs LIFT1..4 in order; head gyro in walk + fly;
# streamer motion is a travelling wave (X1 -> X2 -> X3 lag), L / C / R never in unison; any swing > 60 deg in one frame
# gets an in-between; no head shakes, no airborne spins, no stoop (Thunderbird). Model-round limits (v1 report D7-D9):
# planted crouches stay at Spine z >= -0.05 (the trouser tops reach the lower body), streamers on the ground at rest
# stay at X1 >= -4 (vanes >= -0.02), the fly tuck is THI 60 / roll 18, the rising legs spread 15.
import petkit as pk
import _common as cm

LEGS = ["Leg_L", "Leg_R"]
OPEN = (30.0, 0.0, 0.0, 0.0)
BOT = (-38.0, 8.0, 6.0, 4.0)
BRAKE = (24.0, 16.0, -10.0, -4.0)
DROOP1, DROOP2 = (-20.0, -10.0, 4.0, -6.0), (-45.0, -15.0, 6.0, -8.0)
PYRE = (-60.0, -22.0, 10.0, -6.0)
CH = "LCR"
PH = {"L": 0.0, "C": 0.33, "R": 0.66}
LAG = {"L": 0, "C": 1, "R": 2}          # frame offsets so the three plumes never move in unison
CROUCH = -0.05                         # deepest planted Spine z (v1 report D7)
WALK_LIFT, WALK_DIP = 0.08, 0.04       # strut swing lift / dip (0.10 drives the trouser into the belly; clip gate)
REGRIP_AMP, REGRIP_CURL = 0.045, 6.0   # idle talon re-grip (14 deg curled the talons into the ground)


def curve(keys, f):
    """smoothstep through (frame, value) keys"""
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / float(f1 - f0) if f1 > f0 else 1.0
            return v0 + (v1 - v0) * u * u * (3 - 2 * u)
    return keys[-1][1] if f > keys[-1][0] else keys[0][1]


def ease(u):
    u = max(0.0, min(1.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u)


def wp(k, f, P, side=None):
    wings(k, f, *P, side=side)


def blend(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def stream(k, f, c, x1=0.0, x2=0.0, x3=0.0, y1=0.0, y2=0.0, y3=0.0):
    """one plume chain c (L / C / R): pitch + LIFTS (+Y bones); yaw + swings the tip toward -x"""
    k.key("Streamer%s1" % c, f, rot=(x1, y1, 0))
    k.key("Streamer%s2" % c, f, rot=(x2, y2, 0))
    k.key("Streamer%s3" % c, f, rot=(x3, y3, 0))


def neck(k, f, n1=0.0, n2=0.0, hd=0.0, y1=0.0, y2=0.0, yh=0.0, jaw=0.0, crest=0.0):
    """Neck / Neck2 / Head pitch + = nose DOWN, yaw + = toward the bird's LEFT; Jaw + = open; Crest + = ERECT"""
    k.key("Neck", f, rot=(n1, y1, 0))
    k.key("Neck2", f, rot=(n2, y2, 0))
    k.key("Head", f, rot=(hd, yh, 0))
    k.key("Jaw", f, rot=(jaw, 0, 0))
    k.key("Crest", f, rot=(crest, 0, 0))


def rest_keys(k, f, z=0.0, pitch=0.0):
    k.key("Spine", f, rot=(pitch, 0, 0), loc=(0, 0, z))
    k.key("Chest", f, rot=(0, 0, 0))
    neck(k, f)
    wp(k, f, FOLD)
    for c in CH:
        stream(k, f, c)


def plant_frames(k, frames, dy=0.0, regrip=None, amp=0.07, curl=14.0):
    """feet on their rest spots (+dy); regrip = {leg: (f0, f1)}: that foot lifts `amp` and curls its toes"""
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        for leg in LEGS:
            z, toe = FOOT_LIFT, 0.0
            if regrip and leg in regrip and regrip[leg][0] <= f <= regrip[leg][1]:
                u = (f - regrip[leg][0]) / float(regrip[leg][1] - regrip[leg][0])
                z, toe = FOOT_LIFT + amp * math.sin(math.pi * u), curl * math.sin(math.pi * u)
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


# ---- idle
def idle(k):
    """SMOULDER (refs #7, #9): a bellows breath (2 cycles, the head kept level) with the crest swelling on each inhale;
    a constant streamer drift (travelling wave, L / C / R phases 0 / .33 / .66); the proud rise (the S straightens);
    a LICK up each plume in turn (L f18, C f48, R f78); the 44-deg LOOK BACK over the left shoulder at the follow
    camera, held dead still 18 f; a crest flare + glare with a crack of gape; a heat lift of the cloak (FOLD <-> LIFT1);
    a right talon re-grip; exact rest f120."""
    n = 120
    k.new_action("idle", n, True)
    prise = [(0, 0), (10, 0), (22, 1), (64, 1), (74, 0), (120, 0)]
    look = [(0, 0), (38, 0), (46, 1), (64, 1), (74, 0), (120, 0)]
    crest = [(0, 0), (84, 0), (88, 12), (94, 12), (100, 0), (120, 0)]
    glare = [(0, 0), (84, 0), (88, 6), (96, 6), (100, 0), (120, 0)]
    jaw = [(0, 0), (86, 0), (88, 4), (96, 4), (98, 0), (120, 0)]
    heat = [(0, 0), (92, 0), (98, 0.5), (104, 0), (120, 0)]
    LICK0 = {"L": 18, "C": 48, "R": 78}
    for f in range(n + 1):
        b = 0.5 + 0.5 * math.cos(2 * math.pi * (f - 22) / 60.0)          # inhale peaks f22 / f82
        pr, lk = curve(prise, f), curve(look, f)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.008 * b))
        k.key("Chest", f, rot=(-1.5 * b, 0, 0))
        neck(k, f, n1=-4 * pr, n2=-4 * pr, hd=7 * pr + 1.5 * b + curve(glare, f), y1=8 * lk, y2=12 * lk, yh=24 * lk,
             jaw=curve(jaw, f), crest=4 * b + curve(crest, f))
        wp(k, f, blend(FOLD, LIFT1, curve(heat, f)))
        for c in CH:
            ph, l0 = PH[c], LICK0[c]
            a2 = curve([(0, 0), (l0, 0), (l0 + 5, 8), (l0 + 12, -1), (l0 + 16, 0), (n, 0)], f)      # (ground floor:
            a3 = curve([(0, 0), (l0, 0), (l0 + 5, 18), (l0 + 12, -1), (l0 + 16, 0), (n, 0)], f)     # review 1 s6.2)
            stream(k, f, c, 1.5 + 1.5 * pk.wave(f, n, ph, 2), 1 + 2 * pk.wave(f, n, ph - 0.08, 2) + a2,
                   2 + 3 * pk.wave(f, n, ph - 0.16, 2) + a3, y3=3 * pk.wave(f, n, ph - 0.16 + 0.25, 2))
    plant_frames(k, range(0, n + 1), regrip={"Leg_R": (56, 62)}, amp=REGRIP_AMP, curl=REGRIP_CURL)
    k.finish()
    k.meta["planted"] = ["Leg_L"]
    k.events["idle"] = {"lick1": round(23 / n, 3), "ember1": round(24 / n, 3), "lick2": round(53 / n, 3),
                        "lick3": round(83 / n, 3), "ember2": round(84 / n, 3), "flare": round(88 / n, 3)}


# ---- walk
def walk(k):
    """STALKING STRUT (ref #4, the Thunderbird's approved ROLLING STRUT machinery): the body rolls +-4 / yaws +-3 over
    the stance leg with an asymmetric contact dip (-0.04 within 3 f), the head gyro-stabilised (cancels 75 %: Neck .2 /
    Neck2 .25 / Head .3), high-stepping (lift 0.10) toes curled in the swing; the cloak folded with a 0-15 % LIFT1
    blend on contacts; the plumes trail on X1 +3 with a travelling yaw / pitch wave (lags 3 / 6 / 9 and 3 / 5 / 7 f)
    and the crest follows through 3 f after each contact."""
    n = 28

    def dip(f):
        t = f % (n // 2)
        if t <= 3:
            u = t / 3.0
            return -WALK_DIP * (u * u * (3 - 2 * u))
        u = (t - 3) / (n / 2 - 3)
        return -WALK_DIP * (1 - u * u * (3 - 2 * u))

    def body(f):
        sp = 1.2 * pk.wave(f, n, 0.1, 2)
        sy = 3 * pk.wave(f, n, 0.0)
        sr = 4 * pk.wave(f, n, 0.05)
        cy, cr = -1.5 * pk.wave(f, n, 0.05), -1.5 * pk.wave(f, n, 0.05)
        k.key("Spine", f, rot=(sp, sy, sr), loc=(0, 0, dip(f)))
        k.key("Chest", f, rot=(0, cy, cr))
        P, Y, R = sp, sy + cy, sr + cr
        k.key("Neck", f, rot=(-0.2 * P, -0.2 * Y, -0.2 * R))
        k.key("Neck2", f, rot=(-0.25 * P, -0.25 * Y, -0.25 * R))
        k.key("Head", f, rot=(-0.3 * P, -0.3 * Y, -0.3 * R))
        k.key("Jaw", f, rot=(0, 0, 0))
        k.key("Crest", f, rot=(2 * dip(f - 3) / -WALK_DIP, 0, 0))
        c = max(0.0, math.cos(2 * math.pi * (2 * f / n)))           # contact pulse (2 per cycle)
        wp(k, f, blend(FOLD, LIFT1, 0.15 * c ** 3))
        for ch in CH:
            o = LAG[ch]
            yb = [3 * pk.wave(f - lag - o, n, 0.0) for lag in (3, 6, 9)]
            dn = [dip(f - lag - o) / -WALK_DIP for lag in (3, 5, 7)]
            stream(k, f, ch, 4 - 2 * (2 * dn[0] - 1), -3 * (2 * dn[1] - 1), 2 - 4 * (2 * dn[2] - 1),
                   y1=0.5 * yb[0], y2=1.0 * yb[1], y3=1.5 * yb[2])
    orig = k.solve_leg

    def strut(leg, f, T, foot_z=0.0, toe=None):
        lift = max(0.0, T.z)
        sx = 1.0 if leg.endswith("L") else -1.0                   # the passing foot swings wide of the keel
        T = Vector(T) + Vector((sx * 0.06 * min(1.0, lift / 0.05), 0, FOOT_LIFT))      # wide swing: clears the belly
        return orig(leg, f, T, foot_z, toe=22.0 * min(1.0, lift / 0.09))
    k.solve_leg = strut
    try:
        return cm.biped_walk(k, n, 0.15, WALK_LIFT, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.6)
    finally:
        del k.solve_leg


# ---- flight
FPITCH, FN1, FN2, FHEAD = 45.0, -8.0, -8.0, -28.0
THI, SHI, FOO, FSPREAD = 60.0, -40.0, 70.0, 18.0            # the tuck (v1 report D9)


def fly_legs(k, f, ph, amt=1.0):
    for s, side in ((1, "L"), (-1, "R")):
        p = ph + 0.03 * s
        k.key("Leg_" + side, f, rot=((THI + 3 * math.sin(2 * math.pi * (p - 0.15))) * amt, 0, -s * FSPREAD * amt),
              loc=(0, 0, 0))
        k.key("Shin_" + side, f, rot=((SHI - 4 * math.sin(2 * math.pi * (p - 0.30))) * amt, 0, 0))
        k.key("Foot_" + side, f, rot=((FOO + 6 * math.sin(2 * math.pi * (p - 0.42))) * amt, 0, 0))


def fly_stream(ph, c):
    """the BURNING WAKE: X1 -22 with a travelling S (+-5 / 9 / 13, lag 0.10 cycle, X1 peaking 0.15 after the
    downstroke starts); a forked fan (L -8 / R +8); X3 lateral +-3 offset 0.25; the chains offset 0.03 cycle"""
    q = ph - 0.03 * LAG[c]
    fan = {"L": -8.0, "C": 0.0, "R": 8.0}[c]
    w = lambda d: math.cos(2 * math.pi * (q - d))
    return dict(x1=-22 + 5 * w(0.15), x2=9 * w(0.25), x3=13 * w(0.35), y1=fan, y3=3 * w(0.60))


def fly_pose(k, f, ph, legs=True, plumes=True):
    w = wing3.stroke(ph, top=34, bot=-40, down=0.45, sweep=10, twist=10, fold=36)
    wings(k, f, w["up"], w["fwd"], w["twist"], w["tip"])
    rise = math.cos(2 * math.pi * (ph - 0.45))               # the body rises on the downstroke
    sp = FPITCH - 3 * math.sin(2 * math.pi * (ph - 0.1))
    g = 1.5 * math.sin(2 * math.pi * (ph - 0.1))
    k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, 0.10 + 0.07 * rise))
    k.key("Chest", f, rot=(-2 * math.sin(2 * math.pi * (ph - 0.2)), 0, 0))
    neck(k, f, n1=FN1 + 0.75 * g, n2=FN2 + 0.75 * g, hd=FHEAD - 1.5 * g + 2 * math.sin(2 * math.pi * (ph - 0.2)),
         crest=-6 + 2 * math.sin(2 * math.pi * (ph - 0.1)))
    if plumes:
        for c in CH:
            stream(k, f, c, **fly_stream(ph, c))
    if legs:
        fly_legs(k, f, ph)


def fly(k):
    """BURNING WAKE (refs #5 + #8): a regal 32-f beat (slower than the Thunderbird's 28), the outer wing tucks on the
    upstroke, the body rises on the downstroke, the head level; three plumes trail a travelling S-wave fire wake."""
    n = 32
    k.new_action("fly", n, True)
    for f in range(0, n + 1):
        fly_pose(k, f, f / n)
    k.finish()


def takeoff(k):
    """(refs #5 + #8) the Thunderbird keys: crouch (D7 depth) with the cloak opening FOLD -> LIFT1..4 -> OPEN, LAUNCH on
    the big downbeat (f11), legs push then tuck, into the flight cycle; the plumes DRAG (sag, hang at the launch with a
    2-f lag down the chain, swing back into the trail with a +6 overshoot); the crest erects at the crouch."""
    n = 30
    k.new_action("takeoff", n, False)
    rest_keys(k, 0)
    for f, z, p, ch, hd, w in ((3, -0.02, 4, 2, -2, LIFT1), (6, -0.035, 8, 4, -6, LIFT2), (8, -0.045, 9, 5, -9, LIFT3),
                               (9, -0.05, 10, 6, -11, LIFT4), (10, -0.05, 10, 6, -12, OPEN),
                               (13, 0.08, 20, 0, -20, (-14, 8, 8, -6)), (16, 0.14, 30, -2, -26, BOT)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        neck(k, f, n1=-p * 0.12, n2=-p * 0.13, hd=hd, crest=curve([(0, 0), (10, 8), (16, 0)], f))
        wp(k, f, w)
    tr = fly_stream(0.0, "C")
    for f in range(1, 23):
        for c in CH:
            o = LAG[c]
            x1 = curve([(0, 0), (3, -4), (10, -4), (13, -12), (16, -12), (21, tr["x1"] + 6), (23, fly_stream(0.0, c)["x1"])],
                       f - o)
            x2 = curve([(0, 0), (5, 0), (15, -8), (18, -8), (21, 4), (23, fly_stream(0.0, c)["x2"])], f - o)
            x3 = curve([(0, 0), (7, 0), (17, -4), (20, -4), (22, 2), (23, fly_stream(0.0, c)["x3"])], f - o)
            stream(k, f, c, x1, x2, x3, y1=curve([(0, 0), (16, 0), (23, fly_stream(0.0, c)["y1"])], f))
    fly_pose(k, 23, 0.0)
    fly_pose(k, n, 0.45)
    plant_frames(k, range(0, 13))
    legs_fk(k, 15, 24, -10, 40)
    legs_fk(k, 19, 50, -30, 66, spread=15)
    fly_legs(k, 23, 0.0)
    fly_legs(k, n, 0.45)
    lift_air_frames(k, range(13, n + 1))
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    """(ref #5: the tail fans to brake) the Thunderbird flare + brake + reaching talons to f15 with the plumes FLARED up
    (+20 / +10 / +6); TOUCH f17 with the cloak at LIFT4 (never the raised V), a D7-depth absorb, then LIFT4 -> LIFT3 ->
    LIFT2 -> LIFT1 -> FOLD (the tested brake path); the plumes swing down with the momentum and settle."""
    n = 32
    k.new_action("land", n, False)
    fly_pose(k, 0, 0.0)
    for f, p, z, nk, hd, w, lg in (
            (6, 16, 0.10, -4, -18, BRAKE, (40, -20, 50)),
            (10, -4, 0.10, 0, -8, (-24, 22, -10, 8), (-24, 4, -8)),
            (13, -6, 0.08, 0, -6, (22, 18, -8, -6), (-24, 10, -20)),
            (15, -4, 0.04, 0, -4, (30, 10, -6, -8), (-14, 6, -20))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(-3, 0, 0))
        neck(k, f, n1=nk * 0.5, n2=nk * 0.5, hd=hd)
        wp(k, f, w)
        legs_fk(k, f, *lg)
    for f, z, p, w in ((17, -0.04, 6, LIFT4), (22, -0.03, 4, LIFT4), (24, -0.02, 3, LIFT3), (26, -0.012, 2, LIFT2),
                       (28, -0.005, 1, LIFT1), (31, 0.0, 0, FOLD)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(2, 0, 0))
        neck(k, f, n1=p * 0.25, n2=p * 0.25, hd=-p * 0.4)
        wp(k, f, w)
    for f in range(1, n + 1):
        for c in CH:
            o = LAG[c]
            x1 = curve([(0, fly_stream(0.0, c)["x1"]), (6, 20), (15, 20), (20, -3), (26, 1), (30, 0)], f - o)
            x2 = curve([(0, fly_stream(0.0, c)["x2"]), (8, 10), (16, 10), (22, -2), (28, 0)], f - o)
            x3 = curve([(0, fly_stream(0.0, c)["x3"]), (9, 6), (17, 6), (23, -2), (29, 0)], f - o)
            stream(k, f, c, x1, x2, x3, y1=curve([(0, fly_stream(0.0, c)["y1"]), (10, 0)], f))
    rest_keys(k, n)
    lift_air_frames(k, range(0, 17))
    plant_frames(k, range(17, n + 1))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(17 / n, 3)}


# ---- roar
def roar(k):
    """FIRE-TRAIN SCREECH (refs #6, #3): gather (head in, LIFT1 -> LIFT2, the plumes sag); the TRAIN RISE: the cloak
    lifts to BREATH (never the V) while the three plumes rise into a fire train behind the hips (X1 +56 / X2 +24 /
    X3 -14, 2-f lag down the chain), the crest erects; the head thrusts forward and the jaw opens 3 f after it
    (SCREECH f25); a jaw buzz + the TRAIN RATTLE (plume shiver, L / C / R 1 f apart); release with a drop overshoot,
    the cloak back through LIFT1 to FOLD; exact rest f66."""
    n = 66
    k.new_action("roar", n, False)
    zc = [(0, 0), (10, -0.04), (20, 0), (56, 0), (66, 0)]
    pc = [(0, 0), (10, 4), (20, -4), (46, -4), (56, 0), (66, 0)]
    n1 = [(0, 0), (10, 6), (20, 6), (24, 8), (46, 8), (56, 0), (66, 0)]
    n2 = [(0, 0), (10, 4), (20, 4), (24, -6), (46, -6), (56, 0), (66, 0)]
    hd = [(0, 0), (10, 4), (20, 4), (24, -6), (46, -6), (56, 0), (66, 0)]
    jw = [(0, 0), (23, 0), (26, 34), (46, 34), (52, 0), (66, 0)]
    cr = [(0, 0), (12, 0), (18, 14), (50, 14), (56, 0), (66, 0)]
    wk = [(0, FOLD), (5, LIFT1), (52, LIFT1), (56, FOLD), (66, FOLD)]     # the train in front of LIFT1 (review 1 s6.4)
    for f, w in wk:
        wp(k, f, w)
    for f in range(n + 1):
        k.key("Spine", f, rot=(curve(pc, f), 0, 0), loc=(0, 0, curve(zc, f)))
        k.key("Chest", f, rot=(0, 0, 0))
        buzz = (2 if (f // 3) % 2 else -2) if 27 <= f <= 45 else 0
        neck(k, f, n1=curve(n1, f), n2=curve(n2, f), hd=curve(hd, f), jaw=curve(jw, f) + buzz, crest=curve(cr, f))
        for c in CH:
            o = LAG[c]
            sh2 = (3 if ((f + o) // 2) % 2 else -3) if 27 <= f <= 46 else 0
            sh3 = (5 if ((f + o) // 2) % 2 else -5) if 27 <= f <= 46 else 0
            x1 = curve([(0, 0), (8, -4), (10, -4), (17, 56), (46, 56), (54, -4), (59, 3), (62, 0), (66, 0)], f)
            x2 = curve([(0, 0), (10, -2), (12, -2), (19, 24), (48, 24), (56, -2), (61, 2), (64, 0), (66, 0)], f)
            x3 = curve([(0, 0), (12, 0), (14, 0), (20, -14), (50, -14), (58, 0), (66, 0)], f)
            stream(k, f, c, x1, x2 + sh2, x3 + sh3)
    plant_frames(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["roar"] = {"screech": round(25 / n, 3), "rattle": round(30 / n, 3)}


# ---- act
def act_rebirth(k):
    """ASHES TO FLAME (signature; refs #9, #5 + #8, #3): IGNITE (crest flares, the neck straightens, the plumes lift);
    the PYRE: the cloak opens and sinks back into a wide burning droop around the bird (LIFT1..4 -> OPEN -> DROOP1 ->
    DROOP2 -> PYRE), the head bows to the breast, the crest lies back, the plumes settle on the ground; EMBER SLEEP dead
    still; two HEARTBEATS; AWAKEN (the head snaps up first); a wind-up and LAUNCH on one huge sweep, two beats lift it
    into the heraldic PHOENIX RISING with a screech (the plumes hang and swing); descend + brake, TOUCH on LIFT4, fold
    LIFT3..1 -> FOLD; a slow breath; exact rest f104."""
    n = 104
    k.new_action("act_rebirth", n, False)
    wk = [(0, FOLD), (4, LIFT1), (8, LIFT2), (10, LIFT3), (11, LIFT4), (13, OPEN), (17, DROOP1), (21, DROOP2),
          (26, PYRE), (50, PYRE), (51, DROOP2), (52, DROOP1), (54, OPEN), (58, BOT), (64, OPEN), (68, BOT), (72, OPEN),
          (76, OPEN), (80, BRAKE), (82, LIFT4), (85, LIFT3), (87, LIFT2), (89, LIFT1), (92, FOLD), (104, FOLD)]
    for f, w in wk:
        wp(k, f, w)
    zc = [(0, 0), (10, -0.02), (26, CROUCH), (34, CROUCH), (36, CROUCH + 0.012), (40, CROUCH), (42, CROUCH + 0.018),
          (46, CROUCH), (53, CROUCH), (58, 0.14), (64, 0.30), (68, 0.44), (72, 0.46), (76, 0.46), (80, 0.16),
          (82, CROUCH), (88, -0.01), (96, 0.0), (104, 0)]
    pc = [(0, 0), (10, 0), (26, 9), (46, 9), (50, 6), (53, 4), (58, -2), (68, -2), (72, -4), (76, -4), (80, 6),
          (82, 4), (92, 0), (104, 0)]
    chest = [(0, 0), (34, 0), (36, -3), (40, 0), (42, -5), (46, 0), (96, 0), (98, -1.5), (102, 0), (104, 0)]
    n1 = [(0, 0), (10, -4), (13, -4), (26, 12), (46, 12), (50, -4), (68, -4), (72, -6), (76, -6), (82, 0), (104, 0)]
    n2 = [(0, 0), (10, -2), (13, -2), (26, 12), (46, 12), (50, -4), (68, -4), (72, -4), (76, -4), (82, 0), (104, 0)]
    hd = [(0, 0), (10, 6), (13, 6), (26, 20), (46, 20), (48, 8), (50, -6), (68, -6), (72, -4), (76, -4), (82, 0),
          (104, 0)]
    cr = [(0, 0), (8, 14), (13, 14), (26, -10), (34, -10), (36, -6), (40, -10), (42, -2), (46, -10), (49, 16),
          (76, 16), (82, 6), (92, 0), (96, -3), (100, 0), (104, 0)]
    jw = [(0, 0), (69, 0), (72, 30), (76, 30), (80, 0), (104, 0)]
    for f in range(n + 1):
        k.key("Spine", f, rot=(curve(pc, f), 0, 0), loc=(0, 0, curve(zc, f)))
        k.key("Chest", f, rot=(curve(chest, f), 0, 0))
        buzz = (2 if (f // 2) % 2 else -2) if 72 <= f <= 76 else 0
        neck(k, f, n1=curve(n1, f), n2=curve(n2, f), hd=curve(hd, f), jaw=curve(jw, f) + buzz, crest=curve(cr, f))
        for c in CH:
            o = LAG[c]
            x1 = curve([(0, 0), (8, 8), (13, 8), (26, -4), (53, -4), (54, 10), (57, -6), (61, 6), (66, -10),
                        (70, -18), (76, -18), (80, 16), (84, -4), (88, 0), (104, 0)], f - o)    # hang -18 (review s6.3)
            x2 = curve([(0, 0), (10, 6), (15, 6), (28, -4), (55, 6), (59, -4), (62, 14), (68, -6), (72, -6), (76, -6),
                        (82, 10), (86, -3), (90, 0), (104, 0)], f - o)
            x3 = curve([(0, 0), (12, 4), (17, 4), (30, -2), (34, -2), (36, 3), (40, -2), (42, 6), (46, -2), (57, 4),
                        (60, -8), (64, 18), (70, 4), (76, 4), (84, 6), (88, -2), (92, 0), (104, 0)], f - o)
            stream(k, f, c, x1, x2, x3)
    plant_frames(k, range(0, 54))
    legs_fk(k, 57, 24, -10, 40)
    legs_fk(k, 66, 50, -30, 66, spread=15)
    legs_fk(k, 76, 50, -30, 66, spread=15)
    legs_fk(k, 80, -14, 6, -20)
    lift_air_frames(k, range(54, 82))
    plant_frames(k, range(82, n + 1))
    k.finish(loop=False)
    k.events["act_rebirth"] = {"ignite": round(8 / n, 3), "pyre": round(20 / n, 3), "ash": round(30 / n, 3),
                               "heartbeat1": round(36 / n, 3), "heartbeat2": round(42 / n, 3),
                               "rebirth": round(54 / n, 3), "reborn": round(72 / n, 3), "touch": round(82 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    act_rebirth(k)
    return stride
