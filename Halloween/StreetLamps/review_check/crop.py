import sys
from PIL import Image
# crop.py src out x0 y0 x1 y1 scale
src, out, x0, y0, x1, y1, s = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7]), float(sys.argv[7])
im = Image.open(src).crop((x0, y0, x1, y1))
im = im.resize((int(im.width * s), int(im.height * s)), Image.NEAREST)
im.save(out)
