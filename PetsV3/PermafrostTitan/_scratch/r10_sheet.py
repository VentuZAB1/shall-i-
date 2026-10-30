# r10: the side-on kneel test sheet - game camera (top) + 2x knee-aimed (bottom) at f40 for every variant tested
import os, datetime
from PIL import Image, ImageDraw, ImageFont
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "r10")
V = [("r8", "EXPORTED r8: yaw 30", "shin 47.8% / 58.5%", "thigh 59.1%  knee -0.008"),
     ("y45", "yaw 45", "shin 46.3% / 58.7%", "thigh 48.3%  knee -0.008"),
     ("y60", "yaw 60", "shin 42.6% / 58.5%", "thigh 25.3%  knee -0.008"),
     ("y75", "yaw 75", "shin 39.0% / 54.3%", "thigh  3.8%  knee -0.008"),
     ("t30", "yaw 30 + toes tucked 40", "shin 64.0% / 63.9%", "thigh 61.1%  knee +0.010 OFF"),
     ("t45", "yaw 45 + toes tucked 40", "shin 58.8% / 64.7%", "thigh 51.5%  knee +0.010 OFF"),
     ("k45", "yaw 45 + tuck 32, drop .37", "shin 43.4% / 61.2%", "thigh 51.8%  knee -0.009")]
C = 360
try:
    F = ImageFont.truetype("arialbd.ttf", 17)
    f2 = ImageFont.truetype("arial.ttf", 15)
    FT = ImageFont.truetype("arialbd.ttf", 20)
except Exception:
    F = f2 = FT = ImageFont.load_default()
H0, HL = 44, 70
sheet = Image.new("RGB", (C * len(V), H0 + HL + 2 * C), (24, 26, 30))
d = ImageDraw.Draw(sheet)
stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
d.text((10, 10), "Permafrost Titan act_kneelrise f40 - r10 side-on test (shin = vert share [arm_search, real game cam] / screen-area share)   %s" % stamp, fill=(235, 235, 235), font=FT)
for i, (tag, a, b, c) in enumerate(V):
    x = i * C
    col = (255, 210, 120) if tag == "r8" else (235, 235, 235)
    d.text((x + 8, H0 + 2), a, fill=col, font=F)
    d.text((x + 8, H0 + 24), b, fill=(160, 230, 160) if ("64" in b or "61" in b) else (235, 235, 235), font=f2)
    d.text((x + 8, H0 + 44), c, fill=(255, 140, 140) if "OFF" in c or " 3.8" in c or "25.3" in c else (200, 200, 200), font=f2)
    for r, v in enumerate(("game", "game2x")):
        p = os.path.join(D, "%s_%s_40.png" % (tag, v))
        if os.path.exists(p):
            im = Image.open(p).convert("RGB").resize((C, C), Image.LANCZOS)
            sheet.paste(im, (x, H0 + HL + r * C))
out = os.path.join(D, "_r10_side_on_tests_f40.png")
sheet.save(out)
print(out, stamp)
