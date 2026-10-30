# (builder D scratch) top surface z of the body (Chest / Spine / Neck vertices) near given (x, y) points
import sys, runpy, json
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
m = R3["spec"]("EclipseSeraph")
k = R3["new_pet"](m, "EclipseSeraph")
m.model(k)
m.rig(k)
k.build_rig()
names = {g.index: g.name for g in k.main.vertex_groups}
vs = [(v.co, names[max(v.groups, key=lambda g: g.weight).group] if v.groups else "") for v in k.main.data.vertices]
out = {}
for x, y in ((0.22, -0.20), (0.22, -0.12), (0.22, -0.05), (0.22, 0.02), (0.24, 0.06), (0.15, -0.05), (0.10, -0.05)):
    zs = [c.z for c, g in vs if g in ("Chest", "Spine") and abs(c.x - x) < 0.04 and abs(c.y - y) < 0.04]
    out["%.2f,%.2f" % (x, y)] = round(max(zs), 3) if zs else None
print("SURF " + json.dumps(out))
