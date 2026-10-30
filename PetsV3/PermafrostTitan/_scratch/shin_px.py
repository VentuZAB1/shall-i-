# blender -b --factory-startup --python PermafrostTitan/_scratch/shin_px.py -- <Name> <frame> [res=700]
# act_kneelrise on the fixed game camera (aimed at rest): the kneeling shin's on-screen length (knee joint -> ankle
# joint, px) and the angle between the shin and the camera view line (90 = fully side-on), + the knee / ankle z
import sys, runpy, json, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name, fr = argv[0], int(argv[1])
opts = dict(a.split("=", 1) for a in argv[2:] if "=" in a)
res = int(opts.get("res", "700"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from bpy_extras.object_utils import world_to_camera_view
pk = R3["pk"]
R3["full"](name, save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
k.set_action("act_kneelrise")
sc.frame_set(0)
loc, tgt = pk.camera_for(k, "game")
pk.aim(sc.camera, loc, tgt)
sc.frame_set(fr)
bpy.context.view_layer.update()
arm = k.arm
K = arm.matrix_world @ arm.pose.bones["Shin_L"].head
A = arm.matrix_world @ arm.pose.bones["Foot_L"].head


def px(p):
    c = world_to_camera_view(sc, sc.camera, p)
    return Vector((c.x * res, (1 - c.y) * res))


view = (K - sc.camera.matrix_world.to_translation()).normalized()
sh = (A - K).normalized()
print("SHINPX " + json.dumps({"f": fr, "shin_px": round((px(A) - px(K)).length, 1),
                              "shin_vs_view_deg": round(math.degrees(math.acos(abs(sh.dot(view)))), 1),
                              "knee_z": round(K.z, 3), "ankle": [round(v, 3) for v in A]}))
