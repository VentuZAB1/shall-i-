# Hammerjaw Shark v2 (Tide egg, NEW 5.5% pet, 2026-10-14) - FIERCE style "THE REEF BREAKER" (review 1 brief): an
# armoured war-hammerhead swimming through the air like our Kraken (MOTION Swim). One lofted fusiform hull (no steps,
# no neck), a WAR-HAMMER head (studded steel cephalofoil, dark armour helm outlined in coral, chunky armour eye lobes
# with coral fierce eyes under back-swept brow spikes, centre notch), a deep crescent jaw resting 10 deg open (teeth
# outside the lip, dark mouth), a war-back of 6 shingled gunmetal lames split by coral seams with jagged lower edges
# and a keel ridge, steel-blue flanks over a crisp white belly, 5 coral gill slashes, tapered claw scars (left side),
# falcate stacked-block fins with 3-step coral leading edges, a heterocercal crescent tail on Tail4, peduncle keels.
# Old version: _tools/rex_versions/HammerjawShark_v1.py. No glow (Studio VFX on the anchors).
import math
from mathutils import Vector, Matrix

DISPLAY = "Hammerjaw Shark"
MOTION = "Swim"
RIG = "fish"
HEIGHT = 8.0        # dorsal tip in studs at x1 (above Kappa 7 / Kraken 7.5, room for the secret above)

# Blender colours (Roblox renders ~0.6x darker)
ARMOR = (46, 60, 88)         # gunmetal navy: lames, helm, eye lobes, brows, chin plate, keel, fairings, keels
STEEL = (70, 130, 180)       # true steel-blue: flanks, head core, hammer, fins, tail sides
FIN_IN = (56, 104, 150)      # inner fin panels
BELLY = (232, 236, 244)
BELLY_D = (196, 204, 222)
CORAL_D = (196, 58, 36)      # coral 3-step (the tier step over the commons' flat coral)
CORAL = (255, 118, 58)
CORAL_HOT = (255, 206, 150)
SCAR = (236, 176, 160)
MOUTH = (60, 16, 28)
TEETH = (240, 236, 222)
BLACK = (14, 14, 22)

Z0 = 0.62                    # body axis height (it hovers)
H_MODEL = Z0 + 0.82          # dorsal tip
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)

# fusiform hull stations: y, half-width, top z, bottom z (z relative to Z0)
STATIONS = [(-0.80, 0.20, 0.17, -0.12), (-0.48, 0.25, 0.29, -0.23), (-0.10, 0.21, 0.25, -0.19),
            (0.30, 0.15, 0.17, -0.15), (0.66, 0.095, 0.12, -0.10), (0.98, 0.055, 0.10, -0.04),
            (1.06, 0.045, 0.085, -0.025)]
JAW_P = Vector((0, -0.80, Z0 - 0.08))
JAW_OPEN = 10.0              # the jaw is MODELLED 10 deg open (teeth + dark mouth read in the icon)
ANCHORS = {}


def hull(y):
    """(half-width, centre z, half-depth) of the hull at y (linear between stations, clamped)"""
    S = STATIONS
    if y <= S[0][0]:
        a, b = S[0], S[1]
    elif y >= S[-1][0]:
        a, b = S[-2], S[-1]
    else:
        a, b = next((S[i], S[i + 1]) for i in range(len(S) - 1) if S[i][0] <= y <= S[i + 1][0])
    t = (y - a[0]) / (b[0] - a[0])
    hw = a[1] + (b[1] - a[1]) * t
    top = a[2] + (b[2] - a[2]) * t
    bot = a[3] + (b[3] - a[3]) * t
    return hw, Z0 + (top + bot) / 2, (top - bot) / 2


def bone_at(y):
    return "Chest" if y < -0.20 else "Spine" if y < 0.30 else "Tail1" if y < 0.62 else "Tail2" if y < 0.90         else "Tail3"


def jawpt(p):
    """rotate a closed-jaw point about the jaw hinge by JAW_OPEN (front goes down)"""
    a = math.radians(JAW_OPEN)
    q = Vector(p) - JAW_P
    return JAW_P + Vector((q.x, q.y * math.cos(a) - q.z * math.sin(a), q.y * math.sin(a) + q.z * math.cos(a)))


def loft(B, y0, y1, color, bone, grow=0.0, zlo=None, zhi=None, ext1=0.0, scale0=1.0, **kw):
    """hull section y0 -> y1 (y0 < y1): tapered rounded seg whose ends match the stations. grow pads the width/top;
    zlo / zhi (fractions of the half-depth, -1 bottom .. +1 top) cut a horizontal band (lames, belly shells)"""
    pts = []
    for y in (y0, y1 + ext1):
        hw, zc, hd = hull(y)
        lo = zc + (zlo if zlo is not None else -1.0) * hd - (grow if zlo is None or zlo <= -1 else 0.0)
        hi = zc + (zhi if zhi is not None else 1.0) * hd + (grow if zhi is None or zhi >= 1 else 0.0)
        pts.append((Vector((0, y, (lo + hi) / 2)), hw + grow, (hi - lo) / 2))
    (p0, w0, d0), (p1, w1, d1) = pts
    kw.setdefault("rnd", 0.40)
    return B.seg(p0, p1, w0 * scale0, d0 * scale0, color, bone, top=(w1 / (w0 * scale0), d1 / (d0 * scale0)), **kw)


def surf_hit(B, blks, origin, direction):
    """exact hit point + normal on the bevelled meshes of blks (CelestialDragon / Thunder Rex)"""
    import blockkit as bk
    from mathutils.bvhtree import BVHTree
    B._resolve()
    best = None
    d = Vector(direction).normalized()
    for blk in blks:
        bm = bk._box_bm(blk)
        t = BVHTree.FromBMesh(bm)
        bm.free()
        loc, nrm, _, dist = t.ray_cast(Vector(origin), d)
        if loc is not None and (best is None or dist < best[2]):
            best = (loc, nrm.normalized(), dist)
    if best is None:
        raise RuntimeError("surf_hit: no surface from %s" % (tuple(origin),))
    return best[0], best[1]


def strip(B, blks, origins, direction, width, thick, color, bone, proud=0.008, tip0=False, tip1=False, **kw):
    """flush bars along a surface through ray hits (Ivonrath surf_strip)"""
    hits = [surf_hit(B, blks, o, direction) for o in origins]
    kw.setdefault("studs", [])
    kw.setdefault("bevel", 0.004)
    kw.setdefault("nostud", True)
    for i in range(len(hits) - 1):
        (a, na), (b, nb) = hits[i], hits[i + 1]
        n = (na + nb).normalized()
        a2, b2 = a + n * (proud - thick), b + n * (proud - thick)
        if tip0 and i == 0:
            B.bar(b2, a2, n, width, thick, color, bone, top=(1, 0.25), **kw)
        elif tip1 and i == len(hits) - 2:
            B.bar(a2, b2, n, width, thick, color, bone, top=(1, 0.25), **kw)
        else:
            B.bar(a2, b2, n, width, thick, color, bone, **kw)


def fierce_eye(B, c, s, bone="Head", yaw=60.0, tilt=18.0, sc=1.5, brow_up=0.044, brow_out=0.020):
    """Thunder Rex / Ivonrath eye in coral: black socket (inner corner down) -> coral slit -> hot highlight, black
    pupil, heavy armour brow"""
    from mathutils import Euler
    R = Euler((0, math.radians(-s * tilt), math.radians(s * yaw)), "XYZ").to_matrix()
    n = R @ Vector((0, -1, 0))
    c = Vector(c)
    B.add(c, (0.052 * sc, 0.008, 0.025 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + n * 0.006, (0.044 * sc, 0.006, 0.0135 * sc), CORAL, bone, R=R, studs=[], role="detail", bevel=0.003)
    B.add(c + n * 0.011 + R @ Vector((s * 0.022 * sc, 0, 0.002)), (0.014 * sc, 0.004, 0.006 * sc), CORAL_HOT, bone,
          R=R, studs=[], role="detail", bevel=0.002)
    B.add(c + n * 0.011 + R @ Vector((-s * 0.004, 0, 0)), (0.006 * sc, 0.004, 0.0135 * sc), BLACK, bone, R=R,
          studs=[], role="detail", bevel=0.002)
    Rb = Euler((0, math.radians(-s * 22), math.radians(s * yaw)), "XYZ").to_matrix()
    B.add(c + Vector((0, 0, brow_up * sc)) + n * brow_out, (0.074 * sc, 0.034, 0.028 * sc), ARMOR, bone, R=Rb,
          role="detail", bevel=0.012)


def edge3(B, pts, bone, hw0, hw1, hd, side, out=Vector()):
    """3-step coral blade edge along a polyline, buried flush in the fin: CORAL_D (root 20 %) -> CORAL -> CORAL_HOT
    (tip); width across the fin tapers hw0 -> hw1 (<= 0.9 x the local fin half-thickness)"""
    P = [Vector(p) + out for p in pts]
    L = [(a - b).length for a, b in zip(P[1:], P[:-1])]
    tot = sum(L)

    def at(u):
        d = u * tot
        for a, b, l in zip(P[:-1], P[1:], L):
            if d <= l:
                return a.lerp(b, d / l)
            d -= l
        return P[-1]
    steps = ((0.0, 0.20, CORAL_D), (0.18, 0.80, CORAL), (0.78, 1.0, CORAL_HOT))
    for si, (u0, u1, c) in enumerate(steps):
        n = 2
        for i in range(n):
            ua, ub = u0 + (u1 - u0) * i / n, u0 + (u1 - u0) * (i + 1) / n
            a, b = at(ua), at(ub)
            if (b - a).length < 1e-4:
                continue
            wa, wb = hw0 + (hw1 - hw0) * ua, hw0 + (hw1 - hw0) * ub
            last = si == 2 and i == n - 1
            B.seg(a, b, wa, hd, c, bone, side=side, ext=0.01, studs=[], nostud=True, role="limb", rnd=0.12,
                  top=(0.25, 0.4) if last else (wb / wa, 1))


def fin(B, R0, R1, T, bone, thick=0.045, fair_bone=None, fair_col=ARMOR, inner=True):
    """falcate fin from a root chord R0 (leading) - R1 (trailing) to tip T: studded root fairing, 2 stacked tapered
    blocks (thickness steps down), FIN_IN inner panel, 3-step coral leading edge"""
    R0, R1, T = Vector(R0), Vector(R1), Vector(T)
    c = R1 - R0
    Rm = (R0 + R1) / 2
    n = c.cross(T - Rm).normalized()
    B.seg(R0 - c * 0.08, R1 + c * 0.08, 0.05, 0.055, fair_col, fair_bone or bone, side=n, rnd=0.45)   # fairing
    M = Rm + (T - Rm) * 0.55
    B.seg(Rm, M, c.length / 2, thick, STEEL, bone, side=c, ext=0.02, top=(0.62, 0.72), rnd=0.35)
    B.seg(Rm + (T - Rm) * 0.5, T, c.length / 2 * 0.64, thick * 0.74, STEEL, bone, side=c, top=(0.14, 0.55),
          rnd=0.35)
    if inner:
        for sg in (1, -1):
            o = n * sg * (thick + 0.003)
            B.poly([Rm.lerp(M, 0.5) + c * 0.12 + o, R1 + o, R1.lerp(M + c * 0.31, 0.55) + o, M + c * 0.2 + o,
                    Rm + c * 0.1 + o], 0.006, FIN_IN, bone)
    E1 = M - c * 0.31
    side = (E1 - R0).cross(n)
    edge3(B, [R0 + c * 0.03, E1, T], bone, 0.020, 0.010, 0.022, n)
    return n


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=307, tier=3, plates=False)
    z = Z0
    # ================= HULL: one lofted fusiform hull, telescoping at every bone joint (rear end buried 0.08)
    body = [loft(B, -0.80, -0.48, STEEL, "Chest", ext1=0.06),            # front ends at the jaw hinge
            loft(B, -0.48, -0.15, STEEL, "Chest", ext1=0.03),
            loft(B, -0.20, 0.30, STEEL, "Spine", ext1=0.04, scale0=0.97),     # clear of the fin roots
            loft(B, 0.22, 0.62, STEEL, "Tail1", ext1=0.03, scale0=0.97),
            loft(B, 0.54, 0.90, STEEL, "Tail2", ext1=0.02, scale0=0.97),
            loft(B, 0.84, 1.04, STEEL, "Tail3", scale0=0.97)]
    # crisp white belly shells (lower ~third, 0.008 proud), split per bone
    belly = []
    for y0, y1, bone, e in ((-0.80, -0.48, "Chest", 0.05), (-0.48, -0.16, "Chest", 0.02), (-0.18, 0.30, "Spine", 0.03),
                            (0.24, 0.62, "Tail1", 0.03), (0.56, 0.86, "Tail2", 0.0)):
        belly.append(loft(B, y0, y1, BELLY, bone, grow=0.008, zlo=-1.0, zhi=-0.32, ext1=e, studs=None))
    # ================= WAR-BACK: 6 shingled gunmetal lames (45 % of the depth), coral seams, jagged lower edges, keel
    lames = [(-0.80, -0.58, "Chest"), (-0.535, -0.345, "Chest"), (-0.305, -0.135, "Chest"),
             (-0.10, 0.05, "Spine"), (0.08, 0.21, "Spine"), (0.235, 0.345, "Spine")]   # graduated 0.22 -> 0.11
    lame_blks = []
    for i, (y0, y1, bone) in enumerate(lames):
        lb = loft(B, y0, y1, ARMOR, bone, grow=0.018, zlo=0.06, zhi=1.0, rnd=0.28)
        lame_blks.append(lb)
        for s in ((1, -1) if i >= 2 else ()):                    # lames 1-2: the gill slashes are the jagged edge
            for t, L in ((0.2, 0.07), (0.5, 0.05), (0.8, 0.06)):
                y = y0 + (y1 - y0) * t
                hw, zc, hd = hull(y)
                p0 = Vector((s * (hw + 0.014), y, zc + 0.06 * hd + 0.03))
                p1 = p0 + Vector((s * 0.004, 0.015, -L - 0.03))
                B.add((p0 + p1) / 2, (0.013, 0.045 * (1 - 0.25 * (i > 3)), (p1 - p0).length / 2), ARMOR, bone,
                      R=bk.frame_from(p0, p1, (s, 0, 0)), top=(1, 0.10), role="detail", bevel=0.006)
        strip(B, [lb], [(0, y0 + 0.03, 3.0), (0, (y0 + y1) / 2, 3.0), (0, y1 - 0.03, 3.0)], (0, 0, -1), 0.05, 0.035,
              ARMOR, bone, proud=0.027, nostud=False)                                              # keel (seated)
    seams = []
    for i, ((ya, _, ba), (yb, _, bb)) in enumerate(zip(lames, lames[1:])):
        g0, g1 = lames[i][1] - 0.012, yb + 0.012
        bone = bone_at((g0 + g1) / 2)
        col = CORAL_D if i == 4 else CORAL                         # coral heat fades toward the tail
        seams.append(loft(B, g0, g1, col, bone, grow=0.016, zlo=0.08, zhi=1.0, rnd=0.24, studs=[],
                          nostud=True))                                                    # seam band
        if i < 2:                                                                                    # shoulder seams
            ym = (g0 + g1) / 2
            loft(B, ym - 0.006, ym + 0.006, CORAL_HOT, bone, grow=0.0185, zlo=0.10, zhi=1.0, rnd=0.24, studs=[],
                 nostud=True)
    # tail top saddles on Tail1-2 (no full rings: they read as hose clamps)
    for y, ln, bone in ((0.50, 0.10, "Tail1"), (0.72, 0.08, "Tail2")):
        loft(B, y - ln / 2, y + ln / 2, ARMOR, bone, grow=0.014, zlo=0.10, zhi=1.0, rnd=0.28)
    # ================= gills: 5 curved coral slashes per side (dark slit + coral flap), crossing the belly line
    gl = body[:2] + belly[:2]
    for s in (1, -1):
        for i, (y, h) in enumerate(zip((-0.70, -0.64, -0.58, -0.52, -0.46), (0.20, 0.21, 0.20, 0.18, 0.15))):
            hw, zc, hd = hull(y)
            zt, zb = zc + 0.01, max(zc + 0.01 - h, zc - hd + 0.035)
            for dy, col, w in ((0.0, MOUTH, 0.02), (0.022, CORAL, 0.028)):
                o = [(s * 1.0, y + dy, zt), (s * 1.0, y + dy + 0.014, (zt + zb) / 2), (s * 1.0, y + dy + 0.004, zb)]
                strip(B, gl, o, (-s, 0, 0), w, 0.010, col, "Chest", proud=0.006, tip0=True, tip1=True)
    # ================= battle scars: 3 tapered claw gouges across lames 2-3, LEFT side only (asymmetric)
    for j, (y0s, ln) in enumerate(((-0.52, 1.0), (-0.48, 1.0), (-0.44, 0.7))):
        pts = []
        for t in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
            t2 = t * ln
            y = y0s + 0.10 * t2
            hw, zc, hd = hull(y)
            pts.append((1.0, y, zc + hd * (0.88 - 0.60 * t2)))
        strip(B, lame_blks[1:2], pts, (-1, 0, 0), 0.022, 0.008, SCAR, "Chest", proud=0.004, tip0=True, tip1=True)
    # ================= WAR-HAMMER HEAD (Head bone): head core buried in the chest, cephalofoil, helm, eye lobes
    core = B.seg((0, -0.70, z + 0.05), (0, -1.00, z + 0.06), 0.20, 0.11, STEEL, "Head", top=(0.80, 0.85), rnd=0.35)
    hc = B.add((0, -1.025, z + 0.075), (0.17, 0.115, 0.06), STEEL, "Head", top=(0.9, 0.88), rnd=0.18)   # centre
    wings, lobes = [], {}
    for s in (1, -1):
        wings.append(B.seg((s * 0.12, -1.03, z + 0.075), (s * 0.44, -0.955, z + 0.075), 0.10, 0.06, STEEL, "Head",
                           side=(0, 1, 0), top=(0.75, 0.75), rnd=0.18))                          # swept wing 14 deg
        lobes[s] = B.add((s * 0.47, -0.97, z + 0.075), (0.07, 0.11, 0.075), ARMOR, "Head", rnd=0.40)  # eye lobe
    for s in (1, -1):                                                                             # notched lead edge
        B.seg((0, -1.128, z + 0.075), (s * 0.07, -1.162, z + 0.075), 0.03, 0.045, STEEL, "Head", side=(0, 1, 0),
              rnd=0.20, studs=[])
        B.seg((s * 0.07, -1.162, z + 0.075), (s * 0.42, -1.078, z + 0.075), 0.03, 0.045, STEEL, "Head",
              side=(0, 1, 0), rnd=0.20, top=(1, 0.8), studs=[])
        B.add((s * 0.355, -1.10, z + 0.085), (0.032, 0.006, 0.007), BLACK, "Head", rot=(0, 0, -s * 14), studs=[],
              role="detail", bevel=0.003)                                                       # nostril slit
    # flat white underside (level at z+0.015: the whole front edge strikes the ground together)
    B.add((0, -1.025, z + 0.017), (0.15, 0.10, 0.006), BELLY, "Head", studs=[])
    for s in (1, -1):
        B.seg((s * 0.13, -1.03, z + 0.017), (s * 0.43, -0.955, z + 0.022), 0.08, 0.006, BELLY, "Head",
              side=(0, 1, 0), studs=[])
    # armour helm: studded dark cap inset 0.025, coral rim front + rear, keel ridge into lame 1
    helm = B.add((0, -1.025, z + 0.149), (0.145, 0.09, 0.016), ARMOR, "Head", top=(0.95, 0.95))
    for s in (1, -1):
        B.seg((s * 0.13, -1.03, z + 0.147), (s * 0.41, -0.96, z + 0.133), 0.072, 0.016, ARMOR, "Head",
              side=(0, 1, 0), top=(0.76, 1))
        for (a, b) in (((0, -1.108, z + 0.166), (s * 0.13, -1.108, z + 0.166)),
                       ((s * 0.13, -1.098, z + 0.164), (s * 0.41, -1.018, z + 0.150)),
                       ((0, -0.942, z + 0.166), (s * 0.13, -0.942, z + 0.166)),
                       ((s * 0.13, -0.962, z + 0.164), (s * 0.41, -0.905, z + 0.150))):
            B.bar(a, b, Vector((0, 0, 1)), 0.022, 0.008, CORAL, "Head", studs=[], nostud=True, bevel=0.003)
    strip(B, [helm, core, lame_blks[0]], [(0, -1.10, 3.0), (0, -0.98, 3.0), (0, -0.86, 3.0), (0, -0.76, 3.0)],
          (0, 0, -1), 0.05, 0.035, ARMOR, "Head", proud=0.027, nostud=False)                    # keel ridge (seated)
    # coral fierce eyes on the outer-front faces of the lobes + two-tone back-swept brow spikes
    for s in (1, -1):
        n = Vector((s * 0.866, -0.5, 0.0))
        c0 = Vector((s * 0.47, -0.97, z + 0.085))
        p, nn = surf_hit(B, [lobes[s]], c0 + n * 0.4, -n)
        fierce_eye(B, p + nn * 0.004, s, yaw=60, tilt=18, sc=1.6, brow_up=0.030, brow_out=-0.012)   # brow seated
        b0 = Vector((s * 0.47, -0.99, z + 0.13))
        d = Vector((s * 0.45, 0.80, 0.40)).normalized()
        B.add(b0 + d * 0.065, (0.022, 0.05, 0.065), ARMOR, "Head", R=bk.frame_from(b0, b0 + d, (1, 0, 0)),
              top=(0.62, 0.5), studs=[], role="limb")
        b1 = b0 + d * 0.11
        B.add(b1 + d * 0.05, (0.016, 0.028, 0.05), CORAL, "Head",
              R=bk.frame_from(b1, b1 + d, (1, 0, 0)), top=(0.30, 0.10), studs=[], nostud=True, role="limb")
    # ================= crescent jaw (set back, MODELLED 10 deg open): white jaws, teeth outside the lip, dark mouth
    B.seg((0, -0.78, z - 0.05), (0, -0.985, z - 0.04), 0.175, 0.024, BELLY, "Head", top=(0.62, 1), rnd=0.35)  # upper
    B.seg((0, -0.80, z - 0.068), (0, -0.96, z - 0.062), 0.14, 0.006, MOUTH, "Head", top=(0.62, 1), studs=[],
          role="detail", bevel=0.003)                                                           # mouth roof
    up = [(0.03, -0.985, 0.055), (0.075, -0.98, 0.052), (0.11, -0.955, 0.048), (0.13, -0.92, 0.045),
          (0.148, -0.885, 0.042), (0.162, -0.85, 0.038), (0.172, -0.815, 0.035)]
    for s in (1, -1):
        for x, y, L in up:
            dx = 0.016 if up.index((x, y, L)) < 3 else 0.006
            B.spike((s * (x + dx), y, z - 0.062), (s * 0.14, -0.05, -1), L, 0.018 if L > 0.045 else 0.016,
                    TEETH, "Head")
    jb = B.seg(jawpt((0, -0.78, z - 0.09)), jawpt((0, -0.965, z - 0.09)), 0.16, 0.025, BELLY, "Jaw", top=(0.62, 1),
               rnd=0.35)                                                                         # lower jaw
    B.seg(jawpt((0, -0.80, z - 0.117)), jawpt((0, -0.94, z - 0.117)), 0.10, 0.008, ARMOR, "Jaw", top=(0.7, 1))
    B.seg(jawpt((0, -0.80, z - 0.064)), jawpt((0, -0.95, z - 0.064)), 0.13, 0.006, MOUTH, "Jaw", top=(0.62, 1),
          studs=[], role="detail", bevel=0.003)                                                 # mouth floor
    lo = [(0.035, -0.955, 0.045), (0.07, -0.945, 0.042), (0.10, -0.92, 0.04), (0.12, -0.89, 0.02),
          (0.135, -0.855, 0.035), (0.145, -0.82, 0.03)]
    for s in (1, -1):
        for x, y, L in lo:
            B.spike(jawpt((s * x, y, z - 0.068)), (s * 0.08, -0.05, 1), L, 0.012, TEETH, "Jaw")
    # ================= fins: pectorals (falcate, swept + drooped), dorsal (stacked sickle), caudal crescent
    for s, side in ((1, "L"), (-1, "R")):
        fin(B, (s * 0.20, -0.46, z - 0.15), (s * 0.20, -0.275, z - 0.16), (s * 0.46, -0.10, z - 0.32), "Fin_" + side,
            thick=0.045, fair_bone="Chest", fair_col=ARMOR)
    # dorsal: armour fairing, 3 stacked blocks stepping back, falcate free rear tip with a bite notch
    B.seg((0, -0.19, z + 0.235), (0, 0.17, z + 0.215), 0.065, 0.045, STEEL, "Spine", rnd=0.45)        # dorsal root
    for p0, p1, hw, hd, tp in (((0, -0.01, z + 0.20), (0, 0.05, z + 0.46), 0.15, 0.045, (0.62, 0.71)),
                               ((0, 0.06, z + 0.44), (0, 0.12, z + 0.66), 0.095, 0.032, (0.55, 0.70)),
                               ((0, 0.115, z + 0.64), (0, 0.155, z + 0.82), 0.055, 0.022, (0.15, 0.60))):
        B.seg(p0, p1, hw, hd, STEEL, "Spine", side=(0, 1, 0), top=tp, rnd=0.30, ext=0.02)
    B.poly([Vector((0, 0.09, z + 0.33)), Vector((0, 0.12, z + 0.21)), Vector((0, 0.25, z + 0.285)),
            Vector((0, 0.19, z + 0.335)), Vector((0, 0.205, z + 0.375)), Vector((0, 0.15, z + 0.44)),
            Vector((0, 0.08, z + 0.44))], 0.03, STEEL, "Spine")                                      # free rear tip
    edge3(B, [(0, -0.17, z + 0.23), (0, -0.04, z + 0.48), (0, 0.068, z + 0.672), (0, 0.152, z + 0.815)], "Spine",
          0.022, 0.010, 0.02, (1, 0, 0))
    ANCHORS["DorsalTip"] = (0, 0.155, z + 0.82)
    # small fins: 2nd dorsal + anal (Tail1), pelvics (Tail1), coral_d tips
    for p0, p1, bone in (((0, 0.47, z + 0.12), (0, 0.56, z + 0.28), "Tail1"), ((0, 0.49, z - 0.10), (0, 0.58, z - 0.22),
                                                                            "Tail1")):
        B.seg(p0, p1, 0.05, 0.018, STEEL, bone, side=(0, 1, 0), top=(0.25, 0.6), ext=0.03, rnd=0.3)
        q = Vector(p0).lerp(Vector(p1), 0.72)
        B.spike(q, Vector(p1) - Vector(p0), 0.06, 0.016, CORAL_D, bone, studs=[], nostud=True)
    for s in (1, -1):
        B.seg((s * 0.08, 0.34, z - 0.12), (s * 0.19, 0.46, z - 0.23), 0.045, 0.016, STEEL, "Tail1", side=(0, 1, 0),
              top=(0.3, 0.6), ext=0.03, rnd=0.3)
        B.spike((s * 0.165, 0.435, z - 0.21), (s * 0.5, 0.55, -0.5), 0.05, 0.014, CORAL_D, "Tail1", studs=[],
                nostud=True)
        B.seg((s * 0.06, 0.86, z + 0.03), (s * 0.06, 1.00, z + 0.035), 0.03, 0.012, ARMOR, "Tail3",
              side=(1, 0, 0), top=(0.6, 1), rnd=0.4)                                            # peduncle keel
    # caudal (Tail4): studded root, upper lobe 3 blocks curving up-back, lower lobe 2 blocks, coral leading edges
    lobes_axis = []
    B.seg((0, 0.97, z + 0.03), (0, 1.10, z + 0.04), 0.05, 0.065, STEEL, "Tail4", rnd=0.4)
    for path, dims, tip_t in (([(1.04, 0.05), (1.14, 0.22), (1.26, 0.42), (1.38, 0.60)],
                               ((0.10, 0.040, (0.82, 0.85)), (0.082, 0.034, (0.72, 0.8)), (0.06, 0.027, (0.12, 0.6))),
                               None),
                              ([(1.06, 0.0), (1.13, -0.12), (1.20, -0.22)],
                               ((0.085, 0.035, (0.66, 0.8)), (0.056, 0.026, (0.12, 0.6))), None)):
        P = [Vector((0, y, z + dz)) for y, dz in path]
        lead = []
        for (a, b), (hw, hd, tp) in zip(zip(P, P[1:]), dims):
            d = (b - a).normalized()
            sd = Vector((0, -d.z, d.y)) if d.z > 0 else Vector((0, d.z, -d.y))   # leading side: forward-up / -down
            B.seg(a, b, hw, hd, STEEL, "Tail4", side=sd, top=tp, ext=0.02, rnd=0.3)
            lead.append(a + sd * hw)
        lead.append(P[-1])
        edge3(B, lead, "Tail4", 0.018, 0.009, 0.022, (1, 0, 0))
        lobes_axis.append((P, dims))
    # FIX 6 - upper caudal lobe trailing fill with one V bite notch (2nd notch in the silhouette)
    P, dims = lobes_axis[0]
    seglen = [(b - a).length for a, b in zip(P, P[1:])]
    tot = sum(seglen)
    hws = [d[0] for d in dims] + [dims[-1][0] * dims[-1][2][0]]

    def lobe_at(t):
        d = t * tot
        for i, l in enumerate(seglen):
            if d <= l or i == len(seglen) - 1:
                u = min(1.0, d / l)
                a, b = P[i], P[i + 1]
                dd = (b - a).normalized()
                tr = Vector((0, dd.z, -dd.y))                 # back-down (trailing) side
                return a.lerp(b, u), tr, hws[i] + (hws[i + 1] - hws[i]) * u
            d -= l
    C = lobe_at(0.5)[0]
    out_ = []
    for t, k_ in ((0.12, -0.5), (0.25, 0.03), (0.45, 0.05), (0.56, 0.05), (0.60, 0.005), (0.66, 0.045), (0.82, 0.03),
                  (0.95, -0.7)):
        a, tr, w = lobe_at(t)
        out_.append(a + tr * (w * (1 + k_) if k_ < 0 else w + k_))
    out_.append(lobe_at(0.80)[0])
    B.poly([C] + out_ + [out_[0]], 0.03, STEEL, "Tail4")
    ANCHORS["Wake"] = (0, 1.34, z + 0.45)
    ANCHORS["Slam"] = (0, -1.15, z + 0.03)
    ANCHORS["Mouth"] = (0, -0.99, z - 0.075)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


# ------------------------------------------------------------------ rig
def rig(k):
    z = Z0
    k.joint("Spine", (0, 0.05, z + 0.02), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.20, z + 0.03), "Spine", tail=(0, -0.4, 0))
    k.joint("Head", (0, -0.74, z - 0.05), "Chest", tail=(0, -0.3, 0))          # throat pivot inside the body
    k.joint("Jaw", tuple(JAW_P), "Head", tail=(0, -0.2, 0))
    k.joint("Mouth", ANCHORS.get("Mouth", (0, -0.99, z - 0.075)), "Head", tail=(0, -0.15, 0))
    k.joint("Slam", ANCHORS.get("Slam", (0, -1.15, z + 0.03)), "Head", tail=(0, 0, -0.15))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Fin_" + side, (s * 0.20, -0.35, z - 0.15), "Chest", tail=(s * 0.3, 0.15, -0.1))
    k.joint("Tail1", (0, 0.30, z + 0.01), "Spine", tail=(0, 0.3, 0))
    k.joint("Tail2", (0, 0.62, z + 0.01), "Tail1", tail=(0, 0.28, 0.01))
    k.joint("Tail3", (0, 0.90, z + 0.025), "Tail2", tail=(0, 0.1, 0.005))
    k.joint("Tail4", (0, 1.00, z + 0.03), "Tail3", tail=(0, 0.3, 0.2))
    k.joint("Wake", ANCHORS.get("Wake", (0, 1.30, z + 0.45)), "Tail4", tail=(0, 0.15, 0))
    k.joint("DorsalTip", ANCHORS.get("DorsalTip", (0, 0.155, z + 0.82)), "Spine", tail=(0, 0, 0.12))


def check_pairs():
    P = [("Head", "Fin_L"), ("Head", "Fin_R"), ("Jaw", "Fin_L"), ("Jaw", "Fin_R"), ("Tail3", "Spine"),
         ("Tail3", "Chest"), ("Tail2", "Chest"), ("Fin_L", "Spine"), ("Fin_R", "Spine"), ("Jaw", "Chest"),
         ("Tail4", "Spine"), ("Tail4", "Chest"), ("Tail4", "Tail2")]
    for f in ("Fin_L", "Fin_R"):
        P += [(f, "Tail1"), (f, "Tail2"), ("Tail4", f)]
    return P


def joints():
    # jaw hinge line: the lower jaw's root turns against the chest hull's front cap (the throat wall, hidden under the
    # head core and the upper jaw)
    return [((-0.17, -0.80, Z0 - 0.08), (0.17, -0.80, Z0 - 0.08), 0.09, "Head")]


# ------------------------------------------------------------------ animation
# Reference (owner rule 2026-10-10, notes in _review/ANIM_REFERENCES_1014.md): animationreference.org
# "The Old Man and the Sea" (A. Petrov, Sakugabooru #17124, 30.5-37 s): the sharks circle on long nearly straight
# glides, one tail beat ~0.9 s; on the strike (33.6 -> 34.2 s, ~18 f) the head yaws INTO the target while the tail swings
# the other way (C-curve), head travel ~1/5 of the tail tip, pectorals spread and rigid. "Children of the Sea" #111777:
# hovering fish only flick the tail third. "Sea Beasts" 0-3 s: heavy-head roar = drop/tuck, lift, the jaw opens ~0.4 s
# after the lift starts. Jaw keys are measured from the MODELLED 10 deg gape: closed = -10, never below (review 2).
import petkit as pk
import _common as cm

TAIL = ["Tail1", "Tail2", "Tail3", "Tail4"]
SWIM_AMP = (2.0, 6.0, 9.0, 10.0, 9.0)            # relative yaw: Spine, Tail1..Tail4 (review 1 wave limits)
JAW_SHUT = -10.0


def fins(k, f, down, trim=0.0):
    """down + = both pectoral tips drop (roll), - = tips rise; trim + = left tip lower / right tip higher"""
    k.key("Fin_L", f, rot=(0, 0, down + trim))
    k.key("Fin_R", f, rot=(0, 0, -(down - trim)))


def body_wave(k, f, n, scale=1.0, cycles=1, lag=0.12, head_world=-1.0):
    """carangiform wave: Spine + Tail1-4 yaw with a 0.12-cycle lag per bone; Chest counter-yaws, the Head nets a
    small opposite recoil (head_world x the spine phase), so the hammer never sweeps (head shakes are banned)"""
    s = pk.wave(f, n, 0.0, cycles)
    sp, ch = SWIM_AMP[0] * scale * s, -1.5 * scale * s
    return sp, ch, head_world * scale * s - sp - ch


def tail_wave(k, f, n, scale=1.0, cycles=1, lag=0.12, pitch=(0, 0, 0, 0), roll4=0.0):
    for i, b in enumerate(TAIL):
        ph = -lag * (i + 1)
        r = roll4 * pk.cwave(f, n, ph, cycles) if b == "Tail4" else 0.0
        k.key(b, f, rot=(pitch[i], SWIM_AMP[i + 1] * scale * pk.wave(f, n, ph, cycles), r))


def smooth(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def idle(k):
    """PATROL HOVER: hangs nose-down hunting, bobbing slowly while a lazy S-wave (40 % of the swim) rolls down the
    tail; the pectorals trim and swap to balance; two jaw breaths and one teeth flash; ONE slow banked glance."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        g = smooth((f - 70) / 12.0) * (1 - smooth((f - 96) / 14.0))           # glance f70-82 in, f96-110 out
        sp, ch, hd = body_wave(k, f, n, 0.4, 2, head_world=-0.4)
        k.key("Spine", f, rot=(3 + 1.5 * pk.wave(f, n, 0.15), sp, 8 * g), loc=(0, 0, 0.03 + 0.025 * pk.wave(f, n)))
        k.key("Chest", f, rot=(0, ch + 4 * g, 0))
        k.key("Head", f, rot=(0, hd + 6 * g, 0))
        tail_wave(k, f, n, 0.4, 2)
        fins(k, f, 1 + 2 * pk.wave(f, n, 0.1, 4), 5 * pk.cwave(f, n))
    for f, j in ((0, 0), (4, 0), (14, 6), (28, 0), (40, 0), (46, 8), (52, 0), (64, 0), (76, 6), (90, 0), (120, 0)):
        k.key("Jaw", f, rot=(j, 0, 0))
    k.finish()


def swim(k):
    """CARANGIFORM S-WAVE: the rear third drives a travelling yaw wave (tail tip ~+-0.25), the front two thirds stay
    nearly rigid, one thrust pulse per tail stroke, the caudal twists on each reversal; pectorals planing ~10 deg
    down with tiny trims (they never flap), dorsal stiff, nose 3 deg down."""
    n = 32
    k.new_action("swim", n, True)
    for f in range(0, n + 1, 2):
        sp, ch, hd = body_wave(k, f, n, 1.0, 1, head_world=-1.0)
        k.key("Spine", f, rot=(3, sp, 0), loc=(0, 0.012 * pk.wave(f, n, 0.0, 2), 0.01 * pk.wave(f, n, 0.25, 2)))
        k.key("Chest", f, rot=(0, ch, 0))
        k.key("Head", f, rot=(-0.5 * pk.wave(f, n, 0.1, 2), hd, 0))
        tail_wave(k, f, n, 1.0, 1, roll4=5.0)
        fins(k, f, 10 + 2 * pk.wave(f, n, 0.3), 1.5 * pk.wave(f, n, 0.05))
        k.key("Jaw", f, rot=(1.5 * pk.wave(f, n, 0.2, 2), 0, 0))
    k.finish()
    return 0.0


def roar(k):
    """THREAT DISPLAY (grey-reef agonistic display, stays low): gathers, then hunches the back into a hump with the
    snout up, the pectorals DROP and the tail droops; the jaw gapes late (Sea Beasts: the jaw lags the head lift),
    buzzes while the tail tip shivers; snaps shut hard; settles with a small pectoral overshoot. No roll, no sweep."""
    n = 66
    k.new_action("roar", n, False)
    K = [  # f, spine z, spine pitch, chest, head, jaw, tail1, tail2, fins (down +)
        (0, 0.0, 0, 0, 0, 0, 0, 0, 0),
        (10, -0.05, 4, 0, 4, -4, 2, 2, -10),
        (14, -0.04, 5, -3, -2, -6, -2, -2, 8),
        (20, -0.02, 6, -6, -10, 28, -6, -6, 30),
        (46, -0.02, 6, -6, -10, 28, -6, -6, 30),
        (50, -0.02, 5, -5, -7, JAW_SHUT, -5, -5, 26),
        (58, -0.01, 1, -1, -1, 2, -1, -1, -4),
        (66, 0.0, 0, 0, 0, 0, 0, 0, 0)]
    for f, z, p, ch, hd, jw, t1, t2, fd in K:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Tail1", f, rot=(t1, 0, 0))
        k.key("Tail2", f, rot=(t2, 0, 0))
        k.key("Tail3", f, rot=(t2 * 0.5, 0, 0))
        k.key("Tail4", f, rot=(0, 0, 0))
        fins(k, f, fd)
    for f in range(23, 46, 3):                       # hold: jaw buzz + tail-tip shiver (~3 Hz), body still
        w = 1 if (f // 3) % 2 else -1
        k.key("Jaw", f, rot=(28 + 3 * w, 0, 0))
    for f in range(22, 46, 5):
        w = 1 if (f // 5) % 2 else -1
        k.key("Tail3", f, rot=(-3, 4 * w, 0))
        k.key("Tail4", f, rot=(0, 8 * w, 0))
    k.key("Tail3", 46, rot=(-3, 0, 0))
    k.key("Tail4", 46, rot=(0, 0, 0))
    k.finish(loop=False)
    k.events["roar"] = {"roar": round(18 / n, 3), "snap": round(50 / n, 3)}


def head_mins(k, f, groups=("Head", "Jaw")):
    """lowest world z of the vertices whose dominant group is in `groups` at frame f"""
    import bpy
    body = k.main
    key = tuple(groups)
    if not hasattr(k, "_grp_idx"):
        k._grp_idx = {}
    if key not in k._grp_idx:
        names = {g.index: g.name for g in body.vertex_groups}
        k._grp_idx[key] = [v.index for v in body.data.vertices if v.groups and
                           names[max(v.groups, key=lambda g: g.weight).group] in groups]
    bpy.context.scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    z = min((mw @ me.vertices[i].co).z for i in k._grp_idx[key])
    ev.to_mesh_clear()
    return z


def head_contact(k, frames, target=0.005, pin=None):
    """FLOOR SOLVE (the Kraken ground_lift pattern): key Spine loc on every frame so the hammer's lowest vertex sits
    at `target`; on `pin` frames also hold the Slam anchor's x/y where it was on the first pin frame, so the body
    pivots AROUND the contact point instead of sliding it (<= 0.01)."""
    import bpy
    pb = k.arm.pose.bones["Spine"]
    R0 = k.arm.data.bones["Spine"].matrix_local.to_quaternion()
    mw = k.arm.matrix_world
    k.bake_bezier_now()
    hold = None
    for f in frames:
        bpy.context.scene.frame_set(f)
        cur = R0 @ pb.location
        dz = target - head_mins(k, f)
        dx = dy = 0.0
        if pin and f in pin:
            s = mw @ k.arm.pose.bones["Slam"].head
            if hold is None:
                hold = (s.x, s.y)
            dx, dy = hold[0] - s.x, hold[1] - s.y
        k.key("Spine", f, loc=(cur.x + dx, cur.y + dy, cur.z + dz))


def hammerslam(k):
    """SIGNATURE - STINGRAY PIN (great-hammerhead hunt; ref: Petrov's strike = head into the target, tail the other
    way): slows and eyes the ground, rears up and hangs, PITCHES OVER and slams the hammer flat on the floor with the
    jaw shut (contact solved to 0.005), pins the prey and PIVOTS 20 deg around the pinned point with two press pulses
    driven by hard tail strokes, lifts and bites ONCE, releases and glides back to the hover. No head shake."""
    n = 104
    k.new_action("act_hammerslam", n, False)
    K = [  # f, spine z, spine pitch, spine yaw, chest, head, jaw, tail1, tail2, tail3, fins (down +)
        (0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (8, 0.0, 6, 0, 0, 4, 0, 1, 1, 1, -10),
        (14, 0.01, 8, 0, 0, 6, -4, 1, 1, 1, -15),
        (22, 0.09, -7, 0, -7, -9, JAW_SHUT, -3, -3, -4, -20),
        (24, 0.10, -8, 0, -8, -10, JAW_SHUT, -4, -4, -4, -20),
        (28, 0.10, -8, 0, -8, -10, JAW_SHUT, -4, -4, -4, -18),
        (33, 0.025, 22, 0, 10, 10, JAW_SHUT, -4, -5, -6, -12),
        (35, 0.025, 22, 0, 12, 10, JAW_SHUT, -4, -5, -6, 10),
        (38, 0.025, 22, 0, 10, 10, JAW_SHUT, -4, -5, -6, 4),
        (54, 0.025, 22, 20, 10, 10, JAW_SHUT, -4, -5, -6, 4),
        (70, 0.025, 22, 20, 10, 10, JAW_SHUT, -4, -5, -6, 4),
        (74, 0.025, 22, 20, 4, 10, 24, -4, -5, -6, 0),
        (78, 0.025, 22, 20, 4, 10, JAW_SHUT, -4, -5, -6, 0),
        (80, 0.025, 20, 20, 4, 9, -6, -4, -5, -6, -4),
        (92, 0.06, 6, 6, 0, 2, 0, -1, -1, -1, -12),
        (104, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]
    for f, z, p, yw, ch, hd, jw, t1, t2, t3, fd in K:
        k.key("Spine", f, rot=(p, yw, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        for b, t in zip(TAIL, (t1, t2, t3, 0)):
            k.key(b, f, rot=(t, 0, 0))
        fins(k, f, fd)
    for f, y in ((2, 3), (6, -3), (10, 1.5)):          # the swim sway decays as it slows
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(1 if f >= 8 else 0, y * (1 + 0.5 * i), 0))
    for f, y in ((30, -10), (33, 8), (36, -4)):        # Tail4 flick on the strike, then the impact shiver
        k.key("Tail4", f, rot=(0, y, 0))
    for c in (46, 58):                                 # press pulses: chest presses + one hard tail stroke
        k.key("Chest", c - 4, rot=(10, 0, 0))
        k.key("Chest", c, rot=(12, 0, 0))
        k.key("Chest", c + 6, rot=(10, 0, 0))
        for i, b in enumerate(TAIL[1:]):
            tp = (-5, -6, 0)[i]
            k.key(b, c - 3, rot=(tp, -10 - 2 * i, 0))
            k.key(b, c + 2, rot=(tp, 12 + 2 * i, 0))
            k.key(b, c + 7, rot=(tp, 0, 0))
    k.finish(loop=False)
    head_contact(k, range(33, 71), pin=set(range(33, 71)))
    pb = k.arm.pose.bones["Spine"]
    R0 = k.arm.data.bones["Spine"].matrix_local.to_quaternion()
    import bpy
    bpy.context.scene.frame_set(70)
    held = R0 @ pb.location
    for f in (74, 78, 80):                              # bite: the body holds where the pin left it
        k.key("Spine", f, loc=tuple(held))
    k.key("Spine", 92, loc=(held.x * 0.4, held.y * 0.4 + 0.10, 0.06))       # glides back and up to the hover
    k.finish(loop=False)
    k.events["act_hammerslam"] = {"spot": round(8 / n, 3), "slam": round(33 / n, 3), "pin": round(40 / n, 3),
                                  "bite": round(78 / n, 3)}


def anim(k):
    idle(k)
    stride = swim(k)
    roar(k)
    hammerslam(k)
    return stride


HEAD_XF = []
