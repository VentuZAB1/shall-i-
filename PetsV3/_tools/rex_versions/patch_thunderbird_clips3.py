# Thunderbird clip pass 3: the STORM flank-skirt rows become thin feather BLADES on the body, hung OUTSIDE the
# trousers' swing band (the shin only pitches about the knee, so nothing outside its x band can be cut); trouser
# top flare removed; stoop grip held 2 cm higher; idle pump without the up-overshoot; walk tail lower + follows the
# chest yaw.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\Thunderbird.py"
s = open(p, encoding="utf-8").read()
R = []
R.append(('''    for s, sd in ((1, "L"), (-1, "R")):
        for z, L, c in ((0.70, 0.20, TEAL), (0.60, 0.19, STORM), (0.50, 0.16, STORM)):
            for dy in (-0.06, 0.04):                          # the 2 lower rows ride the trousers (thigh feathers)
                B.spike((s * 0.18, dy, z), (s * 0.25, 0.65, -0.72), L, 0.06, c,
                        "Spine" if z > 0.65 else "Shin_" + sd, side=(s, 0, 0), top=(0.2, 0.3))''',
'''    for s in (1, -1):
        for dy in (-0.06, 0.04):                                                  # TEAL top row over the hip
            B.spike((s * 0.18, dy, 0.70), (s * 0.25, 0.65, -0.72), 0.20, 0.06, TEAL, "Spine", side=(s, 0, 0),
                    top=(0.2, 0.3))
        dv = Vector((s * 0.40, 0.62, -0.68)).normalized()
        for z, x0, L in ((0.61, 0.225, 0.18), (0.52, 0.25, 0.15)):                # STORM flank blades, hung outside
            for dy in (-0.06, 0.04):                                              # the trousers' swing band
                b0 = Vector((s * x0, dy, z))
                B.bar(b0, b0 + dv * L, Vector((s, 0, 0)), 0.11, 0.02, STORM, "Spine", top=(0.2, 0.5), studs=[])'''))
R.append(('''        B.seg(K, A + Vector((0, 0, 0.04)), 0.07, 0.075, STORM, "Shin_" + side, ext=0.05, top=(1.21, 1.2), rnd=0.45)''',
          '''        B.seg(K, A + Vector((0, 0, 0.04)), 0.07, 0.075, STORM, "Shin_" + side, ext=0.05, top=(1.0, 1.15), rnd=0.45)'''))
R.append(('''            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, FOOT_LIFT + 0.01 + (0.025 if f >= 58 else 0.0))) +
                        reach, toe=-8.0 if f < 35 else (6.0 if f < 57 else 0.0))   # open, clenched, released''',
'''            zg = FOOT_LIFT + 0.01 + (0.02 if 35 <= f < 57 else 0.0) + (0.025 if f >= 58 else 0.0)
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, zg)) + reach,
                        toe=-8.0 if f < 35 else (6.0 if f < 57 else 0.0))   # open, clenched (claws >= -0.02), released'''))
R.append(('''    for f, p in ((0, 0), (86, 0), (89, -6), (92, 2), (95, 0), (132, 0)):    # tail pump DOWN (pitch only: the''',
          '''    for f, p in ((0, 0), (85, 0), (88, -5), (92, -1), (96, 0), (132, 0)):   # tail pump DOWN (pitch only: the'''))
R.append(('''        tail(k, f, -1.5 + 1.5 * pk.wave(f, n, 0.2, 2), 0)                # never above the folded primaries''',
          '''        tail(k, f, -2.5 + 1.5 * pk.wave(f, n, 0.2, 2), cy)               # below the folded primaries, with the chest'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
