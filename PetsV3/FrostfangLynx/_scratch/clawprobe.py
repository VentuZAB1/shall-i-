# probe the front claw bone directions at a frame (review 3 M2 check)
import sys, runpy, math
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"]("FrostfangLynx", save=False)
k = R3["STATE"]["k"]
import bpy
k.set_action("act_clawflex")
for f in (0, 50):
    bpy.context.scene.frame_set(f)
    for j in range(1, 5):
        pb = k.arm.pose.bones["Claw_FL%d" % j]
        m = pb.matrix
        d = (m[0][1], m[1][1], m[2][1])
        print("PROBE", f, pb.name, tuple(round(x, 3) for x in d), tuple(round(x, 3) for x in pb.head))
    vg = [g.name for g in k.main.vertex_groups if g.name.startswith("Claw")]
    print("PROBE vgroups", vg)
