import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
s = io.open(p, encoding="utf-8").read()
R = [
("ring(y, hw + RIM_OUT, zc + 0.004 - rim_h(y) + RIM_H, rim_h(y), rim_h(y), seg=28)",
 "ring(y, hw + RIM_OUT + 0.035 * rear(y), zc + 0.004 - rim_h(y) + RIM_H, rim_h(y), rim_h(y), seg=28)"),
("ring(y, hw + RIM_OUT + 0.003, zc + 0.010 + RIM_H, 0.006, 0.006, seg=28)",
 "ring(y, hw + RIM_OUT + 0.003 + 0.035 * rear(y), zc + 0.010 + RIM_H, 0.006, 0.006, seg=28)"),
("    return RIM_H + 0.030 * rear(y)          # f85 MM2: the band deepens downward toward the rear (0.040 -> 0.070)",
 "    return RIM_H + 0.045 * rear(y)          # f85 MM2: the band deepens downward toward the rear (0.040 -> 0.085)"),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
