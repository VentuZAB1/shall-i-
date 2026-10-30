# python sheet3.py <Name> <glob-prefix> [cols]  -> <Name>/renders/_<prefix>_sheet.png (review contact sheet)
import sys, glob, os
from PIL import Image

name, pre = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 2
here = os.path.dirname(os.path.abspath(__file__))
fs = sorted(glob.glob(os.path.join(here, name, "renders", pre + "*.png")))
fs = [f for f in fs if not os.path.basename(f).startswith("_") and "sheet" not in os.path.basename(f)]
ims = [Image.open(f).convert("RGB") for f in fs]
w, h = ims[0].size
rows = (len(ims) + cols - 1) // cols
s = Image.new("RGB", (cols * w, rows * h), "white")
for i, im in enumerate(ims):
    s.paste(im, ((i % cols) * w, (i // cols) * h))
s.thumbnail((1800, 1800))
out = os.path.join(here, name, "renders", "_" + pre.strip("_*") + "_sheet.png")
s.save(out)
print(out, s.size, [os.path.basename(f) for f in fs])
