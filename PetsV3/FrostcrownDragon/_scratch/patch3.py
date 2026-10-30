# review 1 (REVISE 6/10): MUST 1-5 + NICE N1, N2
p = "pets/FrostcrownDragon.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


# MUST 4 colours
rep("STEEL_BLUE = (88, 136, 210)   # body, neck, legs, tail, head (studded) - plan hue 216, richer (MODEL_NOTES D1)",
    "STEEL_BLUE = (70, 118, 190)   # body, neck, legs, tail, head (studded) - plan hue 216, richer (review 1 MUST 4)")
rep("MEMBRANE = (150, 178, 228)    # wing membranes (smooth), frost blue (MODEL_NOTES D1)",
    "MEMBRANE = (116, 146, 206)    # wing membranes (smooth), frost blue (review 1 MUST 4)")
rep("DEEP_STEEL = (58, 86, 156)    # dorsal saddle", "DEEP_STEEL = (38, 64, 130)    # dorsal saddle")
# MUST 1 seven fins
rep('FIN_BONES = ["Fin_%d" % i for i in range(1, 6)]', 'FIN_BONES = ["Fin_%d" % i for i in range(1, 8)]\n'
    'FIN_PARENTS = ("Neck2", "Neck", "Chest", "Spine", "Spine", "Tail1", "Tail2")')
rep('''    fin_spec = (("Fin_1", N1.lerp(N2, 0.55), 0.31, 0.21, "Neck2", (0, 0.13, 0.0)),
                ("Fin_2", (N0 + Vector((0, 0.03, -0.05))).lerp(N1, 0.55), 0.41, 0.26, "Neck", (0, 0.15, 0.07)),
                ("Fin_3", Vector((0, -0.50, 1.0)), 0.48, 0.32, "Chest", None),
                ("Fin_4", Vector((0, 0.08, 1.0)), 0.42, 0.29, "Spine", None),
                ("Fin_5", Vector((0, 0.46, 1.0)), 0.32, 0.24, "Spine", None))''',
    '''    # bases spaced so the swept blades never overlap (spacing >= ~0.8 chord): neck bases are explicit points on
    # the neck back, body bases are ray hits on the saddle shells, tail bases sit on the tail's dorsal band
    TA = [Vector(p) for p in TAILP]
    fin_spec = (("Fin_1", Vector((0, -0.83, 1.52)), 0.40, 0.26, "Neck2", (0, 0, 0)),
                ("Fin_2", Vector((0, -0.56, 1.18)), 0.55, 0.31, "Neck", (0, 0, 0)),
                ("Fin_3", Vector((0, -0.15, 1.0)), 0.60, 0.38, "Chest", None),
                ("Fin_4", Vector((0, 0.24, 1.0)), 0.52, 0.35, "Spine", None),
                ("Fin_5", Vector((0, 0.60, 1.0)), 0.42, 0.29, "Spine", None),
                ("Fin_6", TA[0].lerp(TA[1], 0.45), 0.30, 0.20, "Tail1", (0, 0, 0.165)),
                ("Fin_7", TA[1].lerp(TA[2], 0.45), 0.24, 0.17, "Tail2", (0, 0, 0.125)))''')
rep('ANCH["FX_FinSpark_" + nm[-1]] = tuple(frost_fin(B, base, h, ch, 0.075, nm))',
    'ANCH["FX_FinSpark_" + nm[-1]] = tuple(frost_fin(B, base, h, ch, 0.085, nm))')
rep('''    for i, (nm, parent) in enumerate(zip(FIN_BONES, ("Neck2", "Neck", "Chest", "Spine", "Spine"))):''',
    '''    assert len(FIN_PARENTS) == len(FIN_BONES)
    for i, (nm, parent) in enumerate(zip(FIN_BONES, FIN_PARENTS)):''')
# the old body ridge spikes sat where fins 3 / 4 / 6 now stand: removed (the DARK stripe stays)
a0 = s.index("    # dark back line: small laid-back ridge scales between the fins, down to the tail")
a1 = s.index("    # ================= legs:")
s = s[:a0] + s[a1:]
# tail: no ridge spikes on Tail1 / Tail2 (fins 6 / 7 stand there)
rep('''        for t in (0.30, 0.75):
            p = a.lerp(b, t)''', '''        for t in ((0.30, 0.75) if i >= 2 else ()):
            p = a.lerp(b, t)''')
# MUST 2 frost core replaces the keel plate + grille; belly rungs 4 -> 2
rep('''    for t, w in ((0.10, 0.10), (0.36, 0.10), (0.62, 0.095), (0.88, 0.085)):''',
    '''    for t, w in ((0.40, 0.10), (0.80, 0.09)):''')
a0 = s.index("    keel = seat_plate(B, [rib], (0, -2, 0.84)")
a1 = s.index("    # ================= S-neck")
s = s[:a0] + '''    # the FROST CORE: one faceted ICE_W crystal on the chest front (0.20 wide x 0.26 tall, 0.012 proud) in a DARK
    # setting, with an ICE_BELLY inner facet - the crystal focal point against the studded hide
    cp, cn = surf_hit(B, [rib], (0, -2, 0.86), (0, 1, 0))
    cu = Vector((1, 0, 0))
    cv = cn.cross(cu).normalized()
    if cv.z < 0:
        cv = -cv
    hexa = [(0, 0.13), (0.10, 0.052), (0.10, -0.052), (0, -0.13), (-0.10, -0.052), (-0.10, 0.052)]
    B.poly([cp + cn * 0.004 + cu * (x * 1.18) + cv * (y * 1.14) for x, y in hexa], 0.03, DARK, "Chest")
    B.poly([cp + cn * (0.012 - 0.022) + cu * x + cv * y for x, y in hexa], 0.044, ICE_W, "Chest")
    B.poly([cp + cn * 0.016 + cu * (x * 0.52) + cv * (y * 0.56) for x, y in hexa], 0.008, ICE_BELLY, "Chest")
    for x0, y0, x1, y1 in ((0, 0.13, 0, -0.13), (-0.10, 0.052, 0.10, -0.052), (0.10, 0.052, -0.10, -0.052)):
        B.bar(cp + cn * 0.013 + cu * x0 + cv * y0, cp + cn * 0.013 + cu * x1 + cv * y1, cn, 0.012, 0.004, ICE_BELLY,
              "Chest", studs=[], role="detail", bevel=0.002)                                     # facet edges
    ANCH["Core"] = tuple(cp + cn * 0.02)
''' + s[a1:]
# MUST 3 crown
rep('''        P = [HC + Vector((s * 0.09, -0.06, 0.12)), HC + Vector((s * 0.165, 0.11, 0.26)),
             HC + Vector((s * 0.235, 0.34, 0.345)), HC + Vector((s * 0.285, 0.64, 0.38))]
        tip = horn(B, P, 0.066, "Horn_" + side)''',
    '''        P = [HC + Vector((s * 0.09, -0.06, 0.12)), HC + Vector((s * 0.17, 0.11, 0.27)),
             HC + Vector((s * 0.25, 0.36, 0.36)), HC + Vector((s * 0.31, 0.74, 0.40))]
        tip = horn(B, P, 0.080, "Horn_" + side)''')
rep('''    B.add(HC + Vector((0, -0.150, 0.11)), (0.13, 0.022, 0.032), GOLD, "Head", top=(0.92, 1), role="limb",''',
    '''    B.add(HC + Vector((0, -0.152, 0.11)), (0.15, 0.030, 0.040), GOLD, "Head", top=(0.92, 1), role="limb",''')
rep('''        B.seg(HC + Vector((s * 0.134, -0.15, 0.106)), HC + Vector((s * 0.132, 0.14, 0.10)), 0.016, 0.032, GOLD,''',
    '''        B.seg(HC + Vector((s * 0.146, -0.15, 0.106)), HC + Vector((s * 0.142, 0.15, 0.10)), 0.022, 0.040, GOLD,''')
rep('''    B.add(HC + Vector((0, 0.145, 0.10)), (0.12, 0.016, 0.03), GOLD_D, "Head", studs=[], nostud=True, role="limb",''',
    '''    B.add(HC + Vector((0, 0.158, 0.10)), (0.13, 0.016, 0.04), GOLD_D, "Head", studs=[], nostud=True, role="limb",''')
rep('''    for x, h in ((-0.07, 0.07), (0.0, 0.105), (0.07, 0.07)):                                       # three points
        base = HC + Vector((x * 1.1, -0.155, 0.13))
        B.spike(base, (x * 0.8, -0.18, 1), h, 0.022, GOLD, "Head", top=(0.12, 0.12), nostud=True)''',
    '''    for x, h, w in ((-0.10, 0.06, 0.020), (-0.05, 0.09, 0.024), (0.0, 0.13, 0.030), (0.05, 0.09, 0.024),
                    (0.10, 0.06, 0.020)):                                                       # five points
        base = HC + Vector((x, -0.160, 0.13))
        B.spike(base, (x * 0.8, -0.16, 1), h, w, GOLD, "Head", top=(0.12, 0.12), nostud=True)''')
rep('# ================= HERO: the GOLD HORN CROWN - two long back-swept horns from the brow + a slim diadem, 3 points',
    '# ================= HERO: the GOLD HORN CROWN - two long back-swept horns from the brow + a diadem, 5 points')
# MUST 5 tail crystal
rep('B.spike(main, tipd + Vector((0, 0, 0.18)), 0.32, 0.065, ICE_W', 'B.spike(main, tipd + Vector((0, 0, 0.18)), 0.44, 0.085, ICE_W')
rep('B.spike(main - tipd * 0.02, Vector((sx * 0.55, 0.7, 0.42)), 0.19, 0.042, ICE_W', 'B.spike(main - tipd * 0.02, Vector((sx * 0.55, 0.7, 0.42)), 0.26, 0.05, ICE_W')
rep('ANCH["FX_IceDust"] = tuple(main + (tipd + Vector((0, 0, 0.18))).normalized() * 0.30)', 'ANCH["FX_IceDust"] = tuple(main + (tipd + Vector((0, 0, 0.18))).normalized() * 0.42)')
# NICE N1 / N2
rep('B.add(HC, (0.155, 0.16, 0.125), STEEL_BLUE, "Head", top=(0.80, 0.85), rnd=0.25)', 'B.add(HC, (0.17, 0.175, 0.135), STEEL_BLUE, "Head", top=(0.80, 0.85), rnd=0.25)')
rep('B.seg(H + Vector((0, 0, 0.06)), K, 0.105, 0.13, STEEL_BLUE, leg', 'B.seg(H + Vector((0, 0, 0.06)), K, 0.12, 0.14, STEEL_BLUE, leg')
# check pairs: the new fins
rep('''          ("Fin_3", "Neck"), ("Fin_4", "Fin_3"), ("Fin_4", "Fin_5")]''',
    '''          ("Fin_3", "Neck"), ("Fin_4", "Fin_3"), ("Fin_4", "Fin_5"), ("Fin_5", "Fin_6"), ("Fin_6", "Fin_7"),
          ("Fin_6", "Spine"), ("Fin_7", "Tail1"), ("Fin_1", "Head"), ("Fin_1", "Horn_L"), ("Fin_1", "Horn_R"),
          ("Fin_2", "Horn_L"), ("Fin_2", "Horn_R")]''')
# header text
rep("the brow (GOLD_D ridges + tips) and a slim gold diadem with three points. Signature: FIVE flat ICE-WHITE frost fins",
    "the brow (GOLD_D ridges + tips) and a gold diadem with five points. Signature: SEVEN flat ICE-WHITE frost fins")
open(p, "w", encoding="utf-8").write(s)
print("ok")
