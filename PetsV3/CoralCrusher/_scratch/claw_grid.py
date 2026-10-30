# blender -b --factory-startup --python CoralCrusher/_scratch/claw_grid.py
# keys the R claw on a temp action over a grid of (lift, spread, fore) and prints the pincer-tip world position per
# pose (the act's stand-tall body pose is applied), to pick a wave top (high + out) and a trough (low + in front)
import sys, runpy, json, itertools
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"]("CoralCrusher", save=False)
k, m = R3["STATE"]["k"], R3["STATE"]["m"]
grid = list(itertools.product((0, 20, 35, 50, 65), (0, 30, 60, 90), (-30, -10, 10, 30)))
k.new_action("probe", len(grid), False)
for i, (l, s, fo) in enumerate(grid):
    m.body(k, i, up=0.10, pitch=-5, roll=-2)
    m.claw(k, i, "R", lift=l, spread=s, fore=fo, wrist=-10, pinch=10)
k.bake_bezier_now()
arm = k.arm
res = []
for i, g in enumerate(grid):
    bpy.context.scene.frame_set(i)
    t = arm.matrix_world @ arm.pose.bones["Pincer_R"].tail
    e = arm.matrix_world @ arm.pose.bones["Fore_R"].head
    res.append([g, [round(c, 2) for c in t], [round(c, 2) for c in e]])
print("GRID " + json.dumps(res))
