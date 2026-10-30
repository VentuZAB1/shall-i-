# builder D scratch: horn cross-section variants -> front horn width (px, crown_front at 400 px) + game gold counts
# python FrostcrownDragon/_scratch/horn_var.py '{"lab": [["old","new"],...], ...}'   (restores the module)
import subprocess, json, sys, os, colorsys, shutil
from PIL import Image
NL = chr(10)
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
P = os.path.join(ROOT, "pets", "FrostcrownDragon.py")
BL = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
R = os.path.join(ROOT, "FrostcrownDragon", "renders")
orig = open(P, encoding="utf-8").read()
VARS = json.loads(sys.argv[1])


def horn_width(png):
    im = Image.open(png).convert("RGB")
    W, H = im.size
    rows = []
    for y in range(H):
        n = 0
        for x in range(0, int(W * 0.40)):          # left horn only (the diadem points sit in the centre)
            r, g, b = im.getpixel((x, y))
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if 0.06 <= h <= 0.18 and s > 0.4 and v > 0.4:
                n += 1
        if n:
            rows.append(n)
    rows.sort()
    return (rows[len(rows) // 2] if rows else 0, rows[int(len(rows) * 0.9)] if rows else 0, sum(rows))


try:
    for lab, pairs in VARS.items():
        s = orig
        for a, b in pairs:
            assert s.count(a) == 1, (lab, a)
            s = s.replace(a, b)
        open(P, "w", encoding="utf-8", newline=NL).write(s)
        subprocess.run([BL, "-b", "--factory-startup", "--python", os.path.join(ROOT, "_tools", "headless_closeup.py"), "--",
                        "FrostcrownDragon", "0,-0.95,1.85", "1.8", "400", "front=0,-1,0.15", "hvx_"], capture_output=True, cwd=ROOT)
        shutil.copy(os.path.join(R, "hvx_front.png"), os.path.join(ROOT, "FrostcrownDragon", "_scratch", "hv", lab + "_front.png"))
        subprocess.run([BL, "-b", "--factory-startup", "--python", os.path.join(ROOT, "_tools", "game_raw.py"), "--", "FrostcrownDragon"], capture_output=True, cwd=ROOT)
        subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "game_icon.py"), "FrostcrownDragon", "ThunderRex"], capture_output=True, cwd=ROOT)
        out = subprocess.run([sys.executable, os.path.join(ROOT, "FrostcrownDragon", "_scratch", "goldcount.py"), os.path.join(ROOT, "FrostcrownDragon", "FrostcrownDragon_icon_game.png")],
                             capture_output=True, text=True, cwd=ROOT).stdout.strip().splitlines()[0]
        print("==", lab, "| front horn width median / p90 / area", horn_width(os.path.join(R, "hvx_front.png")), "|", out.split(" ", 2)[2][:200], flush=True)
finally:
    open(P, "w", encoding="utf-8", newline=NL).write(orig)
