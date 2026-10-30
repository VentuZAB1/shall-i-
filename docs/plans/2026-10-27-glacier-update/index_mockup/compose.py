"""Index mockup (Glacier update): Studio capture of the live Index re-laid out client-side (7 tabs, 2 rows of 3 cards,
MYTHIC badge) + the new pets' portraits pasted into the card/inspect view rects (they are not uploaded yet).
Run: python compose.py <capture.jpg> <out.png>"""
import os, sys
from PIL import Image

PETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "PetsV3")
NAMES = ["FrostfangLynx", "IceMammoth", "GlacierYeti", "BlizzardRoc", "PermafrostTitan", "FrostcrownDragon"]
# view rects from the client (x, y incl. the 58 px top inset, w, h)
RECTS = [(148, 299, 103, 52), (265, 299, 103, 52), (382, 299, 103, 52), (148, 405, 103, 52), (265, 405, 103, 52),
         (380, 404, 107, 54)]
INSP = (504, 234, 185, 166)
WIN = (14, 114, 714, 502)


def portrait(name):
    im = Image.open(os.path.join(PETS, name, name + "_portrait_raw.png")).convert("RGBA")
    x0, y0, x1, y1 = im.getbbox()
    return im.crop((max(0, x0 - 4), max(0, y0 - 4), min(512, x1 + 4), min(512, y1 + 4)))


def paste_fit(base, im, rect, grow=1.0):
    x, y, w, h = rect
    W, H = w * grow, h * grow
    s = min(W / im.width, H / im.height)
    p = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    base.alpha_composite(p, (int(x + w / 2 - p.width / 2), int(y + h / 2 - p.height / 2)))


def main(src, out, scale=2):
    base = Image.open(src).convert("RGBA")
    for n, r in zip(NAMES, RECTS):
        paste_fit(base, portrait(n), r, 1.0)
    paste_fit(base, portrait(NAMES[-1]), INSP, 0.95)
    x, y, w, h = WIN
    crop = base.crop((x - 6, y - 6, x + w + 6, y + h + 6))
    crop = crop.resize((crop.width * scale, crop.height * scale), Image.LANCZOS)
    crop.convert("RGB").save(out)
    print("saved", out, crop.size)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
