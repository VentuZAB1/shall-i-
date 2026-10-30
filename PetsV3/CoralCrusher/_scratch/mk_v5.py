D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
p = D + r"\pets\CoralCrusher.py"
t = open(p, encoding="utf-8").read()
rep = [
("""CLAW = (Vector((0.32, -0.40, 0.31)), Vector((0.56, -0.64, 0.42)), Vector((0.50, -0.85, 0.57)),
        Vector((0.44, -0.98, 0.86)))""",
 """CLAW = (Vector((0.32, -0.40, 0.31)), Vector((0.57, -0.62, 0.44)), Vector((0.50, -0.84, 0.58)),
        Vector((0.47, -1.04, 0.84)))"""),
("""    o = Vector((-s * 0.55, 0.0, 0.83))""", """    o = Vector((-s * 0.18, 0.0, 1.0))"""),
("""    def bar_on(pts, w, bone="Spine", color=SHELL_D, thick=0.010):""",
 """    def bar_on(pts, w, bone="Spine", color=SHELL_D, thick=0.007):"""),
("""            B.bar(a + na * 0.003 - d * 0.012, b + nb * 0.003 + d * 0.012, n, w, thick, color, bone, studs=[],
                  nostud=True, role="limb", rnd=0.15)""",
 """            B.bar(a + na * 0.002 - d * 0.012, b + nb * 0.002 + d * 0.012, n, w, thick, color, bone, studs=[],
                  nostud=True, role="detail", bevel=0.003)"""),
]
for a, b in rep:
    if a not in t:
        print("MISSING", a[:70])
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("ok")
