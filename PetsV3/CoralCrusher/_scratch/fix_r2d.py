import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
s = io.open(P, encoding="utf-8").read()
rep = [
# cream lip must stick out past the slate rim band (rim = hw + 0.016) or the rim overhang hides it
('''    B.tube([ring(y, shell_w(hw, hb, 0.040) + 0.024, zc - 0.040, 0.019, 0.019, seg=28)''',
 '''    B.tube([ring(y, shell_w(hw, hb, 0.042) + 0.040, zc - 0.042, 0.022, 0.020, seg=28)'''),
# broad cream underside on each palm (lower third; real crab claws are pale below) - not a strip
('''        palm = B.tube(rings, BRONZE, claw)                                                          # oval palm''',
 '''        palm = B.tube(rings, BRONZE, claw)                                                          # oval palm
        urings = []                                   # r2 M4b: broad cream underside of the palm (lower third)
        for t, wx, wo in ((0.06, 0.086, 0.122), (0.32, 0.118, 0.172), (0.58, 0.120, 0.172), (0.86, 0.104, 0.146)):
            cc = P0.lerp(F, t)
            arcs = []
            for off in (0.007, -0.014):
                rg = []
                for q in range(13):
                    ang = math.radians(212 + 116 * q / 12)
                    cs, sn = math.cos(ang), math.sin(ang)
                    rg.append(cc + out * ((wx * c + off) * math.copysign(abs(cs) ** (2 / 2.3), cs)) +
                              o * ((wo * c + off) * math.copysign(abs(sn) ** (2 / 2.3), sn)))
                arcs.append(rg)
            urings.append((arcs[0], arcs[1]))
        B.tube(urings, BELLY_PALE, claw, closed=False, nostud=True)'''),
]
for a, b in rep:
    assert a in s, "MISSING " + a[:80]
    s = s.replace(a, b)
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
