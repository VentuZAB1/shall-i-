import os
p = os.path.join(os.path.dirname(__file__), "..", "..", "pets", "GlacierYeti.py")
s = open(p, encoding="utf-8").read()


def R(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


# palette: darker belly / lower-leg navy (NICE)
R("POLAR_NAVY = (108, 116, 196)  # torso, legs, head, arms (studded)",
  "POLAR_NAVY = (108, 116, 196)  # torso, legs, head, arms, muzzle (studded)\n"
  "NAVY_D = (92, 100, 178)       # belly / pelvis, abdominal mass, shins (one step darker)")
R("SNOW = (232, 240, 248)        # muzzle\n", "")
# belly darker
R('''    Lt.tube(B, 0.0, sj + 0.05, POLAR_NAVY, "Spine", j1=sj, step=0.08)''',
  '''    Lt.tube(B, 0.0, sj + 0.05, NAVY_D, "Spine", j1=sj, step=0.08)''')
# MUST 4: pectoral masses + abdominal mass (navy form, studded)
R('''    # broken ice sheets frozen onto the hump''', '''    # chest form (review 1 M4): two pectoral masses + one abdominal mass laid on the loft front, studded
    for z, da, half, out, col, bn in ((1.16, 0.36, (0.075, 0.12, 0.10), 0.05, POLAR_NAVY, "Chest"),
                                      (1.16, -0.36, (0.075, 0.12, 0.10), 0.05, POLAR_NAVY, "Chest"),
                                      (0.97, 0.0, (0.06, 0.14, 0.08), 0.04, NAVY_D, "Spine")):
        sv = s_at_z(Lt, z)
        c0, T, N, w_, h_ = Lt.at(sv)
        pnt = Lt.surf(sv, -math.pi / 2 + da)
        nrm = (pnt - c0).normalized()
        along = (-T - nrm * (-T).dot(nrm)).normalized()
        if along.z < 0:
            along = -along
        c = pnt + nrm * (out - half[0])
        B.add(c, half, col, bn, R=bk.frame_from(c, c + along, nrm), rnd=0.50)
    # broken ice sheets frozen onto the hump''')
# MUST 7: lower + tilt the upper hump sheet so it never peeks over the skull
R("    for z, hw, hl, tilt in ((1.30, 0.20, 0.13, 10), (1.13, 0.17, 0.12, 14)):",
  "    for z, hw, hl, tilt in ((1.25, 0.20, 0.13, 20), (1.10, 0.17, 0.12, 14)):")
# NICE: skull wider
R('''    B.add((0, -0.535, 1.475), (0.205, 0.155, 0.150), POLAR_NAVY, "Head",''',
  '''    B.add((0, -0.535, 1.475), (0.220, 0.155, 0.150), POLAR_NAVY, "Head",''')
# MUST 5: muzzle navy, fangs shorter
R('''(0.118, 0.080, 0.066), SNOW, "Head", top=(0.78, 0.70), bot=(1.0, 0.9), rnd=0.42)  # muzzle''',
  '''(0.118, 0.080, 0.066), POLAR_NAVY, "Head", top=(0.78, 0.70), bot=(1.0, 0.9), rnd=0.42)  # muzzle''')
R('''(s * 0.22, -0.15, 1.0), 0.14, 0.030, IVORY, "Jaw", top=(0.06, 0.10))''',
  '''(s * 0.22, -0.15, 1.0), 0.10, 0.028, IVORY, "Jaw", top=(0.08, 0.12))''')
# NICE: narrower brow wings
R('''        B.add((s * 0.096, -0.694, 1.552), (0.114, 0.060, 0.040), BROW, "Head", rot=(-14, -s * 25, 0),''',
  '''        B.add((s * 0.086, -0.694, 1.552), (0.095, 0.060, 0.040), BROW, "Head", rot=(-14, -s * 25, 0),''')
# MUST 2: tapered arms
R('''        B.seg(Sv, Ev, 0.145, 0.15, POLAR_NAVY, arm, ext=0.0, ext1=0.05, top=(0.78, 0.78), rnd=0.46)
        B.seg(Ev, Wv, 0.165, 0.17, POLAR_NAVY, fore, ext=0.06, ext1=0.0, top=(0.66, 0.68), rnd=0.46)''',
  '''        B.seg(Sv, Ev, 0.17, 0.17, POLAR_NAVY, arm, ext=0.0, ext1=0.05, top=(0.82, 0.82), rnd=0.50)   # 0.17 -> 0.14
        B.seg(Ev, Wv, 0.15, 0.15, POLAR_NAVY, fore, ext=0.06, ext1=0.0, top=(0.68, 0.68), rnd=0.50)  # 0.15 -> 0.10''')
# MUST 1: knuckle plates on the top edge of the fist, no seam on them
R('''        # 3 ice knuckle plates across the fist front-top, aurora seam on the middle one
        for i, gx in enumerate((-0.075, 0.0, 0.075)):
            c = Fv + Vector((gx, -0.11, 0.055))
            slab(B, c, (1, 0, 0), (0, 0.55, 1), (0, -1, 0.55),
                 [(-0.034, -0.045), (0.030, -0.05), (0.036, 0.02), (0.012, 0.048), (-0.030, 0.040)], 0.04, hand,
                 seam_edges=(0,) if i == 1 else ())''',
  '''        # 3 ice knuckle plates along the TOP edge of the fist (review 1 M1: the fist front stays smooth BROW)
        for i, gx in enumerate((-0.075, 0.0, 0.075)):
            c = Fv + Vector((gx, -0.075, 0.105))
            slab(B, c, (1, 0, 0), (0, 1, 0.45), (0, -0.45, 1),
                 [(-0.034, -0.045), (0.030, -0.05), (0.036, 0.02), (0.012, 0.048), (-0.030, 0.040)], 0.04, hand)''')
# NICE: crust spikes trimmed to two (the two rim icicles); MUST 6: full-length aurora seam round the crust's lower edge
R('''        for ly, L, lean in ((-0.07, 0.13, 0.35), (0.07, 0.10, 0.55)):                 # broken shards on top
            base = cap.world(Vector((s * cap.h.x * 0.25, ly, cap.h.z - 0.02)))
            B.spike(base, cap.R @ Vector((s * lean, 0.1, 1)), L, 0.045, PLATE_ICE, arm, top=(0.15, 0.45),
                    nostud=True)
        for j, (ly, L, tilt) in enumerate(((-0.12, 0.09, 0.15), (0.02, 0.15, 0.40), (0.14, 0.07, 0.65))):
            base = cap.world(Vector((s * (cap.h.x - 0.015), ly, -cap.h.z + 0.025)))
            B.spike(base, cap.R @ Vector((s * tilt, 0.15 * (j - 1), -1)), L, 0.04, PLATE_ICE, arm, top=(0.10, 0.35),
                    nostud=True)
        a0 = cap.world(Vector((s * (cap.h.x + 0.004), -cap.h.y * 0.85, -cap.h.z + 0.035)))
        a1 = cap.world(Vector((s * (cap.h.x + 0.004), cap.h.y * 0.85, -cap.h.z + 0.035)))
        B.bar(a0, a1, cap.R @ Vector((s, 0, 0)), 0.022, 0.006, AURORA, arm, studs=[], bevel=0.003)''',
  '''        for j, (ly, L, tilt) in enumerate(((-0.08, 0.10, 0.20), (0.07, 0.14, 0.45))):       # 2 rim icicles
            base = cap.world(Vector((s * (cap.h.x - 0.015), ly, -cap.h.z + 0.025)))
            B.spike(base, cap.R @ Vector((s * tilt, 0.15 * (2 * j - 1), -1)), L, 0.042, PLATE_ICE, arm,
                    top=(0.10, 0.35), nostud=True)
        zs = -cap.h.z + 0.032
        hx, hy = cap.h.x + 0.004, cap.h.y + 0.004
        rim = [(-s * hx * 0.55, -hy, Vector((0, -1, 0))), (s * hx, -hy, Vector((s, -1, 0))),
               (s * hx, hy, Vector((s, 1, 0))), (-s * hx * 0.55, hy, Vector((0, 1, 0)))]
        for (xa, ya, na), (xb, yb, nb) in zip(rim, rim[1:]):                        # aurora seam round the rim
            pa, pb = cap.world(Vector((xa, ya, zs))), cap.world(Vector((xb, yb, zs)))
            B.bar(pa, pb, cap.R @ (na + nb).normalized(), 0.034, 0.008, AURORA, arm, studs=[], bevel=0.003)''')
# MUST 6: wider seams in slab()
R('''        o = n * (thick / 2 + 0.004) + inward * 0.018
        B.bar(a + o + d * 0.012, b + o - d * 0.012, n, 0.020, 0.006, AURORA, bone, studs=[], bevel=0.003)''',
  '''        o = n * (thick / 2 + 0.004) + inward * 0.022
        B.bar(a + o + d * 0.012, b + o - d * 0.012, n, 0.034, 0.008, AURORA, bone, studs=[], bevel=0.003)''')
# MUST 3: tapered legs, calf bulge, wedge feet with 3 rounded toe blocks
R('''        B.seg(H + Vector((0, 0, 0.08)), K, 0.17, 0.19, POLAR_NAVY, leg, ext=0.0, ext1=0.04, top=(0.80, 0.78),
              rnd=0.45)
        B.seg(K, A, 0.13, 0.14, POLAR_NAVY, shin, ext=0.05, ext1=0.02, top=(0.84, 0.84), rnd=0.44)
        B.add((A.x, A.y - 0.07, 0.06), (0.13, 0.18, 0.06), BROW, foot, top=(0.85, 0.8), rnd=0.40)
        for gx in (-0.07, 0.0, 0.07):
            B.add((A.x + gx, A.y - 0.235, 0.045), (0.036, 0.045, 0.040), BROW, foot, top=(0.85, 0.8), rnd=0.3,
                  role="limb")
            B.spike((A.x + gx, A.y - 0.27, 0.035), (0, -1, -0.45), 0.075, 0.017, BLACK, foot)''',
  '''        B.seg(H + Vector((0, 0, 0.08)), K, 0.19, 0.19, POLAR_NAVY, leg, ext=0.0, ext1=0.04, top=(0.79, 0.79),
              rnd=0.50)                                                                   # thigh 0.19 -> 0.15
        B.seg(K, A, 0.14, 0.14, NAVY_D, shin, ext=0.05, ext1=0.02, top=(0.71, 0.71), rnd=0.50)   # shin 0.14 -> 0.10
        dk = (A - K).normalized()
        B.add(K + dk * 0.10 + Vector((0, 0.06, 0)), (0.11, 0.08, 0.10), NAVY_D, shin, rnd=0.50)   # calf bulge
        B.seg((A.x, A.y + 0.06, 0.065), (A.x, A.y - 0.19, 0.055), 0.125, 0.06, BROW, foot, top=(0.70, 0.78),
              rnd=0.45)                                                                   # wedge foot (heel -> toe)
        for gx in (-0.062, 0.0, 0.062):
            B.add((A.x + gx, A.y - 0.215, 0.042), (0.040, 0.045, 0.040), BROW, foot, rnd=0.45, role="limb")
            B.spike((A.x + gx, A.y - 0.25, 0.035), (0, -1, -0.45), 0.07, 0.017, BLACK, foot)''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
