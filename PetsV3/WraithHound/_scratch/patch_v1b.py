p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\WraithHound.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (a[:70], s.count(a))
    s = s.replace(a, b)


# ---- mane = billowing columns of rounded soot puffs ending in a curled indigo wisp
i0 = s.index("def plume(")
i1 = s.index("def model(k):")
s = s[:i0] + '''def column(B, root, d0, d1, r0, n, bone, shrink=0.80, wisp=True, side=(1, 0, 0)):
    """a smoke column: n rounded soot puffs (radius r0, shrinking) along a path that bends from d0 to d1, ending in a
    curled indigo wisp; consecutive puffs overlap ~30 %. Returns the wisp tip."""
    import blockkit as bk
    p = Vector(root)
    r = r0
    d0, d1 = Vector(d0).normalized(), Vector(d1).normalized()
    for i in range(n):
        t = i / max(1, n - 1)
        d = (d0 * (1 - t) + d1 * t).normalized()
        R = bk.frame_from(p, p + d, side)
        B.add(p, (r * 1.05, r * 1.10, r), SOOT, bone, R=R, top=(0.86, 0.86), rnd=0.45)
        if i < n - 1:
            rn = r * shrink
            p = p + d * 0.70 * (r + rn)
            r = rn
    tip = p
    if wisp:
        b = p + d1 * (r * 0.55)
        dw = (d1 + Vector((0, 0.35, -0.25))).normalized()
        tip = b + dw * (r * 2.6)
        B.spike(b, dw, r * 2.6, r * 0.78, INDIGO, bone, side=side, top=(0.12, 0.30), nostud=True)
    return tip


MANE_COLS = {   # per row: (dx, dz, d0, d1, r0 factor, n) - centre column + side columns (L mirrored to R)
    "C": (0.0, 0.0, (0, 0.30, 1.0), (0, 1.0, 0.30), 1.00, 4),
    "S": (0.058, -0.022, (0.30, 0.42, 1.0), (0.18, 1.0, 0.10), 0.80, 4),
}


def mane_row(B, bone, root, sc):
    """one mane row: a tall centre column (bone) + two side columns splayed out (bone_L / bone_R, fan-out)"""
    out = {}
    dx, dz, d0, d1, f, n = MANE_COLS["C"]
    out["C"] = column(B, root, d0, d1, 0.072 * sc * f, n, bone)
    dx, dz, d0, d1, f, n = MANE_COLS["S"]
    for s_, sd in ((1, "L"), (-1, "R")):
        r = root + Vector((s_ * dx, 0.02, dz))
        out[sd] = column(B, r, (s_ * d0[0], d0[1], d0[2]), (s_ * d1[0], d1[1], d1[2]), 0.072 * sc * f, n,
                         bone + "_" + sd)
    return out


''' + s[i1:]
rep('''MANE = [("Mane1", "Neck", Vector((0, -0.66, 1.03)), 0.85),
        ("Mane2", "Chest", Vector((0, -0.42, 0.93)), 1.00),
        ("Mane3", "Spine", Vector((0, -0.14, 0.89)), 0.80)]''',
    '''MANE = [("Mane1", "Neck", Vector((0, -0.64, 0.995)), 0.95),
        ("Mane2", "Chest", Vector((0, -0.40, 0.915)), 1.20),
        ("Mane3", "Spine", Vector((0, -0.13, 0.885)), 0.95)]''')
rep('''    tips = {}
    for bone, parent, root, sc in MANE:
        tips[bone] = mane_row(B, bone, root, sc)''', '''    global MANE_TIPS
    MANE_TIPS = {}
    for bone, parent, root, sc in MANE:
        MANE_TIPS[bone] = mane_row(B, bone, root, sc)''')
# rig: wisp anchors at the computed centre tips (model() runs before rig())
rep('''        tip = mane_tip(root, sc)
        k.joint("FX_SmokeWisp_%d" % (i + 1), tuple(tip), bone, tail=(0, 0.06, 0.02))''',
    '''        k.joint("FX_SmokeWisp_%d" % (i + 1), tuple(MANE_TIPS[bone]["C"]), bone, tail=(0, 0.06, 0.02))''')
rep('''def mane_tip(root, sc):
    p = Vector(root)
    for dv, L in (((0, 0.34, 1.0), 0.19 * sc), ((0, 0.85, 0.75), 0.16 * sc), ((0, 1.0, 0.20), 0.15 * sc)):
        p = p + Vector(dv).normalized() * L
    return p


''', '''MANE_TIPS = {}


''')
# ---- mist muzzle + jaw + cheeks lower half; bigger chest front
rep('''    B.seg((0, -0.95, 0.968), (0, -1.165, 0.962), 0.070, 0.026, MIST, "Head", top=(0.72, 0.9))          # mist lip''',
    '''    B.seg((0, -0.99, 0.985), (0, -1.168, 0.975), 0.073, 0.040, MIST, "Head", top=(0.74, 0.86), ext=0.01)  # muzzle
    for s in (1, -1):                                                                       # mist cheek / jowl
        B.add((s * 0.082, -0.90, 0.962), (0.038, 0.070, 0.024), MIST, "Head", rot=(0, 0, s * 8), rnd=0.40)''')
rep('''    B.add((0, -0.565, 0.68), (0.110, 0.028, 0.150), MIST, "Chest", bot=(0.40, 0.8), top=(0.95, 1), rot=(-14, 0, 0),
          rnd=0.35)''', '''    B.add((0, -0.567, 0.66), (0.122, 0.030, 0.175), MIST, "Chest", bot=(0.40, 0.8), top=(0.95, 1), rot=(-14, 0, 0),
          rnd=0.35)''')
rep('''    B.seg((0, -0.10, 0.500), (0, 0.24, 0.628), 0.072, 0.020, MIST, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)''',
    '''    B.seg((0, -0.10, 0.500), (0, 0.24, 0.628), 0.090, 0.024, MIST, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)''')
# ---- thicker legs
rep('''B.seg(K, A, 0.044, 0.050, ASH_LAV, shin, top=(0.85, 0.85), ext=0.03, ext1=0.02, rnd=0.40)''',
    '''B.seg(K, A, 0.050, 0.056, ASH_LAV, shin, top=(0.85, 0.85), ext=0.03, ext1=0.02, rnd=0.40)''')
rep('''B.seg(K, A, 0.046, 0.054, ASH_LAV, shin, top=(0.80, 0.80), ext=0.03, ext1=0.02, rnd=0.40)''',
    '''B.seg(K, A, 0.052, 0.060, ASH_LAV, shin, top=(0.80, 0.80), ext=0.03, ext1=0.02, rnd=0.40)''')
rep('''B.seg(A, Pw + Vector((0, 0.03, 0.025)), 0.040, 0.042, ASH_LAV, foot, ext=0.03, rnd=0.40)''',
    '''B.seg(A, Pw + Vector((0, 0.03, 0.025)), 0.046, 0.048, ASH_LAV, foot, ext=0.03, rnd=0.40)''')
rep('''            B.add(Pw, (0.050, 0.070, 0.036), SOOT, foot, top=(0.86, 0.80), rnd=0.35)              # narrow paw''',
    '''            B.add(Pw, (0.054, 0.072, 0.036), SOOT, foot, top=(0.86, 0.80), rnd=0.35)              # narrow paw''')
# ---- bushier tail: thicker, smoother, a fuller tuft
rep('''    for i, ((a, b), (w, d)) in enumerate(zip(zip(P, P[1:]), ((0.042, 0.050), (0.044, 0.050), (0.046, 0.052),
                                                             (0.050, 0.056)))):
        B.seg(a, b, w, d, ASH_LAV if i == 0 else SOOT, "Tail%d" % (i + 1), ext=0.035, top=(0.92, 0.92), rnd=0.40)
    B.spike(P[4] - Vector((0, 0.03, -0.01)), (0, 0.45, -0.9), 0.10, 0.050, SOOT, "Tail4", top=(0.20, 0.30))   # tuft''',
    '''    for i, ((a, b), (w, d)) in enumerate(zip(zip(P, P[1:]), ((0.046, 0.056), (0.054, 0.064), (0.060, 0.070),
                                                             (0.064, 0.074)))):
        B.seg(a, b, w, d, ASH_LAV if i == 0 else SOOT, "Tail%d" % (i + 1), ext=0.045, ext1=0.02, top=(0.94, 0.94),
              rnd=0.45)
    B.spike(P[4] - Vector((0, 0.04, -0.02)), (0, 0.40, -0.92), 0.13, 0.062, SOOT, "Tail4", top=(0.20, 0.30))  # tuft''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
