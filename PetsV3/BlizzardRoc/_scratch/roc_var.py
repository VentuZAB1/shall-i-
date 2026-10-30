# builder D scratch: Roc value variants -> flat shares (edits pets/BlizzardRoc.py text, restores after)
import subprocess, json, sys
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
P = ROOT + r"\pets\BlizzardRoc.py"
BL = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
orig = open(P, encoding="utf-8").read()
R = {
 "neck": [('    neck_cape(B, n2a, n2b, 0.13, [(0.50, (-0.065, 0.0, 0.065))], "Neck2")',
           '    neck_cape(B, n2a, n2b, 0.13, [(0.50, (-0.065, 0.0, 0.065))], "Neck2", col=SNOW)'),
          ('    neck_cape(B, n1a, n1b, 0.155, [(0.85, (-0.09, -0.03, 0.03, 0.09)), (0.45, (-0.06, 0.06))], "Neck")',
           '    neck_cape(B, n1a, n1b, 0.155, [(0.85, (-0.09, -0.03, 0.03, 0.09))], "Neck", col=SNOW)\n'
           '    neck_cape(B, n1a, n1b, 0.155, [(0.45, (-0.06, 0.06))], "Neck")')],
 "prim": [("PBARS = [(CHAR, 0.11), (FROST_V, 0.17)]", "PBARS = [(CHAR, 0.11), (FROST_V, 0.17), (CHAR, 0.36)]"),
          ("0.25, 0.034, CHAR, wb, bars=PBARS)", "0.25, 0.034, STORM_GREY, wb, bars=PBARS)"),
          ("0.23, 0.034, CHAR, tb, bars=PBARS)", "0.23, 0.034, STORM_GREY, tb, bars=PBARS)")],
 "rump": [('B.add((0, 0.31, 0.62), (0.12, 0.11, 0.08), STORM_GREY, "Spine"', 'B.add((0, 0.31, 0.62), (0.12, 0.11, 0.08), SNOW, "Spine"'),
          ('B.seg(T[0], T[1], 0.13, 0.085, STORM_GREY, "Tail1"', 'B.seg(T[0], T[1], 0.13, 0.085, SNOW, "Tail1"'),
          ('(0.06, 0.085, 0.02), STORM_GREY, "Tail1",', '(0.06, 0.085, 0.02), SNOW, "Tail1",')],
}
VARS = json.loads(sys.argv[1])
res = {}
try:
    for lab, keys in VARS.items():
        s = orig
        for key in keys:
            for a, b in R[key]:
                assert s.count(a) == 1, a
                s = s.replace(a, b)
        open(P, "w", encoding="utf-8").write(s)
        subprocess.run([BL, "-b", "--factory-startup", "--python", ROOT + r"\_tools\headless_pack.py", "--", "BlizzardRoc"],
                       capture_output=True, cwd=ROOT)
        out = subprocess.run([sys.executable, ROOT + r"\_tools\pack_post.py", "BlizzardRoc", ""], capture_output=True,
                             text=True, cwd=ROOT).stdout
        sh = json.loads(out)["shares_pct"]
        res[lab] = {v: {c: sh[v].get(c) for c in ("SNOW", "STORM_GREY", "CHAR", "FROST_V")} for v in sh}
        print(lab, json.dumps(res[lab]), flush=True)
finally:
    open(P, "w", encoding="utf-8").write(orig)
