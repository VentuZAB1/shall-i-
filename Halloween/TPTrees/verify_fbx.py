# Fresh-import check of the exported FBX files (what the reviewer / Studio importer sees).
# blender.exe -b --factory-startup --python verify_fbx.py -- C:\cdimp\Halloween_TPTree.fbx [more.fbx]
import sys, json
import bpy
import numpy as np

paths = sys.argv[sys.argv.index("--") + 1:]
out = {}
for path in paths:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=path)
    rep = {"objects": {}}
    allv = []
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        me = o.data
        me.calc_loop_triangles()
        mw = o.matrix_world
        V = np.array([tuple(mw @ v.co) for v in me.vertices])
        allv.append(V)
        mats = []
        for m in me.materials:
            imgs = []
            if m and m.use_nodes:
                for n in m.node_tree.nodes:
                    if n.type == "TEX_IMAGE" and n.image:
                        links = [l.to_socket.name for l in m.node_tree.links if l.from_node == n]
                        imgs.append(dict(image=n.image.name, size=list(n.image.size), to=links,
                                         packed=bool(n.image.packed_file), file=n.image.filepath))
            mats.append(dict(name=m.name if m else None, textures=imgs))
        rep["objects"][o.name] = dict(tris=len(me.loop_triangles), verts=len(me.vertices), uv_layers=len(me.uv_layers),
                                      location=[round(x, 4) for x in o.location], rot=[round(x, 3) for x in o.rotation_euler],
                                      scale=[round(x, 4) for x in o.scale],
                                      bbox_min=[round(float(x), 3) for x in V.min(0)],
                                      bbox_max=[round(float(x), 3) for x in V.max(0)], materials=mats)
    V = np.vstack(allv)
    mn, mx = V.min(0), V.max(0)
    rep["total_tris"] = sum(v["tris"] for v in rep["objects"].values())
    rep["bbox_blender_min"] = [round(float(x), 3) for x in mn]
    rep["bbox_blender_max"] = [round(float(x), 3) for x in mx]
    rep["size_roblox_XYZ"] = [round(float(mx[0] - mn[0]), 2), round(float(mx[2] - mn[2]), 2),
                              round(float(mx[1] - mn[1]), 2)]
    out[path] = rep
print("VERIFY " + json.dumps(out, indent=1))
