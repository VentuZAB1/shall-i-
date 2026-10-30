import bpy, sys
bpy.ops.wm.open_mainfile(filepath=sys.argv[sys.argv.index("--") + 1])
for o in bpy.data.objects:
    if o.type != "MESH":
        continue
    me = o.data
    low = [(o.matrix_world @ v.co) for v in me.vertices]
    low = [p for p in low if p.z < -0.2]
    if low:
        print("LOW", o.name, len(low), "min z %.3f" % min(p.z for p in low))
        for p in sorted(low, key=lambda p: p.z)[:8]:
            print("   %.3f %.3f %.3f" % tuple(p))
