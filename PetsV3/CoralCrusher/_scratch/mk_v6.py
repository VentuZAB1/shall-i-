D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
p = D + r"\pets\CoralCrusher.py"
t = open(p, encoding="utf-8").read()
rep = [
# eyes forward, out of the shell front
("""        base = Vector((s * 0.20, -0.49, 0.41))
        top = base + Vector((s * 0.02, -0.055, 0.07))
        B.seg(base, top, 0.044, 0.044, BRONZE, eb, ext=0.03, rnd=0.42, role="limb")              # stalk (0.07H)
        bulb = B.add(top + Vector((0, -0.012, 0.012)), (0.064, 0.050, 0.056), BRONZE, eb, rnd=0.45, role="limb")
        ep, en = surf_hit(B, [bulb], (s * 0.222, -1.0, 0.486), (0, 1, 0))""",
 """        base = Vector((s * 0.20, -0.525, 0.40))
        top = base + Vector((s * 0.02, -0.055, 0.07))
        B.seg(base, top, 0.044, 0.044, BRONZE, eb, ext=0.02, rnd=0.42, role="limb")              # stalk (0.07H)
        bulb = B.add(top + Vector((0, -0.016, 0.012)), (0.062, 0.046, 0.054), BRONZE, eb, rnd=0.45, role="limb")
        ep, en = surf_hit(B, [bulb], (s * 0.222, -1.0, 0.476), (0, 1, 0))"""),
("""        B.add(Vector((s * 0.066, -0.548, 0.455)), (0.068, 0.030, 0.026), SHELL_D, "Spine", R=Rb, rnd=0.3,""",
 """        B.add(Vector((s * 0.066, -0.560, 0.448)), (0.068, 0.030, 0.026), SHELL_D, "Spine", R=Rb, rnd=0.3,"""),
# claw base further forward / outward (elbow clear of the carapace corner)
("""CLAW = (Vector((0.32, -0.40, 0.31)), Vector((0.57, -0.62, 0.44)), Vector((0.50, -0.84, 0.58)),
        Vector((0.47, -1.04, 0.84)))""",
 """CLAW = (Vector((0.30, -0.46, 0.30)), Vector((0.60, -0.71, 0.44)), Vector((0.52, -0.92, 0.58)),
        Vector((0.49, -1.12, 0.84)))"""),
# joint zone defaults follow
("(s * 0.215, -0.50, 0.585)", "(s * 0.20, -0.525, 0.40)"),
("(s * 0.20, -0.49, 0.41)", "(s * 0.20, -0.525, 0.40)"),
]
for a, b in rep:
    if a not in t:
        print("MISSING", a[:80])
    t = t.replace(a, b)
t = t.replace("""0.585)), 0.07,""", """0.40)), 0.09,""")
t = t.replace("""0.41)), 0.07,""", """0.40)), 0.09,""")
open(p, "w", encoding="utf-8").write(t)
print("ok")
