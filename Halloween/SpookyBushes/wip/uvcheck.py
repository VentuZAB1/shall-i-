import bpy, sys, numpy as np
bpy.ops.wm.open_mainfile(filepath=sys.argv[sys.argv.index("--") + 1])
for name in sys.argv[sys.argv.index("--") + 2:]:
    ob = bpy.data.objects[name]
    me = ob.data
    uv = me.uv_layers.active.data
    tot = 0.0
    mn = np.array([9.0, 9.0]); mx = np.array([-9.0, -9.0])
    for p in me.polygons:
        pts = np.array([uv[li].uv[:] for li in p.loop_indices])
        mn = np.minimum(mn, pts.min(0)); mx = np.maximum(mx, pts.max(0))
        a = 0.0
        for k in range(1, len(pts) - 1):
            d1, d2 = pts[k] - pts[0], pts[k + 1] - pts[0]
            a += 0.5 * abs(d1[0] * d2[1] - d1[1] * d2[0])
        tot += a
    print("UVCHECK", name, "uv area sum", round(tot, 3), "bounds", mn.round(3), mx.round(3), "faces", len(me.polygons))
