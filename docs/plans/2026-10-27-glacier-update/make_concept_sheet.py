"""Concept sheet for the owner (Glacier update, 2026-10-27): one card per new pet with tier, odds, egg, colour
swatches, look, hero piece and signature act. Reads the ```json block at the end of
PetsV3/_review/GLACIER_CONCEPTS.md. Run: python make_concept_sheet.py
"""
import glob, io, json, os, re
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "PetsV3", "_review", "GLACIER_CONCEPTS.md")
OUT = os.path.join(HERE, "GLACIER_CONCEPT_SHEET.png")

BLACK = sorted(glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions\*\content\fonts\Montserrat-Black.ttf")))
BLACK = BLACK[-1] if BLACK else r"C:\Windows\Fonts\arialbd.ttf"
BODY = r"C:\Windows\Fonts\segoeui.ttf"
BODY_B = r"C:\Windows\Fonts\segoeuib.ttf"

TIER_COL = {"starter": (150, 160, 170), "medium": (60, 190, 170), "medium-high": (80, 150, 230), "big": (70, 130, 235),
            "high": (130, 90, 235), "ultra-rare": (235, 120, 40), "secret": (255, 196, 50), "mythic": (235, 50, 90)}
EGG_COL = {"glacier": (120, 210, 255), "grass": (90, 200, 70), "wood": (90, 200, 70), "water": (60, 160, 255),
           "tide": (60, 160, 255), "thunder": (250, 210, 40), "storm": (250, 210, 40), "fire": (255, 110, 40),
           "magma": (255, 110, 40), "shadow": (150, 90, 230), "void": (150, 90, 230), "celestial": (255, 220, 120)}

W, COLS, CW, CH, PAD = 1920, 3, 620, 345, 10


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lookup(table, key):
    key = (key or "").lower()
    for k, v in table.items():
        if k in key:
            return v
    return (140, 140, 150)


def card(img, x, y, p):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((x, y, x + CW, y + CH), 14, fill=(30, 46, 56), outline=(12, 18, 22), width=4)
    egg = lookup(EGG_COL, p.get("egg"))
    d.rounded_rectangle((x + 4, y + 4, x + CW - 4, y + 70), 12, fill=tuple(int(c * 0.55) for c in egg))
    d.text((x + 18, y + 12), p["name"].upper(), font=font(BLACK, 32), fill=(255, 255, 255),
           stroke_width=3, stroke_fill=(0, 0, 0))
    # tier + odds pill, egg label
    tier = p.get("tier", "")
    tc = lookup(TIER_COL, tier)
    pill = f"{tier.upper()}  {p.get('odds')}%"
    pf = font(BLACK, 20)
    pw = d.textlength(pill, font=pf) + 24
    d.rounded_rectangle((x + 18, y + 82, x + 18 + pw, y + 114), 16, fill=tc, outline=(0, 0, 0), width=2)
    d.text((x + 30, y + 86), pill, font=pf, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
    eg = f"{p.get('egg', '')} egg  ·  {p.get('height', '')} studs"
    d.text((x + 30 + pw, y + 87), eg, font=font(BODY_B, 20), fill=(200, 220, 230))
    # swatches
    sw = p.get("swatches", [])[:5]
    sx, sy, sww, swh = x + 18, y + 128, (CW - 36 - 8 * (max(len(sw), 1) - 1)) / max(len(sw), 1), 70
    for i, (label, hx) in enumerate(sw):
        rgb = hexrgb(hx)
        x0 = sx + i * (sww + 8)
        d.rounded_rectangle((x0, sy, x0 + sww, sy + swh), 8, fill=rgb, outline=(0, 0, 0), width=2)
        lum = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
        tcol = (0, 0, 0) if lum > 150 else (255, 255, 255)
        d.text((x0 + 8, sy + 6), label[:12], font=font(BODY_B, 17), fill=tcol)
        d.text((x0 + 8, sy + 40), hx.upper(), font=font(BODY, 16), fill=tcol)
    # text lines
    ty = sy + swh + 14
    bf, bb = font(BODY, 21), font(BODY_B, 21)
    for head, text in (("Look", p.get("look", "")), ("Hero", p.get("hero", "")), ("Act", p.get("act", ""))):
        if not text:
            continue
        hw = d.textlength(head + ": ", font=bb)
        lines = wrap(d, text, bf, CW - 40 - hw)
        d.text((x + 20, ty), head + ":", font=bb, fill=(255, 214, 90))
        for ln in lines:
            d.text((x + 20 + hw, ty), ln, font=bf, fill=(235, 242, 246))
            ty += 27
        ty += 4


def main():
    md = io.open(SRC, encoding="utf-8").read()
    m = re.findall(r"```json\s*(.*?)```", md, re.S)
    if not m:
        raise SystemExit("no json block in GLACIER_CONCEPTS.md")
    pets = json.loads(m[-1])
    glacier = [p for p in pets if "glacier" in str(p.get("egg", "")).lower()]
    others = [p for p in pets if p not in glacier]
    rows_g = (len(glacier) + COLS - 1) // COLS
    rows_o = (len(others) + COLS - 1) // COLS
    H = 120 + rows_g * (CH + PAD) + 70 + rows_o * (CH + PAD) + 20
    img = Image.new("RGB", (W, H), (59, 88, 102))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 50), "GLACIER UPDATE: 12 NEW PETS (CONCEPTS)", font=font(BLACK, 46), fill=(255, 255, 255),
           anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    x0 = (W - (COLS * CW + (COLS - 1) * PAD)) / 2
    y = 100
    d.text((x0, y), "NEW AREA 7: FROSTFALL GLACIER (Glacier Egg)", font=font(BLACK, 26), fill=(160, 225, 255),
           stroke_width=2, stroke_fill=(0, 0, 0))
    y += 40
    for i, p in enumerate(glacier):
        card(img, x0 + (i % COLS) * (CW + PAD), y + (i // COLS) * (CH + PAD), p)
    y += rows_g * (CH + PAD) + 10
    d.text((x0, y), "+1 NEW PET IN EACH EXISTING EGG", font=font(BLACK, 26), fill=(255, 225, 140),
           stroke_width=2, stroke_fill=(0, 0, 0))
    y += 40
    for i, p in enumerate(others):
        card(img, x0 + (i % COLS) * (CW + PAD), y + (i // COLS) * (CH + PAD), p)
    img.save(OUT)
    print("saved", OUT, img.size)


if __name__ == "__main__":
    main()
