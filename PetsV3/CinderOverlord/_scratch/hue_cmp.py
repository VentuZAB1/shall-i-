# python CinderOverlord/_scratch/hue_cmp.py -> CinderOverlord/_scratch/hue_cmp.png
# candidates (rows) at 128 px and 64 px next to Ivonrath, InfernoPhoenix, ThunderRex (pack_post card style)
import os
from PIL import Image, ImageDraw
R = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
S = os.path.join(R, "CinderOverlord", "_scratch")
rows = [("r4 now (160,87,102) pink", os.path.join(S, "hue_r4_icon.png")),
        ("A ember (166,66,50)", os.path.join(S, "hue_A_icon.png")),
        ("B oxblood (160,50,56)", os.path.join(S, "hue_B_icon.png")),
        ("A2 = A + ember accent (255,84,48)", os.path.join(S, "hue_A2_icon.png")),
        ("B2 = B + ember accent (255,84,48)", os.path.join(S, "hue_B2_icon.png"))]
cmps = [os.path.join(R, n, n + "_icon.png") for n in ("Ivonrath", "InfernoPhoenix", "ThunderRex")]
LBL = 250
def card(p, px):
    im = Image.open(p).convert("RGBA").resize((px, px), Image.LANCZOS)
    bg = Image.new("RGBA", (px + 6, px + 6), (52, 62, 74, 255))
    bg.alpha_composite(im, (3, 3))
    return bg.convert("RGB")
W = LBL + 4 * 134 + 30 + 4 * 70
H = len(rows) * 140 + 24
out = Image.new("RGB", (W, H), (22, 24, 30))
d = ImageDraw.Draw(out)
d.text((LBL, 4), "128 px:  candidate | Ivonrath | InfernoPhoenix | ThunderRex", fill=(230, 230, 230))
d.text((LBL + 4 * 134 + 30, 4), "64 px", fill=(230, 230, 230))
for i, (name, p) in enumerate(rows):
    y = 24 + i * 140
    d.text((6, y + 60), name, fill=(240, 240, 240))
    for j, q in enumerate([p] + cmps):
        out.paste(card(q, 128), (LBL + j * 134, y))
        out.paste(card(q, 64), (LBL + 4 * 134 + 30 + j * 70, y + 32))
out.save(os.path.join(S, "hue_cmp.png"))
print(out.size)
