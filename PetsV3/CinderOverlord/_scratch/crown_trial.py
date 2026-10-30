# python crown_trial.py <centre> <middle> <outer> : set the crown blade heights in the pet file (r13 MUST 3 area trials)
import io, re, sys
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()
c, m, o = sys.argv[1:4]
s = re.sub(r"\(-CR_X1, [0-9.]+, 0.042, -24, 24\), \(-CR_X2, [0-9.]+, 0.050, -12, 24\)",
           "(-CR_X1, %s, 0.042, -24, 24), (-CR_X2, %s, 0.050, -12, 24)" % (o, m), s)
s = re.sub(r"\(0.0, [0-9.]+, 0.064, 0, 24\), \(CR_X2, [0-9.]+, 0.050, 12, 24\)",
           "(0.0, %s, 0.064, 0, 24), (CR_X2, %s, 0.050, 12, 24)" % (c, m), s)
s = re.sub(r"\(CR_X1, [0-9.]+, 0.042, 24, 24\)\)\)", "(CR_X1, %s, 0.042, 24, 24)))" % o, s)
io.open(p, "w", encoding="utf-8").write(s)
print("crown", c, m, o)
