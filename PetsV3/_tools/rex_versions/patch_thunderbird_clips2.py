# Thunderbird clip pass 2: lower flank-skirt rows ride the trousers (no slicing), tail fan never lifts into the
# folded primaries, stoop grip released before the hop. Plain python.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\Thunderbird.py"
s = open(p, encoding="utf-8").read()
R = []
R.append(('''    for s in (1, -1):
        for z, L, c in ((0.70, 0.20, TEAL), (0.60, 0.19, STORM), (0.50, 0.16, STORM)):
            for dy in (-0.06, 0.04):
                B.spike((s * 0.18, dy, z), (s * 0.25, 0.65, -0.72), L, 0.06, c, "Spine", side=(s, 0, 0),
                        top=(0.2, 0.3))''',
'''    for s, sd in ((1, "L"), (-1, "R")):
        for z, L, c in ((0.70, 0.20, TEAL), (0.60, 0.19, STORM), (0.50, 0.16, STORM)):
            for dy in (-0.06, 0.04):                          # the 2 lower rows ride the trousers (thigh feathers)
                B.spike((s * 0.18, dy, z), (s * 0.25, 0.65, -0.72), L, 0.06, c,
                        "Spine" if z > 0.65 else "Shin_" + sd, side=(s, 0, 0), top=(0.2, 0.3))'''))
R.append(('''    for f, p in ((0, 0), (86, 0), (89, 8), (92, -3), (95, 0), (132, 0)):    # tail flick (pitch only: the''',
          '''    for f, p in ((0, 0), (86, 0), (89, -6), (92, 2), (95, 0), (132, 0)):    # tail pump DOWN (pitch only: the'''))
R.append(('''        tail(k, f, 2 * pk.wave(f, n, 0.2, 2), 0)
    orig = k.solve_leg''', '''        tail(k, f, -1.5 + 1.5 * pk.wave(f, n, 0.2, 2), 0)                # never above the folded primaries
    orig = k.solve_leg'''))
R.append(('''        (26, 0.25, 19, 0, -2, 10, 0, LIFT2, 10), (27, 0.21, 22, 0, -2, 10, 0, LIFT1, 8),
        (28, 0.16, 25, 0, -2, 10, 0, FOLD, 6), (30, 0.10, 25, 0, -2, 10, 0, FOLD, 6),''',
'''        (26, 0.25, 19, 0, -2, 10, 0, LIFT2, 8), (27, 0.21, 22, 0, -2, 10, 0, LIFT1, 3),
        (28, 0.16, 25, 0, -2, 10, 0, FOLD, 0), (30, 0.10, 25, 0, -2, 10, 0, FOLD, 0),'''))
R.append(('''            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, FOOT_LIFT + 0.01)) + reach,
                        toe=-8.0 if f < 35 else 6.0)                 # open, then clenched by f36''',
'''            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, FOOT_LIFT + 0.01 + (0.025 if f >= 58 else 0.0))) +
                        reach, toe=-8.0 if f < 35 else (6.0 if f < 57 else 0.0))   # open, clenched, released'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
