# python BlizzardRoc/_scratch/clip_sheet.py <Name> <view> <clip> [cols] : pose_<view>_<clip>_<f>.png sorted by frame,
# labelled with the frame + time (30 fps) and a footer with the render timestamp -> renders/_pose_<view>_<clip>_sheet.png
import sys, glob, os, re, time
from PIL import Image, ImageDraw
name, view, clip = sys.argv[1], sys.argv[2], sys.argv[3]
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 5
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
fs = glob.glob(os.path.join(here, name, "renders", "pose_%s_%s_*.png" % (view, clip)))
fs = [f for f in fs if re.match(r".*_(\d+)\.png$", f)]
fs.sort(key=lambda f: int(re.match(r".*_(\d+)\.png$", f).group(1)))
ims = [Image.open(f).convert("RGB") for f in fs]
w, h = ims[0].size
rows = (len(ims) + cols - 1) // cols
s = Image.new("RGB", (cols * w, rows * h + 18), "white")
d = ImageDraw.Draw(s)
for i, (f, im) in enumerate(zip(fs, ims)):
    x, y = (i % cols) * w, (i // cols) * h
    s.paste(im, (x, y))
    fr = int(re.match(r".*_(\d+)\.png$", f).group(1))
    d.rectangle((x, y, x + 150, y + 18), fill=(255, 230, 0))
    d.text((x + 4, y + 3), "%s f%d  %.2f s" % (clip, fr, fr / 30.0), fill=(0, 0, 0))
t = time.strftime("%Y-%m-%d %H:%M", time.localtime(max(os.path.getmtime(f) for f in fs)))
d.text((4, rows * h + 3), "%s  %s view  rendered %s (30 fps)" % (name, view, t), fill=(0, 0, 0))
out = os.path.join(here, name, "renders", "_pose_%s_%s_sheet.png" % (view, clip))
s.save(out)
print(out, s.size, len(ims))
