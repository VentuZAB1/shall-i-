import os
import numpy as np
from PIL import Image

V = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\vfx"
for name, cols in (("CandleFlame_8x8", 8), ("FireTongue_8x8", 8), ("SmokeWisp_4x4", 4)):
    a = np.asarray(Image.open(os.path.join(V, name + ".png"))).astype(float)[..., 3] / 255
    px = a.shape[0] // cols
    bots, tops, wids, cx = [], [], [], []
    for i in range(cols * cols):
        r, c = divmod(i, cols)
        t = a[r * px:(r + 1) * px, c * px:(c + 1) * px]
        m = t > 0.08
        if not m.any():
            continue
        ys, xs = np.nonzero(m)
        tops.append(ys.min() / px)
        bots.append(1 - ys.max() / px)
        wids.append((xs.max() - xs.min()) / px)
        cx.append(xs.mean() / px)
    print(name, "bottom margin min/med", round(min(bots), 3), round(float(np.median(bots)), 3),
          "top margin min/med", round(min(tops), 3), round(float(np.median(tops)), 3),
          "width med/max", round(float(np.median(wids)), 3), round(max(wids), 3), "cx med", round(float(np.median(cx)), 3))
for name in ("Glow", "Ember", "Mist"):
    a = np.asarray(Image.open(os.path.join(V, name + ".png"))).astype(float) / 255
    print(name, a.shape, "max alpha", round(a[..., 3].max(), 3), "centre rgba", np.round(a[a.shape[0] // 2, a.shape[1] // 2], 3))
