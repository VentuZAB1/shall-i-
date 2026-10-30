import io
P = "pets/CinderOverlord.py"
s = io.open(P, encoding="utf-8").read()
a = '''    skull = B.tube(rings, PLUM_OBS, "Head")
'''
b = '''    skull = B.tube(rings, PLUM_OBS, "Head")
    cap = []                                   # obsidian skull cap (r2: darker, fiercer face read; brow to crown)
    for f, rw, rh, dz in ((0.03, 0.150, 0.118, 0.0), (0.06, 0.172, 0.138, 0.0), (0.18, 0.200, 0.155, 0.0),
                          (0.40, 0.188, 0.146, 0.0), (0.56, 0.168, 0.130, -0.004), (0.66, 0.152, 0.116, -0.008)):
        c = SK0 + sd * skl * f + Vector((0, 0, dz))
        aa, ab = math.radians(58), math.radians(122)
        cap.append((oval(c, sside, sup, rw, rh, aa, ab, seg=8, n=2.6, off=0.008),
                    oval(c, sside, sup, rw, rh, aa, ab, seg=8, n=2.6, off=-0.014)))
    B.tube(cap, OBS_D, "Head", closed=False, nostud=False)
'''
assert a in s
s = s.replace(a, b)
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
