# python EclipseSeraph/_scratch/halo_vis.py <clip> : (builder D scratch) visible halo gold px (h .08-.17, s > .45,
# v > .45) in each renders/pose_game_<clip>_NN.png, and the ratio to the clip's first rendered frame
import sys, glob, os, colorsys, re
from PIL import Image
clip = sys.argv[1]
fs = sorted(glob.glob("EclipseSeraph/renders/pose_game_%s_*.png" % clip), key=lambda p: int(re.findall(r"_(\d+)\.png$", p)[0]))
base = None
out = []
for p in fs:
    im = Image.open(p).convert("RGB")
    n = 0
    for r, g, b in im.getdata():
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if 0.08 <= h <= 0.17 and s > 0.45 and v > 0.45:
            n += 1
    base = base or n
    out.append("f%s %d (%.0f%%)" % (re.findall(r"_(\d+)\.png$", p)[0], n, 100.0 * n / base))
print(" | ".join(out))
