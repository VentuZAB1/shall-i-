# python sheet.py <out.png> <title> <cols> <file> [file ...]   labelled sheet with a title bar (render + pet file time)
import sys, os, time
from PIL import Image, ImageDraw
out, title, cols, files = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4:]
st = lambda p: time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(p)))
ims = [Image.open(f).convert("RGB") for f in files]
w = max(i.width for i in ims); h = max(i.height for i in ims)
rows = (len(ims) + cols - 1) // cols
TB = 26
S = Image.new("RGB", (cols * w, rows * h + TB), (255, 255, 255))
d = ImageDraw.Draw(S)
d.rectangle([0, 0, cols * w, TB], fill=(20, 24, 30))
spec = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(files[0])))), "pets",
                    os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(files[0])))) + ".py")
d.text((8, 7), "%s | rendered %s | %s %s" % (title, st(max(files, key=os.path.getmtime)), os.path.basename(spec),
                                            st(spec) if os.path.exists(spec) else ""), fill=(255, 255, 255))
for i, (im, f) in enumerate(zip(ims, files)):
    x, y = (i % cols) * w, (i // cols) * h + TB
    S.paste(im, (x, y))
    d.rectangle([x, y, x + 150, y + 20], fill=(0, 0, 0))
    d.text((x + 6, y + 4), os.path.basename(f).replace(".png", ""), fill=(255, 255, 255))
S.save(out)
print(out, S.size)
