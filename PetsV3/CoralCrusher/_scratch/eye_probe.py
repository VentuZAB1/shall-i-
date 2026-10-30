# blender -b --factory-startup --python CoralCrusher/_scratch/eye_probe.py -- <Name> <clip> <f,f,...>
# For each frame: the angle (deg) between each eyestalk's facing and the direction from the eye to the crusher tip
# (Claw_Tip_R), plus the Spine roll (deg). Tracking works if the angle shrinks at the wave tops.
import sys, runpy, json, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, frames = argv[0], argv[1], [int(v) for v in argv[2].split(",")]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
k.set_action(clip)
arm = k.arm
sc = bpy.context.scene
out = {}
for f in frames:
    sc.frame_set(f)
    bpy.context.view_layer.update()
    tip = arm.matrix_world @ arm.pose.bones["Claw_Tip_R"].head
    row = {}
    for e in ("Eye_L", "Eye_R"):
        pb = arm.pose.bones[e]
        m = arm.matrix_world @ pb.matrix
        h = m.to_translation()
        fwd = (m.to_3x3() @ Vector((0, 1, 0))).normalized()            # the stalk direction (bone Y; leans forward)
        to = (tip - h)
        to.z = 0.0
        f2 = fwd.copy()
        f2.z = 0.0
        row[e] = round(math.degrees(f2.angle(to)), 1)
        row[e + "_heading"] = round(math.degrees(math.atan2(f2.x, -f2.y)), 1)     # world heading of the stalk (deg)
    zl = (arm.matrix_world @ arm.pose.bones["Arm_L"].head).z
    zr = (arm.matrix_world @ arm.pose.bones["Arm_R"].head).z
    row["shoulder_zR_minus_zL"] = round(zr - zl, 4)               # < rest value = the crusher side dips
    out[f] = row
print("EYE_RESULT " + json.dumps(out))
