import os
p = os.path.join(os.path.dirname(__file__), "..", "..", "pets", "IceMammoth.py")
s = open(p, encoding="utf-8").read()


def R(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


# M2 colours + NICE 2 tusk ice-ivory
R("CHAR_TEAL = (112, 152, 162)", "CHAR_TEAL = (96, 168, 184) ")
R("WOOL_D = (64, 84, 96)   ", "WOOL_D = (80, 110, 124) ")
R("TUSK_ICE = (238, 246, 250)", "TUSK_ICE = (226, 240, 246)")
# NICE 4: trunk lower, tip below the knee line, curling forward-up
R("TRUNK = [(0, -1.205, 1.07), (0, -1.255, 0.86), (0, -1.28, 0.665), (0, -1.275, 0.49), (0, -1.33, 0.355)]",
  "TRUNK = [(0, -1.205, 1.07), (0, -1.255, 0.86), (0, -1.28, 0.655), (0, -1.27, 0.455), (0, -1.32, 0.285)]")
R("TRUNK_TIP = (0, -1.43, 0.37)", "TRUNK_TIP = (0, -1.425, 0.30)")
# NICE 8: softer accordion steps
R("        sx, sy = w1[0] / w0[0] * 0.90, w1[1] / w0[1] * 0.90", "        sx, sy = w1[0] / w0[0] * 0.94, w1[1] / w0[1] * 0.94")
# NICE 3: rounder skull front
R('''    B.add((0, -1.02, 1.30), (0.215, 0.20, 0.26), CHAR_TEAL, "Head", top=(0.74, 0.70), bot=(0.88, 0.86), rnd=0.42)''',
  '''    B.add((0, -1.02, 1.30), (0.215, 0.20, 0.26), CHAR_TEAL, "Head", top=(0.74, 0.70), bot=(0.88, 0.86), rnd=0.55)''')
R('''    B.seg((0, -1.03, 1.52), (0, -1.205, 1.10), 0.175, 0.10, CHAR_TEAL, "Head", top=(0.82, 0.9), ext=0.03, rnd=0.40)''',
  '''    B.seg((0, -1.03, 1.52), (0, -1.205, 1.10), 0.175, 0.10, CHAR_TEAL, "Head", top=(0.82, 0.9), ext=0.03, rnd=0.55)''')
# M4: rounded wool clumps on the head dome
R('''        B.spike((x, y, z), (x * 2.5, -0.9 + dz, 1.0), L, 0.07, WOOL_D, "Head", top=(0.2, 0.4), studs=None,
                role="limb")''',
  '''        B.spike((x, y, z - 0.03), (x * 2.5, -0.9 + dz, 1.0), 0.08 + 0.03, 0.07, WOOL_D, "Head", top=(0.6, 0.6),
                studs=None, role="limb", rnd=0.45)                                      # rounded wool clump''')
# NICE 7 brows into the skull; M1 eyes bigger
R('''        B.add((s * 0.098, -1.198, 1.418), (0.108, 0.042, 0.036), WOOL_D, "Head", rot=(-14, -s * 22, 0),''',
  '''        B.add((s * 0.098, -1.188, 1.418), (0.108, 0.042, 0.036), WOOL_D, "Head", rot=(-14, -s * 22, 0),''')
R('''        B.add((s * 0.128, -1.186, 1.352), (0.068, 0.012, 0.027), DARK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.005)
        B.add((s * 0.130, -1.195, 1.352), (0.058, 0.008, 0.015), MINT, "Head", rot=rot, studs=[], role="detail",
              bevel=0.004)
        B.add((s * 0.138, -1.199, 1.354), (0.010, 0.004, 0.014), BLACK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.002)''',
  '''        B.add((s * 0.128, -1.186, 1.350), (0.082, 0.012, 0.030), DARK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.005)
        B.add((s * 0.130, -1.195, 1.350), (0.074, 0.008, 0.018), MINT, "Head", rot=rot, studs=[], role="detail",
              bevel=0.004)
        B.add((s * 0.140, -1.199, 1.352), (0.010, 0.004, 0.017), BLACK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.002)''')
# NICE 1: tusk socket ring WOOL_D, M1: 3 bolder cracks + a mint tip cap
R('''        B.seg(P[0] + d0 * 0.05, P[0] + d0 * 0.085, 0.086, 0.086, DARK, "Head", rnd=0.35, role="limb", nostud=True)''',
  '''        B.seg(P[0] + d0 * 0.05, P[0] + d0 * 0.085, 0.086, 0.086, WOOL_D, "Head", rnd=0.35, role="limb", nostud=True)''')
R('''        B.tube(tube_rings(C, R, 10), TUSK_ICE, "Head", nostud=True)
        for t in (0.62, 0.78):''',
  '''        B.tube(tube_rings(C, R, 10), TUSK_ICE, "Head", nostud=True)
        i0 = int(0.84 * (len(C) - 1))                                       # mint ice cap on the tusk tip
        B.tube(tube_rings(C[i0:], [r + 0.004 for r in R[i0:]], 10), MINT, "Head", nostud=True)
        for t in (0.55, 0.68, 0.79):''')
R('''                B.bar(u, v, ((u + v) / 2 - c).normalized(), 0.022, 0.007, MINT, "Head", studs=[], bevel=0.003)''',
  '''                B.bar(u, v, ((u + v) / 2 - c).normalized(), 0.035, 0.012, MINT, "Head", studs=[], bevel=0.004)''')
# M3: pale belly band a little higher
R('''    Lb.band(B, sy(-0.60), sj, BELLY_PALE, "Chest", zlo=-1.0, zhi=-0.70, grow=0.008, step=0.08)       # pale belly
    Lb.band(B, sj, sy(0.62), BELLY_PALE, "Spine", zlo=-1.0, zhi=-0.70, grow=0.008, step=0.08)''',
  '''    Lb.band(B, sy(-0.60), sj, BELLY_PALE, "Chest", zlo=-1.0, zhi=-0.60, grow=0.008, step=0.08)       # pale belly
    Lb.band(B, sj, sy(0.62), BELLY_PALE, "Spine", zlo=-1.0, zhi=-0.60, grow=0.008, step=0.08)''')
# NICE 6: two transverse teal ridge seams breaking the dark dorsal wool
R('''    # mane ridge tufts laid back along the spine (the shaggy hump silhouette)''',
  '''    for y in (-0.42, -0.06):
        Lb.band(B, sy(y) - 0.009, sy(y) + 0.009, CHAR_TEAL, "Chest" if y < SPLIT_Y else "Spine", zlo=0.46,
                grow=0.030, inset=0.02, step=0.009)
    # mane ridge tufts laid back along the spine (the shaggy hump silhouette)''')
# M4: spine tufts -> laid-back wool clumps
R('''    for y, L, ang, bn in ((-0.74, 0.15, 56, "Chest"), (-0.60, 0.17, 60, "Chest"), (-0.44, 0.18, 63, "Chest"),
                          (-0.28, 0.17, 66, "Chest"), (-0.12, 0.15, 68, "Chest"), (0.06, 0.14, 70, "Spine"),
                          (0.22, 0.12, 72, "Spine")):''',
  '''    for y, L, ang, bn in ((-0.74, 0.11, 60, "Chest"), (-0.58, 0.12, 64, "Chest"), (-0.42, 0.12, 66, "Chest"),
                          (-0.26, 0.12, 68, "Chest"), (-0.10, 0.11, 70, "Chest"), (0.07, 0.10, 72, "Spine"),
                          (0.23, 0.10, 74, "Spine")):''')
R('''        B.spike(top - Vector((0, 0, 0.05)), d, L + 0.05, 0.085, WOOL_D, bn, top=(0.25, 0.35), studs=None,
                role="limb")''',
  '''        B.spike(top - Vector((0, 0, 0.05)), d, L + 0.05, 0.085, WOOL_D, bn, top=(0.7, 0.7), studs=None,
                role="limb", rnd=0.45)                                                  # laid-back wool clump''')
# M3: shorter rows 2-3 (tips stop near z 0.64, the pale underside shows); NICE 5 more even row 2
R("    ROWS = ((0.40, 0.25, WOOL_D, 0.0), (0.02, 0.29, CHAR_TEAL, 0.5), (-0.38, 0.30, CHAR_TEAL, 0.0))",
  "    ROWS = ((0.40, 0.25, WOOL_D, 0.0, 0.16), (0.02, 0.20, CHAR_TEAL, 0.5, 0.08), (-0.38, 0.16, CHAR_TEAL, 0.0, 0.10))")
R("    for f, L, col, off in ROWS:", "    for f, L, col, off, var in ROWS:")
R("                ln = L * (1.0 + 0.16 * r)", "                ln = L * (1.0 + var * r)")
open(p, "w", encoding="utf-8").write(s)
print("patched")
