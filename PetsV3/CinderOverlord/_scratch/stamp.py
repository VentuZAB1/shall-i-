# python CinderOverlord/_scratch/stamp.py <PetFolder> "<label>" file1.png [file2.png ...]
# adds a dark title bar "<Pet>  <file>  -  rendered <time>  <label>" on top of each render (in place; skips stamped files)
import sys, os, time
from PIL import Image, ImageDraw
pet, label, files = sys.argv[1], sys.argv[2], sys.argv[3:]
d = os.path.join(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3", pet, "renders")
stamp = time.strftime("%Y-%m-%d %H:%M", time.localtime())
for fn in files:
    p = os.path.join(d, fn)
    im = Image.open(p)
    if im.info.get("stamped"):
        continue
    mode = "RGBA" if im.mode == "RGBA" else "RGB"
    im = im.convert(mode)
    bar = 22
    out = Image.new(mode, (im.width, im.height + bar), (24, 26, 32, 255) if mode == "RGBA" else (24, 26, 32))
    out.paste(im, (0, bar))
    ImageDraw.Draw(out).text((8, 5), "%s  %s  -  rendered %s (file time %s)  %s" % (
        pet, fn, stamp, time.strftime("%H:%M", time.localtime(os.path.getmtime(p))), label), fill=(255, 255, 255))
    from PIL import PngImagePlugin
    meta = PngImagePlugin.PngInfo()
    meta.add_text("stamped", stamp)
    out.save(p, pnginfo=meta)
print("stamped", stamp, files)
