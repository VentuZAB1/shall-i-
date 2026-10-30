# python PermafrostTitan/_scratch/shares_all.py <Name> [views]  (variant of shares.py: no edge exclusion)
# strict value shares from the flat ID renders: background (max < 6) AND anti-aliased edge / speckle pixels
# (farther than TOL from every palette colour) are excluded. Same palette parse as _tools/pack_post.py.
import sys, os, re, json
from PIL import Image
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
name = sys.argv[1]
views = sys.argv[2].split(",") if len(sys.argv) > 2 else ["side", "tq", "game"]
TOL = float("inf")   # ALL figure pixels (background only excluded) -> nearest palette colour
src = open(os.path.join(ROOT, "pets", name + ".py"), encoding="utf-8").read()
pal = {}
for m in re.finditer(r"^([A-Z][A-Z0-9_]*)\s*=\s*\((\d+),\s*(\d+),\s*(\d+)\)", src, re.M):
    pal[m.group(1)] = tuple(int(m.group(i)) for i in (2, 3, 4))
keys = list(pal)
out = {}
for v in views:
    im = Image.open(os.path.join(ROOT, name, "renders", "flat_%s.png" % v)).convert("RGB")
    cnt = {kk: 0 for kk in keys}
    tot = skip = 0
    for (c, rgb) in im.getcolors(1 << 24):
        if max(rgb) < 6:
            continue
        d, best = min((sum((a - b) ** 2 for a, b in zip(pal[kk], rgb)), kk) for kk in keys)
        if d > TOL:
            skip += c
            continue
        cnt[best] += c
        tot += c
    out[v] = {kk: round(100.0 * cnt[kk] / tot, 1) for kk in keys if cnt[kk]}
    out[v]["_edge_px_skipped_pct"] = round(100.0 * skip / (tot + skip), 1)
print(json.dumps(out))
