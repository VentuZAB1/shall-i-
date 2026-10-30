# blender -b --factory-startup --python _tools/headless_full.py -- <Name> [act:frame,act:frame,...] [step] [export]
# Background-Blender version of the per-pet "full" pass: model + rig + all clips + audit, then the collision report
# (overlap_report with the spec's check_pairs / joints) and optional pose renders, printed as one JSON line.
# Pass "export" as the 4th argument to also bake + export C:\cdimp\<Name>.fbx (+ meta / portrait) like R3["export"].
import sys, runpy, json, os
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
picks = []
if len(argv) > 1 and argv[1] not in ("-", ""):
    for tok in argv[1].split(","):
        a, f = tok.split(":")
        picks.append((a, int(f)))
step = int(argv[2]) if len(argv) > 2 else 2
do_export = len(argv) > 3 and argv[3] == "export"
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
out = R3["full"](name, pose_picks=picks or None)
k, m = R3["STATE"]["k"], R3["STATE"]["m"]
rep = {}
if hasattr(m, "check_pairs"):
    js = m.joints() if hasattr(m, "joints") else None
    rep = R3["blockkit"].overlap_report(k, m.check_pairs(), step=step, joints=js)
# ground check: lowest point of the posed mesh per clip (parts sinking into the floor), sampled every 2 frames
import bpy
gmin = {}
for clip, (n, loop) in k.clips.items():
    k.set_action(clip)
    lo = (9.0, -1)
    for f in range(0, n + 1):                  # every frame (review: odd frames can dip)
        bpy.context.scene.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        ev = k.main.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        z = min((mw @ v.co).z for v in me.vertices)
        ev.to_mesh_clear()
        if z < lo[0]:
            lo = (round(z, 3), f)
    gmin[clip] = lo
k.set_action("idle")
out["ground_min_z"] = gmin           # [lowest z, frame]; below about -0.02 = something sinks into the ground
out["collisions"] = {c: v for c, v in rep.items() if v}
out["collision_free"] = not any(rep.values())
if do_export:
    info = R3["export"]()
    out["export"] = {"meta": info.get("meta"), "portrait": info.get("portrait")}
print("HEADLESS_RESULT " + json.dumps(out, default=str))
