# python CoralCrusher/_scratch/wave_strip.py -> renders/_wave_strip.png (tq rows then game rows, every 2 f f18-78)
import os
from PIL import Image, ImageDraw
d = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher\renders"
frames = list(range(18, 83, 2))
peaks = {26: "top", 28: "top", 30: "HOLD wave1", 32: "top", 34: "top", 49: "top", 50: "top", 52: "top", 53: "HOLD wave2", 54: "top", 56: "top", 72: "top", 74: "top", 76: "HOLD wave3", 78: "top", 80: "top", 38: "trough", 40: "trough", 62: "trough"}
cols = 17
blocks = []
for v in ("tq", "game"):
    ims = []
    for f in frames:
        im = Image.open(os.path.join(d, "wv_%s_act_semaphore_%02d.png" % (v, f))).convert("RGB")
        dr = ImageDraw.Draw(im)
        dr.text((5, 4), "%s f%d" % (v, f), fill=(200, 0, 0))
        if f in peaks:
            dr.text((5, 16), peaks[f], fill=(0, 90, 200))
        ims.append(im)
    blocks.append(ims)
w, h = blocks[0][0].size
rows = (len(frames) + cols - 1) // cols
S = Image.new("RGB", (cols * w, 2 * rows * h + 10), (30, 30, 30))
for b, ims in enumerate(blocks):
    for i, im in enumerate(ims):
        S.paste(im, ((i % cols) * w, b * (rows * h + 10) + (i // cols) * h))
S.save(os.path.join(d, "_wave_strip.png"))
print(S.size)
