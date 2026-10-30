# blender -b --factory-startup --python CinderOverlord/_scratch/portrait_pose.py -- <Name> <action> <frame>
#     [dir=1,-1.36,0.62] [res=512] [out=<Name>_portrait_alt.png]
#   or  ... -- <Name> jobs "action:frame:dx,dy,dz:out[:fac]|..." [res=512]   (fac = camera distance / size, kit 1.75)
# The kit portrait (petkit.portrait: transparent, glow swap, same lights, camera at the kit distance) from ANY clip
# frame and camera direction (dir default = the kit "tq" portrait direction). Output goes to <Name>/<out> (relative to
# the pet folder); the kit <Name>_portrait_raw.png is untouched.
import sys, runpy, os
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
if argv[1] == "jobs":
    jobs = [j.split(":") for j in argv[2].split("|") if j]
    rest = argv[3:]
else:
    o0 = dict(a.split("=", 1) for a in argv[3:] if "=" in a)
    jobs = [[argv[1], argv[2], o0.get("dir", "1,-1.36,0.62"), o0.get("out", name + "_portrait_alt.png")]]
    rest = argv[3:]
opts = dict(a.split("=", 1) for a in rest if "=" in a)
res = int(opts.get("res", "512"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
pk = R3["pk"]
R3["full"](name, save=False)
k = R3["STATE"]["k"]
real = k.name
kit_tq = pk.VIEWS["tq"]
orig_cf = pk.camera_for
for job in jobs:
    action, frame, dv, out = job[:4]
    fac = float(job[4]) if len(job) > 4 else 1.75          # camera distance / model size (kit portrait = 1.75)

    def cf(kk, view, dist=None, _f=fac):
        # aim at the POSED bounds (evaluated meshes at the current frame), distance = posed size x fac
        import bpy
        from mathutils import Vector
        dg = bpy.context.evaluated_depsgraph_get()
        lo, hi = Vector((9e9,) * 3), Vector((-9e9,) * 3)
        for o in kk.coll.objects:
            if o.type != "MESH" or o.hide_render:
                continue
            ev = o.evaluated_get(dg)
            me = ev.to_mesh()
            for v in me.vertices:
                w = ev.matrix_world @ v.co
                lo = Vector(map(min, lo, w))
                hi = Vector(map(max, hi, w))
            ev.to_mesh_clear()
        c = (lo + hi) / 2
        d = Vector(pk.VIEWS[view]).normalized() * max((hi - lo).length, 2.0) * _f
        return c + d, c
    pk.camera_for = cf
    pk.VIEWS["tq"] = tuple(float(v) for v in dv.split(","))
    k.name = "_pp_tmp_" + real              # pk.portrait writes <k.dir>/<k.name>_portrait_raw.png
    p = pk.portrait(k, res=res, action=action, frame=int(frame))
    k.name = real
    dst = out if os.path.isabs(out) else os.path.join(k.dir, out)
    os.replace(p, dst)
    print("PORTRAIT_POSE ok", action, frame, dv, dst)
pk.VIEWS["tq"] = kit_tq
pk.camera_for = orig_cf
