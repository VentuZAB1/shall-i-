import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
s = io.open(p, encoding="utf-8").read()
a = "ring(y, hw + RIM_OUT + 0.003 + 0.035 * rear(y), zc + 0.010 + RIM_H, 0.006, 0.006, seg=28)"
b = "ring(y, hw + 0.012, zc + 0.010 + RIM_H, 0.006, 0.006, seg=28)"
assert s.count(a) == 1
s = s.replace(a, b)
s = s.replace("# f85 MM2: thin slate seam above it", "# f85 MM2: thin slate seam above it (inside the band edge)")
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
