p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\FrostfangLynx.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('''LEGS = {"F": ((0.108, -0.30, 0.585), (0.114, -0.235, 0.340), (0.118, -0.285, 0.095), (0.118, -0.335, 0.042)),
        "B": ((0.106, 0.30, 0.605), (0.112, 0.175, 0.380), (0.115, 0.365, 0.158), (0.115, 0.320, 0.042))}''',
    '''LEGS = {"F": ((0.108, -0.30, 0.555), (0.114, -0.235, 0.312), (0.118, -0.285, 0.085), (0.118, -0.335, 0.042)),
        "B": ((0.106, 0.30, 0.575), (0.112, 0.175, 0.352), (0.115, 0.365, 0.148), (0.115, 0.320, 0.042))}
DZ = -0.030                    # the whole body / head / tail sits this much lower than the coordinates below
BODYB = ("Chest", "Spine", "Neck", "Head", "Jaw", "Ear_L", "Ear_R", "Tail1", "Tail2", "Tail3")''')
rep('''def X(p, s):''', '''def bz(p):
    """body-group rest point (the body is lowered by DZ after it is built)"""
    return tuple(Vector(p) + Vector((0, 0, DZ)))


def X(p, s):''')
# tufts: thin pencils (2 per ear), slightly wider ear
rep('''        ear = B.add(root + R @ Vector((0, 0, 0.054)), (0.036, 0.015, 0.058), BACK_SHADE, "Ear_" + side, R=R,
                    top=(0.30, 0.6), rnd=0.25)''', '''        ear = B.add(root + R @ Vector((0, 0, 0.054)), (0.040, 0.015, 0.058), BACK_SHADE, "Ear_" + side, R=R,
                    top=(0.26, 0.6), rnd=0.25)''')
rep('''        B.spike(tip - R @ Vector((0, 0, 0.012)), R @ Vector((0, 0.12, 1)), 0.074, 0.016, ICE, "Ear_" + side,
                top=(0.08, 0.3))''', '''        for dx, L in ((-0.25, 0.066), (0.15, 0.054)):                       # the tuft: two thin ice pencils
            B.spike(tip - R @ Vector((0, 0, 0.014)), R @ Vector((s * dx * 0.5, 0.10, 1)), L, 0.0085, ICE,
                    "Ear_" + side, top=(0.15, 0.35))''')
# no chin tuft (goat beard); ruff flares sideways (sideburns)
rep('''    B.spike((0, -0.700, 0.810), (0, 0.15, -1), 0.052, 0.026, SNOW, "Jaw", top=(0.2, 0.4))
''', '')
rep('''        for y, z, d, L, w in ((-0.668, 0.818, (s * 0.25, 0.30, -0.92), 0.090, 0.028),
                              (-0.645, 0.826, (s * 0.55, 0.45, -0.70), 0.096, 0.030),
                              (-0.622, 0.846, (s * 0.80, 0.55, -0.38), 0.088, 0.028),
                              (-0.612, 0.878, (s * 0.85, 0.50, -0.05), 0.070, 0.024)):''',
    '''        for y, z, d, L, w in ((-0.664, 0.822, (s * 0.45, 0.35, -0.82), 0.080, 0.027),
                              (-0.645, 0.828, (s * 0.72, 0.45, -0.52), 0.098, 0.030),
                              (-0.622, 0.848, (s * 0.88, 0.50, -0.22), 0.094, 0.029),
                              (-0.610, 0.880, (s * 0.88, 0.48, 0.08), 0.070, 0.024)):''')
# thicker forearms / shins / socks
rep('''lo = B.seg(K, A, 0.050, 0.056, WARM_SILVER, shin, top=(0.86, 0.86), ext=0.03, ext1=0.02, rnd=0.40)''',
    '''lo = B.seg(K, A, 0.056, 0.062, WARM_SILVER, shin, top=(0.86, 0.86), ext=0.03, ext1=0.02, rnd=0.40)''')
rep('''B.seg(A + Vector((0, 0.005, 0.07)), A, 0.054, 0.058, SNOW, shin, ext1=0.02, rnd=0.40)''',
    '''B.seg(A + Vector((0, 0.005, 0.07)), A, 0.060, 0.064, SNOW, shin, ext1=0.02, rnd=0.40)''')
rep('''lo = B.seg(K, A, 0.050, 0.058, WARM_SILVER, shin, top=(0.82, 0.82), ext=0.03, ext1=0.02, rnd=0.40)''',
    '''lo = B.seg(K, A, 0.054, 0.062, WARM_SILVER, shin, top=(0.82, 0.82), ext=0.03, ext1=0.02, rnd=0.40)''')
rep('''B.seg(A, Pw + Vector((0, 0.03, 0.025)), 0.046, 0.046, SNOW, foot, ext=0.03, rnd=0.40)''',
    '''B.seg(A, Pw + Vector((0, 0.03, 0.025)), 0.050, 0.050, SNOW, foot, ext=0.03, rnd=0.40)''')
# bigger crescents in the rosettes
rep('''        blob(B, b, s, ly + math.cos(a) * r * 0.62, lz + math.sin(a) * r * 0.62, r * 0.50, seed + i, el=1.5,
             ang=ang + 120 * i + 90, n=7)''', '''        blob(B, b, s, ly + math.cos(a) * r * 0.64, lz + math.sin(a) * r * 0.64, r * 0.58, seed + i, el=1.45,
             ang=ang + 120 * i + 90, n=7)''')
# denser, bigger flank spots
rep('''            for i, (ly, lz, r, a, ros) in enumerate(((-0.150, 0.075, 0.040, 15, True), (-0.040, 0.105, 0.036, 70, False),
                                                     (0.075, 0.065, 0.040, 40, True), (-0.095, -0.020, 0.036, 120, False),
                                                     (0.020, -0.010, 0.042, 10, True), (0.120, -0.030, 0.032, 80, False),
                                                     (-0.010, 0.120, 0.026, 0, False))):''',
    '''            for i, (ly, lz, r, a, ros) in enumerate(((-0.150, 0.080, 0.046, 15, True), (-0.045, 0.110, 0.040, 70, False),
                                                     (0.075, 0.070, 0.048, 40, True), (-0.100, -0.015, 0.042, 120, False),
                                                     (0.015, -0.005, 0.050, 10, True), (0.125, -0.030, 0.038, 80, False),
                                                     (-0.180, -0.070, 0.030, 30, False), (0.180, 0.120, 0.030, 50, False),
                                                     (-0.050, -0.090, 0.032, 100, False), (0.075, -0.095, 0.030, 20, False))):''')
rep('''            for i, (ly, lz, r, a, ros) in enumerate(((-0.075, 0.035, 0.038, 30, True), (0.060, 0.050, 0.034, 70, False),
                                                     (0.000, -0.035, 0.030, 0, False))):''',
    '''            for i, (ly, lz, r, a, ros) in enumerate(((-0.070, 0.030, 0.046, 30, True), (0.065, 0.050, 0.040, 70, False),
                                                     (0.010, -0.045, 0.036, 0, False))):''')
rep('''            for i, (ly, lz, r, a, ros) in enumerate(((-0.060, 0.060, 0.040, 15, True), (0.070, 0.030, 0.036, 50, False),
                                                     (-0.005, -0.050, 0.038, 85, True), (0.085, -0.075, 0.028, 20, False))):''',
    '''            for i, (ly, lz, r, a, ros) in enumerate(((-0.060, 0.060, 0.048, 15, True), (0.070, 0.035, 0.042, 50, False),
                                                     (-0.010, -0.050, 0.046, 85, True), (0.090, -0.075, 0.034, 20, False),
                                                     (-0.100, -0.060, 0.030, 60, False))):''')
rep('''                blob(B, up, s, 0.010, -0.040, 0.030, sd, el=1.1, ang=70)
                blob(B, up, s, -0.020, 0.060, 0.024, sd + 3, el=1.2, ang=20)
                blob(B, lo, s, 0.000, -0.050, 0.020, sd + 5, el=1.2, ang=80)''',
    '''                blob(B, up, s, 0.010, -0.040, 0.034, sd, el=1.1, ang=70)
                blob(B, up, s, -0.020, 0.060, 0.028, sd + 3, el=1.2, ang=20)
                blob(B, lo, s, 0.000, -0.050, 0.024, sd + 5, el=1.2, ang=80)
                blob(B, lo, s, 0.010, 0.040, 0.020, sd + 7, el=1.2, ang=10)''')
rep('''                rosette(B, up, s, 0.000, -0.050, 0.040, sd, ang=20)
                blob(B, up, s, 0.020, 0.060, 0.028, sd + 3, el=1.2, ang=60)
                blob(B, lo, s, 0.000, -0.040, 0.020, sd + 5, el=1.2, ang=80)''',
    '''                rosette(B, up, s, 0.000, -0.050, 0.048, sd, ang=20)
                blob(B, up, s, 0.020, 0.065, 0.032, sd + 3, el=1.2, ang=60)
                blob(B, lo, s, 0.000, -0.040, 0.024, sd + 5, el=1.2, ang=80)''')
# lower the body group before build
rep('''    B.build()
    bk.stud_skin(k, PITCH)''', '''    dz = Vector((0, 0, DZ))
    for blk in B.items:
        if blk.bone in BODYB:
            if hasattr(blk, "pts"):
                blk.pts = [q + dz for q in blk.pts]
            blk.c = blk.c + dz
    B.build()
    bk.stud_skin(k, PITCH)''')
# rig: body joints lowered
rep('''    k.joint("Spine", (0, 0.16, 0.65), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.08, 0.65), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.34, 0.685), "Chest", tail=(0, -0.15, 0.14))
    k.joint("Head", tuple(HJ), "Neck", tail=(0, -0.25, 0.0))                  # throat pivot
    k.joint("Jaw", tuple(hs((0, -0.605, 0.826))), "Head", tail=(0, -0.15, 0))''',
    '''    k.joint("Spine", bz((0, 0.16, 0.65)), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", bz((0, -0.08, 0.65)), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", bz((0, -0.34, 0.685)), "Chest", tail=(0, -0.15, 0.14))
    k.joint("Head", bz(HJ), "Neck", tail=(0, -0.25, 0.0))                     # throat pivot
    k.joint("Jaw", bz(hs((0, -0.605, 0.826))), "Head", tail=(0, -0.15, 0))''')
rep('''        k.joint("Ear_" + side, tuple(hs((s * 0.060, -0.585, 0.985))), "Head", tail=(s * 0.02, 0, 0.1))
        k.joint("FX_IceDust_" + side, tuple(hs((s * 0.068, -0.575, 1.150))), "Ear_" + side, tail=(0, 0, 0.05))''',
    '''        k.joint("Ear_" + side, bz(hs((s * 0.060, -0.585, 0.985))), "Head", tail=(s * 0.02, 0, 0.1))
        k.joint("FX_IceDust_" + side, bz(hs((s * 0.066, -0.575, 1.140))), "Ear_" + side, tail=(0, 0, 0.05))''')
rep('''        k.joint("Tail%d" % (i + 1), TAILP[i], "Spine" if i == 0 else "Tail%d" % i,
                tail=tuple(Vector(TAILP[i + 1]) - Vector(TAILP[i])))
    k.joint("FX_SnowFlick", TAILP[3], "Tail3", tail=(0, 0.05, -0.03))''',
    '''        k.joint("Tail%d" % (i + 1), bz(TAILP[i]), "Spine" if i == 0 else "Tail%d" % i,
                tail=tuple(Vector(TAILP[i + 1]) - Vector(TAILP[i])))
    k.joint("FX_SnowFlick", bz(TAILP[3]), "Tail3", tail=(0, 0.05, -0.03))''')
rep('''    return [((0, -0.52, 0.82), (0, -0.56, 0.89), 0.14, "Head")]''',
    '''    return [(bz((0, -0.52, 0.82)), bz((0, -0.56, 0.89)), 0.14, "Head")]''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
