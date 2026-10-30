import bpy, sys, numpy as np
for blend, names in (("thorn.blend", ["Bush", "Web", "WebSilk"]), ("autumn.blend", ["Bush", "Gourds"]), ("bramble.blend", ["Bramble"])):
    bpy.ops.wm.open_mainfile(filepath=blend)
    for n in names:
        o = bpy.data.objects[n]
        a = np.array([v.co[:] for v in o.data.vertices])
        mn, mx = a.min(0), a.max(0)
        c = (mn + mx) / 2
        s = mx - mn
        print("PART", blend, n, "tris", sum(len(p.vertices) - 2 for p in o.data.polygons),
              "sizeRbx", [round(s[0], 3), round(s[2], 3), round(s[1], 3)],
              "centreRbx", [round(c[0], 3), round(c[2], 3), round(-c[1], 3)], "minZ", round(mn[2], 3))
