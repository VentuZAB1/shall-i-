# Cinder Overlord final-8.5 round 5 (_review/CinderOverlord_final85_r5.md + coordinator): 9+ cheap items
# (MUST 1 gold is applied separately: GOLD (255,196,50) -> (250,160,35) after the 4-colour sweep)
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


# T-a: the slits read side-set from the front -> the OUTER ends come in 0.02 (socket + slit shorter, inner ends kept)
rep("""        B.add(ep, (0.125, 0.010, 0.036), BLACK, "Head", bevel=0.005, top=(0.78, 1.0), **kw)       # socket (f85 M3)
        B.add(ep + en * 0.018 + R @ Vector((0, 0, -0.004)), (0.110, 0.010, 0.020), ROSE, "Head", bevel=0.004,
              top=(0.55, 1.0), **kw)                                                            # rose slit (wedge)""",
    """        ei = R @ Vector((-s * 0.010, 0, 0))                     # r5 T-a: outer ends in 0.02, the inner ends stay
        B.add(ep + ei, (0.115, 0.010, 0.036), BLACK, "Head", bevel=0.005, top=(0.78, 1.0), **kw)  # socket (f85 M3)
        B.add(ep + ei + en * 0.018 + R @ Vector((0, 0, -0.004)), (0.100, 0.010, 0.020), ROSE, "Head", bevel=0.004,
              top=(0.55, 1.0), **kw)                                                            # rose slit (wedge)""")
# T-b: the studded chin bulb read pig-like from the front -> the jaw tip a touch flatter + a stud-free front cover
rep("""    loft(B, jp((0, 0.03, -0.01)), jp((0, -0.48, -0.035)), ((0.0, 0.118, 0.044, 0.0), (0.12, 0.148, 0.054, 0.0),
                                                            (0.55, 0.126, 0.052, 0.0), (0.85, 0.098, 0.046, 0.0),
                                                            (1.0, 0.074, 0.034, 0.0)), PLUM_OBS, "Jaw", n=2.8)""",
    """    _jaw, jkf = loft(B, jp((0, 0.03, -0.01)), jp((0, -0.48, -0.035)), ((0.0, 0.118, 0.044, 0.0), (0.12, 0.148, 0.054, 0.0),
                                                            (0.55, 0.126, 0.052, 0.0), (0.85, 0.098, 0.044, 0.0),
                                                            (1.0, 0.074, 0.030, 0.0)), PLUM_OBS, "Jaw", n=2.8)  # r5 T-b: tip flatter
    B.tube([oval(*jkf(f)[:3], jkf(f)[3] + 0.004, jkf(f)[4] + 0.004, seg=20, n=2.8) for f in (0.80, 0.88, 0.95, 1.0)],
           PLUM_OBS, "Jaw", nostud=True)                                            # r5 T-b: chin front without stud dots""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
