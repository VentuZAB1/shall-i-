# blender -b --factory-startup --python _tools/fold_render.py -- <Name> up,fwd,twist,tip;up,fwd,twist,tip;...
import sys, runpy
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
cands = [tuple(float(v) for v in c.split(",")) for c in argv[1].split(";")]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
m = R3["spec"](name)
k = R3["new_pet"](m, name)
m.model(k)
m.rig(k)
k.build_rig()
k.new_action("foldview", len(cands), False)
for f, c in enumerate(cands):
    m.wings(k, f, *c)
R3["pk"].stage(k)
for f in range(len(cands)):
    R3["pk"].shots(k, "fold%d" % f, tuple(__import__("os").environ.get("FOLD_VIEWS", "tq,game").split(",")), 360,
                   frame=f, action="foldview")
print("FOLD_RENDER ok")
