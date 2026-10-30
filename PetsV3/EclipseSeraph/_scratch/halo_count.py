# python EclipseSeraph/_scratch/halo_count.py <dir> : (builder D scratch) for every <dir>/<tag>_full.png + _alone.png,
# halo gold px (h .08-.17, s > .45, v > .45, alpha > 128) and the hidden share = 1 - full / alone
import glob, colorsys, os, re, sys
from PIL import Image


def gold(p):
    n = 0
    for r, g, b, a in Image.open(p).convert("RGBA").getdata():
        if a > 128:
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if 0.08 <= h <= 0.17 and s > 0.45 and v > 0.45:
                n += 1
    return n


rows = []
for p in glob.glob(os.path.join(sys.argv[1], "*_full.png")):
    tag = os.path.basename(p)[:-9]
    a, b = gold(p), gold(p.replace("_full.png", "_alone.png"))
    c, f = tag.rsplit("_", 1)
    rows.append((c, int(f), a, b))
rows.sort()
print(" | ".join("%s f%d %d/%d hidden %.0f%%" % (c, f, a, b, 100.0 * (1 - a / max(1, b))) for c, f, a, b in rows))
