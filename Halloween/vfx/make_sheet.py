# SLINGSHOT Halloween VFX - review contact sheet (system Python + Pillow; run after vfx.py).
#   python "C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\vfx\make_sheet.py"
# -> vfx_contact_sheet.png : every texture + a run of frames from each flipbook, each shown
#    (1) over a dark background (normal alpha blend = LightEmission 0) and additive (= LightEmission 1),
#    (2) over the daytime sky-blue sRGB (140,170,205) (normal alpha blend = LightEmission 0),
#    (3) over the same sky, additive (= LightEmission 1),
#    plus the CandleFlame loop-seam check (frame 63 -> frame 0) and the full atlases.
# Blending is done in linear light, the PNGs are straight (un-premultiplied) alpha.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

VFX = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(VFX, "vfx_contact_sheet.png")
DARK = (12, 10, 16)
SKY = (140, 170, 205)
PAPER = (30, 30, 36)
INK = (235, 235, 240)
DIM = (160, 160, 175)


def font(sz):
    for f in (r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


F_H, F_L, F_S = font(30), font(20), font(15)


def s2l(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def l2s(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def load(name):
    return np.asarray(Image.open(os.path.join(VFX, name)).convert("RGBA")).astype(np.float32) / 255.0


def frame(im, cols, i):
    px = im.shape[0] // cols
    r, c = divmod(i, cols)
    return im[r * px:(r + 1) * px, c * px:(c + 1) * px]


def comp(t, bg, add, size):
    rgb, a = s2l(t[..., :3]), t[..., 3:4]
    b = s2l(np.array(bg, np.float32) / 255.0)[None, None, :] * np.ones_like(rgb)
    o = b + rgb * a if add else b * (1 - a) + rgb * a
    img = Image.fromarray((l2s(o) * 255 + 0.5).astype(np.uint8))
    return img.resize(size, Image.LANCZOS) if img.size != size else img


MODES = [("over dark (LightEmission 0)", DARK, False), ("over dark, additive (LightEmission 1)", DARK, True),
         ("over sky (LightEmission 0)", SKY, False), ("over sky, additive (LightEmission 1)", SKY, True)]


def strip_block(title, sub, tiles, labels, cell):
    """tiles: list of RGBA float arrays; returns an image with one row per blend mode."""
    pad, lab_w, head = 8, 300, 64
    w = lab_w + len(tiles) * (cell[0] + pad) + pad
    h = head + len(MODES) * (cell[1] + pad) + 26
    img = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(img)
    d.text((14, 10), title, font=F_H, fill=INK)
    d.text((14, 44), sub, font=F_S, fill=DIM)
    for r, (mname, bg, add) in enumerate(MODES):
        y = head + r * (cell[1] + pad)
        d.text((14, y + cell[1] // 2 - 10), mname, font=F_S, fill=DIM)
        for i, t in enumerate(tiles):
            x = lab_w + i * (cell[0] + pad)
            img.paste(comp(t, bg, add, cell), (x, y))
    y = head + len(MODES) * (cell[1] + pad)
    for i, lab in enumerate(labels):
        x = lab_w + i * (cell[0] + pad)
        d.text((x + 4, y), lab, font=F_S, fill=DIM)
    return img


def seam_block(im):
    f63, f0, f62, f1 = frame(im, 8, 63), frame(im, 8, 0), frame(im, 8, 62), frame(im, 8, 1)
    pm = lambda t: t[..., :3] * t[..., 3:4]
    steps = [float(np.abs(pm(frame(im, 8, i + 1)) - pm(frame(im, 8, i))).mean()) for i in range(63)]
    seam = float(np.abs(pm(f0) - pm(f63)).mean())
    cell = (256, 256)
    w, h = 300 + 4 * (cell[0] + 8) + 8, 64 + cell[1] + 40
    img = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(img)
    d.text((14, 10), "CandleFlame loop seam", font=F_H, fill=INK)
    d.text((14, 44), f"mean |frame i+1 - frame i| = {np.mean(steps):.5f} (max {np.max(steps):.5f});  "
                     f"|frame 0 - frame 63| = {seam:.5f}  -> seamless", font=F_S, fill=DIM)
    tiles = [f62, f63, f0, f1]
    labs = ["frame 62", "frame 63", "frame 0 (loops)", "frame 1"]
    for i, t in enumerate(tiles):
        x = 300 + i * (cell[0] + 8)
        img.paste(comp(t, DARK, False, cell), (x, 64))
        d.text((x + 4, 64 + cell[1] + 6), labs[i], font=F_S, fill=DIM)
    d.text((14, 64 + cell[1] // 2 - 10), "over dark, 2x", font=F_S, fill=DIM)
    return img


def atlas_block(items):
    cell = 400
    w = 300 + len(items) * (cell + 8) + 8
    h = 64 + cell + 40
    img = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(img)
    d.text((14, 10), "Full atlases (row-major from the top-left)", font=F_H, fill=INK)
    d.text((14, 44), "over dark, scaled down", font=F_S, fill=DIM)
    for i, (name, lab) in enumerate(items):
        x = 300 + i * (cell + 8)
        img.paste(comp(load(name), DARK, False, (cell, cell)), (x, 64))
        d.text((x + 4, 64 + cell + 6), lab, font=F_S, fill=DIM)
    return img


def main():
    blocks = []
    candle = load("CandleFlame_8x8.png")
    fr = [0, 8, 16, 22, 23, 24, 25, 26, 32, 40, 48, 51, 56, 63]
    blocks.append(strip_block("CandleFlame_8x8.png  (1024, 8x8 x 128 px, Loop)",
                              "gentle sway (a bend travelling up the flame); strong flicker frames 22-26 (stretch + tip pinches off), "
                              "weak flicker ~frame 51", [frame(candle, 8, i) for i in fr], [f"f{i}" for i in fr], (176, 176)))
    blocks.append(seam_block(candle))
    tongue = load("FireTongue_8x8.png")
    fr = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60]
    blocks.append(strip_block("FireTongue_8x8.png  (1024, 8x8 x 128 px, OneShot)",
                              "born (f0-8) -> licks upward (f8-32) -> waist eaten through, top breaks away (f34-50) -> cools + burns out (f50-63)",
                              [frame(tongue, 8, i) for i in fr], [f"f{i}" for i in fr], (152, 152)))
    smoke = load("SmokeWisp_4x4.png")
    fr = list(range(0, 16, 2)) + [15]
    blocks.append(strip_block("SmokeWisp_4x4.png  (1024, 4x4 x 256 px, OneShot)",
                              "lit volumetric puff: rises, rolls/curls, thins into wisps and fades (lit from the upper left)",
                              [frame(smoke, 4, i) for i in fr], [f"f{i}" for i in fr], (200, 200)))
    singles = [load("Glow.png"), load("Ember.png"), load("Mist.png")]
    blocks.append(strip_block("Glow.png (256)   |   Ember.png (64, shown 4x)   |   Mist.png (512)",
                              "single images; all reach alpha 0 before the edge",
                              singles, ["Glow 256", "Ember 64", "Mist 512"], (256, 256)))
    blocks.append(atlas_block([("CandleFlame_8x8.png", "CandleFlame_8x8"), ("FireTongue_8x8.png", "FireTongue_8x8"),
                               ("SmokeWisp_4x4.png", "SmokeWisp_4x4")]))
    W = max(b.width for b in blocks)
    H = sum(b.height for b in blocks) + 70 + 10 * len(blocks)
    sheet = Image.new("RGB", (W, H), (20, 20, 24))
    d = ImageDraw.Draw(sheet)
    d.text((14, 16), "SLINGSHOT Halloween - VFX textures (rendered in Blender 5.2, Cycles + OSL)  -  straight alpha PNG",
           font=F_H, fill=INK)
    y = 70
    for b in blocks:
        sheet.paste(b, (0, y))
        y += b.height + 10
    sheet.save(OUT)
    print(OUT, sheet.size)


if __name__ == "__main__":
    main()
