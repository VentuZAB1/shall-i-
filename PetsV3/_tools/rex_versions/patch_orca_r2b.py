# follow-up to patch_orca_r2: buried-shell + joint-groove fixes found in the first v3 render. Run with plain python.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\AbyssalOrca.py"
s = open(p, encoding="utf-8").read()
R = []
R.append(('''    pts = []
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
    kw.setdefault("rnd", 0.40)''',
'''    pts = []
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
    kw.setdefault("rnd", 0.40)'''))
R.append(('''def hseg(B, a, b, color, bone, zlo=-1.0, ext_far=0.05, ext_start=0.0):
    """review 2 FIX 3: one hull seg per station pair, from its BIG end `a` to `b` with the exact station dims; the far
    end is extended `ext_far` along the pair's own slope (buried in the next seg), never by reading hull() past it"""''',
'''def hseg(B, a, b, color, bone, zlo=-1.0, ext_far=0.0, ext_start=0.10):
    """review 2 FIX 3: one hull seg per station pair, from its BIG end `a` to `b` with the exact station dims. Joints:
    the rounded end faces recede ~0.4 x min(hw, hh), so instead of a short far-end extension every smaller seg runs
    `ext_start` BACK at its constant station size into its bigger neighbour (always inside it: the hull only shrinks
    away from the hump), covering the neighbour's receding end without any lip"""'''))
R.append(('''    headb = [hseg(B, S[1], S[0], INK, "Head", zlo=MOUTH_F, ext_far=0.0),
             hseg(B, S[2], S[1], INK, "Head", zlo=MOUTH_F),
             hseg(B, S[3], S[2], INK, "Head", zlo=MOUTH_F)]
    bodyb = [hseg(B, S[4], S[3], INK, "Chest"),
             hseg(B, S[4], S[5], INK, "Chest", ext_start=0.05),
             hseg(B, S[5], S[6], INK, "Spine"),
             hseg(B, S[6], S[7], INK, "Tail1"),
             hseg(B, S[7], S[8], INK, "Tail2"),
             hseg(B, S[8], S[9], INK, "Tail3", ext_far=0.0)]''',
'''    headb = [hseg(B, S[1], S[0], INK, "Head", zlo=MOUTH_F),
             hseg(B, S[2], S[1], INK, "Head", zlo=MOUTH_F),
             hseg(B, S[3], S[2], INK, "Head", zlo=MOUTH_F)]
    bodyb = [hseg(B, S[4], S[3], INK, "Chest", ext_start=0.0),            # the hump (max station) ...
             hseg(B, S[4], S[5], INK, "Chest", ext_start=0.08),           # ... covered from behind
             hseg(B, S[5], S[6], INK, "Spine"),
             hseg(B, S[6], S[7], INK, "Tail1"),
             hseg(B, S[7], S[8], INK, "Tail2"),
             hseg(B, S[8], S[9], INK, "Tail3")]'''))
R.append(('''        B.add(ORB + Vector((0, 0, 0.04)), (0.15, 0.15, 0.11), GLOW, "Esca", rot=(0, 0, a), rnd=0.5, role="limb",
              studs=[], nostud=True, top=(0.90, 0.90))
        B.add(ORB - Vector((0, 0, 0.10)), (0.15, 0.15, 0.065), GLOW, "Esca", rot=(0, 0, a), rnd=0.5, role="limb",
              studs=[], nostud=True, bot=(0.40, 0.40))''',
'''        B.add(ORB + Vector((0, 0, 0.04)), (0.15, 0.15, 0.11), GLOW, "Esca", rot=(0, 0, a), rnd=0.92, role="limb",
              studs=[], nostud=True, top=(0.90, 0.90))
        B.add(ORB - Vector((0, 0, 0.10)), (0.15, 0.15, 0.065), GLOW, "Esca", rot=(0, 0, a), rnd=0.92, role="limb",
              studs=[], nostud=True, bot=(0.40, 0.40))'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
