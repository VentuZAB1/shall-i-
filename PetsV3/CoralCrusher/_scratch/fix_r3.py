import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
s = io.open(p, encoding="utf-8").read()
R = [
# N1: the two dome clusters taper - wider ROSE_D base, pointed ROSE spikes
("""        B.add(p + n * 0.005, (0.045 * sc, 0.045 * sc, 0.022 * sc), ROSE_D, "Spine", R=face_R(-n, up=(0, 1, 0)),
              rnd=0.45, nostud=True)""",
 """        dome = sc >= 1.2                                  # r3 N1: the dome clusters taper (wide base, pointed tips)
        bw = 0.060 if dome else 0.045
        B.add(p + n * 0.005, (bw * sc, bw * sc, 0.022 * sc), ROSE_D, "Spine", R=face_R(-n, up=(0, 1, 0)),
              rnd=0.45, nostud=True)"""),
("""            B.spike(p + Vector((bx, by, 0)) * sc, d, L * sc, 0.024 * sc, ROSE, "Spine", top=(0.85, 0.85),
                    nostud=True, rnd=0.45, role="limb")""",
 """            B.spike(p + Vector((bx, by, 0)) * sc, d, L * sc, (0.030 if dome else 0.024) * sc, ROSE, "Spine",
                    top=(0.22, 0.22) if dome else (0.85, 0.85), nostud=True, rnd=0.45, role="limb")"""),
# idle breath +/-6
("    breath = [(0, 0), (28, 0), (45, -5), (62, 5), (80, -5), (98, 0), (120, 0)]   # f85 CM1 / r2: the guard breathes +/-5",
 "    breath = [(0, 0), (28, 0), (45, -6), (62, 6), (80, -6), (98, 0), (120, 0)]   # r3: the guard breathes +/-6 (r2 5, f85 3)"),
("arc (r2: +/-5), troughs f45 / f80", "arc (r3: +/-6), troughs f45 / f80"),
# shell roll +/-4
("roll=-2 * u - 3 * (2 * tr - 1) * u)   # f85 r2: +/-3 deg with each beat (was 2)",
 "roll=-2 * u - 4 * (2 * tr - 1) * u)   # r3: +/-4 deg with each beat (r2 3, f85 2)"),
# eyes: right 26, left -16
("l=-12 * tr * u, r=4 * u + 20 * tr * u)", "l=-16 * tr * u, r=4 * u + 26 * tr * u)"),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
