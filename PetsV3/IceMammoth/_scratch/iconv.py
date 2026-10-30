# python iconv.py <icon.png> [hue_lo hue_hi]  median HSV of the body pixels of an icon (alpha > 200, hue window, s > 0.2)
import sys, colorsys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGBA").resize((128, 128), Image.LANCZOS)
lo, hi = (float(sys.argv[2]), float(sys.argv[3])) if len(sys.argv) > 3 else (170.0, 215.0)
vals = []
for r, g, b, a in im.getdata():
    if a < 200:
        continue
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    if lo <= h * 360 <= hi and s > 0.2:
        vals.append((h * 360, s, v))
vals.sort(key=lambda x: x[2])
m = vals[len(vals) // 2]
print("n %d median V %.2f  (H %.0f S %.2f)" % (len(vals), m[2], m[0], m[1]))
