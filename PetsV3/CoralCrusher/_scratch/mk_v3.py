src = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher\_scratch\model_v2.txt"
s = open(src, encoding="utf-8").read()
rep = [
("""            B.bar(a + na * 0.003, b + nb * 0.003, n, w, thick, color, bone, studs=[], nostud=True, role="limb",
                  rnd=0.3, ext=0.0)""",
 """            d = (b - a).normalized()
            B.bar(a + na * 0.003 - d * 0.012, b + nb * 0.003 + d * 0.012, n, w, thick, color, bone, studs=[],
                  nostud=True, role="limb", rnd=0.15)"""),
('def bar_on(pts, w, bone="Spine", color=SHELL_D, thick=0.014):',
 'def bar_on(pts, w, bone="Spine", color=SHELL_D, thick=0.010):'),
("bar_on([(0, -0.46), (0, -0.37), (0, -0.28), (0, -0.19), (0, -0.11)], 0.055)",
 "bar_on([(0, -0.46), (0, -0.37), (0, -0.28), (0, -0.19), (0, -0.11)], 0.062)"),
("(0.44, 0.08)], 0.048)", "(0.44, 0.08)], 0.056)"),
("(s * 0.11, 0.40)], 0.042)", "(s * 0.11, 0.40)], 0.050)"),
('rose_spike(B, Vector((s * 0.075, -0.538, 0.53)), (s * 0.15, -1.0, 0.35), 0.07, 0.026, "Spine")',
 'rose_spike(B, Vector((s * 0.075, -0.538, 0.44)), (s * 0.15, -1.0, 0.35), 0.07, 0.026, "Spine")'),
("""        base = Vector((s * 0.20, -0.49, 0.50))
        top = base + Vector((s * 0.02, -0.06, 0.075))
        B.add(Vector((s * 0.20, -0.505, 0.50)), (0.068, 0.03, 0.05), BLACK, "Spine", role="detail", bevel=0.012,
              studs=[])                                                                             # orbit
        B.seg(base, top, 0.042, 0.042, BRONZE, eb, ext=0.03, rnd=0.42, role="limb")              # stalk (0.07H)
        bulb = B.add(top + Vector((0, -0.012, 0.012)), (0.060, 0.046, 0.052), BRONZE, eb, rnd=0.45, role="limb")
        ep, en = surf_hit(B, [bulb], (s * 0.225, -1.0, 0.585), (0, 1, 0))
        crab_eye(B, ep + en * 0.002, s, en, eb, tilt=15, sc=1.15)""",
"""        base = Vector((s * 0.20, -0.49, 0.41))
        top = base + Vector((s * 0.02, -0.055, 0.07))
        B.seg(base, top, 0.044, 0.044, BRONZE, eb, ext=0.03, rnd=0.42, role="limb")              # stalk (0.07H)
        bulb = B.add(top + Vector((0, -0.012, 0.012)), (0.064, 0.050, 0.056), BRONZE, eb, rnd=0.45, role="limb")
        ep, en = surf_hit(B, [bulb], (s * 0.225, -1.0, 0.488), (0, 1, 0))
        crab_eye(B, ep + en * 0.002, s, en, eb, tilt=15, sc=1.2)"""),
("""        B.add(Vector((s * 0.135, -0.565, 0.638)), (0.13, 0.045, 0.024), SHELL_D, "Spine", R=Rb, rnd=0.3,""",
 """        B.add(Vector((s * 0.14, -0.578, 0.552)), (0.13, 0.045, 0.024), SHELL_D, "Spine", R=Rb, rnd=0.3,"""),
("""    B.add(Vector((0, -0.528, 0.405)), (0.10, 0.012, 0.048), MOUTH, "Spine", role="detail", bevel=0.004, studs=[])
    for s in (1, -1):
        B.add(Vector((s * 0.058, -0.548, 0.405)), (0.046, 0.016, 0.062), BELLY_PALE, "Mouth", rot=(6, 0, -s * 8),
              rnd=0.35, role="limb", nostud=True, bot=(0.8, 1.0))
        for z in (0.44, 0.405, 0.37):
            B.spike(Vector((s * 0.014, -0.56, z)), (-s * 1.0, -0.2, -0.1), 0.026, 0.010, IVORY, "Mouth")
    ANCH["Mouth"] = (0, -0.58, 0.41)""",
"""    B.add(Vector((0, -0.526, 0.33)), (0.092, 0.012, 0.042), MOUTH, "Spine", role="detail", bevel=0.004, studs=[])
    for s in (1, -1):
        B.add(Vector((s * 0.052, -0.540, 0.325)), (0.040, 0.014, 0.050), BELLY_PALE, "Mouth", rot=(6, 0, -s * 8),
              rnd=0.35, role="limb", nostud=True, bot=(0.8, 1.0))
        for z in (0.345, 0.310):
            B.spike(Vector((s * 0.016, -0.552, z)), (-s * 1.0, -0.2, -0.1), 0.020, 0.009, IVORY, "Mouth")
    ANCH["Mouth"] = (0, -0.57, 0.33)"""),
("""        P0 = W - a * 0.03
        palm = B.seg(P0, F, 0.118 * c, 0.170 * c, BRONZE, claw, side=out, top=(0.92, 0.86), rnd=0.45)""",
"""        P0 = W - a * 0.03
        rings = []
        for t, wx, wo in ((0.0, 0.070, 0.095), (0.10, 0.098, 0.140), (0.32, 0.118, 0.172), (0.58, 0.120, 0.172),
                          (0.82, 0.108, 0.152), (1.0, 0.088, 0.128)):
            cc = P0.lerp(F, t)
            rg = []
            for q in range(20):
                ang = 2 * math.pi * q / 20
                cs, sn = math.cos(ang), math.sin(ang)
                rg.append(cc + out * (wx * c * math.copysign(abs(cs) ** (2 / 2.3), cs)) +
                          o * (wo * c * math.copysign(abs(sn) ** (2 / 2.3), sn)))
            rings.append(rg)
        palm = B.tube(rings, BRONZE, claw)                                                          # oval palm"""),
("""        for bone, sgn, Lf, w0 in ((claw, -1, 0.28, 0.080), (pin, 1, 0.30, 0.074)):
            r0 = F + o * sgn * 0.085 * c - a * 0.05
            dirf = (a - o * sgn * 0.22).normalized()
            tip = r0 + dirf * Lf * c
            B.seg(r0, r0.lerp(tip, 0.66), w0 * c, 0.062 * c, BRONZE, bone, side=out, top=(0.82, 0.74),
                  rnd=0.40)
            m = r0.lerp(tip, 0.60)
            B.seg(m, m.lerp(tip, 0.78), w0 * 0.70 * c, 0.046 * c, SHELL_D, bone, side=out, top=(0.70, 0.70),
                  rnd=0.35, role="limb")
            B.spike(m.lerp(tip, 0.66), dirf, (tip - m).length * 0.50, w0 * 0.42 * c, BLACK, bone, side=out)
            for t in (0.28, 0.52):                                                                  # crusher molars
                q = r0.lerp(tip, t) - o * sgn * 0.058 * c
                B.add(q, (0.026 * c, 0.020 * c, 0.018 * c), SHELL_D, bone, R=bk.frame_from(r0, tip, out),
                      role="detail", bevel=0.005, studs=[])
            if bone == pin:""",
"""        for bone, sgn, L1, L2, w0 in ((claw, -1, 0.17, 0.15, 0.080), (pin, 1, 0.18, 0.16, 0.074)):
            r0 = F + o * sgn * 0.072 * c - a * 0.06
            d1 = (a - o * sgn * 0.06).normalized()
            m1 = r0 + d1 * L1 * c
            d2 = (a - o * sgn * 0.48).normalized()
            tip = m1 + d2 * L2 * c
            B.seg(r0, m1, w0 * c, 0.064 * c, BRONZE, bone, side=out, ext1=0.02, top=(0.88, 0.80), rnd=0.40)
            B.seg(m1 - d1 * 0.03, m1 + d2 * L2 * 0.62 * c, w0 * 0.82 * c, 0.052 * c, SHELL_D, bone, side=out,
                  top=(0.72, 0.70), rnd=0.35, role="limb")
            B.spike(m1 + d2 * L2 * 0.50 * c, d2, L2 * 0.55 * c, w0 * 0.45 * c, BLACK, bone, side=out)
            for t in (0.35, 0.75):                                                                  # crusher molars
                q = r0.lerp(m1, t) - o * sgn * 0.060 * c
                B.add(q, (0.028 * c, 0.022 * c, 0.018 * c), SHELL_D, bone, R=bk.frame_from(r0, m1, out),
                      role="detail", bevel=0.005, studs=[])
            if bone == pin:"""),
("""                rose_spike(B, r0.lerp(tip, 0.30) + o * 0.06 * c, o + a * 0.7, 0.07 * c, 0.024 * c, pin)""",
 """                rose_spike(B, r0.lerp(m1, 0.55) + o * 0.06 * c, o + a * 0.7, 0.075 * c, 0.026 * c, pin)"""),
("""            B.add(H, (0.066, 0.066, 0.055), SHELL_D, leg, rnd=0.42)                                  # coxa
            B.seg(H, K, 0.056, 0.078, SHELL_D, leg, side=(0, 0, 1), ext=0.05, ext1=0.025, top=(0.90, 0.85),
                  rnd=0.40)                                                                         # merus (flat)
            B.add(K, (0.058, 0.058, 0.058), BRONZE, shin, rnd=0.42)                                   # knee
            B.seg(K, A, 0.046, 0.056, SHELL_D, shin, ext=0.02, ext1=0.01, top=(0.80, 0.80), rnd=0.38)  # propodus
            B.seg(A, T, 0.034, 0.036, SHELL_D, foot, ext=0.02, top=(0.7, 0.7), rnd=0.3)              # dactyl""",
"""            B.add(H, (0.072, 0.072, 0.062), SHELL_D, leg, rnd=0.42)                                  # coxa
            B.seg(H, K, 0.068, 0.088, SHELL_D, leg, side=(0, 0, 1), ext=0.05, ext1=0.03, top=(0.90, 0.86),
                  rnd=0.40)                                                                         # merus (flat)
            B.add(K, (0.066, 0.066, 0.066), BRONZE, shin, rnd=0.42)                                   # knee
            B.seg(K, A, 0.054, 0.064, SHELL_D, shin, ext=0.025, ext1=0.01, top=(0.78, 0.78), rnd=0.38)  # propodus
            B.seg(A, T, 0.038, 0.040, SHELL_D, foot, ext=0.02, top=(0.7, 0.7), rnd=0.3)              # dactyl"""),
]
for a, b in rep:
    if a not in s:
        print("MISSING", a[:70])
        continue
    s = s.replace(a, b)
open(src.replace("model_v2", "model_v3"), "w", encoding="utf-8").write(s)

p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
t = open(p, encoding="utf-8").read()
for a, b in (('k.joint("Spine", (0, -0.05, 0.47), "Root"', 'k.joint("Spine", (0, -0.05, 0.38), "Root"'),
             ('k.joint("Mouth", (0, -0.54, 0.46), "Spine"', 'k.joint("Mouth", (0, -0.535, 0.375), "Spine"'),
             ('out.append(((0, -0.54, 0.46), (0, -0.54, 0.38), 0.07, "Mouth"))',
              'out.append(((0, -0.535, 0.375), (0, -0.535, 0.29), 0.07, "Mouth"))'),
             ('(s * 0.215, -0.50, 0.585)', '(s * 0.20, -0.49, 0.41)')):
    if a not in t:
        print("MISSING2", a)
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("ok")
