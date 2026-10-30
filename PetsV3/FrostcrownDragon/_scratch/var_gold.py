# builder D scratch: crown variants -> game-camera gold counts (game_raw + game_icon + goldcount), restores the module
import subprocess, json, sys, os
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
P = os.path.join(ROOT, "pets", "FrostcrownDragon.py")
BL = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
orig = open(P, encoding="utf-8").read()
VARS = json.load(open(sys.argv[1]))
try:
    for lab, pairs in VARS.items():
        s = orig
        for a, b in pairs:
            assert s.count(a) == 1, (lab, a)
            s = s.replace(a, b)
        open(P, "w", encoding="utf-8", newline="\n").write(s)
        subprocess.run([BL, "-b", "--factory-startup", "--python", os.path.join(ROOT, "_tools", "game_raw.py"), "--", "FrostcrownDragon"], capture_output=True, cwd=ROOT)
        subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "game_icon.py"), "FrostcrownDragon", "ThunderRex"], capture_output=True, cwd=ROOT)
        out = subprocess.run([sys.executable, os.path.join(ROOT, "FrostcrownDragon", "_scratch", "goldcount.py"), os.path.join(ROOT, "FrostcrownDragon", "FrostcrownDragon_icon_game.png")],
                             capture_output=True, text=True, cwd=ROOT).stdout.strip().splitlines()
        print("==", lab, "|", " || ".join(l.split(" ", 1)[1] for l in out[:2]), flush=True)
finally:
    open(P, "w", encoding="utf-8", newline="\n").write(orig)
