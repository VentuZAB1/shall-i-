import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
s = io.open(p, encoding="utf-8").read()
R = [
("    breath = [(0, 0), (28, 0), (45, -3), (62, 3), (80, -3), (98, 0), (120, 0)]   # f85 CM1: the guard breathes",
 "    breath = [(0, 0), (28, 0), (45, -5), (62, 5), (80, -5), (98, 0), (120, 0)]   # f85 CM1 / r2: the guard breathes +/-5"),
("roll=-2 * u - 2 * (2 * tr - 1) * u)   # f85 CM2: +/-2 deg with each beat",
 "roll=-2 * u - 3 * (2 * tr - 1) * u)   # f85 r2: +/-3 deg with each beat (was 2)"),
("l=-12 * tr * u, r=4 * u + 12 * tr * u)",
 "l=-12 * tr * u, r=4 * u + 20 * tr * u)"),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
s = s.replace("arc, troughs f45 / f80, peak f62; the body bobs 0.008)", "arc (r2: +/-5), troughs f45 / f80, peak f62; the body bobs 0.008)")
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
