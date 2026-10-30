import sys, glob, os
from PIL import Image
d = sys.argv[1]
fs = sorted(glob.glob(os.path.join(d, "_scratch", "fr_*.png")))
ims = [Image.open(f) for f in fs]
w, h = ims[0].size
S = Image.new("RGB", (w * len(ims), h))
for i, im in enumerate(ims):
    S.paste(im, (i * w, 0))
S.save(os.path.join(d, "_scratch", "strip.png"))
