# python CoralCrusher/_scratch/walk_strip.py -> renders/_walk_strip_game.png / _walk_strip_tq.png
# (wk6_<view>_walk_<f>.png from clip_views, 390 px, fixed camera) in one titled row each + a x2 eye-level crop row of
# the game view f0 / f3 / f6 / f9 with the f0 outline in red (motion check)
import os, time, glob, re
from PIL import Image, ImageDraw, ImageChops, ImageFilter
R = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher\renders"
for view in ("game", "tq"):
    fs = sorted(glob.glob(os.path.join(R, "wk6_%s_walk_*.png" % view)), key=lambda p: int(re.findall(r"_(\d+)\.png$", p)[0]))
    t = time.strftime("%Y-%m-%d %H:%M", time.localtime(max(os.path.getmtime(p) for p in fs)))
    ims = [Image.open(p).convert("RGB") for p in fs]
    W, H = ims[0].size
    o = Image.new("RGB", (W * len(ims), H + 22), (24, 26, 34))
    d = ImageDraw.Draw(o)
    d.text((6, 5), "Coral Crusher _walk_strip_%s.png - rendered %s (lift 0.10, bob 0.016, roll 2.4, pitch 1.5; 390 px)" % (view, t),
           fill=(235, 235, 235))
    for i, (p, im) in enumerate(zip(fs, ims)):
        f = int(re.findall(r"_(\d+)\.png$", p)[0])
        ImageDraw.Draw(im).text((5, 4), "walk %s f%d" % (view, f), fill=(200, 0, 0))
        o.paste(im, (i * W, 22))
    o.save(os.path.join(R, "_walk_strip_%s.png" % view))
    print(view, t, len(ims))
