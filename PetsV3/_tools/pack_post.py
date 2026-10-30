# python _tools/pack_post.py <Name> <CmpA,CmpB,...> [views=side,tq,game]
# After headless_pack.py: icon3 outline icon, the 64/128 icon strips next to the comparison pets
# (renders/_icons_strip_64.png / _128.png) and value shares per palette colour from the flat ID renders
# (palette = the pet module's module-level RGB tuples). Prints JSON.
import sys, os, json, re, subprocess
from PIL import Image
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
name = sys.argv[1]
cmps = [c for c in sys.argv[2].split(",") if c] if len(sys.argv) > 2 else []
opts = dict(a.split("=", 1) for a in sys.argv[3:] if "=" in a)
views = opts.get("views", "side,tq,game").split(",")
subprocess.run([sys.executable, os.path.join(ROOT, "icon3.py"), name], check=True, capture_output=True)
out = {}
for px in (64, 128):
    ims = []
    for n in [name] + cmps:
        p = os.path.join(ROOT, n, n + "_icon.png")
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA").resize((px, px), Image.LANCZOS)
            bg = Image.new("RGBA", (px, px), (52, 62, 74, 255))
            bg.alpha_composite(im)
            ims.append(bg.convert("RGB"))
    strip = Image.new("RGB", (len(ims) * (px + 6) + 6, px + 12), (24, 28, 34))
    for i, im in enumerate(ims):
        strip.paste(im, (6 + i * (px + 6), 6))
    sp = os.path.join(ROOT, name, "renders", "_icons_strip_%d.png" % px)
    strip.save(sp)
    out["strip_%d" % px] = sp
# palette from the module source: NAME = (r, g, b)
src = open(os.path.join(ROOT, "pets", name + ".py"), encoding="utf-8").read()
pal = {}
for m in re.finditer(r"^([A-Z][A-Z0-9_]*)\s*=\s*\((\d+),\s*(\d+),\s*(\d+)\)", src, re.M):
    pal[m.group(1)] = tuple(int(m.group(i)) for i in (2, 3, 4))
keys = list(pal)
shares = {}
for v in views:
    p = os.path.join(ROOT, name, "renders", "flat_%s.png" % v)
    im = Image.open(p).convert("RGB")
    cnt = {kk: 0 for kk in keys}
    tot = 0
    for (c, rgb) in im.getcolors(1 << 24):
        if max(rgb) < 6:                     # black background
            continue
        best = min(keys, key=lambda kk: sum((a - b) ** 2 for a, b in zip(pal[kk], rgb)))
        cnt[best] += c
        tot += c
    shares[v] = {kk: round(100.0 * cnt[kk] / tot, 1) for kk in keys if cnt[kk]}
out["shares_pct"] = shares
print(json.dumps(out))
