# python FrostcrownDragon/_scratch/goldcount.py <icon.png> [...] : (builder D scratch) gold px on a 64 px icon under
# several stated rules and resize filters, so the count can be reproduced
import sys, colorsys
from PIL import Image
RULES = {
    "hsv_tool (h .08-.16, s>.50, v>.45)": lambda r, g, b: (lambda h, s, v: .08 <= h <= .16 and s > .50 and v > .45)(*colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)),
    "hsv_brief (h .09-.17, s>.45, v>.55)": lambda r, g, b: (lambda h, s, v: .09 <= h <= .17 and s > .45 and v > .55)(*colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)),
    "hsv_strict (h .10-.15, s>.60, v>.70)": lambda r, g, b: (lambda h, s, v: .10 <= h <= .15 and s > .60 and v > .70)(*colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)),
    "rgb_strict (R>=200, G>=140, B<=110)": lambda r, g, b: r >= 200 and g >= 140 and b <= 110,
}
for f in sys.argv[1:]:
    im = Image.open(f).convert("RGBA")
    for fil, fn in (("LANCZOS", Image.LANCZOS), ("BOX", Image.BOX), ("NEAREST", Image.NEAREST)):
        sm = im.resize((64, 64), fn)
        px = [p for p in sm.getdata() if p[3] > 128]
        print(f.split("/")[-1], fil, {k: sum(1 for r, g, b, a in px if rule(r, g, b)) for k, rule in RULES.items()})
