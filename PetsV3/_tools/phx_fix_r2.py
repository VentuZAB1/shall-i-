# one-off patch: Inferno Phoenix review 2 K1 (fly plumes) + M1 (narrower collar row)
import os
os.chdir(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3")
p = "pets/InfernoPhoenix.py"
s = open(p, encoding="utf-8").read()
i0 = s.index("def fly_stream(ph, c):")
i1 = s.index("def fly_pose(")
s = s[:i0] + '''def fly_stream(ph, c):
    """the BURNING WAKE (review 2 K1): X2 / X3 baselines cancel the chain's rest curl (seg1 -34.6 -> seg2 -20 -> vane
    +14 deg), so in flight the plumes stream nearly straight behind (ref #8), seg1 ~12 deg under the flight line, vanes
    ~+8 deg, with a travelling S on top (X1 peaking 0.15 after the downstroke start, lag 0.10 per segment); forked fan
    L -8 / R +8; the chains offset 0.03 cycle"""
    q = ph - 0.03 * LAG[c]
    fan = {"L": -8.0, "C": 0.0, "R": 8.0}[c]
    w = lambda d: math.cos(2 * math.pi * (q - d))
    return dict(x1=-22 + 4 * w(0.15), x2=-11 + 7 * w(0.25), x3=-18 + 7 * w(0.35), y1=fan, y3=3 * w(0.60))


''' + s[i1:]
a = "neck_cape(B, n1a, n1b, 0.15, [(0.90, (-0.11, -0.04, 0.04, 0.11), True)],"
assert s.count(a) == 1
s = s.replace(a, "neck_cape(B, n1a, n1b, 0.15, [(0.90, (-0.085, -0.03, 0.03, 0.085), True)],      # review 2 M1")
open(p, "w", encoding="utf-8").write(s)
print("K1 + M1 ok")
