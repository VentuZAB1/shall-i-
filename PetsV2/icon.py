# python icon.py <Pet>  -> crops <Pet>_portrait_raw.png to its alpha bounds, pads to a square, writes <Pet>_icon.png (512)
import sys, os
from PIL import Image
name = sys.argv[1]
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
im = Image.open(os.path.join(d, name + "_portrait_raw.png")).convert("RGBA")
a = im.split()[3].point(lambda v: 255 if v > 8 else 0)
x0, y0, x1, y1 = a.getbbox()
w, h = x1 - x0, y1 - y0
side = int(max(w, h) * 1.08)
out = Image.new("RGBA", (side, side), (0, 0, 0, 0))
out.paste(im.crop((x0, y0, x1, y1)), ((side - w) // 2, (side - h) // 2))
out = out.resize((512, 512), Image.LANCZOS)
p = os.path.join(d, name + "_icon.png")
out.save(p)
print(p, (w, h))
