import bpy, sys, json
out = {}
for nm in ("Garland_Long", "Garland_Short", "Garland_Hook"):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=rf"C:\cdimp\Halloween_{nm}.fbx")
    obs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    r = []
    for o in obs:
        me = o.data
        dims = [round(v, 3) for v in o.dimensions]
        mats = []
        for m in me.materials:
            texs = [n.image.name + f" {n.image.size[0]}x{n.image.size[1]} packed={bool(n.image.packed_file)}" for n in m.node_tree.nodes if n.type == "TEX_IMAGE" and n.image]
            mats.append((m.name, texs))
        tris = sum(len(p.vertices) - 2 for p in me.polygons)
        r.append(dict(name=o.name, tris=tris, dims=dims, loc=[round(v, 3) for v in o.location], rot=[round(v, 3) for v in o.rotation_euler], scale=[round(v, 3) for v in o.scale], uvs=len(me.uv_layers), mats=mats))
    out[nm] = r
print("VERIFY " + json.dumps(out, indent=1))
