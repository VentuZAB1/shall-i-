# one-shot patch: Hammerjaw review-2 fixes 1-6 (+ Slam anchor, front-teeth nudge). Run with plain python.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\HammerjawShark.py"
s = open(p, encoding="utf-8").read()
R = []
# ---- FIX 3: edge3 flush, tapered, 2 sub-segs per step, less red
R.append(('''def edge3(B, pts, bone, hw, hd, side, out=Vector()):
    """3-step coral leading edge along a polyline: CORAL_D (root) -> CORAL -> CORAL_HOT (tip), smooth rods"""
    P = [Vector(p) + out for p in pts]''',
'''def edge3(B, pts, bone, hw0, hw1, hd, side, out=Vector()):
    """3-step coral blade edge along a polyline, buried flush in the fin: CORAL_D (root 20 %) -> CORAL -> CORAL_HOT
    (tip); width across the fin tapers hw0 -> hw1 (<= 0.9 x the local fin half-thickness)"""
    P = [Vector(p) + out for p in pts]'''))
R.append(('''    for (u0, u1, c, tp) in ((0.0, 0.42, CORAL_D, (1, 1)), (0.40, 0.78, CORAL, (0.85, 0.85)),
                            (0.76, 1.0, CORAL_HOT, (0.25, 0.4))):
        n = 4
        for i in range(n):
            a, b = at(u0 + (u1 - u0) * i / n), at(u0 + (u1 - u0) * (i + 1) / n)
            if (b - a).length < 1e-4:
                continue
            B.seg(a, b, hw, hd, c, bone, side=side, ext=0.004, studs=[], nostud=True, role="limb",
                  top=tp if i == n - 1 else (1, 1))''',
'''    steps = ((0.0, 0.20, CORAL_D), (0.18, 0.80, CORAL), (0.78, 1.0, CORAL_HOT))
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
                  top=(0.25, 0.4) if last else (wb / wa, 1))'''))
R.append(('''    edge3(B, [R0 + c * 0.03, E1, T], bone, 0.022, thick * 0.95, n, out=-c.normalized() * 0.012)''',
          '''    edge3(B, [R0 + c * 0.03, E1, T], bone, 0.038, 0.018, 0.022, n)'''))
R.append(('''    edge3(B, [(0, -0.17, z + 0.23), (0, -0.04, z + 0.48), (0, 0.068, z + 0.672), (0, 0.152, z + 0.815)], "Spine",
          0.028, 0.02, (1, 0, 0), out=Vector((0, -0.008, 0.003)))''',
          '''    edge3(B, [(0, -0.17, z + 0.23), (0, -0.04, z + 0.48), (0, 0.068, z + 0.672), (0, 0.152, z + 0.815)], "Spine",
          0.040, 0.018, 0.02, (1, 0, 0))'''))
R.append(('''        edge3(B, lead, "Tail4", 0.02, 0.024, (1, 0, 0), out=Vector())''',
          '''        edge3(B, lead, "Tail4", 0.034, 0.016, 0.022, (1, 0, 0))
        lobes_axis.append((P, dims))'''))
R.append(('''    # caudal (Tail4): studded root, upper lobe 3 blocks curving up-back, lower lobe 2 blocks, coral leading edges''',
          '''    # caudal (Tail4): studded root, upper lobe 3 blocks curving up-back, lower lobe 2 blocks, coral leading edges
    lobes_axis = []'''))
# ---- FIX 6: notched trailing fill on the upper caudal lobe
R.append(('''    # notch near the upper-lobe tip (bite) - dark gap block flush on both faces
''', '''    # FIX 6 - upper caudal lobe trailing fill with one V bite notch (2nd notch in the silhouette)
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
'''))
R.append(('''    ANCHORS["Slam"] = (0, -1.03, z + 0.0)''', '''    ANCHORS["Slam"] = (0, -1.15, z + 0.03)'''))
R.append(('''    k.joint("Slam", ANCHORS.get("Slam", (0, -1.03, z)), "Head", tail=(0, 0, -0.15))''',
          '''    k.joint("Slam", ANCHORS.get("Slam", (0, -1.15, z + 0.03)), "Head", tail=(0, 0, -0.15))'''))
# ---- FIX 1 (belly shells kept) + FIX 4 (graduated lames, flatter, near-flush seams, fading coral, saddles)
R.append(('''    for y0, y1, bone, e in ((-0.84, -0.48, "Chest", 0.05), (-0.48, -0.16, "Chest", 0.02), (-0.22, 0.30, "Spine", 0.03),
                            (0.24, 0.62, "Tail1", 0.03), (0.56, 0.86, "Tail2", 0.0)):
        loft(B, y0, y1, BELLY, bone, grow=0.008, zlo=-1.0, zhi=-0.36, ext1=e, studs=None)''',
'''    belly = []
    for y0, y1, bone, e in ((-0.84, -0.48, "Chest", 0.05), (-0.48, -0.16, "Chest", 0.02), (-0.22, 0.30, "Spine", 0.03),
                            (0.24, 0.62, "Tail1", 0.03), (0.56, 0.86, "Tail2", 0.0)):
        belly.append(loft(B, y0, y1, BELLY, bone, grow=0.008, zlo=-1.0, zhi=-0.36, ext1=e, studs=None))'''))
R.append(('''    lames = [(-0.78, -0.60, "Chest"), (-0.565, -0.385, "Chest"), (-0.35, -0.17, "Chest"), (-0.135, 0.045, "Spine"),
             (0.08, 0.26, "Spine"), (0.295, 0.44, "Tail1")]''',
'''    lames = [(-0.80, -0.58, "Chest"), (-0.535, -0.345, "Chest"), (-0.305, -0.135, "Chest"),
             (-0.10, 0.05, "Spine"), (0.08, 0.21, "Spine"), (0.235, 0.345, "Spine")]   # graduated 0.22 -> 0.11'''))
R.append(('''        lb = loft(B, y0, y1, ARMOR, bone, grow=0.024, zlo=0.06, zhi=1.0, rnd=0.42)
        lame_blks.append(lb)
        for s in (1, -1):''',
'''        lb = loft(B, y0, y1, ARMOR, bone, grow=0.018, zlo=0.06, zhi=1.0, rnd=0.28)
        lame_blks.append(lb)
        for s in ((1, -1) if i >= 2 else ()):                    # lames 1-2: the gill slashes are the jagged edge'''))
R.append(('''                p0 = Vector((s * (hw + 0.018), y, zc + 0.06 * hd + 0.03))''',
          '''                p0 = Vector((s * (hw + 0.014), y, zc + 0.06 * hd + 0.03))'''))
# ---- FIX 2: keels seated through surface hits
R.append(('''        hw0, zc0, hd0 = hull(y0 + 0.02)
        hw1, zc1, hd1 = hull(y1 - 0.02)
        B.seg((0, y0 + 0.02, zc0 + hd0 + 0.04), (0, y1 - 0.02, zc1 + hd1 + 0.04), 0.026, 0.018, ARMOR, bone,
              ext=0.01, ext1=0.01, top=(0.9, 1))                                                         # keel''',
'''        strip(B, [lb], [(0, y0 + 0.03, 3.0), (0, (y0 + y1) / 2, 3.0), (0, y1 - 0.03, 3.0)], (0, 0, -1), 0.05, 0.035,
              ARMOR, bone, proud=0.027, nostud=False)                                              # keel (seated)'''))
R.append(('''        seams.append(loft(B, g0, g1, CORAL, bone, grow=0.013, zlo=0.08, zhi=1.0, rnd=0.30, studs=[],
                          nostud=True))                                                    # seam band''',
'''        col = CORAL_D if i == 4 else CORAL                         # coral heat fades toward the tail
        seams.append(loft(B, g0, g1, col, bone, grow=0.016, zlo=0.08, zhi=1.0, rnd=0.24, studs=[],
                          nostud=True))                                                    # seam band'''))
R.append(('''            loft(B, ym - 0.006, ym + 0.006, CORAL_HOT, bone, grow=0.017, zlo=0.10, zhi=1.0, rnd=0.30, studs=[],
                 nostud=True)''',
'''            loft(B, ym - 0.006, ym + 0.006, CORAL_HOT, bone, grow=0.0185, zlo=0.10, zhi=1.0, rnd=0.24, studs=[],
                 nostud=True)'''))
R.append(('''    # tail rings on Tail1-3 (smaller lames)
    for y, bone in ((0.54, "Tail1"), (0.75, "Tail2"), (0.93, "Tail3")):
        loft(B, y - 0.035, y + 0.035, ARMOR, bone, grow=0.014, rnd=0.40)''',
'''    # tail top saddles on Tail1-2 (no full rings: they read as hose clamps)
    for y, ln, bone in ((0.50, 0.10, "Tail1"), (0.72, 0.08, "Tail2")):
        loft(B, y - ln / 2, y + ln / 2, ARMOR, bone, grow=0.014, zlo=0.10, zhi=1.0, rnd=0.28)'''))
# ---- FIX 1: gills over the belly line, seated on the outermost surface
R.append(('''    gl = body[:2]''', '''    gl = body[:2] + belly[:2]'''))
R.append(('''            zt, zb = min(zc - 0.03 + h / 2, zc + 0.03), zc - 0.03 - h / 2''',
          '''            zt, zb = zc + 0.01, zc + 0.01 - h'''))
# ---- FIX 2: scars on lame 2 only, 6 hits, parallel, proud 0.004
R.append(('''    for j, (dy, ln) in enumerate(((0.0, 1.0), (0.055, 1.0), (0.11, 0.7))):
        pts = []
        for t in (0.0, 0.5, 1.0):
            t2 = t * ln
            y = -0.52 + dy + 0.16 * t2
            hw, zc, hd = hull(y)
            pts.append((1.0, y, zc + hd * (0.85 - 0.62 * t2)))
        strip(B, lame_blks[1:3] + seams[1:2], pts, (-1, 0, 0), 0.022, 0.008, SCAR, "Chest", proud=0.006, tip0=True,
              tip1=True)''',
'''    for j, (y0s, ln) in enumerate(((-0.52, 1.0), (-0.48, 1.0), (-0.44, 0.7))):
        pts = []
        for t in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
            t2 = t * ln
            y = y0s + 0.10 * t2
            hw, zc, hd = hull(y)
            pts.append((1.0, y, zc + hd * (0.88 - 0.60 * t2)))
        strip(B, lame_blks[1:2], pts, (-1, 0, 0), 0.022, 0.008, SCAR, "Chest", proud=0.004, tip0=True, tip1=True)'''))
# ---- FIX 5: crisp hammer, studless lead edges, 1.5x brow spikes, bigger eyes; head keel seated
R.append(('''    B.seg((0, -0.70, z + 0.05), (0, -1.00, z + 0.06), 0.20, 0.11, STEEL, "Head", top=(0.80, 0.85), rnd=0.35)
    hc = B.add((0, -1.025, z + 0.075), (0.17, 0.115, 0.06), STEEL, "Head", top=(0.9, 0.88), rnd=0.30)   # centre''',
'''    core = B.seg((0, -0.70, z + 0.05), (0, -1.00, z + 0.06), 0.20, 0.11, STEEL, "Head", top=(0.80, 0.85), rnd=0.35)
    hc = B.add((0, -1.025, z + 0.075), (0.17, 0.115, 0.06), STEEL, "Head", top=(0.9, 0.88), rnd=0.18)   # centre'''))
R.append(('''                           side=(0, 1, 0), top=(0.75, 0.75), rnd=0.32))                          # swept wing 14 deg''',
          '''                           side=(0, 1, 0), top=(0.75, 0.75), rnd=0.18))                          # swept wing 14 deg'''))
R.append(('''        B.seg((0, -1.128, z + 0.075), (s * 0.07, -1.162, z + 0.075), 0.03, 0.052, STEEL, "Head", side=(0, 1, 0),
              rnd=0.5, studs=[])
        B.seg((s * 0.07, -1.162, z + 0.075), (s * 0.42, -1.078, z + 0.075), 0.03, 0.05, STEEL, "Head",
              side=(0, 1, 0), rnd=0.5, top=(1, 0.8))''',
'''        B.seg((0, -1.128, z + 0.075), (s * 0.07, -1.162, z + 0.075), 0.03, 0.045, STEEL, "Head", side=(0, 1, 0),
              rnd=0.20, studs=[])
        B.seg((s * 0.07, -1.162, z + 0.075), (s * 0.42, -1.078, z + 0.075), 0.03, 0.045, STEEL, "Head",
              side=(0, 1, 0), rnd=0.20, top=(1, 0.8), studs=[])'''))
R.append(('''    B.add((0, -1.025, z + 0.149), (0.145, 0.09, 0.016), ARMOR, "Head", top=(0.95, 0.95))''',
          '''    helm = B.add((0, -1.025, z + 0.149), (0.145, 0.09, 0.016), ARMOR, "Head", top=(0.95, 0.95))'''))
R.append(('''    B.seg((0, -1.10, z + 0.178), (0, -0.78, z + 0.205), 0.026, 0.018, ARMOR, "Head", top=(1, 1))    # keel ridge''',
          '''    strip(B, [helm, core, lame_blks[0]], [(0, -1.10, 3.0), (0, -0.98, 3.0), (0, -0.86, 3.0), (0, -0.76, 3.0)],
          (0, 0, -1), 0.05, 0.035, ARMOR, "Head", proud=0.027, nostud=False)                    # keel ridge (seated)'''))
R.append(('''        fierce_eye(B, p + nn * 0.004, s, yaw=60, tilt=18, sc=1.4, brow_up=0.030, brow_out=-0.012)   # brow seated''',
          '''        fierce_eye(B, p + nn * 0.004, s, yaw=60, tilt=18, sc=1.6, brow_up=0.030, brow_out=-0.012)   # brow seated'''))
R.append(('''        B.add(b0 + d * 0.045, (0.035 * 0.42, 0.035, 0.045), ARMOR, "Head", R=bk.frame_from(b0, b0 + d, (1, 0, 0)),
              top=(0.62, 0.5), studs=[], role="limb")
        b1 = b0 + d * 0.075
        B.add(b1 + d * 0.035, (0.035 * 0.30, 0.035 * 0.52, 0.035), CORAL, "Head",
              R=bk.frame_from(b1, b1 + d, (1, 0, 0)), top=(0.30, 0.10), studs=[], nostud=True, role="limb")''',
'''        B.add(b0 + d * 0.065, (0.022, 0.05, 0.065), ARMOR, "Head", R=bk.frame_from(b0, b0 + d, (1, 0, 0)),
              top=(0.62, 0.5), studs=[], role="limb")
        b1 = b0 + d * 0.11
        B.add(b1 + d * 0.05, (0.016, 0.028, 0.05), CORAL, "Head",
              R=bk.frame_from(b1, b1 + d, (1, 0, 0)), top=(0.30, 0.10), studs=[], nostud=True, role="limb")'''))
# ---- FIX 7 (part): nudge the front three upper teeth out
R.append(('''            B.spike((s * (x + 0.006), y, z - 0.062), (s * 0.14, -0.05, -1), L, 0.018 if L > 0.045 else 0.016,
                    TEETH, "Head")''',
'''            dx = 0.016 if up.index((x, y, L)) < 3 else 0.006
            B.spike((s * (x + dx), y, z - 0.062), (s * 0.14, -0.05, -1), L, 0.018 if L > 0.045 else 0.016,
                    TEETH, "Head")'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:80]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
