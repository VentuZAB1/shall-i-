# usage: python earmeasure.py a.png b.png ycut -> top ICE tip of each ear (pixels above row ycut), and the move
import sys
from PIL import Image
import numpy as np
def ears(p, ycut):
    a = np.asarray(Image.open(p).convert("RGB")).astype(int)
    r, b = a[..., 0], a[..., 2]
    m = (b > 200) & (r < 170) & (b - r > 60)
    m[ycut:, :] = False
    ys, xs = np.nonzero(m); cx = xs.mean(); out = []
    for side in (xs < cx, xs >= cx):
        X, Y = xs[side], ys[side]; i = Y.argmin(); out.append((int(X[i]), int(Y[i])))
    return out
ycut = int(sys.argv[3])
A, B = ears(sys.argv[1], ycut), ears(sys.argv[2], ycut)
for nm, a, b in zip(("screen-left ear", "screen-right ear"), A, B):
    print(nm, a, "->", b, "tip move %.1f px" % (((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5))
