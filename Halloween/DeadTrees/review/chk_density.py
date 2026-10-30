import bpy, sys, numpy as np
fbx = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=fbx)
for o in bpy.context.scene.objects:
    if o.type != "MESH" or not o.name.endswith("_Trunk"):
        continue
    me = o.data; me.calc_loop_triangles()
    mw = o.matrix_world * 100 if False else None
    vs = np.array([(o.matrix_world @ v.co) * 100 for v in me.vertices])
    tris = np.array([t.vertices[:] for t in me.loop_triangles]); tl = np.array([t.loops[:] for t in me.loop_triangles])
    uv = np.zeros(len(me.loops) * 2, dtype=np.float32); me.uv_layers.active.data.foreach_get("uv", uv); uv = uv.reshape(-1, 2)
    P = vs[tris]; U = uv[tl]
    a3 = 0.5 * np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1)
    au = 0.5 * np.abs(np.cross(U[:, 1] - U[:, 0], U[:, 2] - U[:, 0]))
    dens = np.sqrt(au / np.maximum(a3, 1e-9)) * 1024
    n = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-12
    low = dens < 30
    c = P.mean(1)
    print("CHK", o.name, "low-density tris", int(low.sum()), "area", round(float(a3[low].sum()), 2), "of", round(float(a3.sum()), 2))
    print("CHK  centroid z range", round(float(c[low, 2].min()), 3), round(float(c[low, 2].max()), 3), "mean normal z", round(float(n[low, 2].mean()), 3))
