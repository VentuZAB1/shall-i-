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
H_MODEL = 2.05                                     # centre crest tip at idle f0
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
STREAM = {"C": [(0, 0.38, 0.60), (0, 0.78, 0.31), (0, 1.12, 0.135), (0, 1.48, 0.20), (0, 1.64, 0.27)],
          "L": [(0.095, 0.37, 0.53), (0.125, 0.72, 0.27), (0.20, 1.03, 0.14), (0.27, 1.33, 0.21), (0.30, 1.46, 0.28)]}
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
    face_shingles(B, low, -1, [(0.09, (-0.09, 0.0, 0.09)), (-0.02, (-0.10, -0.035, 0.035, 0.10))],
                  lambda r, x: PALE, "Spine", size=(0.05, 0.02, 0.065))         # the pale belly under the tongue
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
    neck_cape(B, n2a, n2b, 0.13, [(0.70, (-0.07, 0.0, 0.07), False), (0.35, (-0.10, -0.035, 0.035, 0.10), False)],
              "Neck2", col=BASALT)                         # the dark hood runs down the nape (shares: EMBER <= target)
    neck_cape(B, n1a, n1b, 0.15, [(0.70, (-0.08, 0.0, 0.08), False), (0.30, (-0.11, -0.04, 0.04, 0.11), True)],
              "Neck", hem=True, col=BASALT, last_col=EMBER)     # BASALT cape over an EMBER collar + LAVA hem
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
    B.seg(HC + Vector((0, -0.255, -0.006)), HC + Vector((0, -0.325, -0.050)), 0.038, 0.044, GOLD, "Head",
          top=(0.8, 0.8), role="limb", nostud=True)                                                   # hook segment
    B.spike(HC + Vector((0, -0.32, -0.046)), (0, -0.55, -1), 0.075, 0.032, BLACK, "Head", top=(0.15, 0.2))  # hook tip
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
        for dx, dy in ((-0.045, -0.08), (0.0, -0.10), (0.045, -0.08)):
            d = Vector((dx * 1.2, dy, 0)).normalized()
            tb = T + Vector((dx, 0, 0)) + d * 0.10 + Vector((0, 0, -0.005))
            B.seg(T + Vector((dx * 0.5, -0.02, 0.0)), tb, 0.026, 0.024, EMBER, "Foot_" + side, role="limb")
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


# ------------------------------------------------------------------ animation helpers (v0: model-gate stub only - the
# real clips follow the brief section 7 after the model review)
import petkit as pk

LEGS = ["Leg_L", "Leg_R"]


def ease(u):
    u = max(0.0, min(1.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u)


def wp(k, f, P, side=None):
    wings(k, f, *P, side=side)


def folded(k, f, du=0.0, dfwd=0.0, dtw=0.0, dtip=0.0, side=None):
    wings(k, f, FOLD[0] + du, FOLD[1] + dfwd, FOLD[2] + dtw, FOLD[3] + dtip, side)


def blend(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def streamers(k, f, x1=0.0, x2=0.0, x3=0.0, yaw=0.0, spread=0.0):
    """kit pitch + LIFTS a +Y streamer; spread fans L / R out (yaw)"""
    for c, s in (("C", 0), ("L", 1), ("R", -1)):
        k.key("Streamer%s1" % c, f, rot=(x1, yaw * 0.5 + s * spread, 0))
        k.key("Streamer%s2" % c, f, rot=(x2, yaw * 0.3, 0))
        k.key("Streamer%s3" % c, f, rot=(x3, yaw * 0.2, 0))


def rest_keys(k, f, z=0.0, pitch=0.0):
    k.key("Spine", f, rot=(pitch, 0, 0), loc=(0, 0, z))
    for b in ("Chest", "Neck", "Neck2", "Head", "Jaw", "Crest"):
        k.key(b, f, rot=(0, 0, 0))
    folded(k, f)
    streamers(k, f)


def plant_frames(k, frames, dy=0.0, regrip=None):
    """feet on their rest spots (+dy); regrip = {leg: (f0, f1)}: that foot lifts 0.07 and curls its toes"""
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


def idle(k):
    """v0 STUB: the cloak fold held (model gate shares / portrait at idle f0)"""
    n = 120
    k.new_action("idle", n, True)
    for f in (0, 60, n):
        rest_keys(k, f)
    plant_frames(k, range(0, n + 1, 10))
    k.finish()
    k.meta["planted"] = LEGS


def anim(k):
    idle(k)
    return 0.0
