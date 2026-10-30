# python beats_sheet.py <manifest json> [title]  -> one labelled sheet per view next to the manifest
# A title bar carries the pet, the view, the render time (newest frame file) and the pet file's time, so a reviewer can
# see the sheet is newer than the final file.
import sys, json, os, time
from PIL import Image, ImageDraw
m = json.load(open(sys.argv[1]))
title = sys.argv[2] if len(sys.argv) > 2 else ""
res = m["res"]
name = os.path.basename(os.path.dirname(os.path.dirname(sys.argv[1])))
spec = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[1]))), "pets", name + ".py")
stamp = lambda p: time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(p)))
for v, files in m["files"].items():
    ims = [Image.open(f).convert("RGB") for f in files]
    cols = min(4, len(ims))
    rows = (len(ims) + cols - 1) // cols
    TB = 26
    sheet = Image.new("RGB", (cols * res, rows * res + TB), "white")
    d = ImageDraw.Draw(sheet)
    d.rectangle([0, 0, cols * res, TB], fill=(20, 24, 30))
    newest = max(files, key=os.path.getmtime)
    d.text((8, 7), "%s  %s  view %s  | rendered %s  | pets/%s.py %s" % (name, title, v, stamp(newest), name,
                                                                          stamp(spec) if os.path.exists(spec) else "?"),
           fill=(255, 255, 255))
    for i, (im, (c, f)) in enumerate(zip(ims, m["picks"])):
        x, y = (i % cols) * res, (i // cols) * res + TB
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 140, y + 20], fill=(0, 0, 0))
        d.text((x + 6, y + 4), "%s f%d" % (c, f), fill=(255, 255, 255))
    out = sys.argv[1].replace(".json", "_%s.png" % v)
    sheet.save(out)
    print(out, sheet.size)
