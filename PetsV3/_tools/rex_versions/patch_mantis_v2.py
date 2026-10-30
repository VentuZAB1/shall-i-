# Thornblade Mantis v2 (review 1 fixes 0-8). Plain python; rewrites the constants, model() and the antenna joint.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\ThornbladeMantis.py"
s = open(p, encoding="utf-8").read()
R = []
R.append(('''LEGS = {"F": ((0.12, -0.06, 0.42), (0.40, -0.22, 0.66), (0.52, -0.42, 0.11), (0.56, -0.54, 0.02)),
        "B": ((0.12, 0.14, 0.42), (0.42, 0.30, 0.66), (0.54, 0.60, 0.11), (0.58, 0.72, 0.02))}''',
'''LEGS = {"F": ((0.12, -0.06, 0.42), (0.35, -0.22, 0.64), (0.45, -0.40, 0.11), (0.48, -0.51, 0.02)),     # FIX 8
        "B": ((0.12, 0.14, 0.42), (0.37, 0.30, 0.64), (0.47, 0.56, 0.11), (0.50, 0.67, 0.02))}'''))
R.append(('''HC = Vector((0, -0.50, 1.10))                                     # head centre''',
          '''HC = Vector((0, -0.52, 1.14))                                     # head centre (FIX 1: +30 % head)'''))
R.append(('''ARM = (Vector((0.07, -0.30, 0.82)), Vector((0.15, -0.42, 0.58)), Vector((0.165, -0.60, 0.90)),
       Vector((0.16, -0.63, 0.62)))''',
'''ARM = (Vector((0.08, -0.30, 0.84)), Vector((0.17, -0.46, 0.62)), Vector((0.21, -0.64, 1.00)),     # FIX 4: knee at
       Vector((0.20, -0.73, 0.66)))                                                                # head height'''))
R.append(('''def leaf(s, t, w):''', '''ANT0 = (0.03, -0.095, 0.105)          # antenna root offset from HC (above the V-brow)
ANT1 = (0.05, -0.07, 0.15)


def surf_hit(B, blks, origin, direction):
    import blockkit as bk
    from mathutils.bvhtree import BVHTree
    B._resolve()
    best = None
    d = Vector(direction).normalized()
    for blk in blks:
        bm = bk.part_bm(blk)
        t = BVHTree.FromBMesh(bm)
        bm.free()
        loc, nrm, _, dist = t.ray_cast(Vector(origin), d)
        if loc is not None and (best is None or dist < best[2]):
            best = (loc, nrm.normalized(), dist)
    if best is None:
        raise RuntimeError("surf_hit: no surface from %s" % (tuple(origin),))
    return best[0], best[1]


def disc(B, c, r, color, bone, sx=0.75, sy=1.15, thick=0.012, dz=0.0):
    pts = [c + Vector((r * sx * math.cos(a), r * sy * math.sin(a), dz)) for a in
           [2 * math.pi * i / 12 for i in range(12)]]
    B.poly([c + Vector((0, 0, dz))] + pts + [pts[0]], thick, color, bone)


def leaf(s, t, w):'''))
# ---- abdomen (FIX 6)
R.append(('''        B.seg(a, b, w, d, HIDE, bone, ext=0.06 if i == 0 else 0.02, ext1=0.02, top=(0.9 if i < 2 else 0.55, 0.85))
        B.seg(a + Vector((0, 0, -d + 0.01)), b + Vector((0, 0, -d * 0.8 + 0.01)), w * 0.75, 0.014, BELLY, bone,
              ext=0.01)
        for t in (0.3, 0.75):
            p = a.lerp(b, t)
            B.seg(p - (b - a).normalized() * 0.018, p + (b - a).normalized() * 0.018, w * (1.03 - 0.25 * t * (i == 2)),
                  d * 1.04, ARMOR, bone, top=(0.98, 0.98))                                    # tergite ring''',
'''        B.seg(a, b, w, d, HIDE, bone, ext=0.06 if i == 0 else 0.02, ext1=0.02, top=(0.9 if i < 2 else 0.55, 0.85))
        B.seg(a + Vector((0, 0, -d + 0.02)), b + Vector((0, 0, -d * 0.8 + 0.02)), w * 0.98, 0.03, BELLY, bone,
              ext=0.01, top=(0.9 if i < 2 else 0.6, 1))                                       # sternites (FIX 6)
        u = (b - a).normalized()
        p = a.lerp(b, 0.85)
        tw = 1.04 if i < 2 else 0.80
        B.seg(p - u * 0.022 + Vector((0, 0, d * 0.40)), p + u * 0.022 + Vector((0, 0, d * 0.40)), w * tw, d * 0.62,
              ARMOR, bone, top=(0.98, 0.98))                                                 # tergite band (upper 60 %)
        B.seg(p - u * 0.014 + Vector((0, 0, -d * 0.8 + 0.02)), p + u * 0.014 + Vector((0, 0, -d * 0.8 + 0.02)),
              w * 0.99 * (1 if i < 2 else 0.7), 0.034, BELLY_D, bone, studs=[])                # sternite gap bar'''))
# ---- hindwings: two-sided, bigger eye-spots (FIX 7 W1)
R.append(('''        eye = leaf(s, 0.55, 0.45) - Vector((0, 0, 0.026))
        for r, c, dz in ((0.085, BLACK, 0.0), (0.062, RUBY_D, 0.004), (0.046, RUBY, 0.008), (0.018, RUBY_HOT, 0.012)):
            pts = [eye + Vector((r * 0.75 * math.cos(a), r * 1.15 * math.sin(a), dz)) for a in
                   [2 * math.pi * i / 12 for i in range(12)]]
            B.poly([eye + Vector((0, 0, dz))] + pts + [pts[0]], 0.012, c, hb)''',
'''        eye = leaf(s, 0.55, 0.45) - Vector((0, 0, 0.026))
        sc = 0.10 / 0.085
        for r, c, dz in ((0.085, BLACK, 0.0), (0.062, RUBY_D, 0.004), (0.046, RUBY, 0.008), (0.018, RUBY_HOT, 0.012)):
            disc(B, eye, r * sc, c, hb, dz=dz)                                                  # top face
            disc(B, eye, r * sc, c, hb, dz=-0.016 - dz / 0.004 * 0.004)                          # underside (FIX 7)'''))
# ---- tegmina: wider dark rim (W3) + ruby stigma (W2)
R.append(('''        inner = [leaf(s, t, 0.86) + Vector((0, 0, 0.006)) for t in (0.08, 0.3, 0.5, 0.7, 0.84)]
        inner += [leaf(s, t, 0.12) + Vector((0, 0, 0.006)) for t in (0.84, 0.6, 0.3, 0.08)]''',
'''        inner = [leaf(s, t, 0.80) + Vector((0, 0, 0.006)) for t in (0.08, 0.3, 0.5, 0.7, 0.84)]
        inner += [leaf(s, t, 0.16) + Vector((0, 0, 0.006)) for t in (0.84, 0.6, 0.3, 0.08)]'''))
R.append(('''            B.bar(a, b, Vector((0, 0, 1)), 0.012, 0.006, ARMOR, eb, studs=[], bevel=0.002)      # side veins''',
'''            B.bar(a, b, Vector((0, 0, 1)), 0.012, 0.006, ARMOR, eb, studs=[], bevel=0.002)      # side veins
        st = leaf(s, 0.42, 0.72)
        for i, (r, c) in enumerate(((0.035, RUBY_D), (0.025, RUBY), (0.012, RUBY_HOT))):        # ruby stigma (W2)
            disc(B, st, r, c, eb, sx=1.0, sy=1.3, thick=0.006, dz=0.014 + 0.004 * i)'''))
# ---- prothorax shield (FIX 5) replaces keel + flares; throat tie shortened
R.append(('''    B.seg(PRO[0].lerp(PRO[1], 0.08), PRO[1], 0.035, 0.085, ARMOR, "Chest", top=(0.7, 0.9))           # dorsal keel
    d = (PRO[1] - PRO[0]).normalized()
    nrm = Vector((0, 0.8, -0.6)).normalized()
    B.seg(PRO[0].lerp(PRO[1], 0.15) - nrm * 0.0 + Vector((0, -0.05, -0.04)),
          PRO[1] + Vector((0, -0.05, -0.05)), 0.06, 0.03, BELLY, "Chest", top=(0.8, 1))                # throat
    for t, w in ((0.55, 0.13), (0.78, 0.115)):                                               # pronotum flares
        p = PRO[0].lerp(PRO[1], t)
        B.seg(p - d * 0.05, p + d * 0.05, w, 0.05, ARMOR, "Chest", top=(0.9, 0.9))
        for s in (1, -1):
            B.spike(p + Vector((s * w, 0, 0)), (s, 0.25, 0.15), 0.07, 0.02, ARMOR, "Chest", top=(0.12, 0.3))
    B.seg(NECK + Vector((0, 0.02, -0.03)), HEADP + Vector((0, -0.02, 0.0)), 0.06, 0.05, HIDE, "Neck", ext=0.03)''',
'''    d = (PRO[1] - PRO[0]).normalized()
    n_up = Vector((0, 0.795, 0.606))

    def A(t):
        return PRO[0].lerp(PRO[1], t) + n_up * 0.09

    def shw(t):                                       # shield half-width: a diamond, widest at the front third
        return 0.155 * (0.42 + 0.58 * (t - 0.15) / 0.30 if t < 0.45 else 1.0 - 0.65 * (t - 0.45) / 0.53)
    B.seg(A(0.15), A(0.45), 0.155, 0.018, ARMOR, "Chest", bot=(0.42, 1))                    # PRONOTUM SHIELD (FIX 5)
    B.seg(A(0.45), A(0.98), 0.155, 0.018, ARMOR, "Chest", top=(0.35, 1))
    for t, L in ((0.25, 0.07), (0.45, 0.09), (0.65, 0.07)):                                  # thorny edge, ruby points
        for s in (1, -1):
            base = A(t) + Vector((s * shw(t) * 0.92, 0, 0))
            dv = (Vector((s, 0, 0)) + d * 0.35 + n_up * 0.25).normalized()
            B.spike(base, dv, L, 0.024, ARMOR, "Chest", top=(0.3, 0.3))
            B.spike(base + dv * L * 0.6, dv, L * 0.55, 0.014, RUBY, "Chest", studs=[], nostud=True)
    nrm = Vector((0, 0.8, -0.6)).normalized()
    B.seg(PRO[0].lerp(PRO[1], 0.40) + Vector((0, -0.05, -0.04)),
          PRO[1] + Vector((0, -0.05, -0.05)), 0.045, 0.03, BELLY, "Chest", top=(0.8, 1))               # throat tie
    for t in (0.55, 0.78):
        q = PRO[0].lerp(PRO[1], t) + Vector((0, -0.05, -0.045))
        B.seg(q - d * 0.012, q + d * 0.012, 0.047, 0.032, BELLY_D, "Chest", studs=[])
    B.seg(NECK + Vector((0, 0.02, -0.03)), HEADP + Vector((0, -0.02, 0.0)), 0.07, 0.05, HIDE, "Neck", ext=0.03)'''))
# ---- head, eyes, brows, mandibles, antennae, crown (FIX 0-3)
R.append(('''    B.add(HC, (0.115, 0.07, 0.085), HIDE, "Head", bot=(0.42, 0.85), top=(1.0, 0.95), rnd=0.25)
    B.add(HC + Vector((0, -0.015, -0.115)), (0.05, 0.05, 0.035), HIDE, "Head", bot=(0.6, 0.8))       # lower face
    B.add(HC + Vector((0, -0.068, 0.0)), (0.06, 0.01, 0.06), BELLY, "Head", bot=(0.5, 1), studs=[], role="detail",
          bevel=0.005)                                                                         # face plate
    for s in (1, -1):
        e = HC + Vector((s * 0.125, -0.015, 0.045))
        B.add(e, (0.058, 0.06, 0.066), RUBY_D, "Head", rnd=0.5, studs=[], nostud=True, bot=(0.75, 0.8),
              top=(0.75, 0.8))                                                                 # eye bulb
        B.add(e + Vector((s * 0.006, -0.014, 0.004)), (0.052, 0.05, 0.05), RUBY, "Head", rnd=0.5, studs=[],
              nostud=True, bot=(0.7, 0.8), top=(0.7, 0.8), role="detail")
        B.add(e + Vector((s * 0.012, -0.058, 0.02)), (0.016, 0.006, 0.016), RUBY_HOT, "Head", studs=[],
              role="detail", bevel=0.004)                                                     # highlight
        B.add(e + Vector((-s * 0.006, -0.061, -0.006)), (0.013, 0.006, 0.02), BLACK, "Head", studs=[],
              role="detail", bevel=0.004)                                                     # pseudo-pupil
        B.add(e + Vector((-s * 0.04, -0.05, 0.062)), (0.06, 0.026, 0.018), ARMOR, "Head", rot=(0, s * 24, 0),
              role="detail", bevel=0.008)                                                     # angry brow
        # mandibles (dark, ivory tips) + palps
        m0 = HC + Vector((s * 0.035, -0.04, -0.15))
        B.spike(m0, (-s * 0.55, -0.6, -0.55), 0.075, 0.018, ARMOR, "Jaw", top=(0.4, 0.4))
        B.spike(m0 + Vector((-s * 0.03, -0.035, -0.035)), (-s * 0.9, -0.3, -0.3), 0.035, 0.009, IVORY, "Jaw")
        B.spike(HC + Vector((s * 0.05, -0.03, -0.12)), (s * 0.4, -0.5, -1), 0.07, 0.01, ARMOR, "Jaw")
        # antennae: long thin whips from between the eyes, swept up-back
        a0 = HC + Vector((s * 0.028, -0.06, 0.07))
        a1 = a0 + Vector((s * 0.08, 0.02, 0.24))
        a2 = a1 + Vector((s * 0.12, 0.16, 0.16))
        B.seg(a0, a1, 0.012, 0.012, ARMOR, "Antenna_" + side, ext=0.01, role="limb")
        B.seg(a1, a2, 0.009, 0.009, ARMOR, "Antenna_" + side, ext=0.005, role="limb")
    # GOLD CONE-CROWN (hero #1): tall central cone + 2 side prongs on a gold band, ruby gem at the base
    cb = HC + Vector((0, 0.01, 0.10))
    B.add(cb, (0.07, 0.04, 0.022), GOLD, "Head", top=(0.85, 0.85), role="limb", bevel=0.008)
    B.spike(cb + Vector((0, 0.0, 0.01)), (0, 0.35, 1), 0.26, 0.045, GOLD, "Head", top=(0.12, 0.12))
    for s in (1, -1):
        B.spike(cb + Vector((s * 0.05, 0.0, 0.01)), (s * 0.45, 0.25, 1), 0.13, 0.03, GOLD, "Head", top=(0.12, 0.12))
    B.spike(cb + Vector((0, 0.02, 0.06)), (0, 0.35, 1), 0.12, 0.022, GOLD_D, "Head", top=(0.3, 0.3))   # cone keel
    ruby_gem(B, cb + Vector((0, -0.038, 0.0)), (0, -1, 0.15), 0.045, "Head")''',
'''    B.add(HC, (0.15, 0.09, 0.11), HIDE, "Head", bot=(0.38, 0.85), top=(1.0, 0.95), rnd=0.25)        # FIX 1 head
    B.add(HC + Vector((0, -0.02, -0.145)), (0.065, 0.06, 0.045), HIDE, "Head", bot=(0.6, 0.8))       # lower face
    B.add(HC + Vector((0, -0.088, 0.055)), (0.085, 0.012, 0.05), ARMOR, "Head", bot=(0.35, 1), role="detail",
          bevel=0.006)                                                                         # executioner hood
    B.add(HC + Vector((0, -0.083, -0.15)), (0.035, 0.008, 0.022), BELLY, "Head", studs=[], role="detail",
          bevel=0.004)                                                                         # mouth plate
    for s, side in ((1, "L"), (-1, "R")):                                                     # FIX 0: own side
        e = HC + Vector((s * 0.165, -0.02, 0.075))                                             # FIX 2: ruby domes
        rot = (0, s * 12, s * 18)
        B.add(e, (0.072, 0.07, 0.088), RUBY_D, "Head", rot=rot, rnd=0.5, studs=[], nostud=True, bot=(0.70, 0.75),
              top=(0.60, 0.70))
        body = B.add(e + Vector((s * 0.006, -0.012, 0.014)), (0.064, 0.062, 0.078), RUBY, "Head", rot=rot, rnd=0.5,
                     studs=[], nostud=True, bot=(0.65, 0.7), top=(0.55, 0.65), role="detail")
        B.add(e + Vector((s * 0.028, -0.04, 0.06)), (0.024, 0.022, 0.016), RUBY_HOT, "Head", rot=rot, rnd=0.5,
              studs=[], nostud=True, role="detail")                                              # hot cap
        hp, hn = surf_hit(B, [body], e + Vector((-s * 0.022, -0.5, -0.004)), (0, 1, 0))
        import blockkit as bk
        Rp = bk.frame_from(hp, hp + Vector((0, 0, 1)), hn)
        B.add(hp + hn * 0.004, (0.006, 0.013, 0.028), BLACK, "Head", R=Rp, studs=[], role="detail",
              bevel=0.003)                                                                     # pseudo-pupil slit
        B.add(HC + Vector((s * 0.065, -0.10, 0.07)), (0.06, 0.016, 0.02), ARMOR, "Head", rot=(0, -s * 30, 0),
              role="detail", bevel=0.008)                                                     # V-brow (lids the eye)
        # mandibles (dark, ivory tips) + palps
        m0 = HC + Vector((s * 0.035, -0.05, -0.185))
        B.spike(m0, (-s * 0.55, -0.6, -0.55), 0.10, 0.024, ARMOR, "Jaw", top=(0.4, 0.4))
        B.spike(m0 + Vector((-s * 0.04, -0.045, -0.045)), (-s * 0.9, -0.3, -0.3), 0.045, 0.011, IVORY, "Jaw")
        B.spike(HC + Vector((s * 0.06, -0.035, -0.155)), (s * 0.4, -0.5, -1), 0.085, 0.012, ARMOR, "Jaw")
        # antennae: from ABOVE the V, swept up-back (never through the brows); tips under the crown tip
        a0 = HC + Vector((s * ANT0[0], ANT0[1], ANT0[2]))
        a1 = a0 + Vector((s * ANT1[0], ANT1[1], ANT1[2]))
        a2 = a1 + Vector((s * 0.17, 0.24, 0.02))
        B.seg(a0, a1, 0.013, 0.013, ARMOR, "Antenna_" + side, ext=0.01, role="limb")
        B.seg(a1, a2, 0.010, 0.010, ARMOR, "Antenna_" + side, ext=0.005, role="limb")
    # GOLD CROWN (FIX 3, hero #1): solid band between the eye domes + a dominant 0.34 cone (the model top) + prongs
    B.add(HC + Vector((0, 0, 0.12)), (0.09, 0.06, 0.032), GOLD, "Head", top=(0.85, 0.85), role="limb", bevel=0.01)
    B.spike(HC + Vector((0, 0, 0.14)), (0, 0.25, 1), 0.34, 0.065, GOLD, "Head", top=(0.12, 0.12))
    for s in (1, -1):
        B.spike(HC + Vector((s * 0.055, 0, 0.14)), (s * 0.5, 0.2, 1), 0.18, 0.042, GOLD, "Head", top=(0.12, 0.12))
    B.spike(HC + Vector((0, 0.02, 0.19)), (0, 0.35, 1), 0.16, 0.03, GOLD_D, "Head", top=(0.3, 0.3))   # cone keel
    ruby_gem(B, HC + Vector((0, -0.062, 0.12)), (0, -1, 0.15), 0.06, "Head")
    B.add(HC + Vector((0, 0.062, 0.115)), (0.07, 0.012, 0.03), GOLD, "Head", role="limb", bevel=0.006)  # back plate
    ruby_gem(B, HC + Vector((0, 0.072, 0.115)), (0, 1, 0.15), 0.045, "Head")'''))
# ---- raptorial forelegs (FIX 4)
R.append(('''        B.seg(C0, C1, 0.045, 0.05, HIDE, arm, ext=0.04, ext1=0.03, top=(0.8, 0.8))                  # coxa
        B.add(C1, (0.05, 0.05, 0.05), ARMOR, arm, rnd=0.3)                                           # joint
        fem = B.seg(C1, F1, 0.055, 0.08, HIDE, fore, ext=0.03, ext1=0.04, top=(0.7, 0.8))            # femur
        fd = (F1 - C1).normalized()
        fwd = Vector((0, -1, 0))
        edge = (fwd - fd * fwd.dot(fd)).normalized()                                             # femur's front edge
        B.seg(C1 + edge * 0.07 + fd * 0.02, F1 + edge * 0.06, 0.03, 0.026, GOLD, fore, top=(0.6, 0.8), ext1=0.02)
        for t in (0.25, 0.45, 0.65, 0.85):
            ruby_gem(B, C1.lerp(F1, t) + edge * 0.085, edge + fd * 0.35, 0.05 if t in (0.45, 0.65) else 0.04, fore)
        B.add(F1, (0.045, 0.045, 0.045), ARMOR, fore, rnd=0.3)                                       # knee
        td = (T1 - F1).normalized()
        B.seg(F1, T1, 0.028, 0.034, GOLD, blade, ext=0.02, top=(0.7, 0.6))                           # tibia
        tedge = (fwd - td * fwd.dot(td)).normalized()
        for t in (0.3, 0.55, 0.78):
            B.spike(F1.lerp(T1, t) + tedge * 0.025, tedge * 0.8 - td * 0.6, 0.045, 0.012, GOLD_D, blade)
        B.spike(T1 - td * 0.01, td * 0.6 + tedge * 0.8 + Vector((0, 0, 0.3)), 0.07, 0.018, BLACK, blade)  # hook''',
'''        B.seg(C0, C1, 0.05, 0.055, HIDE, arm, ext=0.04, ext1=0.03, top=(0.8, 0.8))                  # coxa
        B.add(C1, (0.055, 0.055, 0.055), ARMOR, arm, rnd=0.5)                                        # joint
        B.seg(C1, F1, 0.045, 0.075, ARMOR, fore, ext=0.03, ext1=0.03, top=(0.75, 0.6))              # dark femur
        fd = (F1 - C1).normalized()
        fwd = Vector((0, -1, 0))
        edge = (fwd - fd * fwd.dot(fd)).normalized()                                             # femur's front edge
        P0 = C1 + fd * 0.03 + edge * 0.075
        Pm = C1.lerp(F1, 0.5) + edge * 0.11
        P1 = F1 - fd * 0.03 + edge * 0.07
        kw = dict(side=(1, 0, 0), studs=[], nostud=True, role="limb")
        B.seg(P0, Pm, 0.035, 0.04, GOLD, fore, bot=(0.7, 0.7), ext1=0.01, **kw)                    # GOLD CRESCENT
        B.seg(Pm, P1, 0.035, 0.04, GOLD, fore, top=(0.7, 0.7), ext=0.01, **kw)

        def cres(t):
            return P0.lerp(Pm, t * 2) if t < 0.5 else Pm.lerp(P1, t * 2 - 1)
        for i, t in enumerate((0.2, 0.36, 0.52, 0.68, 0.84)):                                    # ruby saw: outer row
            ruby_gem(B, cres(t) + edge * 0.035, edge * 0.8 + fd * 0.3 + Vector((s * 0.45, 0, 0)),
                     0.075 if i % 2 == 0 else 0.05, fore)
        for t in (0.28, 0.6):                                                                     # inner row
            ruby_gem(B, cres(t) + edge * 0.03, edge * 0.8 + fd * 0.3 - Vector((s * 0.35, 0, 0)), 0.045, fore)
        B.add(F1, (0.045, 0.045, 0.045), ARMOR, fore, rnd=0.5)                                       # knee knuckle
        B.spike(F1 + Vector((0, 0, 0.03)), (s * 0.7, 0.5, 0.5), 0.11, 0.032, GOLD, fore, top=(0.12, 0.12))  # spine
        td = (T1 - F1).normalized()
        B.seg(F1, T1, 0.032, 0.042, GOLD, blade, ext=0.02, top=(0.7, 0.6))                           # gold tibia
        tedge = (fwd - td * fwd.dot(td)).normalized()
        hd_ = (td * 0.3 - tedge * 0.95).normalized()
        B.spike(T1 - td * 0.01, hd_, 0.08, 0.028, GOLD, blade, top=(0.3, 0.3))                       # hook
        B.spike(T1 - td * 0.01 + hd_ * 0.075, hd_ + td * 0.3, 0.05, 0.015, BLACK, blade)              # claw'''))
# ---- walking legs (FIX 8)
R.append(('''            B.seg(H, K, 0.042, 0.048, HIDE, leg, ext=0.03, ext1=0.03, top=(0.8, 0.8))
            B.add(K, (0.048, 0.048, 0.048), ARMOR, leg, rnd=0.3)
            B.seg(K, A, 0.032, 0.034, ARMOR, shin, ext=0.02, ext1=0.02, top=(0.7, 0.7))
            for t in (0.3, 0.55):
                B.spike(K.lerp(A, t), (s * 0.5, 0.0, -0.4) if fb == "F" else (s * 0.5, 0.3, -0.3), 0.04, 0.009,
                        GOLD_D, shin)
            B.seg(A, P, 0.02, 0.018, ARMOR, foot, ext=0.015)''',
'''            B.seg(H, K, 0.048, 0.054, HIDE, leg, ext=0.03, ext1=0.03, top=(0.8, 0.8))
            B.add(K, (0.052, 0.052, 0.052), ARMOR, leg, rnd=0.3)
            B.seg(K, A, 0.038, 0.040, ARMOR, shin, ext=0.02, ext1=0.02, top=(0.7, 0.7))
            for t in (0.3, 0.55):
                B.spike(K.lerp(A, t), (s * 0.5, 0.0, -0.4) if fb == "F" else (s * 0.5, 0.3, -0.3), 0.04, 0.009,
                        BLACK, shin)
            B.seg(A, P, 0.024, 0.022, ARMOR, foot, ext=0.015)'''))
# ---- rig: antenna joint at the new root
R.append(('''        k.joint("Antenna_" + side, tuple(HC + Vector((s * 0.028, -0.06, 0.07))), "Head", tail=(s * 0.08, 0.02, 0.24))''',
          '''        k.joint("Antenna_" + side, tuple(HC + Vector((s * ANT0[0], ANT0[1], ANT0[2]))), "Head",
                tail=(s * ANT1[0], ANT1[1], ANT1[2]))'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
