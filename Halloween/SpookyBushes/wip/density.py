import bpy, sys, numpy as np
bpy.ops.wm.open_mainfile(filepath=sys.argv[sys.argv.index("--") + 1])
ob = bpy.data.objects["Bush"]; me = ob.data; uv = me.uv_layers.active.data
nb = int(sys.argv[sys.argv.index("--") + 2])
def ratios(rng_):
    a3 = au = 0.0
    for i in rng_:
        p = me.polygons[i]
        a3 += p.area
        pts = np.array([uv[li].uv[:] for li in p.loop_indices])
        for k in range(1, len(pts) - 1):
            d1, d2 = pts[k] - pts[0], pts[k + 1] - pts[0]
            au += 0.5 * abs(d1[0] * d2[1] - d1[1] * d2[0])
    return a3, au, au / max(a3, 1e-9)
n = len(me.polygons)
print("DENS body", [round(x, 5) for x in ratios(range(nb))])
print("DENS rest", [round(x, 5) for x in ratios(range(nb, n))])
