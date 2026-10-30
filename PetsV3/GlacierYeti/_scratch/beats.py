# blender -b --factory-startup --python IceMammoth/_scratch/beats.py -- <Name> <views e.g. tq,side> <res> <clip:f,...> <tag> [shift_y] [zoom]
# Renders the key beats of the clips (model + rig + anim via run3.full, no save) with the camera target shifted
# forward by shift_y (so a raised trunk / horn stays in frame) and the distance scaled by zoom; writes a manifest
# <Name>/renders/_beats_<tag>.json for beats_sheet.py (labelled contact sheets, system Python + PIL).
import sys, runpy, os, json
argv = sys.argv[sys.argv.index("--") + 1:]
name, views, res, picks, tag = argv[0], argv[1].split(","), int(argv[2]), argv[3], argv[4]
shift_y = float(argv[5]) if len(argv) > 5 else -0.25
zoom = float(argv[6]) if len(argv) > 6 else 1.12
picks = [(t.split(":")[0], int(t.split(":")[1])) for t in picks.split(",")]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"](name, save=False)
k = R3["STATE"]["k"]
pk = R3["pk"]
import bpy
from mathutils import Vector
sc = bpy.context.scene
cam = sc.camera
sc.render.resolution_x = sc.render.resolution_y = res
man = {}
for v in views:
    k.set_action("idle")
    sc.frame_set(0)
    loc, c = pk.camera_for(k, v)
    tgt = c + Vector((0, shift_y, 0.08))
    pk.aim(cam, tgt + (loc - c) * zoom, tgt)
    files = []
    for act, f in picks:
        k.set_action(act)
        sc.frame_set(f)
        p = os.path.join(k.dir, "renders", "beat_%s_%s_%s_%03d.png" % (tag, v, act, f))
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        files.append(p)
    man[v] = files
out = os.path.join(k.dir, "renders", "_beats_%s.json" % tag)
json.dump({"picks": picks, "files": man, "res": res}, open(out, "w"))
print("BEATS " + out)
