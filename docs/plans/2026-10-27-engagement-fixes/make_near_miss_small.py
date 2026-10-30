"""SMALL near-miss text MOCKUP (2026-10-27): the owner said the first banner was too big ("maybe like a small text or
do not add it"). Same backdrop and area strip as make_near_miss_mockup.py; the line is now small HUD-sized text
(about the size of the "Friend Boost: +0%" label), mixed case, thin outline, just under the area strip.
Run: python make_near_miss_small.py
"""
import os
from PIL import Image
import make_near_miss_mockup as M

HERE = os.path.dirname(os.path.abspath(__file__))


def small(out_path, studs=12):
    img = Image.open(M.BACK).convert("RGBA").resize((M.W, M.H))
    sy, sh = round(0.0593 * M.H), round(0.1111 * M.H)
    M.strip(img, sy, sh)
    M.area_title(img, "Grass", "\U0001F33F", M.GRASS, sy, sh)
    size = round(16 * M.DEVICE)               # 16 px design size (the old banner was 34)
    M.rich_text(img, M.W / 2, sy + sh + round(16 * M.DEVICE), [
        ("Water", M.WATER), (" is only ", (255, 255, 255)), (f"{studs} studs", M.AMBER), (" away!", (255, 255, 255)),
    ], size, max(2, round(2 * M.DEVICE)))
    img.convert("RGB").save(out_path, quality=95)
    return img


if __name__ == "__main__":
    a = small(os.path.join(HERE, "near_miss_small_mockup.png"))
    z = a.crop((int(M.W * 0.25), 30, int(M.W * 0.75), 190)).resize((int(M.W * 0.5 * 2), 320), Image.LANCZOS)
    z.convert("RGB").save(os.path.join(HERE, "near_miss_small_zoom.png"))
    print("ok, device scale", round(M.DEVICE, 3))
