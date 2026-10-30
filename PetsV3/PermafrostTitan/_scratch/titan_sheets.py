# python PermafrostTitan/_scratch/titan_sheets.py -> renders/_kneel_views.png (kv_*), _beats2x_roar/kneel/idle.png (b2_*),
# _kneel_close_f40.png (hx_* + pclose_* posed close-ups at f40)
import os
from PIL import Image, ImageDraw
d = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan\renders"


def lab(im, t):
    ImageDraw.Draw(im).text((6, 4), t, fill=(200, 0, 0))
    return im


views, frames, w = ("front", "tq", "back", "game"), (18, 40, 58), 420
S = Image.new("RGB", (len(views) * w, len(frames) * w))
for r, f in enumerate(frames):
    for c, v in enumerate(views):
        S.paste(lab(Image.open(os.path.join(d, "kv_%s_act_kneelrise_%02d.png" % (v, f))).convert("RGB"), "%s f%d" % (v, f)),
                (c * w, r * w))
S.save(os.path.join(d, "_kneel_views.png"))
for name, picks, cols in (("_beats2x_roar.png", [("roar", f) for f in (0, 10, 22, 27, 50, 66)], 3),
                          ("_beats2x_kneel.png", [("act_kneelrise", f) for f in (0, 9, 18, 20, 40, 58, 70, 84)], 4),
                          ("_beats2x_idle.png", [("idle", f) for f in (0, 30, 60, 90)], 4)):
    ims = [lab(Image.open(os.path.join(d, "b2_tq_%s_%02d.png" % (c, f))).convert("RGB"), "%s f%d" % (c, f)) for c, f in picks]
    W, H = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (cols * W, rows * H))
    for i, im in enumerate(ims):
        S.paste(im, ((i % cols) * W, (i // cols) * H))
    S.save(os.path.join(d, name))
ims = [lab(Image.open(os.path.join(d, fn)).convert("RGB").resize((560, 560)), t) for fn, t in (
    ("hx_tq_act_kneelrise_40.png", "tq f40 (fixed cam)"), ("hx_game_act_kneelrise_40.png", "game f40 (fixed cam)"),
    ("pclose_tq_act_kneelrise_40.png", "tq f40 close (Knee_L)"), ("pclose_game_act_kneelrise_40.png", "game f40 close (Knee_L)"))]
S = Image.new("RGB", (2 * 560, 2 * 560))
for i, im in enumerate(ims):
    S.paste(im, ((i % 2) * 560, (i // 2) * 560))
S.save(os.path.join(d, "_kneel_close_f40.png"))
print("sheets ok")
