# blender -b --factory-startup --python _tools/headless_model.py -- <Name> [views] [res]
# Builds a pet's model with run3 in a background Blender and renders review views (no MCP, so it can run in parallel).
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
views = tuple(argv[1].split(";" if "=" in argv[1] else ",")) if len(argv) > 1 else ("tq", "front", "side", "back")
res = int(argv[2]) if len(argv) > 2 else 520
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
for v in [v for v in views if "=" in v]:          # custom camera directions: "top=0,0.02,1;game;belly=0.3,-0.6,-0.5"
    nm, d = v.split("=")
    R3["pk"].VIEWS[nm] = tuple(float(x) for x in d.split(","))
views = tuple(v.split("=")[0] for v in views)
out = R3["model"](name, views=views, res=res)
print("HEADLESS_RESULT " + json.dumps(out))
