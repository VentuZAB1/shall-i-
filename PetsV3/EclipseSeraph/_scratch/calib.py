# builder D scratch: candidate versions of the reviewer's 64 px icon measure (strip cell vs background, outline in/out)
import sys, colorsys
from PIL import Image
for path in sys.argv[1:]:
    im = Image.open(path).convert("RGBA").resize((64, 64), Image.LANCZOS)
    bg = Image.new("RGBA", (64, 64), (52, 62, 74, 255))
    bg.alpha_composite(im)
    px = list(bg.convert("RGB").getdata())
    pet = [p for p in px if abs(p[0] - 52) + abs(p[1] - 62) + abs(p[2] - 74) > 12]
    for lab, sel in (("all", pet), ("no-outline(lum>=30)", [p for p in pet if 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2] >= 30])):
        L = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b in sel]
        S = [colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[1] for r, g, b in sel]
        t = len(sel)
        print("%s %s: px %d white %.1f%% sat %.2f dark90 %.1f%%" % (path.split("/")[-1], lab, t, 100.0 * sum(l > 200 for l in L) / t,
              sum(S) / t, 100.0 * sum(l < 90 for l in L) / t))
