import re
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\PermafrostTitan.py"
s = open(p, encoding="utf-8").read()
a = s.index("def model(k):")
b = s.index("# ------------------------------------------------------------------ rig")
new_model = open(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan\_scratch\model_v3.txt", encoding="utf-8").read()
s = s[:a] + new_model + "\n\n" + s[b:]
open(p, "w", encoding="utf-8").write(s)
print("patched")
