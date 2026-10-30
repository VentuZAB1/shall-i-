# blender -b --factory-startup --python _tools/path_test.py -- <Name> "<f:up,fwd,twist,tip;f:...>|<path2>|..."
# Wing collisions along keyed wing3 transitions (bezier between keys, checked every frame) - wing pairs + Chest/Spine.
# (adapted from the Thunderbird reviewer's path_try.py, 2026-10-14)
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
m = R3["spec"](name)
k = R3["new_pet"](m, name)
m.model(k)
m.rig(k)
k.build_rig()
res = {}
pairs = [p for p in m.check_pairs() if "Wing" in p[0] or "Wing" in p[1]]
for w in ("Wing_L", "WingTip_L", "Wing_R", "WingTip_R"):
    for b in ("Chest", "Spine"):
        if (w, b) not in pairs:
            pairs.append((w, b))
js = m.joints() if hasattr(m, "joints") else None
for pi, path in enumerate(argv[1].split("|")):
    keys = []
    for kk in path.split(";"):
        f, c = kk.split(":")
        keys.append((int(f), tuple(float(v) for v in c.split(","))))
    n = keys[-1][0]
    act = "path%d" % pi
    k.new_action(act, n, False)
    for f, c in keys:
        m.wings(k, f, *c)
    k.bake_bezier_now()
    rep = R3["blockkit"].overlap_report(k, pairs, step=1, clips=[act], frames={act: list(range(0, n + 1))}, joints=js)
    hits = {"%s|%s" % kk if isinstance(kk, tuple) else str(kk): v for kk, v in rep.get(act, {}).items() if v[0]}
    res["P%d" % pi] = hits
print("PATH_RESULT " + json.dumps(res))
