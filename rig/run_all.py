"""Rig every creature in creatures.RIG (parallel Blender runs) and build a review sheet.
python run_all.py [--export] [names...]"""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from creatures import RIG

BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
HERE = os.path.dirname(os.path.abspath(__file__))
export = "--export" in sys.argv
names = [a for a in sys.argv[1:] if not a.startswith("--")] or list(RIG)


def run(name):
    typ, opts = RIG[name]
    args = [BLENDER, "-b", "-P", os.path.join(HERE, "rigger.py"), "--", name, typ]
    args += [f"{k}={v}" for k, v in opts.items()]
    args += ["--export"] if export else ["--pose"]
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    info = [l for l in r.stdout.splitlines() if l.startswith(("RIG", "EXPORTED"))]
    err = [l for l in (r.stdout + r.stderr).splitlines() if "Error" in l or "Traceback" in l]
    return name, info, err


with ThreadPoolExecutor(5) as ex:
    for name, info, err in ex.map(run, names):
        print(name, "|", " ".join(info), "|", " ".join(err[:2]))

if not export:
    from PIL import Image, ImageDraw
    tiles = []
    for n in names:
        row = []
        for k in ("00", "10", "11"):
            p = os.path.join(HERE, "out", f"_{n}_{k}.png")
            if os.path.exists(p):
                row.append(Image.open(p).convert("RGB").resize((240, 200)))
        tiles.append((n, row))
    per = 10
    for s in range(0, len(tiles), per):
        chunk = tiles[s:s + per]
        sheet = Image.new("RGB", (720 * 2, 215 * ((len(chunk) + 1) // 2)), (20, 20, 25))
        d = ImageDraw.Draw(sheet)
        for i, (n, row) in enumerate(chunk):
            x, y = (i % 2) * 720, (i // 2) * 215
            for j, im in enumerate(row):
                sheet.paste(im, (x + j * 240, y + 15))
            d.text((x + 4, y + 2), n, fill=(255, 255, 0))
        sheet.save(os.path.join(HERE, "out", f"review{s // per}.png"))
    print("sheets done")
