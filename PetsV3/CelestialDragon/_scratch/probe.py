# blender -b --python probe.py -- <Name> <clip> <f,f,...> "<bone>:x,y,z;<bone>:x,y,z;..."
# full build + anim, prints the world position of rest points carried by bones at the given frames
import sys, runpy
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip = argv[0], argv[1]
frames = [int(x) for x in argv[2].split(",")]
pts = []
for tok in argv[3].split(";"):
    b, p = tok.split(":")
    pts.append((b, Vector([float(v) for v in p.split(",")])))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
m = R3["spec"](name)
k = R3["new_pet"](m, name)
m.model(k)
m.rig(k)
k.build_rig()
if len(argv) > 4:
    exec(argv[4], {'m': m, 'Vector': Vector})
m.anim(k)
k.set_action(clip)
arm = k.arm
for f in frames:
    bpy.context.scene.frame_set(f)
    out = []
    for b, p in pts:
        pb = arm.pose.bones[b]
        M = arm.matrix_world @ pb.matrix @ arm.data.bones[b].matrix_local.inverted()
        q = M @ p
        out.append("%s(%.3f,%.3f,%.3f)" % (b, q.x, q.y, q.z))
    print("HEADLESS_RESULT f%d " % f + " ".join(out))
