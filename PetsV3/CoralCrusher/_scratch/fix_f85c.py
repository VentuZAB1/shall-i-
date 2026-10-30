import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
s = io.open(p, encoding="utf-8").read()
R = [
("ring(y, hw + RIM_OUT, zc + 0.004, RIM_H, RIM_H, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]], BELLY_PALE,",
 "ring(y, hw + RIM_OUT, zc + 0.004 - rim_h(y) + RIM_H, rim_h(y), rim_h(y), seg=28) for y, hw, zc, ht, hb in CAR[1:-1]], BELLY_PALE,"),
("ring(y, hw + 0.040, zc - 0.100, 0.026, 0.030, seg=28)",
 "ring(y, hw + 0.040 + 0.030 * rear(y), zc - 0.100, 0.026, 0.030, seg=28)"),
("RIM_OUT, RIM_H = 0.030, 0.040   # f85 MM2: the cream rim band (r5 slate band 0.016 proud, 0.026 half-height)\n",
 "RIM_OUT, RIM_H = 0.030, 0.040   # f85 MM2: the cream rim band (r5 slate band 0.016 proud, 0.026 half-height)\n\n\n"
 "def rear(y):\n"
 "    \"\"\"0 at the shell middle -> 1 at the rear (the game camera sees the rear edge; no spines or legs cover it)\"\"\"\n"
 "    return min(max(y / 0.36, 0.0), 1.0)\n\n\n"
 "def rim_h(y):\n"
 "    return RIM_H + 0.030 * rear(y)          # f85 MM2: the band deepens downward toward the rear (0.040 -> 0.070)\n"),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
