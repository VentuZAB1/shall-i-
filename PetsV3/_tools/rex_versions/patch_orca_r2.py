# one-shot patch: Abyssal Orca review-2 fixes 1-7 (+ chin dash from 8). Run with plain python.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\AbyssalOrca.py"
s = open(p, encoding="utf-8").read()
R = []
# FIX 3 (+ melon) / FIX 5: stations
R.append(('''STATIONS = [(-1.30, 0.10, 0.085, -0.07), (-1.06, 0.19, 0.20, -0.03), (-0.82, 0.26, 0.28, 0.0),
            (-0.50, 0.30, 0.32, 0.01), (-0.14, 0.285, 0.31, 0.03), (0.20, 0.23, 0.265, 0.02),
            (0.50, 0.13, 0.19, 0.02), (0.80, 0.065, 0.10, 0.03), (0.88, 0.05, 0.075, 0.03)]''',
'''STATIONS = [(-1.30, 0.10, 0.085, -0.07), (-1.06, 0.19, 0.20, -0.03), (-0.94, 0.235, 0.25, 0.01),   # melon
            (-0.82, 0.26, 0.28, 0.0), (-0.50, 0.30, 0.32, 0.01), (-0.14, 0.285, 0.31, 0.03),
            (0.20, 0.23, 0.265, 0.02), (0.50, 0.13, 0.19, 0.02), (0.80, 0.065, 0.10, 0.03),
            (0.94, 0.03, 0.045, 0.03)]                    # review 2: the hull ends in a point (V notch)'''))
R.append(('''ROD = [Vector(p) for p in ((0, -0.94, 0.84), (0, -0.98, 1.10),''',
          '''ROD = [Vector(p) for p in ((0, -0.94, 0.875), (0, -0.98, 1.10),'''))
R.append(('''SADDLE = (150, 162, 194)''', '''SADDLE = (136, 146, 182)     # review 2: halfway between INK and WHITE'''))
# loft: matched rounding + separate start multipliers; new hseg (station-exact hull segs)
R.append(('''def loft(B, y0, y1, color, bone, grow=0.0, zlo=-1.0, zhi=1.0, ext1=0.0, scale0=1.0, end_w=1.0, xf=None, **kw):
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
                 **kw)''',
'''def loft(B, y0, y1, color, bone, grow=0.0, zlo=-1.0, zhi=1.0, ext1=0.0, scale0=1.0, end_w=1.0, xf=None, w0s=None,
         d0s=None, match=False, **kw):
    """hull section y0 -> y1: tapered rounded seg whose ends match the stations; zlo / zhi (fractions of the
    half-height) cut a horizontal band; grow pads it (shells); end_w narrows the far end (chevrons); xf maps points;
    w0s / d0s override scale0 per axis; match = the hull's corner radius (0.40 x min(hw, hh)) for flush shells"""
    pts = []
    for y in (y0, y1 + ext1):
        hw, zc, hh = hull(y)
        lo = zc + zlo * hh - (grow if zlo <= -1 else 0.0)
        hi = zc + zhi * hh + (grow if zhi >= 1 else 0.0)
        pts.append((Vector((0, y, (lo + hi) / 2)), hw + grow, (hi - lo) / 2))
    (p0, w0, d0), (p1, w1, d1) = pts
    if xf:
        p0, p1 = xf(p0), xf(p1)
    ws, ds = (w0s if w0s is not None else scale0), (d0s if d0s is not None else scale0)
    if match:
        hw, zc, hh = hull(y0)
        kw["rnd"] = min(0.9, 0.40 * min(hw, hh) / min(w0 * ws, d0 * ds))
    kw.setdefault("rnd", 0.40)
    return B.seg(p0, p1, w0 * ws, d0 * ds, color, bone, top=(w1 * end_w / (w0 * ws), d1 / (d0 * ds)), **kw)


def hseg(B, a, b, color, bone, zlo=-1.0, ext_far=0.05, ext_start=0.0):
    """review 2 FIX 3: one hull seg per station pair, from its BIG end `a` to `b` with the exact station dims; the far
    end is extended `ext_far` along the pair's own slope (buried in the next seg), never by reading hull() past it"""
    (ya, wa, ha, za), (yb, wb, hb, zb) = a, b
    t = 1.0 + ext_far / abs(yb - ya)
    yf, wf, hf, zf = (ya + (yb - ya) * t, wa + (wb - wa) * t, ha + (hb - ha) * t, za + (zb - za) * t)

    def band(w, h, zc):
        lo, hi = Z0 + zc + zlo * h, Z0 + zc + h
        return w, (lo + hi) / 2, (hi - lo) / 2
    w0, c0, d0 = band(wa, ha, za)
    w1, c1, d1 = band(wf, hf, zf)
    return B.seg((0, ya, c0), (0, yf, c1), w0, d0, color, bone, top=(w1 / w0, d1 / d0), rnd=0.40, ext=ext_start)'''))
# FIX 3: hull
R.append(('''    head_up = loft(B, -1.30, -0.80, INK, "Head", zlo=MOUTH_F, ext1=0.10)
    hullb = [head_up,
             loft(B, -0.86, -0.50, INK, "Chest", ext1=0.12, scale0=0.97),
             loft(B, -0.50, -0.05, INK, "Chest", ext1=0.12),
             loft(B, -0.12, 0.26, INK, "Spine", ext1=0.10, scale0=0.97),
             loft(B, 0.20, 0.50, INK, "Tail1", ext1=0.07, scale0=0.97),
             loft(B, 0.44, 0.79, INK, "Tail2", ext1=0.04, scale0=0.97),
             loft(B, 0.74, 0.88, INK, "Tail3", scale0=0.97)]''',
'''    S = STATIONS                     # review 2 FIX 3: exact stations, one seg per pair, big end first
    headb = [hseg(B, S[1], S[0], INK, "Head", zlo=MOUTH_F, ext_far=0.0),
             hseg(B, S[2], S[1], INK, "Head", zlo=MOUTH_F),
             hseg(B, S[3], S[2], INK, "Head", zlo=MOUTH_F)]
    bodyb = [hseg(B, S[4], S[3], INK, "Chest"),
             hseg(B, S[4], S[5], INK, "Chest", ext_start=0.05),
             hseg(B, S[5], S[6], INK, "Spine"),
             hseg(B, S[6], S[7], INK, "Tail1"),
             hseg(B, S[7], S[8], INK, "Tail2"),
             hseg(B, S[8], S[9], INK, "Tail3", ext_far=0.0)]
    hullb = headb + bodyb'''))
# FIX 8 chin dash
R.append(('''    B.seg(jawpt((0, -1.25, z - 0.125)), jawpt((0, -0.96, z - 0.145)), 0.12, 0.006, MOUTH, "Jaw", top=(1.6, 1),''',
          '''    B.seg(jawpt((0, -1.25, z - 0.125)), jawpt((0, -0.96, z - 0.145)), 0.09, 0.006, MOUTH, "Jaw", top=(1.3, 1),'''))
# belly band: matched rounding
R.append(('''        loft(B, y0, y1, WHITE, bone, grow=0.008, zlo=-1.0, zhi=zhi, ext1=e, end_w=0.85 if bone == "Tail1" else 1.0)''',
          '''        loft(B, y0, y1, WHITE, bone, grow=0.008, zlo=-1.0, zhi=zhi, ext1=e, end_w=0.85 if bone == "Tail1" else 1.0,
             match=True)'''))
# FIX 2: lobes as stepped shells; FIX 4: bigger lens; FIX 1: saddle
R.append(('''    for s in (1, -1):
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
        loft(B, y0, y1, SADDLE, bone, grow=0.008, zlo=-0.10, zhi=1.0, rnd=0.40, end_w=ew)          # saddle''',
'''    # flank lobes (review 2 FIX 2): 5 stepped, studded WHITE shells rising toward the back, split at Tail1
    for y0, y1, bone, zhi, ew in ((-0.04, 0.08, "Spine", -0.45, 1.0), (0.08, 0.18, "Spine", -0.25, 1.0),
                                  (0.18, 0.26, "Spine", -0.05, 1.0), (0.26, 0.36, "Tail1", 0.10, 0.92),
                                  (0.36, 0.42, "Tail1", 0.12, 0.55)):
        loft(B, y0, y1, WHITE, bone, grow=0.008, zlo=-1.0, zhi=zhi, ext1=0.02, end_w=ew, match=True)
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
    # saddle (FIX 1): flush 2-piece chevron with matched rounding, no visible joint (Tail1 piece buried 0.01)
    hwS = hull(0.26)[0]
    loft(B, 0.10, 0.26, SADDLE, "Spine", grow=0.010, zlo=-0.10, zhi=1.0, end_w=0.90, match=True)
    w_end = (hwS + 0.010) * 0.90
    hw25, zc25, hh25 = hull(0.25)
    hw26, zc26, hh26 = hull(0.26)
    d_end = ((zc26 + hh26 + 0.010) - (zc26 - 0.10 * hh26)) / 2
    d25 = ((zc25 + hh25 + 0.010) - (zc25 - 0.10 * hh25)) / 2
    loft(B, 0.25, 0.46, SADDLE, "Tail1", grow=0.010, zlo=-0.10, zhi=1.0, end_w=0.30, match=True,
         w0s=0.98 * w_end / (hw25 + 0.010), d0s=0.98 * d_end / d25)'''))
R.append(('''        p, n = surf_hit(B, hullb[:2], (s * 1.0, -1.00, z - 0.05), (-s, 0, 0))''',
          '''        p, n = surf_hit(B, headb, (s * 1.0, -1.00, z - 0.05), (-s, 0, 0))'''))
# FIX 6: teardrop orb + longer drip; glint on the new front face
R.append(('''    for rot in ((0, 0, 0), (0, 0, 45)):                                                       # faceted jade orb
        B.add(ORB, (0.15, 0.15, 0.16), GLOW, "Esca", rot=rot, rnd=0.62, role="limb", studs=[], nostud=True,
              top=(0.92, 0.92), bot=(0.86, 0.86))
    B.add(ORB + Vector((0.05, -0.135, 0.06)), (0.026, 0.006, 0.026), HOT, "Esca", rot=(0, 0, 18), studs=[],
          role="detail", bevel=0.004)                                                          # glint facet
    B.spike(ORB + Vector((0, 0, -0.14)), (0, 0, -1), 0.08, 0.03, HOT, "Esca", studs=[], nostud=True,
            top=(0.12, 0.12))                                                                  # drip tip''',
'''    for a in (0, 30, 60):                          # FIX 6: jade drop of light - smooth 12-sided body + lower cone
        B.add(ORB + Vector((0, 0, 0.04)), (0.15, 0.15, 0.11), GLOW, "Esca", rot=(0, 0, a), rnd=0.5, role="limb",
              studs=[], nostud=True, top=(0.90, 0.90))
        B.add(ORB - Vector((0, 0, 0.10)), (0.15, 0.15, 0.065), GLOW, "Esca", rot=(0, 0, a), rnd=0.5, role="limb",
              studs=[], nostud=True, bot=(0.40, 0.40))
    B.add(ORB + Vector((0.05, -0.151, 0.07)), (0.026, 0.006, 0.026), HOT, "Esca", rot=(0, 0, 18), studs=[],
          role="detail", bevel=0.004)                                                          # glint facet
    B.spike(ORB - Vector((0, 0, 0.165)), (0, 0, -1), 0.10, 0.035, HOT, "Esca", studs=[], nostud=True,
            top=(0.12, 0.12))                                                                  # drip tip'''))
# FIX 5: fluke V notch, no root knob
R.append(('''        P = [Vector((s * x, y, z + 0.03)) for x, y in ((0.03, 0.82), (0.20, 0.92), (0.34, 1.00), (0.46, 1.12))]''',
          '''        P = [Vector((s * x, y, z + 0.03)) for x, y in ((0.015, 0.82), (0.20, 0.92), (0.34, 1.00), (0.46, 1.12))]'''))
R.append(('''    B.add((0, 0.97, z + 0.03), (0.035, 0.03, 0.028), INK, "Tail3", rnd=0.4)                   # notch root fill
''', ''))
# FIX 7: octagonal lantern beads
R.append(('''    B.add(p + n * 0.006, (r, r, 0.012), GLOW, bone, R=R, studs=[], role="detail", rnd=0.6, nostud=True)''',
'''    from mathutils import Matrix
    for Rr in (R, R @ Matrix.Rotation(math.radians(45), 3, "Z")):      # FIX 7: two domes 45 deg apart = octagon
        B.add(p + n * 0.006, (r, r, 0.012), GLOW, bone, R=Rr, studs=[], role="detail", rnd=0.6, nostud=True)'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
