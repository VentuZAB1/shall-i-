# r10: print the kneeling leg chain (hip / knee / ankle / toe-tip) at f40 + the bone lengths, to see why the drop
# hardly lowers the knee with tucked toes
import sys, runpy, json
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"]("PermafrostTitan", save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
k.set_action("act_kneelrise")
sc.frame_set(40)
A = k.arm
P = {b: A.matrix_world @ A.pose.bones[b].head for b in ("Leg_L", "Shin_L", "Foot_L")}
P["foot_tail"] = A.matrix_world @ A.pose.bones["Foot_L"].tail
r = lambda v: [round(x, 3) for x in v]
L1 = (k.J["Shin_L"] - k.J["Leg_L"]).length
L2 = (k.J["Foot_L"] - k.J["Shin_L"]).length
print("CHAIN " + json.dumps({b: r(v) for b, v in P.items()}) + " L1 %.3f L2 %.3f hip-ankle %.3f" % (L1, L2, (P["Foot_L"] - P["Leg_L"]).length)
      + " rest " + json.dumps({b: r(k.J[b]) for b in ("Leg_L", "Shin_L", "Foot_L")}))
