# python PermafrostTitan/_scratch/cv_sheet.py <Name> <view> <clip:frame,...> <out.png> [cols] [prefix]
# labelled sheet of clip_views.py renders
import sys, os
from PIL import Image, ImageDraw
name, view, picks, outn = sys.argv[1], sys.argv[2], sys.argv[3].split(","), sys.argv[4]
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 5
prefix = sys.argv[6] if len(sys.argv) > 6 else "cv"
d = os.path.join(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3", name, "renders")
ims = []
for p in picks:
    c, f = p.rsplit(":", 1)
    im = Image.open(os.path.join(d, "%s_%s_%s_%02d.png" % (prefix, view, c, int(f)))).convert("RGB")
    ImageDraw.Draw(im).text((5, 4), "%s f%s" % (c, f), fill=(200, 0, 0))
    ims.append(im)
w, h = ims[0].size
rows = (len(ims) + cols - 1) // cols
S = Image.new("RGB", (cols * w, rows * h), (30, 30, 30))
for i, im in enumerate(ims):
    S.paste(im, ((i % cols) * w, (i // cols) * h))
S.save(os.path.join(d, outn))
print(os.path.join(d, outn), S.size)
