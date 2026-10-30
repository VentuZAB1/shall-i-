import bpy, numpy as np, os, json
out = {}
for n in ("Grave_A", "Grave_B", "Grave_C"):
    bpy.ops.wm.open_mainfile(filepath=os.path.join(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\Graveyard", n + ".blend"))
    h = bpy.data.objects[n + "_hi"]
    co = np.array([v.co for v in h.data.vertices])
    up = co[co[:, 2] > 0.0]
    out[n] = dict(stone_min=[round(float(v), 3) for v in up.min(0)], stone_max=[round(float(v), 3) for v in up.max(0)],
                  stone_size=[round(float(v), 3) for v in up.max(0) - up.min(0)], hi_tris=sum(len(p.vertices) - 2 for p in h.data.polygons))
print("SB " + json.dumps(out))
