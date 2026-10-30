p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
t = open(p, encoding="utf-8").read()
rep = [
("""def oval(c, side, upv, rw, rh, a0=0.0, a1=2 * math.pi, seg=18, n=2.2, off=0.0):""",
 """def oval(c, side, upv, rw, rh, a0=0.0, a1=2 * math.pi, seg=16, n=2.2, off=0.0):"""),
("""def band(B, a, b, r0, r1, bone, color, a0, a1, off=0.012, thick=0.02, up=(0, 0, 1), seg=10, flat=0.92, nr=3,""",
 """def band(B, a, b, r0, r1, bone, color, a0, a1, off=0.012, thick=0.02, up=(0, 0, 1), seg=8, flat=0.92, nr=2,"""),
("""             math.radians(8), math.radians(172), off=0.011, thick=0.026, up=up, seg=14, nostud=False)""",
 """             math.radians(8), math.radians(172), off=0.011, thick=0.026, up=up, seg=12, nostud=False)"""),
("""        scutes(a, b, RAD[i], RAD[i + 1], bone, 212, 328)""",
 """        scutes(a, b, RAD[i], RAD[i + 1], bone, 212, 328, ts=((0.04, 0.44), (0.52, 0.94)))"""),
("""FRONT = [Vector(p) for p in ((0, -0.24, 0.221), (0, -0.48, 0.34), (0, -0.57, 0.62), (0, -0.56, 0.93),
                             (0, -0.49, 1.22), (0, -0.50, 1.50))]""",
 """FRONT = [Vector(p) for p in ((0, -0.24, 0.221), (0, -0.48, 0.34), (0, -0.58, 0.60), (0, -0.57, 0.89),
                             (0, -0.50, 1.16), (0, -0.50, 1.42))]"""),
("""HEAD_XF = []""",
 """HEAD_XF = [((0, -0.50, 1.50), 1.15, ["Head", "Jaw", "Mouth", "Crown_1", "Crown_2", "Crown_3", "Crown_4",
                                      "Crown_5"], (0, 0, -0.08))]     # head group built at 1.0, shown 15 % bigger"""),
]
for a, b in rep:
    if a not in t:
        print("MISSING", a[:80])
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("ok")
