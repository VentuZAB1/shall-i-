import sys
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]
shots = [("DAY (original, restored)", "mcp-Roblox_Studio-blob-1791915896752-aswkhc.jpg"),
         ("A  Moonlit", "mcp-Roblox_Studio-blob-1791916177636-fvb85s.jpg"),
         ("B  Dusk", "mcp-Roblox_Studio-blob-1791916190134-i3cbvw.jpg"),
         ("C  Halloween night", "mcp-Roblox_Studio-blob-1791916201716-u6jfc5.jpg")]
W = 760
tiles = []
for label, f in shots:
    im = Image.open(f"{src}/{f}").convert("RGB")
    im = im.resize((W, int(im.height * W / im.width)))
    d = ImageDraw.Draw(im)
    try: font = ImageFont.truetype("arialbd.ttf", 34)
    except Exception: font = ImageFont.load_default()
    d.rectangle([0, 0, W, 50], fill=(15, 20, 25))
    d.text((14, 7), label, fill=(255, 255, 255), font=font)
    tiles.append((label, im))
    im.save(f"{out}/{label.split()[0]}_{'_'.join(label.split()[1:]).replace('(', '').replace(')', '').replace(',', '')}.jpg", quality=92)
h = tiles[0][1].height
sheet = Image.new("RGB", (W * 2 + 10, h * 2 + 10), (0, 0, 0))
for i, (_, im) in enumerate(tiles):
    sheet.paste(im, ((i % 2) * (W + 10), (i // 2) * (h + 10)))
sheet.save(f"{out}/night_options.jpg", quality=92)
print("ok", sheet.size)
