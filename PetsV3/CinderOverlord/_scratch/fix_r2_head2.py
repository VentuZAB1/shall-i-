import io
P = "pets/CinderOverlord.py"
s = io.open(P, encoding="utf-8").read()
rep = [
('''                          (0.40, 0.188, 0.146, 0.0), (0.62, 0.160, 0.124, -0.004), (0.80, 0.122, 0.100, -0.008),
                          (0.93, 0.078, 0.070, -0.010), (1.0, 0.036, 0.040, -0.012)):''',
 '''                          (0.40, 0.188, 0.146, 0.0), (0.62, 0.160, 0.122, -0.006), (0.80, 0.124, 0.094, -0.014),
                          (0.92, 0.088, 0.064, -0.022), (1.0, 0.050, 0.034, -0.030)):'''),
('''        B.add((s * 0.17, -0.60, 1.64), (0.065, 0.12, 0.095), PLUM_OBS, "Head", rot=(0, 0, s * 10), rnd=0.42)''',
 '''        B.add((s * 0.16, -0.60, 1.64), (0.055, 0.11, 0.090), PLUM_OBS, "Head", rot=(0, 0, s * 10), rnd=0.45)'''),
('''        npt, nn = surf_hit(B, [skull], (s * 0.042, -1.00, 2.4), (0, 0, -1))
        B.add(npt, (0.014, 0.006, 0.020), BLACK, "Head", R=face_R(nn, up=(0, 1, 0)), studs=[], role="detail",''',
 '''        npt, nn = surf_hit(B, [skull], (s * 0.040, -0.955, 2.4), (0, 0, -1))
        B.add(npt, (0.010, 0.005, 0.016), BLACK, "Head", R=face_R(nn, up=(s * 0.4, 1, 0)), studs=[], role="detail",'''),
('''        scutes(a, b, FRAD[i], FRAD[i + 1], fb[i], 232, 308, up=(0, 1, 0))''',
 '''        scutes(a, b, FRAD[i], FRAD[i + 1], fb[i], 232, 308, up=(0, 1, 0), ts=((0.04, 0.46), (0.52, 0.94)))'''),
]
for a, b in rep:
    assert a in s, a[:60]
    s = s.replace(a, b)
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
