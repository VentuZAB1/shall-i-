# builder D scratch: Dragon value variants -> portrait icon stats (edits pets/FrostcrownDragon.py, restores after)
NL = chr(10)
import subprocess, json, sys
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
P = ROOT + r"\pets\FrostcrownDragon.py"
BL = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
orig = open(P, encoding="utf-8").read()
R = {
 "arms": [('    B.seg(S, W, 0.07, 0.075, STEEL_BLUE, wb, side=(0, 0, 1), ext=0.10, role="limb", top=(0.8, 0.8))\n    B.add(W, (0.08, 0.08, 0.08), STEEL_BLUE, wb, role="limb")',
           '    B.seg(S, W, 0.07, 0.075, DEEP_STEEL, wb, side=(0, 0, 1), ext=0.10, role="limb", top=(0.8, 0.8))\n    B.add(W, (0.08, 0.08, 0.08), DEEP_STEEL, wb, role="limb")')],
 "memb": [("MEMBRANE = (116, 146, 206)", "MEMBRANE = (100, 130, 196)")],
 "base": [],
 "throat5": [("ICE_THROAT = (210, 226, 246)", "ICE_THROAT = (224, 236, 252)")],
 "claw5": [("(0, -1, -0.62), 0.08, 0.016, ICE_W, foot)", "(0, -1, -0.62), 0.09, 0.019, ICE_W, foot)")],
 "belly4": [("ICE_BELLY = (196, 214, 240)", "ICE_BELLY = (204, 220, 244)")],
 "throat4": [("ICE_THROAT = (210, 226, 246)", "ICE_THROAT = (218, 232, 250)")],
 "facw": [("        B.poly(q2, 0.008, ICE_THROAT, bone)", "        B.poly(q2, 0.008, ICE_W, bone)")],
 "chestp": [('B.add((0, -0.36, 0.595), (0.14, 0.21, 0.026), ICE_BELLY, "Chest"', 'B.add((0, -0.36, 0.595), (0.14, 0.21, 0.026), ICE_THROAT, "Chest"')],
 "fac2": [("q2 = [c2.lerp(p, 0.30)", "q2 = [c2.lerp(p, 0.42)")],
 "trimw": [("def trim_band(B, blks, y, zs, bone, w=0.018):", "def trim_band(B, blks, y, zs, bone, w=0.026):")],
 "memb3": [("MEMBRANE = (86, 112, 184)", "MEMBRANE = (78, 102, 174)")],
 "dark3": [("DARK = (54, 60, 94)", "DARK = (46, 52, 84)")],
 "belly3": [("ICE_BELLY = (196, 214, 240)", "ICE_BELLY = (190, 208, 236)")],
 "finf": [("        B.poly(q, 0.008, ICE_BELLY, bone)", "        B.poly(q, 0.008, ICE_THROAT, bone)")],
 "tailt": [('B.spike(main - tipd * 0.02, Vector((0, 0.45, 0.9)), 0.17, 0.04, ICE_BELLY, "Tail_Tip"', 'B.spike(main - tipd * 0.02, Vector((0, 0.45, 0.9)), 0.17, 0.04, ICE_THROAT, "Tail_Tip"')],
 "lips": [("0.084, 0.02, ICE_BELLY, \"Head\",", "0.084, 0.02, ICE_THROAT, \"Head\","), ("0.06, 0.012, ICE_BELLY, \"Jaw\",", "0.06, 0.012, ICE_THROAT, \"Jaw\",")],
 "belly": [("ICE_BELLY = (210, 226, 246)", "ICE_BELLY = (196, 214, 240)")],
 "d1": [("DARK = (66, 72, 108)", "DARK = (54, 60, 94)")],
 "d2": [("DARK = (66, 72, 108)", "DARK = (46, 52, 86)")],
 "m1": [("MEMBRANE = (100, 130, 196)", "MEMBRANE = (92, 120, 190)")],
 "m2": [("MEMBRANE = (100, 130, 196)", "MEMBRANE = (86, 112, 184)")],
 "trim": [("B.bar(a, b, nrm, 0.042, 0.022, DARK, bone, studs=[], bevel=0.007, nostud=True)", "B.bar(a, b, nrm, 0.06, 0.022, DARK, bone, studs=[], bevel=0.007, nostud=True)"),
          ("for f, w in ((f1, 0.052), (f2, 0.046), (f3, 0.042)):", "for f, w in ((f1, 0.062), (f2, 0.056), (f3, 0.052)):"),
          ("hw * 1.25, 0.06, DEEP_STEEL, bone", "hw * 1.5, 0.06, DEEP_STEEL, bone")],
 "legs": [("B.seg(K, A, 0.082, 0.088, STEEL_BLUE, shin,", "B.seg(K, A, 0.082, 0.088, DEEP_STEEL, shin,"),
          ("B.seg(K, A, 0.078, 0.088, STEEL_BLUE, shin,", "B.seg(K, A, 0.078, 0.088, DEEP_STEEL, shin,"),
          ("B.seg(A, P + Vector((0, 0.03, 0.03)), 0.064, 0.068, STEEL_BLUE, foot, ext=0.03)", "B.seg(A, P + Vector((0, 0.03, 0.03)), 0.064, 0.068, DEEP_STEEL, foot, ext=0.03)"),
          ("B.add(P, (0.095, 0.11, 0.05), STEEL_BLUE, foot, top=(0.85, 0.80))", "B.add(P, (0.095, 0.11, 0.05), DEEP_STEEL, foot, top=(0.85, 0.80))")],
 "shells": [("sh_rib = shell(B, rib, -0.40, 0.40, 0.08, DEEP_STEEL)", "sh_rib = shell(B, rib, -0.40, 0.40, -0.06, DEEP_STEEL)"),
            ("sh_waist = shell(B, waist, -0.26, 0.26, 0.02, DEEP_STEEL)", "sh_waist = shell(B, waist, -0.26, 0.26, -0.08, DEEP_STEEL)"),
            ("sh_hips = shell(B, hips, -0.24, 0.24, 0.0, DEEP_STEEL)", "sh_hips = shell(B, hips, -0.24, 0.24, -0.10, DEEP_STEEL)")],
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
        subprocess.run([BL, "-b", "--factory-startup", "--python", ROOT + r"\_tools\headless_pack.py", "--", "FrostcrownDragon"],
                       capture_output=True, cwd=ROOT)
        out = subprocess.run([sys.executable, ROOT + r"\_tools\pack_post.py", "FrostcrownDragon", "ThunderRex,CosmicLeviathan"],
                             capture_output=True, text=True, cwd=ROOT).stdout
        sh = json.loads(out)["shares_pct"]
        st = subprocess.run([sys.executable, ROOT + r"\FrostcrownDragon\_scratch\iconstats.py", "FrostcrownDragon"],
                            capture_output=True, text=True, cwd=ROOT).stdout.strip()
        ss = subprocess.run([sys.executable, ROOT + r"\FrostcrownDragon\_scratch\stripstats.py",
                             ROOT + r"\FrostcrownDragon\renders\_icons_strip_128.png", "128"],
                            capture_output=True, text=True, cwd=ROOT).stdout.strip().splitlines()[0]
        print(lab, "|", st, "|", ss, "| tq", json.dumps(sh["tq"]), flush=True)
finally:
    open(P, "w", encoding="utf-8", newline=NL).write(orig)
