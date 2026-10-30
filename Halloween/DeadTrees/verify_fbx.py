# Re-import an exported FBX in a clean scene and report what Roblox will get: objects, triangles, size (studs),
# lowest point, materials + their textures (and whether they are embedded).
#   blender.exe -b --factory-startup --python verify_fbx.py -- C:\cdimp\Halloween_DeadTree.fbx
import bpy, sys, json, os
import numpy as np

path = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=path)
out = {"fbx": path, "kb": round(os.path.getsize(path) / 1024, 1), "objects": []}
allv = []
for o in bpy.context.scene.objects:
    if o.type != "MESH":
        continue
    me = o.data
    vs = np.array([o.matrix_world @ v.co for v in me.vertices])
    allv.append(vs)
    mats = []
    for m in me.materials:
        texs = []
        if m and m.node_tree:
            for n in m.node_tree.nodes:
                if n.type == "TEX_IMAGE" and n.image:
                    links = [l.to_socket.name for l in m.node_tree.links if l.from_node == n]
                    texs.append(dict(image=n.image.name, size=list(n.image.size), packed=bool(n.image.packed_file),
                                     channels=n.image.channels, to=links))
        mats.append(dict(name=m.name if m else None, textures=texs))
    out["objects"].append(dict(name=o.name, tris=sum(len(p.vertices) - 2 for p in me.polygons),
                               size_xyz=[round(float(v), 3) for v in vs.max(0) - vs.min(0)],
                               min=[round(float(v), 3) for v in vs.min(0)], max=[round(float(v), 3) for v in vs.max(0)],
                               uv_layers=len(me.uv_layers), materials=mats))
V = np.concatenate(allv)
out["total_tris"] = sum(o["tris"] for o in out["objects"])
out["bbox_min"] = [round(float(v), 3) for v in V.min(0)]
out["bbox_max"] = [round(float(v), 3) for v in V.max(0)]
print("VERIFY " + json.dumps(out, indent=1))
