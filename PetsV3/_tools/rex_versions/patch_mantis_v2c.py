# Thornblade Mantis v2c: FIERCE eyes - no cartoon glint, cleaner deep-ruby rim crescent, the V-brows stretched
# outward over the eye tops as angry lids.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\ThornbladeMantis.py"
s = open(p, encoding="utf-8").read()
R = []
R.append(('''        ellipsoid(B, e, (0.072, 0.07, 0.088), RUBY_D, "Head", Re)                                # deep rim
        eb, axb = e + Vector((s * 0.007, -0.010, 0.006)), (0.068, 0.066, 0.084)
        ellipsoid(B, eb, axb, RUBY, "Head", Re)                                                  # ruby body
        ellipsoid(B, on_surf(eb, axb, Re, (s * 0.45, -0.5, 0.74), 0.93), (0.024, 0.022, 0.016), RUBY_HOT, "Head",
                  Re)                                                                            # hot glint
        ellipsoid(B, on_surf(eb, axb, Re, (-s * 0.15, -0.98, -0.05), 0.92), (0.010, 0.012, 0.030), BLACK, "Head",
                  Re)                                                                            # pseudo-pupil slit''',
'''        ellipsoid(B, e, (0.072, 0.07, 0.090), RUBY_D, "Head", Re, n=24, rings=14)               # deep rim (back)
        eb, axb = e + Vector((s * 0.012, -0.018, 0.004)), (0.066, 0.064, 0.086)
        ellipsoid(B, eb, axb, RUBY, "Head", Re, n=24, rings=14)                                  # ruby body
        ellipsoid(B, on_surf(eb, axb, Re, (-s * 0.12, -0.98, 0.0), 0.92), (0.009, 0.012, 0.032), BLACK, "Head",
                  Re)                                                                            # pseudo-pupil slit'''))
R.append(('''        B.add(HC + Vector((s * 0.065, -0.10, 0.07)), (0.06, 0.016, 0.02), ARMOR, "Head", rot=(0, -s * 30, 0),
              role="detail", bevel=0.008)                                                     # V-brow (lids the eye)''',
'''        B.add(HC + Vector((s * 0.115, -0.105, 0.088)), (0.105, 0.018, 0.022), ARMOR, "Head",
              rot=(0, -s * 22, s * 14), role="detail", bevel=0.008)                            # V-brow = ANGRY LID'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
