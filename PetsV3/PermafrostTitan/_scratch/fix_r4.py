# Permafrost Titan final-8.5 round 4 (_review/PermafrostTitan_final85_r4.md + coordinator)
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


# MM1: the waist block tapers into the belt (0.95 -> 0.86); the seam sits between the waist base and the hip top
rep("""    B.add((0, 0.02, 1.10), (0.262, 0.19, 0.08), MAUVE, "Spine", bot=(0.95, 0.95), top=(1.08, 1.06), rnd=0.36)""",
    """    B.add((0, 0.02, 1.10), (0.262, 0.19, 0.08), MAUVE, "Spine", bot=(0.86, 0.86), top=(1.08, 1.06), rnd=0.36)  # r4 MM1""")
rep("""    B.add((0, 0.03, 1.03), (0.262, 0.19, 0.02), JOINT_D, "Spine", rnd=0.5)              # belt seam (r3 M2: 0.04 -> 0.02)""",
    """    B.add((0, 0.03, 1.03), (0.248, 0.178, 0.02), JOINT_D, "Spine", rnd=0.5)             # belt seam (r4: tucked to the waist taper)""")
# MC4: the jaw cavity near-black (the open mouth read as a grey slab)
rep("""    B.add((0, -0.335, 1.707), (0.086, 0.040, 0.018), JOINT_D, "Head", studs=[], nostud=True, role="detail",""",
    """    B.add((0, -0.335, 1.707), (0.086, 0.040, 0.018), (24, 26, 34), "Head", studs=[], nostud=True, role="detail",  # r4 MC4""")
# MC2: idle arm sway +/-5
rep("""        sway = 2.5 * sn(f, n)                                                # r3 M5: the shoulders turn with the hips -""",
    """        sway = 5.0 * sn(f, n)                                                # r4 MC2 (r3 2.5): the shoulders turn with the hips -""")
# MC3: walk arm swing 9
rep("""            k.key("Arm_" + side, f, rot=(5.5 * s * sn(f, n, 0.0), 0, 0))         # opposite the same-side leg (r3: 4 -> 5.5)""",
    """            k.key("Arm_" + side, f, rot=(9.0 * s * sn(f, n, 0.0), 0, 0))         # opposite the same-side leg (r4 MC3: 9; r3 5.5)""")
# MC1: the kneeling shin leans back ~10 deg (the ankle 0.025 further back, 0.054 lower; the knee stays pinned)
rep("""    L = [(0, aL), (6, aL), (11, aL + Vector((0, 0.18, 0.10))), (15, aL + Vector((0, 0.31, 0.16))), (18, aL + Vector((0, 0.34, 0.155))),
         (52, aL + Vector((0, 0.34, 0.155))), (62, aL + Vector((0, 0.24, 0.11))), (70, aL + Vector((0, 0.08, 0.07))),""",
    """    L = [(0, aL), (6, aL), (11, aL + Vector((0, 0.18, 0.10))), (15, aL + Vector((0, 0.32, 0.13))), (18, aL + Vector((0, 0.365, 0.101))),
         (52, aL + Vector((0, 0.365, 0.101))), (62, aL + Vector((0, 0.24, 0.10))), (70, aL + Vector((0, 0.08, 0.07))),""")   # r4 MC1
rep("""    TL = [(0, 0), (6, 0), (18, 26), (52, 26), (62, 18), (70, 6), (76, 0), (100, 0)]""",
    """    TL = [(0, 0), (6, 0), (18, 16), (52, 16), (62, 14), (70, 6), (76, 0), (100, 0)]   # r4: toes 26 -> 16 with the flatter shin""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
