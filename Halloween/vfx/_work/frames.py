# python frames.py <png name> <cols> <frame list e.g. 0,8,16 or 0-15> <scale> [out suffix]
# -> _work/<name>_frames<suffix>.png : selected frames, rows = over dark | over sky (alpha) | over sky (additive)
import sys, os
import numpy as np
from PIL import Image

VFX = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\vfx"
name, cols = sys.argv[1], int(sys.argv[2])
spec = sys.argv[3]
scale = float(sys.argv[4])
suffix = sys.argv[5] if len(sys.argv) > 5 else ""
fr = []
for part in spec.split(","):
    if "-" in part:
        a, b = part.split("-")
        fr += list(range(int(a), int(b) + 1))
    else:
        fr.append(int(part))
im = np.asarray(Image.open(os.path.join(VFX, name + ".png")).convert("RGBA")).astype(np.float32) / 255.0
px = im.shape[0] // cols


def s2l(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def l2s(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


rows = []
for bg, add in (((0.05, 0.04, 0.06), False), ((140 / 255, 170 / 255, 205 / 255), False),
                ((140 / 255, 170 / 255, 205 / 255), True)):
    row = []
    for f in fr:
        r, c = divmod(f, cols)
        t = im[r * px:(r + 1) * px, c * px:(c + 1) * px]
        rgb, a = s2l(t[..., :3]), t[..., 3:4]
        b = s2l(np.array(bg, np.float32))[None, None, :] * np.ones_like(rgb)
        o = b + rgb * a if add else b * (1 - a) + rgb * a
        o = (l2s(o) * 255 + 0.5).astype(np.uint8)
        o[:, -1] = 60
        row.append(o)
    rows.append(np.concatenate(row, axis=1))
out = Image.fromarray(np.concatenate(rows, axis=0))
out = out.resize((int(out.width * scale), int(out.height * scale)), Image.LANCZOS)
p = os.path.join(VFX, "_work", f"{name}_frames{suffix}.png")
out.save(p)
print(p, out.size)
