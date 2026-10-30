# blender -b --factory-startup --python _tools/fold_pairs.py -- <Name> <up,fwd,twist,tip> [<up,fwd,twist,tip> ...]
# Per-pair cut-through counts of a wing3 flyer's wing pose(s) (which body part blocks a fold?).
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
poses = [tuple(float(v) for v in a.split(",")) for a in argv[1:]]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
m = R3["spec"](name)
k = R3["new_pet"](m, name)
m.model(k)
m.rig(k)
k.build_rig()
k.new_action("foldpairs", max(1, len(poses)), False)
for f, p in enumerate(poses):
    m.wings(k, f, *p)
pairs = [p for p in m.check_pairs() if "Wing" in p[0] or "Wing" in p[1]]
js = m.joints() if hasattr(m, "joints") else None
out = {}
for f, p in enumerate(poses):
    rep = R3["blockkit"].overlap_report(k, pairs, step=1, clips=["foldpairs"], frames={"foldpairs": [f]}, joints=js)
    out[str(p)] = {"%s|%s" % kk if isinstance(kk, tuple) else str(kk): v[0] for kk, v in
                   rep.get("foldpairs", {}).items() if v[0]}
print("FOLDPAIRS " + json.dumps(out))
