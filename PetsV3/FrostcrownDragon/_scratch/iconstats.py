# python FrostcrownDragon/_scratch/iconstats.py Name [Name...] : mean luminance / dark share / near-white / gold of the
# pet pixels of <Name>_icon.png scaled to 128 px (the reviewer's measure, approximately)
import sys, colorsys
from PIL import Image
for n in sys.argv[1:]:
    im = Image.open("%s/%s_icon.png" % (n, n)).convert("RGBA").resize((128, 128), Image.LANCZOS)
    px = [p for p in im.getdata() if p[3] > 200]
    lum = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b, a in px]
    tot = len(px)
    gold = 0
    white = 0
    red = 0
    for (r, g, b, a), L in zip(px, lum):
        h, s_, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if 0.08 <= h <= 0.16 and s_ > 0.5 and v > 0.45:
            gold += 1
        if L > 215 and s_ < 0.15:
            white += 1
        if (h < 0.03 or h > 0.95) and s_ > 0.45 and v > 0.45:
            red += 1
    print(n, "lum %.0f" % (sum(lum) / tot), "dark %.0f%%" % (100.0 * sum(1 for L in lum if L < 70) / tot),
          "white %.1f%%" % (100.0 * white / tot), "gold %.1f%%" % (100.0 * gold / tot), "red %.1f%%" % (100.0 * red / tot))
