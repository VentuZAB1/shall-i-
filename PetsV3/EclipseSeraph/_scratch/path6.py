# blender -b --factory-startup --python EclipseSeraph/_scratch/path6.py -- <paths.json>
# (builder D scratch) six-wing transitions: json = {"label": [[f, {"A": [up,fwd,twist,tip], "B": [...], "C": [...],
# "Spine": [p,y,r(,x,y,z)], ...}], ...]} -> bezier-baked, every frame checked against the spec's check_pairs() + joints.
# Prints PATH6 {"label": {"A|B": [hits, first_frame]}}.
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
paths = json.load(open(argv[0]))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
m = R3["spec"]("EclipseSeraph")
k = R3["new_pet"](m, "EclipseSeraph")
m.model(k)
m.rig(k)
k.build_rig()
pairs = m.check_pairs()
js = m.joints()
res = {}
for lab, keys in paths.items():
    n = keys[-1][0]
    act = "p_" + lab
    k.new_action(act, n, False)
    for f, d in keys:
        for b, v in d.items():
            if b in ("A", "B", "C"):
                m.wings(k, f, b, *v)
            elif len(v) >= 6:
                k.key(b, f, rot=tuple(v[:3]), loc=tuple(v[3:6]))
            else:
                k.key(b, f, rot=tuple(v[:3]))
    k.bake_bezier_now()
    rep = R3["blockkit"].overlap_report(k, pairs, step=1, clips=[act], frames={act: list(range(0, n + 1))}, joints=js)
    res[lab] = {"%s|%s" % kk if isinstance(kk, tuple) else str(kk): v for kk, v in rep.get(act, {}).items() if v[0]}
print("PATH6 " + json.dumps(res))
