# python EclipseSeraph/_scratch/satcells.py <strip.png> <px> : per strip cell, pet px (not bg), mean sat, saturated share
# (s > 0.35), dark (lum < 90), near-white (lum > 200) - 3 decimals
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
    S = [colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[1] for r, g, b in pts]
    L = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b in pts]
    t = len(pts)
    print("cell %d: px %d sat %.3f satshare %.1f%% dark90 %.1f%% white200 %.1f%%" % (
        i, t, sum(S) / t, 100.0 * sum(s > 0.35 for s in S) / t, 100.0 * sum(l < 90 for l in L) / t,
        100.0 * sum(l > 200 for l in L) / t))
