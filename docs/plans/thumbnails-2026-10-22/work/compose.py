"""Composite the SLINGSHOT thumbnails (2026-10-22) from Studio Edit captures.

python compose.py            -> thumb_1_launch.png, thumb_2_secret.png, thumb_3_tsunami.png, sheet.png (one folder up)
Each capture is cropped to 16:9, upscaled to 1920x1080 (Lanczos), colour graded, edge-blurred (soft focus away from
the subject), sharpened, vignetted, then gets ONE headline in Luckiest Guy (Roblox's font) with a thick dark outline,
a gradient fill and a chunky drop shadow.
"""
import glob
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
CAPS = os.path.join(HERE, "caps")
W, H = 1920, 1080


def find_font():
    pats = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions\*\content\fonts\LuckiestGuy-Regular.ttf"))
    if pats:
        return pats[0]
    return r"C:\Windows\Fonts\impact.ttf"


FONT = find_font()


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(w, h, stops):
    """vertical gradient image from [(t, (r,g,b)), ...]"""
    im = Image.new("RGB", (1, h))
    px = im.load()
    for y in range(h):
        t = y / max(1, h - 1)
        for i in range(1, len(stops)):
            if t <= stops[i][0]:
                a, b = stops[i - 1], stops[i]
                px[0, y] = lerp(a[1], b[1], (t - a[0]) / max(1e-6, b[0] - a[0]))
                break
        else:
            px[0, y] = stops[-1][1]
    return im.resize((w, h))


def radial(w, h, cx, cy, rx, ry, inner, outer, power=2.0):
    """L mask: inner value inside the ellipse centre, outer at/after its edge"""
    small = Image.new("L", (w // 8, h // 8))
    px = small.load()
    sw, sh = small.size
    for y in range(sh):
        for x in range(sw):
            dx = (x / sw - cx) / rx
            dy = (y / sh - cy) / ry
            d = min(1.0, (dx * dx + dy * dy) ** 0.5)
            v = inner + (outer - inner) * (d ** power)
            px[x, y] = int(max(0, min(255, v)))
    return small.resize((w, h), Image.BICUBIC)


def base_image(cfg):
    src = Image.open(os.path.join(CAPS, cfg["cap"])).convert("RGB")
    for p in cfg.get("patches", []):
        if p[0] == "copy":  # ("copy", (x0, y0, x1, y1), dx, dy): fill the box from the area offset by dx, dy
            x0_, y0_, x1_, y1_ = p[1]
            patch = src.crop((x0_ + p[2], y0_ + p[3], x1_ + p[2], y1_ + p[3]))
            m = Image.new("L", patch.size, 255).filter(ImageFilter.GaussianBlur(0))
            src.paste(patch, (x0_, y0_), m)
        elif p[0] == "blur":  # ("blur", box, radius)
            region = src.crop(p[1]).filter(ImageFilter.GaussianBlur(p[2]))
            src.paste(region, p[1][:2])
    sw, sh = src.size
    ch = cfg.get("crop_h", sh)
    cw = round(ch * 16 / 9)
    x0 = cfg.get("crop_x", (sw - cw) // 2)
    y0 = cfg.get("crop_y", sh - ch)
    im = src.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)
    # grade
    im = ImageEnhance.Color(im).enhance(cfg.get("sat", 1.18))
    im = ImageEnhance.Contrast(im).enhance(cfg.get("contrast", 1.08))
    im = ImageEnhance.Brightness(im).enhance(cfg.get("bright", 1.02))
    # soft focus away from the subject
    fx, fy, frx, fry = cfg["focus"]
    blurred = im.filter(ImageFilter.GaussianBlur(cfg.get("edge_blur", 5)))
    keep = radial(W, H, fx, fy, frx, fry, 255, 0, power=3.0)
    im = Image.composite(im, blurred, keep)
    # sharpen the subject
    sharp = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=cfg.get("sharpen", 90), threshold=2))
    im = Image.composite(sharp, im, keep)
    # vignette
    vig = radial(W, H, 0.5, 0.5, 0.78, 0.78, 255, cfg.get("vignette", 170), power=2.4)
    dark = Image.merge("RGB", (vig, vig, vig))
    im = ImageChops.multiply(im, dark)
    return im


def text_block(lines, size_list, fill_stops, outline, stroke, line_gap, extrude, angle, align="center"):
    """returns an RGBA image of the stacked headline"""
    fonts = [ImageFont.truetype(FONT, s) for s in size_list]
    pad = stroke + extrude + 20
    boxes = [f.getbbox(t, stroke_width=stroke) for f, t in zip(fonts, lines)]
    widths = [b[2] - b[0] for b in boxes]
    heights = [b[3] - b[1] for b in boxes]
    bw = max(widths) + pad * 2
    bh = sum(heights) + line_gap * (len(lines) - 1) + pad * 2
    mask_fill = Image.new("L", (bw, bh), 0)
    mask_stroke = Image.new("L", (bw, bh), 0)
    df = ImageDraw.Draw(mask_fill)
    ds = ImageDraw.Draw(mask_stroke)
    y = pad
    line_masks = []
    for f, t, b, w_, h_ in zip(fonts, lines, boxes, widths, heights):
        if align == "center":
            x = (bw - w_) // 2 - b[0]
        elif align == "left":
            x = pad - b[0]
        else:
            x = bw - pad - w_ - b[0]
        ds.text((x, y - b[1]), t, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
        lm = Image.new("L", (bw, bh), 0)
        ImageDraw.Draw(lm).text((x, y - b[1]), t, font=f, fill=255)
        line_masks.append((lm, y, h_))
        df.text((x, y - b[1]), t, font=f, fill=255)
        y += h_ + line_gap
    out = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    # soft shadow
    sh = mask_stroke.filter(ImageFilter.GaussianBlur(10))
    shadow = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    shadow.putalpha(sh.point(lambda v: int(v * 0.55)))
    out.alpha_composite(shadow, (6, extrude + 8))
    # chunky extrude: the outline shape stacked downwards, a touch darker
    ext_col = tuple(max(0, c - 10) for c in outline)
    for k in range(extrude, 0, -1):
        layer = Image.new("RGBA", (bw, bh), ext_col + (255,))
        layer.putalpha(mask_stroke)
        out.alpha_composite(layer, (0, k))
    # outline
    ol = Image.new("RGBA", (bw, bh), outline + (255,))
    ol.putalpha(mask_stroke)
    out.alpha_composite(ol)
    # gradient fill per line (each line gets the full gradient)
    for (lm, ly, lh), stops in zip(line_masks, fill_stops):
        g = Image.new("RGB", (bw, bh), stops[-1][1])
        g.paste(vgrad(bw, lh + 8, stops), (0, max(0, ly - 4)))
        fill = g.convert("RGBA")
        fill.putalpha(lm)
        out.alpha_composite(fill)
        # glossy top highlight: a white band on the upper third of the letters
        hl = Image.new("L", (bw, bh), 0)
        ImageDraw.Draw(hl).rectangle((0, ly, bw, ly + int(lh * 0.30)), fill=70)
        hl = ImageChops.multiply(hl, lm.filter(ImageFilter.MinFilter(5)))
        white = Image.new("RGBA", (bw, bh), (255, 255, 255, 0))
        white.putalpha(hl)
        out.alpha_composite(white)
    if angle:
        out = out.rotate(angle, resample=Image.BICUBIC, expand=True)
    return out


def place(im, block, cx, cy, max_w=None):
    if max_w and block.width > max_w:
        k = max_w / block.width
        block = block.resize((int(block.width * k), int(block.height * k)), Image.LANCZOS)
    im = im.convert("RGBA")
    im.alpha_composite(block, (int(cx - block.width / 2), int(cy - block.height / 2)))
    return im.convert("RGB"), block.size


YELLOW = [(0, (255, 251, 170)), (0.45, (255, 222, 40)), (1, (255, 138, 0))]
GOLD = [(0, (255, 250, 200)), (0.5, (255, 200, 30)), (1, (240, 120, 0))]
CYAN = [(0, (240, 255, 255)), (0.5, (120, 235, 255)), (1, (30, 140, 255))]
HOT = [(0, (255, 245, 160)), (0.45, (255, 170, 30)), (1, (255, 60, 30))]
NAVY = (22, 14, 48)

THUMBS = {
    "thumb_1_launch.png": dict(
        cap="S1_6.jpg", crop_x=95, focus=(0.36, 0.46, 0.62, 0.75), edge_blur=3,
        text=dict(lines=["LAUNCH", "FOR EGGS!"], sizes=[170, 128], fills=[YELLOW, YELLOW], angle=5,
                  cx=0.70, cy=0.215, max_w=0.36),
    ),
    "thumb_2_secret.png": dict(
        cap="S2_8.jpg", crop_x=180, focus=(0.42, 0.47, 0.5, 0.68), edge_blur=4, sat=1.12,
        patches=[("blur", (1178, 536, 1245, 560), 6)],
        text=dict(lines=["1% SECRET", "PET!"], sizes=[150, 200], fills=[GOLD, GOLD], angle=-4,
                  cx=0.735, cy=0.245, max_w=0.34),
    ),
    "thumb_3_tsunami.png": dict(
        cap="S3_5.jpg", crop_x=150, crop_h=700, focus=(0.6, 0.55, 0.5, 0.65), edge_blur=4,
        patches=[("copy", (1163, 420, 1223, 482), -58, 0), ("copy", (1223, 420, 1283, 482), -118, 0)],
        text=dict(lines=["RUN FROM THE", "TSUNAMI!"], sizes=[112, 176], fills=[HOT, HOT], angle=-4,
                  cx=0.30, cy=0.235, max_w=0.44),
    ),
}


def build(name, cfg):
    im = base_image(cfg)
    t = cfg["text"]
    block = text_block(t["lines"], t["sizes"], t["fills"], NAVY, stroke=t.get("stroke", 16), line_gap=10,
                       extrude=t.get("extrude", 10), angle=t["angle"])
    im, size = place(im, block, t["cx"] * W, t["cy"] * H, max_w=int(t["max_w"] * W))
    im.save(os.path.join(OUT, name), optimize=True)
    return im, size


def sheet(images):
    gap = 24
    big_w = 960
    big_h = 540
    small_w = 400
    small_h = 225
    sw = gap + (big_w + gap) * 3
    sh_ = gap + big_h + gap + small_h + gap + 40
    s = Image.new("RGB", (sw, sh_), (24, 26, 34))
    d = ImageDraw.Draw(s)
    f = ImageFont.truetype(FONT, 28)
    for i, (n, im) in enumerate(images):
        x = gap + i * (big_w + gap)
        s.paste(im.resize((big_w, big_h), Image.LANCZOS), (x, gap))
        sm = im.resize((small_w, small_h), Image.LANCZOS)
        s.paste(sm, (x, gap + big_h + gap))
        d.text((x + small_w + 20, gap + big_h + gap + 10), n, font=f, fill=(235, 235, 245))
        d.text((x + small_w + 20, gap + big_h + gap + 50), "400 px preview", font=ImageFont.truetype(FONT, 22), fill=(160, 165, 180))
    s.save(os.path.join(OUT, "sheet.png"), optimize=True)


if __name__ == "__main__":
    only = sys.argv[1:]
    done = []
    for n, c in THUMBS.items():
        if only and n not in only:
            continue
        im, size = build(n, c)
        print(n, "text block", size)
        done.append((n, im))
    if not only:
        sheet(done)
        print("sheet.png")
