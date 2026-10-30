from PIL import Image
import os
root = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\WraithHound\renders"
for v in ("side", "tq", "game"):
    im = Image.open(os.path.join(root, "flat_%s.png" % v)).convert("RGB")
    tot = mag = 0
    for c, rgb in im.getcolors(1 << 24):
        if max(rgb) < 6:
            continue
        tot += c
        if rgb[0] > 200 and rgb[1] < 60 and rgb[2] > 200:
            mag += c
    print(v, "saddle %.1f %%" % (100.0 * mag / tot))
