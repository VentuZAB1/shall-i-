p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\PermafrostTitan.py"
t = open(p, encoding="utf-8").read()
rep = [
("""    B.seg((0, 0.0, 1.56), (0, -0.14, 1.74), 0.12, 0.10, JOINT_D, "Head", ext=0.02, rnd=0.4)            # neck joint""",
 """    B.add((0, -0.085, 1.665), (0.112, 0.105, 0.095), JOINT_D, "Head", rnd=0.45)                     # neck joint
    # (a rounded slate knuckle centred on the throat pivot: a head bow / lift turns it in place)"""),
("""    B.add((0, -0.29, 1.722), (0.122, 0.115, 0.052), MAUVE, "Jaw", top=(1.0, 0.95), bot=(0.86, 0.90), rnd=0.34)""",
 """    B.add((0, -0.295, 1.732), (0.120, 0.105, 0.046), MAUVE, "Jaw", top=(1.0, 0.95), bot=(0.84, 0.86), rnd=0.34)"""),
("""def joints():
    out = [((0, 0.0, 1.62), (0, -0.08, 1.72), 0.13, "Head")]""",
 """def joints():
    out = [((0, 0.0, 1.62), (0, -0.10, 1.70), 0.15, "Head")]"""),
("""HEAD_XF = []""",
 """HEAD_XF = [((0, -0.10, 1.66), 1.0, ["Head", "Jaw"], (0, -0.03, 0.035))]   # head group lifted / forward (chin
#   clears the chest top in the kneel bow and the bellow lift) - a pure translation, built at final size"""),
]
for a, b in rep:
    if a not in t:
        print("MISSING", a[:70])
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("ok")
