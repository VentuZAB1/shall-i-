# python CinderOverlord/_scratch/gold_cmp.py Name [Name...]  -> gold px at 64 px (portrait icon) under several windows
import sys, os, colorsys, json
from PIL import Image
R = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
WIN = {"kit_29-58_s.5_v.45": (29, 58, 0.5, 0.45), "review_38-48_s.6": (38, 48, 0.6, 0.45),
       "rendered_40-62_s.6_v.55": (40, 62, 0.6, 0.55)}
def run(p):
    im = Image.open(p).convert("RGBA").resize((64, 64), Image.LANCZOS)
    px = im.load()
    res = {}
    for k, (h0, h1, s0, v0) in WIN.items():
        def g(x, y):
            if not (0 <= x < 64 and 0 <= y < 64):
                return False
            r, gg, b, a = px[x, y]
            if a <= 128:
                return False
            h, s, v = colorsys.rgb_to_hsv(r / 255, gg / 255, b / 255)
            return h0 <= h * 360 <= h1 and s >= s0 and v >= v0
        allp = [(x, y) for y in range(64) for x in range(64) if g(x, y)]
        core = [(x, y) for (x, y) in allp if sum(g(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) >= 2]
        res[k] = [len(allp), len(core)]
    return res
for n in sys.argv[1:]:
    print(n, json.dumps({v: run(os.path.join(R, n, n + f)) for v, f in (("portrait", "_icon.png"), ("game", "_icon_game.png")) if os.path.exists(os.path.join(R, n, n + f))}))
