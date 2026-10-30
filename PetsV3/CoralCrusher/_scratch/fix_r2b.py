import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
s = io.open(P, encoding="utf-8").read()
# 1) pale lip -> a pale underside "bowl" hugging the lower shell up to just under the rim band (side-visible)
a = s.index("    def lip_w(hw, hb, dz):")
b = s.index("    # stepped rear plate (r2 M4a)")
s = s[:a] + '''    # pale underside (r2 M4b): a cream skin hugging the lower carapace from just under the slate rim band down to
    # the belly (0.008 proud), so it shows as a cream band from the side between the legs
    B.tube([ring(y, hw + 0.008, zc - 0.012, 0.012, hb + 0.008, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]],
           BELLY_PALE, "Spine", nostud=True)                                                       # pale underside
''' + s[b:]
rep = [
('''        B.add(S, (0.080 * c, 0.080 * c, 0.080 * c), SHELL_D, arm, rnd=0.45)                        # shoulder knuckle''',
 '''        B.add(S, (0.080 * c, 0.080 * c, 0.080 * c), BRONZE_D, arm, rnd=0.45)                       # shoulder knuckle'''),
('''        B.add(E, (0.088 * c, 0.088 * c, 0.088 * c), SHELL_D, fore, rnd=0.42)                          # knuckle''',
 '''        B.add(E, (0.088 * c, 0.088 * c, 0.088 * c), BRONZE_D, fore, rnd=0.42)                         # knuckle'''),
('''        B.add(W, (0.095 * c, 0.095 * c, 0.095 * c), SHELL_D, claw, rnd=0.42)                          # wrist knuckle''',
 '''        B.add(W, (0.095 * c, 0.095 * c, 0.095 * c), BRONZE_D, claw, rnd=0.42)                         # wrist knuckle'''),
('''            B.add(K, (0.072, 0.072, 0.072), SHELL_D, shin, rnd=0.42)                                  # knee''',
 '''            B.add(K, (0.072, 0.072, 0.072), BRONZE_D, shin, rnd=0.42)                                 # knee (r2 M2)'''),
]
for x, y in rep:
    assert x in s, "MISSING " + x[:80]
    s = s.replace(x, y)
# 2) N2: drop the palm keel + merus keel strips (they read as plastic inserts)
a = s.index("        prings = []\n")
b = s.index("        for t, L in ((0.18, 0.08), (0.42, 0.095)")
s = s[:a] + "        # (r2 N2: the pale palm keel + merus keel strips were dropped - they read as plastic inserts)\n" + s[b:]
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
