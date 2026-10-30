# python CinderOverlord/_scratch/gold_tight.py <Name>
# Tight gold counter (review 4 MUST 3): the same 64 px icons as _tools/game_icon.py (<Name>_icon.png = portrait,
# <Name>_icon_game.png = game camera, LANCZOS to 64), but gold = hue 38-48 deg, saturation >= 0.6, value >= 0.45, and
# BLEND pixels excluded: a pixel counts only if at least 2 of its 4 neighbours also pass the gold test (an anti-aliased
# fringe pixel between gold and another colour has at most 1 gold neighbour along the edge normal).
import sys, os, json, colorsys
from PIL import Image
R = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
name = sys.argv[1]
def count(p):
    im = Image.open(p).convert("RGBA").resize((64, 64), Image.LANCZOS)
    px = im.load()
    def gold(x, y):
        if not (0 <= x < 64 and 0 <= y < 64):
            return False
        r, g, b, a = px[x, y]
        if a <= 128:
            return False
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        return 38 <= h * 360 <= 48 and s >= 0.6 and v >= 0.45
    win = core = 0
    for y in range(64):
        for x in range(64):
            if gold(x, y):
                win += 1
                if sum(gold(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) >= 2:
                    core += 1
    return win, core
out = {}
for k, f in (("portrait", name + "_icon.png"), ("game", name + "_icon_game.png")):
    w, c = count(os.path.join(R, name, f))
    out[k] = {"tight_window": w, "tight_no_blend": c}
print(json.dumps(out))
