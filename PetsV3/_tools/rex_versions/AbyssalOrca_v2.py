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
SADDLE = (150, 162, 194)
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
STATIONS = [(-1.30, 0.10, 0.085, -0.07), (-1.06, 0.19, 0.20, -0.03), (-0.82, 0.26, 0.28, 0.0),
            (-0.50, 0.30, 0.32, 0.01), (-0.14, 0.285, 0.31, 0.03), (0.20, 0.23, 0.265, 0.02),
            (0.50, 0.13, 0.19, 0.02), (0.80, 0.065, 0.10, 0.03), (0.88, 0.05, 0.075, 0.03)]
JAW_P = Vector((0, -0.94, Z0 - 0.12))
JAW_OPEN = 8.0               # lower jaw MODELLED 8 deg open (rest)
MOUTH_F = -0.40              # mouth line as a fraction of the half-height (upper jaw above, lower jaw below)
ROD = [Vector(p) for p in ((0, -0.94, 0.84), (0, -0.98, 1.10), (0, -1.10, 1.32), (0, -1.27, 1.42), (0, -1.36, 1.38))]
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


def loft(B, y0, y1, color, bone, grow=0.0, zlo=-1.0, zhi=1.0, ext1=0.0, scale0=1.0, end_w=1.0, xf=None, **kw):
    """hull section y0 -> y1: tapered rounded seg whose ends match the stations; zlo / zhi (fractions of the
    half-height) cut a horizontal band; grow pads it (shells); end_w narrows the far end (chevrons); xf maps points"""
    pts = []
    for y in (y0, y1 + ext1):
        hw, zc, hh = hull(y)
        lo = zc + zlo * hh - (grow if zlo <= -1 else 0.0)
        hi = zc + zhi * hh + (grow if zhi >= 1 else 0.0)
        pts.append((Vector((0, y, (lo + hi) / 2)), hw + grow, (hi - lo) / 2))
    (p0, w0, d0), (p1, w1, d1) = pts
    if xf:
        p0, p1 = xf(p0), xf(p1)
    kw.setdefault("rnd", 0.40)
    return B.seg(p0, p1, w0 * scale0, d0 * scale0, color, bone, top=(w1 * end_w / (w0 * scale0), d1 / (d0 * scale0)),
                 **kw)


def surf_hit(B, blks, origin, direction):
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
    B.add(p + n * 0.006, (r, r, 0.012), GLOW, bone, R=R, studs=[], role="detail", rnd=0.6, nostud=True)
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
    Rb = Matrix((t3, n, up3)).transposed()
    B.add(c + up2 * 0.040 * sc + n * 0.006, (0.07 * sc, 0.022, 0.022 * sc), INK_D, bone, R=Rb, role="detail",
          bevel=0.01)


def blade_seg(B, a, b, hw0, hw1, th0, th1, color, bone, side, **kw):
    """tapered fin block a -> b: chord half-width hw0 -> hw1 along `side`, half-thickness th0 -> th1"""
    return B.seg(a, b, hw0, th0, color, bone, side=side, top=(hw1 / hw0, th1 / th0), **kw)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=401, tier=5, plates=False)
    z = Z0
    # ================= HULL: lofted INK torpedo (upper head above the mouth line; lower jaw separate, WHITE)
    head_up = loft(B, -1.30, -0.80, INK, "Head", zlo=MOUTH_F, ext1=0.10)
    hullb = [head_up,
             loft(B, -0.86, -0.50, INK, "Chest", ext1=0.12, scale0=0.97),
             loft(B, -0.50, -0.05, INK, "Chest", ext1=0.12),
             loft(B, -0.12, 0.26, INK, "Spine", ext1=0.10, scale0=0.97),
             loft(B, 0.20, 0.50, INK, "Tail1", ext1=0.07, scale0=0.97),
             loft(B, 0.44, 0.79, INK, "Tail2", ext1=0.04, scale0=0.97),
             loft(B, 0.74, 0.88, INK, "Tail3", scale0=0.97)]
    # throat under the head behind the jaw (the jaw hinge is at y -0.94)
    loft(B, -0.96, -0.80, WHITE, "Head", zlo=-1.0, zhi=MOUTH_F, grow=0.004)
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
    B.seg(jawpt((0, -1.25, z - 0.125)), jawpt((0, -0.96, z - 0.145)), 0.12, 0.006, MOUTH, "Jaw", top=(1.6, 1),
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
    for y0, y1, bone, zhi, e in ((-0.86, -0.50, "Chest", -0.42, 0.05), (-0.50, -0.05, "Chest", -0.52, 0.03),
                                 (-0.12, 0.26, "Spine", -0.62, 0.03), (0.20, 0.50, "Tail1", -0.70, 0.0)):
        loft(B, y0, y1, WHITE, bone, grow=0.008, zlo=-1.0, zhi=zhi, ext1=e, end_w=0.85 if bone == "Tail1" else 1.0)
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
    for s in (1, -1):
        # flank lobe: a white tongue rising from the belly behind the pectorals up and back to a point
        lobe = []
        for t in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):                       # upper edge, front -> tip
            y = -0.06 + 0.44 * t
            hw, zc, hh = hull(y)
            lobe.append((y, zc - 0.48 * hh + 0.62 * hh * t ** 1.3))
        for t in (0.75, 0.5, 0.25, 0.0):                               # lower edge back along the belly line
            y = -0.06 + 0.40 * t
            hw, zc, hh = hull(y)
            lobe.append((y, zc - 0.62 * hh))
        patch(s, lobe, bone_at, hullb)
        # eye-patch lens: pointed at both ends, (y -0.97, z+0.04) -> (y -0.72, z+0.10), ~0.10 tall, rising 12 deg
        lens = []
        for t in (0.0, 0.25, 0.5, 0.75, 1.0):
            y = -0.97 + 0.25 * t
            lens.append((y, Z0 + 0.04 + 0.06 * t + 0.055 * math.sin(math.pi * t)))
        for t in (0.75, 0.5, 0.25):
            y = -0.97 + 0.25 * t
            lens.append((y, Z0 + 0.04 + 0.06 * t - 0.045 * math.sin(math.pi * t)))
        patch(s, lens, "Head", hullb[:2])
    for y0, y1, bone, ew in ((0.12, 0.26, "Spine", 1.0), (0.24, 0.46, "Tail1", 0.30)):
        loft(B, y0, y1, SADDLE, bone, grow=0.008, zlo=-0.10, zhi=1.0, rnd=0.40, end_w=ew)          # saddle
    B.add((0, -0.76, hull(-0.76)[1] + hull(-0.76)[2] + 0.004), (0.035, 0.0125, 0.006), INK_D, "Head", studs=[],
          role="detail", bevel=0.004)                                                          # blowhole
    ANCH["Blow"] = (0, -0.76, hull(-0.76)[1] + hull(-0.76)[2] + 0.02)
    # ================= face: jade slit eyes seated just above the mouth corner
    for s in (1, -1):
        p, n = surf_hit(B, hullb[:2], (s * 1.0, -1.00, z - 0.05), (-s, 0, 0))
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
    for rot in ((0, 0, 0), (0, 0, 45)):                                                       # faceted jade orb
        B.add(ORB, (0.15, 0.15, 0.16), GLOW, "Esca", rot=rot, rnd=0.62, role="limb", studs=[], nostud=True,
              top=(0.92, 0.92), bot=(0.86, 0.86))
    B.add(ORB + Vector((0.05, -0.135, 0.06)), (0.026, 0.006, 0.026), HOT, "Esca", rot=(0, 0, 18), studs=[],
          role="detail", bevel=0.004)                                                          # glint facet
    B.spike(ORB + Vector((0, 0, -0.14)), (0, 0, -1), 0.08, 0.03, HOT, "Esca", studs=[], nostud=True,
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
        P = [Vector((s * x, y, z + 0.03)) for x, y in ((0.03, 0.82), (0.20, 0.92), (0.34, 1.00), (0.46, 1.12))]
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
    B.add((0, 0.97, z + 0.03), (0.035, 0.03, 0.028), INK, "Tail3", rnd=0.4)                   # notch root fill
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


HEAD_XF = []
