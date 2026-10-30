# builder D scratch: six-wing fly-cycle candidates -> paths json for path6.py
import sys, json, math
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3")
import importlib.util
spec = importlib.util.spec_from_file_location("wing3s", r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\wing3.py")
# wing3 imports mathutils (Blender); reimplement stroke here (same maths as wing3.stroke)
def _ease(u): return 0.5 - 0.5 * math.cos(math.pi * u)
def stroke(ph, top=28.0, bot=-48.0, down=0.45, sweep=10.0, twist=12.0, fold=34.0):
    ph %= 1.0
    if ph < down:
        u = ph / down
        return dict(up=top + (bot - top) * _ease(u), fwd=sweep * math.sin(math.pi * u) - 2,
                    twist=twist * math.sin(math.pi * u), tip=-5 - 10 * math.sin(math.pi * u) + 13 * u)
    u = (ph - down) / (1 - down)
    return dict(up=bot + (top - bot) * _ease(u), fwd=-2 - 0.8 * sweep * math.sin(math.pi * u),
                twist=-0.7 * twist * math.sin(math.pi * u), tip=8 + fold * math.sin(math.pi * u) - 13 * u)
N = 28
CANDS = json.loads(sys.argv[1])   # label: {"A": [top, bot, lagf, fwd0, twist0, fold], ...}
out = {}
for lab, spec_ in CANDS.items():
    keys = []
    for f in range(0, N + 1):
        d = {}
        for P, vals in spec_.items():
            top, bot, lag, fwd0, tw0, fold = vals[:6]
            tip0 = vals[6] if len(vals) > 6 else 0.0
            sw = vals[7] if len(vals) > 7 else 8.0
            twa = vals[8] if len(vals) > 8 else 10.0
            tk = vals[9] if len(vals) > 9 else 1.0
            w = stroke((f - lag) / N, top=top, bot=bot, down=0.45, sweep=sw, twist=twa, fold=fold)
            d[P] = [round(w["up"], 2), round(w["fwd"] + fwd0, 2), round(w["twist"] + tw0, 2), round(w["tip"] * tk + tip0, 2)]
        keys.append([f, d])
    out[lab] = keys
json.dump(out, open(sys.argv[2], "w"))
print(len(out), "paths")
