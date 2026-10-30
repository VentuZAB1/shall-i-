# Current (Check-UI) vs the HATCH NIGHT mockups, one sheet per window + a phone strip + a 1050 / 667 strip.
# usage (from this folder): python make_compare.py   (run bash render.sh first)
# Current images: the 2026-10-15 review captures for Free Gift / Welcome Back (Studio 1519 x 753, the live v2 layouts) and
# current_upgrades_1519.png = a reconstruction from UpgradeClient's numbers (no capture exists; the builder re-shoots it in
# Task 0 and re-runs this script with CUR_UPGRADES pointing at the real shot).
from PIL import Image, ImageDraw, ImageFont
import os
R = '../../../reviews/'
F = ImageFont.truetype('../assets/fonts/Montserrat-Black.ttf', 28)
f2 = ImageFont.truetype('../assets/fonts/Montserrat-Bold.ttf', 20)
CUR_UPGRADES = os.environ.get('CUR_UPGRADES', 'current_upgrades_1519.png')
cur = {
    'freegift': (R + '2026-10-15-freegift-ui/current_v2.jpg', (405, 81, 1114, 672), 'NOW (Check-UI, Studio 1519x753)'),
    'welcome': (R + '2026-10-15-offline-ui/current_v2.jpg', (417, 99, 1102, 654), 'NOW (Check-UI, Studio 1519x753)'),
    'upgrades': (CUR_UPGRADES, (366, 123, 1153, 630), 'NOW (reconstruction from UpgradeClient)' if CUR_UPGRADES.startswith('current_') else 'NOW (Check-UI, Studio 1519x753)'),
}
# window rect on the 1920 x 1080 renders (gui y 58 + the fit), +-24 px margin; the tutorial views start at the guide
win = {'freegift': (629.6, 297.6, 661, 543), 'welcome': (641.4, 315.3, 637, 507), 'upgrades': (419.5, 225.7, 1081, 687)}
new = {'freegift': ['freegift', 'freegift_joined', 'freegift_claimed'], 'welcome': ['welcome', 'welcome_x5'],
       'upgrades': ['upgrades', 'upgrades_free', 'upgrades_max']}
notes = {
    'freegift': 'Kept: art left, ONE-TIME GIFT + 3 POTIONS right, the 2 step cards, CLAIM centred. Moved (83 % rule at 16 px): the x2 line -> a 3-row list; the red hint line -> the CLAIM button word.',
    'welcome': 'Kept: OFFLINE EARNINGS, cash art, the amount, CLAIM x5 left + CLAIM right. Moved: the price tag (it hung over the x5 button corner) -> inside the gold button.',
    'upgrades': 'Kept: header + REBIRTH n, 3 rows (icon, name, desc, level bar, now > next, $ buy, +1 LV Robux), the footer. Moved: short desc copy, the area word to the desc line (min 16 px).',
}
H = 600
for k, (p, box, lab0) in cur.items():
    a = Image.open(p).convert('RGB').crop(box)
    a = a.resize((round(a.width * H / a.height), H), Image.LANCZOS)
    tiles = [(lab0, a)]
    for v in new[k]:
        x, y, w, h = win[k]
        top = 60 if v == 'upgrades_free' else y - 24
        b = Image.open(f'{v}_pc.png').convert('RGB').crop((round(x - 24), round(top), round(x + w + 24), round(y + h + 24)))
        b = b.resize((round(b.width * H / b.height), H), Image.LANCZOS)
        tiles.append((f'HATCH NIGHT: {v}', b))
    W = sum(t[1].width for t in tiles) + 20 * (len(tiles) + 1)
    sheet = Image.new('RGB', (W, H + 130), (16, 13, 36))
    d = ImageDraw.Draw(sheet)
    x = 20
    for lab, im in tiles:
        sheet.paste(im, (x, 70))
        d.text((x, 22), lab, font=F, fill=(255, 214, 60) if lab.startswith('NOW') else (184, 255, 106))
        x += im.width + 20
    d.text((20, H + 86), notes[k], font=f2, fill=(210, 202, 255))
    sheet.save(f'compare_{k}.png')
    print('compare', k, sheet.size)
for name, views, dev in [('sheet_phone', ['freegift_joined', 'welcome', 'upgrades', 'upgrades_free'], 'phone'),
                         ('sheet_small', ['freegift', 'welcome', 'upgrades'], '1050'),
                         ('sheet_667', ['freegift', 'welcome', 'upgrades'], '667')]:
    ph = [Image.open(f'{v}_{dev}.png').convert('RGB') for v in views]
    s = Image.new('RGB', (sum(i.width for i in ph) + 20 * (len(ph) + 1), max(i.height for i in ph) + 40), (16, 13, 36))
    x = 20
    for i in ph:
        s.paste(i, (x, 20))
        x += i.width + 20
    s.save(f'{name}.png')
    print(name, s.size)
