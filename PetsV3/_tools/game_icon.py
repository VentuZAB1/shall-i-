# python _tools/game_icon.py <Name> <CmpA,CmpB,...>
# After headless_pack + pack_post (<Name>_icon.png) and game_raw.py (<Name>_game_raw.png): builds an icon3-style
# game-camera icon (<Name>_icon_game.png), a 64/128 strip [portrait icon, game-cam icon, comparisons...]
# (renders/_icons2_strip_64.png / _128.png) and counts GOLD pixels on both 64 px icons (HSV hue 0.08-0.16, s > 0.5,
# v > 0.45: lit + shaded gold). Prints JSON. (Recipe from the Weaver plan reviewer's icons.py.)
import sys, os, json
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


def gold_px(im):
    import colorsys
    sm = im.resize((64, 64), Image.LANCZOS)
    n = 0
    for r, g, b, a in (sm.get_flattened_data() if hasattr(sm, "get_flattened_data") else sm.getdata()):
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if a > 128 and 0.08 <= h <= 0.16 and s > 0.5 and v > 0.45:
            n += 1
    return n


me = Image.open(os.path.join(d, name + "_icon.png")).convert("RGBA")
gm = icon(os.path.join(d, name + "_game_raw.png"))
gm.save(os.path.join(d, name + "_icon_game.png"))
def gold_px_brief(im):
    """the Weaver brief's counter: hue 0.09-0.17, s > .45, v > .55"""
    import colorsys
    sm = im.resize((64, 64), Image.LANCZOS)
    n = 0
    for r, g, b, a in (sm.get_flattened_data() if hasattr(sm, "get_flattened_data") else sm.getdata()):
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if a > 128 and 0.09 <= h <= 0.17 and s > 0.45 and v > 0.55:
            n += 1
    return n


out = {"gold_px_portrait_64": gold_px(me), "gold_px_game_64": gold_px(gm),
       "gold_px_brief_counter": [gold_px_brief(me), gold_px_brief(gm)]}
for px in (64, 128):
    ims = []
    for im in [me, gm] + [Image.open(os.path.join(ROOT, n, n + "_icon.png")).convert("RGBA") for n in cmps
                          if os.path.exists(os.path.join(ROOT, n, n + "_icon.png"))]:
        im = im.resize((px, px), Image.LANCZOS)
        bg = Image.new("RGBA", (px, px), (52, 62, 74, 255))
        bg.alpha_composite(im)
        ims.append(bg.convert("RGB"))
    strip = Image.new("RGB", (len(ims) * (px + 6) + 6, px + 12), (24, 28, 34))
    for i, im in enumerate(ims):
        strip.paste(im, (6 + i * (px + 6), 6))
    sp = os.path.join(d, "renders", "_icons2_strip_%d.png" % px)
    strip.save(sp)
    out["strip_%d" % px] = sp
print(json.dumps(out))
