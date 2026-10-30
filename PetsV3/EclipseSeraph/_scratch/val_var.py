# builder D scratch: Seraph value variants -> raw portrait stats (edits pets/EclipseSeraph.py, restores after)
NL = chr(10)
import subprocess, json, sys, os
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
P = os.path.join(ROOT, "pets", "EclipseSeraph.py")
SCR = os.path.join(ROOT, "EclipseSeraph", "_scratch")
BL = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
orig = open(P, encoding="utf-8").read()
COV = "        feather(B, a + nrm * 0.018, end + nrm * 0.018, nrm, fw * 0.80, 0.032, "
R = {
    "cov_bc": [(COV + "MOON_IVORY, wb,", COV + "MOON_IVORY if rows3 else BODY_MID, wb,")],
    "sec_a": [("IVORY_D if rows3 else WING_LILAC, wb,", "WING_LILAC, wb,")],
    "deep": [("BODY_MID = (206, 160, 232)", "BODY_MID = (184, 128, 214)"),
             ("WING_LILAC = (214, 186, 236)", "WING_LILAC = (190, 150, 226)")],
    "obs": [("OBSID = (60, 60, 84)", "OBSID = (46, 46, 70)")],
    "a_lilac": [(COV + "MOON_IVORY if rows3 else BODY_MID, wb,", COV + "WING_LILAC if rows3 else BODY_MID, wb,"),
                ("nrm, 0.20, 0.03, MOON_IVORY, tb,", "nrm, 0.20, 0.03, WING_LILAC, tb,")],
}
VARS = json.loads(sys.argv[1])
try:
    for lab, keys in VARS.items():
        s = orig
        for key in keys:
            for a, b in R[key]:
                assert s.count(a) == 1, a
                s = s.replace(a, b)
        open(P, "w", encoding="utf-8", newline=NL).write(s)
        subprocess.run([BL, "-b", "--factory-startup", "--python", os.path.join(ROOT, "_tools", "headless_pack.py"), "--",
                        "EclipseSeraph"], capture_output=True, cwd=ROOT)
        out = subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "pack_post.py"), "EclipseSeraph", "SolarLion"],
                             capture_output=True, text=True, cwd=ROOT).stdout
        sh = json.loads(out)["shares_pct"]
        st = subprocess.run([sys.executable, os.path.join(SCR, "raw_stats.py"),
                             os.path.join(ROOT, "EclipseSeraph", "EclipseSeraph_portrait_raw.png"), "64"],
                            capture_output=True, text=True, cwd=ROOT).stdout.strip()
        print(lab, "|", st, "| tq", json.dumps(sh["tq"]), flush=True)
finally:
    open(P, "w", encoding="utf-8", newline=NL).write(orig)
