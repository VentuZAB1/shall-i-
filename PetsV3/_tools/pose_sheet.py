# python _tools/pose_sheet.py <Name> <view> <out_name> act:frame,act:frame,... [cols]
import sys, os
from PIL import Image, ImageDraw
name, view, outn, picks = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split(",")
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 4
d = os.path.join(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3", name, "renders")
ims = []
for p in picks:
    a, f = p.rsplit(":", 1)
    im = Image.open(os.path.join(d, "pose_%s_%s_%02d.png" % (view, a, int(f)))).convert("RGB")
    ImageDraw.Draw(im).text((6, 4), "%s f%s" % (a, f), fill=(255, 255, 0))
    ims.append(im)
w, h = ims[0].size
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h), (30, 30, 30))
for i, im in enumerate(ims):
    sheet.paste(im, ((i % cols) * w, (i // cols) * h))
out = os.path.join(d, outn)
sheet.save(out)
print(out, sheet.size)
