# Thunderbird clip pass 5: knee capsule covers the trouser's top third (the knee is buried in the belly by design,
# like the wing shoulders); walk swing lift 0.12 -> 0.09; belly keel narrower between the trousers.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\Thunderbird.py"
s = open(p, encoding="utf-8").read()
R = []
R.append(('''        out.append((tuple(K - d * 0.05), tuple(K + d * 0.16), 0.105, "Shin_" + sd))''',
          '''        out.append((tuple(K - d * 0.10), tuple(K + d * 0.20), 0.13, "Shin_" + sd))'''))
R.append(('''        return orig(leg, f, T, foot_z, toe=22.0 * min(1.0, lift / 0.12))''',
          '''        return orig(leg, f, T, foot_z, toe=22.0 * min(1.0, lift / 0.09))'''))
R.append(('''        return cm.biped_walk(k, n, 0.15, 0.12, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.6)''',
          '''        return cm.biped_walk(k, n, 0.15, 0.09, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.6)'''))
R.append(('''    low = B.add((0, 0.10, 0.64), (0.20, 0.20, 0.17), TEAL, "Spine", rot=(52, 0, 0), bot=(0.36, 0.66),''',
          '''    low = B.add((0, 0.10, 0.64), (0.20, 0.20, 0.17), TEAL, "Spine", rot=(52, 0, 0), bot=(0.28, 0.66),'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
