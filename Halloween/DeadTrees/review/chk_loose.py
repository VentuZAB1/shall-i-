import bpy, bmesh, sys, numpy as np
fbx = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=fbx)
for o in sorted([o for o in bpy.context.scene.objects if o.type == "MESH"], key=lambda o: o.name):
    if not o.name.endswith(("_Trunk", "_Limbs")):
        continue
    bm = bmesh.new(); bm.from_mesh(o.data)
    for v in bm.verts: v.co = (o.matrix_world @ v.co) * 100.0
    seen = set(); parts = []
    for f in bm.faces:
        if f.index in seen: continue
        stack = [f]; comp = []
        seen.add(f.index)
        while stack:
            g = stack.pop(); comp.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen:
                        seen.add(h.index); stack.append(h)
        parts.append(comp)
    parts.sort(key=len, reverse=True)
    print("LOOSE", o.name, "parts", len(parts), "sizes", [len(p) for p in parts[:12]])
    for p in parts[1:]:
        vs = np.array([v.co[:] for f in p for v in f.verts])
        c = vs.mean(0); ext = vs.max(0) - vs.min(0)
        area = sum(f.calc_area() for f in p)
        print("LOOSE    faces %d area %.4f centre blender (%.2f, %.2f, %.2f) extent (%.2f, %.2f, %.2f) roblox (%.2f, %.2f, %.2f)" % (len(p), area, c[0], c[1], c[2], ext[0], ext[1], ext[2], c[0], c[2], -c[1]))
    bm.free()
