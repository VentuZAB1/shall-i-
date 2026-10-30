# python icon3.py Name [Name...] -> <Name>/<Name>_icon.png : square 512 portrait, transparent, thick black outline
# (Steal-an-Egg style pet cards), from <Name>/<Name>_portrait_raw.png
import sys, os
from PIL import Image, ImageFilter
here = os.path.dirname(os.path.abspath(__file__))
for n in sys.argv[1:]:
    im = Image.open(os.path.join(here, n, n + "_portrait_raw.png")).convert("RGBA")
    a = im.split()[3]
    bb = a.point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop(bb)
    w, h = im.size
    side = int(max(w, h) * 1.16)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(im, ((side - w) // 2, (side - h) // 2))
    sq = sq.resize((512, 512), Image.LANCZOS)
    alpha = sq.split()[3].point(lambda v: 255 if v > 40 else 0)
    ring = alpha.filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.GaussianBlur(1.2))
    out = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    black = Image.new("RGBA", (512, 512), (12, 12, 16, 255))
    out.paste(black, (0, 0), ring)
    out.alpha_composite(sq)
    p = os.path.join(here, n, n + "_icon.png")
    out.save(p)
    print(p)
