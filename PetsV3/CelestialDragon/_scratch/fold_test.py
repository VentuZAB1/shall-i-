# blender -b --python fold_test.py -- <Name> "up,fwd,twist,tip;up,fwd,twist,tip;..." [tx,ty,tz dist]
# keys each fold variant on its own frame, renders side + back + tq per variant, prints wing collisions per variant
import sys, runpy, os, json
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
vs = [tuple(float(x) for x in v.split(",")) for v in argv[1].split(";")]
tgt = Vector([float(v) for v in argv[2].split(",")]) if len(argv) > 2 else Vector((0, 0.3, 0.9))
dist = float(argv[3]) if len(argv) > 3 else 5.0
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
pk, bk = R3["pk"], R3["blockkit"]
m = R3["spec"](name)
k = R3["new_pet"](m, name)
m.model(k)
m.rig(k)
k.build_rig()
n = len(vs) - 1
k.new_action("t", max(n, 1), False)
for f, (up, fwd, tw, tip) in enumerate(vs):
    m.WING.key(k, f, up, fwd, tw, tip)
    k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
if n == 0:
    m.WING.key(k, 1, *vs[0])
k.finish(loop=False)
pk.stage(k)
k.set_action("t")
pairs = [p for p in m.check_pairs() if "Wing" in p[0] or "Wing" in p[1]]
for f in range(len(vs)):
    rep = bk.overlap_report(k, pairs, step=1, joints=m.joints() if hasattr(m, "joints") else None, clips=["t"],
                            frames={"t": [f]})
    print("HEADLESS_RESULT", f, vs[f], {a: b[0] for a, b in rep.get("t", {}).items()})
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = 400
cam = sc.camera
D = {"tq": (0.8, -1.0, 0.35), "side": (1.0, 0.0, 0.1), "back": (-0.5, 1.0, 0.45)}
for f in range(len(vs)):
    sc.frame_set(f)
    for v in ("side", "back", "tq"):
        pk.aim(cam, tgt + Vector(D[v]).normalized() * dist, tgt)
        sc.render.filepath = os.path.join(k.dir, "_scratch", "fold_%d_%s.png" % (f, v))
        bpy.ops.render.render(write_still=True)
