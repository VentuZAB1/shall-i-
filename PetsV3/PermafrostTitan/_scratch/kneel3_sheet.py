# python PermafrostTitan/_scratch/kneel3_sheet.py -> renders/_kneel_2x_f30_f40_f50.png (rows game / tq, cols f30 / f40 / f50)
import os, time
from PIL import Image, ImageDraw
R = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan\renders"
fs = [(v, f) for v in ("game", "tq") for f in (30, 40, 50)]
paths = [os.path.join(R, "hx_%s_act_kneelrise_%d.png" % (v, f)) for v, f in fs]
t = time.strftime("%Y-%m-%d %H:%M", time.localtime(max(os.path.getmtime(p) for p in paths)))
S = 700
o = Image.new("RGB", (3 * S, 2 * S + 22), (24, 26, 34))
d = ImageDraw.Draw(o)
d.text((8, 5), "Permafrost Titan  _kneel_2x_f30_f40_f50.png  -  rendered %s (final 8.5 round 8)" % t, fill=(235, 235, 235))
for i, ((v, f), p) in enumerate(zip(fs, paths)):
    im = Image.open(p).convert("RGB").resize((S, S))
    ImageDraw.Draw(im).text((6, 6), "%s f%d" % (v, f), fill=(200, 0, 0))
    o.paste(im, ((i % 3) * S, 22 + (i // 3) * S))
o.save(os.path.join(R, "_kneel_2x_f30_f40_f50.png"))
print("kneel3", t)
