# python _vfx/pack.py : Blender frames (out/<fx>/###.png) -> Roblox-ready textures in tex/
#   brightness -> alpha (black = transparent), + soft glow, 16 frames -> 4x4 flipbook sheet (1024 px)
#   white effects stay white (tinted per pet in Roblox); "fire" keeps its colours
# also writes _preview.png (every texture on a dark checker) for review
import os, sys
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
TEX = os.path.join(HERE, "tex")
os.makedirs(TEX, exist_ok=True)

GLOW = {"bolt": 1.3, "arc": 1.1, "ring": 0.45, "slash": 0.7, "splash": 0.25, "fire": 0.35, "smoke": 0.0,
        "swirl": 0.35, "star": 1.0, "flare": 1.3, "streak": 0.9, "drip": 0.25, "bubble": 0.35, "leaf": 0.0,
        "zap1": 1.1, "zap2": 1.1, "zap3": 1.1, "silk": 0.5}
COLOURED = {"fire"}


def process(path, name):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im).astype(np.float32) / 255.0
    srgb = a[..., :3]
    lin = np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)   # PNG is sRGB: back to the
    rgb = lin * a[..., 3:4]                                                         # emission values I designed
    k = GLOW.get(name, 0.5)
    if k > 0:
        w = im.size[0]
        src = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8))
        g1 = np.asarray(src.filter(ImageFilter.GaussianBlur(w * 0.012))).astype(np.float32) / 255.0
        g2 = np.asarray(src.filter(ImageFilter.GaussianBlur(w * 0.035))).astype(np.float32) / 255.0
        rgb = rgb + (g1 * 0.6 + g2 * 0.9) * k
    alpha = np.clip(rgb.max(axis=2), 0, 1)
    if name in COLOURED:
        col = np.where(alpha[..., None] > 1e-4, rgb / np.maximum(alpha[..., None], 1e-4), 0)
        col = np.clip(col, 0, 1) ** (1 / 2.2)
    else:
        col = np.ones_like(rgb)
    outp = np.dstack([col, alpha])
    return Image.fromarray((outp * 255 + 0.5).astype(np.uint8), "RGBA")


def main(only):
    made = []
    for name in sorted(os.listdir(OUT)):
        d = os.path.join(OUT, name)
        if not os.path.isdir(d) or (only and name not in only):
            continue
        frames = sorted(f for f in os.listdir(d) if f.endswith(".png"))
        imgs = [process(os.path.join(d, f), name) for f in frames]
        if len(imgs) == 16:
            s = imgs[0].size[0]
            sheet = Image.new("RGBA", (s * 4, s * 4), (255, 255, 255, 0))
            for i, im in enumerate(imgs):
                sheet.paste(im, ((i % 4) * s, (i // 4) * s))
            sheet.save(os.path.join(TEX, f"fx_{name}.png"))
        else:
            imgs[0].save(os.path.join(TEX, f"fx_{name}.png"))
        made.append(name)
    # preview
    files = sorted(f for f in os.listdir(TEX) if f.startswith("fx_") and f.endswith(".png"))
    cell = 340
    cols = 4
    rows = (len(files) + cols - 1) // cols
    prev = Image.new("RGB", (cols * cell, rows * cell), (24, 28, 34))
    chk = np.indices((cell, cell)).sum(axis=0) // 20 % 2
    for i, f in enumerate(files):
        im = Image.open(os.path.join(TEX, f)).convert("RGBA")
        im.thumbnail((cell - 20, cell - 20))
        bg = Image.fromarray(np.where(chk[..., None] == 1, 44, 30).astype(np.uint8).repeat(3, axis=2))
        tint = (150, 200, 255) if "fire" not in f else (255, 255, 255)
        a = np.asarray(im).astype(np.float32) / 255
        rgb = a[..., :3] * np.array(tint) / 255
        base = np.asarray(bg.crop((0, 0, im.size[0], im.size[1]))).astype(np.float32) / 255
        comp = base * (1 - a[..., 3:4]) + rgb * a[..., 3:4]
        tile = Image.fromarray((np.clip(comp, 0, 1) * 255).astype(np.uint8))
        prev.paste(tile, ((i % cols) * cell + 10, (i // cols) * cell + 10))
    prev.save(os.path.join(HERE, "_preview.png"))
    print("packed", made)


if __name__ == "__main__":
    main(set(sys.argv[1:]))
