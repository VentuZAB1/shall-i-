# blender -b --factory-startup --python _tools/fold_search.py -- <Name> [grid]
# Searches the ground FOLD of a wing3 flyer: for each (up, fwd, twist, tip) candidate it poses the wings, counts real
# wing cut-throughs (blockkit.overlap_report with the spec's wing pairs + joints) and measures the folded wing
# envelope (from the Wing_*/WingTip_* vertex groups). Prints the best collision-free candidates as JSON.
import sys, runpy, json, itertools
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from mathutils import Vector
m = R3["spec"](name)
k = R3["new_pet"](m, name)
m.model(k)
m.rig(k)
k.build_rig()
import os
G = os.environ.get("FOLD_GRID")      # "ups;fwds;twists;tips" (comma lists) - default = the old flat-fold grid
if G:
    ups, fwds, twists, tips = ([float(v) for v in part.split(",")] for part in G.split(";"))
else:
    ups = [-50, -35, -20, -5, 10, 25, 40]
    fwds = [-24, -12, 0]
    twists = [0, -15]
    tips = [60, 100, 140, 170]
cands = list(itertools.product(ups, fwds, twists, tips))
k.new_action("foldsearch", len(cands), False)
for f, (u, fw, tw, tp) in enumerate(cands):
    m.wings(k, f, u, fw, tw, tp)
pairs = [p for p in m.check_pairs() if "Wing" in p[0] or "Wing" in p[1]]
js = m.joints() if hasattr(m, "joints") else None
body = k.main
groups = {g.index: g.name for g in body.vertex_groups}
wing_idx = {i for i, nm in groups.items() if nm.startswith("Wing")}
wverts = [v.index for v in body.data.vertices if any(g.group in wing_idx and g.weight > 0.5 for g in v.groups)]
rows = []
sc = bpy.context.scene
for f, c in enumerate(cands):
    rep = R3["blockkit"].overlap_report(k, pairs, step=1, clips=["foldsearch"], frames={"foldsearch": [f]}, joints=js)
    hits = sum(v[0] for v in rep.get("foldsearch", {}).values())
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    P = [mw @ me.vertices[i].co for i in wverts]
    ev.to_mesh_clear()
    xs = sorted(abs(p.x) for p in P)
    tipv = max(P, key=lambda p: p.y)
    lo = min(P, key=lambda p: p.z)
    rows.append({"c": c, "hits": hits, "maxz": round(max(p.z for p in P), 3), "minz": round(lo.z, 3),
                 "minzy": round(lo.y, 3),
                 "w": round(xs[-1], 3), "w90": round(xs[int(len(xs) * 0.9)], 3), "back": round(tipv.y, 3),
                 "backz": round(tipv.z, 3)})
ok = [r for r in rows if r["hits"] == 0]
if os.environ.get("FOLD_TAIL"):            # "y,z" of the tail tip: rank by wingtip-to-tail distance (+ width, floor)
    ty, tz = (float(v) for v in os.environ["FOLD_TAIL"].split(","))
    for r in ok:
        r["tail_d"] = round(((r["back"] - ty) ** 2 + (r["backz"] - tz) ** 2) ** 0.5, 3)
    ok.sort(key=lambda r: r["tail_d"] + max(0, r["w90"] - 0.50) * 2 + max(0, 0.12 - r["minz"]) * 4)
    print("FOLD_RESULT " + json.dumps({"n": len(rows), "free": len(ok), "best": ok[:12], "near": [],
                                       "all": rows if os.environ.get("FOLD_ALL") else []}))
    raise SystemExit
ok.sort(key=lambda r: (r["w"] + max(0, r["maxz"] - 1.7) * 2 + max(0, 0.25 - r["minz"]) * 3))
print("FOLD_RESULT " + json.dumps({"n": len(rows), "free": len(ok), "best": ok[:12],
                                   "near": sorted(rows, key=lambda r: r["hits"])[:5]}))
