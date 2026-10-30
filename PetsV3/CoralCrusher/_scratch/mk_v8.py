p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
t = open(p, encoding="utf-8").read()
a = """        for y, L, w in ((-0.47, 0.095, 0.032), (-0.39, 0.12, 0.038), (-0.30, 0.13, 0.040), (-0.20, 0.125, 0.040),
                        (-0.10, 0.11, 0.036), (0.0, 0.09, 0.032)):"""
b = """        for y, L, w in ((-0.47, 0.095, 0.032), (-0.39, 0.12, 0.038), (-0.30, 0.13, 0.040), (-0.20, 0.125, 0.040),
                        (-0.10, 0.11, 0.036), (0.0, 0.095, 0.033), (0.11, 0.08, 0.030), (0.22, 0.065, 0.026)):"""
assert a in t
t = t.replace(a, b)
a2 = """    # ================= front: orbits + short thick eyestalks, rose slit eyes, slate V brow plate"""
b2 = """    # rose coral growths on the rear carapace (the game camera sees the back): short smooth branches
    for x, y, sc, rot in ((0.26, 0.20, 1.0, 20), (-0.20, 0.30, 0.85, -35), (0.06, 0.40, 0.7, 60)):
        p, n = surf_hit(B, [car], (x, y, 2.0), (0, 0, -1))
        B.add(p + n * 0.005, (0.045 * sc, 0.045 * sc, 0.022 * sc), ROSE_D, "Spine", R=face_R(-n, up=(0, 1, 0)),
              rnd=0.45, nostud=True)
        for bx, by, L, lean in ((0.0, 0.0, 0.11, 0.0), (0.03, 0.02, 0.08, 0.6), (-0.03, -0.01, 0.075, -0.6)):
            d = Vector((bx * 8 + lean * 0.5, by * 6, 1.0))
            d = Euler((0, 0, math.radians(rot)), "XYZ").to_matrix() @ d
            B.spike(p + Vector((bx, by, 0)) * sc, d, L * sc, 0.022 * sc, ROSE, "Spine", top=(0.45, 0.45),
                    nostud=True)
    # ================= front: orbits + short thick eyestalks, rose slit eyes, slate V brow plate"""
assert a2 in t
t = t.replace(a2, b2)
open(p, "w", encoding="utf-8").write(t)
print("ok")
