import bpy, numpy as np, sys
bpy.ops.wm.open_mainfile(filepath=sys.argv[sys.argv.index("--") + 1])
ob = bpy.data.objects["Shell_hi"]
me = ob.data
for nm in ("Col", "Rough", "Depth"):
    a = me.color_attributes.get(nm)
    if a is None:
        print(nm, "missing"); continue
    arr = np.empty(len(a.data) * 4, np.float32); a.data.foreach_get("color", arr); arr = arr.reshape(-1, 4)
    zero = (arr[:, :3].sum(1) == 0)
    print(nm, a.domain, a.data_type, "n", len(arr), "all-zero rgb", zero.sum(), "alpha0", (arr[:, 3] == 0).sum(),
          "unique depth vals" if nm == "Depth" else "", np.unique(arr[:, 0].round(2))[:10] if nm == "Depth" else "")
