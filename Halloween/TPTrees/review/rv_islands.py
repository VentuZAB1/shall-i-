import bpy, sys, numpy as np
argv = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=argv[0])
o = bpy.data.objects[argv[1]]; me = o.data
V = np.array([v.co[:] for v in me.vertices]); n = len(V); par = list(range(n))
def f(x):
    while par[x] != x:
        par[x] = par[par[x]]; x = par[x]
    return x
for e in me.edges:
    a, b = f(e.vertices[0]), f(e.vertices[1])
    if a != b: par[a] = b
r = np.array([f(i) for i in range(n)])
for k in np.unique(r):
    P = V[r == k]
    print("RV_ISL", argv[1], len(P), P.min(0).round(2), P.max(0).round(2))
