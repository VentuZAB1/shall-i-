# HubGrime - quick 2D look: decal PNG(s) over a pre-lit studded swatch (linear-light blend), for fast iteration.
# python gen\quickview.py OUT.png NAME [NAME...] [--bg green|blue|cream|orange] [--scale 0.5] [--tilt 0.35]
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grime_lib import HERE, DECALS, lin, to_srgb  # noqa: E402

BG = {"green": (128, 170, 96), "blue": (96, 132, 170), "cream": (222, 205, 170), "orange": (230, 150, 105),
      "black": (0, 0, 0), "white": (255, 255, 255), "magenta": (255, 0, 255)}
LIT = None


def stud_surface(w, h, pps, col, lit=True):
    global LIT
    if LIT is None:
        LIT = np.load(os.path.join(HERE, "mock", "stud_lit.npy"))
    base = lin(col)
    if not lit:
        return np.ones((h, w, 3), np.float32) * base
    t = LIT.shape[0]
    ys = ((np.arange(h) + 0.5) / pps * t).astype(int) % t
    xs = ((np.arange(w) + 0.5) / pps * t).astype(int) % t
    f = LIT[ys][:, xs]
    return base[None, None, :] * f[..., None]


def comp(dst_lin, png_path, x, y, scale=1.0):
    im = Image.open(png_path).convert("RGBA")
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    a = np.asarray(im).astype(np.float32) / 255.0
    rgb = lin(np.asarray(im)[..., :3].astype(np.float32))
    al = a[..., 3:4]
    h, w = al.shape[:2]
    H, W = dst_lin.shape[:2]
    y0, x0 = max(0, y), max(0, x)
    y1, x1 = min(H, y + h), min(W, x + w)
    if y1 <= y0 or x1 <= x0:
        return dst_lin
    sub = dst_lin[y0:y1, x0:x1]
    ss = (slice(y0 - y, y1 - y), slice(x0 - x, x1 - x))
    dst_lin[y0:y1, x0:x1] = rgb[ss] * al[ss] + sub * (1 - al[ss])
    return dst_lin


def save(lin_img, path):
    Image.fromarray(np.round(to_srgb(lin_img) * 255).astype(np.uint8)).save(path)


if __name__ == "__main__":
    args = sys.argv[1:]
    out = args[0]
    names, bg, scale = [], "green", 1.0
    i = 1
    while i < len(args):
        if args[i] == "--bg":
            bg = args[i + 1]
            i += 2
        elif args[i] == "--scale":
            scale = float(args[i + 1])
            i += 2
        else:
            names.append(args[i])
            i += 1
    ims = [Image.open(os.path.join(DECALS, n + ".png")) for n in names]
    pad = 20
    W = sum(int(im.width * scale) + pad for im in ims) + pad
    H = max(int(im.height * scale) for im in ims) + 2 * pad
    bgs = bg.split(",")
    rows = []
    for b in bgs:
        img = stud_surface(W, H, 73 * scale, BG[b])
        x = pad
        for n, im in zip(names, ims):
            comp(img, os.path.join(DECALS, n + ".png"), x, pad, scale)
            x += int(im.width * scale) + pad
        rows.append(img)
    save(np.concatenate(rows, 0), out)
    print("wrote", out)
