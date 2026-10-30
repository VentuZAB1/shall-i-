"""Near-miss banner MOCKUP (engagement fix 2, 2026-10-27) - NOT built in the game.

Backdrop: a real Studio Edit capture of the Grass runway with the HUD visible (lighting-2026-10-21/
6_vivid_cumulus_runway.jpg, 1519 x 753 = the Studio viewport; today's screen_capture came back white because Studio
was not in front, and its HUD layer is identical). On top, drawn with PIL in the game's existing styles:
  * the AreaTitle strip that is on screen at the same moment (you just landed in Grass): StarterGui.AreaTitle.Banner,
    y 0.0593, h 0.1111, navy (10,14,28) @ 35% transparency, ends fade 0-22% / 78-100%, thin white lines @ 75%
  * the NEAR-MISS line, Check-UI floating text like REBIRTH READY! (RebirthClientLegacy): centred at y 0.22,
    GothamBlack (Montserrat Black = Roblox's bundled look-alike, from the Studio content/fonts folder), 3.5 px black
    stroke x device scale, white with the area name in the area colour and the distance in tutorial amber #FFD000
Run: python make_near_miss_mockup.py
"""
import glob, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BACK = os.path.join(HERE, "..", "lighting-2026-10-21", "6_vivid_cumulus_runway.jpg")
FONT = sorted(glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions\*\content\fonts\Montserrat-Black.ttf")))[-1]
EMOJI = r"C:\Windows\Fonts\seguiemj.ttf"

W, H = 1519, 753
DEVICE = max(0.52, min(1.18, min(W / 1050, H / 620)))   # BrickUI.deviceScale (the same clamp the HUD uses)
WATER = (60, 200, 255)       # Area2_Water.AreaZone TextColor
GRASS = (90, 235, 70)        # Area1_Grass.AreaZone TextColor
AMBER = (255, 208, 0)        # tutorial accent #FFD000
NAVY = (10, 14, 28)


def fade_alpha(x, w, a):
    t = x / max(w - 1, 1)
    if t < 0.22: return a * t / 0.22
    if t > 0.78: return a * (1 - t) / 0.22
    return a


def strip(img, y, h):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    px = lay.load()
    line = max(2, round(0.035 * h))
    for x in range(W):
        a_bg = int(fade_alpha(x, W, 255 * 0.65))
        a_ln = int(fade_alpha(x, W, 255 * 0.25))
        for yy in range(y, y + h):
            px[x, yy] = NAVY + (a_bg,)
        for yy in list(range(y - line // 2, y + line - line // 2)) + list(range(y + h - line // 2, y + h + line - line // 2)):
            if 0 <= yy < H:
                px[x, yy] = (255, 255, 255, a_ln)
    img.alpha_composite(lay)


def rich_text(img, cx, cy, parts, size, stroke):
    """parts = [(text, rgb)], one line centred on (cx, cy), black outline (Check-UI)."""
    font = ImageFont.truetype(FONT, size)
    d = ImageDraw.Draw(img)
    widths = [d.textlength(t, font=font) for t, _ in parts]
    x = cx - sum(widths) / 2
    asc, desc = font.getmetrics()
    y = cy - (asc + desc) / 2
    for (t, col), w in zip(parts, widths):
        d.text((x, y), t, font=font, fill=col + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
        x += w
    return sum(widths)


def area_title(img, text, emoji, color, y, h):
    size = int(h * 0.62)
    font = ImageFont.truetype(FONT, size)
    d = ImageDraw.Draw(img)
    tw = d.textlength(text, font=font)
    ew = 0
    efont = None
    try:
        efont = ImageFont.truetype(EMOJI, 109)  # bitmap/colour emoji sizes are fixed: draw big, scale down
    except OSError:
        pass
    ex = cx = W / 2
    total = tw + (size * 1.15 if efont else 0)
    x0 = cx - total / 2
    asc, desc = font.getmetrics()
    d.text((x0, y + h / 2 - (asc + desc) / 2), text, font=font, fill=color + (255,),
           stroke_width=max(2, round(size * 0.06)), stroke_fill=(0, 0, 0, 255))
    if efont:
        em = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
        ImageDraw.Draw(em).text((10, 0), emoji, font=efont, embedded_color=True)
        em = em.crop(em.getbbox() or (0, 0, 140, 140)).resize((int(size * 0.95), int(size * 0.95)), Image.LANCZOS)
        img.alpha_composite(em, (int(x0 + tw + size * 0.18), int(y + h / 2 - em.height / 2)))


def mockup(out_path, studs=12, with_area_title=True):
    img = Image.open(BACK).convert("RGBA").resize((W, H))
    if with_area_title:
        sy, sh = round(0.0593 * H), round(0.1111 * H)
        strip(img, sy, sh)
        area_title(img, "Grass", "\U0001F33F", GRASS, sy, sh)
    size = round(34 * DEVICE)                 # 34 px design size (REBIRTH READY! is ~42 for half the letters)
    rich_text(img, W / 2, 0.22 * H, [("WATER", WATER), (" IS ONLY ", (255, 255, 255)), (f"{studs} STUDS", AMBER),
                                      (" AWAY!", (255, 255, 255))], size, round(3.5 * DEVICE))
    img.convert("RGB").save(out_path, quality=95)
    return img


if __name__ == "__main__":
    a = mockup(os.path.join(HERE, "near_miss_banner_mockup.png"), 12, True)
    b = mockup(os.path.join(HERE, "near_miss_banner_mockup_no_area_title.png"), 12, False)
    # a 2x zoom of the banner area for reading the type
    z = a.crop((int(W * 0.12), 30, int(W * 0.88), 215)).resize((int(W * 0.76 * 2), 370), Image.LANCZOS)
    z.convert("RGB").save(os.path.join(HERE, "near_miss_banner_mockup_zoom.png"))
    print("device scale", round(DEVICE, 3), "font", FONT)
