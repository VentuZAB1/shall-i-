p = "pets/FrostcrownDragon.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:80])
    s = s.replace(a, b)


# bigger torso
rep('rib = B.add((0, -0.30, 0.88), (0.27, 0.38, 0.30), STEEL_BLUE', 'rib = B.add((0, -0.30, 0.88), (0.30, 0.40, 0.32), STEEL_BLUE')
rep('withers = B.add((0, -0.38, 1.17), (0.20, 0.25, 0.07)', 'withers = B.add((0, -0.38, 1.19), (0.22, 0.26, 0.07)')
rep('waist = B.add((0, 0.14, 0.92), (0.20, 0.24, 0.18)', 'waist = B.add((0, 0.14, 0.92), (0.215, 0.24, 0.19)')
rep('hips = B.add((0, 0.50, 0.90), (0.22, 0.22, 0.20)', 'hips = B.add((0, 0.50, 0.90), (0.235, 0.22, 0.21)')
# neck thicker
rep('N1, 0.15, 0.16, STEEL_BLUE, "Neck"', 'N1, 0.165, 0.17, STEEL_BLUE, "Neck"')
rep('0.125, 0.13, STEEL_BLUE, "Neck2"', '0.14, 0.145, STEEL_BLUE, "Neck2"')
rep('(N0 + Vector((0, 0.03, -0.05)), N1, "Neck", 0.11, 0.16), (N1, N2, "Neck2", 0.09, 0.13)',
    '(N0 + Vector((0, 0.03, -0.05)), N1, "Neck", 0.12, 0.17), (N1, N2, "Neck2", 0.10, 0.145)')
# head: bigger skull, cleaner brows / eyes
rep('B.add(HC, (0.14, 0.15, 0.115), STEEL_BLUE, "Head", top=(0.80, 0.85), rnd=0.25)',
    'B.add(HC, (0.155, 0.16, 0.125), STEEL_BLUE, "Head", top=(0.80, 0.85), rnd=0.25)')
rep('''    B.seg(HC + Vector((0, -0.14, 0.045)), HC + Vector((0, -0.41, -0.035)), 0.032, 0.016, DARK, "Head",
          top=(0.5, 0.6))                                                                          # nose ridge''',
    '''    B.seg(HC + Vector((0, -0.30, 0.0)), HC + Vector((0, -0.42, -0.036)), 0.03, 0.014, DARK, "Head",
          top=(0.5, 0.6))                                                                          # nose ridge''')
rep('''    Rb = Euler((0, math.radians(-s * 22), math.radians(s * yaw)), "XYZ").to_matrix()
    B.add(c + Vector((0, 0, 0.040 * sc)) + n * 0.020, (0.078 * sc, 0.032, 0.026 * sc), DARK, bone, R=Rb,
          role="detail", bevel=0.010)                                                             # heavy brow''',
    '''    Rb = Euler((0, math.radians(-s * 22), math.radians(s * yaw)), "XYZ").to_matrix()
    B.add(c + Vector((0, 0, 0.034 * sc)) + n * 0.018 + Rb @ Vector((s * 0.008, 0, 0)), (0.066 * sc, 0.028, 0.017 * sc),
          DARK, bone, R=Rb, role="detail", bevel=0.008)                                          # heavy brow''')
rep('fierce_eye(B, HC + Vector((s * 0.080, -0.150, 0.030)), s, yaw=24, sc=1.12)',
    'fierce_eye(B, HC + Vector((s * 0.088, -0.160, 0.030)), s, yaw=24, sc=1.25)')
rep('''        B.spike(HC + Vector((s * 0.10, -0.10, 0.075)), (s * 0.35, 0.70, 0.62), 0.14, 0.026, DARK, "Head",
                top=(0.12, 0.3))                                                                   # brow spine''',
    '''        B.spike(HC + Vector((s * 0.135, -0.10, 0.06)), (s * 0.45, 0.85, 0.30), 0.16, 0.03, DARK, "Head",
                top=(0.12, 0.3))                                                                   # brow spine''')
rep('B.add(HC + Vector((s * 0.09, -0.115, 0.012)), (0.036, 0.03, 0.05)', 'B.add(HC + Vector((s * 0.10, -0.125, 0.006)), (0.036, 0.03, 0.05)')
# horns longer + thicker
rep('''        P = [HC + Vector((s * 0.085, -0.06, 0.11)), HC + Vector((s * 0.15, 0.10, 0.23)),
             HC + Vector((s * 0.21, 0.30, 0.30)), HC + Vector((s * 0.25, 0.54, 0.33))]
        tip = horn(B, P, 0.058, "Horn_" + side)''',
    '''        P = [HC + Vector((s * 0.09, -0.06, 0.12)), HC + Vector((s * 0.165, 0.11, 0.26)),
             HC + Vector((s * 0.235, 0.34, 0.345)), HC + Vector((s * 0.285, 0.64, 0.38))]
        tip = horn(B, P, 0.066, "Horn_" + side)''')
rep('B.add(HC + Vector((0, -0.145, 0.098)), (0.118, 0.022, 0.032), GOLD', 'B.add(HC + Vector((0, -0.150, 0.11)), (0.13, 0.022, 0.032), GOLD')
rep('B.seg(HC + Vector((s * 0.122, -0.14, 0.098)), HC + Vector((s * 0.12, 0.13, 0.092)), 0.016, 0.032, GOLD,',
    'B.seg(HC + Vector((s * 0.134, -0.15, 0.106)), HC + Vector((s * 0.132, 0.14, 0.10)), 0.016, 0.032, GOLD,')
rep('B.add(HC + Vector((0, 0.135, 0.092)), (0.11, 0.016, 0.03), GOLD_D', 'B.add(HC + Vector((0, 0.145, 0.10)), (0.12, 0.016, 0.03), GOLD_D')
rep('base = HC + Vector((x, -0.15, 0.115))', 'base = HC + Vector((x * 1.1, -0.155, 0.13))')
# bigger fins
rep('("Fin_1", N1.lerp(N2, 0.55), 0.22, 0.17, "Neck2", (0, 0.12, 0.0)),', '("Fin_1", N1.lerp(N2, 0.55), 0.28, 0.20, "Neck2", (0, 0.13, 0.0)),')
rep('("Fin_2", (N0 + Vector((0, 0.03, -0.05))).lerp(N1, 0.55), 0.29, 0.21, "Neck", (0, 0.14, 0.06)),',
    '("Fin_2", (N0 + Vector((0, 0.03, -0.05))).lerp(N1, 0.55), 0.38, 0.25, "Neck", (0, 0.15, 0.07)),')
rep('("Fin_3", Vector((0, -0.36, 1.0)), 0.38, 0.25, "Chest", None),', '("Fin_3", Vector((0, -0.36, 1.0)), 0.48, 0.32, "Chest", None),')
rep('("Fin_4", Vector((0, 0.08, 1.0)), 0.33, 0.23, "Spine", None),', '("Fin_4", Vector((0, 0.08, 1.0)), 0.42, 0.29, "Spine", None),')
rep('("Fin_5", Vector((0, 0.46, 1.0)), 0.26, 0.20, "Spine", None))', '("Fin_5", Vector((0, 0.46, 1.0)), 0.32, 0.24, "Spine", None))')
rep('ANCH["FX_FinSpark_" + nm[-1]] = tuple(frost_fin(B, base, h, ch, 0.07, nm))', 'ANCH["FX_FinSpark_" + nm[-1]] = tuple(frost_fin(B, base, h, ch, 0.075, nm))')
# dark dorsal stripe: along the neck back + the body top + the tail top (frames the white fins)
rep('''    # dark back line: small laid-back ridge scales between the fins, down to the tail''',
    '''    # dark dorsal stripe (the back line): a DARK band along the neck back, the body top and the tail top
    for a, b, bone, off, hw in ((N0 + Vector((0, 0.03, -0.05)), N1, "Neck", 0.17, 0.085), (N1, N2, "Neck2", 0.145, 0.07)):
        d = (b - a).normalized()
        bn = Vector((0, -d.z, d.y)) if d.z > 0 else Vector((0, d.z, -d.y))
        if bn.y < 0:
            bn = -bn
        B.seg(a + bn * (off - 0.03), b + bn * (off - 0.03), hw, 0.042, DARK, bone, ext=0.03, ext1=0.0, rnd=0.4)
    prev = None
    for y in (-0.62, -0.42, -0.20, 0.0, 0.20, 0.40, 0.60):
        p, n = surf_hit(B, tops, (0, y, 3.0), (0, 0, -1))
        if prev is not None:
            a, b = prev[0] + prev[1] * 0.004, p + n * 0.004
            B.bar(a, b, (prev[1] + n).normalized(), 0.15, 0.012, DARK, "Chest" if y <= -0.20 else "Spine",
                  studs=[], bevel=0.004)
        prev = (p, n)
    # dark back line: small laid-back ridge scales between the fins, down to the tail''')
# tail: dark top band + bigger crystal tip
rep('''        for t in (0.30, 0.75):
            p = a.lerp(b, t)''', '''        B.seg(a + Vector((0, 0, d - 0.025)), b + Vector((0, 0, dims[min(i + 1, 3)][1] * 0.82 - 0.025)), w * 0.55,
              0.02, DARK, bone, ext=0.02 if i else -0.04, top=(0.8, 1), rnd=0.4)                  # dorsal band
        for t in (0.30, 0.75):
            p = a.lerp(b, t)''')
rep('B.spike(main, tipd + Vector((0, 0, 0.18)), 0.24, 0.05, ICE_W', 'B.spike(main, tipd + Vector((0, 0, 0.18)), 0.32, 0.065, ICE_W')
rep('B.spike(main - tipd * 0.02, Vector((sx * 0.55, 0.7, 0.42)), 0.13, 0.034, ICE_W', 'B.spike(main - tipd * 0.02, Vector((sx * 0.55, 0.7, 0.42)), 0.19, 0.042, ICE_W')
rep('B.spike(main - tipd * 0.02, Vector((0, 0.45, 0.9)), 0.12, 0.032, ICE_BELLY', 'B.spike(main - tipd * 0.02, Vector((0, 0.45, 0.9)), 0.17, 0.04, ICE_BELLY')
rep('ANCH["FX_IceDust"] = tuple(main + (tipd + Vector((0, 0, 0.18))).normalized() * 0.22)', 'ANCH["FX_IceDust"] = tuple(main + (tipd + Vector((0, 0, 0.18))).normalized() * 0.30)')
rep('B.add(T[4], (0.06, 0.06, 0.045), DARK, "Tail_Tip"', 'B.add(T[4], (0.07, 0.07, 0.05), DARK, "Tail_Tip"')
# legs thicker
rep('(0.11, 0.15, 0.15), STEEL_BLUE, leg, rnd=0.40', '(0.125, 0.17, 0.17), STEEL_BLUE, leg, rnd=0.40')
rep('B.seg(H + Vector((0, 0, 0.06)), K, 0.095, 0.115, STEEL_BLUE, leg', 'B.seg(H + Vector((0, 0, 0.06)), K, 0.105, 0.13, STEEL_BLUE, leg')
rep('B.seg(K, A, 0.072, 0.078, STEEL_BLUE, shin, top=(0.84, 0.84)', 'B.seg(K, A, 0.082, 0.088, STEEL_BLUE, shin, top=(0.84, 0.84)')
rep('B.seg(H + Vector((0, 0.03, 0.08)), K, 0.11, 0.165, STEEL_BLUE, leg', 'B.seg(H + Vector((0, 0.03, 0.08)), K, 0.125, 0.185, STEEL_BLUE, leg')
rep('B.seg(K, A, 0.07, 0.08, STEEL_BLUE, shin, top=(0.80, 0.80)', 'B.seg(K, A, 0.078, 0.088, STEEL_BLUE, shin, top=(0.80, 0.80)')
rep('B.seg(A, P + Vector((0, 0.03, 0.03)), 0.058, 0.062, STEEL_BLUE, foot', 'B.seg(A, P + Vector((0, 0.03, 0.03)), 0.064, 0.068, STEEL_BLUE, foot')
rep('B.add(P, (0.085, 0.10, 0.048), STEEL_BLUE, foot', 'B.add(P, (0.095, 0.11, 0.05), STEEL_BLUE, foot')
rep('for gx in (-0.054, -0.018, 0.018, 0.054):', 'for gx in (-0.060, -0.020, 0.020, 0.060):')
open(p, "w", encoding="utf-8").write(s)
print("ok")
