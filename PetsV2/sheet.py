"""python sheet.py <out.png> <cell> <cols> img1 img2 ...  -> contact sheet with file-stem labels"""
import sys, os
from PIL import Image, ImageDraw
out, cell, cols = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
files = sys.argv[4:]
rows = (len(files) + cols - 1) // cols
im = Image.new("RGB", (cols * cell, rows * cell), "white")
d = ImageDraw.Draw(im)
for i, f in enumerate(files):
    x, y = (i % cols) * cell, (i // cols) * cell
    im.paste(Image.open(f).convert("RGB").resize((cell, cell)), (x, y))
    d.text((x + 5, y + 4), os.path.splitext(os.path.basename(f))[0], fill=(0, 0, 0))
im.save(out)
print(out)
