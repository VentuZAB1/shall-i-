# blender -b --factory-startup --python BrambleBadger/_scratch/act_lifts.py -- <out_dir>
# r6 MUST 2: act_burrow scoop / kick lift peaks at 2x side + 2x game cameras, with the paw's projected lift measured:
# P = the posed foot point (k.foot_world), P0 = the same x/y on the ground; px = |proj(P) - proj(P0)|.
import sys, runpy, os, json
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
out = sys.argv[sys.argv.index("--") + 1]
os.makedirs(out, exist_ok=True)
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"]("BrambleBadger", save=False)
k = R3["STATE"]["k"]
pk = R3["pk"]
import bpy
sc = bpy.context.scene
RES = 600
sc.render.resolution_x = sc.render.resolution_y = RES
# (frame, leg, label): the lift peaks (scoop +3 f, kick +3 f) and the dig-event sweeps
PICKS = [(11, "Leg_FL", "scoop 1 lift peak"), (16, "Leg_FL", "dig1 sweep"), (21, "Leg_FR", "scoop 2 lift peak"),
         (26, "Leg_FR", "dig2 sweep"), (31, "Leg_FL", "scoop 3 lift peak"), (36, "Leg_FL", "dig3 sweep"),
         (44, "Leg_BL", "kick 1 peak"), (53, "Leg_BR", "kick 2 peak")]
k.set_action("act_burrow")
def foot(leg):
    fb = "Foot_" + leg.split("_")[1]
    return k.arm.matrix_world @ k.arm.pose.bones[fb].head
sc.frame_set(0)
Z0 = {l: foot(l).z for l in ("Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR")}   # planted ankle height (act f0 = rest)
res = []
for f, leg, lab in PICKS:
    sc.frame_set(f)
    P = foot(leg)
    P0 = Vector((P.x, P.y, Z0[leg]))                     # the same ankle point at its planted height
    side = 1.0 if leg.endswith("L") else -1.0
    front = leg.startswith("Leg_F")
    views = {"side2x": (Vector((side, 0, 0.1)), 1.6, Vector((0, -0.30 if front else 0.30, 0.16))),
             "game2x": (Vector((0.45, 1.0, 0.85)), 1.9, Vector((0, -0.05, 0.12)))}
    row = {"f": f, "leg": leg, "label": lab, "ankle_lift": round(P.z - Z0[leg], 4)}
    for v, (d, dist, t) in views.items():
        pk.aim(sc.camera, t + d.normalized() * dist, t)
        bpy.context.view_layer.update()
        a = world_to_camera_view(sc, sc.camera, P)
        b = world_to_camera_view(sc, sc.camera, P0)
        pa = (a.x * RES, (1 - a.y) * RES)
        pb = (b.x * RES, (1 - b.y) * RES)
        cam = sc.camera.matrix_world.translation
        dg = bpy.context.evaluated_depsgraph_get()
        dv = P - cam
        hit, loc, nrm, idx, ob, mx = sc.ray_cast(dg, cam, dv.normalized(), distance=dv.length - 0.02)
        row.setdefault("visible", {})[v] = (not hit) or (ob is not None and (loc - P).length < 0.04)
        row[v] = {"paw": [round(pa[0], 1), round(pa[1], 1)], "ground": [round(pb[0], 1), round(pb[1], 1)],
                  "lift_px": round(((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2) ** 0.5, 1)}
        p = os.path.join(out, "act_%s_%02d.png" % (v, f))
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
    res.append(row)
json.dump(res, open(os.path.join(out, "act_lifts.json"), "w"), indent=1)
print("ACTLIFTS " + json.dumps(res))
