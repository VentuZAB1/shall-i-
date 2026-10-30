# blender -b --factory-startup --python EclipseSeraph/_scratch/side_check.py -- [view=game]
# (builder D scratch) which wing side is NEAR / FAR for the view camera, and its image side (screen x)
import sys, runpy
argv = sys.argv[sys.argv.index("--") + 1:]
view = argv[0] if argv else "game"
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
name = "EclipseSeraph"
m = R3["spec"](name); k = R3["new_pet"](m, name); m.model(k); m.rig(k); k.build_rig()
pk = R3["pk"]
k.new_action("rest", 2, False)
for f in (0, 2):
    m.wset(k, f, m.DISPLAY_POSE)
k.finish(loop=False)
pk.stage(k)
k.set_action("rest"); bpy.context.scene.frame_set(0)
cam, tgt = pk.camera_for(k, view)
fwd = (tgt - cam).normalized(); right = fwd.cross((0, 0, 1)).normalized()
arm = k.arm
for b in ("Wing_A_L", "Wing_A_R", "WingTip_A_L", "WingTip_A_R"):
    pb = arm.pose.bones[b]
    p = arm.matrix_world @ pb.tail
    print("SIDE", view, b, "dist %.3f" % (p - cam).length, "screen_x %+.3f" % (p - cam).dot(right), "world", tuple(round(c, 2) for c in p))
