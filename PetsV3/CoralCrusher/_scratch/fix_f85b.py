import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
s = io.open(p, encoding="utf-8").read()
a = "ring(y, hw + 0.016, zc + 0.004, 0.026, 0.026, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]], BELLY_PALE,"
b = "ring(y, hw + RIM_OUT, zc + 0.004, RIM_H, RIM_H, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]], BELLY_PALE,"
c = "ring(y, hw + 0.019, zc + 0.036, 0.006, 0.006, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]], SHELL_D,"
d = "ring(y, hw + RIM_OUT + 0.003, zc + 0.010 + RIM_H, 0.006, 0.006, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]], SHELL_D,"
e = "NC = 2.4\n"
f = "NC = 2.4\nRIM_OUT, RIM_H = 0.030, 0.040   # f85 MM2: the cream rim band (r5 slate band 0.016 proud, 0.026 half-height)\n"
for x, y in ((a, b), (c, d), (e, f)):
    assert s.count(x) == 1, x[:50]
    s = s.replace(x, y)
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
