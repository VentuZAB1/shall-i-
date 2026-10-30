# Cinder r11 (d): MUST 3b - change the seats the strict run flagged instead of only documenting them
#  - the shoulder root moves out onto the neck side (its ball sat 0.10 deep in Neck1 and reached Neck2 / the chest caps)
#  - the chest cap (Spine, FRONT segment 1) and the Neck2 start cap stop meeting inside Neck1 (ext 0.5 -> 0.30 x r)
#  - the Body2 end cap and the Body4 start cap stop meeting inside the Body3 bend (ext 0.45 / 0.55 -> 0.30 / 0.35 x r)
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()
n_ok = 0


def rep(a, b, cnt=1):
    global s
    global n_ok
    c = s.count(a)
    assert c == cnt, (c, a[:100])
    s = s.replace(a, b)
    n_ok += 1


rep("""SH_Z = 0.77                            # shoulder height (r10 tried 0.74: the root still meets Neck2 inside the neck, so kept)""",
    """SH_Z = 0.77                            # shoulder height (r10 tried 0.74: the root still meets Neck2 inside the neck, so kept)
SH_X, SH_Y = 0.234, -0.754             # r11 MUST 3b: the shoulder ball sits ON the neck side (r10 0.17, -0.71: 0.10 deep)
EXT_CHEST1, EXT_NECK2_0 = 0.30, 0.30   # r11 MUST 3b: the chest end cap / Neck2 start cap inside Neck1 (were 0.5 x r)
EXT_BODY2_1, EXT_BODY4_0 = 0.30, 0.35  # r11 MUST 3b: the Body2 end / Body4 start caps inside the Body3 bend (0.45 / 0.55)""")
rep("""        sh = Vector((s * 0.17, -0.71, SH_Z))                  # moved out/forward with the thicker chest (r2); r10 z SH_Z""",
    """        sh = Vector((s * SH_X, SH_Y, SH_Z))                   # r11: on the neck side (r2 0.17, -0.71); r10 z SH_Z""")
rep("""                                             (s * 0.17, -0.71, SH_Z)))""",
    """                                             (s * SH_X, SH_Y, SH_Z)))""")
rep("""        out.append(((s * 0.17, -0.71, SH_Z), (s * 0.17, -0.71, SH_Z), 0.09, "Arm_" + side))""",
    """        out.append(((s * SH_X, SH_Y, SH_Z), (s * SH_X, SH_Y, SH_Z), 0.09, "Arm_" + side))""")
rep("""        SEGS[i] = body_seg(B, a, b, RAD[i], RAD[i + 1], bone, ext0=0.0 if i == 0 else RAD[i] * 0.55,
                           ext1=RAD[i + 1] * 0.45)""",
    """        SEGS[i] = body_seg(B, a, b, RAD[i], RAD[i + 1], bone,
                           ext0=0.0 if i == 0 else RAD[i] * (EXT_BODY4_0 if i == 4 else 0.55),
                           ext1=RAD[i + 1] * (EXT_BODY2_1 if i == 2 else 0.45))         # r11 MUST 3b (Body2 / Body4 caps)""")
rep("""        body_seg(B, a, b, FRAD[i], FRAD[i + 1], fb[i], ext0=FRAD[i] * 0.5 if i else 0.0, ext1=FRAD[i + 1] * 0.5,""",
    """        body_seg(B, a, b, FRAD[i], FRAD[i + 1], fb[i], ext0=FRAD[i] * (EXT_NECK2_0 if i == 3 else 0.5) if i else 0.0,
                 ext1=FRAD[i + 1] * (EXT_CHEST1 if i == 1 else 0.5),""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
