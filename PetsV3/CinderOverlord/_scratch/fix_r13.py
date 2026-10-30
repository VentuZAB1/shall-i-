# Cinder Overlord final-8.5 round 13 (_review/CinderOverlord_final85_r13.md + coordinator: the reviewer's 5 fixes only)
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()
n_ok = 0


def rep(a, b):
    global s
    global n_ok
    c = s.count(a)
    assert c == 1, (c, a[:100])
    s = s.replace(a, b)
    n_ok += 1


# MUST 1: the hood back plate ember (was obsidian, it fused with the frill / crown from the game camera), ribs pale
rep("""            B.tube(dark, OBS_D, bone, closed=False, nostud=False)""",
    """            B.tube(dark, PLUM_OBS, bone, closed=False, nostud=False)           # r13 MUST 1: ember (r12 OBS_D)""")
rep("""            B.bar(a, b, n, 0.026, 0.010, PLUM_OBS, bone, studs=[], nostud=True, role="detail", bevel=0.004)""",
    """            B.bar(a, b, n, 0.026, 0.010, PALE_S, bone, studs=[], nostud=True, role="detail", bevel=0.004)  # r13: pale""")
# MUST 2: the lumps under the nostrils (hide test _scratch/nose_hide_r13.png): the snout's flat oval front (skull tip
# station + the snout pad tube + its cap ring) and the jaw's rounded chin cap. Both taper to a wedge now.
rep("""(0.82, 0.112, 0.066, -0.026), (0.96, 0.060, 0.028, -0.034),   # r12 MUST 2: 0.082 / 0.040 -> 0.066 / 0.028""",
    """(0.82, 0.112, 0.066, -0.026), (0.96, 0.046, 0.028, -0.034),   # r13 MUST 2: 0.96 width 0.060 -> 0.046 (r12: heights 0.066 / 0.028)""")
rep("""           (1.0, 0.044, 0.022, -0.036))     # r11 MUST 2""",
    """           (1.0, 0.026, 0.018, -0.038))     # r13 MUST 2: a pointed tip 0.044 x 0.022 -> 0.026 x 0.018 (wedge, no oval pad); r11 MUST 2""")
rep("""                   + [oval(*skf(1.012)[:3], skf(1.0)[3] * 0.80, skf(1.0)[4] * 0.60, seg=20, n=2.8)],   # r11: cap height x0.60 (r9 x0.80)""",
    """                   + [oval(*skf(1.010)[:3], skf(1.0)[3] * 0.55, skf(1.0)[4] * 0.55, seg=20, n=2.8)],   # r13: small cap (r11 x0.80 / x0.60)""")
rep("""        npt, nn = surf_hit(B, [skull, snout], (s * 0.042, -1.07, 2.4), (0, 0, -1))      # r3 MUST 3: at the tip""",
    """        npt, nn = surf_hit(B, [skull, snout], (s * 0.034, -1.06, 2.4), (0, 0, -1))      # r13: on the narrower tip (r3 0.042 / -1.07)""")
rep("""(0.55, 0.126, 0.052, 0.0), (0.85, 0.078, 0.032, 0.0),   # r10 MUST 2""",
    """(0.55, 0.126, 0.052, 0.0), (0.85, 0.070, 0.026, 0.0),   # r13 MUST 2: 0.078 / 0.032 -> 0.070 / 0.026 (flat chin); r10 MUST 2""")
rep("""                                                            (1.0, 0.034, 0.016, 0.0)), PLUM_OBS, "Jaw", n=2.8)""",
    """                                                            (1.0, 0.024, 0.012, 0.0)), PLUM_OBS, "Jaw", n=2.8)  # r13: tip 0.034 / 0.016 -> 0.024 / 0.012""")
rep("""           + [oval(*jkf(1.006)[:3], jkf(1.0)[3] * 0.80, jkf(1.0)[4] * 0.80, seg=20, n=2.8)],   # r8 / r9: flatter cap""",
    """           + [oval(*jkf(1.006)[:3], jkf(1.0)[3] * 0.60, jkf(1.0)[4] * 0.55, seg=20, n=2.8)],   # r13: small chin cap (r9 x0.80)""")
# MUST 3: the centre crown blade 0.40 -> 0.44 (kit icon area >= Thunder Rex 0.372)
rep("""                                               (0.0, 0.40, 0.064, 0, 24), (CR_X2, 0.23, 0.050, 12, 24),""",
    """                                               (0.0, 0.44, 0.064, 0, 24), (CR_X2, 0.23, 0.050, 12, 24),   # r13: centre 0.40 -> 0.44""")
# MUST 4: the molt head hold 20.5 -> 14 (the game-camera head gap >= 50 px through the hold)
rep("""    head = [(0, 0), (18, 20.5), (84, 20.5), (100, 3), (110, 0)]""",
    """    head = [(0, 0), (18, 14.0), (84, 14.0), (100, 3), (110, 0)]          # r13 MUST 4: hold 20.5 -> 14 (game-camera gap)""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
