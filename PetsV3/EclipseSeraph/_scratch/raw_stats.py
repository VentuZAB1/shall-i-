# python EclipseSeraph/_scratch/raw_stats.py <png> [size] : metrics on a raw render (transparent bg, NO icon outline),
# cropped to the alpha bbox and fitted to size px: near-white (lum > 200), mean sat, dark (lum < 90 / < 70), gold, red
import sys, colorsys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGBA")
sz = int(sys.argv[2]) if len(sys.argv) > 2 else 64
im = im.crop(im.split()[3].point(lambda v: 255 if v > 8 else 0).getbbox())
w, h = im.size
f = sz / max(w, h)
im = im.resize((max(1, int(w * f)), max(1, int(h * f))), Image.LANCZOS)
px = [p for p in im.getdata() if p[3] > 200]
t = len(px)
L = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b, a in px]
S = [colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[1] for r, g, b, a in px]
gold = red = 0
for r, g, b, a in px:
    hh, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    gold += 0.08 <= hh <= 0.16 and s > 0.5 and v > 0.45
    red += (hh < 0.03 or hh > 0.95) and s > 0.45 and v > 0.45
print("%s @%d: px %d lum %.0f white(>200) %.1f%% sat %.2f dark(<90) %.1f%% dark(<70) %.1f%% gold %d red %d" % (
    sys.argv[1].split("\\")[-1].split("/")[-1], sz, t, sum(L) / t, 100.0 * sum(l > 200 for l in L) / t, sum(S) / t,
    100.0 * sum(l < 90 for l in L) / t, 100.0 * sum(l < 70 for l in L) / t, gold, red))
