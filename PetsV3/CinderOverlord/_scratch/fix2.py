p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
t = open(p, encoding="utf-8").read()
rep = [
('''FRONT = [Vector(p) for p in ((0, -0.24, 0.207), (0, -0.47, 0.33), (0, -0.55, 0.64), (0, -0.54, 0.98),
                             (0, -0.47, 1.31), (0, -0.50, 1.60))]
FRAD = [0.230, 0.226, 0.212, 0.192, 0.172, 0.158]''',
 '''FRONT = [Vector(p) for p in ((0, -0.24, 0.221), (0, -0.48, 0.34), (0, -0.57, 0.62), (0, -0.56, 0.93),
                             (0, -0.49, 1.22), (0, -0.50, 1.50))]
FRAD = [0.230, 0.224, 0.205, 0.182, 0.162, 0.150]'''),
('''THROAT = Vector((0, -0.50, 1.60))''', '''THROAT = Vector((0, -0.50, 1.50))'''),
# rig updates
('''    k.joint("Jaw", (0, -0.56, 1.67), "Head", tail=(0, -0.35, -0.03))''',
 '''    k.joint("Jaw", (0, -0.55, 1.555), "Head", tail=(0, -0.35, -0.03))'''),
('''    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Arm_" + side, (s * 0.16, -0.60, 0.50), "Spine")
        h, e = ANCH.get("Claw_" + side, ((s * 0.22, -0.80, 0.32), (s * 0.24, -0.70, 0.40)))
        k.joint("Claw_" + side, e, "Arm_" + side, tail=tuple(Vector(h) - Vector(e)))''',
 '''    for s, side in ((1, "L"), (-1, "R")):
        h, e, sh = ANCH.get("Claw_" + side, ((s * 0.21, -0.88, 0.58), (s * 0.25, -0.78, 0.64),
                                             (s * 0.15, -0.68, 0.76)))
        k.joint("Arm_" + side, sh, "Neck1")
        k.joint("Claw_" + side, e, "Arm_" + side, tail=tuple(Vector(h) - Vector(e)))'''),
('''    out.append(((0, -0.56, 1.67), (0, -0.62, 1.67), 0.10, "Jaw"))''',
 '''    out.append(((0, -0.55, 1.555), (0, -0.61, 1.555), 0.10, "Jaw"))'''),
('''        out.append(((s * 0.16, -0.60, 0.50), (s * 0.16, -0.60, 0.50), 0.09, "Arm_" + side))
        out.append(((s * 0.24, -0.70, 0.40), (s * 0.24, -0.70, 0.40), 0.07, "Claw_" + side))''',
 '''        out.append(((s * 0.15, -0.68, 0.76), (s * 0.15, -0.68, 0.76), 0.09, "Arm_" + side))
        out.append(((s * 0.25, -0.78, 0.64), (s * 0.25, -0.78, 0.64), 0.07, "Claw_" + side))'''),
('''    B.bar(p0, p1, n, w, 0.010, ROSE, bone, studs=[], nostud=True, role="detail", bevel=0.004)
    B.bar(p0 + ax * L * 0.18 + n * 0.006, p1 - ax * L * 0.18 + n * 0.006, n, w * 0.36, 0.008, ROSE_H, bone,
          studs=[], nostud=True, role="detail", bevel=0.002)''',
 '''    B.bar(p0, p1, n, w, 0.012, ROSE, bone, studs=[], nostud=True, role="detail", bevel=0.004, top=(1, 0.55))
    B.bar(p0 + ax * L * 0.16 + n * 0.007, p1 - ax * L * 0.22 + n * 0.007, n, w * 0.38, 0.008, ROSE_H, bone,
          studs=[], nostud=True, role="detail", bevel=0.002)'''),
('''        B.seg(p - dv * 0.012, q + dv * 0.012, 0.022, t * 0.5 + 0.010, GOLD, bone, side=nrm.cross(dv),''',
 '''        B.seg(p - dv * 0.012, q + dv * 0.012, 0.019, t * 0.5 + 0.009, GOLD, bone, side=nrm.cross(dv),'''),
]
for a, b in rep:
    if a not in t:
        print("MISSING", a[:80])
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("ok")
