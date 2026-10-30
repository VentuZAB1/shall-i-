# r10: does arm_search.py measure from the real game camera? pk.aim sets cam.location, but matrix_world is only
# refreshed by a depsgraph update; arm_search reads matrix_world right after aim (no update).
import sys, runpy, json
from mathutils import Vector
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
pk = R3["pk"]
R3["full"]("PermafrostTitan", save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
k.set_action("act_kneelrise")
sc.frame_set(0)
loc, tgt = pk.camera_for(k, "game")
pre = sc.camera.matrix_world.to_translation().copy()
pk.aim(sc.camera, loc, tgt)
stale = sc.camera.matrix_world.to_translation().copy()
bpy.context.view_layer.update()
fresh = sc.camera.matrix_world.to_translation().copy()
r = lambda v: [round(x, 3) for x in v]
c = (Vector(loc) - Vector(tgt)).normalized()
s = (stale - Vector(tgt)).normalized()
import math
print("CAMCHECK " + json.dumps({"camera_for_loc": r(loc), "target": r(tgt), "arm_search_cam(stale)": r(stale),
      "after_update": r(fresh), "angle_between_deg": round(math.degrees(c.angle(s)), 1)}))
