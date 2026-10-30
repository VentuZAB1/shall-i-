import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
s = io.open(P, encoding="utf-8").read()
a = '''    B.tube([ring(y, hw + 0.008, zc - 0.012, 0.012, hb + 0.008, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]],
           BELLY_PALE, "Spine", nostud=True)                                                       # pale underside
'''
b = '''    B.tube([ring(y, hw + 0.008, zc - 0.012, 0.012, hb + 0.008, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]],
           BELLY_PALE, "Spine", nostud=True)                                                       # pale underside

    def shell_w(hw, hb, dz):                     # carapace half width at dz below the station centre
        return hw * max(1.0 - (min(dz / hb, 0.99)) ** NC, 0.0) ** (1.0 / NC)
    B.tube([ring(y, shell_w(hw, hb, 0.040) + 0.024, zc - 0.040, 0.019, 0.019, seg=28)
            for y, hw, zc, ht, hb in CAR[1:-1]], BELLY_PALE, "Spine", nostud=True)              # cream lip (M4b)
'''
assert a in s
s = s.replace(a, b)
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
