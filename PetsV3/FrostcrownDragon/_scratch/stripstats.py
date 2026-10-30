# python FrostcrownDragon/_scratch/stripstats.py <strip.png> <px> : per cell of a pack_post / game_icon strip: pet px
# (differs from the cell background (52,62,74)), mean luminance, dark share (lum < 70), near-white (lum > 200 and
# s < 0.2), gold px (HSV 0.08-0.16, s > 0.5, v > 0.45), red px - the reviewer's strip method, approximately
import sys, colorsys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGB")
px = int(sys.argv[2])
n = (im.width - 6) // (px + 6)
for i in range(n):
    c = im.crop((6 + i * (px + 6), 6, 6 + i * (px + 6) + px, 6 + px))
    pts = [p for p in c.getdata() if abs(p[0] - 52) + abs(p[1] - 62) + abs(p[2] - 74) > 12]
    if not pts:
        continue
    L = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b in pts]
    gold = white = red = 0
    for (r, g, b), l in zip(pts, L):
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if 0.08 <= h <= 0.16 and s > 0.5 and v > 0.45:
            gold += 1
        if l > 200 and s < 0.2:
            white += 1
        if (h < 0.03 or h > 0.95) and s > 0.45 and v > 0.45:
            red += 1
    t = len(pts)
    print("cell %d: px %d lum %.0f dark %.0f%% white %.1f%% gold %d (%.1f%%) red %d" % (
        i, t, sum(L) / t, 100.0 * sum(1 for l in L if l < 70) / t, 100.0 * white / t, gold, 100.0 * gold / t, red))
