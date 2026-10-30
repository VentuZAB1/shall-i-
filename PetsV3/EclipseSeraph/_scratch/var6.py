# builder D scratch: middle-pair root variants -> static cut-throughs of wing poses (pose_cands.py), restores the module
import subprocess, json, sys, os
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
P = os.path.join(ROOT, "pets", "EclipseSeraph.py")
BL = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
orig = open(P, encoding="utf-8").read()
BOLD = '''WB, H2B, TB = make_wing("B", (0.235, -0.20, 1.10), (0.205, 0.12, 1.06), (0.82, -0.10, 1.16), (0.64, 0.42, 1.02),
                        (1.56, 0.28, 1.10), -4.0)'''
POLD = '''k.joint("Wing_%s_%s" % (P, side), X(wg.S, s), "Chest" if P != "C" else "Spine")'''
POSES = json.load(open(os.path.join(ROOT, "EclipseSeraph", "_scratch", "paths", "poses6.json")))
VARS = json.loads(sys.argv[1])          # label: [dy, dz, dx, parent]
try:
    for lab, (dy, dz, dx, par) in VARS.items():
        s = orig
        assert s.count(BOLD) == 1 and s.count(POLD) == 1
        f = lambda x, y, z: "(%.3f, %.3f, %.3f)" % (x + dx, y + dy, z + dz)
        s = s.replace(BOLD, 'WB, H2B, TB = make_wing("B", %s, %s, %s, %s,\n                        %s, -4.0)' % (
            f(0.235, -0.20, 1.10), f(0.205, 0.12, 1.06), f(0.82, -0.10, 1.16), f(0.64, 0.42, 1.02), f(1.56, 0.28, 1.10)))
        s = s.replace(POLD, 'k.joint("Wing_%%s_%%s" %% (P, side), X(wg.S, s), "Chest" if P == "A" or (P == "B" and "%s" == "Chest") else "Spine")' % par)
        open(P, "w", encoding="utf-8", newline="\n").write(s)
        r = subprocess.run([BL, "-b", "--factory-startup", "--python", os.path.join(ROOT, "EclipseSeraph", "_scratch", "pose_cands.py"),
                            "--", os.path.join(ROOT, "EclipseSeraph", "_scratch", "paths", "poses6.json"), "tq", "160"],
                           capture_output=True, text=True, cwd=ROOT)
        line = [l for l in r.stdout.splitlines() if l.startswith("CANDS")]
        d = json.loads(line[0][6:]) if line else {"err": r.stdout[-300:] + r.stderr[-300:]}
        print(lab, "|", json.dumps({kk: {p: n for p, n in v.items() if p.endswith("_L") or "_L|" in p or p.split("|")[0].endswith("_L")} for kk, v in d.items()} if "err" not in d else d), flush=True)
finally:
    open(P, "w", encoding="utf-8", newline="\n").write(orig)
