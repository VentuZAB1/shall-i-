# one-shot patch: Venom Basilisk review-2 fixes 1-6. Run with plain python.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\VenomBasilisk.py"
s = open(p, encoding="utf-8").read()
R = []
R.append(('''# sabre fangs with venom tips hanging outside the lip, heat pits, a forked light-violet tongue (Tongue bone, slides
# out through the rostral notch), banded whip tail ending in a small violet tail-frill. No gold, no glow.''',
'''# sabre fangs with venom tips hanging outside the lip, a forked light-violet tongue (Tongue bone, slides out through
# the lip gap with a 3-4 deg jaw open), banded whip tail ending in a small violet tail-frill. No gold, no glow.
# Review 2 (2026-10-14): 7-point frill + hidden under-flaps, pale under-shells, fanned violet sail, scute seams.'''))
R.append(('''PALE_D = (176, 186, 108)     # belly scute gaps''',
          '''PALE_D = (176, 186, 108)     # belly scute gaps
SEAM = (40, 104, 64)         # transverse scute seams on the dorsal shells'''))
# helper: pale under-shell (mirror of shell)
R.append(('''def side_pt(b, s, ly, lz, off=0.006):''',
'''def ushell(B, b, zt, color, pad=0.012, rnd=0.30, **kw):
    """pale under-shell over body block b: local z from the bottom (-h.z - pad) up to zt (mirror of shell())"""
    xt, yt, ot = prof(b, zt)
    xb, yb, ob = prof(b, -b.h.z)
    z0 = -b.h.z - pad
    hz = (zt - z0) / 2
    c = b.world(Vector((0, ob, (zt + z0) / 2)))
    return B.add(c, (xb + pad, yb + pad, hz), color, b.bone, R=b.R,
                 top=((xt + pad) / (xb + pad), (yt + pad) / (yb + pad)), top_shift=(0, ot - ob), rnd=rnd, **kw)


def side_pt(b, s, ly, lz, off=0.006):'''))
# FIX 2: tuck = belly (PALE), under-shells, scute gaps, stripe teeth from under the shell lip to above the belly
R.append(('''    B.seg((0, -0.10, 0.36), (0, 0.26, 0.44), 0.165, 0.07, HIDE, "Spine", top=(0.82, 0.75), side=(1, 0, 0))   # tuck''',
          '''    B.seg((0, -0.10, 0.36), (0, 0.26, 0.44), 0.165, 0.07, PALE, "Spine", top=(0.82, 0.75), side=(1, 0, 0))   # tuck'''))
R.append(('''    for b in torso:
        shell(B, b, -b.h.y, b.h.y, 0.30 * b.h.z, DORSAL, rnd=0.42)''',
'''    shells = [shell(B, b, -b.h.y, b.h.y, 0.30 * b.h.z, DORSAL, rnd=0.42) for b in torso]
    # pale under-shells (one clean cream form per block, up to -0.50 h.z) with PALE_D scute gaps on the flanks
    for b in torso:
        ub = ushell(B, b, -0.50 * b.h.z, PALE)
        for s in (1, -1):
            for f in (-0.55, -0.18, 0.18, 0.55):
                a, n = side_pt(ub, s, f * ub.h.y, ub.h.z * 0.75, off=0.004)
                c, n2 = side_pt(ub, s, f * ub.h.y, -ub.h.z * 0.6, off=0.004)
                B.bar(a, c, (n + n2).normalized(), 0.014, 0.008, PALE_D, b.bone, studs=[], bevel=0.003)
    # transverse scute seams across the dorsal shells (lighter dorsal, between the stripe teeth)
    for y in (-0.29, -0.07, 0.15, 0.31):
        b = chest if y < -0.05 else waist if y < 0.24 else hips
        hw = b.h.x * 0.8
        surf_strip(B, shells, [(x, y, 2.0) for x in (-hw, -hw * 0.5, 0.0, hw * 0.5, hw)], (0, 0, -1), 0.018, 0.010,
                   SEAM, b.bone, proud=0.006)'''))
R.append(('''            P = [side_pt(b, s, ly + dy, lz, off=0.008)[0] for dy, lz in
                 ((0.0, za - 0.004), (-0.05, za - 0.004), (-0.035, za - 0.09), (0.09, za - 0.22), (0.05, za - 0.09),
                  (0.05, za - 0.004))]
            B.poly([P[0].lerp(P[3], 0.35)] + P[1:] + [P[1]], 0.012, DORSAL, b.bone)''',
'''            L = 0.80 * b.h.z - 0.02                      # tip ends 0.02 above the pale under-shell
            P = [side_pt(b, s, ly + dy, lz, off=0.008)[0] for dy, lz in
                 ((0.0, za + 0.03), (-0.05, za + 0.03), (-0.035, za - 0.41 * L), (0.09 * L / 0.22, za - L),
                  (0.05, za - 0.41 * L), (0.05, za + 0.03))]
            B.poly([P[0].lerp(P[3], 0.35)] + P[1:] + [P[1]], 0.016, DORSAL, b.bone)'''))
R.append(('''    # pale belly: brisket, scute strip along the tuck, a wide pale underside band low on the flank with scute gaps
    B.add((0, -0.26, 0.345), (0.15, 0.18, 0.022), PALE, "Chest", bot=(0.8, 0.9), studs=[])
    B.seg((0, -0.10, 0.293), (0, 0.24, 0.37), 0.12, 0.022, PALE, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    for s in (1, -1):
        pts = [(-0.38 + 0.60 * t, 0.378 + 0.075 * t) for t in (0, 0.25, 0.5, 0.75, 1.0)]
        surf_strip(B, torso, [(s * 1.0, y, z) for y, z in pts[:3]], (-s, 0, 0), 0.12, 0.010, PALE, "Chest",
                   proud=0.009)
        surf_strip(B, torso, [(s * 1.0, y, z) for y, z in pts[2:]], (-s, 0, 0), 0.12, 0.010, PALE, "Spine",
                   proud=0.009)
        for y, bone in ((-0.33, "Chest"), (-0.21, "Chest"), (-0.06, "Spine"), (0.07, "Spine"), (0.18, "Spine")):
            z = 0.378 + 0.075 * (y + 0.38) / 0.60
            a, n = surf_hit(B, torso, (s * 1.0, y, z + 0.045), (-s, 0, 0))
            c, n2 = surf_hit(B, torso, (s * 1.0, y, z - 0.03), (-s, 0, 0))
            B.bar(a + n * 0.006, c + n2 * 0.006, (n + n2).normalized(), 0.014, 0.008, PALE_D, bone, studs=[],
                  bevel=0.003)
''', ''))
# FIX 5: delete the rostral notch and the heat pits
R.append(('''    B.add((0, -1.238, 0.708), (0.012, 0.010, 0.007), BLACK, "Head", studs=[], role="detail", bevel=0.003)  # notch
''', ''))
R.append(('''        B.add((s * 0.084, -1.15, 0.748), (0.005, 0.011, 0.007), BLACK, "Head", rot=(0, 0, s * 8), studs=[],
              role="detail", bevel=0.002)                                                       # heat pit
''', ''))
# FIX 4: tongue at the lip line
R.append(('''    B.seg((0, -0.90, 0.688), (0, -1.10, 0.688), 0.024, 0.010, VENOM_L, "Tongue", studs=[], role="detail")''',
          '''    B.seg((0, -0.90, 0.703), (0, -1.10, 0.703), 0.024, 0.010, VENOM_L, "Tongue", studs=[], role="detail")'''))
R.append(('''        B.spike((0, -1.095, 0.688), (s * 0.35, -1, 0), 0.08, 0.016, VENOM_L, "Tongue", side=(0, 0, 1), studs=[],''',
          '''        B.spike((0, -1.095, 0.703), (s * 0.35, -1, 0), 0.08, 0.016, VENOM_L, "Tongue", side=(0, 0, 1), studs=[],'''))
R.append(('''    k.joint("Tongue", (0, -0.90, 0.688), "Jaw", tail=(0, -0.2, 0))''',
          '''    k.joint("Tongue", (0, -0.90, 0.703), "Jaw", tail=(0, -0.2, 0))'''))
# FIX 1: frill = 7 points; visible boundary panels 30 -> 58 on the outer bones + hidden under-flaps 15 -> 30
R.append(('''    nback = Vector((0, math.cos(math.radians(FRILL_TILT)), -math.sin(math.radians(FRILL_TILT)))) * 0.008
    for (i_in, i_out, bone, sgn) in ((4, 5, "Frill_L", 1), (2, 1, "Frill_R", -1)):
        # pseudo spine at +-15 deg (under the centre membrane) -> real outer spine at +-58 deg
        u15 = Vector((math.sin(math.radians(15 * sgn)), 0, math.cos(math.radians(15))))
        T = math.radians(FRILL_TILT)
        d15 = Vector((u15.x, u15.z * math.sin(T) + 0.16 + 0.42 * abs(u15.x), u15.z * math.cos(T))).normalized()
        r15 = FRILL0 + Vector((u15.x * 0.10, 0.02, u15.z * 0.03 - 0.01))
        t15 = r15 + d15 * (FRILL_L[i_in] + FRILL_L[3]) / 2
        pr = [r15 + nback, roots[i_out] + nback]
        pt = [t15 + nback, tips[i_out] + nback]
        if sgn < 0:
            pr, pt = pr[::-1], pt[::-1]
        web(B, pr, pt, 0.02, (VENOM_DEEP, VENOM_L), bone)''',
'''    web(B, roots[4:6], tips[4:6], 0.02, (VENOM_DEEP, VENOM_L), "Frill_L")          # visible boundary 30 -> 58
    web(B, roots[1:3], tips[1:3], 0.02, (VENOM_DEEP, VENOM_L), "Frill_R")
    nback = Vector((0, math.cos(math.radians(FRILL_TILT)), -math.sin(math.radians(FRILL_TILT)))) * 0.008
    T = math.radians(FRILL_TILT)

    def pseudo(a_deg, L):
        u = Vector((math.sin(math.radians(a_deg)), 0, math.cos(math.radians(a_deg))))
        d = Vector((u.x, u.z * math.sin(T) + 0.16 + 0.42 * abs(u.x), u.z * math.cos(T))).normalized()
        r = FRILL0 + Vector((u.x * 0.10, 0.02, u.z * 0.03 - 0.01))
        return r + nback, r + d * L + nback
    for sgn, bone in ((1, "Frill_L"), (-1, "Frill_R")):                            # hidden under-flap 15 -> 30
        (ra, ta), (rb, tb_) = pseudo(15 * sgn, 0.44), pseudo(30 * sgn, 0.50)
        pr, pt = ([ra, rb], [ta, tb_]) if sgn > 0 else ([rb, ra], [tb_, ta])
        web(B, pr, pt, 0.02, (VENOM_DEEP, VENOM_L), bone, scallop=0.0, reach=0.86)'''))
# FIX 3: sail = spined crest: violet shafts, fanned spines 8 -> 33 deg, shorter web with deeper notches
R.append(('''    sd = Vector((0, 0.32, 1)).normalized()
    sroots = [Vector((0, y, 0.715)) for y in sy]
    stips = [thorn(B, r - sd * 0.04, sd, L, 0.028, b) for r, L, b in zip(sroots, sl, sb)]
    web(B, sroots[:3], stips[:3], 0.018, (VENOM_DEEP, VENOM), "Chest", scallop=0.12, reach=0.92, inner=0.75)
    web(B, sroots[2:], stips[2:], 0.018, (VENOM_DEEP, VENOM), "Spine", scallop=0.12, reach=0.92, inner=0.75)''',
'''    sroots = [Vector((0, y, 0.715)) for y in sy]
    stips = []
    for r, L, b, a_deg in zip(sroots, sl, sb, (8, 13, 18, 23, 28, 33)):
        sd = Vector((0, math.sin(math.radians(a_deg)), math.cos(math.radians(a_deg))))
        stips.append(thorn(B, r - sd * 0.04, sd, L, 0.028, b, col=VENOM_DEEP))
    web(B, sroots[:3], stips[:3], 0.018, (VENOM_DEEP, VENOM), "Chest", scallop=0.20, reach=0.80, inner=0.60)
    web(B, sroots[2:], stips[2:], 0.018, (VENOM_DEEP, VENOM), "Spine", scallop=0.20, reach=0.80, inner=0.60)'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
