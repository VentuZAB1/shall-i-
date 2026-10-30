import sys
pet, src = sys.argv[1], sys.argv[2]
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\%s.py" % pet
s = open(p, encoding="utf-8").read()
a = s.index("def model(k):")
b = s.index("# ------------------------------------------------------------------ rig")
s = s[:a] + open(src, encoding="utf-8").read().rstrip() + "\n\n\n" + s[b:]
open(p, "w", encoding="utf-8").write(s)
print("patched", pet)
