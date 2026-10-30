# Thunderbird clip pass 4: the crouches put the belly ON the legs -> belly bottom narrows to a keel that fits between
# the trousers, the cuff feathers never splay inward (and are mirrored L/R), one flank-blade row (covers the knee),
# takeoff / land crouch 3-4 cm shallower.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\Thunderbird.py"
s = open(p, encoding="utf-8").read()
R = []
R.append(('''    low = B.add((0, 0.10, 0.64), (0.20, 0.20, 0.17), TEAL, "Spine", rot=(52, 0, 0), bot=(0.72, 0.66),''',
          '''    low = B.add((0, 0.10, 0.64), (0.20, 0.20, 0.17), TEAL, "Spine", rot=(52, 0, 0), bot=(0.36, 0.66),'''))
R.append(('''        for z, x0, L in ((0.61, 0.225, 0.18), (0.52, 0.25, 0.15)):                # STORM flank blades, hung outside''',
          '''        for z, x0, L in ((0.61, 0.225, 0.16),):                                  # STORM flank blades, hung outside'''))
R.append(('''            rv = Vector((math.cos(ang) * 0.075, math.sin(ang) * 0.08, 0))''',
          '''            rv = Vector((s * math.cos(ang) * 0.075, math.sin(ang) * 0.08, 0))                 # mirrored L / R'''))
R.append(('''            B.spike(A + rv + Vector((0, 0, 0.11)), (rv.x * 6, rv.y * 6 - 0.15, -1), L, 0.04,''',
          '''            B.spike(A + rv + Vector((0, 0, 0.11)), (rv.x * (3 if rv.x * s > 0 else 0), rv.y * 6 - 0.15, -1), L, 0.04,'''))
R.append(('''    for f, z, p, ch, hd, w in ((3, -0.05, 4, 2, -2, LIFT1), (6, -0.10, 8, 4, -6, LIFT2), (8, -0.13, 9, 5, -9, LIFT3),
                               (9, -0.15, 10, 6, -11, LIFT4), (10, -0.16, 10, 6, -12, (30, 0, 0, 0)),''',
'''    for f, z, p, ch, hd, w in ((3, -0.04, 4, 2, -2, LIFT1), (6, -0.08, 8, 4, -6, LIFT2), (8, -0.10, 9, 5, -9, LIFT3),
                               (9, -0.115, 10, 6, -11, LIFT4), (10, -0.12, 10, 6, -12, (30, 0, 0, 0)),'''))
R.append(('''    for f, z, p, w in ((17, -0.12, 8, RAISED_V), (22, -0.07, 4, RAISED_V), (24, -0.05, 3, LIFT4),''',
          '''    for f, z, p, w in ((17, -0.09, 8, RAISED_V), (22, -0.06, 4, RAISED_V), (24, -0.045, 3, LIFT4),'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
