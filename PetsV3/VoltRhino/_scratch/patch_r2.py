import os
p = os.path.join(os.path.dirname(__file__), "..", "..", "pets", "VoltRhino.py")
s = open(p, encoding="utf-8").read()


def R(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:80])
    s = s.replace(a, b)


# M1 + M6 colours + NICE accent
R("IRON_D = (100, 108, 122)", "IRON_D = (92, 100, 116) ")
R("IRON = (172, 178, 190)", "IRON = (156, 164, 178)")
R("HORN_IVORY = (240, 236, 222)  # main horn + brow nub (smooth)",
  "HORN_IVORY = (232, 224, 204)  # main horn + brow nub (smooth, warm ivory)\n"
  "HORN_SHADE = (205, 198, 180)  # horn collars + growth rings")
R("VOLT = (210, 255, 80) ", "VOLT = (190, 255, 64) ")
# M4 pale
R('zhi=-0.54, grow=0.008, step=0.06)\n    Lb.band(B, sj, sy(0.80), PALE, "Spine", zlo=-1.0, zhi=-0.54,',
  'zhi=-0.46, grow=0.008, step=0.06)\n    Lb.band(B, sj, sy(0.80), PALE, "Spine", zlo=-1.0, zhi=-0.46,')
# M3 sloped armour + M2 fold wedges
R('''    Lb.band(B, sy(-0.90), sy(-0.08), IRON_D, "Chest", zlo=-0.22, grow=0.034, inset=0.02, step=0.08)
    Lb.band(B, sy(-0.14), sy(0.40), IRON_D, "Spine", zlo=0.28, grow=0.020, inset=0.02, step=0.08)
    Lb.band(B, sy(0.36), sy(0.93), IRON_D, "Spine", zlo=-0.16, grow=0.032, inset=0.02, step=0.08)
    # fold rims: heavy skin folds crossing the flank down to the belly at the shield's rear and the rump's front
    for y0, y1, bn, zl in ((-0.12, -0.05, "Chest", -0.44), (0.36, 0.43, "Spine", -0.40)):
        Lb.band(B, sy(y0), sy(y1), IRON_D, bn, zlo=zl, grow=0.050, inset=0.02, step=0.04)
    # withers hump over the shoulders (the top line peaks here)
''', '''    # (review 1 M3: every lower edge slopes - narrow1 sweeps the band edge between its front and rear height)
    for y0, y1, bn, f0, f1, g in ARMOUR:
        Lb.band(B, sy(y0), sy(y1), IRON_D, bn, zlo=f0, grow=g, inset=0.02, step=0.06,
                narrow1=arc_half(Lb, f1) / arc_half(Lb, f0))
    # fold wedges (review 1 M2): from the spine down the flank to a point at the belly line, proud 0.030 -> 0
    for y, bn in ((-0.065, "Chest"), (0.405, "Spine")):
        for s in (1, -1):
            fold_wedge(B, Lb, y, s, bn)
''')
# M7 rump bolts (after shoulder bolts)
R('''        zig(B, Q, VOLT, "Chest", 0.072)
''', '''        zig(B, Q, VOLT, "Chest", 0.072)
    # volt rump bolts on the rump plate (review 1 M7)
    for s in (1, -1):
        Q = []
        for y, a in ((0.50, 0.62), (0.63, 0.42), (0.57, 0.31), (0.74, 0.12)):
            Q.append(surf(Lb, y, a if s > 0 else math.pi - a, grow=armour_grow(Lb, y, a) + 0.004))
        zig(B, Q, VOLT, "Spine", 0.060)
''')
# M8 nasal ridge
R('''IRON_D, "Head", zlo=0.62, grow=0.022, inset=0.02, step=0.04)''',
  '''IRON_D, "Head", zlo=0.62, grow=0.012, inset=0.02, step=0.04)''')
# M7 eyes + M8 brow
R("d = (back * math.cos(math.radians(16)) + up * math.sin(math.radians(16))).normalized()",
  "d = (back * math.cos(math.radians(22)) + up * math.sin(math.radians(22))).normalized()")
R("((BLACK, (0.010, 0.032, 0.085), 0.004), (VOLT, (0.007, 0.016, 0.070), 0.010),",
  "((BLACK, (0.010, 0.034, 0.094), 0.004), (VOLT, (0.008, 0.018, 0.080), 0.010),")
R("        bc = p + up * 0.066 + n * 0.024 + d * 0.004", "        bc = p + up * 0.066 + n * 0.016 + d * 0.004")
R("B.add(bc, (0.034, 0.034, 0.112), IRON_D,", "B.add(bc, (0.040, 0.026, 0.096), IRON_D,")
# M5 ears
R('''    # ---------------- cupped tube ears at the poll, dark inner
    for s, side in ((1, "L"), (-1, "R")):
        root = Vector((s * 0.14, -0.98, 1.24))
        d = Vector((s * 0.40, 0.35, 1.0))
        B.spike(root, d, 0.27, 0.070, IRON, "Ear_" + side, top=(0.62, 0.42), studs=None, role="limb")
        B.spike(root + d.normalized() * 0.13 + Vector((0, -0.04, 0)), d, 0.13, 0.038, IRON_D, "Ear_" + side,
                top=(0.7, 0.3))''',
  '''    # ---------------- small dark ear flaps at the poll (review 1 M5), black inner
    for s, side in ((1, "L"), (-1, "R")):
        root = Vector((s * 0.14, -0.98, 1.18))
        d = Vector((s * 0.40, 0.35, 1.0))
        B.spike(root, d, 0.20, 0.064, IRON_D, "Ear_" + side, top=(0.55, 0.40), studs=None, role="limb")
        B.spike(root + d.normalized() * 0.09 + Vector((0, -0.035, 0)), d, 0.10, 0.034, BLACK, "Ear_" + side,
                top=(0.65, 0.3), nostud=True)''')
# M6 horn collars, growth rings, wider zig
R('''        zig(B, Q, VOLT, "Head", 0.050, thick=0.010)''', '''        zig(B, Q, VOLT, "Head", 0.060, thick=0.013)
    # horn collars over the segment seams + growth rings on the upper horn (review 1 M6 + NICE)
    for a, c, t, hw, hd, L in ((b0, h1, 0.17, 0.112, 0.118, 0.034), (h1, h2, 0.0, 0.090, 0.094, 0.030)):
        d = (c - a).normalized()
        m = a.lerp(c, t)
        B.seg(m - d * L / 2, m + d * L / 2, hw + 0.014, hd + 0.014, HORN_SHADE, "Head", side=(1, 0, 0),
              nostud=True, role="limb", rnd=0.35)
    for a, c, t, hw in ((h1, h2, 0.55, 0.090 * (1 - 0.26 * 0.55)), (h2, tip, 0.15, 0.068 * 0.87)):
        d = (c - a).normalized()
        m = a.lerp(c, t)
        B.seg(m - d * 0.011, m + d * 0.011, hw + 0.008, hw + 0.008, HORN_SHADE, "Head", side=(1, 0, 0),
              nostud=True, role="limb", rnd=0.35)''')
# NICE fore shin gaiter
R('''            B.add(P + Vector((0, 0.0, 0.015)), (0.160, 0.165, 0.075), IRON_D, foot, top=(0.84, 0.82), rnd=0.40)''',
  '''            if fb == "F":                                                                       # shin gaiter
                B.seg(K + dk * 0.22, K + dk * 0.30, 0.134, 0.139, IRON_D, shin, rnd=0.40, role="limb")
            B.add(P + Vector((0, 0.0, 0.015)), (0.160, 0.165, 0.075), IRON_D, foot, top=(0.84, 0.82), rnd=0.40)''')
# helpers
R('''def horn_pts():''', '''# armour plates (y0, y1, bone, lower-edge height fraction front, rear, grow): sloped bottoms (review 1 M3)
ARMOUR = [(-0.90, -0.08, "Chest", -0.26, -0.12, 0.034),     # shoulder shield (proud, overlaps the saddle)
          (-0.14, 0.40, "Spine", 0.34, 0.22, 0.020),        # saddle
          (0.36, 0.93, "Spine", -0.30, -0.02, 0.032)]       # rump plate


def arc_half(L, f):
    """half-angle (from the top) of a top band whose lower edge sits at height fraction f"""
    return math.pi / 2 - L.zang(f)


def armour_grow(L, y, a):
    """outer offset of the armour covering body point (y, section angle a on the +x side), 0 on bare hide"""
    g = 0.0
    for y0, y1, bn, f0, f1, gr in ARMOUR:
        if y0 <= y <= y1:
            t = (y - y0) / (y1 - y0)
            half = arc_half(L, f0) * (1 + (arc_half(L, f1) / arc_half(L, f0) - 1) * t)
            if abs(a - math.pi / 2) <= half:
                g = max(g, gr)
    return g


def fold_wedge(B, L, y, s, bone, f_end=-0.50, w=0.07, thick=0.030, n=6):
    """tapered skin-fold wedge from the spine down the flank to a point at height fraction f_end"""
    a0, a1 = math.pi / 2, L.zang(f_end)
    pts = []
    for i in range(n + 1):
        t = i / n
        a = a0 + (a1 - a0) * t
        th = thick * (1 - 0.75 * t)
        aa = a if s > 0 else math.pi - a
        p, nrm = surf(L, y, aa, grow=armour_grow(L, y, a) + th / 2)
        pts.append((p, nrm, w * (1 - 0.85 * t), th))
    for (p, nrm, wa, ta), (q, nq, wb, tb) in zip(pts, pts[1:]):
        B.seg(p, q, wa / 2, ta / 2, IRON_D, bone, side=(0, 1, 0), top=(wb / wa, tb / ta), ext=0.008, ext1=0.008,
              rnd=0.30, role="limb")


def horn_pts():''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
