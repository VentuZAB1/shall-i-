# Cinder Overlord final-8.5 round 7 (_review/CinderOverlord_final85_r7.md + coordinator)
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


# MUST 1a: vents only on Spine / Body1 / Body2 (the Body3 / Body4 / Tail1 bars read as centipede legs from the game cam)
rep("""    for vi, (bone, t) in enumerate((("Spine", 0.27), ("Body1", 0.27), ("Body2", 0.27), ("Body3", 0.27),
                                    ("Body4", 0.27), ("Tail1", 0.27))):""",
    """    for vi, (bone, t) in enumerate((("Spine", 0.27), ("Body1", 0.27), ("Body2", 0.27))):   # r7 MUST 1a: Body3-Tail1 dropped""")
rep("""    for i in range(1, 7):
        p, bone = ANCH.get("Vent_%d" % i, ((0.2, 0.0, 0.2), "Spine"))
        k.joint("Vent_%d" % i, p, bone, tail=(0.1, 0, 0.05))""",
    """    for i in range(1, 7):
        if "Vent_%d" % i not in ANCH:                                    # r7: Vent_4..6 go with their slits
            continue
        p, bone = ANCH["Vent_%d" % i]
        k.joint("Vent_%d" % i, p, bone, tail=(0.1, 0, 0.05))""")
# MUST 1b: the head group x1.15 (1.20 -> 1.38) about the throat; the crown mount 0.04 wider each side
rep("""HEAD_XF = [((0, -0.50, 1.50), 1.20, [""", """HEAD_XF = [((0, -0.50, 1.50), 1.38, [""")
rep("""        B.seg((0, -0.585, 1.835), (s * 0.22, -0.585, 1.815), 0.034, 0.050, OBS_D, "Head", side=(0, 0, 1),""",
    """        B.seg((0, -0.585, 1.835), (s * 0.26, -0.585, 1.815), 0.034, 0.050, OBS_D, "Head", side=(0, 0, 1),   # r7: 0.22 -> 0.26""")
# MUST 2: centre blade 0.34 -> 0.36; centre + middle gold frames +0.004
rep("""(0.0, 0.34, 0.064, 0, 24)""", """(0.0, 0.36, 0.064, 0, 24)""")
rep("""        gw0 = 0.020 if i in (0, 4) else 0.038 if i == 2 else 0.028""",
    """        gw0 = 0.020 if i in (0, 4) else 0.042 if i == 2 else 0.032      # r7 MUST 2: centre / middle +0.004 (0.038 / 0.028)""")
# 9+ T-a: slit outer ends in another 0.01 (inner ends stay)
rep("""        ei = R @ Vector((-s * 0.010, 0, 0))                     # r5 T-a: outer ends in 0.02, the inner ends stay
        B.add(ep + ei, (0.115, 0.010, 0.036), BLACK, "Head", bevel=0.005, top=(0.78, 1.0), **kw)  # socket (f85 M3)
        B.add(ep + ei + en * 0.018 + R @ Vector((0, 0, -0.004)), (0.100, 0.010, 0.020), ROSE, "Head", bevel=0.004,""",
    """        ei = R @ Vector((-s * 0.015, 0, 0))                     # r5 / r7 T-a: outer ends in 0.03 in all, inner ends stay
        B.add(ep + ei, (0.110, 0.010, 0.036), BLACK, "Head", bevel=0.005, top=(0.78, 1.0), **kw)  # socket (f85 M3)
        B.add(ep + ei + en * 0.018 + R @ Vector((0, 0, -0.004)), (0.095, 0.010, 0.020), ROSE, "Head", bevel=0.004,""")
# 9+ T-b: the chin front ~15 % flatter / narrower (the tip station and the cap ring)
rep("""                                                            (1.0, 0.074, 0.030, 0.0)), PLUM_OBS, "Jaw", n=2.8)  # r5 T-b: tip flatter""",
    """                                                            (1.0, 0.063, 0.026, 0.0)), PLUM_OBS, "Jaw", n=2.8)  # r5 / r7 T-b: tip flatter (r7 -15 %)""")
rep("""           + [oval(*jkf(1.024)[:3], jkf(1.0)[3] * 0.72, jkf(1.0)[4] * 0.72, seg=20, n=2.8)],""",
    """           + [oval(*jkf(1.012)[:3], jkf(1.0)[3] * 0.72, jkf(1.0)[4] * 0.72, seg=20, n=2.8)],   # r7: cap 1.024 -> 1.012""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
