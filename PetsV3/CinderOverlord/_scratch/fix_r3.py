# Cinder Overlord final-8.5 round 3 (_review/CinderOverlord_final85_r3.md + coordinator): forehead, neck, nostrils,
# flush vents, taller centre blade, eyes toward the nose
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()
n_ok = 0


def rep(a, b):
    global s, n_ok
    c = s.count(a)
    assert c == 1, (c, a[:100])
    s = s.replace(a, b)
    n_ok += 1


# MUST 1: the skull cap ends at the eye line (stations 0.66 / 0.78 removed) - a red forehead band shows
rep("""    for f in (0.03, 0.08, 0.18, 0.30, 0.42, 0.54, 0.66, 0.78):""",
    """    for f in (0.03, 0.08, 0.18, 0.30, 0.42, 0.54):                     # r3 MUST 1: cap ends at the eye line (was ... 0.78)""")
# MUST 2: only Neck1 keeps a full ring; Neck2 + Neck3 narrow bands
rep("""        if i in (2, 4):                                   # f85 r2 R2-M1: rings on Neck1 + Neck3 only""",
    """        if i == 2:                                        # r3 MUST 2: a full ring on Neck1 only""")
rep("""        elif i == 3:                                      # Neck2: a narrow band (0.62-0.80)""",
    """        elif i in (3, 4):                                 # Neck2 + Neck3: narrow bands (0.62-0.80)""")
# MUST 3: small nostril pits at the snout tip (they read as a second pair of eyes)
rep("""        npt, nn = surf_hit(B, [skull, snout], (s * 0.042, -1.035, 2.4), (0, 0, -1))
        B.add(npt, (0.010, 0.005, 0.016), BLACK, "Head",""",
    """        npt, nn = surf_hit(B, [skull, snout], (s * 0.042, -1.07, 2.4), (0, 0, -1))      # r3 MUST 3: at the tip
        B.add(npt, (0.006, 0.004, 0.009), BLACK, "Head",""")
# T1: flush vents (the blue sits in the surface; the hot core line just proud of it)
rep("""    B.bar(p0, p1, n, w, 0.012, ROSE, bone, studs=[], nostud=True, role="detail", bevel=0.004, top=(1, 0.55))
    B.bar(p0 + ax * L * 0.16 + n * 0.007, p1 - ax * L * 0.22 + n * 0.007, n, w * 0.50, 0.008, LAVA, bone,""",
    """    B.bar(p0, p1, n, w, 0.006, ROSE, bone, studs=[], nostud=True, role="detail", bevel=0.002, top=(1, 0.55))  # r3 T1: flush
    B.bar(p0 + ax * L * 0.16 + n * 0.004, p1 - ax * L * 0.22 + n * 0.004, n, w * 0.50, 0.004, LAVA, bone,""")
rep("""                p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t + dt, ang, off=0.004)
                vent(B, p, n, dv, bone, L=vl, w=vw)""",
    """                p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t + dt, ang, off=0.000)   # r3 T1: flush
                vent(B, p, n, dv, bone, L=vl, w=vw)""")
rep("""                p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t, ang, off=0.004)""",
    """                p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t, ang, off=0.000)""")
# T2: the centre crest blade 0.32 -> 0.34
rep("""(0.0, 0.32, 0.064, 0, 24)""", """(0.0, 0.34, 0.064, 0, 24)""")
# T3: eyes 0.03 toward the nose (the brows follow the eye point)
rep("""        ep, en = surf_hit(B, [skull], (s * 0.6, -0.80, 1.722), (-s, 0, 0))""",
    """        ep, en = surf_hit(B, [skull], (s * 0.6, -0.83, 1.722), (-s, 0, 0))            # r3 T3: 0.03 toward the nose""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
