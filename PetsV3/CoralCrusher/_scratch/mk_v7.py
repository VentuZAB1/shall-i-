D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
p = D + r"\pets\CoralCrusher.py"
t = open(p, encoding="utf-8").read()
rep = [
# pale lip under the dark rim band (the two-tone crab edge, visible from the side)
("""    B.tube([ring(y, hw * 0.80, zc - hb * 0.72, 0.03, 0.035, n=2.2, seg=20) for y, hw, zc, ht, hb in CAR[1:-1]],
           BELLY_PALE, "Spine", nostud=True)                                                       # sternum""",
 """    B.tube([ring(y, hw * 0.80, zc - hb * 0.72, 0.03, 0.035, n=2.2, seg=20) for y, hw, zc, ht, hb in CAR[1:-1]],
           BELLY_PALE, "Spine", nostud=True)                                                       # sternum
    B.tube([ring(y, hw * 0.975 + 0.006, zc - 0.052, 0.030, 0.032, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]],
           BELLY_PALE, "Spine", nostud=True)                                                       # pale lip"""),
# claw: pale underside strip along the palm (the -o side) + under the merus
("""        palm = B.tube(rings, BRONZE, claw)                                                          # oval palm""",
 """        palm = B.tube(rings, BRONZE, claw)                                                          # oval palm
        prings = []
        for t, wx, wo in ((0.06, 0.086, 0.122), (0.32, 0.118, 0.172), (0.58, 0.120, 0.172), (0.86, 0.104, 0.146)):
            cc = P0.lerp(F, t)
            arcs = []
            for off in (0.008, -0.012):
                rg = []
                for q in range(9):
                    ang = math.radians(215 + 110 * q / 8)
                    cs, sn = math.cos(ang), math.sin(ang)
                    rg.append(cc + out * ((wx * c + off) * math.copysign(abs(cs) ** (2 / 2.3), cs)) +
                              o * ((wo * c + off) * math.copysign(abs(sn) ** (2 / 2.3), sn)))
                arcs.append(rg)
            prings.append((arcs[0], arcs[1]))
        B.tube(prings, BELLY_PALE, claw, closed=False, nostud=True)                                 # pale underside
        dmz = (E - S).normalized()
        B.seg(S + dmz * 0.06 - Vector((0, 0, 0.078 * c)), E - dmz * 0.05 - Vector((0, 0, 0.074 * c)), 0.06 * c,
              0.016, BELLY_PALE, arm, side=dmz.cross(Vector((0, 0, 1))), studs=[], nostud=True, role="limb",
              rnd=0.3)                                                                              # merus belly"""),
# legs: bronze merus top plate + a rose spike on each merus
("""            B.add(K, (0.072, 0.072, 0.072), BRONZE, shin, rnd=0.42)                                   # knee""",
 """            dm = (K - H).normalized()
            B.seg(H + dm * 0.05 + Vector((0, 0, 0.060)), K - dm * 0.04 + Vector((0, 0, 0.062)), 0.020, 0.075,
                  BRONZE, leg, side=(0, 0, 1), top=(1.0, 0.85), rnd=0.35)                           # merus top plate
            rose_spike(B, H.lerp(K, 0.62) + Vector((0, 0, 0.085)), dm * 0.35 + Vector((0, 0, 1)), 0.075, 0.026, leg)
            B.add(K, (0.072, 0.072, 0.072), SHELL_D, shin, rnd=0.42)                                  # knee"""),
]
for a, b in rep:
    if a not in t:
        print("MISSING", a[:80])
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)

p2 = D + r"\pets\CinderOverlord.py"
t = open(p2, encoding="utf-8").read()
rep2 = [
("""            for dt in (-0.07, 0.07):
                p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t + dt, ang, off=0.004)
                vent(B, p, n, dv, bone, L=0.15 * sc + 0.03, w=0.036 * sc + 0.008)""",
 """            for dt in (-0.09, 0.0, 0.09):
                p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t + dt, ang, off=0.004)
                vent(B, p, n, dv, bone, L=0.18 * sc + 0.035, w=0.042 * sc + 0.010)"""),
("""    for vi, (bone, t) in enumerate((("Spine", 0.30), ("Body1", 0.28), ("Body2", 0.28), ("Body3", 0.28),
                                    ("Body4", 0.28), ("Tail1", 0.28))):""",
 """    for vi, (bone, t) in enumerate((("Spine", 0.27), ("Body1", 0.27), ("Body2", 0.27), ("Body3", 0.27),
                                    ("Body4", 0.27), ("Tail1", 0.27))):"""),
]
for a, b in rep2:
    if a not in t:
        print("MISSING2", a[:80])
    t = t.replace(a, b)
open(p2, "w", encoding="utf-8").write(t)
print("ok")
