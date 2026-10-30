# Contact sheets of VFX Studio library textures (public Roblox thumbnails), to pick textures by eye.
import json, sys, io, urllib.request, time
from PIL import Image, ImageDraw
ids = json.load(open("lib_ids.json"))
CELL, COLS = 110, 10
def thumbs(batch):
    url = "https://thumbnails.roblox.com/v1/assets?assetIds=" + ",".join(batch) + "&returnPolicy=PlaceHolder&size=110x110&format=Png&isCircular=false"
    for _ in range(4):
        data = json.load(urllib.request.urlopen(url, timeout=20))["data"]
        if all(d["state"] == "Completed" for d in data): break
        time.sleep(2)
    return {str(d["targetId"]): d.get("imageUrl") for d in data}
for cat in sys.argv[1:]:
    lst = ids[cat].split(",")[:100]
    urls = {}
    for i in range(0, len(lst), 50):
        urls.update(thumbs(lst[i:i + 50]))
    rows = (len(lst) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * CELL, rows * (CELL + 14)), (38, 40, 48))
    dr = ImageDraw.Draw(sheet)
    for n, aid in enumerate(lst):
        x, y = (n % COLS) * CELL, (n // COLS) * (CELL + 14)
        u = urls.get(aid)
        if u:
            try:
                im = Image.open(io.BytesIO(urllib.request.urlopen(u, timeout=20).read())).convert("RGBA")
                bg = Image.new("RGBA", im.size, (38, 40, 48, 255))
                sheet.paste(Image.alpha_composite(bg, im).convert("RGB").resize((CELL - 4, CELL - 4)), (x + 2, y + 2))
            except Exception as e:
                pass
        dr.text((x + 3, y + CELL), f"{cat[0]}{n}", fill=(255, 220, 90))
    sheet.save(f"sheets/{cat}.png")
    print(cat, len(lst))
