# python CinderOverlord/_scratch/icon_game_64_128.py -> renders/_icon_game_64_128.png (the game icon at 64 and 128 px
# on the slate tile, title = render time of CinderOverlord_icon_game.png)
import os, time
from PIL import Image, ImageDraw
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
src = os.path.join(D, "CinderOverlord_icon_game.png")
t = time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(src)))
ic = Image.open(src).convert("RGBA")
o = Image.new("RGB", (210, 162), (24, 28, 34))
d = ImageDraw.Draw(o)
d.text((6, 6), "game icon 64 / 128 - %s r14" % t, fill=(235, 235, 235))
for sz, (x, y) in ((64, (6, 28)), (128, (76, 28))):
    tile = Image.new("RGBA", (sz, sz), (52, 62, 74, 255))
    tile.alpha_composite(ic.resize((sz, sz), Image.LANCZOS))
    o.paste(tile.convert("RGB"), (x, y))
o.save(os.path.join(D, "renders", "_icon_game_64_128.png"))
print("icon_game_64_128", t)
