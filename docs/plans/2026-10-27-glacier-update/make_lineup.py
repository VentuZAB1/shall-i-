"""Owner lineup of the 12 new pets (Glacier update, 2026-10-27): the three-quarter model render of each pet on a card
with its name, tier and odds, the Glacier six on top and the +1 pets below (each next to two of its egg siblings
for scale). Run: python make_lineup.py [tag]  -> LINEUP_<tag>.png
"""
import glob, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "PetsV3")
OUT = os.path.dirname(os.path.abspath(__file__))
BLACK = sorted(glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions\*\content\fonts\Montserrat-Black.ttf")))
BLACK = BLACK[-1] if BLACK else r"C:\Windows\Fonts\arialbd.ttf"
BODY_B = r"C:\Windows\Fonts\segoeuib.ttf"

GLACIER = [("FrostfangLynx", "Frostfang Lynx", "50%"), ("IceMammoth", "Ice Mammoth", "26%"),
           ("GlacierYeti", "Glacier Yeti", "14%"), ("BlizzardRoc", "Blizzard Roc", "7.4%"),
           ("PermafrostTitan", "Permafrost Titan", "2.5% SECRET"), ("FrostcrownDragon", "Frostcrown Dragon", "0.1% MYTHIC")]
PLUS1 = [("BrambleBadger", "Bramble Badger", "Grass 40%", ["MossbackTortoise", "ForestStag"]),
         ("CoralCrusher", "Coral Crusher", "Water 15%", ["Kappa", "Kraken"]),
         ("VoltRhino", "Volt Rhino", "Thunder 6%", ["Raiju", "Thunderbird"]),
         ("CinderOverlord", "Cinder Overlord", "Fire 0.5%", ["InfernoPhoenix", "Ivonrath"]),
         ("WraithHound", "Wraith Hound", "Shadow 10%", ["ShadePanther", "BlackDragon"]),
         ("EclipseSeraph", "Eclipse Seraph", "Celestial 0.1% MYTHIC", ["SolarLion", "CosmicLeviathan"])]


SHORT = {"MossbackTortoise": "Tortoise", "ForestStag": "Stag", "InfernoPhoenix": "Phoenix", "ShadePanther": "Panther",
         "BlackDragon": "Black Dragon", "SolarLion": "Solar Lion", "CosmicLeviathan": "Leviathan"}


def pic(name, size):
    for p in (os.path.join(ROOT, "_LU_" + name, "_LU_" + name + "_icon.png"), os.path.join(ROOT, name, name + "_icon.png"), os.path.join(ROOT, name, "renders", "model_tq.png"),
              os.path.join(ROOT, name, name + "_portrait_raw.png")):
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA")
            im.thumbnail((size, size), Image.LANCZOS)
            return im
    return None


def card(img, x, y, w, h, name, label, odds, new=True):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((x, y, x + w, y + h), 12, fill=(30, 46, 56) if new else (24, 32, 40),
                        outline=(255, 214, 90) if new else (12, 18, 22), width=4 if new else 2)
    im = pic(name, min(w, h - 60) - 16)
    if im:
        img.alpha_composite(im, (int(x + (w - im.width) / 2), int(y + 8 + (h - 60 - im.height) / 2)))
    else:
        d.text((x + w / 2, y + (h - 60) / 2), "not built yet", font=ImageFont.truetype(BODY_B, 20),
               fill=(160, 170, 180), anchor="mm")
    d.text((x + w / 2, y + h - 44), label.upper(), font=ImageFont.truetype(BLACK, 22 if new else 16),
           fill=(255, 255, 255), anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    if odds:
        d.text((x + w / 2, y + h - 18), odds, font=ImageFont.truetype(BODY_B, 18), fill=(255, 214, 90), anchor="mm")


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "round2"
    W, cw, ch = 1980, 320, 340
    H = 90 + ch + 60 + 2 * (ch + 50) + 30
    img = Image.new("RGBA", (W, H), (59, 88, 102, 255))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 45), "GLACIER UPDATE: NEW PETS (" + tag.upper() + ")", font=ImageFont.truetype(BLACK, 40),
           fill=(255, 255, 255), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    x0 = (W - 6 * cw - 5 * 10) / 2
    for i, (n, lab, odds) in enumerate(GLACIER):
        card(img, x0 + i * (cw + 10), 90, cw, ch, n, lab, odds)
    y = 90 + ch + 50
    d.text((40, y - 30), "+1 NEW PET PER EGG (gold frame), next to two pets of the same egg",
           font=ImageFont.truetype(BLACK, 22), fill=(255, 225, 140), stroke_width=2, stroke_fill=(0, 0, 0))
    gw, sw = 290, 150
    for i, (n, lab, odds, sib) in enumerate(PLUS1):
        col, row = i % 3, i // 3
        gx = 30 + col * (gw + 2 * (sw + 6) + 34)
        gy = y + row * (ch + 50)
        card(img, gx, gy, gw, ch, n, lab, odds)
        for j, s in enumerate(sib):
            card(img, gx + gw + 6 + j * (sw + 6), gy + ch - 220, sw, 220, s, SHORT.get(s, s), "", new=False)
    out = os.path.join(OUT, "LINEUP_%s.png" % tag)
    img.convert("RGB").save(out)
    print("saved", out, img.size)


if __name__ == "__main__":
    main()
