# Permafrost Titan final-8.5 round 2 (_review/PermafrostTitan_final85_r2.md): legs one tube, hips, chest->pelvis,
# kneel mirrored to the LEFT knee (Knee_L), idle sway, belly band narrower
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\PermafrostTitan.py"
s = io.open(p, encoding="utf-8").read()
n_ok = 0


def rep(a, b):
    global s, n_ok
    c = s.count(a)
    assert c == 1, (c, a[:100])
    s = s.replace(a, b)
    n_ok += 1


# ---- MUST 2: narrower hip base; the plum hip plates sit on the hip, not over the thigh tops
rep("""    B.add((0, 0.04, 0.90), (0.30, 0.21, 0.13), MAUVE, "Spine", bot=(0.80, 0.82), top=(1.0, 1.0), rnd=0.36)
    B.mirror((0.272, 0.045, 0.885), (0.058, 0.17, 0.12), PLUM, "Spine", rot=(0, 10, 0), bot=(0.8, 0.85), rnd=0.38)
    B.add((0, 0.03, 1.03), (0.268, 0.19, 0.04), JOINT_D, "Spine", rnd=0.4)                           # belt joint""",
    """    B.add((0, 0.04, 0.90), (0.27, 0.21, 0.13), MAUVE, "Spine", bot=(0.78, 0.82), top=(1.0, 1.0), rnd=0.40)  # r2 M2
    B.mirror((0.238, 0.045, 0.905), (0.034, 0.16, 0.10), PLUM, "Spine", rot=(0, 10, 0), bot=(0.8, 0.85),
             rnd=0.45)                                                       # r2 M2: hip plates on the hip, thinner
    B.add((0, 0.03, 1.03), (0.262, 0.19, 0.04), JOINT_D, "Spine", rnd=0.5)                     # belt joint (r2 M3)""")
# ---- NICE 1: belly band narrower (reads as underside, not a white belt)
rep("""    B.add((0, -0.176, 1.098), (0.20, 0.016, 0.036), ICE_W, "Spine", top=(1.06, 1.0), nostud=True, role="limb",""",
    """    B.add((0, -0.176, 1.098), (0.16, 0.012, 0.030), ICE_W, "Spine", top=(1.06, 1.0), nostud=True, role="limb",""")
# ---- MUST 3: chest bottom tapers further, the chest/waist gap rounder
rep("""    rib = B.add((0, 0.0, 1.42), (0.38, 0.28, 0.29), MAUVE, "Chest", rot=(10, 0, 0), bot=(0.66, 0.74),""",
    """    rib = B.add((0, 0.0, 1.42), (0.38, 0.28, 0.29), MAUVE, "Chest", rot=(10, 0, 0), bot=(0.62, 0.74),""")
rep("""    B.add((0, 0.05, 1.165), (0.28, 0.20, 0.035), JOINT_D, "Chest", rnd=0.4)                          # chest/waist gap""",
    """    B.add((0, 0.05, 1.165), (0.26, 0.20, 0.035), JOINT_D, "Chest", rnd=0.5)                    # chest/waist gap (r2)""")

# ---- MUST 1: each leg = one tapered tube (flush plate, flush knee cap, one ankle band)
rep("""        B.seg(H + Vector((0, 0.0, 0.07)), K, 0.182, 0.194, MAUVE, leg, ext=0.0, ext1=0.02, top=(0.72, 0.72),
              rnd=0.40)                                                                                # thigh
        B.seg(H + Vector((s * 0.12, 0.01, 0.0)), K + Vector((s * 0.095, 0.0, 0.10)), 0.046, 0.155, PLUM, leg,
              top=(0.75, 0.70), rnd=0.42)                                                              # thigh plate
        dk = (A - K).normalized()
        B.seg(K - dk * 0.035, K + dk * 0.05, 0.138, 0.150, JOINT_D, shin, rnd=0.38)                    # knee joint
        B.add(K + Vector((0, -0.145, 0.0)), (0.10, 0.04, 0.088), PLUM, shin, rnd=0.55)                 # knee cap
        B.seg(K, A, 0.156, 0.164, MAUVE, shin, ext=0.0, ext1=0.0, top=(0.74, 0.74), rnd=0.42)          # shin (f85 taper)
        B.seg(K + Vector((0, -0.134, -0.085)), A + Vector((0, -0.128, 0.07)), 0.116, 0.028, PLUM, shin,
              top=(0.86, 1.0), rnd=0.40)                                                               # shin guard
        B.seg(A - Vector((0, 0, 0.005)), A + Vector((0, 0, 0.015)), 0.155, 0.164, JOINT_D, foot, rnd=0.35)  # ankle""",
    """        # r2 MUST 1: ONE tapered tube per leg - thigh 0.182 -> 0.66 at the knee, the shin carries on from the same
        # width down to the ankle; the plum plate, knee cap and shin guard are flush (no steps); one thin ankle band
        TW, TD, TT = 0.182, 0.194, 0.66                       # thigh half-width / half-depth at the hip, knee taper
        SW, SD, ST = TW * TT + 0.006, TD * TT + 0.006, 0.84   # shin starts at the thigh's knee width (+ a calf)
        H2 = H + Vector((s * 0.02, 0.0, 0.07))                # r2 MUST 2: the thigh top 0.02 further out
        B.seg(H2, K, TW, TD, MAUVE, leg, ext=0.0, ext1=0.02, top=(TT, TT), rnd=0.40)                  # thigh
        f0, f1 = 0.10, 0.80                                   # the plum outer plate rides the thigh surface
        q0, q1 = H2.lerp(K, f0), H2.lerp(K, f1)
        w0, w1 = TW * (1 - (1 - TT) * f0), TW * (1 - (1 - TT) * f1)
        B.seg(q0 + Vector((s * (w0 - 0.012), 0.01, 0)), q1 + Vector((s * (w1 - 0.012), 0.0, 0)), 0.020, 0.125 * (w0 / TW),
              PLUM, leg, top=(1.0, w1 / w0), rnd=0.45)                                                 # thigh plate
        dk = (A - K).normalized()
        B.seg(K - dk * 0.030, K + dk * 0.040, SW * 0.86, SD * 0.86, JOINT_D, shin, rnd=0.45)        # knee joint (inside)
        B.add(K + Vector((0, -(SD - 0.004), 0.0)), (0.088, 0.020, 0.080), PLUM, shin, rnd=0.60)       # knee cap (flush)
        B.seg(K, A, SW, SD, MAUVE, shin, ext=0.02, ext1=0.0, top=(ST, ST), rnd=0.42)                  # shin
        g0, g1 = 0.18, 0.82                                   # the plum front guard rides the shin surface
        B.seg(K.lerp(A, g0) + Vector((0, -(SD * (1 - (1 - ST) * g0) - 0.010), 0)),
              A.lerp(K, 1 - g1) + Vector((0, -(SD * (1 - (1 - ST) * g1) - 0.010), 0)), 0.100, 0.018, PLUM, shin,
              top=(0.88, 1.0), rnd=0.45)                                                               # shin guard
        B.seg(A + Vector((0, 0, 0.012)), A + Vector((0, 0, 0.034)), SW * ST + 0.008, SD * ST + 0.008, JOINT_D, shin,
              rnd=0.35)                                                                                # one ankle band
        B.seg(A - Vector((0, 0, 0.005)), A + Vector((0, 0, 0.014)), SW * ST - 0.004, SD * ST - 0.004, JOINT_D, foot,
              rnd=0.35)                                                                                # ankle (inside)""")

# ---- MUST 4: the kneel anchor moves to the LEFT knee (camera side)
rep("""    k.joint("Knee_R", X(KNEE, -1) + Vector((0, -0.20, 0.0)), "Shin_R", tail=(0, -0.1, 0))""",
    """    k.joint("Knee_L", X(KNEE, 1) + Vector((0, -0.17, 0.0)), "Shin_L", tail=(0, -0.1, 0))   # r2 MUST 4: kneel on the LEFT""")

# ---- MUST 5: idle sway 4 -> 6 deg, chest counter-yaw (head stays forward)
rep("""        yaw = 4 * sn(f, n)                                                   # f85 MUST 5: 3 -> 4 deg""",
    """        yaw = 6 * sn(f, n)                                                   # r2 MUST 5: 4 -> 6 deg""")
rep("""        k.key("Chest", f, rot=(-2.0 * br, -0.4 * yaw, 0))                   # breath 1 -> 2 deg
        k.key("Head", f, rot=(2.0 * br, -0.6 * yaw, 0))                     # the head stays level""",
    """        k.key("Chest", f, rot=(-2.0 * br, -0.75 * yaw, 0))                  # r2: counter-yaw (chest vs spine <= 5)
        k.key("Head", f, rot=(2.0 * br, -0.25 * yaw, 0))                    # the head stays level and forward""")

# ---- MUST 4: mirror the kneel (LEFT knee down, the RIGHT foot steps forward)
rep("""ROLL_S = [(0, 0), (8, 0), (18, -7), (50, -7), (62, -4), (76, 0), (100, 0)]
ROLL_C = [(0, 0), (8, 0), (18, 3.5), (50, 3.5), (62, 2), (76, 0), (100, 0)]
ROLL_H = [(0, 0), (8, 0), (18, 3.5), (50, 3.5), (62, 2), (76, 0), (100, 0)]
STEP_L = Vector((0.04, -0.30, 0.0))   # r4: the left foot steps forward 0.30 (was 0.22) and 0.04 out""",
    """# r2 MUST 4: MIRRORED - the LEFT knee goes down (the camera side), the RIGHT foot steps forward; rolls flip sign
ROLL_S = [(0, 0), (8, 0), (18, 7), (50, 7), (62, 4), (76, 0), (100, 0)]
ROLL_C = [(0, 0), (8, 0), (18, -3.5), (50, -3.5), (62, -2), (76, 0), (100, 0)]
ROLL_H = [(0, 0), (8, 0), (18, -3.5), (50, -3.5), (62, -2), (76, 0), (100, 0)]
STEP_R = Vector((-0.04, -0.30, 0.0))  # the right foot steps forward 0.30 and 0.04 out""")
rep("""        (0, 0.0, 0.0, 0.0, 0, 0, 0), (6, -0.03, 0.0, -0.01, 0, 0, 0),""",
    """        (0, 0.0, 0.0, 0.0, 0, 0, 0), (6, 0.03, 0.0, -0.01, 0, 0, 0),""")
rep("""    aL, aR = k.J["Foot_L"].copy(), k.J["Foot_R"].copy()
    L = [(0, aL), (2, aL), (5, aL + STEP_L * 0.5 + Vector((0, 0, 0.06))), (9, aL + STEP_L),
         (70, aL + STEP_L), (74, aL + STEP_L * 0.5 + Vector((0, 0, 0.05))), (79, aL), (100, aL)]
    R = [(0, aR), (6, aR), (11, aR + Vector((0, 0.18, 0.10))), (15, aR + Vector((0, 0.31, 0.15))), (18, aR + Vector((0, 0.34, 0.135))),
         (52, aR + Vector((0, 0.34, 0.135))), (62, aR + Vector((0, 0.24, 0.10))), (70, aR + Vector((0, 0.08, 0.07))),
         (76, aR), (100, aR)]
    TR = [(0, 0), (6, 0), (18, 26), (52, 26), (62, 18), (70, 6), (76, 0), (100, 0)]
    YR = [(0, 0), (10, 0), (18, -10), (50, -10), (62, -4), (72, 0), (100, 0)]   # f85 MUST 6: right foot 10 deg out
    TL = [(0, 0), (2, 0), (5, 8), (9, 0), (70, 0), (74, 8), (79, 0), (100, 0)]
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        ankle_to(k, "Leg_L", f, vcurve(L, f), toe=curve(TL, f))
        ankle_to(k, "Leg_R", f, vcurve(R, f), toe=curve(TR, f), yaw=curve(YR, f))""",
    """    aL, aR = k.J["Foot_L"].copy(), k.J["Foot_R"].copy()
    # r2 MUST 4 (mirrored): the RIGHT foot steps forward and back; the LEFT knee goes down, its foot tucks + turns out
    R = [(0, aR), (2, aR), (5, aR + STEP_R * 0.5 + Vector((0, 0, 0.06))), (9, aR + STEP_R),
         (70, aR + STEP_R), (74, aR + STEP_R * 0.5 + Vector((0, 0, 0.05))), (79, aR), (100, aR)]
    L = [(0, aL), (6, aL), (11, aL + Vector((0, 0.18, 0.10))), (15, aL + Vector((0, 0.31, 0.15))), (18, aL + Vector((0, 0.34, 0.135))),
         (52, aL + Vector((0, 0.34, 0.135))), (62, aL + Vector((0, 0.24, 0.10))), (70, aL + Vector((0, 0.08, 0.07))),
         (76, aL), (100, aL)]
    TL = [(0, 0), (6, 0), (18, 26), (52, 26), (62, 18), (70, 6), (76, 0), (100, 0)]
    YL = [(0, 0), (10, 0), (18, 10), (50, 10), (62, 4), (72, 0), (100, 0)]      # the left foot turns 10 deg out
    TR = [(0, 0), (2, 0), (5, 8), (9, 0), (70, 0), (74, 8), (79, 0), (100, 0)]
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        ankle_to(k, "Leg_R", f, vcurve(R, f), toe=curve(TR, f))
        ankle_to(k, "Leg_L", f, vcurve(L, f), toe=curve(TL, f), yaw=curve(YL, f))""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
