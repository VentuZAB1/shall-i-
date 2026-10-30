D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
p = D + r"\pets\CoralCrusher.py"
t = open(p, encoding="utf-8").read()
rep = [
("""        B.add(Vector((s * 0.075, -0.548, 0.455)), (0.085, 0.030, 0.026), SHELL_D, "Spine", R=Rb, rnd=0.3,""",
 """        B.add(Vector((s * 0.066, -0.548, 0.455)), (0.068, 0.030, 0.026), SHELL_D, "Spine", R=Rb, rnd=0.3,"""),
("""    cm.key_axis(k, "Pincer_" + side, f, out * s, pinch)""",
 """    cm.key_axis(k, "Pincer_" + side, f, out * s, -pinch)"""),
("""        out.append((ANCH.get("Eye_" + side, (s * 0.20, -0.49, 0.41)), ANCH.get("Eye_" + side, (s * 0.20, -0.49,
                                                                                                0.41)), 0.07,""",
 """        out.append((ANCH.get("Eye_" + side, (s * 0.20, -0.49, 0.41)), ANCH.get("Eye_" + side, (s * 0.20, -0.49,
                                                                                                0.41)), 0.09,"""),
("""    up = [(0, 0), (18, 1), (88, 1), (100, 0)]
    lift = [(0, 0), (18, 60), (26, 75), (33, 45), (40, 75), (47, 45), (54, 75), (62, 60), (72, 60), (88, 0), (100, 0)]
    for f in range(0, n + 1, 2):
        u = curve(up, f)
        k.key("Spine", f, rot=(-3 * u, 0, -2 * u), loc=(0, 0, 0.05 * u))
        claw(k, f, "R", lift=curve(lift, f), spread=10 * u, fore=-20 * u, wrist=15 * u)
        claw(k, f, "L", lift=-6 * u, fore=0)""",
 """    up = [(0, 0), (18, 1), (88, 1), (100, 0)]
    fore = [(0, 0), (18, 20), (26, 38), (33, 8), (40, 38), (47, 8), (54, 38), (62, 22), (72, 22), (88, 0), (100, 0)]
    for f in range(0, n + 1, 2):
        u = curve(up, f)
        k.key("Spine", f, rot=(-3 * u, 0, -2 * u), loc=(0, 0, 0.05 * u))
        claw(k, f, "R", lift=30 * u, spread=35 * u, fore=curve(fore, f), wrist=-10 * u)
        claw(k, f, "L", lift=-6 * u, fore=0)"""),
]
for a, b in rep:
    if a not in t:
        print("MISSING", a[:80])
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("ok")
