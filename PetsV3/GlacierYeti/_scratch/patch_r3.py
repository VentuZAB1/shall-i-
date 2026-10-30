# round-2 verdict fixes: upper-arm shelf back / down / shorter (white bib), front crust icicle points straight out,
# NICE: sunk pecs, knuckle-wedge fists, a bicep block; the deltoid crust (+ icicles + seam) moves to the Plate_ bone
# so the idle can lift the plates
import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\GlacierYeti.py"
s = io.open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)


rep('''    for z, da, half, out, col, mirror in ((1.24, 0.42, (0.05, 0.17, 0.12), 0.024, POLAR_NAVY, True),
                                          (1.04, 0.0, (0.05, 0.16, 0.09), 0.022, NAVY_D, False)):''',
    '''    for z, da, half, out, col, mirror in ((1.24, 0.42, (0.05, 0.17, 0.12), 0.014, POLAR_NAVY, True),   # sunk (r2)
                                          (1.04, 0.0, (0.05, 0.16, 0.09), 0.016, NAVY_D, False)):''')
rep('''        B.add(Fv, (0.13, 0.14, 0.125), BROW, hand, rnd=0.50)                                           # fist (rounded)''',
    '''        B.add(Fv, (0.13, 0.14, 0.125), BROW, hand, top=(0.82, 0.78), rnd=0.40)          # fist: knuckle wedge (r2)''')
rep('''        B.seg(Ev, Wv, 0.15, 0.15, POLAR_NAVY, fore, ext=0.06, ext1=0.0, top=(0.68, 0.68), rnd=0.50)  # 0.15 -> 0.10''',
    '''        B.seg(Ev, Wv, 0.15, 0.15, POLAR_NAVY, fore, ext=0.06, ext1=0.0, top=(0.68, 0.68), rnd=0.50)  # 0.15 -> 0.10
        B.seg(Sv + (Ev - Sv) * 0.28 + Vector((0, -0.07, 0)), Sv + (Ev - Sv) * 0.70 + Vector((0, -0.06, 0)), 0.115,
              0.10, POLAR_NAVY, arm, top=(0.80, 0.80), rnd=0.50)                          # bicep block (r2 NICE)''')
rep('''        cap = shell(B, dl, -0.03, PLATE_ICE, pad=0.035, rnd=0.14, nostud=True, role="limb")
        for j, (ly, L, tilt) in enumerate(((-0.08, 0.10, 0.20), (0.07, 0.14, 0.45))):       # 2 rim icicles
            base = cap.world(Vector((s * (cap.h.x - 0.015), ly, -cap.h.z + 0.025)))
            B.spike(base, cap.R @ Vector((s * tilt, 0.15 * (2 * j - 1), -1)), L, 0.042, PLATE_ICE, arm,
                    top=(0.10, 0.35), nostud=True)''',
    '''        pl = "Plate_" + side                                       # the crust rides the Plate bone (idle settle)
        cap = shell(B, dl, -0.03, PLATE_ICE, pad=0.035, rnd=0.14, nostud=True, role="limb", bone=pl)
        for ly, L, d in ((-0.03, 0.10, (s * 0.65, 0.0, -1)), (0.07, 0.14, (s * 0.45, 0.15, -1))):   # 2 rim icicles,
            base = cap.world(Vector((s * (cap.h.x - 0.015), ly, -cap.h.z + 0.025)))          # front one points OUT
            B.spike(base, cap.R @ Vector(d), L, 0.042, PLATE_ICE, pl, top=(0.10, 0.35), nostud=True)''')
rep('''            B.bar(pa, pb, cap.R @ (na + nb).normalized(), 0.040, 0.008, AURORA, arm, studs=[], bevel=0.003)''',
    '''            B.bar(pa, pb, cap.R @ (na + nb).normalized(), 0.040, 0.008, AURORA, pl, studs=[], bevel=0.003)''')
rep('''        Ua = Sv + (Ev - Sv) * 0.42 + Vector((s * 0.145, 0.0, 0.0))
        dn = (Ev - Sv).normalized()
        slab(B, Ua, (0, 1, 0), -dn, (s * math.cos(math.radians(20)), 0, math.sin(math.radians(20))),
             [(-0.14, -0.10), (0.0, -0.14), (0.14, -0.09), (0.12, 0.05), (0.15, 0.12), (-0.02, 0.14), (-0.13, 0.09)],
             0.05, arm, seam_edges=(0, 1, 2))''',
    '''        Ua = Sv + (Ev - Sv) * 0.50 + Vector((s * 0.145, 0.08, 0.0))      # back +0.08, down to 0.50 (r2 MUST 1)
        dn = (Ev - Sv).normalized()
        OL = [(-0.14, -0.10), (0.0, -0.14), (0.14, -0.09), (0.12, 0.05), (0.15, 0.12), (-0.02, 0.14), (-0.13, 0.09)]
        slab(B, Ua, (0, 1, 0), -dn, (s * math.cos(math.radians(20)), 0, math.sin(math.radians(20))),
             [(a * 0.85, b * 0.75) for a, b in OL], 0.05, arm, seam_edges=(0, 1, 2))     # 25 % shorter''')
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
