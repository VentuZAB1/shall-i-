# f85 M4 follow-up: the "dark arms" in close_front are the brows' outer ends -> shorter brows (kept toward the nose),
# less roll; the 60 % bulge tucked under the cheek plate
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


rep("""        ellip(B, (s * 0.168, -0.62, 1.628), 0.035, 0.069, 0.053, PLUM_OBS, "Head")      # f85 M2: 60 % bulge""",
    """        ellip(B, (s * 0.158, -0.62, 1.628), 0.035, 0.069, 0.053, PLUM_OBS, "Head")      # f85 M2: 60 % bulge""")
rep("""        Rb = face_R(en) @ Euler((0, math.radians(-s * 22), 0), "XYZ").to_matrix()
        B.add(ep + en * 0.020 + Vector((0, 0, 0.056)), (0.108, 0.036, 0.030), OBS_D, "Head", R=Rb, role="limb",""",
    """        Rb = face_R(en) @ Euler((0, math.radians(-s * BROW_ROLL), 0), "XYZ").to_matrix()
        bc = ep + en * 0.020 + Vector((0, 0, 0.056)) + Rb @ Vector((-s * BROW_IN, 0, 0))      # f85: kept toward the nose
        B.add(bc, (BROW_HL, 0.036, 0.030), OBS_D, "Head", R=Rb, role="limb",""")
rep("""        bf = ep + en * 0.020 + Vector((0, 0, 0.056)) + Rb @ Vector((-s * 0.090, 0, 0))""",
    """        bf = bc + Rb @ Vector((-s * (BROW_HL - 0.018), 0, 0))""")
rep("""H_MODEL = 2.10
ANCH = {}""",
    """H_MODEL = 2.10
ANCH = {}
# f85 (review M4 "dark arms over the brows" = the brows' outer ends seen from the front): shorter, less rolled brows
BROW_ROLL, BROW_HL, BROW_IN = 16, 0.090, 0.018      # r6: 22 deg, half-length 0.108, centred on the eye""")
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
