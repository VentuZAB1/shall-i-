# Abyssal Orca v3 tune: saddle band on the upper back only, more white, lathed teardrop orb, lighter rings.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\AbyssalOrca.py"
s = open(p, encoding="utf-8").read()
R = []
R.append(('''SEG = 32                     # points per full ring''', '''SEG = 24                     # points per full ring'''))
R.append(('''    for y0, y1, bone, zh0, zh1, g in ((-0.82, -0.05 + 0.02, "Chest", -0.42, -0.55, 0.0075),
                                      (-0.05, 0.26 + 0.02, "Spine", -0.55, -0.62, 0.0072),
                                      (0.26, 0.50, "Tail1", -0.62, -0.72, 0.0070)):''',
'''    for y0, y1, bone, zh0, zh1, g in ((-0.82, -0.05 + 0.02, "Chest", -0.30, -0.45, 0.0075),
                                      (-0.05, 0.26 + 0.02, "Spine", -0.45, -0.52, 0.0072),
                                      (0.26, 0.50, "Tail1", -0.52, -0.66, 0.0070)):'''))
R.append(('''    for i, (y0, y1, bone, zhi, zhi1) in enumerate(((-0.04, 0.10, "Spine", -0.45, -0.45),
                                                   (0.08, 0.20, "Spine", -0.25, -0.25),
                                                   (0.18, 0.26, "Spine", -0.05, -0.05),
                                                   (0.26, 0.38, "Tail1", 0.10, 0.10),
                                                   (0.36, 0.46, "Tail1", 0.12, -0.55))):    # the tongue's point''',
'''    for i, (y0, y1, bone, zhi, zhi1) in enumerate(((-0.06, 0.10, "Spine", -0.30, -0.30),
                                                   (0.08, 0.20, "Spine", -0.10, -0.10),
                                                   (0.18, 0.26, "Spine", 0.08, 0.08),
                                                   (0.26, 0.38, "Tail1", 0.22, 0.22),
                                                   (0.36, 0.48, "Tail1", 0.24, -0.50))):    # the tongue's point'''))
R.append(('''    band(B, 0.10, 0.26, SADDLE, "Spine", zlo=-0.10, grow=0.010, narrow1=0.90)
    band(B, 0.25, 0.46, SADDLE, "Tail1", zlo=-0.10 + 0.10 * 0.0, grow=0.0095, narrow1=0.10)''',
'''    band(B, 0.10, 0.26, SADDLE, "Spine", zlo=0.40, grow=0.010, narrow1=0.90)
    band(B, 0.25, 0.46, SADDLE, "Tail1", zlo=0.40, grow=0.0095, narrow1=0.08)'''))
R.append(('''    for a in (0, 30, 60):                          # FIX 6: jade drop of light - smooth 12-sided body + lower cone
        B.add(ORB + Vector((0, 0, 0.04)), (0.15, 0.15, 0.11), GLOW, "Esca", rot=(0, 0, a), rnd=0.92, role="limb",
              studs=[], nostud=True, top=(0.90, 0.90))
        B.add(ORB - Vector((0, 0, 0.10)), (0.15, 0.15, 0.065), GLOW, "Esca", rot=(0, 0, a), rnd=0.92, role="limb",
              studs=[], nostud=True, bot=(0.40, 0.40))
    B.add(ORB + Vector((0.05, -0.151, 0.07)), (0.026, 0.006, 0.026), HOT, "Esca", rot=(0, 0, 18), studs=[],
          role="detail", bevel=0.004)                                                          # glint facet''',
'''    # FIX 6: the jade orb as a smooth lathed DROP OF LIGHT (widest just under the middle, a point into the drip)
    PROF = [(0.15, 0.07), (0.13, 0.115), (0.09, 0.145), (0.04, 0.158), (-0.02, 0.155), (-0.07, 0.13), (-0.11, 0.09),
            (-0.145, 0.05), (-0.165, 0.03)]
    rings = [[ORB + Vector((r * math.cos(2 * math.pi * j / 20), r * math.sin(2 * math.pi * j / 20), dz))
              for j in range(20)] for dz, r in PROF]
    B.tube(rings, GLOW, "Esca", nostud=True)
    gd = Vector((0.31, -0.95, 0)).normalized()
    B.add(ORB + gd * 0.154 + Vector((0, 0, 0.07)), (0.026, 0.006, 0.026), HOT, "Esca", rot=(0, 0, 18), studs=[],
          role="detail", bevel=0.004)                                                          # glint facet'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
