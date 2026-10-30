import re
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\FrostfangLynx.py"
s = open(p, encoding="utf-8").read()
def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (a[:60], s.count(a))
    s = s.replace(a, b)
# forehead specks out
rep('''    for s in (1, -1):                                                                       # forehead lines
        B.bar((s * 0.020, -0.690, 0.968), (s * 0.026, -0.640, 1.004), (0, -0.6, 0.8), 0.010, 0.004, BACK_SHADE,
              "Head", studs=[], bevel=0.002)
''', '')
# beard: ruff base block + a fan of chunky points
rep('''    for s in (1, -1):
        for y, z, d, L, w in ((-0.668, 0.838, (s * 0.30, 0.28, -0.91), 0.120, 0.036),
                              (-0.648, 0.862, (s * 0.55, 0.38, -0.74), 0.118, 0.036),
                              (-0.628, 0.892, (s * 0.80, 0.42, -0.43), 0.098, 0.032)):
            B.spike((s * 0.094, y, z), d, L, w, SNOW, "Head", top=(0.14, 0.40))
''', '''    for s in (1, -1):
        B.add((s * 0.086, -0.640, 0.846), (0.030, 0.048, 0.046), SNOW, "Head", rot=(-12, 0, s * 14), bot=(0.8, 0.7),
              rnd=0.40)                                                                     # ruff base (sideburn)
        for y, z, d, L, w in ((-0.668, 0.818, (s * 0.25, 0.30, -0.92), 0.090, 0.028),
                              (-0.645, 0.826, (s * 0.55, 0.45, -0.70), 0.096, 0.030),
                              (-0.622, 0.846, (s * 0.80, 0.55, -0.38), 0.088, 0.028),
                              (-0.612, 0.878, (s * 0.85, 0.50, -0.05), 0.070, 0.024)):
            B.spike((s * 0.096, y, z), d, L, w, SNOW, "Head", top=(0.22, 0.30))
''')
# front leg: less protrusion (block offset inward), spots on upper legs + shins collected
rep('''                B.seg(H + Vector((0, 0.01, 0.05)), K, 0.050, 0.074, WARM_SILVER, leg, ext=0.0, ext1=0.03,
                      top=(0.86, 0.70), rnd=0.45)''', '''                up = B.seg(H + Vector((-s * 0.008, 0.01, 0.03)), K, 0.047, 0.072, WARM_SILVER, leg, ext=0.0,
                           ext1=0.03, top=(0.88, 0.72), rnd=0.45)''')
rep('''                B.seg(K, A, 0.050, 0.056, WARM_SILVER, shin, top=(0.86, 0.86), ext=0.03, ext1=0.02, rnd=0.40)
                B.seg(A + Vector''', '''                lo = B.seg(K, A, 0.050, 0.056, WARM_SILVER, shin, top=(0.86, 0.86), ext=0.03, ext1=0.02, rnd=0.40)
                B.seg(A + Vector''')
rep('''                B.seg(H + Vector((0, 0.03, 0.06)), K, 0.068, 0.112, WARM_SILVER, leg, bot=(0.85, 1), top=(0.75, 0.62),
                      ext=0.0, ext1=0.03, rnd=0.45)
                B.seg(K, A, 0.050, 0.058, WARM_SILVER, shin, top=(0.82, 0.82), ext=0.03, ext1=0.02, rnd=0.40)''',
'''                up = B.seg(H + Vector((0, 0.03, 0.06)), K, 0.068, 0.112, WARM_SILVER, leg, bot=(0.85, 1),
                           top=(0.75, 0.62), ext=0.0, ext1=0.03, rnd=0.45)
                lo = B.seg(K, A, 0.050, 0.058, WARM_SILVER, shin, top=(0.82, 0.82), ext=0.03, ext1=0.02, rnd=0.40)''')
rep('''            B.add(Pw, (0.076, 0.088, 0.042), SNOW, foot, top=(0.86, 0.80), rnd=0.40)            # snowshoe paw''',
'''            LEGBLK.append((s, fb, up, lo))
            B.add(Pw, (0.076, 0.088, 0.042), SNOW, foot, top=(0.86, 0.80), rnd=0.40)            # snowshoe paw''')
rep('''    # ---------------- legs: rounded shoulders + thighs''', '''    LEGBLK = []
    # ---------------- legs: rounded shoulders + thighs''')
# leg spots + tail, replace the hook
rep('''                (rosette if ros else blob)(B, hips, s, ly, lz, r, sd + 201 + 7 * i, ang=a)
    B.build()
    if not nospots:
        _leg_spots(k, B)
    bk.stud_skin(k, PITCH)''', '''                (rosette if ros else blob)(B, hips, s, ly, lz, r, sd + 201 + 7 * i, ang=a)
        for s, fb, up, lo in LEGBLK:                         # spots down the legs (upper: 2, lower: 1)
            sd = (300 if fb == "F" else 400) + (0 if s > 0 else 50)
            if fb == "F":
                blob(B, up, s, 0.010, -0.040, 0.030, sd, el=1.1, ang=70)
                blob(B, up, s, -0.020, 0.060, 0.024, sd + 3, el=1.2, ang=20)
                blob(B, lo, s, 0.000, -0.050, 0.020, sd + 5, el=1.2, ang=80)
            else:
                rosette(B, up, s, 0.000, -0.050, 0.040, sd, ang=20)
                blob(B, up, s, 0.020, 0.060, 0.028, sd + 3, el=1.2, ang=60)
                blob(B, lo, s, 0.000, -0.040, 0.020, sd + 5, el=1.2, ang=80)
    # ---------------- short bobtail with a black tip band
    P = [Vector(p) for p in TAILP]
    for i, ((a, b), (w, d)) in enumerate(zip(zip(P, P[1:]), ((0.042, 0.052), (0.042, 0.048), (0.038, 0.042)))):
        B.seg(a, b, w, d, BLACK if i == 2 else WARM_SILVER, "Tail%d" % (i + 1), ext=0.03, top=(0.92, 0.92), rnd=0.40)
    B.build()
    bk.stud_skin(k, PITCH)''')
rep('''def _leg_spots(k, B):
    """(kept as a hook: leg spots are drawn as part of the blocks pass; nothing to add after build)"""
    return None


''', '')
open(p, "w", encoding="utf-8").write(s)
print("ok")
