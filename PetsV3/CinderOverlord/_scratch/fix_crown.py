p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
t = open(p, encoding="utf-8").read()
a0 = t.index("    # ================= THE HERO: crown of five obsidian blades")
a1 = t.index("    B.build()", a0)
new = '''    # ================= THE HERO: crown of five obsidian blades framed in gold on an obsidian crown mount. The blades
    # stand side by side (no x overlap, tops fanned outward) so each can lift on its own hinge (act_molt) untouched.
    B.add((0, -0.585, 1.835), (0.30, 0.050, 0.034), OBS_D, "Head", top=(0.92, 0.80), rnd=0.40)       # crown mount
    for s in (1, -1):
        B.add((s * 0.27, -0.565, 1.825), (0.06, 0.055, 0.040), OBS_D, "Head", rot=(0, s * 14, 0), rnd=0.40)
    for i, (x, h, w, roll, back) in enumerate(((-0.300, 0.15, 0.040, -24, 24), (-0.150, 0.19, 0.048, -12, 24),
                                               (0.0, 0.25, 0.060, 0, 24), (0.150, 0.19, 0.048, 12, 24),
                                               (0.300, 0.15, 0.040, 24, 24))):
        bone = "Crown_%d" % (i + 1)
        base = Vector((x, -0.585 + abs(x) * 0.08, 1.858 - abs(x) * 0.05))
        up_d = Euler((math.radians(-back), math.radians(roll), 0), "XYZ").to_matrix() @ Vector((0, 0, 1))
        back_d = Vector((0, 1, 0))
        tip = plate_crown(B, base, up_d, back_d, h, w, bone, gem=(i == 2))
        B.add(base + Vector((0, 0.0, -0.012)), (w * 0.95, 0.042, 0.030), OBS_D, bone,
              R=Euler((0, math.radians(roll), 0), "XYZ").to_matrix(), rnd=0.35)                 # plate socket
        ANCH[bone] = (tuple(base), tuple(tip))
'''
t = t[:a0] + new + t[a1:]
t = t.replace("""        B.seg(p - dv * 0.012, q + dv * 0.012, 0.019, t * 0.5 + 0.009, GOLD, bone, side=nrm.cross(dv),""",
              """        B.seg(p - dv * 0.010, q + dv * 0.010, 0.016, t * 0.5 + 0.009, GOLD, bone, side=nrm.cross(dv),""")
open(p, "w", encoding="utf-8").write(t)
print("ok")
