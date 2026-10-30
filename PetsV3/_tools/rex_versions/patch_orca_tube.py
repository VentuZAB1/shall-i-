# Abyssal Orca v3: hull + pattern shells as blockkit Tubes (smooth station-exact loft, flush bands). Plain python.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\AbyssalOrca.py"
s = open(p, encoding="utf-8").read()
R = []
# helpers after hseg()
R.append(('''def surf_hit(B, blks, origin, direction):
    import blockkit as bk
    from mathutils.bvhtree import BVHTree
    B._resolve()
    best = None
    d = Vector(direction).normalized()
    for blk in blks:
        bm = bk._box_bm(blk)''',
'''SE_N = 2.6                   # hull cross-section superellipse exponent (reads as a softly rounded box)
SEG = 32                     # points per full ring
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
        bm = bk.part_bm(blk)'''))
R.append(('''    B = bk.Blocks(k, seed=401, tier=5, plates=False)''',
          '''    B = bk.Blocks(k, seed=401, tier=5, plates=False, th=0.653)       # th: the v2 box hull (tubes are not boxes)'''))
R.append(('''    S = STATIONS                     # review 2 FIX 3: exact stations, one seg per pair, big end first
    headb = [hseg(B, S[1], S[0], INK, "Head", zlo=MOUTH_F),
             hseg(B, S[2], S[1], INK, "Head", zlo=MOUTH_F),
             hseg(B, S[3], S[2], INK, "Head", zlo=MOUTH_F)]
    bodyb = [hseg(B, S[4], S[3], INK, "Chest", ext_start=0.0),            # the hump (max station) ...
             hseg(B, S[4], S[5], INK, "Chest", ext_start=0.08),           # ... covered from behind
             hseg(B, S[5], S[6], INK, "Spine"),
             hseg(B, S[6], S[7], INK, "Tail1"),
             hseg(B, S[7], S[8], INK, "Tail2"),
             hseg(B, S[8], S[9], INK, "Tail3")]
    hullb = headb + bodyb
    # throat under the head behind the jaw (the jaw hinge is at y -0.94)
    loft(B, -0.96, -0.80, WHITE, "Head", zlo=-1.0, zhi=MOUTH_F, grow=0.010)   # clear of the chest seg's buried end''',
'''    # review 2 FIX 3, done as smooth station-exact tubes (one per bone, flush overlapping joints - no seg creases)
    headb = [hull_tube(B, -1.30, -0.80 + OV, INK, "Head", zlo=MOUTH_F, j1=-0.80)]
    bodyb = [hull_tube(B, -0.80 - OV, -0.05 + OV, INK, "Chest", j0=-0.80, j1=-0.05),
             hull_tube(B, -0.05 - OV, 0.26 + OV, INK, "Spine", j0=-0.05, j1=0.26),
             hull_tube(B, 0.26 - OV, 0.50 + OV, INK, "Tail1", j0=0.26, j1=0.50),
             hull_tube(B, 0.50 - OV, 0.79 + OV, INK, "Tail2", j0=0.50, j1=0.79),
             hull_tube(B, 0.79 - OV, 0.94, INK, "Tail3", j0=0.79)]
    hullb = headb + bodyb
    # throat under the head behind the jaw (the jaw hinge is at y -0.94): the part below the mouth line
    hull_tube(B, -0.97, -0.80 + OV, WHITE, "Head", zhi=MOUTH_F, grow=0.004, j1=-0.80)'''))
R.append(('''    for y0, y1, bone, zhi, e in ((-0.86, -0.50, "Chest", -0.42, 0.05), (-0.50, -0.05, "Chest", -0.52, 0.03),
                                 (-0.12, 0.26, "Spine", -0.62, 0.03), (0.20, 0.50, "Tail1", -0.70, 0.0)):
        loft(B, y0, y1, WHITE, bone, grow=0.008, zlo=-1.0, zhi=zhi, ext1=e, end_w=0.85 if bone == "Tail1" else 1.0,
             match=True)''',
'''    # belly band: one smooth white line per bone, falling toward the tail (under the lobes: grow 0.0075)
    for y0, y1, bone, zh0, zh1, g in ((-0.82, -0.05 + 0.02, "Chest", -0.42, -0.55, 0.0075),
                                      (-0.05, 0.26 + 0.02, "Spine", -0.55, -0.62, 0.0072),
                                      (0.26, 0.50, "Tail1", -0.62, -0.72, 0.0070)):
        band(B, y0, y1, WHITE, bone, zhi=zh0, zhi1=zh1, grow=g)'''))
R.append(('''    for y0, y1, bone, zhi, ew in ((-0.04, 0.08, "Spine", -0.45, 1.0), (0.08, 0.18, "Spine", -0.25, 1.0),
                                  (0.18, 0.26, "Spine", -0.05, 1.0), (0.26, 0.36, "Tail1", 0.10, 0.92),
                                  (0.36, 0.42, "Tail1", 0.12, 0.55)):
        loft(B, y0, y1, WHITE, bone, grow=0.008, zlo=-1.0, zhi=zhi, ext1=0.02, end_w=ew, match=True)''',
'''    for i, (y0, y1, bone, zhi, zhi1) in enumerate(((-0.04, 0.10, "Spine", -0.45, -0.45),
                                                   (0.08, 0.20, "Spine", -0.25, -0.25),
                                                   (0.18, 0.26, "Spine", -0.05, -0.05),
                                                   (0.26, 0.38, "Tail1", 0.10, 0.10),
                                                   (0.36, 0.46, "Tail1", 0.12, -0.55))):    # the tongue's point
        band(B, y0, y1, WHITE, bone, zhi=zhi, zhi1=zhi1, grow=0.008 + 0.0003 * i)'''))
R.append(('''    # saddle (FIX 1): flush 2-piece chevron with matched rounding, no visible joint (Tail1 piece buried 0.01)
    hwS = hull(0.26)[0]
    loft(B, 0.10, 0.26, SADDLE, "Spine", grow=0.010, zlo=-0.10, zhi=1.0, end_w=0.90, match=True)
    w_end = (hwS + 0.010) * 0.90
    hw25, zc25, hh25 = hull(0.25)
    hw26, zc26, hh26 = hull(0.26)
    d_end = ((zc26 + hh26 + 0.010) - (zc26 - 0.10 * hh26)) / 2
    d25 = ((zc25 + hh25 + 0.010) - (zc25 - 0.10 * hh25)) / 2
    loft(B, 0.25, 0.46, SADDLE, "Tail1", grow=0.010, zlo=-0.10, zhi=1.0, end_w=0.30, match=True,
         w0s=0.98 * w_end / (hw25 + 0.010), d0s=0.98 * d_end / d25)''',
'''    # saddle (FIX 1): a flush 2-piece chevron on the back (Spine piece hidden under the dorsal's trailing root,
    # Tail1 piece 0.0005 under it in the 0.01 overlap), narrowing to a point toward the tail
    band(B, 0.10, 0.26, SADDLE, "Spine", zlo=-0.10, grow=0.010, narrow1=0.90)
    band(B, 0.25, 0.46, SADDLE, "Tail1", zlo=-0.10 + 0.10 * 0.0, grow=0.0095, narrow1=0.10)'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
