# python EclipseSeraph/_scratch/seraph_stats.py Name [Name...] : review-1 Seraph metrics on the 64 px portrait icon
# (pet px = alpha > 200): near-white (lum > 200) share, mean HSV saturation, dark (lum < 90) share, gold / red px
import sys, colorsys
from PIL import Image
for n in sys.argv[1:]:
    for f in ("_icon.png", "_icon_game.png"):
        try:
            im = Image.open("%s/%s%s" % (n, n, f)).convert("RGBA").resize((64, 64), Image.LANCZOS)
        except FileNotFoundError:
            continue
        px = [p for p in im.getdata() if p[3] > 200]
        t = len(px)
        L = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b, a in px]
        S = [colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[1] for r, g, b, a in px]
        gold = red = 0
        for r, g, b, a in px:
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            gold += 0.08 <= h <= 0.16 and s > 0.5 and v > 0.45
            red += (h < 0.03 or h > 0.95) and s > 0.45 and v > 0.45
        print("%s%s: px %d white(lum>200) %.1f%% sat %.2f dark(lum<90) %.1f%% gold %d red %d" % (
            n, f, t, 100.0 * sum(l > 200 for l in L) / t, sum(S) / t, 100.0 * sum(l < 90 for l in L) / t, gold, red))
