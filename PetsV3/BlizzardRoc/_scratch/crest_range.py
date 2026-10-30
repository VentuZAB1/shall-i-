# python BlizzardRoc/_scratch/crest_range.py <view> <clip> : (builder D scratch) crest position per walk tile: the
# FROST_V crest-plume pixels (hue 0.65-0.80, s > 0.25, v > 0.6) in the top 45 % of each renders/pose_<view>_<clip>_NN.png
# (300 px) -> centroid x / y per frame and the x / y range over the clip (px)
import sys, glob, re, colorsys
from PIL import Image
view, clip = sys.argv[1], sys.argv[2]
fs = sorted(glob.glob("BlizzardRoc/renders/pose_%s_%s_*.png" % (view, clip)), key=lambda p: int(re.findall(r"_(\d+)\.png$", p)[0]))
xs, ys, rows = [], [], []
for p in fs:
    im = Image.open(p).convert("RGB")
    W, H = im.size
    pts = []
    for y in range(int(H * 0.45)):
        for x in range(W):
            r, g, b = im.getpixel((x, y))
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if 0.65 <= h <= 0.80 and s > 0.25 and v > 0.6:
                pts.append((x, y))
    if not pts:
        continue
    cx = sum(q[0] for q in pts) / len(pts)
    cy = sum(q[1] for q in pts) / len(pts)
    xs.append(cx); ys.append(cy)
    rows.append("f%s (%.1f, %.1f)" % (re.findall(r"_(\d+)\.png$", p)[0], cx, cy))
print(" ".join(rows))
print("%s %s crest centroid range: x %.1f px, y %.1f px (tile %d px)" % (view, clip, max(xs) - min(xs), max(ys) - min(ys), W))
