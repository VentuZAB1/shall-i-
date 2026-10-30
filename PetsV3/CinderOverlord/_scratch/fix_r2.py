# Cinder Overlord final-8.5 round 2 (_review/CinderOverlord_final85_r2.md + coordinator): neck bands, brows, vents +15 %,
# body value lift (same ember hue), idle breath x1.5, snout without stud dots, Tail4 shorter
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


# ---- brightness (coordinator): a few points of value at the same ember hue (H 8.3 -> 8.9)
rep("PLUM_OBS = (166, 66, 50)    # r4 lead ruling: EMBER body (H 8, S 0.70, brightest 166), away from the pink wine (160,87,102)",
    "PLUM_OBS = (176, 72, 54)    # f85 r2 (coordinator): +value, same ember hue (was 166,66,50). r4 lead ruling: EMBER body, away from the pink wine (160,87,102)")
# ---- R2-M2: brows shorter, less roll, 0.01 lower
rep("BROW_ROLL, BROW_HL, BROW_IN = 16, 0.090, 0.018      # r6: 22 deg, half-length 0.108, centred on the eye",
    "BROW_ROLL, BROW_HL, BROW_IN = 10, 0.070, 0.018      # f85 r2 R2-M2 (f85: 16 / 0.090; r6: 22 deg, 0.108)\nBROW_DZ = 0.046                                     # f85 r2: 0.01 lower (was 0.056)")
rep("""        bc = ep + en * 0.020 + Vector((0, 0, 0.056)) + Rb @ Vector((-s * BROW_IN, 0, 0))      # f85: kept toward the nose""",
    """        bc = ep + en * 0.020 + Vector((0, 0, BROW_DZ)) + Rb @ Vector((-s * BROW_IN, 0, 0))    # f85: kept toward the nose""")
# ---- T-b: Tail4 shorter (the tip pulled in 45 %; the curl kept)
rep("""                          (-0.12, 2.16, 0.0), (0.04, 2.30, 0.0))]""",
    """                          (-0.12, 2.16, 0.0), (-0.032, 2.237, 0.0))]          # f85 r2 T-b: Tail4 45 % shorter (was 0.04, 2.30)""")
rep("""CP[9].z = 0.16                                  # the tail tip curls up""",
    """CP[9].z = 0.13                                  # the tail tip curls up (f85 r2: 0.16 -> 0.13 on the shorter Tail4)""")
# ---- R2-M1: neck bands - rings on Neck1 and Neck3, Neck2 a narrow band, none on the chest curve
rep("""        if i >= 1:
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.50, 0.84, up=(0, 1, 0))""",
    """        if i in (2, 4):                                   # f85 r2 R2-M1: rings on Neck1 + Neck3 only
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.50, 0.84, up=(0, 1, 0))
        elif i == 3:                                      # Neck2: a narrow band (0.62-0.80)
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.62, 0.80, up=(0, 1, 0))""")
# ---- R2-M3: vent slits 15 % longer (they move 4 deg further up the flank to stay clear of the scutes)
rep("""        vw, vl = 0.060 * sc + 0.014, 0.22 * sc + 0.04            # review 1 MUST 4: wider + longer slits (~6 % rose)""",
    """        vw, vl = 0.060 * sc + 0.014, (0.22 * sc + 0.04) * 1.15   # review 1 MUST 4; f85 r2 R2-M3: +15 % long""")
rep("""            ang = math.radians(28 if s > 0 else 152)                       # f85 (was 24 / 156): clear of the T1 scutes""",
    """            ang = math.radians(32 if s > 0 else 148)                       # f85 r2 (f85 28 / 152, r6 24 / 156): clear of the scutes""")
# ---- T-a: a smooth (no stud dots) cover over the snout tip; the nasal ridge + nostrils sit on it
rep("""    skull, skf = loft(B, SK0, SK1, SKS, PLUM_OBS, "Head", n=2.8)""",
    """    skull, skf = loft(B, SK0, SK1, SKS, PLUM_OBS, "Head", n=2.8)
    snout = B.tube([oval(*skf(f)[:3], skf(f)[3] + 0.004, skf(f)[4] + 0.004, seg=20, n=2.8) for f in (0.74, 0.82, 0.90, 0.96, 1.0)],
                   PLUM_OBS, "Head", nostud=True)                                  # f85 r2 T-a: snout tip without stud dots""")
rep("""    r0, _ = surf_hit(B, [skull], (0, -0.95, 2.4), (0, 0, -1))
    r1, _ = surf_hit(B, [skull], (0, -1.07, 2.4), (0, 0, -1))""",
    """    r0, _ = surf_hit(B, [skull, snout], (0, -0.95, 2.4), (0, 0, -1))
    r1, _ = surf_hit(B, [skull, snout], (0, -1.07, 2.4), (0, 0, -1))""")
rep("""        npt, nn = surf_hit(B, [skull], (s * 0.042, -1.035, 2.4), (0, 0, -1))""",
    """        npt, nn = surf_hit(B, [skull, snout], (s * 0.042, -1.035, 2.4), (0, 0, -1))""")
# ---- idle breath x1.5 (neck 4.5 deg per bone, head counter 9, jaw / crown / forearms with it)
rep("""        neck(k, f, pitch=-9 * br, yaw=sway, head_pitch=6 * br, head_yaw=-0.6 * sway)    # f85 T3 (was -6 / 4)
        k.key("Jaw", f, rot=(1.5 * br, 0, 0))""",
    """        neck(k, f, pitch=-13.5 * br, yaw=sway, head_pitch=9 * br, head_yaw=-0.6 * sway)   # f85 r2: x1.5 (f85 -9 / 6)
        k.key("Jaw", f, rot=(2.25 * br, 0, 0))""")
rep("""        crown(k, f, [(1.5 * br, 0)] * 5)
        arms(k, f, paddle_l=2 * br, paddle_r=2 * br)""",
    """        crown(k, f, [(2.25 * br, 0)] * 5)
        arms(k, f, paddle_l=3 * br, paddle_r=3 * br)""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
