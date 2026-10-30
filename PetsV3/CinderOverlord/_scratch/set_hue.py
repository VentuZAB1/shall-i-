# python CinderOverlord/_scratch/set_hue.py body=r,g,b pale=r,g,b rose=r,g,b  -> rewrites the 3 palette lines in pets/CinderOverlord.py
import io, re, sys
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
opts = dict(a.split("=", 1) for a in sys.argv[1:])
names = {"body": "PLUM_OBS", "pale": "PALE_S", "rose": "ROSE", "lava": "LAVA", "crown": "CROWN_IN"}
t = io.open(P, encoding="utf-8").read()
for k, v in opts.items():
    nm = names[k]
    rgb = "(%s)" % ", ".join(x.strip() for x in v.split(","))
    t, n = re.subn(r"^(%s = )\(\d+, \d+, \d+\)" % nm, lambda m: m.group(1) + rgb, t, count=1, flags=re.M)
    assert n == 1, nm
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print(opts)
