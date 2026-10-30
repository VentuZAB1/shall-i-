# builder D scratch: halo variants -> clearance (display pose) + game gold; edits pets/EclipseSeraph.py, restores after
import re, subprocess, json, sys, os
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
P = os.path.join(ROOT, "pets", "EclipseSeraph.py")
BL = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
orig = open(P, encoding="utf-8").read()
VARS = json.loads(sys.argv[1])
try:
    for lab, v in VARS.items():
        s = orig
        s = re.sub(r"^HALO_LIP = [\d.]+", "HALO_LIP = %.3f" % v["lip"], s, flags=re.M)
        s = re.sub(r"^HALO_R = [\d.]+", "HALO_R = %.3f" % v["R"], s, flags=re.M)
        s = re.sub(r"^HALO_C = HC \+ Vector\(\(0, [\d.]+, [\d.]+\)\)", "HALO_C = HC + Vector((0, %.3f, %.3f))" % (v["y"], v["z"]), s, flags=re.M)
        open(P, "w", encoding="utf-8").write(s)
        out = subprocess.run([BL, "-b", "--factory-startup", "--python", os.path.join(ROOT, "EclipseSeraph", "_scratch", "clearance.py"),
                              "--", "EclipseSeraph", "Halo", "idle", "0"], capture_output=True, text=True, cwd=ROOT).stdout
        line = [l for l in out.splitlines() if l.startswith("CLEAR")]
        print(lab, line[0][:200] if line else out[-500:], flush=True)
finally:
    open(P, "w", encoding="utf-8").write(orig)
