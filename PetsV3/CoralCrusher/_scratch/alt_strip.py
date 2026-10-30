# python CoralCrusher/_scratch/alt_strip.py <Name> <CmpA,CmpB,...>
# icon3-style icon from <Name>_portrait_alt_raw.png (same recipe as _tools/game_icon.py) -> <Name>_icon_alt.png and
# the strips renders/_icons3_strip_64/128.png = [kit portrait icon, ALT portrait icon, game-cam icon, comparisons]
import sys, os
from PIL import Image, ImageFilter
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
name = sys.argv[1]
cmps = [c for c in sys.argv[2].split(",") if c] if len(sys.argv) > 2 else []
d = os.path.join(ROOT, name)


def icon(raw):
    im = Image.open(raw).convert("RGBA")
    bb = im.split()[3].point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop(bb)
    w, h = im.size
    side = int(max(w, h) * 1.16)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(im, ((side - w) // 2, (side - h) // 2))
    sq = sq.resize((512, 512), Image.LANCZOS)
    alpha = sq.split()[3].point(lambda v: 255 if v > 40 else 0)
    ring = alpha.filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.GaussianBlur(1.2))
    out = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    out.paste(Image.new("RGBA", (512, 512), (12, 12, 16, 255)), (0, 0), ring)
    out.alpha_composite(sq)
    return out


alt = icon(os.path.join(d, name + "_portrait_alt_raw.png"))
alt.save(os.path.join(d, name + "_icon_alt.png"))
srcs = [os.path.join(d, name + "_icon.png"), os.path.join(d, name + "_icon_alt.png"),
        os.path.join(d, name + "_icon_game.png")] + [os.path.join(ROOT, n, n + "_icon.png") for n in cmps]
for px in (64, 128):
    ims = []
    for p in srcs:
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGBA").resize((px, px), Image.LANCZOS)
        bg = Image.new("RGBA", (px, px), (52, 62, 74, 255))
        bg.alpha_composite(im)
        ims.append(bg.convert("RGB"))
    strip = Image.new("RGB", (len(ims) * (px + 6) + 6, px + 12), (24, 28, 34))
    for i, im in enumerate(ims):
        strip.paste(im, (6 + i * (px + 6), 6))
    strip.save(os.path.join(d, "renders", "_icons3_strip_%d.png" % px))
print("ok")
