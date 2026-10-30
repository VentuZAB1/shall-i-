# python CinderOverlord/_scratch/hood_sheet.py -> renders/_hood_back_2x_idle_f0_f20.png (rows back / game, cols f0 / f20)
import os, time
from PIL import Image, ImageDraw
R = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord\renders"
fs = [(v, f) for v in ("back", "game") for f in (0, 20)]
paths = [os.path.join(R, "hood_%s_idle_%02d.png" % (v, f)) for v, f in fs]
t = time.strftime("%Y-%m-%d %H:%M", time.localtime(max(os.path.getmtime(p) for p in paths)))
S = 800
o = Image.new("RGB", (2 * S, 2 * S + 22), (24, 26, 34))
d = ImageDraw.Draw(o)
d.text((8, 5), "CinderOverlord _hood_back_2x_idle_f0_f20.png - rendered %s (fixed cameras; final 8.5 round 14)" % t,
       fill=(235, 235, 235))
for i, ((v, f), p) in enumerate(zip(fs, paths)):
    im = Image.open(p).convert("RGB").resize((S, S))
    ImageDraw.Draw(im).text((8, 8), "%s  idle f%d" % (v, f), fill=(200, 0, 0))
    o.paste(im, ((i % 2) * S, 22 + (i // 2) * S))
o.save(os.path.join(R, "_hood_back_2x_idle_f0_f20.png"))
for p in paths:
    os.remove(p)
print("hood sheet", t)
