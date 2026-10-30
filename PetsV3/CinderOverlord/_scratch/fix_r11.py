# Cinder Overlord final-8.5 round 11 (_review/CinderOverlord_final85_r11.md + coordinator: RAISED COBRA STANCE)
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


# MUST 1: raised cobra stance - the upper neck and the throat go up (FRONT[4] +0.12, FRONT[5] +0.18); the head group
# rides up with them through the HEAD_XF offset (the head stays BUILT about the old throat, so every head / jaw / crown
# coordinate and joint keeps its build-space value) and grows 1.45 -> 1.54 to keep head + crown >= 0.30 of the height
rep("""FRONT = [Vector(p) for p in ((0, -0.24, 0.285), (0, -0.48, 0.37), (0, -0.60, 0.62), (0, -0.585, 0.90),
                             (0, -0.51, 1.16), (0, -0.50, 1.42))]""",
    """HEAD_LIFT = 0.18             # r11 MUST 1 (owner: RAISED COBRA STANCE): the throat / head rise 0.18 BU
FRONT = [Vector(p) for p in ((0, -0.24, 0.285), (0, -0.48, 0.37), (0, -0.60, 0.62), (0, -0.585, 0.90),
                             (0, -0.51, 1.16 + 0.12), (0, -0.50, 1.42 + HEAD_LIFT))]     # r11: FRONT[4] 1.28, FRONT[5] 1.60""")
rep("""HEAD_XF = [((0, -0.50, 1.50), 1.45, [""",
    """# r11 MUST 1: scale 1.45 -> 1.54 and the offset -0.08 -> -0.08 + HEAD_LIFT. The pivot stays the BUILD-space throat
# (THROAT, where the head group is modelled), so the Head joint lands on the raised FRONT[5] (z 1.60) - the same world
# result as the review's 'pivot 1.68 + jaw pivot / Jaw joint +0.18', with no build coordinate to re-type.
HEAD_XF = [((0, -0.50, 1.50), 1.54, [""")
rep("""                                      "Crown_5"], (0, 0, -0.08))]""",
    """                                      "Crown_5"], (0, 0, -0.08 + HEAD_LIFT))]""")
# MUST 2: flatter nose cap (the round red bulb): tip station half-height 0.032 -> 0.022, cap ring height x0.80 -> x0.60
rep("""           (1.0, 0.044, 0.032, -0.036))     # r9 MUST 2""",
    """           (1.0, 0.044, 0.022, -0.036))     # r11 MUST 2: tip half-height 0.032 -> 0.022 (flat nose, no bulb); r9 MUST 2""")
rep("""                   + [oval(*skf(1.012)[:3], skf(1.0)[3] * 0.80, skf(1.0)[4] * 0.80, seg=20, n=2.8)],   # r9: flatter cap""",
    """                   + [oval(*skf(1.012)[:3], skf(1.0)[3] * 0.80, skf(1.0)[4] * 0.60, seg=20, n=2.8)],   # r11: cap height x0.60 (r9 x0.80)""")
# MUST 3a: crown neighbours >= 0.02 - Crown_2 / Crown_4 out 0.018 (and Crown_1 / Crown_5 out 0.010 so 1|2 keeps its gap)
rep("""    for i, (x, h, w, roll, back) in enumerate(((-0.300, 0.18, 0.042, -24, 24), (-0.150, 0.23, 0.050, -12, 24),
                                               (0.0, 0.40, 0.064, 0, 24), (0.150, 0.23, 0.050, 12, 24),""",
    """    for i, (x, h, w, roll, back) in enumerate(((-CR_X1, 0.18, 0.042, -24, 24), (-CR_X2, 0.23, 0.050, -12, 24),
                                               (0.0, 0.40, 0.064, 0, 24), (CR_X2, 0.23, 0.050, 12, 24),""")
rep("""                                               (0.300, 0.18, 0.042, 24, 24))):""",
    """                                               (CR_X1, 0.18, 0.042, 24, 24))):""")
rep("""HEAD_WX = 1.15              # r9 MUST 1b""",
    """CR_X1, CR_X2 = 0.310, 0.168   # r11 MUST 3a: outer / middle crown blade x (r10 0.300 / 0.150) - every neighbour >= 0.02
HEAD_WX = 1.15              # r9 MUST 1b""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
