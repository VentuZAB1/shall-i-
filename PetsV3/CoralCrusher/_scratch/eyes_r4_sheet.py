# Crab r4 eyes: titled sheets from the eyA_ / eyB_ renders
#   renders/_eyes_r4_face.png      : before / after face close-ups (front + tq)
#   renders/_eyes_r4_game1x.png    : after, game camera at 1x (390 px) f30 / 41 / 53 / 62 / 66, full frame + eye box x4
#   renders/_eyes_r4_game_cmp.png  : before vs after eye box x4 at f30 / f41 / f66
import os, time
from PIL import Image, ImageDraw
R = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher\renders"
STAMP = time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(os.path.join(R, "eyA_game_act_semaphore_41.png"))))
BOX = (105, 120, 215, 230)          # eye box on the 390 px game frame (both eyes, top to trough)
Z = 4


def titled(img, title):
    o = Image.new("RGB", (img.width, img.height + 22), (24, 26, 34))
    o.paste(img, (0, 22))
    ImageDraw.Draw(o).text((6, 5), title, fill=(235, 235, 235))
    return o


def lab(img, t):
    d = ImageDraw.Draw(img)
    d.text((5, 4), t, fill=(200, 0, 0))
    return img


def crop(path):
    im = Image.open(path).convert("RGB")
    return im.crop(BOX).resize(((BOX[2] - BOX[0]) * Z, (BOX[3] - BOX[1]) * Z), Image.NEAREST)


# face
tiles = []
for tag, nm in (("B", "before"), ("A", "after (stalk x1.25, bulb x1.2)")):
    for v in ("front", "tq"):
        tiles.append(lab(Image.open(os.path.join(R, "ey%s_%s.png" % (tag, v))).convert("RGB").resize((450, 450)),
                         "%s %s" % (nm, v)))
o = Image.new("RGB", (900, 900))
for i, t in enumerate(tiles):
    o.paste(t, ((i % 2) * 450, (i // 2) * 450))
titled(o, "Coral Crusher _eyes_r4_face.png - rendered %s (r4 eye stalks)" % time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(os.path.join(R, "eyA_front.png"))))).save(os.path.join(R, "_eyes_r4_face.png"))

# game 1x
F = (30, 41, 53, 62, 66)
W = (BOX[2] - BOX[0]) * Z
o = Image.new("RGB", (len(F) * W, 390 + W), (255, 255, 255))
for i, f in enumerate(F):
    p = os.path.join(R, "eyA_game_act_semaphore_%d.png" % f)
    full = Image.open(p).convert("RGB")
    d = ImageDraw.Draw(full)
    d.rectangle(BOX, outline=(255, 0, 0))
    full = lab(full, "game 1x (390 px) f%d %s" % (f, "top" if f in (30, 53) else "trough"))
    o.paste(full, (i * W + (W - 390) // 2, 0))
    o.paste(lab(crop(p), "eye box x%d f%d" % (Z, f)), (i * W, 390))
titled(o, "Coral Crusher _eyes_r4_game1x.png - rendered %s (after; red box = eye box, nearest-neighbour x4)" % STAMP).save(
    os.path.join(R, "_eyes_r4_game1x.png"))

# before vs after eye box
o = Image.new("RGB", (3 * W, 2 * W))
for i, f in enumerate((30, 41, 66)):
    o.paste(lab(crop(os.path.join(R, "eyB_game_act_semaphore_%d.png" % f)), "before f%d" % f), (i * W, 0))
    o.paste(lab(crop(os.path.join(R, "eyA_game_act_semaphore_%d.png" % f)), "after f%d" % f), (i * W, W))
titled(o, "Coral Crusher _eyes_r4_game_cmp.png - rendered %s (eye box x%d, game 1x)" % (STAMP, Z)).save(
    os.path.join(R, "_eyes_r4_game_cmp.png"))
print("sheets", STAMP)
