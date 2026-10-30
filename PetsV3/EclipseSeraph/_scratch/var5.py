# builder D scratch: tail-brush variants -> game-camera gold / red (game_raw + game_icon), restores the module after
NL = chr(10)
import subprocess, json, sys, os
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
P = os.path.join(ROOT, "pets", "EclipseSeraph.py")
BL = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
orig = open(P, encoding="utf-8").read()
BLK = "(0.10, 0.11, 0.095), BLOOD, \"Tail4\""
TUF = "tuft(B, tip + Vector((0, 0.02, -0.01)), d, L, 0.07, BLOOD, \"Tail4\")"
LEN = "(((0, 0.5, -0.8), 0.23), ((0.5, 0.4, -0.7), 0.19), ((-0.5, 0.4, -0.7), 0.19), ((0, 0.9, -0.2), 0.20),\n                 ((0, 0.1, -1.0), 0.20))"
R = {"base": [],
     "w085": [(TUF, TUF.replace("0.07,", "0.085,"))],
     "w08": [(TUF, TUF.replace("0.07,", "0.08,"))],
     "up": [(LEN, LEN.replace("((0, 0.1, -1.0), 0.20))", "((0, 0.1, -1.0), 0.20), ((0, 0.8, 0.5), 0.18))"))],
     "up2": [(LEN, LEN.replace("((0, 0.1, -1.0), 0.20))", "((0, 0.1, -1.0), 0.20), ((0.45, 0.8, 0.35), 0.17), ((-0.45, 0.8, 0.35), 0.17))"))],
     "rim95": [("rim_o, rim_i = HALO_R, HALO_R - 0.085", "rim_o, rim_i = HALO_R, HALO_R - 0.095")],
     "rim10": [("rim_o, rim_i = HALO_R, HALO_R - 0.085", "rim_o, rim_i = HALO_R, HALO_R - 0.100")],
     "lip66": [("HALO_LIP = 0.060", "HALO_LIP = 0.066")],
     "t09": [("HALO_T = 0.08 ", "HALO_T = 0.09 ")],
     "c10": [('"C": (10.0, -4.0, 0.0, -6.0)}   # clips', '"C": (10.0, -10.0, 0.0, -6.0)}   # clips')],
     "blk11": [(BLK, "(0.11, 0.12, 0.10), BLOOD, \"Tail4\"")],
     "short": [(LEN, "(((0, 0.5, -0.8), 0.21), ((0.5, 0.4, -0.7), 0.17), ((-0.5, 0.4, -0.7), 0.17), ((0, 0.9, -0.2), 0.18),\n                 ((0, 0.1, -1.0), 0.18))")]}
VARS = json.loads(sys.argv[1])
try:
    for lab, keys in VARS.items():
        s = orig
        for key in keys:
            for a, b in R[key]:
                assert s.count(a) == 1, a
                s = s.replace(a, b)
        open(P, "w", encoding="utf-8", newline=NL).write(s)
        subprocess.run([BL, "-b", "--factory-startup", "--python", os.path.join(ROOT, "_tools", "game_raw.py"), "--",
                        "EclipseSeraph"], capture_output=True, cwd=ROOT)
        g = subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "game_icon.py"), "EclipseSeraph", "CosmicLeviathan"],
                           capture_output=True, text=True, cwd=ROOT).stdout
        d = json.loads(g)
        st = subprocess.run([sys.executable, os.path.join(ROOT, "EclipseSeraph", "_scratch", "seraph_stats.py"), "EclipseSeraph"],
                            capture_output=True, text=True, cwd=ROOT).stdout.strip().splitlines()[-1]
        print(lab, "| game gold strict", d["gold_px_game_64"], "brief", d["gold_px_brief_counter"][1], "|", st, flush=True)
finally:
    open(P, "w", encoding="utf-8", newline=NL).write(orig)
