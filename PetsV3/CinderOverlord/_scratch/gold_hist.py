# python CinderOverlord/_scratch/gold_hist.py <raw.png> [<raw.png> ...]
# For each transparent portrait render: the icon3 recipe (crop to bbox, 1.16 pad, 512, black outline ring) -> 64 px,
# then gold counts (s > .5, v > .45) for the kit window H 29-58 (game_icon.py: hue 0.08-0.16) and the widened
# H 29-60, the lemon count H 59-61, a hue histogram (2-deg bins, H 26-66), plus the silhouette fill (bbox height and
# width of the 64 px icon's opaque pixels / 64).
import sys, os, json, colorsys
from PIL import Image, ImageFilter


def icon(raw):
    im = Image.open(raw).convert("RGBA")
    bb = im.split()[3].point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop(bb)
    w, h = im.size
    side = int(max(w, h) * 1.16)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(im, ((side - w) // 2, (side - h) // 2))
    sq = sq.resize((512, 512), Image.LANCZOS)
    alpha = sq.split()[3].point(lambda v: 255 if v > 40 else 0)
    ring = alpha.filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.GaussianBlur(1.2))
    out = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    out.paste(Image.new("RGBA", (512, 512), (12, 12, 16, 255)), (0, 0), ring)
    out.alpha_composite(sq)
    return out


def stats(ic, size=64):
    sm = ic.resize((size, size), Image.LANCZOS)
    px = list(sm.getdata())
    r = {"kit_29-58": 0, "wide_29-60": 0, "lemon_59-61": 0}
    hist = {}
    for (R, G, B, A) in px:
        if A <= 128:
            continue
        h, s, v = colorsys.rgb_to_hsv(R / 255, G / 255, B / 255)
        H = h * 360
        if s > 0.5 and v > 0.45:
            if 0.08 <= h <= 0.16:
                r["kit_29-58"] += 1
            if 29 <= H <= 60:
                r["wide_29-60"] += 1
            if 59 <= H <= 61:
                r["lemon_59-61"] += 1
            if 26 <= H < 66:
                b = int(H // 2 * 2)
                hist[b] = hist.get(b, 0) + 1
    r["hist"] = dict(sorted(hist.items()))
    # silhouette fill of the 64 px icon (the figure, without the outline ring: alpha of the pet only)
    a = sm.split()[3].point(lambda v: 255 if v > 128 else 0)
    bb = a.getbbox()
    r["fill_h"] = round((bb[3] - bb[1]) / size, 3)
    r["fill_w"] = round((bb[2] - bb[0]) / size, 3)
    r["area"] = round(sum(1 for v in a.getdata() if v) / float(size * size), 3)      # opaque share of the 64 px card (incl. ring)
    return r


res = {}
for p in sys.argv[1:]:
    ic = icon(p)
    o = os.path.splitext(p)[0] + "_icon.png"
    ic.save(o)
    res[os.path.basename(p)] = stats(ic)
print("GOLD_HIST " + json.dumps(res))
