# blender -b --factory-startup --python CoralCrusher/_scratch/claw_try.py -- "label=side:lift,spread,fore,wrist,pinch[;side:...][;z:dz]|label2=..." [views=tq,front]
# pose test for the crab claw FK helper (claw()), collisions on the spec's check_pairs, renders pose_<view>_<label>_00
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
cands = []
for blk in argv[0].split("|"):
    label, spec = blk.split("=", 1)
    keys = []
    for tok in spec.split(";"):
        side, vals = tok.split(":")
        keys.append((side, [float(x) for x in vals.split(",")]))
    cands.append((label, keys))
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
views = opts.get("views", "tq,front").split(",")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
name = "CoralCrusher"
m = R3["spec"](name)
k = R3["new_pet"](m, name)
m.model(k)
m.rig(k)
k.build_rig()
pk, bk = R3["pk"], R3["blockkit"]
k.new_action("idle", 1, False)
for f in (0, 1):
    k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
k.finish(loop=False)
for label, keys in cands:
    k.new_action(label, 1, False)
    dz = 0.0
    for f in (0, 1):
        for side, v in keys:
            if side == "z":
                dz = v[0]
                continue
            m.claw(k, f, side, *v)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, dz))
    m.plant6(k, [0, 1])
    k.finish(loop=False)
rep = bk.overlap_report(k, m.check_pairs(), step=1, joints=m.joints())
pk.stage(k)
files = []
for v in views:
    files += pk.pose_renders(k, [(label, 0) for label, _ in cands], view=v, res=360)
print("HEADLESS_RESULT " + json.dumps({"collisions": {c: rep.get(c) for c, _ in cands}}))
