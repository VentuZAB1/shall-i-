# blender -b --python _tools/style_probe.py -- <Name> <out_prefix> key=val ...  : render a pet with STYLE overrides
import sys, runpy, json, ast
argv = sys.argv[sys.argv.index("--") + 1:]
name, prefix = argv[0], argv[1]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
bk = R3["blockkit"]
for kv in argv[2:]:
    k_, v = kv.split("=")
    try:
        bk.STYLE[k_] = ast.literal_eval(v)
    except Exception:
        bk.STYLE[k_] = v
pk = R3["pk"]
m = R3["spec"](name)
k = R3["new_pet"](m, name)
info = m.model(k) or {}
pk.stage(k)
files = pk.shots(k, prefix, ("tq", "front"), 520)
print("HEADLESS_RESULT " + json.dumps({"files": files, **info}))
