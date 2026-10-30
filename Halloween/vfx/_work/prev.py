# quick iteration preview: python prev.py <png name> [scale] -> _work/<name>_prev.png
# (atlas over dark | over sky-blue alpha | over sky-blue additive), straight alpha assumed
import sys, os
import numpy as np
from PIL import Image

VFX = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\vfx"
name = sys.argv[1]
scale = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
im = np.asarray(Image.open(os.path.join(VFX, name + ".png")).convert("RGBA")).astype(np.float32) / 255.0


def s2l(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def l2s(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


rgb, a = s2l(im[..., :3]), im[..., 3:4]
outs = []
for bg, add in (((0.05, 0.04, 0.06), False), ((140 / 255, 170 / 255, 205 / 255), False),
                ((140 / 255, 170 / 255, 205 / 255), True)):
    b = s2l(np.array(bg, np.float32))[None, None, :] * np.ones_like(rgb)
    o = b + rgb * a if add else b * (1 - a) + rgb * a
    outs.append((l2s(o) * 255 + 0.5).astype(np.uint8))
out = np.concatenate(outs, axis=1)
img = Image.fromarray(out)
if scale != 1.0:
    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
p = os.path.join(VFX, "_work", name + "_prev.png")
img.save(p)
print(p, img.size)
