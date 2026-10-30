# python CinderOverlord/_scratch/alt_strip.py -> renders/_icons_alt_strip_64.png / _128.png
# [Cinder portrait_alt icon (molt peak), Cinder kit portrait icon (idle f0), Thunder Rex, Cosmic Leviathan], same
# background + layout as pack_post's _icons_strip, with a title bar (render time of CinderOverlord_portrait_alt.png)
import os, time
from PIL import Image, ImageDraw
R = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
D = os.path.join(R, "CinderOverlord")
t = time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(os.path.join(D, "CinderOverlord_portrait_alt.png"))))
items = [("Cinder alt (not shipped)", os.path.join(D, "CinderOverlord_icon_alt.png")),
         ("Cinder kit = SHIPS", os.path.join(D, "CinderOverlord_icon.png")),
         ("InfernoPhoenix", os.path.join(R, "InfernoPhoenix", "InfernoPhoenix_icon.png")),
         ("Ivonrath", os.path.join(R, "Ivonrath", "Ivonrath_icon.png")),
         ("ThunderRex", os.path.join(R, "ThunderRex", "ThunderRex_icon.png")),
         ("CosmicLeviathan", os.path.join(R, "CosmicLeviathan", "CosmicLeviathan_icon.png"))]
for px in (64, 128):
    W = len(items) * (px + 6) + 6
    head = 22
    strip = Image.new("RGB", (max(W, 420), px + 12 + head + 14), (24, 28, 34))
    d = ImageDraw.Draw(strip)
    d.text((6, 5), "CinderOverlord _icons_alt_strip_%d.png - rendered %s (final 8.5 round 14)" % (px, t),
           fill=(235, 235, 235))
    for i, (lab, p) in enumerate(items):
        im = Image.open(p).convert("RGBA").resize((px, px), Image.LANCZOS)
        bg = Image.new("RGBA", (px, px), (52, 62, 74, 255))
        bg.alpha_composite(im)
        strip.paste(bg.convert("RGB"), (6 + i * (px + 6), head + 6))
        d.text((6 + i * (px + 6), head + px + 8), lab[:px // 6], fill=(170, 170, 170))
    strip.save(os.path.join(D, "renders", "_icons_alt_strip_%d.png" % px))
print("alt strips", t)
