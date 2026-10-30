# r4b: the held TOP of each wave = the claw highest, up and out (F1); the trough = folded down in front (F2).
# (r4a modulated only the carpus, and its "peak" folded the claw back over the shell = lower, not a display)
import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
t = io.open(P, encoding="utf-8").read()
old_l = "    lift_r = [(0, 0), (18, 45), (74, 45), (80, 32), (90, 32), (97, 28), (104, 0), (120, 0)]\n"
new_l = ("    lift_r = [(0, 0), (18, 40), (26, 58), (30, 58), (38, 22), (48, 58), (52, 58), (60, 22), (70, 58), (74, 58),\n"
         "              (80, 32), (90, 32), (97, 28), (104, 0), (120, 0)]                  # merus: the wave's main arc\n")
old_f = ("    fore_r = [(0, 0), (18, 12), (26, 44), (30, 44), (38, 6), (48, 44), (52, 44), (60, 6), (70, 44), (74, 44),\n"
         "              (80, 0), (120, 0)]\n")
new_f = ("    fore_r = [(0, 0), (18, 8), (26, 16), (30, 16), (38, -4), (48, 16), (52, 16), (60, -4), (70, 16), (74, 16),\n"
         "              (80, 0), (120, 0)]                                                    # carpus follows\n")
assert old_l in t and old_f in t
t = t.replace(old_l, new_l).replace(old_f, new_f)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
