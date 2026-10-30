# Offline phone preview (844x390 touch) of the Auto Reconnect label, built from the real desktop capture's art
# and the same geometry as AutoReconnectConfig.place(): k = clamp(min(844/1050, 390/620), 0.52, 1.18) = 0.629.
import sys, glob, os
from PIL import Image, ImageDraw, ImageFont

src, out = sys.argv[1], sys.argv[2]
cap = Image.open(src).convert("RGB")            # 1519x753 desktop capture, k_desktop = 1.18
W, H, INSET = 844, 390, 58                      # phone screen, topbar inset (shared AbsolutePosition space below it)
k = max(0.52, min(1.18, min(W / 1050, H / 620)))
s = k / 1.18                                    # desktop art -> phone art

# background: the 3D scene only (no desktop HUD), cropped to the phone's aspect
bg = cap.crop((262, 62, 1414, 595)).resize((W, H), Image.LANCZOS)
img = bg.copy()

def paste(box, x, y, anchor="tl"):
    part = cap.crop(box)
    part = part.resize((max(1, round(part.width * s)), max(1, round(part.height * s))), Image.LANCZOS)
    if anchor == "br": x, y = x - part.width, y - part.height
    if anchor == "bl": y = y - part.height
    if anchor == "tr": x = x - part.width
    img.paste(part, (round(x), round(y)))
    return part.size

# left HUD column + top bar buttons + right tiles (same anchors as on desktop, scaled)
paste((8, 285, 262, 748), 8 * s, H - 5 * s, "bl")
paste((168, 8, 330, 58), 168 * s, 8 * s)
paste((1432, 288, 1510, 522), W - 9 * s, round(0.385 * H), "tr")

# touch jump button (Roblox default on small screens: 70x70 at (1,-95, 1,-90) of the area below the topbar)
jx, jy = W - 95, (H - 90)
d = ImageDraw.Draw(img, "RGBA")
d.ellipse((jx, jy, jx + 70, jy + 70), fill=(0, 0, 0, 90), outline=(255, 255, 255, 170), width=3)
d.polygon([(jx + 35, jy + 20), (jx + 52, jy + 42), (jx + 18, jy + 42)], fill=(255, 255, 255, 200))

# the weather / Admin Abuse row: left of the jump button, bottoms lined up (WeatherTilesClient)
row_right = jx - int(55 * 0.2 * k)
row_bottom = jy + 70
paste((1360, 648, 1508, 738), row_right, row_bottom, "br")
row_top = row_bottom - (55 + 19) * k

# hotbar (Satchel, bottom centre; one slot with the bat like the desktop capture)
paste((726, 686, 794, 752), W / 2, H - 2, "br")

# the label: Montserrat-Black (= GothamBlack), white, black stroke, right edge = row right, 6*k above the row
fonts = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions\*\content\fonts\Montserrat-Black.ttf"))
SS = 4                                          # supersample
size_px = 22 * k
font = ImageFont.truetype(fonts[0], round(size_px * SS))
text = "Auto Reconnect: 14:13"
stroke = round(2.6 * k * SS)
tw, th = font.getbbox(text, stroke_width=stroke)[2:]
layer = Image.new("RGBA", (tw + 8 * SS, th + 8 * SS), (0, 0, 0, 0))
ImageDraw.Draw(layer).text((4 * SS, 4 * SS), text, font=font, fill="white", stroke_width=stroke, stroke_fill="black")
layer = layer.resize((layer.width // SS, layer.height // SS), Image.LANCZOS)
box_h = 28 * k
label_bottom = row_top - 6 * k
img.paste(layer, (round(row_right - layer.width + 4), round(label_bottom - box_h / 2 - layer.height / 2)), layer)

img.save(out, quality=92)
print("k=%.3f row right %d top %.1f label bottom %.1f text %dx%d" % (k, row_right, row_top, label_bottom, layer.width, layer.height))
