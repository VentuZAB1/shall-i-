D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
src = D + r"\CoralCrusher\_scratch\model_v3.txt"
s = open(src, encoding="utf-8").read()
rep = [
# remove frontal teeth (read as pyramids on the forehead)
("""        rose_spike(B, Vector((s * 0.075, -0.538, 0.44)), (s * 0.15, -1.0, 0.35), 0.07, 0.026, "Spine")\n""", ""),
# eyes: bulb + narrow slit + a slate lid hooding each eye (15 deg inner-down)
("""        ep, en = surf_hit(B, [bulb], (s * 0.225, -1.0, 0.488), (0, 1, 0))
        crab_eye(B, ep + en * 0.002, s, en, eb, tilt=15, sc=1.2)""",
"""        ep, en = surf_hit(B, [bulb], (s * 0.222, -1.0, 0.486), (0, 1, 0))
        crab_eye(B, ep + en * 0.002, s, en, eb, tilt=15, sc=1.1)
        Rl = face_R(en) @ Euler((0, math.radians(-s * 18), 0), "XYZ").to_matrix()
        B.add(ep + en * 0.012 + Vector((s * 0.004, 0, 0.030)), (0.074, 0.024, 0.022), SHELL_D, eb, R=Rl,
              rnd=0.25, role="limb", studs=[], nostud=True)                                       # slate lid / brow"""),
# replace the two long brow bars by a low slate rostrum plate between the eyes (the brow plate the eyes sit in)
("""    for s in (1, -1):                                                                              # brow plate
        Rb = Euler((math.radians(-12), math.radians(-s * 15), 0), "XYZ").to_matrix()
        B.add(Vector((s * 0.14, -0.578, 0.552)), (0.13, 0.045, 0.024), SHELL_D, "Spine", R=Rb, rnd=0.3,
              role="limb", top=(0.92, 0.85))""",
"""    for s in (1, -1):                                                                              # brow plate
        Rb = Euler((math.radians(-8), math.radians(-s * 15), 0), "XYZ").to_matrix()
        B.add(Vector((s * 0.075, -0.548, 0.455)), (0.085, 0.030, 0.026), SHELL_D, "Spine", R=Rb, rnd=0.3,
              role="limb", top=(0.92, 0.85))"""),
# mandibles: two pale plates splayed into an open V (dark gap), ivory teeth on the inner edges
("""    B.add(Vector((0, -0.526, 0.33)), (0.092, 0.012, 0.042), MOUTH, "Spine", role="detail", bevel=0.004, studs=[])
    for s in (1, -1):
        B.add(Vector((s * 0.052, -0.540, 0.325)), (0.040, 0.014, 0.050), BELLY_PALE, "Mouth", rot=(6, 0, -s * 8),
              rnd=0.35, role="limb", nostud=True, bot=(0.8, 1.0))
        for z in (0.345, 0.310):
            B.spike(Vector((s * 0.016, -0.552, z)), (-s * 1.0, -0.2, -0.1), 0.020, 0.009, IVORY, "Mouth")""",
"""    B.add(Vector((0, -0.522, 0.335)), (0.085, 0.012, 0.045), MOUTH, "Spine", role="detail", bevel=0.004, studs=[])
    for s in (1, -1):
        B.add(Vector((s * 0.050, -0.548, 0.330)), (0.030, 0.012, 0.052), BELLY_PALE, "Mouth",
              rot=(8, s * 25, -s * 6), rnd=0.35, role="limb", nostud=True, bot=(0.75, 1.0))
        for z in (0.355, 0.315):
            B.spike(Vector((s * 0.024, -0.562, z)), (-s * 1.0, -0.3, -0.1), 0.020, 0.009, IVORY, "Mouth")"""),
# pincers: wider gap, longer fingers
("""        for bone, sgn, L1, L2, w0 in ((claw, -1, 0.17, 0.15, 0.080), (pin, 1, 0.18, 0.16, 0.074)):
            r0 = F + o * sgn * 0.072 * c - a * 0.06""",
"""        for bone, sgn, L1, L2, w0 in ((claw, -1, 0.20, 0.17, 0.080), (pin, 1, 0.21, 0.18, 0.074)):
            r0 = F + o * sgn * 0.085 * c - a * 0.06"""),
("""            B.seg(r0, m1, w0 * c, 0.064 * c, BRONZE, bone, side=out, ext1=0.02, top=(0.88, 0.80), rnd=0.40)
            B.seg(m1 - d1 * 0.03, m1 + d2 * L2 * 0.62 * c, w0 * 0.82 * c, 0.052 * c, SHELL_D, bone, side=out,""",
"""            B.seg(r0, m1, w0 * c, 0.054 * c, BRONZE, bone, side=out, ext1=0.02, top=(0.88, 0.80), rnd=0.40)
            B.seg(m1 - d1 * 0.03, m1 + d2 * L2 * 0.62 * c, w0 * 0.82 * c, 0.046 * c, SHELL_D, bone, side=out,"""),
("""                q = r0.lerp(m1, t) - o * sgn * 0.060 * c""", """                q = r0.lerp(m1, t) - o * sgn * 0.050 * c"""),
# legs: chunkier
("""            B.seg(H, K, 0.068, 0.088, SHELL_D, leg, side=(0, 0, 1), ext=0.05, ext1=0.03, top=(0.90, 0.86),""",
 """            B.seg(H, K, 0.074, 0.098, SHELL_D, leg, side=(0, 0, 1), ext=0.06, ext1=0.03, top=(0.90, 0.86),"""),
("""            B.add(K, (0.066, 0.066, 0.066), BRONZE, shin, rnd=0.42)                                   # knee
            B.seg(K, A, 0.054, 0.064, SHELL_D, shin, ext=0.025, ext1=0.01, top=(0.78, 0.78), rnd=0.38)  # propodus""",
 """            B.add(K, (0.072, 0.072, 0.072), BRONZE, shin, rnd=0.42)                                   # knee
            B.seg(K, A, 0.060, 0.070, SHELL_D, shin, ext=0.025, ext1=0.01, top=(0.76, 0.76), rnd=0.38)  # propodus"""),
]
for a, b in rep:
    if a not in s:
        print("MISSING", a[:80])
        continue
    s = s.replace(a, b)
open(src.replace("model_v3", "model_v4"), "w", encoding="utf-8").write(s)

p = D + r"\pets\CoralCrusher.py"
t = open(p, encoding="utf-8").read()
for a, b in (("""HIPZ = 0.31
LEGP = {1: (-32, (0.50, -0.20), (0.27, 0.50), (0.56, 0.085), (0.615, 0.015)),
        2: (0, (0.56, 0.04), (0.28, 0.51), (0.58, 0.085), (0.635, 0.015)),
        3: (32, (0.48, 0.28), (0.26, 0.49), (0.55, 0.085), (0.605, 0.015))}""",
              """HIPZ = 0.27
LEGP = {1: (-34, (0.50, -0.20), (0.30, 0.37), (0.53, 0.075), (0.60, 0.015)),
        2: (0, (0.56, 0.04), (0.31, 0.38), (0.55, 0.075), (0.62, 0.015)),
        3: (34, (0.48, 0.28), (0.29, 0.36), (0.52, 0.075), (0.59, 0.015))}"""),):
    if a not in t:
        print("MISSING2", a[:50])
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("ok")
