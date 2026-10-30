# Abyssal Orca v2 (Tide egg SECRET 1.5%, 2026-10-14) - FIERCE style "THE DEEP SOVEREIGN" (review 1 brief): a bull
# orca from the abyss swimming through the air like our Kraken (MOTION Swim). A lofted torpedo hull (melon head,
# hump under the dorsal, tall narrow peduncle) in crisp black and white - flush studded orca pattern (eye-patch
# lens, white jaw + belly band, flank lobes, grey saddle), a tall stepped sickle-blade dorsal with jade veins and
# trailing serrations, broad paddle pectorals, crescent flukes. HERO: the CROWNED ANGLER LANTERN - a gold coronet on
# the brow, a gold-ringed rod arcing over the head (Lure -> Lure2 -> Esca) and a big faceted jade orb clasped in 5
# gold fangs. Jade lantern beads along the waterline and down the spine (DEEP -> GLOW -> HOT, no Neon).
# Old version: _tools/rex_versions/AbyssalOrca_v1.py
import math
from mathutils import Vector

DISPLAY = "Abyssal Orca"
MOTION = "Swim"
RIG = "fish"
HEIGHT = 10.0       # dorsal tip in studs at x1 - the secret stands over its egg (Turtle 9)

# Blender colours (Roblox renders ~0.6x darker) - review 1 palette
INK = (64, 70, 102)          # navy-black hull (lum ~71, the black-pet band)
INK_D = (36, 40, 64)         # brows, lip line, blowhole, serrations, rod
WHITE = (240, 244, 252)
SADDLE = (136, 146, 182)     # review 2: halfway between INK and WHITE
DEEP = (8, 118, 100)         # bead sockets, vein roots
GLOW = (30, 236, 160)        # abyss jade: orb, beads, veins, eyes
HOT = (214, 255, 226)        # bead centres, vein cores, orb glint, eye hot spot
GOLD = (255, 196, 50)        # ONLY the lantern: coronet, rod rings, collar, cage fangs
GOLD_D = (214, 150, 30)
TEETH = (240, 236, 222)
MOUTH = (70, 16, 40)
BLACK = (14, 14, 22)

Z0 = 0.62
H_MODEL = 1.80               # dorsal tip
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)

# lofted hull stations: y, half-width, half-height, centre z (relative to Z0)
STATIONS = [(-1.30, 0.10, 0.085, -0.07), (-1.06, 0.19, 0.20, -0.03), (-0.94, 0.235, 0.25, 0.01),   # melon
            (-0.82, 0.26, 0.28, 0.0), (-0.50, 0.30, 0.32, 0.01), (-0.14, 0.285, 0.31, 0.03),
            (0.20, 0.23, 0.265, 0.02), (0.50, 0.13, 0.19, 0.02), (0.80, 0.065, 0.10, 0.03),
            (0.94, 0.03, 0.045, 0.03)]                    # review 2: the hull ends in a point (V notch)
JAW_P = Vector((0, -0.94, Z0 - 0.12))
JAW_OPEN = 8.0               # lower jaw MODELLED 8 deg open (rest)
MOUTH_F = -0.40              # mouth line as a fraction of the half-height (upper jaw above, lower jaw below)
ROD = [Vector(p) for p in ((0, -0.94, 0.875), (0, -0.98, 1.10), (0, -1.10, 1.32), (0, -1.27, 1.42), (0, -1.36, 1.38))]
ORB = Vector((0, -1.38, 1.15))
ANCH = {}


def hull(y):
    """(half-width, centre z, half-height) at y, linear between stations (clamped)"""
    S = STATIONS
    if y <= S[0][0]:
        a, b = S[0], S[1]
    elif y >= S[-1][0]:
        a, b = S[-2], S[-1]
    else:
        a, b = next((S[i], S[i + 1]) for i in range(len(S) - 1) if S[i][0] <= y <= S[i + 1][0])
    t = (y - a[0]) / (b[0] - a[0])
    return (a[1] + (b[1] - a[1]) * t, Z0 + a[3] + (b[3] - a[3]) * t, a[2] + (b[2] - a[2]) * t)


def bone_at(y):
    return "Head" if y < -0.80 else "Chest" if y < -0.05 else "Spine" if y < 0.26 else "Tail1" if y < 0.50 else \
        "Tail2" if y < 0.79 else "Tail3"


def jawpt(p):
    a = math.radians(JAW_OPEN)
    q = Vector(p) - JAW_P
    return JAW_P + Vector((q.x, q.y * math.cos(a) - q.z * math.sin(a), q.y * math.sin(a) + q.z * math.cos(a)))


def loft(B, y0, y1, color, bone, grow=0.0, zlo=-1.0, zhi=1.0, ext1=0.0, scale0=1.0, end_w=1.0, xf=None, w0s=None,
         d0s=None, match=False, **kw):
    """hull section y0 -> y1: tapered rounded seg whose ends match the stations; zlo / zhi (fractions of the
    half-height) cut a horizontal band; grow pads it (shells); end_w narrows the far end (chevrons); xf maps points;
    w0s / d0s override scale0 per axis; match = the hull's corner radius (0.40 x min(hw, hh)) for flush shells"""
    pts = []
    for y in (y0, y1 + ext1):
        hw, zc, hh = hull(y)
        lo = zc + zlo * hh - (grow if zlo <= -1 else 0.0)
        hi = zc + zhi * hh + (grow if zhi >= 1 else 0.0)
        if match:
            # a shell with the hull's corner radius R curls under the hull ~(R - sqrt(2 R grow)) before its cut
            # edge: move the cut edge out by that much so the visible white / saddle boundary lands at zhi / zlo
            Rr = 0.40 * min(hw, hh) + grow
            pad = max(0.0, Rr - math.sqrt(max(0.0, 2 * Rr * grow - grow * grow)))
            hi += pad if zhi < 1 else 0.0
            lo -= pad if zlo > -1 else 0.0
        pts.append((Vector((0, y, (lo + hi) / 2)), hw + grow, (hi - lo) / 2))
    (p0, w0, d0), (p1, w1, d1) = pts
    if xf:
        p0, p1 = xf(p0), xf(p1)
    ws, ds = (w0s if w0s is not None else scale0), (d0s if d0s is not None else scale0)
    if match:
        hw, zc, hh = hull(y0)
        kw["rnd"] = min(0.95, (0.40 * min(hw, hh) + grow) / min(w0 * ws, d0 * ds))
    kw.setdefault("rnd", 0.40)
    return B.seg(p0, p1, w0 * ws, d0 * ds, color, bone, top=(w1 * end_w / (w0 * ws), d1 / (d0 * ds)), **kw)


def hseg(B, a, b, color, bone, zlo=-1.0, ext_far=0.0, ext_start=0.10):
    """review 2 FIX 3: one hull seg per station pair, from its BIG end `a` to `b` with the exact station dims. Joints:
    the rounded end faces recede ~0.4 x min(hw, hh), so instead of a short far-end extension every smaller seg runs
    `ext_start` BACK at its constant station size into its bigger neighbour (always inside it: the hull only shrinks
    away from the hump), covering the neighbour's receding end without any lip"""
    (ya, wa, ha, za), (yb, wb, hb, zb) = a, b
    t = 1.0 + ext_far / abs(yb - ya)
    yf, wf, hf, zf = (ya + (yb - ya) * t, wa + (wb - wa) * t, ha + (hb - ha) * t, za + (zb - za) * t)

    def band(w, h, zc):
        lo, hi = Z0 + zc + zlo * h, Z0 + zc + h
        return w, (lo + hi) / 2, (hi - lo) / 2
    w0, c0, d0 = band(wa, ha, za)
    w1, c1, d1 = band(wf, hf, zf)
    return B.seg((0, ya, c0), (0, yf, c1), w0, d0, color, bone, top=(w1 / w0, d1 / d0), rnd=0.40, ext=ext_start)


SE_N = 2.6                   # hull cross-section superellipse exponent (reads as a softly rounded box)
SEG = 24                     # points per full ring
OV = 0.06                    # joint overlap: each tube runs OV under its neighbour, tapering to 0.985


def zang(f):
    """ring angle where the section's height fraction is f (-1 bottom .. +1 top)"""
    return math.asin(max(-1.0, min(1.0, math.copysign(abs(f) ** (SE_N / 2.0), f))))


def ys_between(y0, y1, extra=()):
    return sorted(set([y0, y1] + [st[0] for st in STATIONS if y0 < st[0] < y1] + [e for e in extra if y0 < e < y1]))


def hull_tube(B, y0, y1, color, bone, zlo=-1.0, zhi=1.0, grow=0.0, j0=None, j1=None, nostud=False):
    """closed solid following hull() exactly (rings at every station). zlo > -1: the part ABOVE that height fraction,
    zhi < 1: the part BELOW it (flat chord = the mouth line). j0 / j1: joint y at the front / back end - the tube
    runs OV past it under the neighbour, shrinking to 0.985 there (the two meet flush at the joint)."""
    import blockkit as bk
    ys = ys_between(y0, y1, [v for v in (j0, j1) if v is not None])
    rings = []
    for y in ys:
        hw, zc, hh = hull(y)
        sc = 1.0
        if j0 is not None and y < j0:
            sc -= 0.015 * min(1.0, (j0 - y) / OV)
        if j1 is not None and y > j1:
            sc -= 0.015 * min(1.0, (y - j1) / OV)
        w, h = hw * sc + grow, hh * sc + grow
        if zlo > -1:
            a = zang(zlo)
            r = bk.superellipse(w, h, zc, y, SE_N, SEG // 2, a, math.pi - a)
        elif zhi < 1:
            a = zang(zhi)
            r = bk.superellipse(w, h, zc, y, SE_N, SEG // 2, math.pi - a, 2 * math.pi + a)
        else:
            r = bk.superellipse(w, h, zc, y, SE_N, SEG)
        rings.append(r)
    return B.tube(rings, color, bone, nostud=nostud)


def band(B, y0, y1, color, bone, zlo=-1.0, zhi=1.0, grow=0.008, inset=0.02, zhi1=None, narrow1=None):
    """flush pattern shell on the hull between the height fractions zlo..zhi (a bottom band when zlo = -1, a top band
    when zhi = 1): outer skin `grow` proud, inner skin `inset` under the hull, so only a crisp grow-high edge shows.
    zhi1 ramps the top edge to a new fraction at y1 (tongue points); narrow1 shrinks a top band's arc toward the
    spine (1 = full .. ~0.1 = a point) along the piece - the saddle chevron."""
    import blockkit as bk
    ys = ys_between(y0, y1, [y0 + (y1 - y0) * t for t in (0.25, 0.5, 0.75)])
    rings = []
    for y in ys:
        t = (y - y0) / (y1 - y0)
        hw, zc, hh = hull(y)
        zh = zhi if zhi1 is None else zhi + (zhi1 - zhi) * t
        if zlo <= -1:
            a = zang(zh)
            a0, a1 = a, -math.pi - a                     # right side down round the belly to the left side
        else:
            a = zang(zlo)
            a0, a1 = math.pi - a, a                      # left side over the back to the right side
            if narrow1 is not None:
                k_ = 1.0 + (narrow1 - 1.0) * t
                a0, a1 = math.pi / 2 + (a0 - math.pi / 2) * k_, math.pi / 2 + (a1 - math.pi / 2) * k_
        o = bk.superellipse(hw + grow, hh + grow, zc, y, SE_N, SEG // 2, a0, a1)
        i = bk.superellipse(hw - inset, hh - inset, zc, y, SE_N, SEG // 2, a0, a1)
        rings.append((o, i))
    return B.tube(rings, color, bone, closed=False)


def surf_hit(B, blks, origin, direction):
    import blockkit as bk
    from mathutils.bvhtree import BVHTree
    B._resolve()
    best = None
    d = Vector(direction).normalized()
    for blk in blks:
        bm = bk.part_bm(blk)
        t = BVHTree.FromBMesh(bm)
        bm.free()
        loc, nrm, _, dist = t.ray_cast(Vector(origin), d)
        if loc is not None and (best is None or dist < best[2]):
            best = (loc, nrm.normalized(), dist)
    if best is None:
        raise RuntimeError("surf_hit: no surface from %s" % (tuple(origin),))
    return best[0], best[1]


def strip(B, blks, origins, direction, width, thick, color, bone, proud=0.008, tip0=False, tip1=False, **kw):
    """flush bars along a surface through ray hits (Ivonrath surf_strip); studded unless told otherwise"""
    hits = [surf_hit(B, blks, o, direction) for o in origins]
    kw.setdefault("bevel", 0.004)
    for i in range(len(hits) - 1):
        (a, na), (b, nb) = hits[i], hits[i + 1]
        n = (na + nb).normalized()
        a2, b2 = a + n * (proud - thick), b + n * (proud - thick)
        bn = bone(a.lerp(b, 0.5).y) if callable(bone) else bone
        if tip0 and i == 0:
            B.bar(b2, a2, n, width, thick, color, bn, top=(1, 0.2), **kw)
        elif tip1 and i == len(hits) - 2:
            B.bar(a2, b2, n, width, thick, color, bn, top=(1, 0.2), **kw)
        else:
            B.bar(a2, b2, n, width, thick, color, bn, **kw)


def bead(B, p, n, r, bone, socket=False):
    """jade lantern bead: (DEEP socket) -> GLOW dome -> HOT centre, seated on the surface (normal n)"""
    import blockkit as bk
    n = Vector(n).normalized()
    side = Vector((0, 1, 0)) if abs(n.y) < 0.9 else Vector((1, 0, 0))
    R = bk.frame_from(p, p + n, side)
    if socket:
        B.add(p + n * 0.002, (r * 1.3, r * 1.3, 0.006), DEEP, bone, R=R, studs=[], role="detail", bevel=0.004)
    from mathutils import Matrix
    for Rr in (R, R @ Matrix.Rotation(math.radians(45), 3, "Z")):      # FIX 7: two domes 45 deg apart = octagon
        B.add(p + n * 0.006, (r, r, 0.012), GLOW, bone, R=Rr, studs=[], role="detail", rnd=0.6, nostud=True)
    B.add(p + n * 0.017, (max(0.012, r * 0.42), max(0.012, r * 0.42), 0.005), HOT, bone, R=R, studs=[],
          role="detail", bevel=0.003)


def fierce_eye(B, c, n, s, bone="Head", sc=1.15):
    """jade slit eye on the hull surface (normal n): black socket -> GLOW slit -> HOT spot, pupil, INK_D brow angled
    down toward the snout"""
    import blockkit as bk
    n = Vector(n).normalized()
    fwd = Vector((0, -1, 0))
    t = (fwd - n * fwd.dot(n)).normalized()                     # along the surface toward the snout
    up = n.cross(t).normalized() * (1 if s > 0 else -1)
    if up.z < 0:
        up = -up
    from mathutils import Matrix
    tilt = math.radians(14)
    t2 = (t * math.cos(tilt) - up * math.sin(tilt)).normalized()   # front end lower (inner corner down)
    up2 = n.cross(t2).normalized()
    if up2.z < 0:
        up2 = -up2
    R = Matrix((t2, n, up2)).transposed()                     # local x along the slit, y = out, z = up
    c = Vector(c)
    B.add(c, (0.052 * sc, 0.008, 0.025 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + n * 0.006, (0.044 * sc, 0.006, 0.0135 * sc), GLOW, bone, R=R, studs=[], role="detail", bevel=0.003)
    B.add(c + n * 0.011 - t2 * 0.018 * sc, (0.014 * sc, 0.004, 0.006 * sc), HOT, bone, R=R, studs=[], role="detail",
          bevel=0.002)
    B.add(c + n * 0.011 + t2 * 0.004, (0.006 * sc, 0.004, 0.0135 * sc), BLACK, bone, R=R, studs=[], role="detail",
          bevel=0.002)
    t3 = (t * math.cos(math.radians(-20)) - up * math.sin(math.radians(-20))).normalized()
    up3 = n.cross(t3).normalized()
    if up3.z < 0:
        up3 = -up3
    Rb = Matrix.Rotation(math.radians(-8 * s), 3, "Z") @ Matrix((t3, n, up3)).transposed()   # turned 8 deg to the face
    B.add(c + up2 * 0.040 * sc, (0.07 * sc, 0.022, 0.022 * sc), INK_D, bone, R=Rb, role="detail",
          bevel=0.01)                                                                      # seated flush


def blade_seg(B, a, b, hw0, hw1, th0, th1, color, bone, side, **kw):
    """tapered fin block a -> b: chord half-width hw0 -> hw1 along `side`, half-thickness th0 -> th1"""
    return B.seg(a, b, hw0, th0, color, bone, side=side, top=(hw1 / hw0, th1 / th0), **kw)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=401, tier=5, plates=False, th=0.653)       # th: the v2 box hull (tubes are not boxes)
    z = Z0
    # ================= HULL: lofted INK torpedo (upper head above the mouth line; lower jaw separate, WHITE)
    # review 2 FIX 3, done as smooth station-exact tubes (one per bone, flush overlapping joints - no seg creases)
    headb = [hull_tube(B, -1.30, -0.80 + OV, INK, "Head", zlo=MOUTH_F, j1=-0.80)]
    bodyb = [hull_tube(B, -0.80 - OV, -0.05 + OV, INK, "Chest", j0=-0.80, j1=-0.05),
             hull_tube(B, -0.05 - OV, 0.26 + OV, INK, "Spine", j0=-0.05, j1=0.26),
             hull_tube(B, 0.26 - OV, 0.50 + OV, INK, "Tail1", j0=0.26, j1=0.50),
             hull_tube(B, 0.50 - OV, 0.79 + OV, INK, "Tail2", j0=0.50, j1=0.79),
             hull_tube(B, 0.79 - OV, 0.94, INK, "Tail3", j0=0.79)]
    hullb = headb + bodyb
    # throat under the head behind the jaw (the jaw hinge is at y -0.94): the part below the mouth line
    hull_tube(B, -0.99, -0.80 + OV, WHITE, "Head", zhi=MOUTH_F, grow=0.004, j1=-0.80)
    # ================= lower jaw (WHITE, Jaw bone, 8 deg open) + INK_D lip line, teeth, mouth roof / floor
    jaw = loft(B, -1.29, -0.94, WHITE, "Jaw", zlo=-1.0, zhi=MOUTH_F - 0.02, xf=jawpt, rnd=0.42)
    for s in (1, -1):
        p0, p1 = Vector((s * 0.0, -1.30, 0)), None
    lip = []
    for y in (-1.27, -1.18, -1.09, -1.00, -0.92):
        hw, zc, hh = hull(y)
        lip.append((y, hw, zc + MOUTH_F * hh))
    for s in (1, -1):
        for (ya, wa, za), (yb, wb, zb) in zip(lip, lip[1:]):
            B.seg((s * (wa - 0.012), ya, za + 0.008), (s * (wb - 0.012), yb, zb + 0.004), 0.016, 0.012, INK_D, "Head",
                  side=(0, 0, 1), studs=[], role="detail", ext=0.006)                       # lip line
    # mouth line steps DOWN slightly at the back (snarl, never the smile curve): last lip piece dips 0.012
    B.seg((0, -1.25, z - 0.115), (0, -0.96, z - 0.135), 0.13, 0.006, MOUTH, "Head", top=(1.6, 1), studs=[],
          role="detail", bevel=0.003)                                                       # roof
    B.seg(jawpt((0, -1.25, z - 0.125)), jawpt((0, -0.96, z - 0.145)), 0.09, 0.006, MOUTH, "Jaw", top=(1.3, 1),
          studs=[], role="detail", bevel=0.003)                                             # floor
    up_t = [(-1.255, 0.08), (-1.21, 0.08), (-1.16, 0.072), (-1.11, 0.07), (-1.06, 0.068), (-1.01, 0.066),
            (-0.965, 0.065)]
    for s in (1, -1):
        for y, L in up_t:
            hw, zc, hh = hull(y)
            zl = zc + MOUTH_F * hh
            B.spike((s * (hw * 0.82), y, zl + 0.012), (s * 0.12, -0.05, -1), L, 0.026, TEETH, "Head")
        for y, L in [(-1.235, 0.06), (-1.185, 0.06), (-1.135, 0.06), (-1.085, 0.06), (-1.035, 0.06), (-0.99, 0.058)]:
            hw, zc, hh = hull(y)
            zl = zc + MOUTH_F * hh
            B.spike(jawpt((s * (hw * 0.70), y, zl - 0.03)), (s * 0.08, -0.05, 1), L, 0.024, TEETH, "Jaw")
    # ================= orca pattern (flush, studded): belly band, flank lobes, eye-patch lens, saddle, blowhole
    # belly band: one smooth white line per bone, falling toward the tail (under the lobes: grow 0.0075)
    for y0, y1, bone, zh0, zh1, g in ((-0.82, -0.05 + 0.02, "Chest", -0.30, -0.45, 0.0075),
                                      (-0.05, 0.26 + 0.02, "Spine", -0.45, -0.52, 0.0072),
                                      (0.26, 0.50, "Tail1", -0.52, -0.66, 0.0070)):
        band(B, y0, y1, WHITE, bone, zhi=zh0, zhi1=zh1, grow=g)
    def patch(s, outline, bone, blks, thick=0.016, proud=0.007):
        """flush white patch: outline [(y, z), ...] (closed, star-shaped around its mean) seated on the hull side,
        built in fan sections of <= 4 edges so the flat prisms follow the curve"""
        hits = [surf_hit(B, blks, (s * 1.0, y, zz), (-s, 0, 0)) for y, zz in outline]
        P = [p + n * proud for p, n in hits]
        cy = sum(y for y, _ in outline) / len(outline)
        cz = sum(zz for _, zz in outline) / len(outline)
        cp, cn = surf_hit(B, blks, (s * 1.0, cy, cz), (-s, 0, 0))
        C = cp + cn * proud
        N = len(P)
        step = 3
        for i in range(0, N, step):
            sec = [P[(i + j) % N] for j in range(step + 1)]
            B.poly([C] + sec, thick, WHITE, bone(C.y) if callable(bone) else bone)
    # flank lobes (review 2 FIX 2): 5 stepped, studded WHITE shells rising toward the back, split at Tail1
    for i, (y0, y1, bone, zhi, zhi1) in enumerate(((-0.08, 0.10, "Spine", -0.15, -0.15),
                                                   (0.08, 0.20, "Spine", 0.05, 0.05),
                                                   (0.18, 0.26, "Spine", 0.20, 0.20),
                                                   (0.26, 0.38, "Tail1", 0.30, 0.30),
                                                   (0.36, 0.48, "Tail1", 0.30, -0.45))):    # the tongue's point
        band(B, y0, y1, WHITE, bone, zhi=zhi, zhi1=zhi1, grow=0.008 + 0.0003 * i)
    for s in (1, -1):
        # eye-patch lens (FIX 4, ~1.4x): pointed at both ends, y -1.00 -> -0.70, centre line z+0.03 -> z+0.11
        lens = []
        for t in (0.0, 0.25, 0.5, 0.75, 1.0):
            y = -1.00 + 0.30 * t
            lens.append((y, Z0 + 0.03 + 0.08 * t + 0.065 * math.sin(math.pi * t)))
        for t in (0.75, 0.5, 0.25):
            y = -1.00 + 0.30 * t
            lens.append((y, Z0 + 0.03 + 0.08 * t - 0.055 * math.sin(math.pi * t)))
        patch(s, lens, "Head", headb + bodyb[:1])
    # saddle (FIX 1): a flush 2-piece chevron on the back (Spine piece hidden under the dorsal's trailing root,
    # Tail1 piece 0.0005 under it in the 0.01 overlap), narrowing to a point toward the tail
    band(B, 0.10, 0.26, SADDLE, "Spine", zlo=0.40, grow=0.010, narrow1=0.90)
    band(B, 0.25, 0.46, SADDLE, "Tail1", zlo=0.40, grow=0.0095, narrow1=0.08)
    B.add((0, -0.76, hull(-0.76)[1] + hull(-0.76)[2] + 0.004), (0.035, 0.0125, 0.006), INK_D, "Head", studs=[],
          role="detail", bevel=0.004)                                                          # blowhole
    ANCH["Blow"] = (0, -0.76, hull(-0.76)[1] + hull(-0.76)[2] + 0.02)
    # ================= face: jade slit eyes seated just above the mouth corner
    for s in (1, -1):
        p, n = surf_hit(B, headb, (s * 1.0, -1.00, z - 0.05), (-s, 0, 0))
        fierce_eye(B, p + n * 0.004, n, s, "Head", sc=1.15)
    # ================= HERO: crowned angler lantern
    cr = ROD[0]
    for j in range(8):                                                                         # gold coronet ring
        ang = 2 * math.pi * j / 8
        c = cr + Vector((math.cos(ang), math.sin(ang), 0)) * 0.075 + Vector((0, 0, 0.012))
        B.add(c, (0.014, 0.032, 0.016), GOLD, "Head", rot=(0, 0, math.degrees(ang)), role="limb", bevel=0.004,
              nostud=True)
    for x, h in ((-0.07, 0.06), (-0.035, 0.09), (0.0, 0.12), (0.035, 0.09), (0.07, 0.06)):
        B.spike(cr + Vector((x, -0.05, 0.02)), (0, -0.15, 1), h, 0.028, GOLD, "Head", top=(0.12, 0.12),
                studs=[], nostud=True)
    for i, (a, b) in enumerate(zip(ROD, ROD[1:])):                                            # rod
        w = 0.048 - 0.0055 * i
        bone = "Lure" if i < 2 else "Lure2"
        B.seg(a, b, w * 0.5, w * 0.5, INK_D, bone, ext=0.02, ext1=0.02 if i < 3 else 0.0, top=(0.9, 0.9),
              role="limb", rnd=0.4)
    for p, bone in ((ROD[1], "Lure"), (ROD[2], "Lure2"), (ROD[3], "Lure2")):                  # gold rings
        d = (ROD[min(ROD.index(p) + 1, 4)] - ROD[ROD.index(p) - 1]).normalized()
        B.seg(p - d * 0.022, p + d * 0.022, 0.035, 0.035, GOLD, bone, role="limb", studs=[], nostud=True, rnd=0.3)
    B.seg(ROD[4] + Vector((0, 0, 0.0)), ORB + Vector((0, 0.01, 0.15)), 0.018, 0.018, INK_D, "Esca", role="limb",
          ext=0.01)                                                                            # hanging stalk
    B.add(ORB + Vector((0, 0, 0.165)), (0.065, 0.065, 0.03), GOLD, "Esca", top=(0.8, 0.8), role="limb",
          nostud=True)                                                                         # collar
    # FIX 6: the jade orb as a smooth lathed DROP OF LIGHT (widest just under the middle, a point into the drip)
    PROF = [(0.15, 0.07), (0.13, 0.115), (0.09, 0.145), (0.04, 0.158), (-0.02, 0.155), (-0.07, 0.13), (-0.11, 0.09),
            (-0.145, 0.05), (-0.165, 0.03)]
    rings = [[ORB + Vector((r * math.cos(2 * math.pi * j / 20), r * math.sin(2 * math.pi * j / 20), dz))
              for j in range(20)] for dz, r in PROF]
    B.tube(rings, GLOW, "Esca", nostud=True)
    # (no glint sticker: the lantern's Studio glow supplies the highlight - review 3)
    B.spike(ORB - Vector((0, 0, 0.165)), (0, 0, -1), 0.10, 0.035, HOT, "Esca", studs=[], nostud=True,
            top=(0.12, 0.12))                                                                  # drip tip
    for j in range(5):                                                                         # 5 gold cage fangs
        ang = 2 * math.pi * j / 5 + math.pi / 2
        rv = Vector((math.cos(ang), math.sin(ang), 0))
        a = ORB + rv * 0.075 + Vector((0, 0, 0.19))
        b = ORB + rv * 0.172 + Vector((0, 0, 0.09))
        B.seg(a, b, 0.02, 0.02, GOLD, "Esca", side=rv, top=(0.85, 0.85), role="limb", studs=[], nostud=True,
              ext=0.01)
        c = ORB + rv * 0.165 + Vector((0, 0, -0.03))
        B.seg(b, c, 0.019, 0.019, GOLD, "Esca", side=rv, top=(0.8, 0.8), role="limb", studs=[], nostud=True,
              ext=0.01)
        B.spike(c, (rv * -0.6 + Vector((0, 0, -1))).normalized(), 0.07, 0.016, GOLD_D, "Esca", side=rv,
                studs=[], nostud=True)                                                         # claw tip
    ANCH["Bulb"] = tuple(ORB)
    # ================= DORSAL: the sovereign blade (4 stepped studded INK blocks), serrations, jade veins
    lev = [0.92, 1.16, 1.40, 1.60, 1.80]

    def le(zz):
        return -0.36 + (zz - 0.92) * 0.545

    def te(zz):
        return 0.14 + 0.02 * math.sin(math.pi * (zz - 0.92) / 0.88) - 0.02 * (zz - 0.92) / 0.88

    thick = [0.055, 0.045, 0.037, 0.03, 0.012]
    dblk = []
    for i in range(4):
        z0_, z1_ = lev[i], lev[i + 1]
        yb0, yb1 = le(z0_), te(z0_)
        yt0, yt1 = (le(z1_), te(z1_)) if i < 3 else (0.115, 0.125)
        cb, hb = (yb0 + yb1) / 2, (yb1 - yb0) / 2 * (0.97 if i else 1.0)
        ct, ht = (yt0 + yt1) / 2, max(0.006, (yt1 - yt0) / 2)
        dblk.append(B.add((0, cb, (z0_ + z1_) / 2 - (z1_ - z0_) / 2 + (z1_ - z0_) / 2), (thick[i], hb, (z1_ - z0_) / 2),
                          INK, "Dorsal", top=(thick[i + 1] / thick[i], ht / hb), top_shift=(0, ct - cb),
                          rnd=0.30))
    for zz, L in ((1.05, 0.10), (1.28, 0.09), (1.50, 0.08)):                                   # serrations
        B.spike((0, te(zz) - 0.02, zz), (0, 1, -0.35), L, 0.035, INK_D, "Dorsal", top=(0.15, 0.3))
    for s in (1, -1):                                                                           # veins, both faces
        trunk = [(s * 1.0, -0.02, 0.98), (s * 1.0, 0.0, 1.20), (s * 1.0, 0.04, 1.45), (s * 1.0, 0.075, 1.66)]
        strip(B, dblk, trunk, (-s, 0, 0), 0.04, 0.008, GLOW, "Dorsal", proud=0.006, tip1=True, studs=[],
              nostud=True)
        strip(B, dblk, trunk[:3], (-s, 0, 0), 0.02, 0.008, HOT, "Dorsal", proud=0.010, studs=[], nostud=True)
        for zz, L in ((1.15, 0.16), (1.38, 0.12)):
            y0 = -0.02 + (zz - 0.98) * 0.1
            br = [(s * 1.0, y0, zz), (s * 1.0, y0 - L * 0.45, zz + L * 0.8)]
            strip(B, dblk, br, (-s, 0, 0), 0.028, 0.008, GLOW, "Dorsal", proud=0.006, tip1=True, studs=[],
                  nostud=True)
    ANCH["DorsalTip"] = (0, 0.12, 1.80)
    # ================= pectorals: broad rounded orca paddles (3 tapered blocks), white-free, jade vein
    for s, side in ((1, "L"), (-1, "R")):
        fb = "Fin_" + side
        r0 = Vector((s * 0.24, -0.50, z - 0.20))
        tp = Vector((s * 0.64, -0.30, z - 0.42))
        d = (tp - r0)
        chord = Vector((0, 1, 0)) - d.normalized() * d.normalized().y
        pts = [r0, r0 + d * 0.36, r0 + d * 0.72, tp]
        fins = []
        for (a, b), (w0, w1), (t0, t1) in zip(zip(pts, pts[1:]), ((0.12, 0.15), (0.15, 0.12), (0.12, 0.07)),
                                              ((0.04, 0.033), (0.033, 0.026), (0.026, 0.0175))):
            fins.append(blade_seg(B, a, b, w0, w1, t0, t1, INK, fb, chord, ext=0.02, rnd=0.45 if b != tp else 0.6))
        nf = d.cross(chord).normalized()
        if nf.z < 0:
            nf = -nf
        vt = [r0 + d * 0.15 + nf * 0.5, r0 + d * 0.55 + nf * 0.5, r0 + d * 0.85 + nf * 0.5]
        strip(B, fins, vt, -nf, 0.03, 0.008, GLOW, fb, proud=0.006, tip1=True, studs=[], nostud=True)
    # ================= flukes: crescent, swept tips, centre notch, white undersides, jade vein + HOT tip bead
    for s, side in ((1, "L"), (-1, "R")):
        P = [Vector((s * x, y, z + 0.03)) for x, y in ((0.015, 0.82), (0.20, 0.92), (0.34, 1.00), (0.46, 1.12))]
        fl = []
        for (a, b), (c0, c1), (t0, t1) in zip(zip(P, P[1:]), ((0.10, 0.085), (0.085, 0.06), (0.06, 0.012)),
                                              ((0.03, 0.025), (0.025, 0.02), (0.02, 0.012))):
            dd = (b - a).normalized()
            ch = Vector((-dd.y, dd.x, 0)) * s
            fl.append(blade_seg(B, a, b, c0, c1, t0, t1, INK, "Tail3", ch, ext=0.02, rnd=0.4))
            B.seg(a + Vector((0, 0, -t0 + 0.004)), b + Vector((0, 0, -t1 + 0.004)), c0 * 0.85, 0.006, WHITE, "Tail3",
                  side=ch, top=(c1 / c0, 1), studs=[], ext=0.01)                                  # white underside
        vt = [Vector((s * 0.08, 0.86, 2.0)), Vector((s * 0.25, 0.95, 2.0)), Vector((s * 0.40, 1.06, 2.0))]
        strip(B, fl, vt, (0, 0, -1), 0.026, 0.008, GLOW, "Tail3", proud=0.006, tip1=True, studs=[], nostud=True)
        bead(B, P[3] + Vector((0, -0.03, 0.016)), (0, 0, 1), 0.022, "Tail3")
        ANCH["Fluke" + side] = tuple(P[3])
    # ================= abyssal lights: waterline rows (10 / side) + spine row (3 front, 4 behind the dorsal)
    zfr = {"Chest": -0.30, "Spine": -0.40, "Tail1": -0.48, "Tail2": -0.30}
    for s in (1, -1):
        for i in range(10):
            y = -0.70 + i * 0.147
            hw, zc, hh = hull(y)
            bone = bone_at(y)
            fr = -0.28 if y < -0.50 else -0.38 if y < -0.05 else -0.48 if y < 0.26 else -0.30
            p, n = surf_hit(B, hullb, (s * 1.0, y, zc + fr * hh), (-s, 0, 0))
            bead(B, p, n, 0.032 - 0.0125 * i / 9, bone, socket=i < 4)
    for y in (-0.66, -0.54, -0.42, 0.28, 0.42, 0.56, 0.68):
        hw, zc, hh = hull(y)
        p, n = surf_hit(B, hullb, (0, y, 3.0), (0, 0, -1))
        bead(B, p, n, 0.03 if y < 0 else 0.026, bone_at(y), socket=y < 0)
    ANCH["Glow1"], ANCH["Glow2"], ANCH["Glow3"] = (0, -0.54, hull(-0.54)[1] + hull(-0.54)[2]), \
        (0, 0.42, hull(0.42)[1] + hull(0.42)[2]), (0, 0.68, hull(0.68)[1] + hull(0.68)[2])
    ANCH["Maw"] = (0, -1.31, z - 0.10)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


# ------------------------------------------------------------------ rig
def rig(k):
    z = Z0
    k.joint("Spine", (0, -0.05, z), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.42, z), "Spine", tail=(0, -0.4, 0))
    k.joint("Head", (0, -0.80, z - 0.08), "Chest", tail=(0, -0.3, 0))           # at the throat, low / back
    k.joint("Jaw", tuple(JAW_P), "Head", tail=(0, -0.25, 0))
    k.joint("Lure", tuple(ROD[0]), "Head", tail=tuple(ROD[1] - ROD[0]))
    k.joint("Lure2", tuple(ROD[2]), "Lure", tail=tuple(ROD[3] - ROD[2]))
    k.joint("Esca", tuple(ROD[4]), "Lure2", tail=(0, 0, -0.2))
    k.joint("Bulb", ANCH.get("Bulb", tuple(ORB)), "Esca", tail=(0, 0, -0.1))
    k.joint("Blow", ANCH.get("Blow", (0, -0.76, 0.91)), "Head", tail=(0, 0, 0.2))
    k.joint("Maw", ANCH.get("Maw", (0, -1.31, z - 0.10)), "Head", tail=(0, -0.15, 0))
    k.joint("Dorsal", (0, -0.10, 0.95), "Spine", tail=(0, 0.1, 0.4))
    k.joint("DorsalTip", ANCH.get("DorsalTip", (0, 0.12, 1.80)), "Dorsal", tail=(0, 0.05, 0.1))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Fin_" + side, (s * 0.26, -0.50, z - 0.20), "Chest", tail=(s * 0.3, 0.1, -0.2))
    k.joint("Tail1", (0, 0.26, z + 0.02), "Spine", tail=(0, 0.24, 0))
    k.joint("Tail2", (0, 0.50, z + 0.02), "Tail1", tail=(0, 0.29, 0.01))
    k.joint("Tail3", (0, 0.79, z + 0.03), "Tail2", tail=(0, 0.3, 0.0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Fluke" + side, ANCH.get("Fluke" + side, (s * 0.46, 1.12, z + 0.03)), "Tail3", tail=(s * 0.1, 0.1, 0))
    for nm, bone in (("Glow1", "Chest"), ("Glow2", "Tail1"), ("Glow3", "Tail2")):
        k.joint(nm, ANCH.get(nm, (0, 0, 1)), bone, tail=(0, 0, 0.1))


def check_pairs():
    return [("Head", "Fin_L"), ("Head", "Fin_R"), ("Jaw", "Fin_L"), ("Jaw", "Fin_R"), ("Lure", "Chest"),
            ("Lure", "Dorsal"), ("Lure2", "Dorsal"), ("Esca", "Dorsal"), ("Esca", "Head"), ("Esca", "Jaw"),
            ("Tail1", "Dorsal"), ("Tail2", "Dorsal"), ("Tail3", "Spine"), ("Tail3", "Chest"), ("Tail2", "Chest"),
            ("Fin_L", "Spine"), ("Fin_R", "Spine"), ("Fin_L", "Chest"), ("Fin_R", "Chest")]


def joints():
    # pectoral root hinge: the root chord block sits in the hull surface at the pivot (the paddle turns about it)
    return [((s * 0.25, -0.64, Z0 - 0.20), (s * 0.25, -0.34, Z0 - 0.20), 0.08, "Fin_" + side)
            for s, side in ((1, "L"), (-1, "R"))]


# ------------------------------------------------------------------ animation
# Reference (owner rule 2026-10-10, notes in _review/ANIM_REFERENCES_1014.md): animationreference.org "The Old Man and
# the Sea" (A. Petrov, Sakugabooru #17124): big swimmers glide on a slow ~0.9 s beat with the front of the body almost
# still, the strike drives the head INTO the target while the tail snaps the other way; "Children of the Sea" #111777:
# hovering fish only work the tail third; "Sea Beasts" 0-3 s: heavy-head display = gather/tuck, then the jaw opens
# a beat AFTER the head commits. The orca drives its flukes VERTICALLY (the Hammerjaw owns the lateral sweep).
# Key conventions: kit pitch + = nose down / tail UP (tail + lifts); the jaw is MODELLED 8 deg open, so key = total - 8
# (shut = -8, never below); Chest vs Spine <= 4 (rolls and counters live on Spine); Esca hangs plumb (it cancels the
# rod rotation above it) unless swinging.
import petkit as pk
import _common as cm

TAILS = ["Tail1", "Tail2", "Tail3"]
JAW_SHUT = -JAW_OPEN


def fins(k, f, down=0.0, back=0.0, dl=0.0, dr=0.0):
    """down + = both pectoral tips drop, back + = swept back; dl / dr add per side (roll toward the low side)"""
    k.key("Fin_L", f, rot=(0, back, down + dl))
    k.key("Fin_R", f, rot=(0, -back, -(down + dr)))


def lure(k, f, l1=0.0, l2=0.0, esca=0.0, plumb=True):
    """rod: Lure / Lure2 pitch + = tips forward and down; the Esca hangs plumb (cancels the rod) + its own swing"""
    k.key("Lure", f, rot=(l1, 0, 0))
    k.key("Lure2", f, rot=(l2, 0, 0))
    k.key("Esca", f, rot=((-(l1 + l2) if plumb else 0.0) + esca, 0, 0))


def tails(k, f, p=(0, 0, 0), y=(0, 0, 0)):
    for b, pp, yy in zip(TAILS, p, y):
        k.key(b, f, rot=(pp, yy, 0))


def ground_lift(k, n, target=0.02):
    """FLOOR RULE (Kraken L214, keeps Spine x/y): raise the body on any frame where a vertex dips under target"""
    import bpy
    sc = bpy.context.scene
    pb = k.arm.pose.bones["Spine"]
    R0 = k.arm.data.bones["Spine"].matrix_local.to_quaternion()
    k.bake_bezier_now()
    fix = []
    for f in range(0, n + 1):
        sc.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        ev = k.main.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        z = min((mw @ v.co).z for v in me.vertices)
        ev.to_mesh_clear()
        if z < target:
            fix.append((f, R0 @ pb.location, target - z))
    for f, cur, lift in fix:
        k.key("Spine", f, loc=(cur.x, cur.y, cur.z + lift))


def phase45(u):
    """warped stroke phase: the power DOWNstroke (0 -> 0.5) takes 45 % of the cycle, the recovery 55 %"""
    u %= 1.0
    return 0.5 * u / 0.45 if u < 0.45 else 0.5 + 0.5 * (u - 0.45) / 0.55


def swim(k):
    """FLUKE DRIVE: a vertical travelling wave Spine -> Tail1 -> Tail2 -> Tail3 (+-2.5 / 7 / 13 / 22, lag 0.08),
    power downstroke 45 %, the body heaves up at the end of the downstroke, the head stays level, the pectorals trim
    with the heave and the lantern follows through on the rod (Lure, Lure2 4 f late, Esca pendulum 7 f late)."""
    n = 36
    k.new_action("swim", n, True)
    for f in range(0, n + 1, 2):
        u = f / n
        c = [math.cos(2 * math.pi * phase45(u - 0.08 * i)) for i in range(4)]
        ph = phase45(u)
        k.key("Spine", f, rot=(-2.5 * c[0], 0, 1.5 * math.sin(2 * math.pi * u)),
              loc=(0, 0, 0.0075 - 0.0275 * math.cos(2 * math.pi * ph)))
        k.key("Chest", f, rot=(0.8 * c[0], 0, 0))
        k.key("Head", f, rot=(0.9 * c[0], 0, 0))
        tails(k, f, (7 * c[1], 13 * c[2], 22 * c[3]))
        fins(k, f, down=-3 + 5 * math.sin(2 * math.pi * (ph - 0.1)))
        lure(k, f, 3 * math.sin(2 * math.pi * (u - 0.11)), 6 * math.sin(2 * math.pi * (u - 0.22)),
             10 * math.sin(2 * math.pi * (u - 0.33)))
        k.key("Jaw", f, rot=(0, 0, 0))
    ground_lift(k, n)
    k.finish()
    return 0.0


def idle(k):
    """SOVEREIGN PATROL & BLOW: a slow heave with 2 lazy fluke beats, alternate pectoral sculls and a lagging lantern;
    a SPYHOP glance (nose up, ONE slow look left, hold, ONE slow look right, hold - not a shake); the BLOW (head dips,
    the body rises, pectorals flick, event blow); a lazy 14 deg roll that shows the white belly."""
    n = 120
    k.new_action("idle", n, True)
    spy = [(0, 0, 0, 0, 0), (28, 0, 0, 0, 0), (34, -8, -4, 0, 0), (42, -8, -4, 4, 10), (50, -8, -4, 4, 10),
           (60, -8, -4, -4, -10), (66, -8, -4, -4, -10), (76, 0, 0, 0, 0), (120, 0, 0, 0, 0)]

    def interp(tab, f, i):
        for a, b in zip(tab, tab[1:]):
            if a[0] <= f <= b[0]:
                t = (f - a[0]) / float(b[0] - a[0])
                t = t * t * (3 - 2 * t)
                return a[i] + (b[i] - a[i]) * t
        return 0.0
    for f in range(0, n + 1, 2):
        u = f / n
        sp, hp, cy, hy = (interp(spy, f, i) for i in (1, 2, 3, 4))
        blow = math.sin(math.pi * min(1.0, max(0.0, (f - 76) / 10.0)))          # f76-86
        roll = 14 * math.sin(math.pi * min(1.0, max(0.0, (f - 88) / 28.0))) ** 2  # f88-116
        k.key("Spine", f, rot=(sp + 1.0 * math.sin(4 * math.pi * u), 0, roll),
              loc=(0, 0, 0.03 * math.sin(4 * math.pi * u) + 0.04 * blow))
        k.key("Chest", f, rot=(0, cy, 0))
        k.key("Head", f, rot=(hp + 3 * blow, hy, 0))
        w = math.sin(4 * math.pi * (u - 0.1))
        tails(k, f, (4 * w, 8 * math.sin(4 * math.pi * (u - 0.18)), 12 * math.sin(4 * math.pi * (u - 0.26))))
        sc_ = 6 * math.sin(2 * math.pi * 3 * u)
        fins(k, f, down=-2 - 8 * blow, dl=sc_ - 10 * roll / 14.0, dr=-sc_)
        lure(k, f, 3 * math.sin(4 * math.pi * (u - 0.08)), 5 * math.sin(4 * math.pi * (u - 0.16)),
             8 * math.sin(4 * math.pi * (u - 0.26)))
        k.key("Jaw", f, rot=(0, 0, 0))
    ground_lift(k, n)
    k.finish()
    k.events["idle"] = {"blow": round(80 / n, 3)}


def roar(k):
    """JAW-CLAP THREAT (in place, not a rear-up): draws back with the flukes cocked, SNAPS forward nose-down at the
    viewer with the jaw wide, pectorals flared down as a brake display and the lantern thrust over the snout; three
    hard JAW CLAPS with two vertical tail lashes; releases, the lantern swings back with an overshoot."""
    n = 64
    k.new_action("roar", n, False)
    K = [  # f, spine y, spine pitch, jaw(total), fin down, fin back, lure, lure2, tail1..3 (kit: + lifts)
        (0, 0.0, 0, 8, 0, 0, 0, 0, 0, 0, 0),
        (12, 0.06, -6, 10, 0, 15, -3, -4, -4, -8, -12),
        (16, -0.02, 6, 12, 20, 0, 8, 6, 2, 3, 4),                  # the snap lands first, the gape follows
        (20, -0.04, 10, 44, 30, -6, 14, 10, 3, 4, 6),
        (40, -0.04, 10, 44, 30, -6, 14, 10, 0, 0, 0),
        (48, -0.02, 4, 20, 14, -2, 4, 2, 0, 0, 0),
        (54, 0.0, -1, 8, -4, 0, -5, -6, 0, 0, 0),
        (64, 0.0, 0, 8, 0, 0, 0, 0, 0, 0, 0)]
    for f, y, p, jw, fd, fb, l1, l2, t1, t2, t3 in K:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, y, 0))
        k.key("Chest", f, rot=(0, 0, 0))
        k.key("Head", f, rot=(0, 0, 0))
        k.key("Jaw", f, rot=(jw - JAW_OPEN, 0, 0))
        fins(k, f, fd, fb)
        lure(k, f, l1, l2, {48: 10, 54: -5}.get(f, 0))         # the lantern swings back with an overshoot
        tails(k, f, (t1, t2, t3))
    k.key("Jaw", 17, rot=(12 - JAW_OPEN, 0, 0))
    for c in (26, 32, 38):                                  # 3 jaw claps: 44 -> 12 in 2 f, back to 44 in 3 f
        for f, jw in ((c - 2, 44), (c, 12), (c + 3, 44)):
            k.key("Jaw", f, rot=(jw - JAW_OPEN, 0, 0))
    for f, jw in ((22, 42), (29, 46), (35, 42)):            # +-2 buzz between the claps
        k.key("Jaw", f, rot=(jw - JAW_OPEN, 0, 0))
    for c in (24, 36):                                      # 2 vertical tail lashes (up, then a hard down-lash)
        for f, g in ((c - 5, 1.0), (c, -1.2), (c + 5, 0.0)):     # the down-lash hits ON the event
            tails(k, f, (8 * g, 14 * g, 18 * g))
    ground_lift(k, n)
    k.finish(loop=False)
    k.events["roar"] = {"roar": round(20 / n, 3), "clap1": round(26 / n, 3), "clap2": round(32 / n, 3),
                        "clap3": round(38 / n, 3), "lash1": round(24 / n, 3), "lash2": round(36 / n, 3)}


DANGLE = (24.0, 30.0)          # Lure, Lure2 for the bait pose (scaled down by the Esca clearance check if needed)


def lure_act(k):
    """SIGNATURE - THE ABYSSAL LURE (angler ambush, in place): switches its lights off, lowers the lantern in front of
    its jaws as bait and twitches it three times, draws back and loads the flukes, whips the lure UP out of the strike
    line, then one hard fluke kick drives a GULP (jaw wide -> shut, hard stop); savours with two swallows and a lazy
    belly roll; relights head to tail and resumes its hover."""
    n = 120
    k.new_action("act_lure", n, False)
    d1, d2 = DANGLE
    K = [  # f, spine y, z, pitch, roll, chest, head, jaw(total), fin down, fin back, lure, lure2, esca, tails (kit)
        (0, 0.0, 0.0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, (0, 0, 0)),
        (12, 0.0, -0.05, 5, 0, 0, 0, 8, -8, 20, d1 * 0.6, d2 * 0.6, 0, (0, 0, 0)),
        (18, 0.0, -0.05, 5, 0, 0, 3, 8, -8, 20, d1, d2, 0, (0, 0, 0)),
        (42, 0.0, -0.05, 5, 0, 0, 3, 8, -8, 20, d1, d2, 0, (0, 0, 0)),
        (56, 0.10, -0.05, 5, 0, -4, -5, 14, 12, 0, d1 + 6, d2 + 2, 0, (-8, -12, -16)),
        (58, 0.10, -0.05, 5, 0, -4, -5, 16, 12, 0, -18, -24, 6, (-8, -12, -16)),
        (59, 0.02, -0.04, 6, 0, -2, 6, 44, 6, 10, -18, -24, 8, (14, 22, 30)),
        (60, -0.08, -0.04, 6, 0, 0, 6, 44, 4, 10, -16, -22, 8, (10, 16, 22)),
        (61, -0.12, -0.04, 6, 0, 0, 6, 26, 4, 10, -14, -20, 6, (6, 10, 14)),
        (62, -0.12, -0.04, 6, 0, 0, 6, 0, 4, 10, -12, -18, 4, (2, 4, 6)),
        (64, -0.12, -0.04, 4, 0, 0, 4, 0, 0, 6, -10, -14, 2, (0, 0, 0)),
        (77, -0.10, -0.03, 2, 22, 0, 2, 0, 0, 0, -6, -8, 0, (-2, -3, -4)),
        (90, -0.06, -0.02, 1, 0, 0, 0, 0, 0, 0, -2, -3, 0, (0, 0, 0)),
        (96, -0.03, 0.0, 0, 0, 0, 0, 8, 0, 0, 6, 2, 0, (0, 0, 0)),
        (104, 0.0, 0.0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, (0, 0, 0)),
        (120, 0.0, 0.0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, (0, 0, 0))]
    for f, y, z, p, r, ch, hd, jw, fd, fb, l1, l2, es, tl in K:
        k.key("Spine", f, rot=(p, 0, r), loc=(0, y, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(max(jw, 0) - JAW_OPEN, 0, 0))
        low = 15 * r / 22.0                                        # the low-side pectoral rises in the roll
        fins(k, f, fd, fb, dl=-low)
        lure(k, f, l1, l2, es)
        tails(k, f, tl)
    for c in (20, 28, 36):                                         # 3 bait twitches (Esca + Lure2), then holds
        for f, e, l2 in ((c, 0, d2), (c + 1, 12, d2 + 4), (c + 2, -12, d2 - 4), (c + 3, 0, d2), (c + 8, 0, d2)):
            k.key("Lure2", f, rot=(l2, 0, 0))
            k.key("Esca", f, rot=(-(d1 + l2) + e, 0, 0))
    for c in (66, 72):                                             # 2 swallow pulses
        k.key("Chest", c - 2, rot=(0, 0, 0))
        k.key("Chest", c, rot=(-2, 0, 0))
        k.key("Chest", c + 3, rot=(0, 0, 0))
    for f, e in ((92, 10), (97, -5), (102, 0)):                    # the orb swings back with an overshoot
        k.key("Esca", f, rot=(e, 0, 0))
    for c in (106, 114):                                           # 2 soft fluke strokes to resume
        tails(k, c, (3, 6, 9))
        tails(k, c + 4, (-3, -6, -9))
    tails(k, 120, (0, 0, 0))
    ground_lift(k, n)
    k.finish(loop=False)
    k.events["act_lure"] = {"dim": round(6 / n, 3), "twitch1": round(21 / n, 3), "twitch2": round(29 / n, 3),
                            "twitch3": round(37 / n, 3), "gulp": round(61 / n, 3), "relight": round(92 / n, 3),
                            "ripple": round(96 / n, 3), "glow1": round(96 / n, 3), "glow2": round(100 / n, 3),
                            "glow3": round(104 / n, 3)}


def anim(k):
    idle(k)
    stride = swim(k)
    roar(k)
    lure_act(k)
    return stride


HEAD_XF = []
