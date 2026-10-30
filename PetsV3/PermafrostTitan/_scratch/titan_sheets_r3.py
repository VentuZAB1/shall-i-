# python PermafrostTitan/_scratch/titan_sheets_r3.py -> round-3 sheets, each with a title bar "<name> - rendered <time>"
import os, time
from PIL import Image, ImageDraw
d = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan\renders"
STAMP = time.strftime("%Y-%m-%d %H:%M")


def lab(im, t):
    ImageDraw.Draw(im).text((6, 4), t, fill=(200, 0, 0))
    return im


def titled(img, name):
    bar = 22
    out = Image.new("RGB", (img.width, img.height + bar), (24, 26, 32))
    out.paste(img, (0, bar))
    ImageDraw.Draw(out).text((8, 5), "Permafrost Titan  %s  -  rendered %s (final 8.5 round 8)" % (name, STAMP),
                             fill=(255, 255, 255))
    out.save(os.path.join(d, name))
    return name


def grid(files_labels, cols, size=None):
    ims = []
    for fn, t in files_labels:
        im = Image.open(os.path.join(d, fn)).convert("RGB")
        if size:
            im = im.resize((size, size))
        ims.append(lab(im, t))
    W, H = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (cols * W, rows * H))
    for i, im in enumerate(ims):
        S.paste(im, ((i % cols) * W, (i // cols) * H))
    return S


made = []
# kneel f40 / f50 from the tq and game cameras at 2x (700 px renders)
made.append(titled(grid([("hx_%s_act_kneelrise_%02d.png" % (v, f), "%s f%d" % (v, f)) for f in (40, 50) for v in ("tq", "game")], 2),
                    "_kneel_2x_f40_f50.png"))
# idle beats at 2x
made.append(titled(grid([("b2_tq_idle_%02d.png" % f, "idle f%d" % f) for f in (0, 30, 60, 90)], 4), "_beats2x_idle.png"))
made.append(titled(grid([("b2_tq_roar_%02d.png" % f, "roar f%d" % f) for f in (0, 10, 22, 27, 50, 66)], 3), "_beats2x_roar.png"))
made.append(titled(grid([("b2_tq_act_kneelrise_%02d.png" % f, "kneel f%d" % f) for f in (0, 9, 18, 20, 40, 50, 58, 70, 84)], 3),
                    "_beats2x_kneel.png"))
# walk sheet (tq + game + side, one cycle)
made.append(titled(grid([("wk_%s_walk_%02d.png" % (v, f), "walk %s f%d" % (v, f)) for v in ("tq", "game", "side") for f in (0, 6, 12, 18, 24, 30, 36, 42)], 8),
                    "_walk_sheet.png"))
# roar jaw close-up (front + 3/4 at rest and at the f27 peak)
made.append(titled(grid([("pclose_%s_roar_%02d.png" % (v, f), "roar %s f%d" % (v, f)) for v in ("front", "tq") for f in (0, 27)], 4),
                    "_roar_jaw_close.png"))
# kneel views (front / tq / back / game at f18 / f40 / f58)
made.append(titled(grid([("kv_%s_act_kneelrise_%02d.png" % (v, f), "%s f%d" % (v, f)) for f in (18, 40, 58) for v in ("front", "tq", "back", "game")], 4),
                    "_kneel_views.png"))
# model sheet re-titled
ms = Image.open(os.path.join(d, "_model_sheet.png")).convert("RGB")
if ms.height % 2 == 0:                       # not yet titled (the sheet3 output is square)
    made.append(titled(ms, "_model_sheet.png"))
print("sheets", STAMP, made)
