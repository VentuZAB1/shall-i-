# python FrostcrownDragon/_scratch/white_mask.py <strip.png> [cell] : (builder D scratch) ice-white with the review-7
# mask: the 128 px strip cell (x 6-133, y 6-133 for cell 0; +134 px per cell), pet pixels = max(|R-52|, |G-62|,
# |B-74|) > 6 (the cell background), luma = 0.299 R + 0.587 G + 0.114 B, s = HSV saturation, no resize, no filter.
# portrait rule: luma > 215 and s < 0.15; loose rule: luma > 200 and s < 0.20; also the mean luma of the pet pixels.
import sys, colorsys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGB")
cell = int(sys.argv[2]) if len(sys.argv) > 2 else 0
x0 = 6 + cell * 134
c = im.crop((x0, 6, x0 + 128, 134))
pts = [p for p in c.getdata() if max(abs(p[0] - 52), abs(p[1] - 62), abs(p[2] - 74)) > 6]
n = len(pts)
por = loo = 0
L = 0.0
for r, g, b in pts:
    l = 0.299 * r + 0.587 * g + 0.114 * b
    L += l
    s = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[1]
    if l > 215 and s < 0.15:
        por += 1
    if l > 200 and s < 0.20:
        loo += 1
print("cell %d (x %d-%d, y 6-133): pet px %d | portrait rule (luma > 215, s < 0.15) %.1f %% | loose rule (luma > 200, "
      "s < 0.20) %.1f %% | mean luma %.0f" % (cell, x0, x0 + 127, n, 100.0 * por / n, 100.0 * loo / n, L / n))
