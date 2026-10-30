# Coral Crusher r4 (9+ polish, coordinator): eye stalks ~25 % longer, bulbs ~20 % bigger, still fierce
# (dark copper bulb, black socket, narrow rose slit, black slit pupil, slate lid)
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
s = io.open(p, encoding="utf-8").read()
n_ok = 0


def rep(a, b):
    global s, n_ok
    c = s.count(a)
    assert c == 1, (c, a[:100])
    s = s.replace(a, b)
    n_ok += 1


rep("""        top = base + Vector((s * 0.02, -0.055, 0.07))
        B.seg(base, top, 0.044, 0.044, BRONZE_D, eb, ext=0.02, rnd=0.42, role="limb", nostud=True)  # stalk
        bulb = B.add(top + Vector((0, -0.016, 0.012)), (0.062, 0.046, 0.054), BRONZE_D, eb, rnd=0.45, role="limb",
                     nostud=True)                                                                  # bulb (r2 M7)
        ep, en = surf_hit(B, [bulb], (s * 0.222, -1.0, 0.476), (0, 1, 0))
        crab_eye(B, ep + en * 0.002, s, en, eb, tilt=15, sc=1.1)
        Rl = face_R(en) @ Euler((0, math.radians(-s * 18), 0), "XYZ").to_matrix()
        B.add(ep + en * 0.012 + Vector((s * 0.004, 0, 0.030)), (0.074, 0.024, 0.022), SHELL_D, eb, R=Rl,
              rnd=0.25, role="limb", studs=[], nostud=True)                                       # slate lid / brow""",
    """        top = base + Vector((s * 0.02, -0.055, 0.07)) * ES                                       # r4: stalk x1.25
        B.seg(base, top, 0.044, 0.044, BRONZE_D, eb, ext=0.02, rnd=0.42, role="limb", nostud=True)  # stalk
        bc = top + Vector((0, -0.016, 0.012)) * EB
        bulb = B.add(bc, tuple(Vector((0.062, 0.046, 0.054)) * EB), BRONZE_D, eb, rnd=0.45, role="limb",
                     nostud=True)                                                                  # bulb (r4: x1.2)
        ep, en = surf_hit(B, [bulb], (bc.x + s * 0.002, -1.0, bc.z - 0.006 * EB), (0, 1, 0))
        crab_eye(B, ep + en * 0.002, s, en, eb, tilt=15, sc=1.1 * EB)
        Rl = face_R(en) @ Euler((0, math.radians(-s * 18), 0), "XYZ").to_matrix()
        B.add(ep + en * 0.012 + Vector((s * 0.004, 0, 0.030)) * EB, tuple(Vector((0.074, 0.024, 0.022)) * EB), SHELL_D, eb,
              R=Rl, rnd=0.25, role="limb", studs=[], nostud=True)                                 # slate lid / brow""")
rep("""BLACK = (14, 14, 22)         # claw tips, pupils, eye sockets, leg tips""",
    """BLACK = (14, 14, 22)         # claw tips, pupils, eye sockets, leg tips
ES, EB = 1.25, 1.20          # r4 9+ (coordinator): eyestalk length x1.25, bulb + eye + lid x1.2 (phone-size eye read)""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
