# review 1 (REVISE 5/10): MUST 1-7 + NICE 1 (body split approved by the lead)
p = "pets/EclipseSeraph.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


# MUST 1 body split + lilac wings B / C
rep("MOON_IVORY = (232, 208, 240)  # body, legs, head, wing arms + upper coverts (studded; lilac ivory)",
    "MOON_IVORY = (232, 208, 240)  # face, head, neck, shoulders, wing arms + coverts (studded; lilac ivory)\n"
    "BODY_MID = (206, 160, 232)    # mid lilac: chest, tuck, waist, hips, legs, paws, tail (review 1 MUST 1)\n"
    "WING_LILAC = (214, 186, 236)  # flight feathers of the middle + lower wing pairs (review 1 MUST 1)")
rep('B.add((0, -0.354, 0.838), (0.26, 0.425, 0.319), MOON_IVORY, "Chest"', 'B.add((0, -0.354, 0.838), (0.26, 0.425, 0.319), BODY_MID, "Chest"')
rep('B.seg((0, -0.059, 0.566), (0, 0.472, 0.679), 0.177, 0.094, MOON_IVORY, "Spine"', 'B.seg((0, -0.059, 0.566), (0, 0.472, 0.679), 0.177, 0.094, BODY_MID, "Spine"')
rep('B.add((0, 0.189, 0.861), (0.195, 0.283, 0.195), MOON_IVORY, "Spine"', 'B.add((0, 0.189, 0.861), (0.195, 0.283, 0.195), BODY_MID, "Spine"')
rep('B.add((0, 0.543, 0.873), (0.218, 0.248, 0.212), MOON_IVORY, "Spine"', 'B.add((0, 0.543, 0.873), (0.218, 0.248, 0.212), BODY_MID, "Spine"')
rep('''        feather(B, a - nrm * 0.016, end - nrm * 0.016, nrm, fw, 0.03, IVORY_D if rows3 else WING_IN, wb,
                taper=0.35, tipc=OBSID, tipf=0.19, bev=bev)''',
    '''        feather(B, a - nrm * 0.016, end - nrm * 0.016, nrm, fw, 0.03, IVORY_D if rows3 else WING_LILAC, wb,
                taper=0.35, tipc=OBSID, tipf=0.12, bev=bev)''')
rep('''        feather(B, a + nrm * 0.018, end + nrm * 0.018, nrm, fw * 0.80, 0.032, MOON_IVORY if rows3 else WING_IN, wb,''',
    '''        feather(B, a + nrm * 0.018, end + nrm * 0.018, nrm, fw * 0.80, 0.032, MOON_IVORY, wb,''')
rep('''        tipp = feather(B, W + dv * 0.04 + o, W + dv * ln + o, nrm, fw * 0.90, 0.03, WING_IN, tb, taper=0.22,
                       tipc=OBSID, tipf=0.25, bev=bev)''',
    '''        tipp = feather(B, W + dv * 0.04 + o, W + dv * ln + o, nrm, fw * 0.90, 0.03, WING_IN if rows3 else WING_LILAC,
                       tb, taper=0.22, tipc=OBSID, tipf=0.15, bev=bev)''')
# MUST 3 lion mass: head, muzzle, nose, forelegs, paws, tail
rep('B.add(HC, (0.177, 0.13, 0.136), MOON_IVORY, "Head", top=(0.84, 0.85))', 'B.add(HC, (0.20, 0.14, 0.145), MOON_IVORY, "Head", top=(0.84, 0.85))')
rep('''HC + Vector((0, -0.283, -0.029)), 0.10, 0.071, MOON_IVORY, "Head",''', '''HC + Vector((0, -0.29, -0.029)), 0.12, 0.08, MOON_IVORY, "Head",''')
rep('''        B.add(HC + Vector((s * 0.068, -0.201, -0.088)), (0.073, 0.0885, 0.059), WING_IN, "Head", rnd=0.4)  # pads''',
    '''        B.add(HC + Vector((s * 0.078, -0.208, -0.092)), (0.085, 0.095, 0.066), WING_IN, "Head", rnd=0.4)  # pads''')
rep('''    B.add(HC + Vector((0, -0.300, -0.020)), (0.052, 0.03, 0.032), BLACK, "Head", role="detail", bevel=0.008,''',
    '''    B.add(HC + Vector((0, -0.312, -0.018)), (0.066, 0.034, 0.04), BLACK, "Head", role="detail", bevel=0.009,''')
rep('''HC + Vector((0, -0.285, 0.03)), 0.036, 0.012, IVORY_D, "Head",''', '''HC + Vector((0, -0.295, 0.035)), 0.04, 0.012, IVORY_D, "Head",''')
rep('''        B.spike(HC + Vector((s * 0.068, -0.248, -0.130)), (0, -0.1, -1), 0.10, 0.02, IVORY, "Head")       # canines
        for y in (-0.189, -0.142):
            B.spike(HC + Vector((s * 0.083, y, -0.130)), (0, 0, -1), 0.04, 0.014, IVORY, "Head")''',
    '''        B.spike(HC + Vector((s * 0.08, -0.258, -0.136)), (0, -0.1, -1), 0.11, 0.022, IVORY, "Head")       # canines
        for y in (-0.195, -0.145):
            B.spike(HC + Vector((s * 0.095, y, -0.136)), (0, 0, -1), 0.045, 0.015, IVORY, "Head")''')
rep('''    B.add(HC + Vector((0, -0.177, -0.136)), (0.088, 0.088, 0.007), MOUTH, "Head"''', '''    B.add(HC + Vector((0, -0.183, -0.142)), (0.10, 0.092, 0.007), MOUTH, "Head"''')
rep('''    B.seg(HC + Vector((0, -0.048, -0.171)), HC + Vector((0, -0.260, -0.183)), 0.094, 0.035, WING_IN, "Jaw",''',
    '''    B.seg(HC + Vector((0, -0.048, -0.177)), HC + Vector((0, -0.268, -0.189)), 0.11, 0.035, WING_IN, "Jaw",''')
rep('''    B.add(HC + Vector((0, -0.165, -0.141)), (0.075, 0.088, 0.007), MOUTH, "Jaw"''', '''    B.add(HC + Vector((0, -0.170, -0.147)), (0.088, 0.09, 0.007), MOUTH, "Jaw"''')
rep('''        B.spike(HC + Vector((s * 0.057, -0.24, -0.155)), (0, 0, 1), 0.06, 0.016, IVORY, "Jaw")''',
    '''        B.spike(HC + Vector((s * 0.066, -0.248, -0.161)), (0, 0, 1), 0.065, 0.017, IVORY, "Jaw")''')
# MUST 5 eyes sc 1.25 -> 1.6 (set a little wider on the wider skull)
rep('''        eye(B, HC + Vector((s * 0.090, -0.124, 0.040)), s, sc=1.25)''', '''        eye(B, HC + Vector((s * 0.104, -0.134, 0.044)), s, sc=1.6)''')
rep('''        ear = B.add(HC + Vector((s * 0.14, 0.06, 0.16)), (0.05, 0.024, 0.055), OBSID, "Head",''',
    '''        ear = B.add(HC + Vector((s * 0.16, 0.06, 0.17)), (0.05, 0.024, 0.055), OBSID, "Head",''')
# MUST 2 the mane: denser, wider, swept back; bib 5; cape down the chest
rep('''    for ring, (r0, L, w, n, y, bone, skip) in enumerate(((0.165, 0.13, 0.05, 14, 0.04, "Head", 0.88),
                                                       (0.215, 0.25, 0.065, 14, 0.11, "Head", 0.94),
                                                       (0.27, 0.33, 0.08, 16, 0.19, "Mane", 1.1))):''',
    '''    for ring, (r0, L, w, n, y, bone, skip) in enumerate(((0.185, 0.14, 0.07, 22, 0.04, "Head", 0.88),
                                                       (0.235, 0.26, 0.085, 22, 0.11, "Head", 0.94),
                                                       (0.29, 0.34, 0.10, 24, 0.19, "Mane", 1.1))):''')
rep('''            tuft(B, root, d + Vector((0, 0.42 + 0.12 * ring, 0)), Li, w, OBSID, bone)''',
    '''            tuft(B, root, d + Vector((0, 0.9 + 0.12 * ring, 0)), Li, w, OBSID, bone)''')
rep('''    B.add((0, -0.555, 1.015), (0.30, 0.20, 0.25), OBSID, "Chest", rnd=0.36, top=(0.72, 0.8), bot=(0.85, 0.9))  # cape''',
    '''    B.add((0, -0.56, 0.96), (0.30, 0.21, 0.31), OBSID, "Chest", rnd=0.36, top=(0.72, 0.8), bot=(0.80, 0.9))  # cape''')
rep('''    for x, L in ((0.0, 0.34), (0.12, 0.28), (-0.12, 0.28)):                                     # chest bib
        tuft(B, Vector((x, -0.99, 0.92)), (x * 0.5, 0.15, -1), L, 0.085, OBSID, "Neck")''',
    '''    for x, L in ((0.0, 0.36), (0.09, 0.31), (-0.09, 0.31), (0.17, 0.25), (-0.17, 0.25)):         # chest bib
        tuft(B, Vector((x, -0.99, 0.92)), (x * 0.5, 0.15, -1), L, 0.09, OBSID, "Neck")''')
# legs / paws (BODY_MID) bigger forelegs and paws
rep('''                B.seg(H + Vector((0, 0, 0.094)), K, 0.112, 0.148, MOON_IVORY, leg, ext1=0.035, top=(0.85, 0.75))
                B.seg(K, A, 0.097, 0.097, MOON_IVORY, shin, top=(0.85, 0.88), ext=0.035, ext1=0.024)''',
    '''                B.seg(H + Vector((0, 0, 0.094)), K, 0.13, 0.165, BODY_MID, leg, ext1=0.035, top=(0.85, 0.75))
                B.seg(K, A, 0.11, 0.108, BODY_MID, shin, top=(0.85, 0.88), ext=0.035, ext1=0.024)''')
rep('''                B.seg(H + Vector((0, 0.035, 0.094)), K, 0.092, 0.177, MOON_IVORY, leg,''', '''                B.seg(H + Vector((0, 0.035, 0.094)), K, 0.092, 0.177, BODY_MID, leg,''')
rep('''                B.seg(K, A, 0.077, 0.089, MOON_IVORY, shin, top=(0.80, 0.80), ext=0.035, ext1=0.024)
                B.seg(A, P + Vector((0, 0.035, 0.041)), 0.065, 0.068, MOON_IVORY, foot, ext=0.035)''',
    '''                B.seg(K, A, 0.077, 0.089, BODY_MID, shin, top=(0.80, 0.80), ext=0.035, ext1=0.024)
                B.seg(A, P + Vector((0, 0.035, 0.041)), 0.065, 0.068, BODY_MID, foot, ext=0.035)''')
rep('''            B.add(P, (0.106, 0.118, 0.059), MOON_IVORY, foot, top=(0.85, 0.80))                        # paw
            B.add(P + Vector((0, -0.02, -0.047)), (0.10, 0.10, 0.012), IVORY_D, foot, studs=[], role="detail",''',
    '''            B.add(P, (0.12, 0.13, 0.062), BODY_MID, foot, top=(0.85, 0.80))                            # paw
            B.add(P + Vector((0, -0.02, -0.05)), (0.114, 0.112, 0.012), IVORY_D, foot, studs=[], role="detail",''')
rep('''            for gx in (-0.064, -0.021, 0.021, 0.064):
                B.spike((P.x + gx, P.y - 0.104, 0.047), (0, -1, -0.55), 0.077, 0.017, BLACK, foot)''',
    '''            for gx in (-0.072, -0.024, 0.024, 0.072):
                B.spike((P.x + gx, P.y - 0.116, 0.05), (0, -1, -0.55), 0.084, 0.018, BLACK, foot)''')
rep('''TAILP = [(0, 0.78, 0.98), (0, 1.10, 0.90), (0, 1.40, 0.70), (0, 1.62, 0.44), (0, 1.72, 0.22)]''',
    '''TAILP = [(0, 0.78, 0.98), (0, 1.08, 0.90), (0, 1.36, 0.71), (0, 1.57, 0.47), (0, 1.66, 0.26)]''')
rep('''        B.seg(a, b, w, w * 1.08, MOON_IVORY, "Tail%d" % (i + 1),''', '''        B.seg(a, b, w, w * 1.08, BODY_MID, "Tail%d" % (i + 1),''')
rep('''    B.add(tip + Vector((0, 0.02, -0.01)), (0.075, 0.085, 0.075), OBSID, "Tail4", rnd=0.4)''',
    '''    B.add(tip + Vector((0, 0.02, -0.01)), (0.10, 0.11, 0.095), OBSID, "Tail4", rnd=0.4)''')
# MUST 4 halo stands up, same top; MUST 5 rim + corona
rep('''HALO_C = HC + Vector((0, 0.22, 0.74))''', '''HALO_C = HC + Vector((0, 0.22, 0.60))''')
rep('''HALO_TILT = 20.0                                  # the disc faces forward-up by 20 deg''',
    '''HALO_TILT = 40.0                                  # the disc faces forward-up by 40 deg (review 1 MUST 4)''')
rep('''    rim_o, rim_i = HALO_R, HALO_R - 0.045''', '''    rim_o, rim_i = HALO_R, HALO_R - 0.075''')
rep('''arc(rim_i - 0.032, lo)), (arc(rim_i, hi), arc(rim_i - 0.032, hi))], BLOOD''', '''arc(rim_i - 0.07, lo)), (arc(rim_i, hi), arc(rim_i - 0.07, hi))], BLOOD''')
# MUST 6 lower pair root up 0.03; NICE 1 lower pair display up 18
rep('''WC, H2C, TC = make_wing("C", (0.25, 0.06, 1.02), (0.235, 0.32, 1.00), (0.46, 0.22, 1.00), (0.42, 0.62, 0.97),
                        (0.74, 1.12, 0.95), -2.0)''',
    '''WC, H2C, TC = make_wing("C", (0.25, 0.06, 1.05), (0.235, 0.32, 1.03), (0.46, 0.22, 1.03), (0.42, 0.62, 1.00),
                        (0.74, 1.12, 0.98), -2.0)''')
rep('''"C": (10.0, -10.0, 0.0, -6.0)}''', '''"C": (18.0, -10.0, 0.0, -6.0)}''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
