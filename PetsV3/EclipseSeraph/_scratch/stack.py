# python EclipseSeraph/_scratch/stack.py <out.png> <sheet.png> [...] : stack contact sheets vertically (scaled to one width)
import sys
from PIL import Image
ims = [Image.open(p).convert("RGB") for p in sys.argv[2:]]
w = max(i.width for i in ims)
ims = [i if i.width == w else i.resize((w, int(i.height * w / i.width))) for i in ims]
out = Image.new("RGB", (w, sum(i.height for i in ims)), "white")
y = 0
for i in ims:
    out.paste(i, (0, y))
    y += i.height
out.save(sys.argv[1])
print(sys.argv[1], out.size)
