# builder D scratch: halo variants -> game-camera gold px (edits pets/EclipseSeraph.py constants, restores after)
import re, subprocess, json, sys, shutil
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
P = ROOT + r"\pets\EclipseSeraph.py"
BL = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
orig = open(P, encoding="utf-8").read()
VARS = json.loads(sys.argv[1])
res = {}
try:
    for lab, v in VARS.items():
        s = orig
        s = re.sub(r"^HALO_TILT = [\d.]+", "HALO_TILT = %.1f" % v["tilt"], s, flags=re.M)
        s = re.sub(r"^HALO_LIP = [\d.]+", "HALO_LIP = %.3f" % v["lip"], s, flags=re.M)
        s = re.sub(r"^HALO_BAND = [\d.]+", "HALO_BAND = %.3f" % v["band"], s, flags=re.M)
        s = re.sub(r"^HALO_R = [\d.]+", "HALO_R = %.3f" % v["R"], s, flags=re.M)
        s = re.sub(r"^HALO_C = HC \+ Vector\(\(0, [\d.]+, [\d.]+\)\)", "HALO_C = HC + Vector((0, %.3f, %.3f))" % (v["y"], v["z"]), s, flags=re.M)
        open(P, "w", encoding="utf-8").write(s)
        subprocess.run([BL, "-b", "--factory-startup", "--python", ROOT + r"\_tools\game_raw.py", "--", "EclipseSeraph"],
                       capture_output=True, cwd=ROOT)
        out = subprocess.run([sys.executable, ROOT + r"\_tools\game_icon.py", "EclipseSeraph", ""], capture_output=True,
                             text=True, cwd=ROOT).stdout
        j = json.loads(out)
        shutil.copy(ROOT + r"\EclipseSeraph\EclipseSeraph_icon_game.png", ROOT + r"\EclipseSeraph\_scratch\var_%s.png" % lab)
        from PIL import Image
        import colorsys
        im = Image.open(ROOT + r"\EclipseSeraph\EclipseSeraph_icon_game.png").convert("RGBA").resize((64, 64), Image.LANCZOS)
        red = 0
        for r, g, b, a in im.getdata():
            if a < 128:
                continue
            h, s_, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if (h < 0.03 or h > 0.95) and s_ > 0.45 and v > 0.45:
                red += 1
        res[lab] = (j["gold_px_game_64"], j["gold_px_brief_counter"], "red", red)
        print(lab, res[lab], flush=True)
finally:
    open(P, "w", encoding="utf-8").write(orig)
print("VARS", json.dumps(res))
