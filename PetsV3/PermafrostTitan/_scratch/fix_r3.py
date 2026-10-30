# Permafrost Titan final-8.5 round 3 (_review/PermafrostTitan_final85_r3.md + coordinator): M1-M5 + the polish list
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


# ---- M2: belt groove half-height 0.04 -> 0.02 (a thin seam)
rep("""    B.add((0, 0.03, 1.03), (0.262, 0.19, 0.04), JOINT_D, "Spine", rnd=0.5)                     # belt joint (r2 M3)""",
    """    B.add((0, 0.03, 1.03), (0.262, 0.19, 0.02), JOINT_D, "Spine", rnd=0.5)              # belt seam (r3 M2: 0.04 -> 0.02)""")
# ---- M1: no calf ledge; the knee cap 0.008 proud
rep("""        SW, SD, ST = TW * TT + 0.006, TD * TT + 0.006, 0.84   # shin starts at the thigh's knee width (+ a calf)""",
    """        SW, SD, ST = TW * TT, TD * TT, 0.84                   # r3 M1: the shin starts AT the thigh's knee width""")
rep("""        B.add(K + Vector((0, -(SD - 0.004), 0.0)), (0.088, 0.020, 0.080), PLUM, shin, rnd=0.60)       # knee cap (flush)""",
    """        B.add(K + Vector((0, -(SD - 0.012), 0.0)), (0.088, 0.020, 0.080), PLUM, shin, rnd=0.60)       # knee cap (r3: 0.008 proud)""")
# ---- M5 + polish: idle arm sway (opposite fwd/back swing on the hip-yaw sine), breath 1.8
rep("""        k.key("Chest", f, rot=(-2.0 * br, -0.75 * yaw, 0))                  # r2: counter-yaw (chest vs spine <= 5)
        k.key("Head", f, rot=(2.0 * br, -0.25 * yaw, 0))                    # the head stays level and forward
        k.key("Jaw", f, rot=(0, 0, 0))
        arms_fk(k, f, out=curve(settle, f), bend=2.0 * br)""",
    """        k.key("Chest", f, rot=(-1.8 * br, -0.75 * yaw, 0))                  # r3: breath 2.0 -> 1.8 (chest vs spine margin)
        k.key("Head", f, rot=(1.8 * br, -0.25 * yaw, 0))                    # the head stays level and forward
        k.key("Jaw", f, rot=(0, 0, 0))
        arms_fk(k, f, out=curve(settle, f), bend=2.0 * br)
        sway = 2.5 * sn(f, n)                                                # r3 M5: the shoulders turn with the hips -
        for s_, side in ((1, "L"), (-1, "R")):                               # opposite fwd / back arm swing on the
            k.key("Arm_" + side, f, rot=(-s_ * sway, 0, -s_ * curve(settle, f)))   # hip-yaw sine (the chest counter
                                                                             # does not cancel it)""")
# ---- polish: walk arm swing 4 -> 5.5
rep("""            k.key("Arm_" + side, f, rot=(4 * s * sn(f, n, 0.0), 0, 0))           # opposite the same-side leg""",
    """            k.key("Arm_" + side, f, rot=(5.5 * s * sn(f, n, 0.0), 0, 0))         # opposite the same-side leg (r3: 4 -> 5.5)""")
# ---- polish: knee settle 0.008 -> 0.005
rep("""SETTLE = 0.008      # r4 (review 3 MUST 2, lead ruling): the 3-frame settle after the knee lands (ref K8a)""",
    """SETTLE = 0.005      # r3 polish (was 0.008): the 3-frame settle after the knee lands (ref K8a)""")
# ---- M4: the game-camera L-shape - Spine roll 7 -> 9 in the hold (the head counter-rolls more to stay level) and the
#      kneeling foot's back sole 0.02 higher
rep("""ROLL_S = [(0, 0), (8, 0), (18, 7), (50, 7), (62, 4), (76, 0), (100, 0)]
ROLL_C = [(0, 0), (8, 0), (18, -3.5), (50, -3.5), (62, -2), (76, 0), (100, 0)]
ROLL_H = [(0, 0), (8, 0), (18, -3.5), (50, -3.5), (62, -2), (76, 0), (100, 0)]""",
    """ROLL_S = [(0, 0), (8, 0), (18, 9), (50, 9), (62, 4), (76, 0), (100, 0)]           # r3 M4: 7 -> 9 in the hold
ROLL_C = [(0, 0), (8, 0), (18, -3.5), (50, -3.5), (62, -2), (76, 0), (100, 0)]
ROLL_H = [(0, 0), (8, 0), (18, -5.5), (50, -5.5), (62, -2), (76, 0), (100, 0)]     # r3: the head stays level""")
rep("""    L = [(0, aL), (6, aL), (11, aL + Vector((0, 0.18, 0.10))), (15, aL + Vector((0, 0.31, 0.15))), (18, aL + Vector((0, 0.34, 0.135))),
         (52, aL + Vector((0, 0.34, 0.135))), (62, aL + Vector((0, 0.24, 0.10))), (70, aL + Vector((0, 0.08, 0.07))),""",
    """    L = [(0, aL), (6, aL), (11, aL + Vector((0, 0.18, 0.10))), (15, aL + Vector((0, 0.31, 0.16))), (18, aL + Vector((0, 0.34, 0.155))),
         (52, aL + Vector((0, 0.34, 0.155))), (62, aL + Vector((0, 0.24, 0.11))), (70, aL + Vector((0, 0.08, 0.07))),""")   # r3 M4: sole +0.02
# ---- M3: the left fist rests on the left thigh top (f30 / f50); comment matches what is built
rep("""    # r2 MUST 4: asymmetric hold - the RIGHT fist rests forward on the raised right knee, the LEFT arm hangs out to the
    # side so the kneeling left knee stays visible from the front / 3-4 (f, out, fwd, bend)""",
    """    # asymmetric hold (r2 MUST 4, r3 M3): the RIGHT fist rests forward on the raised right knee; the LEFT fist rests on
    # the top of the left (kneeling) thigh, above the knee, so the knee stays visible from the front / 3-4
    # (f, out, fwd, bend)""")
rep("""    ARM_L = [(0, 0, 0, 0), (18, 10, 6, 40), (30, 12, 8, 48), (50, 12, 8, 48), (62, 5, 4, 14), (80, 0, 0, 0), (100, 0, 0, 0)]""",
    """    ARM_L = [(0, 0, 0, 0), (18, 10, 6, 40), (30, 6, 22, 60), (50, 6, 22, 60), (62, 5, 4, 14), (80, 0, 0, 0), (100, 0, 0, 0)]""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
