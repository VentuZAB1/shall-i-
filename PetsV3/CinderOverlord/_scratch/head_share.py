# blender -b --factory-startup --python CinderOverlord/_scratch/head_share.py -- <Name> [view=game] [clip=idle] [f=0]
# On the kit camera of `view` (as game_raw / portrait): the vertical pixel extent of the head group (Head, Jaw, Mouth,
# Crown_*) vs the whole figure, and vs the icon3 frame (1.16 x the larger bbox side) = the head + crown share of the icon.
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
view, clip, fr = opts.get("view", "game"), opts.get("clip", "idle"), int(opts.get("f", "0"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from bpy_extras.object_utils import world_to_camera_view
pk = R3["pk"]
R3["full"](name, save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = 512
k.set_action(clip)
sc.frame_set(fr)
loc, tgt = pk.camera_for(k, view)
pk.aim(sc.camera, loc, tgt)
bpy.context.view_layer.update()
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]
dg = bpy.context.evaluated_depsgraph_get()
ev = k.main.evaluated_get(dg)
me = ev.to_mesh()
mw = ev.matrix_world
HG = ("Head", "Jaw", "Mouth")
allp, headp = [], []
for i, v in enumerate(me.vertices):
    c = world_to_camera_view(sc, sc.camera, mw @ v.co)
    p = (c.x * 512, (1 - c.y) * 512)
    allp.append(p)
    if own[i] in HG or own[i].startswith("Crown_"):
        headp.append(p)
ev.to_mesh_clear()
W = max(p[0] for p in allp) - min(p[0] for p in allp)
H = max(p[1] for p in allp) - min(p[1] for p in allp)
hh = max(p[1] for p in headp) - min(p[1] for p in headp)
print("HEADSHARE " + json.dumps({"view": view, "clip": clip, "f": fr, "fig_w": round(W, 1), "fig_h": round(H, 1),
                                 "head_h": round(hh, 1), "head_of_figure_h": round(hh / H, 3),
                                 "head_of_icon_h": round(hh / (1.16 * max(W, H)), 3)}))
