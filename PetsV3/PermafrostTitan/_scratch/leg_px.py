# blender -b --factory-startup --python PermafrostTitan/_scratch/leg_px.py -- <Name> <clip> <frame> [res=700]
# Fixed game camera (aimed at rest, like clip_views): px of the leg joints + the px bbox of the verts of each bone
# group (to see what hides what), and whether each lower-leg vert cluster is the FRONT-most surface (ray cast).
import sys, runpy, json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, fr = argv[0], argv[1], int(argv[2])
opts = dict(a.split("=", 1) for a in argv[3:] if "=" in a)
res = int(opts.get("res", "700"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from bpy_extras.object_utils import world_to_camera_view
pk = R3["pk"]
R3["full"](name, save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
k.set_action(clip)
sc.frame_set(0)
loc, tgt = pk.camera_for(k, "game")
pk.aim(sc.camera, loc, tgt)
sc.frame_set(fr)
bpy.context.view_layer.update()
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]
dg = bpy.context.evaluated_depsgraph_get()
ev = k.main.evaluated_get(dg)
me = ev.to_mesh()
mw = ev.matrix_world
W = [mw @ v.co for v in me.vertices]
bvh = BVHTree.FromPolygons(W, [list(p.vertices) for p in me.polygons])
pown = []
for pl in me.polygons:
    c = {}
    for i in pl.vertices:
        c[own[i]] = c.get(own[i], 0) + 1
    pown.append(max(c, key=c.get))
cam = sc.camera.matrix_world.to_translation()


def px(p):
    c = world_to_camera_view(sc, sc.camera, p)
    return (round(c.x * res, 1), round((1 - c.y) * res, 1))


out = {}
for grp in ("Shin_R", "Foot_R", "Shin_L", "Foot_L", "Knee_L", "Leg_R", "Leg_L"):
    ids = [i for i in range(len(W)) if own[i] == grp]
    if not ids:
        continue
    pp = [px(W[i]) for i in ids]
    vis = 0
    for i in ids:
        d = W[i] - cam
        h = bvh.ray_cast(cam, d.normalized(), d.length + 0.01)
        if h[0] is None or h[3] >= d.length - 0.004 or pown[h[2]] == grp:
            vis += 1
    out[grp] = {"x": [min(p[0] for p in pp), max(p[0] for p in pp)], "y": [min(p[1] for p in pp), max(p[1] for p in pp)],
                "visible_frac": round(vis / len(ids), 2)}
ev.to_mesh_clear()
print("LEGPX " + json.dumps(out))
