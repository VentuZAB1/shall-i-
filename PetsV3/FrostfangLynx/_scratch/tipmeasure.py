# usage: python tipmeasure.py img1 img2 ...  -> centroid of the black tail tip (max channel < 90, lower 60 % of frame)
import sys
from PIL import Image
import numpy as np
res = []
for p in sys.argv[1:]:
    a = np.asarray(Image.open(p).convert("RGB")).astype(int)
    h = a.shape[0]
    m = a.max(2) < 90
    m[: int(h * 0.4), :] = False
    ys, xs = np.nonzero(m)
    c = (round(xs.mean(), 1), round(ys.mean(), 1), int(m.sum())) if len(xs) else None
    res.append(c)
    print(p.split("/")[-1], c)
if len(res) == 2 and all(res):
    dx, dy = res[1][0] - res[0][0], res[1][1] - res[0][1]
    print("shift dx %.1f dy %.1f dist %.1f px" % (dx, dy, (dx * dx + dy * dy) ** 0.5))
