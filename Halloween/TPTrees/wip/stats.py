import bpy, numpy as np, sys, json
out = {}
for blend in ("tptree.blend", "tpbush.blend"):
    bpy.ops.wm.open_mainfile(filepath=r"C:/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/Halloween/TPTrees/" + blend)
    r = {}
    for o in bpy.data.objects:
        if o.type == "MESH" and not o.hide_render:
            V = np.array([tuple(o.matrix_world @ v.co) for v in o.data.vertices])
            r[o.name] = [V.min(0).round(3).tolist(), V.max(0).round(3).tolist()]
    out[blend] = r
for name in ("TPTree_CanopyA", "TPTree_CanopyB", "TPBush_Canopy", "TPTree_TP", "TPBush_TP", "TPTree_Trunk"):
    st = {}
    for k in ("albedo", "normal", "rough"):
        img = bpy.data.images.load(r"C:/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/Halloween/TPTrees/maps/%s_%s.png" % (name, k))
        a = np.empty(img.size[0] * img.size[1] * 4, np.float32)
        img.pixels.foreach_get(a)
        a = a.reshape(-1, 4)
        if k == "albedo":
            # sRGB-encoded png read as sRGB -> pixels are linear floats? use luma of stored values
            l = 0.2126 * a[:, 0] + 0.7152 * a[:, 1] + 0.0722 * a[:, 2]
            st["luma_lt_0.10_pct"] = round(float((l < 0.10).mean() * 100), 2)
            st["luma_mean"] = round(float(l.mean()), 3)
        elif k == "normal":
            st["inverted_pct"] = round(float((a[:, 2] < 0.5).mean() * 100), 3)
        else:
            st["rough_mean"] = round(float(a[:, 0].mean()), 3)
    out[name] = st
print("STATS " + json.dumps(out))
