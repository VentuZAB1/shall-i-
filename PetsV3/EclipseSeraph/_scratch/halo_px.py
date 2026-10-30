# blender -b --factory-startup --python EclipseSeraph/_scratch/halo_px.py -- clip <clip> <f0> <f1> <step>
# blender -b --factory-startup --python EclipseSeraph/_scratch/halo_px.py -- cands <json>
# (builder D scratch) area-true halo occlusion from the GAME camera: gold px of the full render vs gold px of a render
# of the halo alone (the posed mesh with every non-Halo vertex deleted), 300 px -> _scratch/$HP_DIR/<tag>_full|alone.png;
# then: python EclipseSeraph/_scratch/halo_count.py <dir>
import sys, runpy, os, json, colorsys
argv = sys.argv[sys.argv.index("--") + 1:]
mode = argv[0]
name = "EclipseSeraph"
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy, bmesh
pk = R3["pk"]
if mode == "clip":
    R3["full"](name, save=False)
    k = R3["STATE"]["k"]
    m = None
    jobs = [(argv[1], f) for f in range(int(argv[2]), int(argv[3]) + 1, int(argv[4]))]
else:
    cands = json.load(open(argv[1]))
    m = R3["spec"](name)
    k = R3["new_pet"](m, name)
    m.model(k)
    m.rig(k)
    k.build_rig()
    for lab in cands:
        k.new_action("c_" + lab, 2, False)
        for f in (0, 2):
            for P, w in cands[lab].items():
                m.wings(k, f, P, *w)
        k.finish(loop=False)
    jobs = [("c_" + lab, 0) for lab in cands]
pk.stage(k)
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = 300
body = k.main
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
OUTD = os.path.join(k.dir, "_scratch", os.environ.get("HP_DIR", "hp"))
os.makedirs(OUTD, exist_ok=True)


def gold_px(path):
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return path


sc.render.film_transparent = True
out = {}
for clip, f in jobs:
    k.set_action(clip)
    sc.frame_set(f)
    loc, tgt = pk.camera_for(k, "game")
    pk.aim(sc.camera, loc, tgt)
    tag = "%s_%d" % (clip, f)
    full = gold_px(os.path.join(OUTD, tag + "_full.png"))
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev)
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if owner[v.index] != "Halo"], context="VERTS")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("_halo_only", me)
    ob.matrix_world = body.matrix_world.copy()
    sc.collection.objects.link(ob)
    hide = [o for o in sc.objects if o.type == "MESH" and o is not ob and not o.hide_render and o.name != "Ground"]
    for o in hide:
        o.hide_render = True
    alone = gold_px(os.path.join(OUTD, tag + "_alone.png"))
    for o in hide:
        o.hide_render = False
    bpy.data.objects.remove(ob)
    bpy.data.meshes.remove(me)
    out[tag] = 1
print("HALO_PX " + json.dumps(out))
