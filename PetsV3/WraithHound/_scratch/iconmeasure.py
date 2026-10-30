# usage: python iconmeasure.py [strip64] [strip128] -> per-slot mean Y (cell and creature-only), eye-box blue count
import sys
from PIL import Image
import numpy as np
def stats(path, px):
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    out = []
    for i in range(6):
        x0 = 6 + i * (px + 6); cell = a[6:6 + px, x0:x0 + px]
        Y = 0.299 * cell[..., 0] + 0.587 * cell[..., 1] + 0.114 * cell[..., 2]
        bg = cell[2, 2]
        m = np.abs(cell - bg).sum(2) > 30
        out.append((round(Y.mean(), 1), round(Y[m].mean(), 1)))
    return out
def blue(path, box):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    x0, y0, x1, y1 = box
    c = a[y0:y1 + 1, x0:x1 + 1]
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    m = (b > 140) & (b - r > 45) & (b - g > 35)
    return int(m.sum())
p64 = sys.argv[1] if len(sys.argv) > 1 else "renders/_icons_strip_64.png"
p128 = sys.argv[2] if len(sys.argv) > 2 else "renders/_icons_strip_128.png"
print("meanY 64 (cell, creature):", stats(p64, 64))
print("meanY 128 (cell, creature):", stats(p128, 128))
print("eye box 64 (16-30, 24-36) blue px:", blue(p64, (16, 24, 30, 36)))
print("eye box 128 (scaled x2 from the strip origin):", blue(p128, (6 + (16 - 6) * 2, 6 + (24 - 6) * 2, 6 + (30 - 6) * 2 + 1, 6 + (36 - 6) * 2 + 1)))
