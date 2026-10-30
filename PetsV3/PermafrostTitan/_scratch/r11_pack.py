# python PermafrostTitan/_scratch/r10_pack.py -> the round-11 act evidence pack, each sheet with a title bar
# "Permafrost Titan <sheet> - rendered <time of the newest source render> (final 8.5 round 11)"
import os, time
from PIL import Image, ImageDraw
d = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan\renders"
r10 = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan\_scratch\r10"


def stamp(paths):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(max(os.path.getmtime(p) for p in paths)))


def lab(im, t):
    ImageDraw.Draw(im).text((6, 4), t, fill=(200, 0, 0))
    return im


def sheet(name, items, cols, size=None, root=d):
    paths = [os.path.join(root, fn) for fn, _ in items]
    ims = []
    for p, (_, t) in zip(paths, items):
        im = Image.open(p).convert("RGB")
        if size:
            im = im.resize((size, size), Image.LANCZOS)
        ims.append(lab(im, t))
    W, H = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    bar = 22
    out = Image.new("RGB", (cols * W, rows * H + bar), (24, 26, 32))
    for i, im in enumerate(ims):
        out.paste(im, ((i % cols) * W, bar + (i // cols) * H))
    ImageDraw.Draw(out).text((8, 5), "Permafrost Titan  %s  -  rendered %s (final 8.5 round 11)" % (name, stamp(paths)),
                             fill=(255, 255, 255))
    out.save(os.path.join(d, name))
    print(name, stamp(paths))


A = "act_kneelrise"
sheet("_kneel_2x_f30_f40_f50.png", [("hx_%s_%s_%02d.png" % (v, A, f), "%s f%d" % (v, f)) for v in ("game", "tq") for f in (30, 40, 50)], 3)
sheet("_kneel_2x_f40_f50.png", [("hx_%s_%s_%02d.png" % (v, A, f), "%s f%d" % (v, f)) for f in (40, 50) for v in ("tq", "game")], 2)
sheet("_kneel_3x_game_f30_f40_f50.png", [("r11_game3x_%02d.png" % f, "game 3x (lower body) f%d" % f) for f in (30, 40, 50)], 3, size=700, root=r10)
sheet("_kneel_close_f30_f40_f50.png", [("r11_%s_%02d.png" % (v, f), "%s (knee-aimed, half distance) f%d" % (v, f))
                                        for v in ("game2x", "tq2x") for f in (30, 40, 50)], 3, size=560, root=r10)
sheet("_beats2x_kneel.png", [("b2_tq_%s_%02d.png" % (A, f), "kneel f%d" % f) for f in (0, 9, 18, 20, 40, 50, 58, 70, 84)], 3)
sheet("_kneel_views.png", [("kv_%s_%s_%02d.png" % (v, A, f), "%s f%d" % (v, f)) for f in (18, 40, 58) for v in ("front", "tq", "back", "game")], 4)
sheet("_kneel_game_strip_f0_f64.png", [("gs_game_%s_%02d.png" % (A, f), "game f%d (%.2f s)" % (f, f / 30.0)) for f in range(0, 65, 4)], 9)
pt = os.path.join(d, "_pose_tq_sheet.png")
im = Image.open(pt).convert("RGB")
bar = 22
out = Image.new("RGB", (im.width, im.height + bar), (24, 26, 32))
out.paste(im, (0, bar))
ImageDraw.Draw(out).text((8, 5), "Permafrost Titan  _pose_tq_sheet.png (24 beats: idle / walk / roar / act)  -  rendered %s (final 8.5 round 11)"
                         % stamp([os.path.join(d, f) for f in os.listdir(d) if f.startswith("pose_tq_act_")]), fill=(255, 255, 255))
out.save(pt)
print("_pose_tq_sheet.png titled")
