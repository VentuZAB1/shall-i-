import sys
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]
shots = [("BEFORE", "mcp-Roblox_Studio-blob-1791929875398-1yth2y.jpg"),
         ("NEW - day", "mcp-Roblox_Studio-blob-1791934062054-uik9ui.jpg"),
         ("NEW - closer (moss creeping up the wall)", "mcp-Roblox_Studio-blob-1791934073898-dmxjqo.jpg"),
         ("NEW - Moonlit night", "mcp-Roblox_Studio-blob-1791934085598-rmf89t.jpg")]
W = 760
try: font = ImageFont.truetype("arialbd.ttf", 30)
except Exception: font = ImageFont.load_default()
tiles = []
for label, f in shots:
    im = Image.open(f"{src}/{f}").convert("RGB")
    im = im.resize((W, int(im.height * W / im.width)))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 44], fill=(15, 20, 25))
    d.text((12, 6), label, fill=(255, 255, 255), font=font)
    tiles.append(im)
h = max(t.height for t in tiles)
sheet = Image.new("RGB", (W * 2 + 10, h * 2 + 10), (0, 0, 0))
for i, im in enumerate(tiles):
    sheet.paste(im, ((i % 2) * (W + 10), (i // 2) * (h + 10)))
sheet.save(f"{out}/grime_test_patch_v2.jpg", quality=92)
print("ok", sheet.size)
