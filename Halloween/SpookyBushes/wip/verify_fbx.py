import bpy, sys, numpy as np
for path in sys.argv[sys.argv.index("--") + 1:]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=path)
    print("FBX", path)
    allv = []
    for o in bpy.context.scene.objects:
        if o.type != "MESH":
            print("  non-mesh", o.name, o.type); continue
        me = o.data
        tris = sum(len(p.vertices) - 2 for p in me.polygons)
        co = np.array([o.matrix_world @ v.co for v in me.vertices])
        allv.append(co)
        mats = []
        for m in me.materials:
            imgs = []
            if m and m.use_nodes:
                for n in m.node_tree.nodes:
                    if n.type == "TEX_IMAGE" and n.image:
                        im = n.image
                        links = [l.to_socket.name for l in m.node_tree.links if l.from_node == n]
                        imgs.append((im.name, tuple(im.size), bool(im.packed_file), im.alpha_mode, links))
            mats.append((m.name if m else None, imgs))
        print("  obj", o.name, "tris", tris, "loc", tuple(round(x, 4) for x in o.location), "scale", tuple(round(x, 4) for x in o.scale),
              "uv layers", [u.name for u in me.uv_layers], "colattrs", [a.name for a in me.color_attributes])
        for mm in mats:
            print("    mat", mm)
    a = np.concatenate(allv)
    mn, mx = a.min(0), a.max(0)
    print("  world bbox min", mn.round(4), "max", mx.round(4), "size", (mx - mn).round(4))
