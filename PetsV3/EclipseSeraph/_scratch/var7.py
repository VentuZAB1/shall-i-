# builder D scratch: generic string-replace variants (json {label: [[old, new], ...]}) -> portrait sat / white / red and
# game-camera red / gold; restores the module after
import subprocess, json, sys, os
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
P = os.path.join(ROOT, "pets", "EclipseSeraph.py")
BL = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
SCR = os.path.join(ROOT, "EclipseSeraph", "_scratch")
orig = open(P, encoding="utf-8").read()
VARS = json.load(open(sys.argv[1]))
try:
    for lab, pairs in VARS.items():
        s = orig
        for a, b in pairs:
            assert s.count(a) == 1, (lab, a)
            s = s.replace(a, b)
        open(P, "w", encoding="utf-8", newline="\n").write(s)
        for t in ("headless_pack.py", "game_raw.py"):
            subprocess.run([BL, "-b", "--factory-startup", "--python", os.path.join(ROOT, "_tools", t), "--", "EclipseSeraph"],
                           capture_output=True, cwd=ROOT)
        subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "pack_post.py"), "EclipseSeraph", "SolarLion,Griffin,CelestialDragon,Cvetibara,CosmicLeviathan"],
                       capture_output=True, cwd=ROOT)
        g = json.loads(subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "game_icon.py"), "EclipseSeraph", "CosmicLeviathan"],
                                      capture_output=True, text=True, cwd=ROOT).stdout)
        st = subprocess.run([sys.executable, os.path.join(SCR, "seraph_stats.py"), "EclipseSeraph"], capture_output=True, text=True,
                            cwd=ROOT).stdout.strip().splitlines()
        raw = subprocess.run([sys.executable, os.path.join(SCR, "raw_stats.py"), os.path.join(ROOT, "EclipseSeraph", "EclipseSeraph_portrait_raw.png"), "64"],
                             capture_output=True, text=True, cwd=ROOT).stdout.strip()
        cell = subprocess.run([sys.executable, os.path.join(SCR, "satcells.py"), os.path.join(ROOT, "EclipseSeraph", "renders", "_icons_strip_64.png"), "64"],
                              capture_output=True, text=True, cwd=ROOT).stdout.strip().splitlines()[0]
        print("==", lab, "| game gold", g["gold_px_game_64"], "|", " / ".join(x.split(": ", 1)[1] for x in st), "| RAW", raw.split(": ", 1)[1], "| CELL", cell.split(": ", 1)[1], flush=True)
finally:
    open(P, "w", encoding="utf-8", newline="\n").write(orig)
