# Current (Check-UI shots, Studio 1519x753) vs the HATCH NIGHT mockups, one sheet per window + a phone strip.
# usage (from this folder): python make_compare.py   (run bash render.sh first)
from PIL import Image, ImageDraw, ImageFont
B = '../../hatch-night-build/popup_shop/'
F = ImageFont.truetype('../assets/fonts/Montserrat-Black.ttf', 28)
f2 = ImageFont.truetype('../assets/fonts/Montserrat-Bold.ttf', 20)
cur = {'rebirth': (B + 'rebirth_after.jpg', (470, 150, 1050, 640)),
       'index': (B + 'index_after.jpg', (316, 55, 1202, 603)),
       'settings': (B + 'settings_after.jpg', (460, 172, 1058, 638))}
new = {'rebirth': ['rebirth_need', 'rebirth_ready'], 'index': ['index', 'index_claim'], 'settings': ['settings', 'settings_off']}
H = 560
for k, (p, box) in cur.items():
    a = Image.open(p).convert('RGB').crop(box)
    a = a.resize((round(a.width * H / a.height), H), Image.LANCZOS)
    tiles = [('NOW (Check-UI, Studio 1519x753)', a)]
    for v in new[k]:
        b = Image.open(f'{v}_pc.png').convert('RGB').crop((511, 280, 1409, 860))
        b = b.resize((round(b.width * H / b.height), H), Image.LANCZOS)
        tiles.append((f'HATCH NIGHT plan: {v}', b))
    W = sum(t[1].width for t in tiles) + 20 * (len(tiles) + 1)
    sheet = Image.new('RGB', (W, H + 120), (16, 13, 36))
    d = ImageDraw.Draw(sheet)
    x = 20
    for lab, im in tiles:
        sheet.paste(im, (x, 70))
        d.text((x, 22), lab, font=F, fill=(255, 214, 60) if lab.startswith('NOW') else (184, 255, 106))
        x += im.width + 20
    d.text((20, H + 84), 'Layout kept (same zones, same order, same content). Look changed: night shell, cracked band, dark cards, gloss buttons, min text 16 logical.', font=f2, fill=(210, 202, 255))
    sheet.save(f'compare_{k}.png')
    print('compare', k, sheet.size)
ph = [Image.open(f'{v}_phone.png').convert('RGB') for v in ['settings', 'index', 'rebirth_need']]
s = Image.new('RGB', (sum(i.width for i in ph) + 80, 430), (16, 13, 36))
x = 20
for i in ph:
    s.paste(i, (x, 20))
    x += i.width + 20
s.save('sheet_phone.png')
print('phone', s.size)
