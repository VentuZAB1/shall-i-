# blender -b --factory-startup --python CinderOverlord/_scratch/paw_px.py -- CinderOverlord [clip:frame]
# r10 MUST 1a pass check: how far each paw (Claw_L / Claw_R group) sticks out past the body outline (every other
# vertex group) on the fixed GAME camera (the gamelook_game.png framing, idle f0), measured per 3-px image row band
# and converted to BU along the camera's screen-right axis at the paw's depth. Also the frill tips past the skull side
# in the TOP view (BU, world x).
import sys, runpy, json
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
pick = argv[1] if len(argv) > 1 else "idle:0"
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from bpy_extras.object_utils import world_to_camera_view
R3["full"](name, save=False)
k = R3["STATE"]["k"]
pk = R3["pk"]
sc = bpy.context.scene
RES = 600
sc.render.resolution_x = sc.render.resolution_y = RES
k.set_action("idle")
sc.frame_set(0)
loc, tgt = pk.camera_for(k, "game")
pk.aim(sc.camera, loc, tgt)
clip, fr = pick.split(":")
k.set_action(clip)
sc.frame_set(int(fr))
bpy.context.view_layer.update()
cam = sc.camera
dg = bpy.context.evaluated_depsgraph_get()
ev = k.main.evaluated_get(dg)
me = ev.to_mesh()
mw = ev.matrix_world
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]
W = [mw @ v.co for v in me.vertices]
P = [world_to_camera_view(sc, cam, p) for p in W]
right = (cam.matrix_world.to_quaternion() @ Vector((1, 0, 0))).normalized()
res = {}
BAND = 3
body = {}
for i, q in enumerate(P):
    if own[i].startswith(("Claw_", "Arm_")):
        continue
    b = int((1 - q.y) * RES) // BAND
    x = q.x * RES
    lo, hi = body.get(b, (1e9, -1e9))
    body[b] = (min(lo, x), max(hi, x))
for side in ("L", "R"):
    ids = [i for i in range(len(W)) if own[i] == "Claw_" + side]
    c = sum((W[i] for i in ids), Vector()) / len(ids)
    p0 = world_to_camera_view(sc, cam, c)
    p1 = world_to_camera_view(sc, cam, c + right * 0.10)
    px_per_bu = abs(p1.x - p0.x) * RES / 0.10
    best_l, best_r = 0.0, 0.0
    for i in ids:
        q = P[i]
        b = int((1 - q.y) * RES) // BAND
        x = q.x * RES
        lo, hi = body.get(b, (1e9, -1e9))
        if lo > 1e8:
            continue
        best_l = max(best_l, lo - x)
        best_r = max(best_r, x - hi)
    res[side] = {"out_left_px": round(best_l, 1), "out_right_px": round(best_r, 1), "px_per_bu": round(px_per_bu, 1),
                 "out_left_bu": round(best_l / px_per_bu, 3), "out_right_bu": round(best_r / px_per_bu, 3),
                 "centre_px": [round(p0.x * RES), round((1 - p0.y) * RES)]}
# top view: frill tips past the skull side (world x), skull = Head-group verts of the lofted skull only is not
# separable here, so the skull side is taken as the widest Head vertex inside y [-0.70, -0.55] at the eye / brow band
# excluding spikes would need part ids; report the Head group's |x| extent per y band instead.
hx = {}
for i, p in enumerate(W):
    if own[i] == "Head":
        b = round(p.y, 1)
        hx[b] = max(hx.get(b, 0.0), abs(p.x))
res["head_absx_by_y"] = dict(sorted(hx.items()))
ev.to_mesh_clear()
print("PAWPX " + json.dumps(res))
