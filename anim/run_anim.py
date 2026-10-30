"""Build animation clips for creatures (parallel Blender runs) + preview sheets.
python run_anim.py [--preview] [only=walk,idle] [names...]     (no names = all creatures)"""
import os, subprocess, sys, glob
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rig"))
sys.path.insert(0, HERE)
from creatures import RIG
from profiles import CREATURE, roblox_name

BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
preview = "--preview" in sys.argv
extra = []
for a in sys.argv[1:]:
    if a.startswith("only="):
        os.environ["ANIM_ONLY"] = a[5:]
names = [a for a in sys.argv[1:] if not a.startswith("--") and "=" not in a] or [n for n in RIG if n in CREATURE]


def run(name):
    typ, opts = RIG[name]
    args = [BLENDER, "-b", "-P", os.path.join(HERE, "..", "rig", "rigger.py"), "-P", os.path.join(HERE, "author.py"),
            "--", name, typ] + [f"{k}={v}" for k, v in opts.items()] + extra + (["--preview"] if preview else [])
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    info = [l for l in r.stdout.splitlines() if l.startswith(("LEGS", "CLIP", "CALM", "LEAN"))]
    err = [l for l in (r.stdout + r.stderr).splitlines() if "Error" in l or "Traceback" in l or l.startswith("  File")]
    return name, info, err


with ThreadPoolExecutor(6) as ex:
    for name, info, err in ex.map(run, names):
        print(name, "|", " ; ".join([i for i in info if not i.startswith("CLIP")]))
        if err:
            print("   ERR", "\n   ".join(err[-6:]))

if preview:
    from PIL import Image, ImageDraw
    for name in names:
        rn = roblox_name(name)
        fdir = os.path.join(HERE, "preview", "_frames", rn)
        files = glob.glob(os.path.join(fdir, "*.png"))
        rows = {}
        for f in files:
            clip, view, j = os.path.basename(f)[:-4].rsplit("_", 2)
            rows.setdefault((clip, view), {})[int(j)] = f
        order = sorted(rows, key=lambda k: (["idle", "walk", "slither", "swim", "fly", "glide", "takeoff", "land", "roar"].index(k[0]) if k[0] in ["idle", "walk", "slither", "swim", "fly", "glide", "takeoff", "land", "roar"] else 20, k[0], k[1]))
        tw, th = 200, 173
        sheet = Image.new("RGB", (tw * 8 + 90, th * len(order)), (25, 25, 30))
        d = ImageDraw.Draw(sheet)
        for r, key in enumerate(order):
            d.text((4, r * th + th // 2), f"{key[0]}\n{key[1]}", fill=(255, 230, 0))
            for j, f in sorted(rows[key].items()):
                sheet.paste(Image.open(f).convert("RGB").resize((tw, th)), (90 + j * tw, r * th))
        os.makedirs(os.path.join(HERE, "preview"), exist_ok=True)
        sheet.save(os.path.join(HERE, "preview", rn + ".png"))
    print("sheets in", os.path.join(HERE, "preview"))
