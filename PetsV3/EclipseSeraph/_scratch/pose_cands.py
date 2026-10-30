# blender -b --factory-startup --python EclipseSeraph/_scratch/pose_cands.py -- <json file> [views] [res]
# (builder D scratch) six-wing display-pose candidates: json = {"label": {"A": [up,fwd,twist,tip], "B": [...], ...}}
# renders renders/cand_<label>_<view>.png and prints the wing-vs-wing / wing-vs-body cut-throughs per candidate.
import sys, runpy, os, json
argv = sys.argv[sys.argv.index("--") + 1:]
cands = json.load(open(argv[0]))
views = argv[1].split(",") if len(argv) > 1 else ["tq", "front"]
res = int(argv[2]) if len(argv) > 2 else 420
name = "EclipseSeraph"
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
m = R3["spec"](name)
k = R3["new_pet"](m, name)
m.model(k)
m.rig(k)
k.build_rig()
pk = R3["pk"]
labels = list(cands)
for lab in labels:
    k.new_action("c_" + lab, 2, False)
    for f in (0, 2):
        for P, w in cands[lab].items():
            m.wings(k, f, P, *w)
    k.finish(loop=False)
pk.stage(k)
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
pairs = m.check_pairs() if hasattr(m, "check_pairs") else []
js = m.joints() if hasattr(m, "joints") else None
out = {}
for lab in labels:
    k.set_action("c_" + lab)
    sc.frame_set(0)
    for v in views:
        loc, tgt = pk.camera_for(k, v)
        pk.aim(sc.camera, loc, tgt)
        sc.render.filepath = os.path.join(k.dir, "renders", "cand_%s_%s.png" % (lab, v))
        bpy.ops.render.render(write_still=True)
    if pairs:
        rep = R3["blockkit"].overlap_report(k, pairs, step=1, clips=["c_" + lab], frames={"c_" + lab: [0]}, joints=js)
        out[lab] = {kk: v[0] for kk, v in rep.get("c_" + lab, {}).items() if v[0]}
print("CANDS " + json.dumps(out))
