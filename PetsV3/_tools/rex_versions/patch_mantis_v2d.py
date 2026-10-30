# Thornblade Mantis v2d: the mint sternite stripe shows in the side view (BELLY >= 7 %): wider than the hide, taller.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\ThornbladeMantis.py"
s = open(p, encoding="utf-8").read()
R = []
R.append(('''        B.seg(a + Vector((0, 0, -d + 0.02)), b + Vector((0, 0, -d * 0.8 + 0.02)), w * 0.98, 0.03, BELLY, bone,
              ext=0.01, top=(0.9 if i < 2 else 0.6, 1))                                       # sternites (FIX 6)''',
'''        B.seg(a + Vector((0, 0, -d + 0.04)), b + Vector((0, 0, -d * 0.8 + 0.04)), w * 1.03, 0.05, BELLY, bone,
              ext=0.01, top=(0.9 if i < 2 else 0.6, 1))                                       # sternites: mint stripe'''))
R.append(('''        B.seg(p - u * 0.014 + Vector((0, 0, -d * 0.8 + 0.02)), p + u * 0.014 + Vector((0, 0, -d * 0.8 + 0.02)),
              w * 0.99 * (1 if i < 2 else 0.7), 0.034, BELLY_D, bone, studs=[])                # sternite gap bar''',
'''        B.seg(p - u * 0.014 + Vector((0, 0, -d * 0.85 + 0.04)), p + u * 0.014 + Vector((0, 0, -d * 0.85 + 0.04)),
              w * 1.045 * (1 if i < 2 else 0.7), 0.054, BELLY_D, bone, studs=[])              # sternite gap bar'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
